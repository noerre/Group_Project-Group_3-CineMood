mood_to_genre_mapping = {
    "happy": ["comedy", "adventure", "animation", "fantasy", "family"],
    "sad": ["drama", "romance", "history", "war"],
    "excited": ["action", "thriller", "crime", "science_fiction", "western"],
    "relaxed": ["documentary", "family", "music", "tv_movie"],
    "nostalgic": ["classic", "musical", "history"],
    "curious": ["mystery", "science_fiction", "thriller"],
    "chill": [ "animation", "music", "family"]
}

mood_isnot_genre_mapping = {
    "happy": [
        "drama", "history", "war", "crime",
        "classic", "mystery", "thriller", "documentary",
        "western",
    ],
    "sad": [
        "animation", "fantasy", "family",
        "mystery", "western", "action", "music"
    ],
    "excited": [
        "fantasy", "family", "drama",
        "romance", "history", "war", "documentary", "classic", "musical",
        "tv_movie", "music"
    ],
    "relaxed": [
        "fantasy", "family", "action",
        "thriller", "crime", "western", "drama", "romance",
        "classic", "musical", "mystery", "war"
    ],
    "nostalgic": [
        "comedy", "adventure", "animation", "family", "action", "thriller",
        "crime", "science_fiction", "tv_movie", "music", "documentary",
        "romance"
    ],
    "curious": [
        "comedy", "animation", "family", "drama", "romance",
        "history", "war", "classic", "musical", "tv_movie", "music",
        "documentary", "western",
    ],
    "chill": [
        "thriller", "science_fiction", "western", "drama",
        "romance", "history", "war",
    ]
}


def get_genres_for_mood(mood):
    """
    Returns a list of genres corresponding to the given mood.

    :param mood: User's current mood.
    :return: List of genres.
    """
    return mood_to_genre_mapping.get(mood.lower(), [])


def filter_movies_by_mood(movies, mood):
    """
    Filters the list of movies based on the genres to exclude for a given mood.

    :param movies: List of movies with genre IDs and other details.
    :param mood: The user's mood to filter movies by.
    :return: Filtered list of movies.
    """
    # Map genre names to genre IDs
    genre_map = get_genre_mapping()  # Assume this returns {genre_name: genre_id}

    # Get excluded genre IDs for the mood
    excluded_genres = set(genre_map.get(genre.lower()) for genre in mood_isnot_genre_mapping.get(mood, []))

    # Filter out movies with any excluded genres
    filtered_movies = [
        movie for movie in movies
        if not excluded_genres.intersection(set(movie['genre_ids']))
    ]

    return filtered_movies

def get_genre_mapping():
    """
    Returns a dictionary of TMDb genres and their IDs.
    """
    return {
        "action": 28,
        "adventure": 12,
        "animation": 16,
        "comedy": 35,
        "crime": 80,
        "documentary": 99,
        "drama": 18,
        "family": 10751,
        "fantasy": 14,
        "history": 36,
        "horror": 27,
        "music": 10402,
        "mystery": 9648,
        "romance": 10749,
        "science_fiction": 878,
        "tv_movie": 10770,
        "thriller": 53,
        "war": 10752,
        "western": 37,
        "classic": 10402,  # Musical
        "musical": 10402
    }