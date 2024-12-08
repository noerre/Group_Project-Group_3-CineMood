import React, { useState, useContext } from "react";
import { FaUser, FaLock } from "react-icons/fa";
import { AuthContext } from "./AuthContext";
import api from "./api";
import { useNavigate, Link } from "react-router-dom";

const Register = () => {
  const { login } = useContext(AuthContext);
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [errors, setErrors] = useState([]);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const validateInputs = () => {
    const validationErrors = [];
    const passwordRegex = /^(?=.*[!@#$%^&*])(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d!@#$%^&*]{8,}$/;

    if (username.length < 3) {
      validationErrors.push("Username must be at least 3 characters long.");
    }

    if (!passwordRegex.test(password)) {
      validationErrors.push(
        "Password must be at least 8 characters long, include at least one letter, one number, and one special character."
      );
    }

    return validationErrors;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrors([]);
    setLoading(true);

    const validationErrors = validateInputs();
    if (validationErrors.length > 0) {
      setErrors(validationErrors);
      setLoading(false);
      return;
    }

    try {
      const response = await api.post("/register", { username, password });
      const { access_token } = response.data;
      login(access_token);
      navigate("/");
    } catch (err) {
      if (err.response && err.response.data && err.response.data.errors) {
        const serverErrors = [];
        for (const [field, messages] of Object.entries(err.response.data.errors)) {
          messages.forEach((msg) => {
            serverErrors.push(`${field}: ${msg}`);
          });
        }
        setErrors(serverErrors);
      } else if (err.response && err.response.data && err.response.data.error) {
        setErrors([err.response.data.error]);
      } else {
        setErrors(["An unexpected error occurred."]);
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="d-flex justify-content-center align-items-center vh-100 bg-secondary">
      <div
        className="card p-4 shadow"
        style={{ width: "400px", borderRadius: "15px" }}
      >
        <h2 className="text-center mb-4">Register</h2>
        <form onSubmit={handleSubmit}>
          <div className="mb-3">
            <label htmlFor="username" className="form-label">
              Username
            </label>
            <div className="input-group">
              <span className="input-group-text">
                <FaUser />
              </span>
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
            <small className="form-text text-muted">
              Please enter a username that is at least 3 characters long.
            </small>
          </div>

          <div className="mb-4">
            <label htmlFor="password" className="form-label">
              Password
            </label>
            <div className="input-group">
              <span className="input-group-text">
                <FaLock />
              </span>
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
            <small className="form-text text-muted">
              Your password should be at least 8 characters, include a letter, a number, and a special character.
            </small>
          </div>

          {errors.length > 0 && (
            <div className="alert alert-danger" role="alert">
              <ul className="mb-0">
                {errors.map((error, index) => (
                  <li key={index}>{error}</li>
                ))}
              </ul>
            </div>
          )}

          <button
            type="submit"
            className="btn btn-success w-100"
            disabled={loading}
          >
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
