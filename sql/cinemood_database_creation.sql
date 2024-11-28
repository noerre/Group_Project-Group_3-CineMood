CREATE DATABASE cine_mood;
USE cine_mood;

# Table creation 
# Users 

CREATE TABLE users (
	id INT AUTO_INCREMENT PRIMARY KEY, 
    username VARCHAR(20) UNIQUE NOT NULL,
    password VARCHAR(20) NOT NULL
);

# Movies related tables 
CREATE TABLE director (
	id INT AUTO_INCREMENT PRIMARY KEY,
    d_name VARCHAR(20) NOT NULL,
    d_surname VARCHAR(20) NOT NULL
);

CREATE TABLE actor (
	id INT AUTO_INCREMENT PRIMARY KEY, 
    a_name VARCHAR(20) NOT NULL,
    a_surname VARCHAR(20) NOT NULL
);

CREATE TABLE country (
	id CHAR(2) PRIMARY KEY, # alpha-2-code for the country
    country VARCHAR(30) NOT NULL
); 

CREATE TABLE platform (
	id INT AUTO_INCREMENT PRIMARY KEY,
    p_name VARCHAR(20) NOT NULL,
    p_web VARCHAR(100) NOT NULL
);

CREATE TABLE movie (
	id INT AUTO_INCREMENT PRIMARY KEY, 
    title VARCHAR(100) NOT NULL, 
    release_year YEAR, 
    # mood SET, //// we need to decide some moods to our mood column if we are setting it as set
    director_id INT, 
    country_id CHAR(2), 
    platform_id INT, 
    # foreign keys
    CONSTRAINT fk_movie_director FOREIGN KEY (director_id) REFERENCES director(id),
	CONSTRAINT fk_movie_country FOREIGN KEY (country_id) REFERENCES country(id),
    CONSTRAINT fk_movie_platform FOREIGN KEY (platform_id) REFERENCES platform(id)
);

CREATE TABLE cast (
	actor_id INT NOT NULL, 
    movie_id INT NOT NULL, 
    PRIMARY KEY (actor_id, movie_id), 
    CONSTRAINT fk_cast_actor FOREIGN KEY (actor_id) REFERENCES actor(id),
    CONSTRAINT fk_cast_movie FOREIGN KEY (movie_id) REFERENCES movie(id)
);

# User actions 
# save the movies watched by the user 7
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
