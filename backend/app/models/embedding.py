# stores precomputed vectors for movies so search is fast
from typing import TYPE_CHECKING

from sqlalchemy import Integer, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from pgvector.sqlalchemy import Vector

from app.database import Base

if TYPE_CHECKING:
    from app.models.movie import Movie

# size of the vector model we use
SEMANTIC_EMBEDDING_DIM = 384


class MovieEmbedding(Base):
    __tablename__ = "movie_embeddings"

    movie_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("movies.id", ondelete="CASCADE"), primary_key=True
    )

    # store tfidf vector as json dictionary
    tfidf_vector: Mapped[dict | None] = mapped_column(JSON, nullable=True)

    # store semantic vector using pgvector
    semantic_embedding: Mapped[list[float] | None] = mapped_column(
        Vector(SEMANTIC_EMBEDDING_DIM), nullable=True
    )

    movie: Mapped["Movie"] = relationship("Movie", back_populates="embedding")

    def __repr__(self) -> str:
        return f"<MovieEmbedding movie_id={self.movie_id}>"