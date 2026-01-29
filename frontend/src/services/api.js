import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000/api';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor: attach token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('jamii_token');
  if (token) {
    config.headers.Authorization = `Token ${token}`;
  }
  return config;
});

// Response interceptor: handle 401
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      localStorage.removeItem('jamii_token');
      localStorage.removeItem('jamii_user');
      if (window.location.pathname !== '/login') {
        window.location.href = '/login';
      }
    }
    return Promise.reject(error);
  }
);

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

export const issueService = {
  createRequest: async (formData) => {
    // FormData is required for image uploads
    const response = await api.post('/issues/requests/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  getMyRequests: async () => {
    const response = await api.get('/issues/requests/');
    return response.data;
  }
};

export const facilityService = {
  getAll: async () => {
    const response = await api.get('/facilities/list/');
    return response.data;
  },
  book: async (bookingData) => {
    const response = await api.post('/facilities/bookings/', bookingData);
    return response.data;
  },
  getMyBookings: async () => {
    const response = await api.get('/facilities/bookings/');
    return response.data;
  }
};

export const projectService = {
  getAll: async (filters = {}) => {
    const response = await api.get('/projects/', { params: filters });
    return response.data;
  },
  getUpdates: async (projectId) => {
    const response = await api.get('/projects/updates/', { params: { project_id: projectId } });
    return response.data;
  },
  postUpdate: async (formData) => {
    const response = await api.post('/projects/updates/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });
    return response.data;
  }
};

export const officialService = {
  getAll: async (filters = {}) => {
    // filters can be { ward_id, constituency_id, etc. }
    const response = await api.get('/locations/officials/', { params: filters });
    return response.data;
  }
};

export const legislationService = {
  getInstruments: async (params = {}) => {
    const response = await api.get('/legislation/instruments/', { params });
    return response.data;
  },
  getActiveInstruments: async () => {
    const response = await api.get('/legislation/instruments/active/');
    return response.data;
  },
  getInstrumentDetail: async (id) => {
    const response = await api.get(`/legislation/instruments/${id}/`);
    return response.data;
  },
  getInstrumentStats: async (id) => {
    const response = await api.get(`/legislation/instruments/${id}/stats/`);
    return response.data;
  },
  submitFeedback: async (formData) => {
    const response = await api.post('/legislation/feedback/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return response.data;
  },
};

export default api;
