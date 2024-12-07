import { useState, useEffect } from "react";
import "./App.css";
import SearchIcon from "./search.svg";
import MovieCard from "./MovieCard";
import Login from "./Login";
import Register from "./Register";
import Navbar from "./Navbar";
import MoodSelector from "./MoodSelector";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
  useNavigate,
} from "react-router-dom";

const API_URL = "http://www.omdbapi.com?apikey=b6003d8a";
const BACKEND_URL = "http://localhost:8000"; 

const HomePage = ({ searchMovies, searchTerm, setSearchTerm, movies }) => {
  const navigate = useNavigate();

  const handleNavigate = () => {
    navigate("/questions"); 
  };

  return (
    <>
      <h1>CineMood</h1>
      <div className="search">
        <input
          placeholder="Search for movies"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter") {
              searchMovies(searchTerm);
            }
          }}
        />
        <img
          src={SearchIcon}
          alt="search"
          onClick={() => searchMovies(searchTerm)}
        />
      </div>
      <div className="map_mood">
        <button className="button-cinemood" onClick={handleNavigate}>
          CINEMOOD
        </button>
      </div>
      {movies.length > 0 ? (
        <div className="container">
          {movies.map((movie) => (
            <MovieCard key={movie.imdbID} movie={movie} />
          ))}
        </div>
      ) : (
        <div className="empty">
          <h2></h2>
        </div>
      )}
    </>
  );
};

const QuestionsPage = () => {
  const navigate = useNavigate();

  const handleMoodSelect = (selectedMood) => {
    localStorage.setItem("userMood", selectedMood); 
    navigate("/recommendations"); 
  };

  return (
    <div>
      <h2>Page with questions</h2>
      <p>Select your mood or answer the questions to get recommendations.</p>
      <MoodSelector onMoodSelect={handleMoodSelect} />
      <div className="map_mood">
        <button className="button-return" onClick={() => navigate("/")}>
          Return to main page
        </button>
      </div>
    </div>
  );
};

const RecommendationsPage = () => {
  const [recommendations, setRecommendations] = useState([]);
  const mood = localStorage.getItem("userMood");

  useEffect(() => {
    const fetchRecommendations = async () => {
      try {
        const response = await fetch(`${BACKEND_URL}/recommendations`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ mood }),
        });

        if (!response.ok) {
          throw new Error("Failed to fetch recommendations");
        }

        const data = await response.json();
        setRecommendations(data); // Ustawiamy dane rekomendacji
      } catch (error) {
        console.error("Error fetching recommendations:", error);
      }
    };

    if (mood) {
      fetchRecommendations();
    }
  }, [mood]);

  return (
    <div>
      <h2>Recommendations for mood: {mood}</h2>
      <div className="container">
        {recommendations.length > 0 ? (
          recommendations.map((movie, index) => (
            <MovieCard key={index} movie={movie} />
          ))
        ) : (
          <h3>No recommendations found</h3>
        )}
      </div>
    </div>
  );
};

const App = () => {
  const [movies, setMovies] = useState([]);
  const [searchTerm, setSearchTerm] = useState("");

  const searchMovies = async (title) => {
    const response = await fetch(`${API_URL}&s=${title}`);
    const data = await response.json();

    setMovies(data.Search || []);
  };

  return (
    <Router>
      <Navbar />
      <div className="app">
        <Routes>
          <Route
            path="/"
            element={
              <HomePage
                searchMovies={searchMovies}
                searchTerm={searchTerm}
                setSearchTerm={setSearchTerm}
                movies={movies}
              />
            }
          />
          <Route path="/questions" element={<QuestionsPage />} />
          <Route
            path="/recommendations"
            element={<RecommendationsPage />}
          />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </div>
    </Router>
  );
};

export default App;
