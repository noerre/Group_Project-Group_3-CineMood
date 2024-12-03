#DROP DATABASE cine_mood;
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



/*-----------------------------------------
----- FEEDING DB WITH STATIC DATA ---------
-------------------------------------------*/
# Countries 
INSERT INTO country (id, country) VALUES ('AD', 'Andorra');
INSERT INTO country (id, country) VALUES ('AE', 'United Arab Emirates');
INSERT INTO country (id, country) VALUES ('AF', 'Afghanistan');
INSERT INTO country (id, country) VALUES ('AG', 'Antigua and Barbuda');
INSERT INTO country (id, country) VALUES ('AI', 'Anguilla');
INSERT INTO country (id, country) VALUES ('AL', 'Albania');
INSERT INTO country (id, country) VALUES ('AM', 'Armenia');
INSERT INTO country (id, country) VALUES ('AO', 'Angola');
INSERT INTO country (id, country) VALUES ('AR', 'Argentina');
INSERT INTO country (id, country) VALUES ('AS', 'American Samoa');
INSERT INTO country (id, country) VALUES ('AT', 'Austria');
INSERT INTO country (id, country) VALUES ('AU', 'Australia');
INSERT INTO country (id, country) VALUES ('AW', 'Aruba');
INSERT INTO country (id, country) VALUES ('AX', 'Åland Islands');
INSERT INTO country (id, country) VALUES ('AZ', 'Azerbaijan');
INSERT INTO country (id, country) VALUES ('BA', 'Bosnia and Herzegovina');
INSERT INTO country (id, country) VALUES ('BB', 'Barbados');
INSERT INTO country (id, country) VALUES ('BD', 'Bangladesh');
INSERT INTO country (id, country) VALUES ('BE', 'Belgium');
INSERT INTO country (id, country) VALUES ('BF', 'Burkina Faso');
INSERT INTO country (id, country) VALUES ('BG', 'Bulgaria');
INSERT INTO country (id, country) VALUES ('BH', 'Bahrain');
INSERT INTO country (id, country) VALUES ('BI', 'Burundi');
INSERT INTO country (id, country) VALUES ('BJ', 'Benin');
INSERT INTO country (id, country) VALUES ('BL', 'Saint Barthélemy');
INSERT INTO country (id, country) VALUES ('BM', 'Bermuda');
INSERT INTO country (id, country) VALUES ('BN', 'Brunei Darussalam');
INSERT INTO country (id, country) VALUES ('BO', 'Bolivia');
INSERT INTO country (id, country) VALUES ('BQ', 'Bonaire, Sint Eustatius and Saba');
INSERT INTO country (id, country) VALUES ('BR', 'Brazil');
INSERT INTO country (id, country) VALUES ('BS', 'Bahamas');
INSERT INTO country (id, country) VALUES ('BT', 'Bhutan');
INSERT INTO country (id, country) VALUES ('BV', 'Bouvet Island');
INSERT INTO country (id, country) VALUES ('BW', 'Botswana');
INSERT INTO country (id, country) VALUES ('BY', 'Belarus');
INSERT INTO country (id, country) VALUES ('BZ', 'Belize');
INSERT INTO country (id, country) VALUES ('CA', 'Canada');
INSERT INTO country (id, country) VALUES ('CC', 'Cocos (Keeling) Islands');
INSERT INTO country (id, country) VALUES ('CD', 'Congo (Democratic Republic)');
INSERT INTO country (id, country) VALUES ('CF', 'Central African Republic');
INSERT INTO country (id, country) VALUES ('CG', 'Congo');
INSERT INTO country (id, country) VALUES ('CH', 'Switzerland');
INSERT INTO country (id, country) VALUES ('CI', 'Ivory Coast');
INSERT INTO country (id, country) VALUES ('CK', 'Cook Islands');
INSERT INTO country (id, country) VALUES ('CL', 'Chile');
INSERT INTO country (id, country) VALUES ('CM', 'Cameroon');
INSERT INTO country (id, country) VALUES ('CN', 'China');
INSERT INTO country (id, country) VALUES ('CO', 'Colombia');
INSERT INTO country (id, country) VALUES ('CR', 'Costa Rica');
INSERT INTO country (id, country) VALUES ('CU', 'Cuba');
INSERT INTO country (id, country) VALUES ('CV', 'Cabo Verde');
INSERT INTO country (id, country) VALUES ('CW', 'Curaçao');
INSERT INTO country (id, country) VALUES ('CX', 'Christmas Island');
INSERT INTO country (id, country) VALUES ('CY', 'Cyprus');
INSERT INTO country (id, country) VALUES ('CZ', 'Czech Republic');
INSERT INTO country (id, country) VALUES ('DE', 'Germany');
INSERT INTO country (id, country) VALUES ('DJ', 'Djibouti');
INSERT INTO country (id, country) VALUES ('DK', 'Denmark');
INSERT INTO country (id, country) VALUES ('DM', 'Dominica');
INSERT INTO country (id, country) VALUES ('DO', 'Dominican Republic');
INSERT INTO country (id, country) VALUES ('DZ', 'Algeria');
INSERT INTO country (id, country) VALUES ('EC', 'Ecuador');
INSERT INTO country (id, country) VALUES ('EE', 'Estonia');
INSERT INTO country (id, country) VALUES ('EG', 'Egypt');
INSERT INTO country (id, country) VALUES ('EH', 'Western Sahara');
INSERT INTO country (id, country) VALUES ('ER', 'Eritrea');
INSERT INTO country (id, country) VALUES ('ES', 'Spain');
INSERT INTO country (id, country) VALUES ('ET', 'Ethiopia');
INSERT INTO country (id, country) VALUES ('FI', 'Finland');
INSERT INTO country (id, country) VALUES ('FJ', 'Fiji');
INSERT INTO country (id, country) VALUES ('FM', 'Micronesia');
INSERT INTO country (id, country) VALUES ('FO', 'Faroe Islands');
INSERT INTO country (id, country) VALUES ('FR', 'France');
INSERT INTO country (id, country) VALUES ('GA', 'Gabon');
INSERT INTO country (id, country) VALUES ('GB', 'United Kingdom');
INSERT INTO country (id, country) VALUES ('GD', 'Grenada');
INSERT INTO country (id, country) VALUES ('GE', 'Georgia');
INSERT INTO country (id, country) VALUES ('GF', 'French Guiana');
INSERT INTO country (id, country) VALUES ('GG', 'Guernsey');
INSERT INTO country (id, country) VALUES ('GH', 'Ghana');
INSERT INTO country (id, country) VALUES ('GI', 'Gibraltar');
INSERT INTO country (id, country) VALUES ('GL', 'Greenland');
INSERT INTO country (id, country) VALUES ('GM', 'Gambia');
INSERT INTO country (id, country) VALUES ('GN', 'Guinea');
INSERT INTO country (id, country) VALUES ('GP', 'Guadeloupe');
INSERT INTO country (id, country) VALUES ('GQ', 'Equatorial Guinea');
INSERT INTO country (id, country) VALUES ('GR', 'Greece');
INSERT INTO country (id, country) VALUES ('GT', 'Guatemala');
INSERT INTO country (id, country) VALUES ('GU', 'Guam');
INSERT INTO country (id, country) VALUES ('GW', 'Guinea-Bissau');
INSERT INTO country (id, country) VALUES ('GY', 'Guyana');
INSERT INTO country (id, country) VALUES ('HK', 'Hong Kong');
INSERT INTO country (id, country) VALUES ('HM', 'Heard Island and McDonald Islands');
INSERT INTO country (id, country) VALUES ('HN', 'Honduras');
INSERT INTO country (id, country) VALUES ('HR', 'Croatia');
INSERT INTO country (id, country) VALUES ('HT', 'Haiti');
INSERT INTO country (id, country) VALUES ('HU', 'Hungary');
INSERT INTO country (id, country) VALUES ('ID', 'Indonesia');
INSERT INTO country (id, country) VALUES ('IE', 'Ireland');
INSERT INTO country (id, country) VALUES ('IL', 'Israel');
INSERT INTO country (id, country) VALUES ('IM', 'Isle of Man');
INSERT INTO country (id, country) VALUES ('IN', 'India');
INSERT INTO country (id, country) VALUES ('IO', 'British Indian Ocean Territory');
INSERT INTO country (id, country) VALUES ('IQ', 'Iraq');
INSERT INTO country (id, country) VALUES ('IR', 'Iran');
INSERT INTO country (id, country) VALUES ('IS', 'Iceland');
INSERT INTO country (id, country) VALUES ('IT', 'Italy');
INSERT INTO country (id, country) VALUES ('JE', 'Jersey');
INSERT INTO country (id, country) VALUES ('JM', 'Jamaica');
INSERT INTO country (id, country) VALUES ('JO', 'Jordan');
INSERT INTO country (id, country) VALUES ('JP', 'Japan');
INSERT INTO country (id, country) VALUES ('KE', 'Kenya');
INSERT INTO country (id, country) VALUES ('KG', 'Kyrgyzstan');
INSERT INTO country (id, country) VALUES ('KH', 'Cambodia');
INSERT INTO country (id, country) VALUES ('KI', 'Kiribati');
INSERT INTO country (id, country) VALUES ('KM', 'Comoros');
INSERT INTO country (id, country) VALUES ('KN', 'Saint Kitts and Nevis');
INSERT INTO country (id, country) VALUES ('KP', 'North Korea');
INSERT INTO country (id, country) VALUES ('KR', 'South Korea');
INSERT INTO country (id, country) VALUES ('KW', 'Kuwait');
INSERT INTO country (id, country) VALUES ('KY', 'Cayman Islands');
INSERT INTO country (id, country) VALUES ('KZ', 'Kazakhstan');
INSERT INTO country (id, country) VALUES ('LA', 'Laos');
INSERT INTO country (id, country) VALUES ('LB', 'Lebanon');
INSERT INTO country (id, country) VALUES ('LC', 'Saint Lucia');
INSERT INTO country (id, country) VALUES ('LI', 'Liechtenstein');
INSERT INTO country (id, country) VALUES ('LK', 'Sri Lanka');
INSERT INTO country (id, country) VALUES ('LR', 'Liberia');
INSERT INTO country (id, country) VALUES ('LS', 'Lesotho');
INSERT INTO country (id, country) VALUES ('LT', 'Lithuania');
INSERT INTO country (id, country) VALUES ('LU', 'Luxembourg');
INSERT INTO country (id, country) VALUES ('LV', 'Latvia');
INSERT INTO country (id, country) VALUES ('LY', 'Libya');
INSERT INTO country (id, country) VALUES ('MA', 'Morocco');
INSERT INTO country (id, country) VALUES ('MC', 'Monaco');
INSERT INTO country (id, country) VALUES ('MD', 'Moldova');
INSERT INTO country (id, country) VALUES ('ME', 'Montenegro');
INSERT INTO country (id, country) VALUES ('MF', 'Saint Martin');
INSERT INTO country (id, country) VALUES ('MG', 'Madagascar');
INSERT INTO country (id, country) VALUES ('MH', 'Marshall Islands');
INSERT INTO country (id, country) VALUES ('MK', 'North Macedonia');
INSERT INTO country (id, country) VALUES ('ML', 'Mali');
INSERT INTO country (id, country) VALUES ('MM', 'Myanmar');
INSERT INTO country (id, country) VALUES ('MN', 'Mongolia');
INSERT INTO country (id, country) VALUES ('MO', 'Macau');
INSERT INTO country (id, country) VALUES ('MP', 'Northern Mariana Islands');
INSERT INTO country (id, country) VALUES ('MQ', 'Martinique');
INSERT INTO country (id, country) VALUES ('MR', 'Mauritania');
INSERT INTO country (id, country) VALUES ('MS', 'Montserrat');
INSERT INTO country (id, country) VALUES ('MT', 'Malta');
INSERT INTO country (id, country) VALUES ('MU', 'Mauritius');
INSERT INTO country (id, country) VALUES ('MV', 'Maldives');
INSERT INTO country (id, country) VALUES ('MW', 'Malawi');
INSERT INTO country (id, country) VALUES ('MX', 'Mexico');
INSERT INTO country (id, country) VALUES ('MY', 'Malaysia');
INSERT INTO country (id, country) VALUES ('MZ', 'Mozambique');
INSERT INTO country (id, country) VALUES ('NA', 'Namibia');
INSERT INTO country (id, country) VALUES ('NC', 'New Caledonia');
INSERT INTO country (id, country) VALUES ('NE', 'Niger');
INSERT INTO country (id, country) VALUES ('NF', 'Norfolk Island');
INSERT INTO country (id, country) VALUES ('NG', 'Nigeria');
INSERT INTO country (id, country) VALUES ('NI', 'Nicaragua');
INSERT INTO country (id, country) VALUES ('NL', 'Netherlands');
INSERT INTO country (id, country) VALUES ('NO', 'Norway');
INSERT INTO country (id, country) VALUES ('NP', 'Nepal');
INSERT INTO country (id, country) VALUES ('NR', 'Nauru');
INSERT INTO country (id, country) VALUES ('NU', 'Niue');
INSERT INTO country (id, country) VALUES ('NZ', 'New Zealand');
INSERT INTO country (id, country) VALUES ('OM', 'Oman');
INSERT INTO country (id, country) VALUES ('PA', 'Panama');
INSERT INTO country (id, country) VALUES ('PE', 'Peru');
INSERT INTO country (id, country) VALUES ('PF', 'French Polynesia');
INSERT INTO country (id, country) VALUES ('PG', 'Papua New Guinea');
INSERT INTO country (id, country) VALUES ('PH', 'Philippines');
INSERT INTO country (id, country) VALUES ('PK', 'Pakistan');
INSERT INTO country (id, country) VALUES ('PL', 'Poland');
INSERT INTO country (id, country) VALUES ('PM', 'Saint Pierre and Miquelon');
INSERT INTO country (id, country) VALUES ('PN', 'Pitcairn Islands');
INSERT INTO country (id, country) VALUES ('PR', 'Puerto Rico');
INSERT INTO country (id, country) VALUES ('PT', 'Portugal');
INSERT INTO country (id, country) VALUES ('PW', 'Palau');
INSERT INTO country (id, country) VALUES ('PY', 'Paraguay');
INSERT INTO country (id, country) VALUES ('QA', 'Qatar');
INSERT INTO country (id, country) VALUES ('RE', 'Réunion');
INSERT INTO country (id, country) VALUES ('RO', 'Romania');
INSERT INTO country (id, country) VALUES ('RS', 'Serbia');
INSERT INTO country (id, country) VALUES ('RU', 'Russia');
INSERT INTO country (id, country) VALUES ('RW', 'Rwanda');
INSERT INTO country (id, country) VALUES ('SA', 'Saudi Arabia');
INSERT INTO country (id, country) VALUES ('SB', 'Solomon Islands');
INSERT INTO country (id, country) VALUES ('SC', 'Seychelles');
INSERT INTO country (id, country) VALUES ('SD', 'Sudan');
INSERT INTO country (id, country) VALUES ('SE', 'Sweden');
INSERT INTO country (id, country) VALUES ('SG', 'Singapore');
INSERT INTO country (id, country) VALUES ('SH', 'Saint Helena');
INSERT INTO country (id, country) VALUES ('SI', 'Slovenia');
INSERT INTO country (id, country) VALUES ('SJ', 'Svalbard and Jan Mayen');
INSERT INTO country (id, country) VALUES ('SK', 'Slovakia');
INSERT INTO country (id, country) VALUES ('SL', 'Sierra Leone');
INSERT INTO country (id, country) VALUES ('SM', 'San Marino');
INSERT INTO country (id, country) VALUES ('SN', 'Senegal');
INSERT INTO country (id, country) VALUES ('SO', 'Somalia');
INSERT INTO country (id, country) VALUES ('SR', 'Suriname');
INSERT INTO country (id, country) VALUES ('SS', 'South Sudan');
INSERT INTO country (id, country) VALUES ('ST', 'São Tomé and Príncipe');
INSERT INTO country (id, country) VALUES ('SV', 'El Salvador');
INSERT INTO country (id, country) VALUES ('SX', 'Sint Maarten');
INSERT INTO country (id, country) VALUES ('SY', 'Syria');
INSERT INTO country (id, country) VALUES ('SZ', 'Eswatini');
INSERT INTO country (id, country) VALUES ('TC', 'Turks and Caicos Islands');
INSERT INTO country (id, country) VALUES ('TD', 'Chad');
INSERT INTO country (id, country) VALUES ('TF', 'French Southern and Antarctic Lands');
INSERT INTO country (id, country) VALUES ('TG', 'Togo');
INSERT INTO country (id, country) VALUES ('TH', 'Thailand');
INSERT INTO country (id, country) VALUES ('TJ', 'Tajikistan');
INSERT INTO country (id, country) VALUES ('TK', 'Tokelau');
INSERT INTO country (id, country) VALUES ('TL', 'Timor-Leste');
INSERT INTO country (id, country) VALUES ('TM', 'Turkmenistan');
INSERT INTO country (id, country) VALUES ('TN', 'Tunisia');
INSERT INTO country (id, country) VALUES ('TO', 'Tonga');
INSERT INTO country (id, country) VALUES ('TR', 'Turkey');
INSERT INTO country (id, country) VALUES ('TT', 'Trinidad and Tobago');
INSERT INTO country (id, country) VALUES ('TV', 'Tuvalu');
INSERT INTO country (id, country) VALUES ('TZ', 'Tanzania');
INSERT INTO country (id, country) VALUES ('UA', 'Ukraine');
INSERT INTO country (id, country) VALUES ('UG', 'Uganda');
INSERT INTO country (id, country) VALUES ('UM', 'United States Minor Outlying Islands');
INSERT INTO country (id, country) VALUES ('US', 'United States');
INSERT INTO country (id, country) VALUES ('UY', 'Uruguay');
INSERT INTO country (id, country) VALUES ('UZ', 'Uzbekistan');
INSERT INTO country (id, country) VALUES ('VA', 'Vatican City');
INSERT INTO country (id, country) VALUES ('VC', 'Saint Vincent and the Grenadines');
INSERT INTO country (id, country) VALUES ('VE', 'Venezuela');
INSERT INTO country (id, country) VALUES ('VG', 'British Virgin Islands');
INSERT INTO country (id, country) VALUES ('VI', 'U.S. Virgin Islands');
INSERT INTO country (id, country) VALUES ('VN', 'Vietnam');
INSERT INTO country (id, country) VALUES ('VU', 'Vanuatu');
INSERT INTO country (id, country) VALUES ('WF', 'Wallis and Futuna');
INSERT INTO country (id, country) VALUES ('WS', 'Samoa');
INSERT INTO country (id, country) VALUES ('YE', 'Yemen');
INSERT INTO country (id, country) VALUES ('YT', 'Mayotte');
INSERT INTO country (id, country) VALUES ('ZA', 'South Africa');
INSERT INTO country (id, country) VALUES ('ZM', 'Zambia');
INSERT INTO country (id, country) VALUES ('ZW', 'Zimbabwe');

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

