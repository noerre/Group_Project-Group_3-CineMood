import requests

# API base URL
base_url = "http://localhost:8000"

# Fetch recommendations
recommendations_payload = {"mood": "happy"}

try:
    response = requests.post(f"{base_url}/recommendations", json=recommendations_payload)

    if response.status_code == 200:
        print("Recommendations fetched successfully:")
        recommendations = response.json()

        # Extract and print only movie titles
        movie_titles = [movie['title'] for movie in recommendations]
        print("\nMovie Titles:")
        for title in movie_titles:
            print(f"- {title}")
    else:
        print(f"Failed to fetch recommendations. Status code: {response.status_code}")
        print("Error:")
        print(response.json())
except requests.exceptions.RequestException as e:
    print(f"An error occurred while making the request: {e}")
