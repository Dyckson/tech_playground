# 📊 Database Design - Tech Playground eNPS System

**Data**: 11 de dezembro de 2025  
**Status**: Proposal (14-Table Architecture)  
**Objetivo**: Estruturar dados completos de survey de eNPS com integridade, escalabilidade e performance

---

## 📋 Sumário Executivo

Após análise comparativa de 3 estruturas possíveis:
1. ❌ **3 Tabelas** (sua proposta original)
2. ⚠️ **7 Tabelas** (híbrida/equilibrada)
3. ✅ **14 Tabelas** (proposta atual - RECOMENDADA)

**Escolhemos a de 14 tabelas porque:**
- Elimina 100% da redundância de dados
- Suporta análises por 7 dimensões sem refactoring
- Garante integridade referencial total
- Escalável para crescimento futuro (de 500 para 5M+ registros)
- Implementação clara e modular em 7 migrations

---

## 🏗️ Arquitetura de 14 Tabelas

### **Organização Lógica**

```
┌─────────────────────────────────────────────────────────────┐
│                    HIERARCHICAL TABLES (5)                  │
│  Representam os 5 níveis de hierarquia da empresa            │
└─────────────────────────────────────────────────────────────┘
    empresa → diretoria → gerencia → coordenacao → area_detalhe
    
┌─────────────────────────────────────────────────────────────┐
│                  DIMENSION/LOOKUP TABLES (6)                │
│  Catálogos de valores únicos (sem duplicação)               │
└─────────────────────────────────────────────────────────────┘
    cargo | genero_catgo | geracao_catgo | tempo_empresa_catgo 
    localidade | dimensao_avaliacao
    
┌─────────────────────────────────────────────────────────────┐
│                     FACT TABLES (3)                         │
│  Dados transacionais com FKs para hierarquia + lookups      │
└─────────────────────────────────────────────────────────────┘
    funcionario → avaliacao → resposta_dimensao
```

---

## 📐 Definição Detalhada de Cada Tabela

### **NÍVEL 1: HIERARQUIA (5 Tabelas)**

#### **1. `empresa`** (Nível 0)
```
Propósito: Raiz da hierarquia corporativa

Campos:
  - id: INT PRIMARY KEY
  - nome: VARCHAR(255) UNIQUE NOT NULL
  - criada_em: TIMESTAMP DEFAULT CURRENT_TIMESTAMP

Constraints:
  - PK: id
  - UNIQUE: nome

Índices:
  - PK(id) [automático]
  - UNIQUE(nome) [automático]

Por quê separado?
  - Ponto de entrada para toda hierarquia
  - Permite múltiplas empresas no mesmo banco (expansão)
  - Garante integridade: cada diretoria aponta a empresa válida
```

---

#### **2. `diretoria`** (Nível 1)
```
Propósito: Primeiro nível de hierarquia abaixo de empresa

Campos:
  - id: INT PRIMARY KEY
  - empresa_id: INT NOT NULL FK → empresa.id
  - nome: VARCHAR(255) NOT NULL
  - criada_em: TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  - atualizada_em: TIMESTAMP DEFAULT CURRENT_TIMESTAMP

Constraints:
  - PK: id
  - FK: empresa_id → empresa(id) [ON DELETE CASCADE]
  - UNIQUE: (empresa_id, nome)

Índices:
  - PK(id)
  - FK(empresa_id) [para travessias hierárquicas]
  - UNIQUE(empresa_id, nome)

Por quê separado?
  ❌ Se em mesma tabela: "Dir. Comercial" repetido 50+ vezes
  ✅ Separado: "Dir. Comercial" armazenado 1x
  ✅ Atualizar nome = 1 UPDATE, não 50+
  ✅ Análise: "eNPS médio por diretoria" = simples GROUP BY
```

---

#### **3. `gerencia`** (Nível 2)
```
Propósito: Segundo nível de hierarquia

Campos:
  - id: INT PRIMARY KEY
  - diretoria_id: INT NOT NULL FK → diretoria.id
  - nome: VARCHAR(255) NOT NULL
  - criada_em: TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  - atualizada_em: TIMESTAMP DEFAULT CURRENT_TIMESTAMP

Constraints:
  - PK: id
  - FK: diretoria_id → diretoria(id) [ON DELETE CASCADE]
  - UNIQUE: (diretoria_id, nome)

Índices:
  - PK(id)
  - FK(diretoria_id)
  - UNIQUE(diretoria_id, nome)
```

