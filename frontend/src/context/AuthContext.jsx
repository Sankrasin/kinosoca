import { createContext, useState, useEffect } from "react";

export const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [tokens, setTokens] = useState({
    access: localStorage.getItem("access_token"),
    refresh: localStorage.getItem("refresh_token"),
  });

  useEffect(() => {
    const stored_access = localStorage.getItem("access_token");
    const stored_refresh = localStorage.getItem("refresh_token");

    if (stored_access && stored_refresh) {
      setTokens({ access: stored_access, refresh: stored_refresh });
      fetchCurrentUser(stored_access);
    } else {
      setLoading(false);
    }
  }, []);

  const fetchCurrentUser = async (token) => {
    try {
      const response = await fetch(
        `${import.meta.env.VITE_API_BASE_URL}/auth/me`,
        {
          headers: { Authorization: `Bearer ${token}` },
        },
      );
      if (response.ok) {
        const data = await response.json();
        setUser(data);
      } else {
        localStorage.removeItem("access_token");
        localStorage.removeItem("refresh_token");
        setTokens({ access: null, refresh: null });
      }
    } catch (err) {
      console.error("Failed to fetch current user:", err);
    } finally {
      setLoading(false);
    }
  };

  const login = (accessToken, refreshToken, userData) => {
    localStorage.setItem("access_token", accessToken);
    localStorage.setItem("refresh_token", refreshToken);
    setTokens({ access: accessToken, refresh: refreshToken });
    setUser(userData);
  };

  const logout = () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    setTokens({ access: null, refresh: null });
    setUser(null);
  };

  const refreshAccessToken = async () => {
    try {
      const response = await fetch(
        `${import.meta.env.VITE_API_BASE_URL}/auth/refresh`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ refresh_token: tokens.refresh }),
        },
      );
      if (response.ok) {
        const data = await response.json();
        localStorage.setItem("access_token", data.access_token);
        setTokens((prev) => ({ ...prev, access: data.access_token }));
        return data.access_token;
      } else {
        logout();
        return null;
      }
    } catch (err) {
      console.error("Failed to refresh token:", err);
      logout();
      return null;
    }
  };

  return (
    <AuthContext.Provider
      value={{ user, tokens, loading, login, logout, refreshAccessToken }}
    >
      {children}
    </AuthContext.Provider>
  );
}
