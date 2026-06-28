# people model like actors and directors
from typing import TYPE_CHECKING

from sqlalchemy import String, Table, Column, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.movie import Movie

# links movies and actors
movie_cast = Table(
    "movie_cast",
    Base.metadata,
    Column("movie_id", Integer, ForeignKey("movies.id", ondelete="CASCADE"), primary_key=True),
    Column("person_id", Integer, ForeignKey("persons.id", ondelete="CASCADE"), primary_key=True),
    Column("character_name", String(255), nullable=True),
)

# links movies and crew (director, writer, etc)
movie_crew = Table(
    "movie_crew",
    Base.metadata,
    Column("movie_id", Integer, ForeignKey("movies.id", ondelete="CASCADE"), primary_key=True),
    Column("person_id", Integer, ForeignKey("persons.id", ondelete="CASCADE"), primary_key=True),
    Column("job", String(100), primary_key=True),
)


class Person(Base):
    __tablename__ = "persons"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)  # using tmdb person id
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    profile_path: Mapped[str | None] = mapped_column(String(255), nullable=True)

    cast_movies: Mapped[list["Movie"]] = relationship(
        "Movie", secondary=movie_cast, back_populates="cast"
    )
    crew_movies: Mapped[list["Movie"]] = relationship(
        "Movie", secondary=movie_crew, back_populates="crew"
    )

    def __repr__(self) -> str:
        return f"<Person id={self.id} name={self.name}>"