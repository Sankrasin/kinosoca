"""
Re-exports the ML engines and explainer functions for convenient imports
(e.g. `from app.ml import get_hybrid_recommendations, get_movies_for_mood`).
"""
from app.ml.tfidf_engine import tfidf_engine, TFIDFEngine, build_and_persist as build_tfidf_index
from app.ml.semantic_engine import semantic_engine, SemanticEngine
from app.ml.hybrid_engine import get_hybrid_recommendations
from app.ml.mood_mapper import get_all_moods, get_movies_for_mood
from app.ml.explainer import explain_recommendation, explain_mood_match

__all__ = [
    "tfidf_engine",
    "TFIDFEngine",
    "build_tfidf_index",
    "semantic_engine",
    "SemanticEngine",
    "get_hybrid_recommendations",
    "get_all_moods",
    "get_movies_for_mood",
    "explain_recommendation",
    "explain_mood_match",
]