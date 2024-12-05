from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt)
import os

from dotenv import load_dotenv
from auth import AuthHandler
from config import db_config
from schemas import RegisterRequestSchema, LoginRequestSchema, AuthResponseSchema
from recomendation_engine import recommend_movies
from mood_to_genres import get_genres_for_mood

def create_app(test_config=None):
    """
    Factory function to create and configure the Flask application.

    :param test_config: Optional dictionary to override default configurations for testing.
    :return: Configured Flask application.
    """

    load_dotenv()

    # Initialize the Flask application
    app = Flask(__name__)

    # Configure Cross-Origin Resource Sharing (CORS)
    # This allows the frontend application running on localhost and port 3000 to interact with the backend
    CORS(app, resources={r"/*": {"origins": ["http://localhost", "http://localhost:3000"]}})

    # Configure JWT (JSON Web Token) with a secret key sourced from environment variables
    # This key is used to securely sign the JWT tokens
    app.config['JWT_SECRET_KEY'] = os.getenv("SECRET_KEY")

    # Allow testing configuration overrides
    if test_config:
        app.config.update(test_config)

    jwt = JWTManager(app)

    # Initialize the AuthHandler with the database configuration
    # AuthHandler manages user authentication, registration, and token revocation
    auth_handler = AuthHandler(db_config)

    # Set to store revoked JWT tokens (for logout functionality)
    # When a user logs out, their token's JTI (JWT ID) is added to this set to prevent further use
    revoked_tokens = set()

    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload):
        """
        Callback function to check if a JWT token has been revoked.

        :param jwt_header: The header part of the JWT.
        :param jwt_payload: The payload part of the JWT.
        :return: True if the token is revoked, False otherwise.
        """
        jti = jwt_payload['jti']
        return auth_handler.is_token_revoked(jti)

    @app.route('/')
    def home():
        """
        Home endpoint to verify that the API is running.

        :return: A simple message indicating the API status.
        """
        return "CineMood API is running."

    @app.route('/register', methods=['POST'])
    def register():
        """
        Endpoint to register a new user.

        Expects a JSON payload with 'username' and 'password'.
        Validates the input, registers the user, and returns a JWT access token.

        :return: JSON response with user information and access token or error message.
        """
        data = request.get_json()
        schema = RegisterRequestSchema()

        # Validate the incoming request data
        errors = schema.validate(data)
        if errors:
            return jsonify({"errors": errors}), 400

        username = data.get('username')
        password = data.get('password')

        try:
            # Register the user using AuthHandler
            auth_handler.register_user(username, password)

            # Create a JWT access token for the new user
            access_token = create_access_token(identity=username)

            # Prepare the response data
            response = {
                "username": username,
                "is_guest": False,
                "access_token": access_token
            }

            # Validate the response schema
            response_schema = AuthResponseSchema()
            result = response_schema.dump(response)

            return jsonify(result), 201
        except Exception as e:
            # Return an error message if registration fails
            return jsonify({"error": str(e)}), 400

    @app.route('/login', methods=['POST'])
    def login():
        """
        Endpoint to log in an existing user.

        Expects a JSON payload with 'username' and 'password'.
        Validates the input, authenticates the user, and returns a JWT access token.

        :return: JSON response with user information and access token or error message.
        """
        data = request.get_json()
        schema = LoginRequestSchema()

        # Validate the incoming request data
        errors = schema.validate(data)
        if errors:
            return jsonify({"errors": errors}), 400

        username = data.get('username')
        password = data.get('password')

        try:
            # Authenticate the user using AuthHandler
            user_info = auth_handler.login_user(username, password)

            # Create a JWT access token for the authenticated user
            access_token = create_access_token(identity=username)

            # Prepare the response data
            response = {
                "username": username,
                "is_guest": user_info.get('is_guest', False),
                "access_token": access_token
            }

            # Validate the response schema
            response_schema = AuthResponseSchema()
            result = response_schema.dump(response)

            return jsonify(result), 200
        except Exception as e:
            # Return an error message if authentication fails
            return jsonify({"error": str(e)}), 401

    @app.route('/logout', methods=['POST'])
    @jwt_required()
    def logout():
        """
        Endpoint to log out a user by revoking their JWT token.

        Requires a valid JWT token in the request headers.
        Adds the token's JTI to the revoked tokens set.

        :return: JSON response confirming successful logout or error message.
        """
        jti = get_jwt()['jti']
        try:
            # Revoke the token using AuthHandler
            auth_handler.logout_user(jti)
            revoked_tokens.add(jti)
            return jsonify({"msg": "Successfully logged out."}), 200
        except Exception as e:
            # Return an error message if logout fails
            return jsonify({"error": str(e)}), 400

    @app.route('/protected', methods=['GET'])
    @jwt_required()
    def protected():
        """
        Protected endpoint accessible only to authenticated users.

        Requires a valid JWT token in the request headers.
        Returns a personalized greeting message.

        :return: JSON response with a welcome message.
        """
        current_user = get_jwt_identity()
        return jsonify({"msg": f"Hello, {current_user}! This is a protected endpoint."}), 200

    @app.route('/login_guest', methods=['POST'])
    def login_guest():
        """
        Endpoint to log in as a guest user.

        Creates a temporary guest user profile without saving it to the database.

        :return: JSON response with guest user information and access token.
        """
        try:
            # Log in as guest using AuthHandler
            guest_info = auth_handler.login_guest()

            # Create a JWT access token for the guest user
            access_token = create_access_token(identity=guest_info['username'])

            # Prepare the response data
            response = {
                "username": guest_info['username'],
                "is_guest": guest_info['is_guest'],
                "access_token": access_token
            }

            # Validate the response schema
            response_schema = AuthResponseSchema()
            result = response_schema.dump(response)

            return jsonify(result), 200
        except Exception as e:
            # Return an error message if guest login fails
            return jsonify({"error": str(e)}), 400
    @app.route('/recommendations', methods=['POST'])
    def get_recommendations():
        data = request.get_json()  # Get JSON payload from the request
        mood = data.get("mood", "")

        try:
            if isinstance(mood, str):
                mood = mood.lower()  # Ensure the mood is lowercase
            else:
                raise ValueError("Mood must be a string.")

            # Fetch genres for the given mood
            genres = get_genres_for_mood(mood)
            print(f"Genres for mood '{mood}': {genres}")  # Debug print

            user_id = 1  # Temporary user ID for testing
            recommendations = recommend_movies(user_id, mood)
            print(f"Recommendations: {recommendations}")  # Debug print
            return jsonify(recommendations), 200
        except Exception as e:
            print(f"Error: {e}")
            return jsonify({"error": str(e)}), 400

    @app.route('/movie_history', methods=['POST'])
    def get_history():
        """
        get user movie history and show it
        :return:
        """


    return app


if __name__ == "__main__":
    """
    Entry point for running the Flask application.

    Configures the host and port, and enables debug mode for development.
    """
    app = create_app()
    app.run(host="0.0.0.0", port=8000, debug=True)