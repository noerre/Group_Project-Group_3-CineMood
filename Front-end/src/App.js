import {useState} from 'react';
import './App.css';
import SearchIcon from './search.svg'
import MovieCard from "./MovieCard";
import Login from "./Login";
import Register from "./Register";
import Navbar from "./Navbar";
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';

//c032e2d7

const API_URL = "http://www.omdbapi.com?apikey=b6003d8a";

const App = () => {
    const [movies, setMovies] = useState([]);
    const [searchTerm, setSearchTerm]= useState('')

    const searchMovies = async (title) => {
        const response =  await fetch(`${API_URL}&s=${title}`);
        const data = await response.json();

        setMovies(data.Search);
    }

    return (
        <Router>
            <Navbar />
            <div className='app'>
                <Routes>
                    <Route path="/" element={
                        <>
                            <h1>CineMood</h1>
                            <div className='search'>
                                <input
                                    placeholder="Search for movies"
                                    value={searchTerm}
                                    onChange={(e) => setSearchTerm(e.target.value)}
                                    onKeyDown={(e) => {
                                        if (e.key === 'Enter') {
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
                            {
                                movies.length > 0 ? (
                                    <div className="container">
                                        {movies.map((movie) => (
                                            <MovieCard key={movie.imdbID} movie={movie} />
                                        ))}
                                    </div>
                                ) : (
                                    <div className="empty">
                                        <h2>No movies found</h2>
                                    </div>
                                )
                            }
                        </>
                    } />
                    <Route path="/login" element={<Login />} />
                    <Route path="/register" element={<Register />} />
                    <Route path="*" element={<Navigate to="/" replace />} />
                </Routes>
            </div>
        </Router>
    );
};

export default App;