-- 001_create_initial_schema.sql
-- Criação completa do schema do banco de dados

-- Extensões
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ===== HIERARQUIA (5 tabelas) =====

-- Empresa (raiz da hierarquia)
CREATE TABLE IF NOT EXISTS empresa (
    id_empresa UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nome_empresa VARCHAR(255) NOT NULL UNIQUE,
    cnpj VARCHAR(20),
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ativo BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Diretoria
CREATE TABLE IF NOT EXISTS diretoria (
    id_diretoria UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    id_empresa UUID NOT NULL REFERENCES empresa(id_empresa) ON DELETE CASCADE,
    nome_diretoria VARCHAR(255) NOT NULL,
    sigla_diretoria VARCHAR(20),
    responsavel_nome VARCHAR(255),
    responsavel_email VARCHAR(255),
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ativo BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(id_empresa, nome_diretoria)
);

-- Gerência
CREATE TABLE IF NOT EXISTS gerencia (
    id_gerencia UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    id_diretoria UUID NOT NULL REFERENCES diretoria(id_diretoria) ON DELETE CASCADE,
    nome_gerencia VARCHAR(255) NOT NULL,
    sigla_gerencia VARCHAR(20),
    responsavel_nome VARCHAR(255),
    responsavel_email VARCHAR(255),
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ativo BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(id_diretoria, nome_gerencia)
);

-- Coordenação
CREATE TABLE IF NOT EXISTS coordenacao (
    id_coordenacao UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    id_gerencia UUID NOT NULL REFERENCES gerencia(id_gerencia) ON DELETE CASCADE,
    nome_coordenacao VARCHAR(255) NOT NULL,
    sigla_coordenacao VARCHAR(20),
    responsavel_nome VARCHAR(255),
    responsavel_email VARCHAR(255),
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ativo BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(id_gerencia, nome_coordenacao)
);

-- Área Detalhe
CREATE TABLE IF NOT EXISTS area_detalhe (
    id_area_detalhe UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    id_coordenacao UUID NOT NULL REFERENCES coordenacao(id_coordenacao) ON DELETE CASCADE,
    nome_area_detalhe VARCHAR(255) NOT NULL,
    sigla_area VARCHAR(20),
    responsavel_nome VARCHAR(255),
    responsavel_email VARCHAR(255),
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ativo BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(id_coordenacao, nome_area_detalhe)
);

-- ===== LOOKUPS/CATEGORIAS (6 tabelas) =====

-- Cargo
CREATE TABLE IF NOT EXISTS cargo (
    id_cargo UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nome_cargo VARCHAR(255) NOT NULL UNIQUE,
    nivel_hierarquico VARCHAR(50),
    descricao TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Gênero (Categoria)
CREATE TABLE IF NOT EXISTS genero_catgo (
    id_genero_catgo UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nome_genero VARCHAR(50) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Geração (Categoria)
CREATE TABLE IF NOT EXISTS geracao_catgo (
    id_geracao_catgo UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nome_geracao VARCHAR(50) NOT NULL UNIQUE,
    faixa_etaria VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tempo de Empresa (Categoria)
CREATE TABLE IF NOT EXISTS tempo_empresa_catgo (
    id_tempo_empresa_catgo UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nome_tempo_empresa VARCHAR(100) NOT NULL UNIQUE,
    meses_min INTEGER,
    meses_max INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Localidade
CREATE TABLE IF NOT EXISTS localidade (
    id_localidade UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nome_localidade VARCHAR(255) NOT NULL UNIQUE,
    cidade VARCHAR(100),
    estado VARCHAR(2),
    pais VARCHAR(50) DEFAULT 'Brasil',
    tipo VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Dimensão de Avaliação
CREATE TABLE IF NOT EXISTS dimensao_avaliacao (
    id_dimensao_avaliacao UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nome_dimensao VARCHAR(255) NOT NULL UNIQUE,
    descricao TEXT,
    tipo_escala VARCHAR(50),
    valor_min INTEGER,
    valor_max INTEGER,
    ordem_exibicao INTEGER,
    ativa BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ===== TRANSACIONAIS (3 tabelas) =====

-- Funcionário
CREATE TABLE IF NOT EXISTS funcionario (
    id_funcionario UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nome_funcionario VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE,
    email_corporativo VARCHAR(255),
    cpf VARCHAR(20) UNIQUE,
    id_area_detalhe UUID NOT NULL REFERENCES area_detalhe(id_area_detalhe),
    id_cargo UUID NOT NULL REFERENCES cargo(id_cargo),
    data_nascimento DATE,
    id_genero_catgo UUID REFERENCES genero_catgo(id_genero_catgo),
    id_geracao_catgo UUID REFERENCES geracao_catgo(id_geracao_catgo),
    id_tempo_empresa_catgo UUID REFERENCES tempo_empresa_catgo(id_tempo_empresa_catgo),
    id_localidade UUID REFERENCES localidade(id_localidade),
    data_admissao DATE NOT NULL,
    data_desligamento DATE,
    tipo_contratacao VARCHAR(100),
    telefone VARCHAR(20),
    endereco TEXT,
    ativo BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Avaliação
CREATE TABLE IF NOT EXISTS avaliacao (
    id_avaliacao UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    id_funcionario UUID NOT NULL REFERENCES funcionario(id_funcionario) ON DELETE CASCADE,
    data_avaliacao DATE NOT NULL DEFAULT CURRENT_DATE,
    periodo_avaliacao VARCHAR(50),
    comentario_geral TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Resposta Dimensão
CREATE TABLE IF NOT EXISTS resposta_dimensao (
    id_resposta_dimensao UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    id_avaliacao UUID NOT NULL REFERENCES avaliacao(id_avaliacao) ON DELETE CASCADE,
    id_dimensao_avaliacao UUID NOT NULL REFERENCES dimensao_avaliacao(id_dimensao_avaliacao),
    valor_resposta INTEGER NOT NULL,
    comentario TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(id_avaliacao, id_dimensao_avaliacao)
);

-- ===== ÍNDICES =====

-- Hierarquia
CREATE INDEX idx_diretoria_empresa ON diretoria(id_empresa);
CREATE INDEX idx_gerencia_diretoria ON gerencia(id_diretoria);
CREATE INDEX idx_coordenacao_gerencia ON coordenacao(id_gerencia);
CREATE INDEX idx_area_coordenacao ON area_detalhe(id_coordenacao);

-- Funcionário
CREATE INDEX idx_funcionario_area ON funcionario(id_area_detalhe);
CREATE INDEX idx_funcionario_cargo ON funcionario(id_cargo);
CREATE INDEX idx_funcionario_localidade ON funcionario(id_localidade);
CREATE INDEX idx_funcionario_ativo ON funcionario(ativo);
CREATE INDEX idx_funcionario_email ON funcionario(email);
CREATE INDEX idx_funcionario_email_corporativo ON funcionario(email_corporativo);

-- Avaliação
CREATE INDEX idx_avaliacao_funcionario ON avaliacao(id_funcionario);
CREATE INDEX idx_avaliacao_data ON avaliacao(data_avaliacao);

-- Resposta
CREATE INDEX idx_resposta_avaliacao ON resposta_dimensao(id_avaliacao);
CREATE INDEX idx_resposta_dimensao ON resposta_dimensao(id_dimensao_avaliacao);

-- Empresa ativo
CREATE INDEX idx_empresa_ativo ON empresa(ativo);
CREATE INDEX idx_diretoria_ativo ON diretoria(ativo);
CREATE INDEX idx_gerencia_ativo ON gerencia(ativo);
CREATE INDEX idx_coordenacao_ativo ON coordenacao(ativo);
CREATE INDEX idx_area_ativo ON area_detalhe(ativo);

-- ===== CONSTRAINTS ADICIONAIS =====

-- Email corporativo único apenas quando não nulo
CREATE UNIQUE INDEX idx_funcionario_email_corporativo_unico ON funcionario(email_corporativo) WHERE email_corporativo IS NOT NULL;

-- ===== TRIGGERS =====

-- Função para atualizar updated_at
CREATE OR REPLACE FUNCTION update_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Triggers de update
CREATE TRIGGER trigger_empresa_update_timestamp
    BEFORE UPDATE ON empresa
    FOR EACH ROW EXECUTE FUNCTION update_timestamp();

CREATE TRIGGER trigger_diretoria_update_timestamp
    BEFORE UPDATE ON diretoria
    FOR EACH ROW EXECUTE FUNCTION update_timestamp();

CREATE TRIGGER trigger_gerencia_update_timestamp
    BEFORE UPDATE ON gerencia
    FOR EACH ROW EXECUTE FUNCTION update_timestamp();

CREATE TRIGGER trigger_coordenacao_update_timestamp
    BEFORE UPDATE ON coordenacao
    FOR EACH ROW EXECUTE FUNCTION update_timestamp();

CREATE TRIGGER trigger_area_update_timestamp
    BEFORE UPDATE ON area_detalhe
    FOR EACH ROW EXECUTE FUNCTION update_timestamp();

CREATE TRIGGER trigger_funcionario_update_timestamp
    BEFORE UPDATE ON funcionario
    FOR EACH ROW EXECUTE FUNCTION update_timestamp();
