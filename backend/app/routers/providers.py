# route for listing providers like netflix, used for search filters
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.movie import WatchProviderOut
from app.services.provider_service import list_all_providers

router = APIRouter(prefix="/providers", tags=["Providers"])


@router.get("", response_model=list[WatchProviderOut])
def get_providers(
    country: str = Query(default="IN", description="ISO country code"),
    db: Session = Depends(get_db),
):
    providers = list_all_providers(db, country=country)
    return [
        WatchProviderOut(
            provider_id=p.id,
            name=p.name,
            logo_path=p.logo_path,
            access_type="flatrate",  # just a dummy value since this is just a list
            provider_url=None,
        )
        for p in providers
    ]