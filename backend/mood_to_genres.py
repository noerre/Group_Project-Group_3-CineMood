mood_to_genre_mapping = {
    "happy": ["comedy", "adventure"],
    "sad": ["drama", "romance"],
    "excited": ["action", "thriller"],
    "relaxed": ["documentary", "family"],
    "nostalgic": ["classic", "musical"]
}

def get_genres_for_mood(mood):
    """
    Returns a list of genres corresponding to the given mood.

    :param mood: User's current mood.
    :return: List of genres.
    """
    return mood_to_genre_mapping.get(mood.lower(), [])