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

        # Drop database if it exists
        cursor.execute("DROP DATABASE IF EXISTS cine_mood;")
        print("Database 'cine_mood' dropped.")

        # Create database
        cursor.execute("CREATE DATABASE cine_mood;")
        print("Database 'cine_mood' created.")

        # Close connection
        cursor.close()
        conn.close()
    except Exception as ex:
        print(f"An error occurred: {ex}")


# Execute SQL file
def execute_sql_file(file_path):
    try:
        # Connect to the database
        conn = mysql.connector.connect(**db_config, database='cine_mood')
        cursor = conn.cursor()

        # Read the SQL file
        with open(file_path, 'r') as sql_file:
            sql_commands = sql_file.read()

        # Execute each command in the SQL file
        for command in sql_commands.split(';'):
            if command.strip():  # Skip empty commands
                cursor.execute(command)

        # Commit changes and close connection
        conn.commit()
        print(f"Executed SQL file: {file_path}")
        cursor.close()
        conn.close()
    except Exception as ex:
        print(f"An error occurred while executing the SQL file: {ex}")


# Call the functions
init_db()
execute_sql_file('cinemood_database_creation.sql')
