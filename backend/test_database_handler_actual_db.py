from database_handler import DatabaseHandler
from config import db_config

def test_database_handler():
    db_handler = DatabaseHandler(db_config)

    if db_handler.test_connection():
        print("Successful connnection")

        director_id = 1234
        director_name = "Steven Spielberg"
        db_handler.add_director(director_id, director_name)
        db_handler.check_record("director", "id", 1234)
        db_handler.check_record("director", "id", 10)

        actor_id = 100
        actor_name = "Tina Turner"
        db_handler.add_actor(actor_id, actor_name)

        genre_id = 4
        genre_name = "Drama"
        db_handler.add_genre(genre_id, genre_name)

        mood_id = "Angry"
        db_handler.add_mood(mood_id)

        movie_data = {
            "id": 5678,
            "title": "Jurassic Park",
            "release_year": 1993,
            "director_id": director_id,
            "country_id": "US"
        }
        db_handler.add_movie(movie_data)

        movie_id = db_handler.get_movie_id("Jurassic Park")
        db_handler.add_cast(actor_id, movie_id)

        db_handler.add_genre(movie_id, genre_id)
        movie = db_handler.get_movie_by_title("Jurassic Park")
        print(movie)

        db_handler.close_connection()
    else:
        print("Connection error")



if __name__ == "__main__":
    test_database_handler()
