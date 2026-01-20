import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000/api';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const locationService = {
  // 1. Get all Counties
  getCounties: async () => {
    const response = await api.get('/counties/');
    return response.data;
  },

  // 2. Get Constituencies (Filtered by County ID)
  getConstituencies: async (countyId) => {
    const response = await api.get(`/constituencies/?county_id=${countyId}`);
    return response.data;
  },

  // 3. Get Wards (Filtered by Constituency ID)
  getWards: async (constituencyId) => {
    const response = await api.get(`/wards/?constituency_id=${constituencyId}`);
    return response.data;
  }
};

export const authService = {
  register: async (userData) => {
    const response = await api.post('/register/', userData);
    return response.data;
  },

  login: async (credentials) => {
    const response = await api.post('/login/', credentials);
    return response.data;
  }
};

export default api;
