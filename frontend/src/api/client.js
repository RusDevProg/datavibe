import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const uploadFile = async (file) => {
  const formData = new FormData();
  formData.append('file', file);
  
  const response = await api.post('/api/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
  return response.data;
};

export const analyzeData = async (data, text) => {
  const response = await api.post('/api/analyze', { data, text });
  return response.data;
};

export const chatWith = async (message, data, context = '') => {
  const response = await api.post('/api/chat', { message, data, context });
  return response.data;
};

export default api;