# script to create embeddings for all movies and save to db
# run this when you add new movies
import sys
from pathlib import Path

# add backend dir so imports work
backend_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(backend_dir))

from sqlalchemy.orm import Session, joinedload
from app.database import SessionLocal
from app.models.movie import Movie
from app.models.embedding import MovieEmbedding
from app.ml.semantic_engine import semantic_engine

BATCH_COMMIT_SIZE = 50


def run_embedding_build(db: Session) -> None:
    movies = (
        db.query(Movie)
        .options(joinedload(Movie.genres), joinedload(Movie.keywords))
        .all()
    )
    print(f"Computing semantic embeddings for {len(movies)} movies...")

    for idx, movie in enumerate(movies, start=1):
        vector = semantic_engine.encode_movie(movie)

        # save vector to db
        embedding_row = (
            db.query(MovieEmbedding).filter(MovieEmbedding.movie_id == movie.id).first()
        )
        if embedding_row is None:
            embedding_row = MovieEmbedding(movie_id=movie.id, semantic_embedding=vector)
            db.add(embedding_row)
        else:
            embedding_row.semantic_embedding = vector

        # commit in batches so we dont crash
        if idx % BATCH_COMMIT_SIZE == 0:
            db.commit()
            print(f"  [{idx}/{len(movies)}] embeddings committed")

    db.commit()
    print(f"  [{len(movies)}/{len(movies)}] embeddings committed")
    print("Done! Semantics search should work now.")


def main() -> None:
    db = SessionLocal()
    try:
        run_embedding_build(db)
    finally:
        db.close()


if __name__ == "__main__":
    main()