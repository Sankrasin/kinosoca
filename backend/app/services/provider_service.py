# logic for getting lists of streaming providers like netflix, amazon prime, etc
from sqlalchemy.orm import Session

from app.models.watch_provider import WatchProvider, MovieWatchProvider


def list_all_providers(db: Session, country: str = "IN") -> list[WatchProvider]:
    # only get providers that actually have movies in this country
    return (
        db.query(WatchProvider)
        .join(MovieWatchProvider, MovieWatchProvider.provider_id == WatchProvider.id)
        .filter(MovieWatchProvider.country_code == country)
        .distinct()
        .order_by(WatchProvider.name.asc())
        .all()
    )


def get_provider_by_name(db: Session, name: str) -> WatchProvider | None:
    return db.query(WatchProvider).filter(WatchProvider.name.ilike(name)).first()