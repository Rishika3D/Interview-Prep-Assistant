import { useState, useEffect } from 'react';
import * as api from '../services/api';

export const useAuth = () => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      api.setAuthToken(token);
      api.getCurrentUser()
        .then(res => setUser(res.data))
        .catch(() => logout())
        .finally(() => setLoading(false));
    } else {
      setLoading(false);
    }
  }, []);

  const signup = async (email, password) => {
    const res = await api.signup(email, password);
    api.setAuthToken(res.data.access_token);
    setUser(res.data.user);
    return res.data;
  };

  const login = async (email, password) => {
    const res = await api.login(email, password);
    api.setAuthToken(res.data.access_token);
    setUser(res.data.user);
    return res.data;
  };

  const logout = () => {
    api.setAuthToken(null);
    setUser(null);
  };

  return { user, loading, signup, login, logout };
};
