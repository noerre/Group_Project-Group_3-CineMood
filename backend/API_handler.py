import requests
from database_handler import DatabaseHandler


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
        self.api_key = "48bb9ee8045809c1d8bc398b65b910a2"  # Replace with your actual TMDb API key
        if not self.api_key:
            raise ValueError("API key not found.")

        # Initialize DatabaseHandler
        self.db_handler = DatabaseHandler(host="localhost", user="root", password="password",
                                          database="movies_db")  # Update with your DB credentials

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


# main function
if __name__ == "__main__":
    tmdb_handler = TMDbAPIHandler()

    # Example of fetching movies by genre and storing them in the database
    genres = ["Action", "Comedy", "Drama", "Adventure"]
    for genre in genres:
        print(f"\nFetching movies for the '{genre}' genre...")
        tmdb_handler.get_movies_by_genre(genre)
