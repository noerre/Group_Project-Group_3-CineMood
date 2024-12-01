from tmdbv3api import TMDb, Discover
from config import tmdb_api_key

# Configure TMDb
tmdb = TMDb()
tmdb.api_key = tmdb_api_key
tmdb.language = 'en'


def fetch_movies_by_genre(genre_name, limit=5):
    """
    Fetches movies based on genre name from TMDb.

    :param genre_name: The genre to search for.
    :param limit: The number of movies to fetch.
    :return: List of movies with title, release year, and overview.
    """
    discover = Discover()
    genre_map = get_genre_mapping()  # Map genre names to TMDb genre IDs
    genre_id = genre_map.get(genre_name.lower())

    if not genre_id:
        raise ValueError(f"Genre '{genre_name}' not found in TMDb.")

    # Fetch movies for the genre
    results = discover.discover_movies({
        'with_genres': genre_id,
        'sort_by': 'popularity.desc'
    })

    # Limit results and return necessary fields
    return [
        {"title": m['title'], "release_year": m['release_date'].split('-')[0], "overview": m['overview']}
        for m in results[:limit]
    ]


def get_genre_mapping():
    """
    Returns a dictionary of TMDb genres and their IDs.
    """
    return {
        "action": 28,
        "adventure": 12,
        "comedy": 35,
        "drama": 18,
        "romance": 10749,
        "thriller": 53,
        "documentary": 99,
        "family": 10751,
        "classic": 10402,  # Musical
        "musical": 10402
    }
