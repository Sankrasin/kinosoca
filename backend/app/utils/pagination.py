# helper for handling pagination in the api
from fastapi import Query

from app.config import settings


def pagination_params(
    page: int = Query(default=1, ge=1, description="Page number, starting at 1"),
    page_size: int = Query(
        default=settings.DEFAULT_PAGE_SIZE,
        ge=1,
        le=settings.MAX_PAGE_SIZE,
        description="Number of items per page",
    ),
) -> tuple[int, int]:
    return page, page_size


def clamp_page_size(page_size: int) -> int:
    # make sure page size doesn't go over max
    return max(1, min(page_size, settings.MAX_PAGE_SIZE))