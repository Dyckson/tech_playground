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

// ========== Analytics - Task 7: Area Level ==========
export const getAreasScoresComparison = async (empresaId?: string) => {
  const { data } = await api.get('/analytics/areas/scores-comparison', {
    params: empresaId ? { empresa_id: empresaId } : {},
  });
  return data;
};

export const getAreasEnpsComparison = async (empresaId?: string) => {
  const { data } = await api.get('/analytics/areas/enps-comparison', {
    params: empresaId ? { empresa_id: empresaId } : {},
  });
  return data;
};

export const getAreaDetailedMetrics = async (areaId: string) => {
  const { data } = await api.get(`/analytics/areas/${areaId}/detailed-metrics`);
  return data;
};

export default api;
