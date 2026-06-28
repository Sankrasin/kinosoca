# script to fetch where you can watch movies (like netflix, prime, etc)
# fetches data for all movies in the db
import argparse
import time

from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.services.tmdb_client import tmdb_client
from app.models.movie import Movie
from app.models.watch_provider import WatchProvider, MovieWatchProvider, AccessType

REQUEST_DELAY_SECONDS = 0.25

# map tmdb keys to our enums
ACCESS_TYPE_KEY_MAP = {
    "flatrate": AccessType.flatrate,
    "rent": AccessType.rent,
    "buy": AccessType.buy,
}


def upsert_provider(db: Session, provider_data: dict, cache: dict[int, WatchProvider]) -> WatchProvider:
    provider_id = provider_data["provider_id"]
    if provider_id in cache:
        return cache[provider_id]

    provider = db.query(WatchProvider).filter(WatchProvider.id == provider_id).first()
    if provider is None:
        provider = WatchProvider(
            id=provider_id,
            name=provider_data["provider_name"],
            logo_path=provider_data.get("logo_path"),
        )
        db.add(provider)
    else:
        provider.name = provider_data["provider_name"]
        provider.logo_path = provider_data.get("logo_path")

    cache[provider_id] = provider
    return provider


def sync_providers_for_movie(
    db: Session,
    movie: Movie,
    country_codes: list[str],
    provider_cache: dict[int, WatchProvider],
) -> int:
    try:
        data = tmdb_client.get_movie_watch_providers(movie.id)
    except Exception as exc:
        print(f"  Skipping movie {movie.id} due to fetch error: {exc}")
        return 0

    results_by_country = data.get("results", {})

    # clear old links so we don't duplicate
    db.query(MovieWatchProvider).filter(MovieWatchProvider.movie_id == movie.id).delete()

    links_created = 0
    for country_code in country_codes:
        country_data = results_by_country.get(country_code)
        if not country_data:
            continue

        provider_page_url = country_data.get("link")

        for access_key, access_enum in ACCESS_TYPE_KEY_MAP.items():
            for provider_data in country_data.get(access_key, []):
                provider = upsert_provider(db, provider_data, provider_cache)
                link = MovieWatchProvider(
                    movie_id=movie.id,
                    provider_id=provider.id,
                    country_code=country_code,
                    access_type=access_enum,
                    provider_url=provider_page_url,
                )
                db.add(link)
                links_created += 1

    return links_created


def run_provider_sync(country_codes: list[str]) -> None:
    db = SessionLocal()
    try:
        movies = db.query(Movie).all()
        print(f"Syncing watch providers for {len(movies)} movies across {country_codes}...\n")

        provider_cache: dict[int, WatchProvider] = {}
        total_links = 0

        for idx, movie in enumerate(movies, start=1):
            links_created = sync_providers_for_movie(db, movie, country_codes, provider_cache)
            total_links += links_created
            db.commit()

            if idx % 25 == 0 or idx == len(movies):
                print(f"  [{idx}/{len(movies)}] processed — {total_links} provider links so far")

            time.sleep(REQUEST_DELAY_SECONDS)

        print(f"\nProvider sync complete. {total_links} total provider links created.")
    finally:
        db.close()
        tmdb_client.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sync OTT watch providers from TMDB.")
    parser.add_argument(
        "--countries",
        nargs="+",
        default=["IN", "US"],
        help="ISO country codes to sync provider availability for",
    )
    args = parser.parse_args()

    run_provider_sync(country_codes=args.countries)