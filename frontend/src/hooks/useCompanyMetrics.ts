import { useQuery } from '@tanstack/react-query';
import * as api from '../services/api';

export const useEmployees = () => {
  return useQuery({
    queryKey: ['employees'],
    queryFn: () => api.getEmployees(1, 1), // Apenas para pegar o total
    staleTime: 5 * 60 * 1000,
  });
};

export const useEnps = () => {
  return useQuery({
    queryKey: ['enps'],
    queryFn: api.getEnpsData,
    staleTime: 5 * 60 * 1000,
  });
};

export const useTenureDistribution = () => {
  return useQuery({
    queryKey: ['tenure'],
    queryFn: api.getTenureDistribution,
    staleTime: 5 * 60 * 1000,
  });
};

export const useSatisfactionScores = () => {
  return useQuery({
    queryKey: ['satisfaction'],
    queryFn: api.getSatisfactionScores,
    staleTime: 5 * 60 * 1000,
  });
};
