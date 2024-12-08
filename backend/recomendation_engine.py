from mood_to_genres import get_genres_for_mood
from API_handler import fetch_movies_by_genre


def recommend_movies(user_id, mood, limit=12):
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
    fetched_movies = set()

    for genre in genres:
        per_genre_limit = limit
        genre_movies = fetch_movies_by_genre(genre, mood, limit=per_genre_limit)

        for movie in genre_movies:
            if movie['title'] not in fetched_movies:
                recommendations.append(movie)
                fetched_movies.add(movie['title'])

        limit -= len(recommendations)
        if limit <= 0:
            break

    if len(recommendations) < limit:
        for genre in genres:
            additional_movies = fetch_movies_by_genre(genre, mood, limit=limit)
            for movie in additional_movies:
                if movie['title'] not in fetched_movies:
                    recommendations.append(movie)
                    fetched_movies.add(movie['title'])
                    if len(recommendations) >= limit:
                        break

    return recommendations
