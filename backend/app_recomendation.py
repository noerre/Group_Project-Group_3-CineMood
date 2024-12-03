from flask import Flask, request, jsonify
from flask_cors import CORS
import os

from dotenv import load_dotenv
from recomendation_engine import recommend_movies
from mood_to_genres import get_genres_for_mood


def create_app(test_config=None):
    """
    Factory function to create and configure the Flask application.
    """
    load_dotenv()
    app = Flask(__name__)

    # Configure CORS
    CORS(app, resources={r"/*": {"origins": ["http://localhost", "http://localhost:3000"]}})

    # Allow testing configuration overrides
    if test_config:
        app.config.update(test_config)

    @app.route('/')
    def home():
        """
        Home endpoint to verify that the API is running.
        """
        return "CineMood API is running."

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

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=8000, debug=True)