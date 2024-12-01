# recommendation_engine.py
from backend.mood_to_genres import get_genres_for_mood
from backend.tmdb_utils import fetch_movies_by_genre


def recommend_movies(user_id, mood, limit=5):
    """
    Recommends movies based on user's mood by fetching data from TMDb.

    :param user_id: ID of the user.
    :param mood: Current mood of the user.
    :param limit: Number of recommendations to fetch.
    :return: List of recommended movies.
    """
    genres = get_genres_for_mood(mood)
    if not genres:
        return {"error": f"No genres found for mood: {mood}"}

    recommendations = []
    for genre in genres:
        recommendations.extend(fetch_movies_by_genre(genre, limit=limit // len(genres)))

    return recommendations

