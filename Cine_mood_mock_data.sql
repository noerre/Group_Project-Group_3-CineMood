CREATE DATABASE cine_mood;
use cine_mood;
CREATE TABLE users (
	id INT AUTO_INCREMENT PRIMARY KEY, 
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);


# Movies related tables 
CREATE TABLE director (
	id INT PRIMARY KEY, 
    d_name VARCHAR(255) NOT NULL
);

CREATE TABLE actor (
	id INT PRIMARY KEY, 
    a_name VARCHAR(255) NOT NULL
);

CREATE TABLE country (
	id CHAR(2) PRIMARY KEY, # alpha-2-code for the country
    country VARCHAR(100) NOT NULL
); 

CREATE TABLE platform (
	id INT AUTO_INCREMENT PRIMARY KEY,
    p_name VARCHAR(20) NOT NULL,
    p_web VARCHAR(100) NOT NULL
);


CREATE TABLE movie (
	id INT PRIMARY KEY, 
    title VARCHAR(255) NOT NULL, 
    release_year YEAR, 
    director_id INT, 
    country_id CHAR(2), 
    # foreign keys
    CONSTRAINT fk_movie_director FOREIGN KEY (director_id) REFERENCES director(id),
	CONSTRAINT fk_movie_country FOREIGN KEY (country_id) REFERENCES country(id)
);

CREATE TABLE movie_platform (
	platform_id INT NOT NULL, 
    movie_id INT NOT NULL, 
    PRIMARY KEY (platform_id, movie_id), 
    CONSTRAINT fk_movie_platform_platf FOREIGN KEY (platform_id) REFERENCES platform(id),
    CONSTRAINT fk_movie_platform_movie FOREIGN KEY (movie_id) REFERENCES movie(id)
);

CREATE TABLE cast (
	actor_id INT NOT NULL, 
    movie_id INT NOT NULL, 
    PRIMARY KEY (actor_id, movie_id), 
    CONSTRAINT fk_cast_actor FOREIGN KEY (actor_id) REFERENCES actor(id),
    CONSTRAINT fk_cast_movie FOREIGN KEY (movie_id) REFERENCES movie(id)
);

CREATE TABLE genre(
	id INT PRIMARY KEY, 
    genre VARCHAR(20) NOT NULL UNIQUE 
);

CREATE TABLE movie_genre(
	movie_id INT NOT NULL, 
    genre_id INT NOT NULL, 
    PRIMARY KEY (movie_id, genre_id), 
    CONSTRAINT fk_movie_genre_movie FOREIGN KEY (movie_id) REFERENCES movie(id),
    CONSTRAINT fk_movie_genre_genre FOREIGN KEY (genre_id) REFERENCES genre(id)
);

CREATE TABLE mood(
	id INT AUTO_INCREMENT PRIMARY KEY, 
    mood VARCHAR(20) NOT NULL UNIQUE 
);

CREATE TABLE movie_mood(
	movie_id INT NOT NULL, 
    mood_id INT NOT NULL, 
    PRIMARY KEY (movie_id, mood_id), 
    CONSTRAINT fk_movie_mood_movie FOREIGN KEY (movie_id) REFERENCES movie(id),
    CONSTRAINT fk_movie_mood_mood FOREIGN KEY (mood_id) REFERENCES mood(id)
);

# User actions 
# save the movies watched by the user 
CREATE TABLE watched (
	user_id INT NOT NULL, 
    movie_id INT NOT NULL, 
    PRIMARY KEY (user_id, movie_id), 
    CONSTRAINT fk_watched_user FOREIGN KEY (user_id) REFERENCES users(id), 
    CONSTRAINT fk_watched_movie FOREIGN KEY (movie_id) REFERENCES movie(id)
);

# save the ratings 
CREATE TABLE rating (
	id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL, 
    movie_id INT NOT NULL, 
    rating INT NOT NULL CHECK (rating BETWEEN 1 AND 5),
    review TEXT,
    CONSTRAINT fk_rating_user FOREIGN KEY (user_id) REFERENCES users(id),
    CONSTRAINT fk_rating_movie FOREIGN KEY (movie_id) REFERENCES movie(id)
);

