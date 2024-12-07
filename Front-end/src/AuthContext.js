import React, { createContext, useState, useEffect } from "react";
import { jwtDecode } from "jwt-decode";

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [auth, setAuth] = useState({
    isAuthenticated: false,
    user: null,
    token: null,
  });

  useEffect(() => {
    const token = localStorage.getItem("access_token");
    if (token) {
      try {
      const user = jwtDecode(token);
      setAuth({
        isAuthenticated: true,
        user: user.username,
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
      const user = jwtDecode(token);
      localStorage.setItem("access_token", token);
      setAuth({
        isAuthenticated: true,
        user: user.username,
        token: token,
      });
    } catch (e) {
      console.error("Failed to decode token:", e);
    }
  };

  const logout = () => {
    localStorage.removeItem("access_token");
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
