import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";

const TMDB_API_KEY = process.env.REACT_APP_TMDB_API_KEY;
const TMDB_API_URL = "https://api.themoviedb.org/3";

const MovieDetailsPage = () => {
  const { id } = useParams();
  const [movie, setMovie] = useState(null);
  const [cast, setCast] = useState([]);
  const [crew, setCrew] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchMovieDetails = async () => {
      try {
        const response = await fetch(`${TMDB_API_URL}/movie/${id}?api_key=${TMDB_API_KEY}&language=en-US`);
        if (!response.ok) {
          throw new Error("Failed to fetch movie details.");
        }
        const data = await response.json();
        setMovie(data);
      } catch (err) {
        console.error("Error fetching movie details:", err);
        setError(err.message);
      }
    };

    const fetchMovieCredits = async () => {
      try {
        const response = await fetch(`${TMDB_API_URL}/movie/${id}/credits?api_key=${TMDB_API_KEY}&language=en-US`);
        if (!response.ok) {
          throw new Error("Failed to fetch movie credits.");
        }
        const data = await response.json();
        setCast(data.cast.slice(0, 10)); 
        setCrew(data.crew);
      } catch (err) {
        console.error("Error fetching credits:", err);
        setError(err.message);
      }
    };

    const fetchData = async () => {
      setLoading(true);
      setError(null);
      await Promise.all([fetchMovieDetails(), fetchMovieCredits()]);
      setLoading(false);
    };

    if (id) {
      fetchData();
    }
  }, [id]);

  if (loading) return <p className="text-center">Loading movie details...</p>;
  if (error) return <p className="text-center text-danger">{error}</p>;

  const posterUrl = movie.poster_path
    ? `https://image.tmdb.org/t/p/w500${movie.poster_path}`
    : "https://via.placeholder.com/500x750?text=No+Image";

  const releaseYear = movie.release_date ? movie.release_date.split('-')[0] : "Unknown";

  return (
    <div className="container mt-4">
      <h1 className="text-center">{movie.title || "Unknown Title"}</h1>
      <div className="text-center">
        <img
          src={posterUrl}
          alt={`${movie.title || "Unknown"} Poster`}
          className="img-fluid rounded my-4"
        />
      </div>
      <p>{movie.overview || "No description available."}</p>
      <p>
        <strong>Release Year:</strong> {releaseYear}
      </p>

      <h3>Cast</h3>
      <ul>
        {cast.map((actor) => (
          <li key={actor.id}>
            {actor.name} as {actor.character}
          </li>
        ))}
      </ul>

      <h3>Crew</h3>
      <ul>
        {crew.map((member) => (
          <li key={member.id}>
            {member.name} - {member.job}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default MovieDetailsPage;