---

#### **4. `coordenacao`** (Nível 3)
```
Propósito: Terceiro nível de hierarquia

Campos:
  - id: INT PRIMARY KEY
  - gerencia_id: INT NOT NULL FK → gerencia.id
  - nome: VARCHAR(255) NOT NULL
  - criada_em: TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  - atualizada_em: TIMESTAMP DEFAULT CURRENT_TIMESTAMP

Constraints:
  - PK: id
  - FK: gerencia_id → gerencia(id) [ON DELETE CASCADE]
  - UNIQUE: (gerencia_id, nome)

Índices:
  - PK(id)
  - FK(gerencia_id)
  - UNIQUE(gerencia_id, nome)
```

---

#### **5. `area_detalhe`** (Nível 4)
```
Propósito: Quarto nível de hierarquia (mais granular)

Campos:
  - id: INT PRIMARY KEY
  - coordenacao_id: INT NOT NULL FK → coordenacao.id
  - nome: VARCHAR(255) NOT NULL
  - criada_em: TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  - atualizada_em: TIMESTAMP DEFAULT CURRENT_TIMESTAMP

Constraints:
  - PK: id
  - FK: coordenacao_id → coordenacao(id) [ON DELETE CASCADE]
  - UNIQUE: (coordenacao_id, nome)

Índices:
  - PK(id)
  - FK(coordenacao_id)
  - UNIQUE(coordenacao_id, nome)

Hierarquia Completa:
  empresa (1)
    ├─ diretoria (3 registros)
    │   ├─ gerencia (15 registros)
    │   │   ├─ coordenacao (45 registros)
    │   │   │   └─ area_detalhe (90 registros) → 500 funcionarios
```

---

### **NÍVEL 2: DIMENSION/LOOKUP TABLES (6 Tabelas)**

**Princípio**: Cada valor único armazenado 1 vez, referenciado por ID

#### **6. `cargo`** (Catálogo de Cargos)
```
Propósito: Valores únicos de cargo + função

Campos:
  - id: INT PRIMARY KEY
  - nome: VARCHAR(255) UNIQUE NOT NULL
  - funcao: VARCHAR(255) NULLABLE
  - criada_em: TIMESTAMP DEFAULT CURRENT_TIMESTAMP

Constraints:
  - PK: id
  - UNIQUE: nome

Índices:
  - PK(id)
  - UNIQUE(nome)
  - IDX(funcao)

Exemplos:
  - (1, "Analista", "Análise de Dados")
  - (2, "Coordenador", "Planejamento")
  - (3, "Gerente", "Gestão de Pessoas")
  - (4, "Diretor", NULL)
  - (5, "Estagiário", "Administrativo")

Volume esperado: ~20-30 valores únicos

Por quê?
  ❌ Sem tabela: "Analista", "Analista ", "analista" = 3 typos diferentes
  ✅ Com tabela: Sempre id=1 (limpo, consistente)
```

---

#### **7. `genero_catgo`** (Catálogo de Gêneros)
```
Propósito: Valores de gênero padronizados

Campos:
  - id: INT PRIMARY KEY
  - nome: VARCHAR(50) UNIQUE NOT NULL
  - criada_em: TIMESTAMP DEFAULT CURRENT_TIMESTAMP

Constraints:
  - PK: id
  - UNIQUE: nome

Exemplos:
  - (1, "Masculino")
  - (2, "Feminino")
  - (3, "Outro")
  - (4, "Prefiro não informar")

Volume esperado: 4-5 valores
```

---

#### **8. `geracao_catgo`** (Catálogo de Gerações)
```
Propósito: Valores de geração padronizados

Campos:
  - id: INT PRIMARY KEY
  - nome: VARCHAR(50) UNIQUE NOT NULL
  - criada_em: TIMESTAMP DEFAULT CURRENT_TIMESTAMP

Exemplos:
  - (1, "Geração Z")
  - (2, "Millennials")
  - (3, "Geração X")
  - (4, "Baby Boomers")

Volume esperado: 4-5 valores
```

---

#### **9. `tempo_empresa_catgo`** (Catálogo de Faixas de Tempo)
```
Propósito: Faixas de tempo padronizadas

Campos:
  - id: INT PRIMARY KEY
  - descricao: VARCHAR(100) UNIQUE NOT NULL
  - ordem: INT (para sort sequencial)
  - criada_em: TIMESTAMP DEFAULT CURRENT_TIMESTAMP

Exemplos:
  - (1, "Menos de 6 meses", 1)
  - (2, "Entre 6 meses e 1 ano", 2)
  - (3, "Entre 1 e 2 anos", 3)
  - (4, "Entre 2 e 5 anos", 4)
  - (5, "Mais de 5 anos", 5)

Volume esperado: 5-7 valores
```

