import React, { useEffect, useState, useContext } from "react";
import axios from "axios";
import MovieCard from "./MovieCard";
import MoodSelector from "./MoodSelector"; 
import { AuthContext } from "./AuthContext";

const fetchRecommendations = async (mood, token, setMovies, setError, setLoading) => {
    setLoading(true);
    setError(null);
  
    try {
      const response = await axios.post(
        "http://localhost:8000/recommendations",
        { mood },
        {
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
        }
      );
  
      if (response.data.error) {
        setError(response.data.error);
      } else {
        setMovies(response.data);
      }
    } catch (err) {
      console.error("Error fetching recommendations:", err);
      setError("Failed to fetch recommendations.");
    } finally {
      setLoading(false);
    }
  };
  
  const Recommendations = () => {
    const [movies, setMovies] = useState([]);
    const [mood, setMood] = useState("");
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
  
    const { token } = useContext(AuthContext);
  
    const handleMoodSelect = (selectedMood) => {
      setMood(selectedMood);
      fetchRecommendations(selectedMood, token, setMovies, setError, setLoading);
    };
  
    useEffect(() => {
      if (mood) {
        fetchRecommendations(mood, token, setMovies, setError, setLoading);
      }
    }, [mood, token]);
  
    if (loading) return <p className="text-center">Loading recommendations...</p>;
    if (error) return <p className="text-center text-danger">{error}</p>;
  
    return (
      <div>
        <h3 className="mb-3 text-center">
          Recommended Movies for Mood: {mood.charAt(0).toUpperCase() + mood.slice(1)}
        </h3>
        <MoodSelector onMoodSelect={handleMoodSelect} />
        <div className="row">
          {movies.length > 0 ? (
            movies.map((movie, index) => (
              <div key={movie.id || index} className="col-md-3 mb-4">
                <MovieCard movie={movie} />
              </div>
            ))
          ) : (
            <p className="text-center">No recommendations found for the selected mood.</p>
          )}
        </div>
      </div>
    );
  };
  
  export default Recommendations;