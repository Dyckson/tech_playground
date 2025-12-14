import { useQuery } from '@tanstack/react-query';
import axios from 'axios';
import type { HierarquiaCompleta, ContagemPorArea } from '../types/api.types';

const API_BASE_URL = 'http://localhost:9876/api/v1';

// ====================
// Tipos de dados
// ====================

interface AreaTreeNode {
  id: string;
  nome: string;
  tipo: 'diretoria' | 'gerencia' | 'coordenacao' | 'area';
  gerencias?: AreaTreeNode[];
  coordenacoes?: AreaTreeNode[];
  areas?: AreaTreeNode[];
}

interface AreaMetrics {
  total_funcionarios: number;
  enps_score: number | null;
  score_medio: number | null;
  promotores: number;
  neutros: number;
  detratores: number;
}

// ====================
// Hook: Lista de áreas com hierarquia
// ====================

export const useAreas = (empresaId?: string) => {
  return useQuery<HierarquiaCompleta[]>({
    queryKey: ['areas', empresaId],
    queryFn: async () => {
      if (!empresaId) {
        // Se não tiver empresa, busca primeira empresa disponível
        const { data: empresas } = await axios.get(`${API_BASE_URL}/hierarquia/empresas`);
        if (empresas.length === 0) throw new Error('Nenhuma empresa encontrada');
        empresaId = empresas[0].id;
      }
      
      const { data } = await axios.get<HierarquiaCompleta[]>(
        `${API_BASE_URL}/hierarquia/empresas/${empresaId}/areas`
      );
      return data;
    },
    enabled: true,
    staleTime: 5 * 60 * 1000, // 5 minutos
  });
};

// ====================
// Hook: Árvore hierárquica completa
// ====================

export const useAreaHierarchy = (empresaId?: string) => {
  return useQuery<AreaTreeNode[]>({
    queryKey: ['areaHierarchy', empresaId],
    queryFn: async () => {
      if (!empresaId) {
        const { data: empresas } = await axios.get(`${API_BASE_URL}/hierarquia/empresas`);
        if (empresas.length === 0) throw new Error('Nenhuma empresa encontrada');
        empresaId = empresas[0].id;
      }
      
      const { data } = await axios.get<AreaTreeNode[]>(
        `${API_BASE_URL}/hierarquia/empresas/${empresaId}/arvore`
      );
      return data;
    },
    enabled: true,
    staleTime: 5 * 60 * 1000,
  });
};

// ====================
// Hook: Detalhes de uma área específica
// ====================

export const useAreaDetails = (areaId?: string) => {
  return useQuery<HierarquiaCompleta>({
    queryKey: ['areaDetails', areaId],
    queryFn: async () => {
      if (!areaId) throw new Error('ID da área é obrigatório');
      
      const { data } = await axios.get<HierarquiaCompleta>(
        `${API_BASE_URL}/hierarquia/areas/${areaId}/hierarquia`
      );
      return data;
    },
    enabled: !!areaId,
    staleTime: 5 * 60 * 1000,
  });
};

// ====================
// Hook: Contagem de funcionários por área
// ====================

export const useAreaEmployeeCount = (empresaId?: string) => {
  return useQuery<ContagemPorArea[]>({
    queryKey: ['areaEmployeeCount', empresaId],
    queryFn: async () => {
      if (!empresaId) {
        const { data: empresas } = await axios.get(`${API_BASE_URL}/hierarquia/empresas`);
        if (empresas.length === 0) throw new Error('Nenhuma empresa encontrada');
        empresaId = empresas[0].id;
      }
      
      const { data } = await axios.get<ContagemPorArea[]>(
        `${API_BASE_URL}/hierarquia/empresas/${empresaId}/funcionarios/contagem`
      );
      return data;
    },
    enabled: true,
    staleTime: 5 * 60 * 1000,
  });
};

// ====================
// Hook: Métricas calculadas de uma área
// ====================

export const useAreaMetrics = (areaId?: string) => {
  return useQuery<AreaMetrics>({
    queryKey: ['areaMetrics', areaId],
    queryFn: async () => {
      if (!areaId) throw new Error('ID da área é obrigatório');
      
      // Buscar todos os funcionários da área com paginação incremental
      // Backend tem limite máximo de 100 items por página (le=100 no controller)
      let allFuncionarios: any[] = [];
      let page = 1;
      let hasMore = true;
      
      while (hasMore) {
        const { data: funcionariosData } = await axios.get(
          `${API_BASE_URL}/funcionarios`,
          {
            params: {
              areas: areaId,
              page,
              page_size: 100, // Respeita limite máximo do backend
            },
          }
        );
        
        allFuncionarios = [...allFuncionarios, ...funcionariosData.items];
        hasMore = funcionariosData.items.length === 100;
        page++;
      }

      const funcionarios = allFuncionarios;
      const total_funcionarios = funcionarios.length;

      if (total_funcionarios === 0) {
        return {
          total_funcionarios: 0,
          enps_score: null,
          score_medio: null,
          promotores: 0,
          neutros: 0,
          detratores: 0,
        };
      }

      // Calcular eNPS e scores
      let promotores = 0;
      let neutros = 0;
      let detratores = 0;
      let somaScores = 0;
      let countScores = 0;

      funcionarios.forEach((func: any) => {
        // eNPS baseado na expectativa_permanencia (escala 1-7)
        const expectativa = func.expectativa_permanencia;
        // Verificar se não é null/undefined/0 (0 significa sem avaliação no backend antigo)
        if (expectativa != null && expectativa > 0) {
          // Convertendo escala 1-7 para lógica eNPS:
          // 6-7 = Promotores
          // 5 = Neutros  
          // 1-4 = Detratores
          if (expectativa >= 6) {
            promotores++;
          } else if (expectativa === 5) {
            neutros++;
          } else if (expectativa >= 1) {
            detratores++;
          }
        }

        // Score médio geral
        const score = func.score_medio_geral;
        // Verificar se não é null/undefined/0 (0 significa sem avaliação no backend antigo)
        if (score != null && score > 0) {
          somaScores += score;
          countScores++;
        }
      });

      const total_respostas = promotores + neutros + detratores;
      const enps_score = total_respostas > 0
        ? Math.round(((promotores - detratores) / total_respostas) * 100)
        : null;

      const score_medio = countScores > 0 ? somaScores / countScores : null;

      return {
        total_funcionarios,
        enps_score,
        score_medio,
        promotores,
        neutros,
        detratores,
      };
    },
    enabled: !!areaId,
    staleTime: 5 * 60 * 1000,
  });
};

// ====================
// Hook: Primeira empresa (helper)
// ====================

export const useFirstEmpresa = () => {
  return useQuery<string>({
    queryKey: ['firstEmpresa'],
    queryFn: async () => {
      const { data: empresas } = await axios.get(`${API_BASE_URL}/hierarquia/empresas`);
      if (empresas.length === 0) throw new Error('Nenhuma empresa encontrada');
      return empresas[0].id;
    },
    staleTime: 10 * 60 * 1000, // 10 minutos
  });
};