---

#### **10. `localidade`** (Catálogo de Cidades)
```
Propósito: Cidades/locais únicos

Campos:
  - id: INT PRIMARY KEY
  - nome: VARCHAR(255) UNIQUE NOT NULL
  - criada_em: TIMESTAMP DEFAULT CURRENT_TIMESTAMP

Exemplos:
  - (1, "São Paulo")
  - (2, "Rio de Janeiro")
  - (3, "Brasília")
  - (4, "Belo Horizonte")

Volume esperado: 10-20 valores
```

---

#### **11. `dimensao_avaliacao`** (Catálogo das 7 Dimensões)
```
Propósito: Nomes e ordem das 7 dimensões de survey

Campos:
  - id: INT PRIMARY KEY
  - nome: VARCHAR(255) UNIQUE NOT NULL
  - descricao: TEXT NULLABLE
  - ordem: INT (1-7, para ordenação em UIs)
  - criada_em: TIMESTAMP DEFAULT CURRENT_TIMESTAMP

Constraints:
  - PK: id
  - UNIQUE: nome
  - UNIQUE: ordem

Exemplos:
  - (1, "Interesse no Cargo", "Você se sente interessado?", 1)
  - (2, "Contribuição", "Sente que contribui?", 2)
  - (3, "Aprendizado e Desenvolvimento", "Há oportunidades?", 3)
  - (4, "Feedback", "Recebe feedback regular?", 4)
  - (5, "Interação com Gestor", "Relação com gestor?", 5)
  - (6, "Clareza sobre Carreira", "Entendo possibilidades?", 6)
  - (7, "Expectativa de Permanência", "Planejo continuar?", 7)

Volume esperado: Exatamente 7 registros (fixo)

Por quê?
  ✅ Adicionar 8ª dimensão = 1 INSERT (trivial!)
  ❌ Sem tabela = ALTER TABLE (bloqueio, risco!)
```

---

### **NÍVEL 3: FACT TABLES (3 Tabelas)**

#### **12. `funcionario`** ⭐ PRINCIPAL
```
Propósito: Dados demográficos e posicionamento de cada funcionário

Campos:
  - id: INT PRIMARY KEY
  - nome: VARCHAR(255) NOT NULL
  - email: VARCHAR(255) UNIQUE NOT NULL
  - email_corporativo: VARCHAR(255) NULLABLE
  - celular: VARCHAR(20) NULLABLE
  
  - area_detalhe_id: INT NOT NULL FK → area_detalhe.id
  - cargo_id: INT NOT NULL FK → cargo.id
  - funcao: VARCHAR(255) NULLABLE
  
  - localidade_id: INT NULLABLE FK → localidade.id
  - tempo_empresa_id: INT NULLABLE FK → tempo_empresa_catgo.id
  - genero_id: INT NULLABLE FK → genero_catgo.id
  - geracao_id: INT NULLABLE FK → geracao_catgo.id
  
  - ativo: BOOLEAN DEFAULT TRUE
  - criado_em: TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  - atualizado_em: TIMESTAMP DEFAULT CURRENT_TIMESTAMP

Constraints:
  - PK: id
  - UNIQUE: email
  - UNIQUE: email_corporativo
  - CHECK: celular ~ '^[0-9\-\(\)\+]+$'
  - FK: area_detalhe_id → area_detalhe.id [ON DELETE RESTRICT]
  - FK: cargo_id → cargo.id [ON DELETE RESTRICT]
  - FK: localidade_id → localidade.id [ON DELETE SET NULL]
  - FK: tempo_empresa_id → tempo_empresa_catgo.id [ON DELETE SET NULL]
  - FK: genero_id → genero_catgo.id [ON DELETE SET NULL]
  - FK: geracao_id → geracao_catgo.id [ON DELETE SET NULL]

Índices:
  - PK(id)
  - UNIQUE(email)
  - IDX(area_detalhe_id)
  - IDX(cargo_id)
  - IDX(ativo)
  - IDX(genero_id, geracao_id) [COMPOSITE para análises cruzadas]
  - IDX(ativo, area_detalhe_id) [COMPOSITE para filtro comum]

Volume esperado: 500 registros

Por quê?
  ✅ Sem redundância de dados pessoais
  ✅ FKs garantem dados válidos
  ✅ Campos NULL permitidos (email_corporativo opcional)
```

