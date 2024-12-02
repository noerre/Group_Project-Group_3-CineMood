import mysql.connector
from mysql.connector import errors
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Database configuration
db_config = {
    'host': os.getenv('DB_HOST'),
    'port': int(os.getenv('PORT', 3306)),  # Use 3306 as the default port
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
}

# Initialize Database
def init_db():
    try:
        # Connect to the server (without specifying the database)
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Create database if it doesn't exist
        cursor.execute("CREATE DATABASE IF NOT EXISTS cine_mood;")
        print("Database 'cine_mood' created or already exists.")

        # Close connection
        cursor.close()
        conn.close()
    except errors.ProgrammingError as e:
        if e.errno == 1049:  # Error code for "Unknown database"
            raise Exception("Database does not exist and could not be created.")
        else:
            raise e
    except Exception as ex:
        print(f"An error occurred: {ex}")

# Call the function
init_db()
