# DROP DATABASE cine_mood;
CREATE DATABASE cine_mood;
 
USE cine_mood;

# Table creation 
# Users 

CREATE TABLE users (
	id INT AUTO_INCREMENT PRIMARY KEY, 
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
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
    title VARCHAR(255) NOT NULL, 
    release_year YEAR, 
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

CREATE TABLE genre(
	id INT AUTO_INCREMENT PRIMARY KEY, 
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

/*-----------------------------------------
----- FEEDING DB WITH STATIC DATA ---------
-------------------------------------------*/
# Countries 
INSERT INTO country (id, country) VALUES ('US', 'United States');
INSERT INTO country (id, country) VALUES ('GB', 'United Kingdom');
INSERT INTO country (id, country) VALUES ('CA', 'Canada');
INSERT INTO country (id, country) VALUES ('AU', 'Australia');
INSERT INTO country (id, country) VALUES ('FR', 'France');
INSERT INTO country (id, country) VALUES ('DE', 'Germany');
INSERT INTO country (id, country) VALUES ('IT', 'Italy');
INSERT INTO country (id, country) VALUES ('ES', 'Spain');
INSERT INTO country (id, country) VALUES ('BR', 'Brazil');
INSERT INTO country (id, country) VALUES ('MX', 'Mexico');
INSERT INTO country (id, country) VALUES ('IN', 'India');
INSERT INTO country (id, country) VALUES ('JP', 'Japan');
INSERT INTO country (id, country) VALUES ('KR', 'South Korea');
INSERT INTO country (id, country) VALUES ('CN', 'China');
INSERT INTO country (id, country) VALUES ('RU', 'Russia');
INSERT INTO country (id, country) VALUES ('SE', 'Sweden');
INSERT INTO country (id, country) VALUES ('FI', 'Finland');
INSERT INTO country (id, country) VALUES ('NO', 'Norway');
INSERT INTO country (id, country) VALUES ('DK', 'Denmark');
INSERT INTO country (id, country) VALUES ('NL', 'Netherlands');
INSERT INTO country (id, country) VALUES ('BE', 'Belgium');
INSERT INTO country (id, country) VALUES ('CH', 'Switzerland');
INSERT INTO country (id, country) VALUES ('AT', 'Austria');
INSERT INTO country (id, country) VALUES ('PL', 'Poland');
INSERT INTO country (id, country) VALUES ('UA', 'Ukraine');
INSERT INTO country (id, country) VALUES ('PT', 'Portugal');
INSERT INTO country (id, country) VALUES ('AR', 'Argentina');
INSERT INTO country (id, country) VALUES ('CO', 'Colombia');
INSERT INTO country (id, country) VALUES ('CL', 'Chile');
INSERT INTO country (id, country) VALUES ('PE', 'Peru');
INSERT INTO country (id, country) VALUES ('VE', 'Venezuela');
INSERT INTO country (id, country) VALUES ('EG', 'Egypt');
INSERT INTO country (id, country) VALUES ('ZA', 'South Africa');

# Platforms 
INSERT INTO platform (p_name, p_web) VALUES ('Netflix', 'https://www.netflix.com');
INSERT INTO platform (p_name, p_web) VALUES ('Hulu', 'https://www.hulu.com');
INSERT INTO platform (p_name, p_web) VALUES ('Amazon Prime Video', 'https://www.amazon.com/Prime-Video');
INSERT INTO platform (p_name, p_web) VALUES ('Disney+', 'https://www.disneyplus.com');
INSERT INTO platform (p_name, p_web) VALUES ('HBO Max', 'https://www.hbomax.com');
INSERT INTO platform (p_name, p_web) VALUES ('Apple TV+', 'https://www.apple.com/tv/');

# Moods 
INSERT INTO mood (mood) VALUES ('Happy');
INSERT INTO mood (mood) VALUES ('Sad');
INSERT INTO mood (mood) VALUES ('Excited');
INSERT INTO mood (mood) VALUES ('Relaxed');
INSERT INTO mood (mood) VALUES ('Romantic');
INSERT INTO mood (mood) VALUES ('Angry');
INSERT INTO mood (mood) VALUES ('Nostalgic');
INSERT INTO mood (mood) VALUES ('Adventurous');

# Genres
INSERT INTO genre (genre) VALUES ('Action');
INSERT INTO genre (genre) VALUES ('Comedy');
INSERT INTO genre (genre) VALUES ('Drama');
INSERT INTO genre (genre) VALUES ('Romance');
INSERT INTO genre (genre) VALUES ('Thriller');
INSERT INTO genre (genre) VALUES ('Horror');
INSERT INTO genre (genre) VALUES ('Fantasy');
INSERT INTO genre (genre) VALUES ('Adventure');
INSERT INTO genre (genre) VALUES ('Sci-Fi');
INSERT INTO genre (genre) VALUES ('Animation');
INSERT INTO genre (genre) VALUES ('Mystery');
INSERT INTO genre (genre) VALUES ('Documentary');
INSERT INTO genre (genre) VALUES ('Musical');
INSERT INTO genre (genre) VALUES ('Crime');
INSERT INTO genre (genre) VALUES ('History');
INSERT INTO genre (genre) VALUES ('War');
INSERT INTO genre (genre) VALUES ('Western');
INSERT INTO genre (genre) VALUES ('Family');
INSERT INTO genre (genre) VALUES ('Classic');

