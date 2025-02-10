# CineMood - Group Project (Group 3)

This project provides a movie recommendation application called **CineMood**, designed to suggest movies based on mood and preferences. It includes a backend service handling API requests and database operations, and a frontend interface for user interaction.


## Table of Contents

1. [Overview](#overview)
2. [Installation](#installation)
3. [Running the Application](#running-the-application)
4. [Project Structure](#project-structure)
5. [Technologies Used](#technologies-used)
6. [Features](#features)
7. [Environment Setup](#environment-setup)
8. [Endpoints Overview](#endpoints-overview)
9. [Testing](#testing)
10. [Future Enhancements](#future-enhancements)
11. [Team Contribution](#team-contribution)

---

## Overview
In an era with an ever-increasing amount of available film content, users often struggle to choose the right movie to watch.
CineMood is an innovative movie recommendation platform tailored to users' moods and preferences. 

It leverages external APIs and custom recommendation logic to create personalized experiences for each user. This project exemplifies a combination of robust backend systems with an interactive and responsive frontend.

---

## Installation

To set up the project, clone this repository and run the installation scripts.

### Steps:

1. Clone the repository:
   ```
   git clone https://github.com/noerre/Group_Project-Group_3-CineMood
   cd CineMood
   ```
2. Run the installation script:
   ```
   ./install.sh
   ```
3. Follow the prompts. If any dependency fails, re-run the script after installing missing requirements.

---

## Running the Application

1. **Start the Backend**:

   ```
   python backend/app.py
   ```

   The backend will run on `http://localhost:8000`.

2. **Start the Frontend**:
   ```
   cd Front-end
   npm start
   ```
   The frontend will run on `http://localhost:3000`.
---
### Demo images
Clic on the CineMood button.
![screen1](https://github.com/user-attachments/assets/d4d48508-4899-4297-9fbd-f815b32de792)

Pick your mood. 
![screen2](https://github.com/user-attachments/assets/c81581d2-35fc-4869-beb5-07e8a3992612)

And you will have some great recommendations from the CineMood app!
![screen3](https://github.com/user-attachments/assets/0e249146-ee66-4ef5-91e7-12638c55c019)

You can also get more details from the movies:
![image (14)](https://github.com/user-attachments/assets/12e5e755-528e-4556-9704-611d29626426)

---

## Project Structure

```
CFG-Group_Project-Group_3-CineMood/
│
├── backend/
│   ├── __init__.py                # Backend initialization
│   ├── API_handler.py             # Handles interactions with external APIs
│   ├── app.py                     # Main application setup and route definitions for the Flask backend
│   ├── auth.py                    # User authentication logic (e.g., login, registration, token management)
│   ├── config.py                  # Configuration settings (e.g., database connection, API keys)
│   ├── database_handler.py        # Handles database interactions (CRUD operations)
│   ├── mood_to_genres.py          # Maps user moods to corresponding movie genres
│   ├── recommendation_engine.py   # Core logic for generating movie recommendations
│   ├── schemas.py                 # Marshmallow schemas for serializing and deserializing data
│   ├── test_database_handler_actual_db.py # Tests for database operations using the actual database
│   ├── test_db_handler.py         # Unit tests for database handler functions
│   ├── test_recomendation.py      # Test for recomendation algorythm work
│
├── documentation/
│   ├── 
│
├── Front-end/
│   ├── node_modules/              # Node.js dependencies
│   ├── public/                    # Static assets (e.g., index.html, icons)
│   ├── src/
│       ├── api.js                 # API interaction logic for frontend
│       ├── App.css                # Global styles for the application
│       ├── App.js                 # Main React application component
│       ├── AuthContext.js         # Context provider for user authentication state
│       ├── index.js               # Application entry point for React
│       ├── Login.js               # Login component
│       ├── MoodSelector.js        # Component for selecting user mood
│       ├── MovieCard.css          # Styles for individual movie cards
│       ├── MovieCard.jsx          # Component for displaying movie details
│       ├── Navbar.js              # Navigation bar component
│       ├── ProtectedRoute.js      # Higher-order component for protected routes
│       ├── Recommendations.js     # Displays movie recommendations
│       ├── Register.js            # User registration component
│       ├── search.svg             # Search icon used in the application
│       ├── .env                   # Environment variables

│
├── sql/
│   ├── cinemood_database_creation.sql  # SQL script to create the CineMood database schema
│   ├── Cine_mood_mock_data.sql         # SQL script to create a mock data for the CineMood database 
│   ├── init_database.py                # Python script to initialize the database
│   ├── test_queries_cinemood.sql       # SQL queries for testing database setup
│
├── tests/
│   ├── __init__.py                     # Test initialization
│   ├── TestApp.py                      # Tests for the Flask application
│   ├── TestAuthHandler.py              # Tests for authentication logic
│
├── venv/                               # Python virtual environment (dependencies managed here)
├── .env                                # Environment variables (excluded from version control)
├── .gitignore                          # Specifies intentionally untracked files
├── install.sh                          # Bash script for setting up the project
├── requirements.txt                    # Python dependencies
└── README.md                           # Project documentation (this file)
```
---
## Technologies used 

- **Python 3.x** (Back-end)
- **React.js** (Front-end)
- **Standard Libraries**:
    - `itertools`
    - `collections`
    - `unittest`
- **External Libraries**:
    - `requests` (for API communication)
    - `Flask` (to build API handling app)
    - `Flask-Cors` (to habilitate Cross-Origin Resource Sharing in backend routes)
    - `Flask-JWT-Extended` (to manage the aunthentication through JWT)
    - `pytest` (for test automation)
    - `mysql-connector-python` (for MySQL database handling)
    - `TMDbv3API` (to interact with TBDb)
- **API**:
    - The Movie Database (TMDb) API 
- **Database**:
    - MySQL: A relational database suitable for medium to large-scale projects, providing robust data handling capabilities.
- **Version Control**:
    - Git: For version control and team collaboration.
---
## Features

1. **User Authentication**: Users can register, login, and logout.
2. **Mood-Based Recommendations**: Suggests movies based on user-selected mood.
3. **Search Functionality**: Allows users to search for movies by title.
4. **Responsive Design**: The frontend is styled using Bootstrap and CSS for responsiveness.

---

## Environment Setup

### Backend Environment Variables:

Create a `.env` file in the root directory with the following content:

```
DB_HOST=localhost
PORT=3306
DB_USER=your_mysql_username
DB_PASSWORD=your_mysql_password
DB_NAME=cine_mood
TMDB_API_KEY=your_tmdb_api_key
API_KEY=your_tmdb_API_Read_Access_Token
```

Replace placeholders with your actual credentials.
You can get the API keys at: https://developer.themoviedb.org/docs/getting-started

Note:

- **Security**: Ensure that the .env file is added to .gitignore to protect sensitive information.

### Frontend Environment:

Create a `Front-end/.env` file in the Front-end directory with the following content:

```
REACT_APP_TMDB_API_KEY==your_tmdb_api_key
```

All frontend files are located in the `Front-end` folder. Use `npm` to install dependencies.

---

## Endpoints Overview

### Backend API Endpoints:

- **POST `/login`**: Authenticates user credentials.
- **POST `/register`**: Registers a new user.
- **POST `/recommendations`**: Fetches movie recommendations based on mood.
- **GET `/search`**: Searches movies using the OMDB API.

### Frontend Pages:

- **`/`**: Home page with search and mood-based navigation.
- **`/questions`**: Mood selection page.
- **`/recommendations`**: Displays recommended movies.
- **`/login`**: Login page.
- **`/register`**: Registration page.

---

## Testing

- Unit tests for backend logic are located in the `tests` folder.
- Run tests with:
  ```
  pytest tests/
  ```

---

## Future Enhancements

1. Add user-specific recommendations based on past activity.
2. Allow users to rate and review movies.
3. Add support for multiple languages.
4. Improve recommendation engine using machine learning.
5. Allow users to ask for more recommendations. 

---

## Team Contribution

Each team member contributed to the development of the backend, frontend, and database design.

- **Justyna Gadjek:** Aunthentication design and implementation, Front-end implementation, system testing and installation, documentation.
- **Hermella Kebede:** Database handler and API handler implementation, documentation.
- **Magdalena Kurek:** Front-end design and implementation, system testing and installation.
- **Aleksandra Dragan:** Recommendations algorithm.
- **Pamela Smardz:** Recommendations algorithm implementation, API implementation, System testing and installation, documentation.
- **Noelia Ruiz Barrales:** Database design and implementation, Database handler implementation, documentation. 

You can check a more detailed task list in [our Activity log](https://docs.google.com/spreadsheets/d/1DOLx7TO7IC1AGiFcujOuicCbr9boKwiO/edit?usp=sharing&ouid=106111739777230038037&rtpof=true&sd=true).


