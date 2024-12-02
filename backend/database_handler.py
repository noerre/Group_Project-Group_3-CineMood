import mysql.connector
from mysql.connector import Error


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
            movie_data["platform_id"]
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

# if __name__ == "__main__":
#     DatabaseHandler('localhost', 'root', 'xv3on5', 'cine_mood')