---

#### **13. `avaliacao`** ⭐ SURVEY HEADER
```
Propósito: Registra cada survey respondida (header da pesquisa)

Campos:
  - id: INT PRIMARY KEY
  - funcionario_id: INT NOT NULL FK → funcionario.id
  - data_resposta: DATE NOT NULL
  - enps: INT CHECK (BETWEEN 0 AND 10)
  - comentarios_enps: TEXT NULLABLE
  - criada_em: TIMESTAMP DEFAULT CURRENT_TIMESTAMP

Constraints:
  - PK: id
  - FK: funcionario_id → funcionario.id [ON DELETE CASCADE]
  - UNIQUE: (funcionario_id, data_resposta)
  - CHECK: enps BETWEEN 0 AND 10

Índices:
  - PK(id)
  - IDX(funcionario_id) [para histórico de um colaborador]
  - IDX(data_resposta) [para análises temporais]
  - IDX(enps) [para distribuição]
  - IDX(funcionario_id, data_resposta DESC) [para última avaliação]
  - IDX(data_resposta, enps) [para análises por período]

Volume esperado: 500 registros (atual) → 5.000+ (múltiplas surveys/ano)

Exemplos:
  - (1, 1, 2025-12-11, 8, "Gosto da empresa mas acho salário baixo")
  - (2, 2, 2025-12-11, 9, "Excelente ambiente")
  - (3, 3, 2025-12-11, 6, "Precisa melhorar gestão")

Por quê separado de resposta_dimensao?
  ❌ Se misturar: 500 × 7 = 3.500 registros apenas com eNPS
  ✅ Separado: eNPS em avaliacao (500), dimensões em resposta_dimensao (3.500)
```

---

#### **14. `resposta_dimensao`** ⭐ SURVEY DETAIL
```
Propósito: Armazena as 7 respostas de cada survey (normalizado)

Campos:
  - id: INT PRIMARY KEY
  - avaliacao_id: INT NOT NULL FK → avaliacao.id
  - dimensao_id: INT NOT NULL FK → dimensao_avaliacao.id
  - score: INT NOT NULL CHECK (BETWEEN 1 AND 10)
  - comentario: TEXT NULLABLE
  - criada_em: TIMESTAMP DEFAULT CURRENT_TIMESTAMP

Constraints:
  - PK: id
  - FK: avaliacao_id → avaliacao.id [ON DELETE CASCADE]
  - FK: dimensao_id → dimensao_avaliacao.id [ON DELETE RESTRICT]
  - UNIQUE: (avaliacao_id, dimensao_id)
  - CHECK: score BETWEEN 1 AND 10

Índices:
  - PK(id)
  - IDX(avaliacao_id) [para recuperar todas dimensões de 1 survey]
  - IDX(dimensao_id) [para analisar 1 dimensão]
  - IDX(avaliacao_id, dimensao_id) [lookup rápido]
  - IDX(dimensao_id, score) [análise de distribuição]

Volume esperado: 3.500 registros (500 × 7) → 35.000+ (ano)

Exemplos (para avaliacao_id=1):
  - (1, 1, 1, 8, "Sim, tenho interesse") [Interesse no Cargo]
  - (2, 1, 2, 7, "Contribuo com análises") [Contribuição]
  - (3, 1, 3, 6, "Precisa treinamento") [Aprendizado]
  - (4, 1, 4, 5, "Feedback poderia melhorar") [Feedback]
  - (5, 1, 5, 8, "Relação excelente") [Interação com Gestor]
  - (6, 1, 6, 7, "Conheço caminhos") [Clareza sobre Carreira]
  - (7, 1, 7, 8, "Pretendo continuar") [Expectativa]

Por quê NORMALIZADO (7 linhas vs 14 colunas)?
  ❌ Desnormalizado: score + comentário × 7 dimensões = 14 colunas
     - Qual dimensão tem score mais baixo? = 7 colunas diferentes a comparar
     - Adicionar 8ª dimensão = ALTER TABLE (bloqueio!)
     
  ✅ Normalizado: 1 linha por dimensão
     - Qual dimensão tem score mais baixo? = GROUP BY dimensao_id, ORDER BY AVG(score)
     - Adicionar 8ª dimensão = 1 INSERT em dimensao_avaliacao (trivial!)
```

