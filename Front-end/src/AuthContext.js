import React, { createContext, useState, useEffect } from "react";
import { jwtDecode } from "jwt-decode";

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [auth, setAuth] = useState({
    isAuthenticated: !!localStorage.getItem("access_token"),
    user: localStorage.getItem("username") || null,
    token: localStorage.getItem("access_token") || null,
  });

  useEffect(() => {
    const token = localStorage.getItem("access_token");
    if (token) {
      try {
        const decoded = jwtDecode(token);
        setAuth({
          isAuthenticated: true,
          user: decoded.username,
          token: token,
        });
      } catch (e) {
        console.error("Invalid token:", e);
        logout();
      }
    }
  }, []);

  const login = (token) => {
    try {
      const decodedToken = jwtDecode(token); // Decode the token
    const username = decodedToken.sub || decodedToken.username; // Adjust based on your token payload structure

    localStorage.setItem("access_token", token);
    localStorage.setItem("username", username);

    setAuth({
      isAuthenticated: true,
      user: username,
      token: token,
    });
  } catch (e) {
    console.error("Failed to decode token:", e);
  }
};

  const logout = () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("username");
    setAuth({
      isAuthenticated: false,
      user: null,
      token: null,
    });
  };

  return (
    <AuthContext.Provider value={{ auth, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};
