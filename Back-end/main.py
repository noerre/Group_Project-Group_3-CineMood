from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt)
from dotenv import load_dotenv
import os

from dotenv import load_dotenv
from auth import AuthHandler
from config import db_config
from schemas import RegisterRequestSchema, LoginRequestSchema, AuthResponseSchema


load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["http://localhost", "http://localhost:3000"]}})

app.config['JWT_SECRET_KEY'] = os.getenv("SECRET_KEY")
jwt = JWTManager(app)


@app.route('/')
def home():
    return "CineMood API is running."


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
