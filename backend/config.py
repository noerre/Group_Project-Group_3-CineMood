from dotenv import load_dotenv
import os

# Load variables from .env file
load_dotenv()

db_config = {
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('PORT'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME'),
    'raise_on_warnings': True,
    'api_key': os.getenv('API_KEY')
}
tmdb_api_key = os.getenv('TMDB_API_KEY')