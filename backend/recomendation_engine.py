# recommendation_engine.py
from mood_to_genres import get_genres_for_mood
from API_handler import fetch_movies_by_genre


def recommend_movies(user_id, mood, limit=10):
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
        recommendations.extend(fetch_movies_by_genre(genre, mood, limit=limit // len(genres)))

    """
    Add here filter movies by user previous watchlist
    add to limit how many movies you deleted from recomendation list
    so that it can be filled more, so each time it showes you equal amount of movies (new movies you haven't watched)
    """

    return recommendations

