# this script figures out why we recommended a movie and returns a readable string
from app.models.movie import Movie

MAX_SHARED_GENRES_TO_MENTION = 2
MAX_SHARED_KEYWORDS_TO_MENTION = 2
MAX_SHARED_CAST_TO_MENTION = 1

SEMANTIC_SIMILARITY_THRESHOLD = 0.55
TFIDF_SIMILARITY_THRESHOLD = 0.15


def explain_recommendation(
    source: Movie,
    candidate: Movie,
    tfidf_score: float = 0.0,
    semantic_score: float = 0.0,
) -> list[str]:
    reasons: list[str] = []

    # check for matching genres
    source_genre_names = {g.name for g in source.genres}
    candidate_genre_names = {g.name for g in candidate.genres}
    shared_genres = list(source_genre_names & candidate_genre_names)
    if shared_genres:
        names = ", ".join(shared_genres[:MAX_SHARED_GENRES_TO_MENTION])
        reasons.append(f"Shares the {names} genre" + ("s" if len(shared_genres) > 1 else ""))

    # check for matching keywords
    source_keyword_names = {k.name for k in source.keywords}
    candidate_keyword_names = {k.name for k in candidate.keywords}
    shared_keywords = list(source_keyword_names & candidate_keyword_names)
    if shared_keywords:
        names = ", ".join(shared_keywords[:MAX_SHARED_KEYWORDS_TO_MENTION])
        reasons.append(f"Similar themes: {names}")

    # check for matching cast
    source_cast_ids = {p.id for p in source.cast}
    candidate_cast_names = [p.name for p in candidate.cast if p.id in source_cast_ids]
    if candidate_cast_names:
        names = ", ".join(candidate_cast_names[:MAX_SHARED_CAST_TO_MENTION])
        reasons.append(f"Features {names}, also in this movie")

    # check for matching director
    source_director_ids = {p.id for p in source.crew}
    candidate_director_names = [p.name for p in candidate.crew if p.id in source_director_ids]
    if candidate_director_names:
        reasons.append(f"Directed by {candidate_director_names[0]}, like the source movie")

    # add reason if ml score was high enough
    if semantic_score >= SEMANTIC_SIMILARITY_THRESHOLD:
        reasons.append("Similar storytelling and tone")

    if tfidf_score >= TFIDF_SIMILARITY_THRESHOLD and not reasons:
        reasons.append("Similar overall content and description")

    # fallback reason
    if not reasons:
        reasons.append("Similar audience interests")

    return reasons


def explain_mood_match(mood_name: str, matched_genre_names: list[str]) -> list[str]:
    if matched_genre_names:
        names = ", ".join(matched_genre_names[:2])
        return [f"Matches the '{mood_name}' mood through {names}"]
    return [f"Matches the '{mood_name}' mood"]