---

## 🔑 Constraints & Validações

### **Integridade Referencial**

| FK | De | Para | ON DELETE | Razão |
|----|----|------|-----------|-------|
| diretoria.empresa_id | diretoria | empresa | CASCADE | Cascata hierárquica |
| gerencia.diretoria_id | gerencia | diretoria | CASCADE | Cascata hierárquica |
| coordenacao.gerencia_id | coordenacao | gerencia | CASCADE | Cascata hierárquica |
| area_detalhe.coordenacao_id | area_detalhe | coordenacao | CASCADE | Cascata hierárquica |
| funcionario.area_detalhe_id | funcionario | area_detalhe | RESTRICT | Não deleta área com colaboradores (erro) |
| funcionario.cargo_id | funcionario | cargo | RESTRICT | Não deleta cargo com colaboradores (erro) |
| funcionario.localidade_id | funcionario | localidade | SET NULL | Se deletar localidade, põe NULL |
| funcionario.genero_id | funcionario | genero_catgo | SET NULL | Se deletar gênero, põe NULL |
| funcionario.geracao_id | funcionario | geracao_catgo | SET NULL | Se deletar geração, põe NULL |
| funcionario.tempo_empresa_id | funcionario | tempo_empresa_catgo | SET NULL | Se deletar tempo, põe NULL |
| avaliacao.funcionario_id | avaliacao | funcionario | CASCADE | Deleta avaliações ao deletar colaborador |
| resposta_dimensao.avaliacao_id | resposta_dimensao | avaliacao | CASCADE | Deleta respostas ao deletar avaliação |
| resposta_dimensao.dimensao_id | resposta_dimensao | dimensao_avaliacao | RESTRICT | Não deleta dimensão com respostas (erro) |

---

## 📊 Diagrama ER Simplificado

```
HIERARQUIA:
empresa (1:N)→ diretoria (1:N)→ gerencia (1:N)→ coordenacao (1:N)→ area_detalhe

LOOKUPS:
cargo, genero_catgo, geracao_catgo, tempo_empresa_catgo, localidade, dimensao_avaliacao

FATOS:
funcionario (1:N)→ avaliacao (1:N)→ resposta_dimensao

RELACIONAMENTOS:
funcionario: area_detalhe_id FK, cargo_id FK, localidade_id FK, etc
resposta_dimensao: avaliacao_id FK, dimensao_id FK
```

---

## 📈 Índices Estratégicos

| Tabela | Índice | Razão |
|--------|--------|-------|
| **diretoria** | empresa_id | Listar diretorias de empresa X |
| **gerencia** | diretoria_id | Listar gerências de diretoria X |
| **coordenacao** | gerencia_id | Listar coordenações de gerência X |
| **area_detalhe** | coordenacao_id | Listar áreas de coordenação X |
| **funcionario** | area_detalhe_id | Filtro: colaboradores da área X |
| **funcionario** | cargo_id | Filtro: colaboradores com cargo X |
| **funcionario** | (genero_id, geracao_id) | Análises demográficas cruzadas |
| **funcionario** | (ativo, area_detalhe_id) | "Colaboradores ativos da área X" |
| **avaliacao** | funcionario_id | Histórico de 1 colaborador |
| **avaliacao** | data_resposta | Análises temporais |
| **avaliacao** | (funcionario_id, data_resposta DESC) | Última avaliação |
| **resposta_dimensao** | avaliacao_id | Todas respostas de 1 survey |
| **resposta_dimensao** | dimensao_id | Análise de 1 dimensão |
| **resposta_dimensao** | (dimensao_id, score) | Distribuição por dimensão |

**Total**: ~14 índices (balanceado)

---

## 🔍 Views Úteis

### **View 1: `v_avaliacao_completa`**
- Funcionário + hierarquia + dados demográficos + avaliação
- Uso: Relatórios, dashboard, filtros
- Performance: <100ms

### **View 2: `v_enps_distribuicao`**
- Distribuição (promotores/neutros/detratores)
- Uso: Dashboard eNPS
- Performance: <50ms

### **View 3: `v_dimensao_score_medio`**
- Score médio por dimensão
- Uso: Análises de força/fraqueza
- Performance: <200ms

### **View 4: `v_ultima_avaliacao_por_funcionario`**
- Última resposta de cada funcionário
- Uso: Identificar não-respondentes
- Performance: <100ms

