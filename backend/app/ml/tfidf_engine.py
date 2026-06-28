# text matching engine using tf-idf to find similar movies
import os
import json

import numpy as np
import joblib
from scipy import sparse
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sqlalchemy.orm import Session, joinedload

from app.models.movie import Movie

CACHE_DIR = os.path.join(os.path.dirname(__file__), "cache")
MATRIX_PATH = os.path.join(CACHE_DIR, "tfidf_matrix.npz")
VECTORIZER_PATH = os.path.join(CACHE_DIR, "tfidf_vectorizer.joblib")
MOVIE_IDS_PATH = os.path.join(CACHE_DIR, "tfidf_movie_ids.json")


def _build_document(movie: Movie) -> str:
    # combine all text for a movie and repeat important stuff so it gets weighted higher
    overview = movie.overview or ""
    genre_tokens = " ".join(g.name for g in movie.genres) * 3
    keyword_tokens = " ".join(k.name for k in movie.keywords) * 2
    cast_tokens = " ".join(p.name.replace(" ", "") for p in movie.cast[:5])
    director_tokens = " ".join(
        p.name.replace(" ", "") for p in movie.crew
    ) * 2

    return " ".join([overview, genre_tokens, keyword_tokens, cast_tokens, director_tokens])


def build_corpus_from_db(db: Session) -> tuple[list[int], list[str]]:
    movies = (
        db.query(Movie)
        .options(
            joinedload(Movie.genres),
            joinedload(Movie.keywords),
            joinedload(Movie.cast),
            joinedload(Movie.crew),
        )
        .all()
    )
    movie_ids = [m.id for m in movies]
    documents = [_build_document(m) for m in movies]
    return movie_ids, documents


def build_and_persist(db: Session) -> None:
    os.makedirs(CACHE_DIR, exist_ok=True)

    movie_ids, documents = build_corpus_from_db(db)

    vectorizer = TfidfVectorizer(
        max_features=20000,
        stop_words="english",
        ngram_range=(1, 2),
        min_df=2,
    )
    matrix = vectorizer.fit_transform(documents)

    sparse.save_npz(MATRIX_PATH, matrix)
    joblib.dump(vectorizer, VECTORIZER_PATH)
    with open(MOVIE_IDS_PATH, "w") as f:
        json.dump(movie_ids, f)

    print(f"TF-IDF matrix built: {matrix.shape[0]} movies, {matrix.shape[1]} features")


class TFIDFEngine:
    def __init__(self):
        self.matrix = None
        self.movie_ids: list[int] = []
        self.id_to_index: dict[int, int] = {}
        self.loaded = False

    def load_cached(self) -> bool:
        if not (os.path.exists(MATRIX_PATH) and os.path.exists(MOVIE_IDS_PATH)):
            self.loaded = False
            return False

        self.matrix = sparse.load_npz(MATRIX_PATH)
        with open(MOVIE_IDS_PATH) as f:
            self.movie_ids = json.load(f)
        self.id_to_index = {mid: idx for idx, mid in enumerate(self.movie_ids)}
        self.loaded = True
        return True

    def get_similar_movie_ids(self, movie_id: int, top_n: int = 12) -> list[tuple[int, float]]:
        # get most similar movies from matrix
        if not self.loaded or movie_id not in self.id_to_index:
            return []

        idx = self.id_to_index[movie_id]
        target_vector = self.matrix[idx]
        similarities = cosine_similarity(target_vector, self.matrix).flatten()

        ranked_indices = np.argsort(similarities)[::-1]

        results = []
        for ranked_idx in ranked_indices:
            candidate_id = self.movie_ids[ranked_idx]
            if candidate_id == movie_id:
                continue
            results.append((candidate_id, float(similarities[ranked_idx])))
            if len(results) >= top_n:
                break

        return results

    def get_score(self, movie_id_a: int, movie_id_b: int) -> float:
        if not self.loaded or movie_id_a not in self.id_to_index or movie_id_b not in self.id_to_index:
            return 0.0
        idx_a = self.id_to_index[movie_id_a]
        idx_b = self.id_to_index[movie_id_b]
        score = cosine_similarity(self.matrix[idx_a], self.matrix[idx_b])
        return float(score[0][0])


tfidf_engine = TFIDFEngine()