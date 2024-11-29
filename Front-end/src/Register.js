import React, { useState, useContext } from "react";
import { FaUser, FaLock } from 'react-icons/fa';
import { AuthContext } from './AuthContext';
import api from './api'; 
import { useNavigate, Link } from 'react-router-dom';

const Register = () => {
    const { login } = useContext(AuthContext);
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError("");
        setLoading(true);

        try {
            const response = await api.post('/register', { username, password });
            const { access_token } = response.data;

            login(access_token);
            navigate('/');
        } catch (err) {
            if (err.response && err.response.data && err.response.data.error) {
                setError(err.response.data.error);
            } else {
                setError("An unexpected error occurred.");
            }
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="d-flex justify-content-center align-items-center vh-100 bg-secondary">
            <div className="card p-4 shadow" style={{ width: '400px', borderRadius: '15px' }}>
                <h2 className="text-center mb-4">Register</h2>
                <form onSubmit={handleSubmit}>
                    <div className="mb-3">
                        <label htmlFor="username" className="form-label">Username</label>
                        <div className="input-group">
                            <span className="input-group-text"><FaUser /></span>
                            <input
                                type="text"
                                className="form-control"
                                id="username"
                                placeholder="Choose a username"
                                value={username}
                                onChange={(e) => setUsername(e.target.value)}
                                required
                            />
                        </div>
                    </div>
                    <div className="mb-4">
                        <label htmlFor="password" className="form-label">Password</label>
                        <div className="input-group">
                            <span className="input-group-text"><FaLock /></span>
                            <input
                                type="password"
                                className="form-control"
                                id="password"
                                placeholder="Create a password"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                required
                            />
                        </div>
                    </div>
                    {error && <div className="alert alert-danger" role="alert">{error}</div>}
                    <button type="submit" className="btn btn-success w-100" disabled={loading}>
                        {loading ? "Registering..." : "Register"}
                    </button>
                </form>
                <div className="mt-3 text-center">
                    <span>Already have an account? </span>
                    <Link to="/login">Login</Link>
                </div>
                <div className="mt-2 text-center">
                    <Link to="/">Back to Home</Link>
                </div>
            </div>
        </div>
    );
};

export default Register;
