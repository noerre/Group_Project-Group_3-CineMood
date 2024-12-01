# db_utils.py
import mysql.connector
from config import db_config


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

