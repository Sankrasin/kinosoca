# script to fetch movies from tmdb and save them to our db
# run with: python -m scripts.ingest_tmdb_data
import sys
from pathlib import Path

# add backend dir to path so imports work
backend_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(backend_dir))

import argparse
import time

from sqlalchemy.orm import Session
from sqlalchemy import delete, insert

from app.database import SessionLocal, engine, Base
from app.services.tmdb_client import tmdb_client
from app.models.movie import Movie, Keyword
from app.models.genre import Genre
from app.models.person import Person, movie_crew

REQUEST_DELAY_SECONDS = 0.25  # don't spam the api
DIRECTOR_JOB_NAME = "Director"
MAX_CAST_MEMBERS_PER_MOVIE = 15
MAX_CREW_MEMBERS_PER_MOVIE = 5  # keep only directors to save space


def sync_genres(db: Session) -> dict[int, Genre]:
    print("Syncing genre list...")
    data = tmdb_client.get_genre_list()
    genre_map: dict[int, Genre] = {}

    for genre_data in data.get("genres", []):
        genre = db.query(Genre).filter(Genre.id == genre_data["id"]).first()
        if genre is None:
            genre = Genre(id=genre_data["id"], name=genre_data["name"])
            db.add(genre)
        else:
            genre.name = genre_data["name"]
        genre_map[genre_data["id"]] = genre

    db.commit()
    print(f"Synced {len(genre_map)} genres.")
    return genre_map


def collect_movie_ids_from_listing(start_page: int, end_page: int) -> set[int]:
    movie_ids: set[int] = set()

    for page in range(start_page, end_page + 1):
        for fetch_fn in (tmdb_client.get_popular_movies, tmdb_client.get_top_rated_movies):
            data = fetch_fn(page=page)
            for result in data.get("results", []):
                movie_ids.add(result["id"])
            time.sleep(REQUEST_DELAY_SECONDS)

        trending_data = tmdb_client.get_trending_movies(time_window="week", page=page)
        for result in trending_data.get("results", []):
            movie_ids.add(result["id"])
        time.sleep(REQUEST_DELAY_SECONDS)

        print(f"Collected movie IDs through page {page}: {len(movie_ids)} total so far.")

    return movie_ids


def upsert_person(db: Session, person_data: dict, cache: dict[int, Person]) -> Person:
    person_id = person_data["id"]
    if person_id in cache:
        return cache[person_id]

    person = db.query(Person).filter(Person.id == person_id).first()
    if person is None:
        person = Person(
            id=person_id,
            name=person_data["name"],
            profile_path=person_data.get("profile_path"),
        )
        db.add(person)
    else:
        person.name = person_data["name"]
        person.profile_path = person_data.get("profile_path")

    cache[person_id] = person
    return person


def upsert_keyword(db: Session, keyword_data: dict, cache: dict[int, Keyword]) -> Keyword:
    keyword_id = keyword_data["id"]
    if keyword_id in cache:
        return cache[keyword_id]

    keyword = db.query(Keyword).filter(Keyword.id == keyword_id).first()
    if keyword is None:
        keyword = Keyword(id=keyword_id, name=keyword_data["name"])
        db.add(keyword)
    else:
        keyword.name = keyword_data["name"]

    cache[keyword_id] = keyword
    return keyword


