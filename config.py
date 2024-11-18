from dotenv import load_dotenv
import os

# Load variables from .env file
load_dotenv()

DB_HOST = os.getenv('DB_HOST')
PORT = os.getenv('PORT')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')