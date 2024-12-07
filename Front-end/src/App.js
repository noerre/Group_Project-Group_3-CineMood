import { useState } from "react";
import "./App.css";
import SearchIcon from "./search.svg";
import MovieCard from "./MovieCard";
import MoodSelector from "./MoodSelector";
import Recommendations from "./Recommendations";
import Login from "./Login";
import Register from "./Register";
import Navbar from "./Navbar";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
  useNavigate,
} from "react-router-dom";

const API_URL = "http://www.omdbapi.com?apikey=b6003d8a";

const HomePage = ({ searchMovies, searchTerm, setSearchTerm, movies }) => {
  const navigate = useNavigate();

  const handleNavigate = () => {
    navigate("/questions"); // Przekierowanie na stronę z pytaniami
  };
  

  const handleMoodSelect = (selectedMood) => {
    localStorage.setItem("userMood", selectedMood); // Zapisanie nastroju w localStorage
    navigate("/recommendations"); // Przekierowanie na stronę z rekomendacjami
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

      <MoodSelector onMoodSelect={handleMoodSelect} />

      {movies.length > 0 ? (
        <div className="container">
          {movies.map((movie) => (
            <MovieCard key={movie.imdbID} movie={movie} />
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
          <Route
            path="/recommendations"
            element={<Recommendations mood={localStorage.getItem("userMood")} />}
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
