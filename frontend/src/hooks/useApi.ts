import { useQuery, UseQueryResult } from '@tanstack/react-query';
import apiService from '@/services/api.service';
import type {
  Empresa,
  CompanyMetrics,
  EnpsDistribution,
  TenureDistribution,
  SatisfactionScores,
  FuncionarioPaginada,
  ContagemPorArea,
} from '@/types/api.types';

// ====================
// Empresas Hooks
// ====================

export const useEmpresas = (): UseQueryResult<Empresa[], Error> => {
  return useQuery({
    queryKey: ['empresas'],
    queryFn: () => apiService.getEmpresas(),
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
};

export const useEmpresa = (empresaId: string): UseQueryResult<Empresa, Error> => {
  return useQuery({
    queryKey: ['empresa', empresaId],
    queryFn: () => apiService.getEmpresa(empresaId),
    enabled: !!empresaId,
  });
};

// ====================
// Analytics Hooks
// ====================

export const useCompanyMetrics = (empresaId?: string): UseQueryResult<CompanyMetrics, Error> => {
  return useQuery({
    queryKey: ['companyMetrics', empresaId],
    queryFn: () => apiService.getCompanyMetrics(empresaId),
    staleTime: 2 * 60 * 1000, // 2 minutes
  });
};

export const useEnpsDistribution = (empresaId?: string): UseQueryResult<EnpsDistribution, Error> => {
  return useQuery({
    queryKey: ['enpsDistribution', empresaId],
    queryFn: () => apiService.getEnpsDistribution(empresaId),
    staleTime: 2 * 60 * 1000,
  });
};

export const useTenureDistribution = (empresaId?: string): UseQueryResult<TenureDistribution, Error> => {
  return useQuery({
    queryKey: ['tenureDistribution', empresaId],
    queryFn: () => apiService.getTenureDistribution(empresaId),
    staleTime: 2 * 60 * 1000,
  });
};

export const useSatisfactionScores = (empresaId?: string): UseQueryResult<SatisfactionScores, Error> => {
  return useQuery({
    queryKey: ['satisfactionScores', empresaId],
    queryFn: () => apiService.getSatisfactionScores(empresaId),
    staleTime: 2 * 60 * 1000,
  });
};

// ====================
// Funcionários Hooks
// ====================

export const useFuncionarios = (params?: {
  empresa_id?: string;
  page?: number;
  page_size?: number;
}): UseQueryResult<FuncionarioPaginada, Error> => {
  return useQuery({
    queryKey: ['funcionarios', params],
    queryFn: () => apiService.getFuncionarios(params),
    staleTime: 1 * 60 * 1000, // 1 minute
  });
};

export const useContagemPorArea = (empresaId: string): UseQueryResult<ContagemPorArea[], Error> => {
  return useQuery({
    queryKey: ['contagemPorArea', empresaId],
    queryFn: () => apiService.getContagemPorArea(empresaId),
    enabled: !!empresaId,
    staleTime: 2 * 60 * 1000,
  });
};
