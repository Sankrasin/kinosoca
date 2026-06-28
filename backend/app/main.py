# main file for the fast api app
# puts together cors, routes, and ml stuff

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.core.exceptions import register_exception_handlers
from app.ml.tfidf_engine import tfidf_engine
from app.ml.semantic_engine import semantic_engine
from app.routers import auth, movies, search, recommendations, mood, watchlist, profile, providers


@asynccontextmanager
async def lifespan(app: FastAPI):
    # load tf-idf matrix when starting up
    # if it's not built yet, it just returns nothing for now
    tfidf_engine.load_cached()

    # note: semantic engine loads its model later when needed, not right now

    yield

    # nothing much to close here


app = FastAPI(
    title=settings.APP_NAME,
    description="movie recommendation app",
    version="1.0.0",
    lifespan=lifespan,
)

# setup cors so frontend can talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_ORIGIN],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_exception_handlers(app)

# add all the routes
app.include_router(auth.router, prefix=settings.API_V1_PREFIX)
app.include_router(movies.router, prefix=settings.API_V1_PREFIX)
app.include_router(search.router, prefix=settings.API_V1_PREFIX)
app.include_router(recommendations.router, prefix=settings.API_V1_PREFIX)
app.include_router(mood.router, prefix=settings.API_V1_PREFIX)
app.include_router(watchlist.router, prefix=settings.API_V1_PREFIX)
app.include_router(profile.router, prefix=settings.API_V1_PREFIX)
app.include_router(providers.router, prefix=settings.API_V1_PREFIX)


@app.get("/", tags=["Health"])
def root():
    return {"status": "ok", "service": settings.APP_NAME}


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "healthy"}