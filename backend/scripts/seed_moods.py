# script to add default moods and map them to genres
# run after you've pulled movies from tmdb
import sys
from pathlib import Path

# add backend dir to path so imports work
backend_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(backend_dir))

from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.genre import Genre
from app.models.watchlist import Mood, MoodGenreMapping

# mapping moods to genres with some custom weights
MOOD_GENRE_WEIGHTS: dict[str, list[tuple[str, float]]] = {
    "Happy": [
        ("Comedy", 1.0),
        ("Family", 0.7),
        ("Animation", 0.6),
        ("Music", 0.5),
    ],
    "Emotional": [
        ("Drama", 1.0),
        ("Romance", 0.7),
        ("Family", 0.4),
    ],
    "Romantic": [
        ("Romance", 1.0),
        ("Drama", 0.5),
        ("Comedy", 0.4),
    ],
    "Mind-Bending": [
        ("Science Fiction", 1.0),
        ("Mystery", 0.9),
        ("Thriller", 0.6),
    ],
    "Dark Thriller": [
        ("Thriller", 1.0),
        ("Crime", 0.8),
        ("Mystery", 0.6),
        ("Horror", 0.4),
    ],
    "Inspirational": [
        ("Drama", 0.8),
        ("History", 0.6),
        ("Family", 0.5),
        ("Documentary", 0.4),
    ],
    "Feel-Good": [
        ("Comedy", 1.0),
        ("Family", 0.8),
        ("Animation", 0.6),
        ("Romance", 0.5),
    ],
    "Action-Packed": [
        ("Action", 1.0),
        ("Adventure", 0.7),
        ("Thriller", 0.5),
    ],
    "Motivational": [
        ("Drama", 0.7),
        ("History", 0.6),
        ("Documentary", 0.6),
        ("Family", 0.4),
    ],
}


def seed_moods(db: Session) -> None:
    genre_by_name = {g.name: g for g in db.query(Genre).all()}
    if not genre_by_name:
        print(
            "No genres found in the database. Run scripts/ingest_tmdb_data.py "
            "at least once before seeding moods."
        )
        return

    moods_created = 0
    mappings_created = 0
    skipped_genre_names: set[str] = set()

    for mood_name, genre_weight_pairs in MOOD_GENRE_WEIGHTS.items():
        mood = db.query(Mood).filter(Mood.name == mood_name).first()
        if mood is None:
            mood = Mood(name=mood_name)
            db.add(mood)
            db.flush()  # need the id before mapping
            moods_created += 1

        # clear old ones so we don't get duplicates if we run this again
        db.query(MoodGenreMapping).filter(MoodGenreMapping.mood_id == mood.id).delete()

        for genre_name, weight in genre_weight_pairs:
            genre = genre_by_name.get(genre_name)
            if genre is None:
                skipped_genre_names.add(genre_name)
                continue

            mapping = MoodGenreMapping(mood_id=mood.id, genre_id=genre.id, weight=weight)
            db.add(mapping)
            mappings_created += 1

    db.commit()

    print(f"Moods created/updated: {len(MOOD_GENRE_WEIGHTS)} (new: {moods_created})")
    print(f"Mood-genre mappings created: {mappings_created}")
    if skipped_genre_names:
        print(
            f"Note: these genre names weren't found in TMDB's genre list and were skipped: "
            f"{sorted(skipped_genre_names)}"
        )


def main() -> None:
    db = SessionLocal()
    try:
        seed_moods(db)
    finally:
        db.close()


if __name__ == "__main__":
    main()