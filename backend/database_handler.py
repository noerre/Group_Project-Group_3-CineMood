import mysql.connector
from mysql.connector import Error
from config import db_config


class DatabaseHandler:
    def __init__(self, host, user, password, database):
        try:
            self.connection = mysql.connector.connect(

                host=host,
                user=user,
                password=password,
                database=database
            )
            if self.connection.is_connected():
                print("Database id connected successfully")
        except Error as e:
            print("Error connecting to database")

    def close_connection(self):
        if self.connection.is_connected():
            self.connection.close()
            print("database connection closed")

    # Add_movie_function
    def add_movie(self, movie_data):
        cursor = self.connection.cursor()
        query = """
        INSERT INTO movie (title, release_year, director_id, country_id, platform_id)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (
            movie_data["title"],
            movie_data["release_year"],
            movie_data["director_id"],
            movie_data["country_id"],
        ))
        self.connection.commit()

    def get_movie_by_title(self, title):
        cursor = self.connection.cursor(dictionary=True)
        query = "SELECT * FROM movie WHERE title = %s"
        cursor.execute(query, (title,))
        return cursor.fetchone()

    # Add_watched_movies
    def add_watched_movie(self, user_id, movie_id):
        cursor = self.connection.cursor()
        query = "INSERT INTO watched (user_id, movie_id) VALUES (%s, %s)"
        cursor.execute(query, (user_id, movie_id))
        self.connection.commit()

    def get_watched_movies(self, user_id):
        cursor = self.connection.cursor(dictionary=True)
        query = """
        SELECT m.title, m.release_year 
        FROM watched w
        JOIN movie m ON w.movie_id = m.id
        WHERE w.user_id = %s
        """
        cursor.execute(query, (user_id,))
        return cursor.fetchall()

    # Add rating
    def add_rating(self, user_id, movie_id, rating, review=None):
        cursor = self.connection.cursor()
        query = """
        INSERT INTO rating (user_id, movie_id, rating, review)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (user_id, movie_id, rating, review))
        self.connection.commit()

    def get_movie_ratings(self, movie_id):
        cursor = self.connection.cursor(dictionary=True)
        query = """
        SELECT r.rating, r.review, u.username
        FROM rating r
        JOIN users u ON r.user_id = u.id
        WHERE r.movie_id = %s
        """
        cursor.execute(query, (movie_id,))
        return cursor.fetchall()




## this is from Aleksandra files:

def connect_db():
    """
    Establishes a connection to the database.
    """
    return mysql.connector.connect(**db_config)


def query_watched_movies(user_id):
    """
    Retrieves IDs of movies watched by a user.

    :param user_id: ID of the user.
    :return: List of movie IDs.
    """
    conn = connect_db()
    cursor = conn.cursor()
    query = "SELECT movie_id FROM watched WHERE user_id = %s"
    cursor.execute(query, (user_id,))
    results = [row[0] for row in cursor.fetchall()]
    conn.close()
    return results


def query_movies(genres, exclude_ids=[], limit=5):
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)

    # Build placeholders for excluded IDs
    exclude_placeholder = ", ".join(["%s"] * len(exclude_ids)) if exclude_ids else ""

    # SQL query
    query = f"""
        SELECT id, title, release_year 
        FROM movie
        WHERE FIND_IN_SET(%s, mood)
    """
    if exclude_ids:
        query += f" AND id NOT IN ({exclude_placeholder})"
    query += " LIMIT %s"

    # Prepare parameters
    params = [genres[0]]  # Use only the first genre for FIND_IN_SET
    if exclude_ids:
        params.extend(exclude_ids)
    params.append(limit)

    # Debugging
    print("Executing query:", query)
    print("With parameters:", params)

    cursor.execute(query, params)
    results = cursor.fetchall()
    print(f"Query Results: {results}")  # Debug print
    conn.close()
    return results
