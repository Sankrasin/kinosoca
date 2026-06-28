# engine for semantic search using sentence transformers
# converts text to vectors and uses pgvector to find similar ones
from sentence_transformers import SentenceTransformer
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.movie import Movie
from app.models.embedding import MovieEmbedding

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


def _build_movie_text(movie: Movie) -> str:
    # make a string to feed to the ai model
    genre_names = ", ".join(g.name for g in movie.genres)
    keyword_names = ", ".join(k.name for k in movie.keywords)
    overview = movie.overview or ""
    return f"{movie.title}. {overview} Genres: {genre_names}. Themes: {keyword_names}."


class SemanticEngine:
    def __init__(self):
        self._model: SentenceTransformer | None = None

    def _ensure_model_loaded(self) -> SentenceTransformer:
        if self._model is None:
            self._model = SentenceTransformer(MODEL_NAME)
        return self._model

    def encode_text(self, text: str) -> list[float]:
        model = self._ensure_model_loaded()
        embedding = model.encode(text, normalize_embeddings=True)
        return embedding.tolist()

    def encode_movie(self, movie: Movie) -> list[float]:
        return self.encode_text(_build_movie_text(movie))

    def search_by_text(self, db: Session, query_text: str, top_n: int = 12) -> list[tuple[int, float]]:
        # turn search query to vector and find nearest movies in db
        query_vector = self.encode_text(query_text)

        stmt = (
            select(
                MovieEmbedding.movie_id,
                MovieEmbedding.semantic_embedding.cosine_distance(query_vector).label("distance"),
            )
            .where(MovieEmbedding.semantic_embedding.is_not(None))
            .order_by("distance")
            .limit(top_n)
        )
        rows = db.execute(stmt).all()
        return [(row.movie_id, 1.0 - float(row.distance)) for row in rows]

    def get_similar_by_movie_id(self, db: Session, movie_id: int, top_n: int = 12) -> list[tuple[int, float]]:
        # find movies similar to a specific movie
        source = db.query(MovieEmbedding).filter(MovieEmbedding.movie_id == movie_id).first()
        if source is None or source.semantic_embedding is None:
            return []

        stmt = (
            select(
                MovieEmbedding.movie_id,
                MovieEmbedding.semantic_embedding.cosine_distance(source.semantic_embedding).label("distance"),
            )
            .where(
                MovieEmbedding.semantic_embedding.is_not(None),
                MovieEmbedding.movie_id != movie_id,
            )
            .order_by("distance")
            .limit(top_n)
        )
        rows = db.execute(stmt).all()
        return [(row.movie_id, 1.0 - float(row.distance)) for row in rows]

    def get_score(self, db: Session, movie_id_a: int, movie_id_b: int) -> float:
        emb_a = db.query(MovieEmbedding).filter(MovieEmbedding.movie_id == movie_id_a).first()
        emb_b = db.query(MovieEmbedding).filter(MovieEmbedding.movie_id == movie_id_b).first()
        if emb_a is None or emb_b is None or emb_a.semantic_embedding is None or emb_b.semantic_embedding is None:
            return 0.0

        stmt = select(
            MovieEmbedding.semantic_embedding.cosine_distance(emb_b.semantic_embedding)
        ).where(MovieEmbedding.movie_id == movie_id_a)
        distance = db.execute(stmt).scalar()
        return 1.0 - float(distance) if distance is not None else 0.0


semantic_engine = SemanticEngine()