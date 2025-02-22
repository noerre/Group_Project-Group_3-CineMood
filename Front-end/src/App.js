
import { useState, useEffect } from "react";
import "./App.css";
import SearchIcon from "./search.svg";
import MovieCard from "./MovieCard";
import Login from "./Login";
import Register from "./Register";
import Navbar from "./Navbar";
import MoodSelector from "./MoodSelector";
import MovieDetailsPage from "./MovieDetailsPage";

import { useLocation } from "react-router-dom";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
  useNavigate,
} from "react-router-dom";

const TMDB_API_KEY = process.env.REACT_APP_TMDB_API_KEY;
const TMDB_API_URL = "https://api.themoviedb.org/3";

const BACKEND_URL = "http://localhost:8000"; 

const HomePage = ({ searchMovies, searchTerm, setSearchTerm, movies }) => {
  const navigate = useNavigate();

  const handleNavigate = () => {
    navigate(`/search?query=${searchTerm}`); // Passing searchTerm as a query parameter
  };


  useEffect(() => {
    setSearchTerm(""); // Reset the search term when the component is mounted
  }, [setSearchTerm]);


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
              handleNavigate(); // Navigate on Enter key press
            }
          }}
        />
        <img
          src={SearchIcon}
          alt="search"
          onClick={handleNavigate} // Navigate on icon click
        />
      </div>
      <div className="map_mood">
        <button className="button-cinemood" onClick={() => navigate("/questions")}>
          CINEMOOD
        </button>
      </div>
    </>
  );
};



const SearchPage = () => {
  const [movies, setMovies] = useState([]);
  const [searchTerm, setSearchTerm] = useState("");
  const location = useLocation(); // Accessing URL query parameters
  const navigate = useNavigate();

  useEffect(() => {
    const params = new URLSearchParams(location.search);
    const query = params.get("query");
    if (query) {
      setSearchTerm(query);
      searchMovies(query);
    }
  }, [location]);

  const searchMovies = async (title) => {
    try {
        const response = await fetch(
          `${TMDB_API_URL}/search/movie?api_key=${TMDB_API_KEY}&query=${encodeURIComponent(title)}`
        );
        const data = await response.json();
    
        if (data.results) {
          setMovies(data.results);
        } else {
          setMovies([]);
        }
      } catch (error) {
        console.error("Error fetching data from TMDB:", error);
      }
    };

    const handleMoreDetails = (movieId) => {
        navigate(`/movie-details/${movieId}`);
      };

      return (
        <>
          <h1>Search Movies</h1>
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
          {movies.length > 0 ? (
            <div className="container">
              {movies.map((movie) => (
                <MovieCard
                  key={movie.id} // Użyj unikalnego identyfikatora TMDB
                  movie={movie}
                  onMoreDetails={handleMoreDetails} // Przekazanie callbacka
                />
              ))}
            </div>
          ) : (
            <div className="empty">
              <h2>No movies found</h2>
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
      <h2>Select your mood to get recommendations.</h2>
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
  const navigate = useNavigate();

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

  const handleMoreDetails = (movie) => {
    if (!movie || !movie.id) {
        console.error("No movie ID provided.", movie);
        return;
      }
      navigate(`/movie-details?id=${movie.id}`);
    };

  return (
    <div>
      <h2>Recommendations for mood: {mood}</h2>
      <div className="row justify-content-center">
        {recommendations.length > 0 ? (
          recommendations.map((movie) => (
            <div
              className="col-6 col-sm-4 col-md-3 col-lg-2 mb-4"
              key={movie.id} 
            >
              <MovieCard
                movie={movie}
                onMoreDetails={handleMoreDetails} 
              />
            </div>
          ))
        ) : (
          <div className="col-12 text-center text-light">
            <h3>No recommendations found</h3>
          </div>
        )}
      </div>
    </div>
  );
};

const App = () => {
  const [movies, setMovies] = useState([]);
  const [searchTerm, setSearchTerm] = useState("");

  const searchMovies = async (title) => {
    const response = await fetch(`${TMDB_API_URL}&s=${title}`);
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
          <Route path="/questions" element={<QuestionsPage />} />
          <Route path="/recommendations" element={<RecommendationsPage />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/search" element={<SearchPage />} /> 
          <Route path="/movie-details/:id" element={<MovieDetailsPage />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </div>
    </Router>
  );
};

export default App;
