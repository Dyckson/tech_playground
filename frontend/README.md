# Frontend - Dashboard Corporativo

Dashboard de analytics para visualização de métricas e indicadores de satisfação de funcionários, desenvolvido com React, TypeScript e Bootstrap.

## 🎯 Objetivo

Implementar a **Task 6 - Data Visualization (Company Level)** do projeto Tech Playground, fornecendo uma interface web moderna e responsiva para visualização de dados consolidados da empresa.

## 🚀 Stack Tecnológica

- **Framework**: React 18.2 com TypeScript 5.2
- **Build Tool**: Vite 5.0
- **UI Framework**: Bootstrap 5.3 + React-Bootstrap 2.10
- **Gráficos**: Chart.js 4.4 + react-chartjs-2 5.2
- **Estado**: TanStack React Query 5.14
- **HTTP Client**: Axios 1.6
- **Roteamento**: React Router DOM 6.21
- **Docker**: Multi-stage build com imagem distroless

## 📊 Funcionalidades

### Dashboard Principal
- **Métricas Gerais**: Total de funcionários, eNPS médio, satisfação média, taxa de resposta
- **Distribuição eNPS**: Gráfico de pizza com promotores, passivos e detratores
- **Tempo de Casa**: Gráfico de barras com distribuição por faixa de tempo
- **Satisfação por Dimensão**: Gráfico radar com 7 dimensões de feedback (Likert 1-5)

### Características
- ✅ **Mobile-First**: Design responsivo otimizado para dispositivos móveis
- ✅ **TypeScript**: Tipagem forte com interfaces para toda a API
- ✅ **React Query**: Cache inteligente e atualização automática de dados
- ✅ **Error Handling**: Tratamento de erros com feedback visual
- ✅ **Loading States**: Estados de carregamento para melhor UX
- ✅ **Path Aliases**: Imports limpos com `@/components`, `@/services`, etc.

## 🏗️ Arquitetura

```
frontend/
├── src/
│   ├── components/           # Componentes React reutilizáveis
│   │   ├── CompanyOverview.tsx          # Cards com métricas gerais
│   │   ├── EnpsDistributionChart.tsx    # Gráfico eNPS (Doughnut)
│   │   ├── TenureDistributionChart.tsx  # Gráfico tempo de casa (Bar)
│   │   └── SatisfactionScoresChart.tsx  # Gráfico dimensões (Radar)
│   ├── hooks/                # Custom React hooks
│   │   └── useApi.ts                    # Hooks React Query para API
│   ├── pages/                # Páginas principais
│   │   └── Dashboard.tsx                # Dashboard principal
│   ├── services/             # Camada de serviços
│   │   └── api.service.ts               # Cliente API com Axios
│   ├── types/                # Definições TypeScript
│   │   └── api.types.ts                 # Interfaces da API
│   ├── App.tsx               # Componente raiz com Router
│   ├── main.tsx              # Entry point React 18
│   └── vite-env.d.ts         # Types do Vite
├── index.html                # HTML template
├── package.json              # Dependências NPM
├── tsconfig.json             # Configuração TypeScript
├── vite.config.ts            # Configuração Vite
├── Dockerfile                # Multi-stage build
├── server.js                 # Server Node.js para produção
└── .dockerignore             # Exclusões do build Docker
```

## 🔧 Configuração e Desenvolvimento

### Pré-requisitos
- Node.js 20+ (recomendado: 20 LTS)
- npm ou yarn
- Backend rodando em `http://localhost:9876`

### Instalação

```bash
# Instalar dependências
npm install

# Configurar variáveis de ambiente (opcional)
echo "VITE_API_URL=http://localhost:9876/api/v1" > .env.local
```

### Scripts Disponíveis

```bash
# Desenvolvimento (hot reload)
npm run dev

# Build para produção
npm run build

# Preview do build de produção
npm run preview

# Type checking
npm run type-check

# Linting
npm run lint
```

### Desenvolvimento Local

1. Certifique-se de que o backend está rodando:
   ```bash
   cd ../backend
   docker-compose up postgres backend
   ```

2. Inicie o servidor de desenvolvimento:
   ```bash
   npm run dev
   ```

3. Acesse: `http://localhost:3000`

## 🐳 Docker

### Build da Imagem

```bash
# Build local
docker build -t tech-playground-frontend .

# Build com variável de ambiente customizada
docker build --build-arg VITE_API_URL=http://api.example.com/api/v1 -t tech-playground-frontend .
```

### Executar Container

```bash
# Executar localmente
docker run -p 3000:3000 tech-playground-frontend

# Com Docker Compose (recomendado)
cd ..
docker-compose up frontend
```

### Multi-stage Build

O Dockerfile implementa um build otimizado em 2 estágios:

1. **Builder (node:20-alpine)**:
   - Instala dependências
   - Compila o código TypeScript
   - Gera bundle otimizado com Vite

