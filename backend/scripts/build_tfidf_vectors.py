# script to build the tfidf matrix so we can find similar movies fast
from app.database import SessionLocal
from app.ml.tfidf_engine import build_and_persist


def main() -> None:
    db = SessionLocal()
    try:
        print("Building TF-IDF matrix from current movie catalog...")
        build_and_persist(db)
        print("Done! Cached matrix is ready to go.")
    finally:
        db.close()


if __name__ == "__main__":
    main()