# Tech Playground - Análise de Feedback de Funcionários

Plataforma full-stack de análise de dados de feedback de funcionários com API REST, dashboard React e PostgreSQL.

---

## 📋 Índice

- [Tarefas Completadas](#-tarefas-completadas)
- [Como Executar](#-como-executar)
- [Como Visualizar os Resultados](#-como-visualizar-os-resultados)
- [Decisões e Premissas](#-decisões-e-premissas)
- [Stack Tecnológica](#️-stack-tecnológica)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Testes](#-testes)
- [Documentação Adicional](#-documentação-adicional)
- [Solução de Problemas](#-solução-de-problemas)

---

## ✅ Tarefas Completadas

### Tarefas Principais

- ✅ **Tarefa 1: Banco de Dados**

  - PostgreSQL 15 com schema normalizado (5NF)
  - 14 tabelas relacionadas com integridade referencial
  - Migrações automatizadas com SQL puro
  - Documentação completa: `DATABASE_ARCHITECTURE.md`
- ✅ **Tarefa 2: Dashboard Interativo**

  - React 18 + TypeScript + Material-UI
  - Interface responsiva e moderna
  - Visualizações em tempo real com gráficos interativos
  - Navegação por empresa → área → funcionário
- ✅ **Tarefa 3: Suite de Testes**

  - 237 testes (unitários + integração)
  - 90% de cobertura de código
  - Testes de API, repositórios, serviços e integridade de dados
  - Relatórios HTML de cobertura
- ✅ **Tarefa 4: Docker Compose**

  - 3 serviços containerizados (PostgreSQL, Backend, Frontend)
  - Configuração automática e orquestração
  - Scripts de inicialização e importação de dados
  - Ambiente isolado e reproduzível

### Tarefas Avançadas

- ✅ **Tarefa 6: Análises no Nível da Empresa**

  - eNPS (Employee Net Promoter Score)
  - Métricas de satisfação por dimensão
  - Distribuição por tempo de casa
- ✅ **Tarefa 7: Análises no Nível de Área**

  - Comparação de scores entre áreas
  - Comparação de eNPS entre áreas
  - Métricas detalhadas por área
  - Navegação hierárquica (Empresa → Diretoria → Gerência → Coordenação → Área)
- ✅ **Tarefa 8: Análises no Nível do Funcionário**

  - Perfil detalhado individual
  - Histórico de avaliações
  - Comparação com média da empresa
  - Comentários e feedback qualitativo
- ✅ **Tarefa 9: API REST**

  - FastAPI 2.0 com documentação automática OpenAPI/Swagger
  - Endpoints RESTful bem estruturados
  - Validação de dados com Pydantic
  - Tratamento de erros e respostas padronizadas

---

## 🚀 Como Executar

### Pré-requisitos

- Docker 20.10+
- Docker Compose 1.29+
- Portas disponíveis: 3000, 9876, 9432

### Instruções de Instalação

#### Passo 1: Clonar o Repositório

```bash
git clone https://github.com/Dyckson/tech_playground.git
cd tech_playground
```

#### Passo 2: Configurar Variáveis de Ambiente

Copie o arquivo de exemplo de variáveis de ambiente:

```bash
cp .env.example .env
```

O arquivo `.env.example` contém todas as configurações necessárias com valores padrão. Você pode customizar:

- Credenciais do banco de dados (`DB_USER`, `DB_PASSWORD`)
- Portas da API (`API_EXTERNAL_PORT`, `DB_EXTERNAL_PORT`)
- Configurações de importação (`IMPORT_CSV=true` carrega 500 funcionários automaticamente)

**Para um início rápido, os valores padrão já funcionam perfeitamente.**

#### Passo 3: Iniciar a Aplicação

```bash
# Recomendado: usando Make
make up

# Ou diretamente com docker-compose
docker-compose up -d
```

O sistema automaticamente:

- Cria e executa migrações do banco PostgreSQL
- Importa 500 funcionários do CSV (quando `IMPORT_CSV=true`)
- Inicia todos os 3 serviços (Banco de Dados, API Backend, Frontend)

#### Passo 4: Aguardar Inicialização

Aguarde aproximadamente 30-60 segundos para que todos os serviços iniciem completamente.

---

## 🎯 Como Visualizar os Resultados

### Dashboard Web

Acesse o dashboard interativo em seu navegador:

**🎨 URL:** http://localhost:3000

**Funcionalidades disponíveis:**

- **Visão Geral:** eNPS score, distribuição de promotores/neutros/detratores
- **Análises de Satisfação:** Scores em 7 dimensões (escala Likert 1-7)
- **Análise de Tempo de Casa:** Distribuição de funcionários por tempo na empresa
- **Gestão de Funcionários:** Lista paginada com busca e filtros (incluindo filtros por geração, gênero e localização)
- **Perfis Individuais:** Análises detalhadas por funcionário com dados demográficos completos
- **Comparações de Áreas:** Métricas comparativas entre áreas organizacionais

### API REST

Explore a API interativa através da documentação Swagger:

**📊 URL:** http://localhost:9876/docs

**Principais endpoints:**

**Health:**

- `GET /health` - Status da aplicação

**Analytics:**

- `GET /api/v1/analytics/enps` - Métricas de eNPS (Employee Net Promoter Score)
- `GET /api/v1/analytics/satisfaction-scores` - Scores de satisfação por dimensão
- `GET /api/v1/analytics/tenure-distribution` - Distribuição por tempo de casa
- `GET /api/v1/analytics/areas/scores-comparison` - Comparação de scores entre áreas
- `GET /api/v1/analytics/areas/enps-comparison` - Comparação de eNPS entre áreas
- `GET /api/v1/analytics/areas/{area_id}/detailed-metrics` - Métricas detalhadas de uma área

**Funcionários:**

- `GET /api/v1/funcionarios` - Listar funcionários (com paginação e filtros)
- `GET /api/v1/funcionarios/buscar` - Buscar funcionários por nome ou email
- `GET /api/v1/funcionarios/filtros` - Obter opções disponíveis para filtros
- `GET /api/v1/funcionarios/{funcionario_id}` - Detalhes do funcionário
- `GET /api/v1/funcionarios/{funcionario_id}/detailed-profile` - Perfil analítico completo
- `POST /api/v1/funcionarios` - Criar novo funcionário

**Hierarquia:**

- `GET /api/v1/hierarquia/empresas` - Listar empresas
- `GET /api/v1/hierarquia/empresas/{empresa_id}` - Buscar empresa por ID
- `GET /api/v1/hierarquia/empresas/{empresa_id}/arvore` - Árvore hierárquica completa
- `GET /api/v1/hierarquia/empresas/{empresa_id}/areas` - Listar áreas com hierarquia
- `GET /api/v1/hierarquia/areas/{area_id}/hierarquia` - Hierarquia de uma área específica
- `GET /api/v1/hierarquia/empresas/{empresa_id}/funcionarios/contagem` - Contagem de funcionários por área

## 💡 Decisões e Premissas

### Arquitetura e Design

**1. Arquitetura em Camadas**

- **Decisão:** Implementar arquitetura em 3 camadas (Controller → Service → Repository)
- **Razão:** Separação clara de responsabilidades, facilita manutenção e testes
- **Benefícios:** Código mais testável, reutilizável e escalável

**2. Normalização do Banco de Dados (5NF)**

- **Decisão:** Schema altamente normalizado com 14 tabelas
- **Razão:** Eliminar redundância de dados e garantir integridade referencial
- **Trade-off:** Queries mais complexas em troca de consistência de dados
- **Documentação:** Ver `DATABASE_ARCHITECTURE.md` para análise detalhada

**3. Docker Compose para Orquestração**

- **Decisão:** Usar Docker Compose em vez de Kubernetes
- **Razão:** Projeto de desenvolvimento/demonstração que não requer escalabilidade complexa
- **Benefícios:** Setup simplificado, ambiente reproduzível, ideal para desenvolvimento local

**4. FastAPI como Framework Backend**

- **Decisão:** FastAPI 2.0 em vez de Flask ou Django
- **Razão:** Performance superior, validação automática, documentação OpenAPI nativa
- **Benefícios:** Type hints Python, async nativo, developer experience excepcional

**5. Material-UI para Interface**

- **Decisão:** Material-UI v5 como biblioteca de componentes
- **Razão:** Componentes profissionais prontos, consistência visual, responsividade
- **Benefícios:** Desenvolvimento rápido, interface moderna e acessível

### Premissas de Dados

**1. Dados de Teste**

- **Premissa:** 500 funcionários fictícios são suficientes para demonstração
- **Fonte:** Arquivo `data.csv` com dados sintéticos
- **Importação:** Automática via variável `IMPORT_CSV=true`

**2. Escala Likert 1-7**

- **Premissa:** Dimensões de satisfação medidas em escala de 1 (muito insatisfeito) a 7 (muito satisfeito)
- **Justificativa:** Padrão comum em pesquisas de clima organizacional

**3. eNPS Calculation**

- **Premissa:** Escala 0-10 para cálculo de eNPS
  - Promotores: 9-10
  - Neutros: 7-8
  - Detratores: 0-6
- **Fórmula:** eNPS = % Promotores - % Detratores

**4. Hierarquia Organizacional**

- **Premissa:** Estrutura fixa de 5 níveis: Empresa → Diretoria → Gerência → Coordenação → Área
- **Justificativa:** Representa estrutura típica de empresas médias/grandes

### Decisões de Implementação

**1. Migrações em SQL Puro**

- **Decisão:** Não usar ORM para migrações
- **Razão:** Controle total sobre schema, performance otimizada
- **Trade-off:** Mais verboso, mas mais explícito e previsível

**2. Paginação Server-Side**

- **Decisão:** Paginação implementada no backend
- **Razão:** Performance com grandes volumes de dados
- **Padrão:** 20 registros por página (configurável)

**3. Testes com Banco Real**

- **Decisão:** Testes de integração usam PostgreSQL via Docker
- **Razão:** Testar comportamento real do banco, não mocks
- **Setup:** Banco de teste isolado, cleanup automático

**4. Validação com Pydantic**

- **Decisão:** Schemas Pydantic para validação de entrada/saída
- **Razão:** Type safety, validação automática, serialização
- **Benefícios:** Menos bugs, documentação automática

**5. CORS Configurado**

- **Decisão:** CORS liberado para localhost
- **Razão:** Permitir frontend em porta diferente do backend
- **Segurança:** Configurável via variável de ambiente `ALLOWED_ORIGINS`

---

## 🏗️ Stack Tecnológica

### Backend

- **FastAPI 2.0** - Framework web moderno e de alta performance
- **Python 3.11** - Linguagem de programação
- **PostgreSQL 15** - Banco de dados relacional
- **Psycopg2** - Driver PostgreSQL para Python
- **Pydantic** - Validação de dados e schemas
- **Pytest** - Framework de testes

### Frontend

- **React 18** - Biblioteca UI
- **TypeScript** - JavaScript tipado
- **Material-UI v5** - Biblioteca de componentes
- **Recharts** - Biblioteca de gráficos
- **Vite** - Build tool e dev server
- **Axios** - Cliente HTTP

### DevOps & Tools

- **Docker & Docker Compose** - Containerização
- **Make** - Automação de comandos
- **Ruff** - Linter Python
- **Black** - Formatador Python
- **Coverage.py** - Análise de cobertura de testes

### Dados

- **500 funcionários** - Dataset sintético
- **500 avaliações** - Uma por funcionário
- **3.500 respostas** - 7 dimensões × 500 funcionários

---

## 📁 Estrutura do Projeto

```
tech_playground/
├── backend/                    # Aplicação FastAPI
│   ├── app/
│   │   ├── controllers/       # Controllers da API (camada de apresentação)
│   │   ├── services/          # Lógica de negócio
│   │   ├── repositories/      # Acesso a dados (camada de persistência)
│   │   ├── schemas/           # Schemas Pydantic (validação)
│   │   ├── routes/            # Definição de rotas
│   │   ├── database/          # Conexão com banco
│   │   ├── config.py          # Configurações da aplicação
│   │   └── main.py            # Ponto de entrada FastAPI
│   ├── database/
│   │   └── migrations/        # Migrações SQL
│   ├── scripts/
│   │   ├── entrypoint.py      # Script de inicialização
│   │   └── import_csv.py      # Importação de dados
│   ├── tests/
│   │   ├── unitarios/         # Testes unitários (177 testes)
│   │   └── integracao/        # Testes de integração (60 testes)
│   ├── Dockerfile             # Imagem Docker do backend
│   ├── requirements.txt       # Dependências Python
│   ├── pytest.ini             # Configuração Pytest
│   └── ruff.toml              # Configuração linter
├── frontend/                   # Aplicação React
│   ├── src/
│   │   ├── components/        # Componentes reutilizáveis
│   │   ├── pages/             # Páginas da aplicação
│   │   ├── services/          # Clientes API
│   │   ├── hooks/             # React hooks customizados
│   │   ├── types/             # TypeScript types
│   │   ├── App.tsx            # Componente raiz
│   │   └── main.tsx           # Ponto de entrada React
│   ├── Dockerfile             # Imagem Docker do frontend
│   ├── package.json           # Dependências Node
│   ├── vite.config.ts         # Configuração Vite
│   └── tsconfig.json          # Configuração TypeScript
├── docker-compose.yml         # Orquestração dos serviços
├── Makefile                   # Comandos de automação
├── .env.example               # Template de variáveis de ambiente
├── README.md                  # Este arquivo
├── DATABASE_ARCHITECTURE.md   # Documentação do banco de dados
└── data.csv                   # Dataset de 500 funcionários
```

---

## 🧪 Testes

### Suite Completa: 237 Testes | 90% Cobertura

#### Executar Testes

```bash
# Todos os testes
make test

# Com relatório de cobertura
make test-cov

# Ou manualmente
docker exec tech_playground_backend pytest tests/ -v
```

#### Categorias de Testes

**Testes de Integração (60 testes)**

- `test_api_integration.py` - Testes end-to-end da API (31 testes)
- `test_database_integration.py` - Testes de integração com PostgreSQL (10 testes)
- `test_data_integrity.py` - Validação de integridade de dados (19 testes)

**Testes Unitários (177 testes)**

- `test_analytics_controller.py` - Controllers de analytics (24 testes)
- `test_analytics_repository.py` - Repositórios de analytics (19 testes)
- `test_analytics_service.py` - Serviços de analytics (18 testes)
- `test_base_repository.py` - Repositório base genérico (26 testes)
- `test_controllers.py` - Controllers gerais (38 testes)
- `test_repositories.py` - Repositórios gerais (35 testes)
- `test_services.py` - Serviços gerais (17 testes)

#### Métricas de Cobertura

```
TOTAL: 948 statements | 95 miss | 90% coverage
```

**Cobertura por módulo:**

- Controllers: 74-100%
- Services: 97-100%
- Repositories: 78-100%
- Schemas: 100%
- Base Repository: 100%

---

## 📚 Documentação Adicional

### Arquivos de Documentação

- **`DATABASE_ARCHITECTURE.md`** - Análise completa do design do banco de dados

  - Modelo de dados normalizado (5NF)
  - Diagrama ER
  - Análise de alternativas (MongoDB vs PostgreSQL, ORM vs SQL puro)
  - Decisões de indexação
  - Estratégias de performance
- **`README.md`** - Este arquivo (guia principal)
- **Documentação Interativa da API** - http://localhost:9876/docs

  - Swagger UI automático
  - Testar endpoints diretamente no navegador
  - Schemas de request/response
  - Códigos de status HTTP

### Comandos Úteis

```bash
# Mostrar todos os comandos disponíveis
make help

# Iniciar aplicação
make up

# Parar aplicação
make down

# Ver logs em tempo real
make logs

# Reiniciar containers
make restart

# Executar testes
make test

# Executar testes com cobertura HTML
make test-cov

# Verificar qualidade do código
make lint

# Formatar código automaticamente
make format
```

---

## 🔧 Solução de Problemas

### Portas em Uso

Se as portas 3000, 9876 ou 9432 já estiverem em uso:

```bash
# Parar containers
make down

# Limpar volumes e rebuild
docker-compose down -v && docker-compose up -d --build
```

Ou edite o arquivo `.env` para usar portas diferentes.

### Containers Não Iniciam

```bash
# Verificar logs
make logs

# Rebuild forçado
docker-compose up -d --build --force-recreate
```

### Banco de Dados Não Responde

```bash
# Verificar status do PostgreSQL
docker-compose exec postgres pg_isready -U tech_user

# Conectar ao banco manualmente
docker-compose exec postgres psql -U tech_user -d tech_playground
```

### Dados Não Importados

```bash
# Verificar variável de ambiente
cat .env | grep IMPORT_CSV

# Reimportar dados manualmente
docker exec tech_playground_backend python /app/scripts/import_csv.py
```

### Erros de Permissão

```bash
# Linux/Mac: ajustar permissões
sudo chown -R $USER:$USER .
```

---

## 🔗 Links Úteis

- **Dashboard:** http://localhost:3000
- **API Backend:** http://localhost:9876
- **API Docs (Swagger):** http://localhost:9876/docs
- **PostgreSQL:** localhost:9432

---

## 📧 Contato

Para dúvidas ou sugestões sobre este projeto, abra uma issue no repositório.

---

## 📄 Licença

Este projeto foi desenvolvido para fins educacionais e de demonstração.
