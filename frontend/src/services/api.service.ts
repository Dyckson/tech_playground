import axios, { AxiosInstance, AxiosError } from 'axios';
import type {
  Empresa,
  FuncionarioPaginada,
  FuncionarioResponse,
  FiltroOpcao,
  ContagemPorArea,
  HierarquiaCompleta,
  CompanyMetrics,
  EnpsDistribution,
  TenureDistribution,
  SatisfactionScores,
  ApiError
} from '@/types/api.types';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:9876/api/v1';

class ApiService {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      timeout: 10000,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Response interceptor for error handling
    this.client.interceptors.response.use(
      (response) => response,
      (error: AxiosError<ApiError>) => {
        const apiError: ApiError = {
          detail: error.response?.data?.detail || error.message || 'Erro desconhecido',
          status: error.response?.status,
        };
        return Promise.reject(apiError);
      }
    );
  }

  // ====================
  // Hierarquia Endpoints
  // ====================

  async getEmpresas(): Promise<Empresa[]> {
    const response = await this.client.get<Empresa[]>('/hierarquia/empresas');
    return response.data;
  }

  async getEmpresa(empresaId: string): Promise<Empresa> {
    const response = await this.client.get<Empresa>(`/hierarquia/empresas/${empresaId}`);
    return response.data;
  }

  async getContagemPorArea(empresaId: string): Promise<ContagemPorArea[]> {
    const response = await this.client.get<ContagemPorArea[]>(
      `/hierarquia/empresas/${empresaId}/funcionarios/contagem`
    );
    return response.data;
  }

  async getAreas(empresaId: string): Promise<HierarquiaCompleta[]> {
    const response = await this.client.get<HierarquiaCompleta[]>(
      `/hierarquia/empresas/${empresaId}/areas`
    );
    return response.data;
  }

  // ====================
  // Funcionários Endpoints
  // ====================

  async getFuncionarios(params?: {
    empresa_id?: string;
    page?: number;
    page_size?: number;
    areas?: string[];
    cargos?: string[];
    localidades?: string[];
  }): Promise<FuncionarioPaginada> {
    const response = await this.client.get<FuncionarioPaginada>('/funcionarios', {
      params,
    });
    return response.data;
  }

  async getFuncionario(funcionarioId: string): Promise<FuncionarioResponse> {
    const response = await this.client.get<FuncionarioResponse>(`/funcionarios/${funcionarioId}`);
    return response.data;
  }

  async buscarFuncionarios(params: {
    termo: string;
    empresa_id?: string;
    page?: number;
    page_size?: number;
  }): Promise<FuncionarioPaginada> {
    const response = await this.client.get<FuncionarioPaginada>('/funcionarios/buscar', {
      params,
    });
    return response.data;
  }

  async getFiltros(empresaId?: string): Promise<{
    areas: FiltroOpcao[];
    cargos: FiltroOpcao[];
    localidades: FiltroOpcao[];
  }> {
    const response = await this.client.get('/funcionarios/filtros', {
      params: { empresa_id: empresaId },
    });
    return response.data;
  }

  // ====================
  // Analytics Endpoints (Mock for now)
  // ====================

  async getCompanyMetrics(_empresaId?: string): Promise<CompanyMetrics> {
    // TODO: Replace with real endpoint when backend implements it
    // For now, get total from first page (backend returns total count)
    const funcionarios = await this.getFuncionarios({
      empresa_id: _empresaId,
      page_size: 1,
      page: 1,
    });

    return {
      totalFuncionarios: funcionarios.total,
      totalEmpresas: 1, // Mock
      enpsAverage: 7.5, // Mock - needs real calculation
      satisfactionAverage: 6.2, // Mock - needs real calculation
      responseRate: 85, // Mock
    };
  }

  async getEnpsDistribution(_empresaId?: string): Promise<EnpsDistribution> {
    // TODO: Replace with real endpoint
    return {
      promoters: 45,
      passives: 30,
      detractors: 25,
      score: 20, // (45-25)
      distribution: [
        { score: 0, count: 5 },
        { score: 1, count: 8 },
        { score: 2, count: 12 },
        { score: 3, count: 15 },
        { score: 4, count: 18 },
        { score: 5, count: 20 },
        { score: 6, count: 22 },
        { score: 7, count: 45 },
        { score: 8, count: 55 },
        { score: 9, count: 80 },
        { score: 10, count: 120 },
      ],
    };
  }

  async getTenureDistribution(_empresaId?: string): Promise<TenureDistribution> {
    // TODO: Replace with real endpoint
    return {
      lessThan1Year: 120,
      oneToTwoYears: 150,
      threeToFiveYears: 180,
      fiveToTenYears: 69,
      moreThan10Years: 0,
    };
  }

  async getSatisfactionScores(_empresaId?: string): Promise<SatisfactionScores> {
    // TODO: Replace with real endpoint
    return {
      interesseNoCargo: 6.5,
      contribuicao: 6.8,
      aprendizadoDesenvolvimento: 5.9,
      feedback: 6.2,
      interacaoGestor: 6.4,
      clarezaCarreira: 5.5,
      expectativaPermanencia: 5.8,
    };
  }
}

export const apiService = new ApiService();
export default apiService;
