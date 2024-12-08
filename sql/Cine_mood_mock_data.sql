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


-- Insert into Movie Genre
INSERT INTO movie_genre (movie_id, genre_id) VALUES 
(1, 1),
(1, 2),
(2, 1),
(3, 3);

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

