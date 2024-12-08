/*
import React from "react";
import PropTypes from "prop-types";
import "./MovieCard.css";


const MovieCard = ({ movie, onMoreDetails }) => {
  const { title, overview, poster_path, release_year } = movie;

  const posterUrl = poster_path
    ? `https://image.tmdb.org/t/p/w500${poster_path}`
    : "https://via.placeholder.com/500x750?text=No+Image";

    return (
        <div className="card movie-card">
          <img src={posterUrl} className="card-img-top" alt={`${title || "Unknown"} Poster`} />
          <div className="card-body">
            <h5 className="card-title">{title || "Unknown Title"}</h5>
            <p className="card-text">
              {overview ? overview.substring(0, 150) + "..." : "No description available."}
            </p>
            <p className="card-text">
              <small className="text-muted">Release year: {release_year || "Unknown"}</small>
            </p>
            <button
              className="btn btn-primary"
              onClick={() => onMoreDetails && onMoreDetails(movie)}
            >
              More details
            </button>
          </div>
        </div>
      );
    };
    
    MovieCard.propTypes = {
      movie: PropTypes.shape({
        title: PropTypes.string,
        overview: PropTypes.string,
        poster_path: PropTypes.string,
        release_year: PropTypes.string,
      }).isRequired,
    };
    
export default MovieCard;

*/

import React from "react";
import PropTypes from "prop-types";
import "./MovieCard.css";

const MovieCard = ({ movie, onMoreDetails }) => {
  const posterUrl = movie.poster_path
    ? `https://image.tmdb.org/t/p/w500${movie.poster_path}`
    : "https://via.placeholder.com/500x750?text=No+Image";

  return (
    <div className="card movie-card">
      <img
        src={posterUrl}
        className="card-img-top"
        alt={`${movie.title || "Unknown"} Poster`}
      />
      <div className="card-body">
        <h5 className="card-title">{movie.title || "Unknown Title"}</h5>
        <p className="card-text">
          {movie.overview ? movie.overview.substring(0, 150) + "..." : "No description available."}
        </p>
        <p className="card-text mt-auto">
    <small className="text-muted">Release Year: {movie.release_year || "Unknown"}</small>
</p>
        {onMoreDetails && (
          <button
            className="btn btn-primary"
            onClick={() => onMoreDetails(movie)}
          >
            More details
          </button>
        )}
      </div>
    </div>
  );
};

MovieCard.propTypes = {
  movie: PropTypes.shape({
    title: PropTypes.string,
    overview: PropTypes.string,
    poster_path: PropTypes.string,
    release_date: PropTypes.string,
  }).isRequired,
};

export default MovieCard;
