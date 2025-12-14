// ====================
// API Response Types
// ====================

export interface Empresa {
  id: string;
  nome: string;
  created_at: string;
}

export interface FuncionarioResponse {
  id: string;
  nome: string;
  email: string;
  email_corporativo: string | null;
  funcao: string | null;
  empresa_id: string;
  area_detalhe_id: string;
  cargo_id: string;
  genero_id: string | null;
  geracao_id: string | null;
  tempo_empresa_id: string | null;
  localidade_id: string | null;
  ativo: boolean;
  created_at: string;
  cargo_nome: string | null;
  area_nome: string;
  localidade_nome: string | null;
  genero_nome: string | null;
  geracao_nome: string | null;
  tempo_empresa_nome: string | null;
}

export interface FuncionarioPaginada {
  items: FuncionarioResponse[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

export interface FiltroOpcao {
  id: string;
  nome: string;
}

export interface ContagemPorArea {
  area_id: string;
  area_nome: string;
  total_funcionarios: number;
}

export interface HierarquiaCompleta {
  empresa_id: string;
  empresa: string;
  diretoria_id: string;
  diretoria: string;
  gerencia_id: string;
  gerencia: string;
  coordenacao_id: string;
  coordenacao: string;
  area_id: string;
  area: string;
}

// ====================
// Analytics Types
// ====================

export interface CompanyMetrics {
  totalFuncionarios: number;
  totalEmpresas: number;
  enpsAverage: number;
  satisfactionAverage: number;
  responseRate: number;
}

export interface EnpsDistribution {
  promoters: number; // 9-10
  passives: number;  // 7-8
  detractors: number; // 0-6
  score: number; // NPS calculation
  distribution: { score: number; count: number }[]; // 1-7 distribution
}

export interface TenureDistribution {
  lessThan1Year: number;
  oneToTwoYears: number;
  threeToFiveYears: number;
  fiveToTenYears: number;
  moreThan10Years: number;
}

export interface SatisfactionScores {
  interesseNoCargo: number;
  contribuicao: number;
  aprendizadoDesenvolvimento: number;
  feedback: number;
  interacaoGestor: number;
  clarezaCarreira: number;
  expectativaPermanencia: number;
}

// ====================
// Dimension Types (Likert Scale 1-5)
// ====================

export type LikertScore = 1 | 2 | 3 | 4 | 5;

export interface DimensionData {
  name: string;
  average: number;
  favorability: number; // % of 4-5 responses
  responses: {
    score: LikertScore;
    count: number;
  }[];
}

// ====================
// API Error Types
// ====================

export interface ApiError {
  detail: string;
  status?: number;
}

// ====================
// Loading States
// ====================

export interface LoadingState<T> {
  data: T | null;
  isLoading: boolean;
  error: ApiError | null;
}