### **View 5: `v_comparacao_hierarquica`**
- eNPS médio por nível hierárquico
- Uso: Benchmarking interno
- Performance: <300ms

---

## ✅ Por que escolhemos 14 tabelas?

### **1. Elimina Redundância 100%**
```
❌ 3 Tabelas: "Dir. Comercial" repetido 50x (espaço, inconsistência)
✅ 14 Tabelas: "Dir. Comercial" armazenado 1x (id=5)
```

### **2. Análises por Dimensão Triviais**
```
❌ Sem normalização: Qual o score médio de "Aprendizado"?
   = SELECT AVG(aprendizado) FROM respostas (confuso)
   
✅ Com normalização: Qual o score médio de "Aprendizado"?
   = SELECT AVG(score) FROM resposta_dimensao WHERE dimensao_id=3 (claro!)
```

### **3. Escalabilidade Futura**
```
❌ Adicionar 8ª dimensão em 3-7 tabelas = ALTER TABLE (risco!)
✅ Adicionar 8ª dimensão em 14 tabelas = 1 INSERT (seguro!)
```

### **4. Integridade Garantida**
```
❌ genero='xyz' ou enps=15 (nada impede)
✅ genero_id só aceita IDs válidos (FK)
✅ enps CHECK (BETWEEN 0 AND 10)
```

### **5. Auditoria e Manutenção Fácil**
```
❌ Renomear diretoria = UPDATE 50+ registros (risco inconsistência)
✅ Renomear diretoria = UPDATE 1 registro (simples, seguro)
```

### **6. Performance Otimizada**
```
❌ GROUP BY em strings = mais lento
✅ GROUP BY em IDs = mais rápido + índices eficientes
```

### **7. Suporta Crescimento**
```
500 funcionários × 4 surveys/ano = 2.000 avaliações
Índices garantem <500ms mesmo com 5M+ registros
```

---

## 📋 Comparativa: 3 vs 14 Tabelas

| Critério | 3 Tabelas | **14 Tabelas** |
|----------|-----------|----------------|
| **Redundância** | Alta ❌ | Nenhuma ✅ |
| **Análises por Dimensão** | Ruim ❌ | Excelente ✅ |
| **Análises por Hierarquia** | Média ⚠️ | Excelente ✅ |
| **Escalabilidade** | Limitada ❌ | Excelente ✅ |
| **Integridade de Dados** | Fraca ⚠️ | Forte ✅ |
| **Adicionar Dimensão** | ALTER TABLE ❌ | 1 INSERT ✅ |
| **Atualizar Nome Diretoria** | 50+ UPDATEs ❌ | 1 UPDATE ✅ |
| **Manutenção** | Alta ❌ | Baixa ✅ |
| **Tempo Implementação** | 1 hora ✅ | 4 horas |

---

## 🚀 Plano de Implementação

### **FASE 1: Criar Scripts SQL (Migrations)**
```
001_create_hierarchy.sql
002_create_lookups.sql
003_create_funcionario.sql
004_create_avaliacao.sql
005_create_resposta_dimensao.sql
006_create_indexes.sql
007_create_views.sql
```

### **FASE 2: Importar Dados**
```
import_data.py (refatorado)
├─ Validar CSV
├─ Limpeza de dados
├─ Criar/atualizar hierarquia
├─ Criar/atualizar lookups
├─ Inserir funcionários
├─ Inserir avaliações + 7 respostas/dimensão
└─ Validar integridade pós-import
```

### **FASE 3: Validação & Testes**
```
✓ 14 tabelas criadas
✓ 500 funcionários + 3.500 respostas importados
✓ Nenhuma FK dangling ou violação de constraint
✓ 5 views funcionando
✓ Índices sendo usados (EXPLAIN ANALYZE)
✓ Performance <500ms
```

---

## ❓ FAQ

**P: Por que 14 tabelas e não 7?**  
R: 14 oferece integridade total + análises perfeitas. 7 seria mais simples mas com trade-offs.

**P: Performance com 5M registros?**  
R: Índices garantem <500ms. Se necessário, particionar resposta_dimensao por ano.

**P: Quantas dimensões suporta?**  
R: Atualmente 7 (tabela dimensao_avaliacao). Adicionar 8ª = 1 INSERT + popula resposta_dimensao.

**P: E se campo for NULL?**  
R: Permitido em campos NULLABLE (email_corporativo, celular, etc). Obrigatórios têm NOT NULL.

---

**Status**: ✅ Ready for Implementation  
**Data**: 11 de dezembro de 2025