2. **Production (distroless/nodejs20-debian12)**:
   - Imagem mínima sem shell (segurança)
   - Apenas arquivos estáticos e server.js
   - Tamanho final reduzido

## 🌐 API Integration

### Endpoints Utilizados

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/api/v1/hierarquia/empresas` | Lista todas as empresas |
| GET | `/api/v1/hierarquia/empresas/{id}` | Detalhes de uma empresa |
| GET | `/api/v1/funcionarios` | Lista funcionários (paginado) |
| GET | `/api/v1/hierarquia/empresas/{id}/funcionarios/contagem` | Contagem por área |

> **Nota**: Atualmente, os endpoints de analytics (métricas, eNPS, tenure, satisfaction) estão mockados no frontend. Quando o backend implementar esses endpoints, basta remover os mocks em `api.service.ts`.

### Variáveis de Ambiente

| Variável | Padrão | Descrição |
|----------|--------|-----------|
| `VITE_API_URL` | `http://localhost:9876/api/v1` | URL base da API backend |

## 📱 Design Responsivo

O dashboard é construído com abordagem **mobile-first** utilizando o sistema de grid do Bootstrap:

- **Mobile (xs)**: 1 coluna (col-12)
- **Tablet (md)**: 2 colunas (col-md-6)
- **Desktop (lg)**: 3 colunas (col-lg-4)

### Breakpoints
- `xs`: < 576px (mobile)
- `sm`: ≥ 576px (mobile grande)
- `md`: ≥ 768px (tablet)
- `lg`: ≥ 992px (desktop)
- `xl`: ≥ 1200px (desktop grande)

## 🎨 Estilização

- **Bootstrap 5.3**: Sistema de design base
- **Bootstrap Icons**: Ícones vetoriais
- **Chart.js**: Gráficos interativos e responsivos
- **Custom CSS**: Mínimo necessário (inline no Bootstrap)

## 🔍 Type Safety

Todas as respostas da API são tipadas com interfaces TypeScript:

```typescript
// Exemplo: api.types.ts
export interface CompanyMetrics {
  totalFuncionarios: number;
  enpsAverage: number;
  satisfactionAverage: number;
  responseRate: number;
}

// Uso nos componentes
const { data: metrics } = useCompanyMetrics();
// metrics é do tipo CompanyMetrics | undefined
```

## 🚦 Estado e Cache

React Query gerencia todo o estado assíncrono:

- **Stale Time**: 2 minutos (dados considerados "frescos")
- **Cache Time**: 5 minutos (dados mantidos em cache)
- **Retry**: 1 tentativa em caso de erro
- **Refetch on Focus**: Desabilitado

## 🧪 Testes (Futuro)

```bash
# Testes unitários (a implementar)
npm run test

# Coverage (a implementar)
npm run test:coverage
```

## 📝 TODOs

- [ ] Implementar endpoints de analytics no backend
- [ ] Remover mocks de `api.service.ts`
- [ ] Adicionar filtro por empresa
- [ ] Adicionar seletor de período (data range)
- [ ] Implementar testes unitários (Vitest + Testing Library)
- [ ] Adicionar skeleton loaders
- [ ] Implementar export de dados (CSV/PDF)
- [ ] Dark mode
- [ ] Adicionar mais gráficos (departamento, localidade, etc.)

## 🐛 Troubleshooting

### Erro de CORS
```
Access to fetch at 'http://localhost:9876/api/v1/...' from origin 'http://localhost:3000' has been blocked by CORS policy
```

**Solução**: Verifique se o backend tem `http://localhost:3000` nos `ALLOWED_ORIGINS` em `backend/app/config.py`.

### Erro de conexão com API
```
Network Error / Failed to fetch
```

**Soluções**:
1. Verifique se o backend está rodando: `docker-compose ps`
2. Teste diretamente: `curl http://localhost:9876/api/v1/health`
3. Verifique logs: `docker-compose logs backend`

### Build falha no Docker
```
error during build
```

**Soluções**:
1. Limpe cache do Docker: `docker builder prune`
2. Reconstrua: `docker-compose build --no-cache frontend`
3. Verifique Node version no builder: deve ser 20+

## 📚 Referências

- [React Documentation](https://react.dev)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [Vite Guide](https://vitejs.dev/guide/)
- [Bootstrap Docs](https://getbootstrap.com/docs/5.3/)
- [Chart.js](https://www.chartjs.org/docs/latest/)
- [React Query](https://tanstack.com/query/latest/docs/react/overview)
- [Distroless Images](https://github.com/GoogleContainerTools/distroless)

## 👥 Contribuição

Frontend desenvolvido como parte do projeto Tech Playground para implementação da Task 6 (Data Visualization - Company Level).

---

**Status**: ✅ Task 6 - Data Visualization (Company Level) - COMPLETO

**Próximos passos**: Implementar analytics endpoints no backend e remover mocks do frontend.
