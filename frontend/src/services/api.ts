import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:9876/api/v1',
  timeout: 10000,
});

// ========== Funcionários ==========
export const getEmployees = async (page = 1, pageSize = 100) => {
  const { data } = await api.get('/funcionarios', {
    params: { page, page_size: pageSize },
  });
  return data;
};

// ========== Analytics ==========
export const getEnpsData = async () => {
  const { data } = await api.get('/analytics/enps');
  return data;
};

export const getTenureDistribution = async () => {
  const { data } = await api.get('/analytics/tenure-distribution');
  return data;
};

export const getSatisfactionScores = async () => {
  const { data } = await api.get('/analytics/satisfaction-scores');
  return data;
};

export default api;
