# the main movie model
# also putting keywords here since they only apply to movies anyway
from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlalchemy import String, Text, Float, Integer, DateTime, Table, Column, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.genre import movie_genres
from app.models.person import movie_cast, movie_crew

if TYPE_CHECKING:
    from app.models.genre import Genre
    from app.models.person import Person
    from app.models.watch_provider import MovieWatchProvider
    from app.models.embedding import MovieEmbedding
    from app.models.watchlist import Watchlist

# table connecting movies and keywords
movie_keywords = Table(
    "movie_keywords",
    Base.metadata,
    Column("movie_id", Integer, ForeignKey("movies.id", ondelete="CASCADE"), primary_key=True),
    Column("keyword_id", Integer, ForeignKey("keywords.id", ondelete="CASCADE"), primary_key=True),
)


class Keyword(Base):
    __tablename__ = "keywords"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)  # using tmdb keyword id
    name: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)

    movies: Mapped[list["Movie"]] = relationship(
        "Movie", secondary=movie_keywords, back_populates="keywords"
    )

    def __repr__(self) -> str:
        return f"<Keyword id={self.id} name={self.name}>"


class Movie(Base):
    __tablename__ = "movies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)  # tmdb movie id
    title: Mapped[str] = mapped_column(String(500), nullable=False, index=True)
    original_title: Mapped[str | None] = mapped_column(String(500), nullable=True)
    overview: Mapped[str | None] = mapped_column(Text, nullable=True)

    release_year: Mapped[int | None] = mapped_column(Integer, nullable=True, index=True)
    runtime: Mapped[int | None] = mapped_column(Integer, nullable=True)

    popularity: Mapped[float] = mapped_column(Float, default=0.0, index=True)
    vote_average: Mapped[float] = mapped_column(Float, default=0.0, index=True)
    vote_count: Mapped[int] = mapped_column(Integer, default=0)

    poster_path: Mapped[str | None] = mapped_column(String(255), nullable=True)
    backdrop_path: Mapped[str | None] = mapped_column(String(255), nullable=True)

    original_language: Mapped[str | None] = mapped_column(String(10), nullable=True, index=True)
    country: Mapped[str | None] = mapped_column(String(10), nullable=True, index=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # relationships to other tables
    genres: Mapped[list["Genre"]] = relationship(
        "Genre", secondary=movie_genres, back_populates="movies"
    )
    cast: Mapped[list["Person"]] = relationship(
        "Person", secondary=movie_cast, back_populates="cast_movies"
    )
    crew: Mapped[list["Person"]] = relationship(
        "Person", secondary=movie_crew, back_populates="crew_movies"
    )
    keywords: Mapped[list["Keyword"]] = relationship(
        "Keyword", secondary=movie_keywords, back_populates="movies"
    )

    watch_providers: Mapped[list["MovieWatchProvider"]] = relationship(
        "MovieWatchProvider", back_populates="movie", cascade="all, delete-orphan"
    )
    embedding: Mapped["MovieEmbedding | None"] = relationship(
        "MovieEmbedding", back_populates="movie", uselist=False, cascade="all, delete-orphan"
    )
    watchlist_entries: Mapped[list["Watchlist"]] = relationship(
        "Watchlist", back_populates="movie", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Movie id={self.id} title={self.title}>"