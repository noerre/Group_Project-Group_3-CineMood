import requests
from database_handler import DatabaseHandler
from config import api_config, db_config

from tmdbv3api import TMDb, Discover, Movie
from config import tmdb_api_key
from mood_to_genres import get_genre_mapping, filter_movies_by_mood


class TMDbAPIHandler:
    BASE_URL = "https://api.themoviedb.org/3"

    # Genre IDs for Action, Comedy, Drama, Adventure
    GENRE_IDS = {
        "Action": 28,
        "Comedy": 35,
        "Drama": 18,
        "Adventure": 12
    }

    def __init__(self):
        # Initialize API key
        self.api_key = api_config['api_key']
        if not self.api_key:
            raise ValueError("API key not found.")

        # Initialize DatabaseHandler with dotenv and file config
        self.db_handler = DatabaseHandler(
            host=db_config['host'],
            user=db_config['user'],
            password=db_config['password'],
            database=db_config['database']
        )

    def test_connection(self):
        """Check if the API key (bearer token) is valid by making a simple request to TMDb API."""
        test_url = f"{self.BASE_URL}/authentication"  # Correct TMDb endpoint
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {self.api_key}"  # Pass the API key as a bearer token
        }

        try:
            response = requests.get(test_url, headers=headers, timeout=10)
            response.raise_for_status()  # Raise an exception for HTTP errors
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Failed to connect to TMDb API: {e}")

        # Optional: Validate the response
        if response.status_code != 200:
            raise ValueError(f"Unexpected response from TMDb API: {response.status_code}")

        print("TMDb API connection established successfully.")

    def get_movie_details(self, movie_id):
        # Fetch detailed information about a movie, including director and country ID

        # Fetch movie details
        movie_url = f"{self.BASE_URL}/movie/{movie_id}"
        movie_params = {"api_key": self.api_key}
        movie_response = requests.get(movie_url, params=movie_params)
        movie_response.raise_for_status()
        movie_data = movie_response.json()

        # Fetch credits for the director information
        credits_url = f"{self.BASE_URL}/movie/{movie_id}/credits"
        credits_response = requests.get(credits_url, params={"api_key": self.api_key})
        credits_response.raise_for_status()
        credits_data = credits_response.json()

        # Extract director ID
        director_id = None
        for crew_member in credits_data['crew']:
            if crew_member['job'] == 'Director':
                director_id = crew_member['id']
                break

        # Extract country ID
        country_id = None
        if movie_data['production_countries']:
            country_id = movie_data['production_countries'][0]['iso_3166_1']

        return {
            "title": movie_data["title"],
            "release_year": movie_data["release_date"][:4],  # Use only the year
            "director_id": director_id,
            "country_id": country_id
        }

    def get_movies_by_genre(self, genre_name, page=1):
        # Fetch a list of movies for a given genre name and store them in the database.

        genre_id = self.GENRE_IDS.get(genre_name)
        if not genre_id:
            print(f"Error: Genre '{genre_name}' not found.")
            return

        url = f"{self.BASE_URL}/discover/movie"
        params = {
            "api_key": self.api_key,
            "with_genres": genre_id,
            "page": page
        }

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()  # Raise an error for HTTP codes like 401 or 404
            data = response.json()

            movies = data.get("results", [])
            for movie in movies:
                details = self.get_movie_details(movie["id"])
                # Save the movie details to the database
                self.db_handler.add_movie(details)
                print(f"Movie '{details['title']}' added to the database.")

        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except Exception as err:
            print(f"An unexpected error occurred: {err}")


## this is from Aleksandra files:


# Configure TMDb
tmdb = TMDb()
tmdb.api_key = tmdb_api_key
tmdb.language = 'en'
movie_api = Movie()

def fetch_movies_by_genre(genre_name, mood, limit=1000):
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

    movies = [
        {
            "title": m['title'],
            "release_year": m['release_date'].split('-')[0],
            "overview": m['overview'],
            "genre_ids": m['genre_ids'],
            "poster_path": m['poster_path']
        }
        for m in results
    ]

    # Filter movies by mood
    filtered_movies = filter_movies_by_mood(movies, mood)

    # Limit results
    return filtered_movies[:limit]


def fetch_movie_info(title, db_handler):

    """
    Fetch movie information. First checks the local database; if not found, fetches from TMDb.

<<<<<<< HEAD
    :param title: Movie title to search for.
    :param db_handler: Instance of the DatabaseHandler class.
    :return: Dictionary with movie details or None if not found.
=======

def fetch_by_movie_name():

    """
    if not title:
        raise ValueError("Movie title is required")


    movie = db_handler.get_movie_by_title(title)
    if movie:
        return movie


    tmdb_results = movie_api.search(title)
    if not tmdb_results:
        return None

    movies = []
    for tmdb_movie in tmdb_results:
        movies.append({
            "title": tmdb_movie.title,
            "release_year": tmdb_movie.release_date.split('-')[0] if tmdb_movie.release_date else "Unknown",
            "overview": tmdb_movie.overview,
            "genres": [genre['name'] for genre in tmdb_movie.genres] if hasattr(tmdb_movie, 'genres') else [],
            "popularity": tmdb_movie.popularity
        })

    return movies



# main function
if __name__ == "__main__":
    tmdb_handler = TMDbAPIHandler()
    tmdb_handler.test_connection()
    tmdb_handler.get_movie_details('181812')

    # # Example of fetching movies by genre and storing them in the database
    # genres = ["Action", "Comedy", "Drama", "Adventure"]
    # for genre in genres:
    #     print(f"\nFetching movies for the '{genre}' genre...")
    #     tmdb_handler.get_movies_by_genre(genre)
