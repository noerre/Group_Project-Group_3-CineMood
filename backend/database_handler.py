from urllib.parse import uses_query

import mysql.connector
from mysql.connector import Error, connect
from starlette.templating import pass_context

from config import db_config

class DatabaseHandler:
    def __init__(self, db_config):
        self.db_config = db_config
        try:
            self.connection = mysql.connector.connect(
                host=db_config["host"],
                user=db_config["user"],
                password=db_config["password"],
                database=db_config["database"]
            )
            if self.connection.is_connected():
                print("DB connected successfully")
        except Error as e:
            print(f"Error connecting DB: {e}")
            self.connection = None

    def close_connection(self):
        # Closes connection if active
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Connection closed")

    def test_connection(self):
        if self.connection and self.connection.is_connected():
            print("success")
            return True
        else:
            print("Failed connection")
            return False

    def check_record(self, table, column, value):
        """
        Checks if a record exists in the DB

        :param table: Name of the table
        :param column: Name of the column
        :param value: Value to check
        :return: id if exists, None if not exists
        """
        if self.connection and self.connection.is_connected():
            cursor = self.connection.cursor()
            try:
                query = f"SELECT id FROM {table} WHERE {column} = %s"
                cursor.execute(query, (value,))
                result = cursor.fetchone()
                if result:
                    return result[0]
                else:
                    return None
            except Error as e:
                print(f"Error checking record: {e}")
                return None
            finally:
                cursor.close()
        else:
            print("No DB connection")
            return None
    # Manage data
    def add_director(self, director_id, director_name):
        """
        Adds a director to its DB table. If the director already exists in the DB, returns its id. If not, the function
        adds it and returns its id

        :param director_id: director id fetched from TMDb API
        :param director_name: director name
        :return: director id in the DB
        """

        # Check if the record already exists
        existing_id = self.check_record("director", "id", director_id)
        if existing_id:
            print(f"Director {director_name} already exists in DB.")
            return existing_id

        # If not, inserts a new director
        if self.connection and self.connection.is_connected():
            cursor = self.connection.cursor()
            try:
                insert_query = "INSERT INTO director (id, d_name) VALUES (%s, %s)"
                cursor.execute(insert_query, (director_id, director_name))
                self.connection.commit()
                print(f"Director {director_name} added to DB")
                return director_id
            except Error as e:
                print(f"Error adding director: {e}")
                return None
            finally:
                cursor.close()
        else:
            print("No DB connection")
            return None

    def add_actor(self, actor_id, actor_name):
        """
        Adds an actor to its DB table. If the actor already exists in the DB, return its id. If not, the function adds it
        and returns its id

        :param actor_id: actor id, fetched from TMDb API
        :param actor_name: actor name
        :return: actor id in the DB
        """
        # Check if the record already exists
        existing_id = self.check_record("actor", "a_name", actor_id)
        if existing_id:
            print(f"Actor {actor_name} already exists in DB.")
            return existing_id

        # If not, inserts a new director
        if self.connection and self.connection.is_connected():
            cursor = self.connection.cursor()
            try:
                insert_query = "INSERT INTO actor (id, a_name) VALUES (%s, %s)"
                cursor.execute(insert_query, (actor_id, actor_name))
                self.connection.commit()
                print(f"Actor {actor_name} added to DB")
                return actor_id
            except Error as e:
                print(f"Error adding actor: {e}")
                return None
            finally:
                cursor.close()
        else:
            print("No DB connection")
            return None

    def add_genre(self, genre_id, genre):
        """
        Adds a new genre to 'genre' table. If it already exists in the DB, returns its id. If not, the function adds it
        and returns its id

        :param genre_id: genre id fetched from TMDb API
        :param genre: genre name
        :return: genre id in the DB
        """
        # Check if the record already exists
        existing_id = self.check_record("genre", "genre", genre_id)
        if existing_id:
            print(f"Genre {genre} already exists in DB.")
            return existing_id

        # If not, inserts a new director
        if self.connection and self.connection.is_connected():
            cursor = self.connection.cursor()
            try:
                insert_query = "INSERT INTO genre (id, genre) VALUES (%s, %s)"
                cursor.execute(insert_query, (genre_id, genre))
                self.connection.commit()
                print(f"Genre {genre} added to DB")
                return genre_id
            except Error as e:
                print(f"Error adding actor: {e}")
                return None
            finally:
                cursor.close()
        else:
            print("No DB connection")
            return None
    def add_mood(self, mood):
        """
        Adds a mood to its table. If this mood exists, returns its id. If not, the function adds it and returns its id

        :param mood: mood name
        :return: mood id in the DB
        """

        # Check if mood exists
        existing_id = self.check_record("mood", "mood", mood)
        if existing_id:
            print(f"Mood {mood} already exists")
            return existing_id

        # if not, adds a new mood
        if self.connection and self.connection.is_connected():
            cursor = self.connection.cursor()
            try:
                insert_query = "INSERT INTO mood (mood) VALUES (%s)"
                cursor.execute(insert_query, (mood,))
                self.connection.commit()
                mood_id = cursor.lastrowid
                print(f"{mood} added with {mood_id} id")
                return mood_id
            except Error as e:
                print(f"Error adding mood: {e}")
                return None
            finally:
                cursor.close()
        else:
            print("No DB connection")
            return None

    # Manage movie data
    def add_movie(self, movie_data):
        """
        Adds a movie to the movie table in the DB.

        :param movie_data: dictionary with the movie information
        :return: movie id if it's added, None if there's an error
        """
        # Checks if director and country exist
        if not self.check_record("director", "id", movie_data["director_id"]):
            print(f"Director with id {movie_data['director_id']} does not exist")
            return None
        if not self.check_record("country", "id", movie_data["country_id"]):
            print(f"Country with id{movie_data['country_id']} does not exist")
            return None

        if self.connection and self.connection.is_connected():
            cursor = self.connection.cursor()
            try:
                insert_query = """
                    INSERT INTO movie (id, title, release_year, director_id, country_id)
                    VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(insert_query, (
                    movie_data["id"], movie_data["title"], movie_data["release_year"],
                    movie_data["director_id"], movie_data["country_id"]
                ))
                self.connection.commit()
                print(f"{movie_data['title']} successfully added")
                return movie_data["id"]
            except Error as e:
                print(f"Error adding movie: {e}")
                return None
            finally:
                cursor.close()
        else:
            print("No DB connection")
            return None

    def add_cast(self, actor_id, movie_id):
        """
        Adds a relation actor-movie in the table 'cast'

        :param actor_id: actor id
        :param movie_id: movie id
        :return: True if the relation is added, False in other scenarios
        """
        # Checking if actor and movie exist
        if not self.check_record("actor", "id", actor_id):
            print(f"Actor {actor_id} does not exist")
            return False
        if not self.check_record("movie", "id", movie_id):
            print(f"Movie {movie_id} does not exist")
            return False

        if self.connection and self.connection.is_connected():
            cursor = self.connection.cursor()
            try:
                # Check if relation already exists
                query = "SELECT * FROM cast WHERE actor_id = %s AND movie_id = %s"
                cursor.execute(query, (actor_id, movie_id))
                result = cursor.fetchone()

                if result:
                    print(f"Relation between actor {actor_id} and movie {movie_id} already exists")
                    return False

                else:
                    insert_query = "INSERT INTO cast (actor_id, movie_id) VALUES (%s, %s)"
                    cursor.execute(insert_query, (actor_id, movie_id))
                    self.connection.commit()
                    print(f"Actor {actor_id} added to movie {movie_id}")
                    return True
            except Error as e:
                print(f"Error adding actor: {e}")
                return False
            finally:
                cursor.close()
        else:
            print("No DB connection")
            return False

    def add_movie_genre(self, movie_id, genre_id):
        """
        Adds a relation movie-genre to the table 'movie_genre'

        :param movie_id: movie id
        :param genre_id: genre id
        :return: True if the relation is added, False in other scenarios
        """
        # Checking if movie and genre exist
        if not self.check_record("genre", "id", genre_id):
            print(f"Genre {genre_id} does not exist")
            return False
        if not self.check_record("movie", "id", movie_id):
            print(f"Movie {movie_id} does not exist")
            return False

        if self.connection and self.connection.is_connected():
            cursor = self.connection.cursor()
            try:
                # Check if relation already exists
                query = "SELECT * FROM movie_genre WHERE movie_id = %s AND genre_id = %s"
                cursor.execute(query, (movie_id, genre_id))
                result = cursor.fetchone()

                if result:
                    print(f"Relation between genre {genre_id} and movie {movie_id} already exists")
                    return False

                else:
                    insert_query = "INSERT INTO movie_genre (movie_id, genre_id) VALUES (%s, %s)"
                    cursor.execute(insert_query, (movie_id, genre_id))
                    self.connection.commit()
                    print(f"Genre {genre_id} added to movie {movie_id}")
                    return True
            except Error as e:
                print(f"Error adding relation: {e}")
                return False
            finally:
                cursor.close()
        else:
            print("No DB connection")
            return False

    def get_movie_by_title(self, title):
        """
        Gets a movie by its title

        :param title: Title of the movie
        :return: Dictionary with movie data. None if there is no movie
        """
        if self.connection and self.connection.is_connected():
            cursor = self.connection.cursor(dictionary=True)
            try:
                query = "SELECT * FROM movie WHERE title = %s"
                cursor.execute(query, (title,))
                result = cursor.fetchone()

                if result:
                    return result
                else:
                    print(f"{title} not found")
                    return None
            except Error as e:
                print(f"Error fetching movie: {e}")
                return None
            finally:
                cursor.close()

        else:
            print("No DB connection")
            return None

    def get_movie_id(self, title):
        """
        Gets a movie id by its title
        :param title: title of the movie
        :return: movie id. None if movie does not exist
        """
        if self.connection and self.connection.is_connected():
            cursor = self.connection.cursor()
            try:
                query = "SELECT id FROM movie WHERE title = %s"
                cursor.execute(query, (title,))
                result = cursor.fetchone()

                if result:
                    return result[0]
                else:
                    print(f"{title} not found")
                    return None
            except Error as e:
                print(f"Error fetching movie: {e}")
                return None
            finally:
                cursor.close()

        else:
            print("No DB connection")
            return None
    def map_movie_mood(self, movie_id, mood_id, genre_id):
        """
        Maps a mood to a genre and adds mood to a certain movie

        :param movie_id:
        :param mood_id:
        :param genre_id:
        :return:
        """
        pass

    # Manage user data
    def add_watched_movie(self, user_id, movie_id):
        """
        Adds a movie to the list of watched movies by an user.

        :param user_id: user id
        :param movie_id: movie id
        :return: True if the watched movie was added. False in other scenarios
        """
        # Checking if user and movie exist
        if not self.check_record("users", "id", user_id):
            print(f"User {user_id} does not exist")
            return False
        if not self.check_record("movie", "id", movie_id):
            print(f"Movie {movie_id} does not exist")
            return False

        if self.connection and self.connection.is_connected():
            cursor = self.connection.cursor()
            try:
                # Check if relation already exists
                query = "SELECT * FROM watched WHERE user_id = %s AND movie_id = %s"
                cursor.execute(query, (user_id, movie_id))
                result = cursor.fetchone()

                if result:
                    print(f"Movie {movie_id} is already in the user {user_id} watched list")
                    return False
                else:
                    insert_query = "INSERT INTO watched (user_id, movie_id) VALUES (%s, %s)"
                    cursor.execute(insert_query, (user_id, movie_id))
                    self.connection.commit()
                    print(f"Movie {movie_id} watched by {user_id}")
                    return True
            except Error as e:
                print(f"Error marking watched movie: {e}")
                return False
            finally:
                cursor.close()
        else:
            print("No DB connection")
            return False

    def get_watched_movies(self, user_id):
        """
        Gets a list of all the movies watched by a user

        :param user_id: user id
        :return: List of dictionaries with all the movies watched. None if there are no watched movies
        """
        # Check if user exists
        if not self.check_record("users", "id", user_id):
            print(f"User {user_id} does not exist")
            return None

        if self.connection and self.connection.is_connected():
            cursor = self.connection.cursor(dictionary=True)
            try:
                query = """
                    SELECT m.id, m.title, m.release_year
                    FROM watched AS w
                    JOIN movie AS m ON w.movie_id = m.id
                    WHERE w.user_id = %s
                """
                cursor.execute(query, (user_id,))
                result = cursor.fetchall()

                if result:
                    return result
                else:
                    print(f"User {user_id} has no watched movies")
                    return None
            except Error as e:
                print(f"Error getting watched movies: {e}")
                return None
            finally:
                cursor.close()
        else:
            print("No DB connection")
            return None

    def add_rating(self, user_id, movie_id, rating, review=None):
        """
        Adds users rating for a movie

        :param user_id: user id
        :param movie_id: movie id
        :param rating: movie rating (between 1 and 5)
        :param review: optional review of the movie
        :return: true if it's successfully added. False in other scenarios
        """
        # Check if parameters exists in the DB
        if not self.check_record("users", "id", user_id):
            print(f"User {user_id} does not exist")
            return False
        if not self.check_record("movie", "id", movie_id):
            print(f"Movie {movie_id} does not exist")
            return False
        # Check ratings constraint
        if not 1 <= rating <= 5:
            print("Rating must be between 1 and 5")
            return False

        if self.connection and self.connection.is_connected():
            cursor = self.connection.cursor()
            try:
                # Check if the user already reviewed this movie
                query = "SELECT * FROM rating WHERE user_id = %s AND movie = %s"
                cursor.execute(query, (user_id, movie_id))
                result = cursor.fetchone()

                if result:
                    print(f"User {user_id} already reviewed movie {movie_id}")
                    return False
                else:
                    insert_query="""
                        INSERT INTO rating (user_id, movie_id, rating, review)
                        VALUES (%s, %s, %s, %s)
                    """
                    cursor.execute(insert_query, (user_id, movie_id, rating, review))
                    self.connection.commit()
                    print("Rating added")
                    return True
            except Error as e:
                print(f"Error adding rating: {e}")
                return False
            finally:
                cursor.close()
        else:
            print("No DB connection")
            return False

    def get_movie_ratings(self, movie_id):
        """
        Gets all the ratings for a movie

        :param movie_id: movie id
        :return: list of dictionaries with the ratings. None if there are no ratings
        """
        # Check if movie exists
        if not self.check_record("movie", "id", movie_id):
            print(f"Movie {movie_id} does not exist")
            return None

        if self.connection and self.connection.is_connected():
            cursor = self.connection.cursor(dictionary=True)
            try:
                query = """
                    SELECT r.user_id, r.rating, r.review, u.username
                    FROM rating AS r
                    JOIN users AS u ON r.user_id = u.id
                    WHERE r.movie = %s
                """
                cursor.execute(query, (movie_id,))
                result = cursor.fetchall()

                if result:
                    return result
                else:
                    print(f"Movie {movie_id} has no califications")
                    return None
            except Error as e:
                print(f"Error retrieving reviews: {e}")
                return None
            finally:
                cursor.close()
        else:
            print("No DB connection")
            return None
    def add_recommendation(self, user_id, movie_id):
        """
        Saves the movie recommendation for an user

        :param user_id: user id
        :param movie_id: movie id
        :return: True if recommendation was added. False in other scenarios
        """
        # Check if user and movie exist
        if not self.check_record("users", "id", user_id):
            print(f"User {user_id} does not exist")
            return False
        if not self.check_record("movie", "id", movie_id):
            print(f"Movie {movie_id} does not exist")
            return False

        if self.connection and self.connection.is_connected():
            cursor = self.connection.cursor()
            try:
                # Check if recommendation was already made
                query = "SELECT * FROM recommendations WHERE user_id = %s AND movie_id = %s"
                cursor.execute(query, (user_id, movie_id))
                result = cursor.fetchone()

                if result:
                    print(f"Movie {movie_id} was already recommended to user {user_id}")
                    return False

                insert_query = "INSERT INTO recommendations (user_id, movie_id) VALUES (%s, %s)"
                cursor.execute(insert_query, (user_id, movie_id))
                self.connection.commit()
                print(f"Movie {movie_id} recommended to user {user_id}.")
                return True
            except Error as e:
                print(f"Error adding recommendation: {e}")
                return False
            finally:
                cursor.close()
        else:
            print("No DB connection")
            return False

    def get_recommendation(self, user_id):
        """
        Gets all the recommendations for a certain user

        :param user_id: user id
        :return: List of dictionaries with the recommended movies. None if there are no recommendations
        """
        # Check if user exists
        if not self.check_record("users", "id", user_id):
            print(f"User {user_id} does not exist")
            return None

        if self.connection and self.connection.is_connected():
            cursor = self.connection.cursor(dictionary=True)
            try:
                query = """
                    SELECT m.id, m.title, m.release_year
                    FROM recommendations AS r
                    JOIN movie AS m ON r.movie_id = m.id
                    WHERE r.user_id = %s
                """
                cursor.execute(query, (user_id,))
                result = cursor.fetchall()

                if result:
                    return result
                else:
                    print(f"User {user_id} has no recommendations")
                    return None
            except Error as e:
                print(f"Error retrieving recommendations: {e}")
                return None
            finally:
                cursor.close()
        else:
            print("No DB connection")
            return None