# recommendations our app made to users 
CREATE TABLE recommendations (
    user_id INT NOT NULL,
    movie_id INT NOT NULL,
    recommended_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, movie_id),
    CONSTRAINT fk_recommendations_user FOREIGN KEY (user_id) REFERENCES users(id),
    CONSTRAINT fk_recommendations_movie FOREIGN KEY (movie_id) REFERENCES movie(id)
);
-- Insert into Users
-- Insert Mock Data into Users Table
INSERT INTO users (username, password, failed_attempts, lockout_time) VALUES
('user1', 'password1', 3, '2024-12-07 12:30:00'), -- Simulating a user with failed attempts and a lockout time
('user2', 'password2', 0, NULL),                  -- No failed attempts or lockout time
('user3', 'password3', 1, NULL),                  -- 1 failed attempt but no lockout
('user4', 'password4', 5, '2024-12-07 13:00:00'); -- A user with the maximum failed attempts and a lockout time


-- Insert into Director
INSERT INTO director (id, d_name) VALUES 
(1, 'Christopher Nolan'),
(2, 'Quentin Tarantino'),
(3, 'Steven Spielberg');

-- Insert into Actor
INSERT INTO actor (id, a_name) VALUES 
(1, 'Leonardo DiCaprio'),
(2, 'Morgan Freeman'),
(3, 'Scarlett Johansson');

-- Insert into Country
INSERT INTO country (id, country) VALUES 
('US', 'United States'),
('UK', 'United Kingdom'),
('CA', 'Canada');

-- Insert into Platform
INSERT INTO platform (p_name, p_web) VALUES 
('Netflix', 'https://www.netflix.com'),
('Amazon Prime', 'https://www.primevideo.com'),
('Disney+', 'https://www.disneyplus.com');

-- Insert into Movies
INSERT INTO movie (id, title, release_year, director_id, country_id) VALUES 
(1, 'Inception', 2010, 1, 'US'),
(2, 'Pulp Fiction', 1994, 2, 'US'),
(3, 'Jurassic Park', 1993, 3, 'US');

-- Insert into Movie Platform
INSERT INTO movie_platform (platform_id, movie_id) VALUES 
(1, 1),
(2, 1),
(1, 2),
(3, 3);

-- Insert into Cast
INSERT INTO cast (actor_id, movie_id) VALUES 
(1, 1),
(2, 2),
(3, 3);

-- Insert into Genre
INSERT INTO genre (id, genre) VALUES 
(1, 'Action'),
(2, 'Thriller'),
(3, 'Adventure');

-- Insert into Movie Genre
INSERT INTO movie_genre (movie_id, genre_id) VALUES 
(1, 1),
(1, 2),
(2, 1),
(3, 3);

-- Insert into Mood
INSERT INTO mood (mood) VALUES 
('Exciting'),
('Suspenseful'),
('Adventurous');

-- Insert into Movie Mood
INSERT INTO movie_mood (movie_id, mood_id) VALUES 
(1, 1),
(2, 2),
(3, 3);

-- Insert into Watched
INSERT INTO watched (user_id, movie_id) VALUES 
(1, 1),
(2, 2),
(3, 3);

-- Insert into Rating
INSERT INTO rating (user_id, movie_id, rating, review) VALUES 
(1, 1, 5, 'Mind-blowing! A must-watch.'),
(2, 2, 4, 'Great dialogues and storytelling.'),
(3, 3, 5, 'Timeless classic!');

-- Insert into Recommendations
INSERT INTO recommendations (user_id, movie_id, recommended_at) VALUES 
(1, 2, NOW()),
(2, 3, NOW()),
(3, 1, NOW());

ALTER TABLE users
ADD COLUMN failed_attempts INT NOT NULL DEFAULT 0,
ADD COLUMN lockout_time DATETIME NULL;
SET SQL_SAFE_UPDATES = 0;
UPDATE users
SET failed_attempts = 0,
    lockout_time = NULL;