def sync_movie(
    db: Session,
    movie_id: int,
    genre_map: dict[int, Genre],
    person_cache: dict[int, Person],
    keyword_cache: dict[int, Keyword],
) -> None:
    try:
        details = tmdb_client.get_movie_details(movie_id)
        time.sleep(REQUEST_DELAY_SECONDS)
        credits = tmdb_client.get_movie_credits(movie_id)
        time.sleep(REQUEST_DELAY_SECONDS)
        keywords_data = tmdb_client.get_movie_keywords(movie_id)
        time.sleep(REQUEST_DELAY_SECONDS)
    except Exception as exc:
        print(f"  Skipping movie {movie_id} due to fetch error: {exc}")
        return

    release_date = details.get("release_date") or ""
    release_year = int(release_date[:4]) if len(release_date) >= 4 else None

    production_countries = details.get("production_countries") or []
    country = production_countries[0]["iso_3166_1"] if production_countries else None

    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if movie is None:
        movie = Movie(id=movie_id)
        db.add(movie)

    movie.title = details.get("title", "")
    movie.original_title = details.get("original_title")
    movie.overview = details.get("overview")
    movie.release_year = release_year
    movie.runtime = details.get("runtime")
    movie.popularity = details.get("popularity", 0.0)
    movie.vote_average = details.get("vote_average", 0.0)
    movie.vote_count = details.get("vote_count", 0)
    movie.poster_path = details.get("poster_path")
    movie.backdrop_path = details.get("backdrop_path")
    movie.original_language = details.get("original_language")
    movie.country = country

    movie.genres = [
        genre_map[g["id"]] for g in details.get("genres", []) if g["id"] in genre_map
    ]

    movie.keywords = [
        upsert_keyword(db, kw, keyword_cache)
        for kw in keywords_data.get("keywords", [])
    ]

    # fix duplicate actors from tmdb
    # like if they do voice and acting in the same movie
    cast_list = credits.get("cast", [])[:MAX_CAST_MEMBERS_PER_MOVIE]
    seen_cast_ids: set[int] = set()
    deduped_cast_people = []
    for c in cast_list:
        person = upsert_person(db, c, person_cache)
        if person.id not in seen_cast_ids:
            seen_cast_ids.add(person.id)
            deduped_cast_people.append(person)
    movie.cast = deduped_cast_people

    # handle crew/directors manually because of the job column
    db.flush()

    crew_list = [
        c for c in credits.get("crew", [])
        if c.get("job") == DIRECTOR_JOB_NAME
    ][:MAX_CREW_MEMBERS_PER_MOVIE]

    # remove duplicate directors
    seen_crew_ids: set[int] = set()
    deduped_crew_people = []
    for c in crew_list:
        person = upsert_person(db, c, person_cache)
        if person.id not in seen_crew_ids:
            seen_crew_ids.add(person.id)
            deduped_crew_people.append(person)

    db.flush()  # make sure people exist before linking them

    db.execute(delete(movie_crew).where(movie_crew.c.movie_id == movie.id))

    if deduped_crew_people:
        db.execute(
            insert(movie_crew),
            [
                {"movie_id": movie.id, "person_id": person.id, "job": DIRECTOR_JOB_NAME}
                for person in deduped_crew_people
            ],
        )

    db.commit()
    print(f"  Synced: {movie.title} ({movie.release_year})")


def run_ingestion(start_page: int, end_page: int) -> None:
    Base.metadata.create_all(bind=engine)  # setup tables just in case

    db = SessionLocal()
    try:
        genre_map = sync_genres(db)

        movie_ids = collect_movie_ids_from_listing(start_page, end_page)
        print(f"\nStarting detail sync for {len(movie_ids)} movies...\n")

        person_cache: dict[int, Person] = {}
        keyword_cache: dict[int, Keyword] = {}

        for idx, movie_id in enumerate(sorted(movie_ids), start=1):
            print(f"[{idx}/{len(movie_ids)}] Movie ID {movie_id}")
            sync_movie(db, movie_id, genre_map, person_cache, keyword_cache)

        print("\nIngestion complete.")
    finally:
        db.close()
        tmdb_client.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sync movie data from TMDB into the database.")
    parser.add_argument("--start-page", type=int, default=1, help="The starting page number to pull")
    parser.add_argument("--pages", type=int, default=5, help="The ending page number to pull (inclusive)")
    args = parser.parse_args()

    run_ingestion(start_page=args.start_page, end_page=args.pages)