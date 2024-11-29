from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os

from dotenv import load_dotenv
from auth import AuthHandler
from config import db_config

load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["http://localhost", "http://localhost:3000"]}})


@app.route('/')
def home():
    return "CineMood API is running."


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
