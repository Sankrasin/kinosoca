# helper class to talk to tmdb api
import httpx

from app.config import settings
from app.core.exceptions import ExternalServiceException


class TMDBClient:
    def __init__(self):
        self.base_url = settings.TMDB_BASE_URL
        self.api_key = settings.TMDB_API_KEY
        self.image_base_url = settings.TMDB_IMAGE_BASE_URL
        self._client = httpx.Client(timeout=15.0)

    def _get(self, path: str, params: dict | None = None) -> dict:
        params = params or {}
        params["api_key"] = self.api_key
        url = f"{self.base_url}{path}"
        try:
            response = self._client.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as exc:
            raise ExternalServiceException(
                f"TMDB request failed ({exc.response.status_code}): {path}"
            ) from exc
        except httpx.RequestError as exc:
            raise ExternalServiceException(f"TMDB request error: {path} — {exc}") from exc

    def close(self):
        self._client.close()

    def get_popular_movies(self, page: int = 1) -> dict:
        return self._get("/movie/popular", {"page": page})

    def get_top_rated_movies(self, page: int = 1) -> dict:
        return self._get("/movie/top_rated", {"page": page})

    def get_trending_movies(self, time_window: str = "week", page: int = 1) -> dict:
        return self._get(f"/trending/movie/{time_window}", {"page": page})

    def discover_movies(self, page: int = 1, **filters) -> dict:
        # lets you pass stuff like with_genres
        params = {"page": page, **filters}
        return self._get("/discover/movie", params)

    def search_movies(self, query: str, page: int = 1) -> dict:
        return self._get("/search/movie", {"query": query, "page": page})

    def get_movie_details(self, movie_id: int) -> dict:
        return self._get(f"/movie/{movie_id}")

    def get_movie_credits(self, movie_id: int) -> dict:
        return self._get(f"/movie/{movie_id}/credits")

    def get_movie_keywords(self, movie_id: int) -> dict:
        return self._get(f"/movie/{movie_id}/keywords")

    def get_movie_watch_providers(self, movie_id: int) -> dict:
        return self._get(f"/movie/{movie_id}/watch/providers")

    def get_genre_list(self) -> dict:
        return self._get("/genre/movie/list")

    def poster_url(self, poster_path: str | None, size: str = "w500") -> str | None:
        if not poster_path:
            return None
        return f"{self.image_base_url}/{size}{poster_path}"

    def backdrop_url(self, backdrop_path: str | None, size: str = "w1280") -> str | None:
        if not backdrop_path:
            return None
        return f"{self.image_base_url}/{size}{backdrop_path}"


tmdb_client = TMDBClient()