mood_to_genre_mapping = {
    "happy": ["comedy", "adventure", "animation", "fantasy", "family"],
    "sad": ["drama", "romance", "history", "war"],
    "excited": ["action", "thriller", "crime", "science_fiction", "western"],
    "relaxed": ["documentary", "family", "music", "tv_movie"],
    "nostalgic": ["classic", "musical", "fantasy", "history"],
    "curious": ["mystery", "science_fiction", "thriller"],
    "chill": ["documentary", "animation", "music", "family"]
}

mood_isnot_genre_mapping = {
    "happy": [
        "drama", "history", "war", "crime", "science_fiction",
        "classic", "musical", "mystery", "thriller", "documentary",
        "western", "action", "music"
    ],
    "sad": [
        "comedy", "adventure", "animation", "fantasy", "family", "science_fiction",
        "tv_movie", "classic", "musical", "mystery", "thriller", "documentary",
        "western", "action", "music"
    ],
    "excited": [
        "comedy", "adventure", "animation", "fantasy", "family", "drama",
        "romance", "history", "war", "documentary", "classic", "musical",
        "tv_movie", "music"
    ],
    "relaxed": [
        "comedy", "adventure", "animation", "fantasy", "family", "action",
        "thriller", "crime", "science_fiction", "western", "drama", "romance",
        "classic", "musical", "mystery", "war"
    ],
    "nostalgic": [
        "comedy", "adventure", "animation", "family", "action", "thriller",
        "crime", "science_fiction", "western", "tv_movie", "music", "documentary",
        "drama", "romance"
    ],
    "curious": [
        "comedy", "adventure", "animation", "family", "drama", "romance",
        "history", "war", "classic", "musical", "tv_movie", "music",
        "documentary", "western", "action"
    ],
    "chill": [
        "action", "thriller", "crime", "science_fiction", "western", "drama",
        "romance", "history", "war", "classic", "musical", "mystery",
        "fantasy", "adventure", "comedy"
    ]
}


def get_genres_for_mood(mood):
    """
    Returns a list of genres corresponding to the given mood.

    :param mood: User's current mood.
    :return: List of genres.
    """
    return mood_to_genre_mapping.get(mood.lower(), [])

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