-- 002_seed_initial_data.sql
-- Dados iniciais para o sistema

-- ===== EMPRESAS =====
INSERT INTO empresa (nome_empresa, cnpj) VALUES
('TechCorp Brasil', '12.345.678/0001-90'),
('InnovaSoft Ltda', '98.765.432/0001-10'),
('CloudServices XYZ', '11.222.333/0001-44');

-- ===== HIERARQUIA - TechCorp Brasil =====
DO $$
DECLARE
    v_empresa_id UUID;
    v_diretoria_ti UUID;
    v_diretoria_rh UUID;
    v_gerencia_dev UUID;
    v_gerencia_infra UUID;
    v_gerencia_talent UUID;
    v_coord_backend UUID;
    v_coord_frontend UUID;
    v_coord_devops UUID;
    v_coord_recrutamento UUID;
BEGIN
    -- Empresa
    SELECT id_empresa INTO v_empresa_id FROM empresa WHERE nome_empresa = 'TechCorp Brasil';
    
    -- Diretorias
    INSERT INTO diretoria (id_empresa, nome_diretoria, sigla_diretoria) VALUES
    (v_empresa_id, 'Tecnologia da Informação', 'TI') RETURNING id_diretoria INTO v_diretoria_ti;
    
    INSERT INTO diretoria (id_empresa, nome_diretoria, sigla_diretoria) VALUES
    (v_empresa_id, 'Recursos Humanos', 'RH') RETURNING id_diretoria INTO v_diretoria_rh;
    
    -- Gerências de TI
    INSERT INTO gerencia (id_diretoria, nome_gerencia, sigla_gerencia) VALUES
    (v_diretoria_ti, 'Desenvolvimento', 'DEV') RETURNING id_gerencia INTO v_gerencia_dev;
    
    INSERT INTO gerencia (id_diretoria, nome_gerencia, sigla_gerencia) VALUES
    (v_diretoria_ti, 'Infraestrutura', 'INFRA') RETURNING id_gerencia INTO v_gerencia_infra;
    
    -- Gerência de RH
    INSERT INTO gerencia (id_diretoria, nome_gerencia, sigla_gerencia) VALUES
    (v_diretoria_rh, 'Gestão de Talentos', 'TALENT') RETURNING id_gerencia INTO v_gerencia_talent;
    
    -- Coordenações
    INSERT INTO coordenacao (id_gerencia, nome_coordenacao) VALUES
    (v_gerencia_dev, 'Backend') RETURNING id_coordenacao INTO v_coord_backend;
    
    INSERT INTO coordenacao (id_gerencia, nome_coordenacao) VALUES
    (v_gerencia_dev, 'Frontend') RETURNING id_coordenacao INTO v_coord_frontend;
    
    INSERT INTO coordenacao (id_gerencia, nome_coordenacao) VALUES
    (v_gerencia_infra, 'DevOps') RETURNING id_coordenacao INTO v_coord_devops;
    
    INSERT INTO coordenacao (id_gerencia, nome_coordenacao) VALUES
    (v_gerencia_talent, 'Recrutamento e Seleção') RETURNING id_coordenacao INTO v_coord_recrutamento;
    
    -- Áreas
    INSERT INTO area_detalhe (id_coordenacao, nome_area_detalhe) VALUES
    (v_coord_backend, 'APIs e Microserviços'),
    (v_coord_backend, 'Banco de Dados'),
    (v_coord_frontend, 'Web Applications'),
    (v_coord_frontend, 'Mobile Apps'),
    (v_coord_devops, 'CI/CD'),
    (v_coord_devops, 'Cloud Infrastructure'),
    (v_coord_recrutamento, 'Tech Hiring'),
    (v_coord_recrutamento, 'Business Hiring');
END $$;

-- ===== LOOKUPS/CATEGORIAS =====

-- Cargos
INSERT INTO cargo (nome_cargo, nivel_hierarquico) VALUES
('Desenvolvedor Júnior', 'Júnior'),
('Desenvolvedor Pleno', 'Pleno'),
('Desenvolvedor Sênior', 'Sênior'),
('Tech Lead', 'Liderança'),
('Engenheiro de Software', 'Pleno'),
('Arquiteto de Software', 'Sênior'),
('DevOps Engineer', 'Pleno'),
('Analista de RH', 'Pleno'),
('Coordenador', 'Coordenação'),
('Gerente', 'Gerência'),
('Diretor', 'Diretoria');

-- Gêneros
INSERT INTO genero_catgo (nome_genero) VALUES
('Masculino'),
('Feminino'),
('Não-binário'),
('Prefiro não informar');

-- Gerações
INSERT INTO geracao_catgo (nome_geracao, faixa_etaria) VALUES
('Baby Boomer', '1946-1964'),
('Geração X', '1965-1980'),
('Millennials', '1981-1996'),
('Geração Z', '1997-2012');

-- Tempo de Empresa
INSERT INTO tempo_empresa_catgo (nome_tempo_empresa, meses_min, meses_max) VALUES
('Menos de 6 meses', 0, 5),
('6 meses a 1 ano', 6, 11),
('1 a 2 anos', 12, 23),
('2 a 5 anos', 24, 59),
('5 a 10 anos', 60, 119),
('Mais de 10 anos', 120, NULL);

-- Localidades
INSERT INTO localidade (nome_localidade, cidade, estado, tipo) VALUES
('São Paulo - Matriz', 'São Paulo', 'SP', 'Escritório'),
('São Paulo - Filial Paulista', 'São Paulo', 'SP', 'Escritório'),
('Rio de Janeiro - Escritório', 'Rio de Janeiro', 'RJ', 'Escritório'),
('Belo Horizonte - Hub Tech', 'Belo Horizonte', 'MG', 'Escritório'),
('Remoto - Brasil', NULL, NULL, 'Remoto'),
('Remoto - Internacional', NULL, NULL, 'Remoto');

-- Dimensões de Avaliação
INSERT INTO dimensao_avaliacao (nome_dimensao, descricao, tipo_escala, valor_min, valor_max, ordem_exibicao) VALUES
('Liderança', 'Avaliação da qualidade da liderança imediata', 'Likert', 1, 5, 1),
('Ambiente de Trabalho', 'Satisfação com o ambiente físico e cultura organizacional', 'Likert', 1, 5, 2),
('Reconhecimento', 'Percepção sobre reconhecimento e valorização do trabalho', 'Likert', 1, 5, 3),
('Desenvolvimento Profissional', 'Oportunidades de crescimento e aprendizado', 'Likert', 1, 5, 4),
('Remuneração e Benefícios', 'Satisfação com pacote de remuneração total', 'Likert', 1, 5, 5),
('Equilíbrio Trabalho-Vida', 'Percepção sobre work-life balance', 'Likert', 1, 5, 6),
('Expectativa de Permanência (eNPS)', 'Probabilidade de recomendar a empresa como lugar para trabalhar', 'NPS', 0, 10, 7);

-- ===== FUNCIONÁRIOS DE EXEMPLO =====
DO $$
DECLARE
    v_area_apis UUID;
    v_area_web UUID;
    v_cargo_dev_jr UUID;
    v_cargo_dev_pl UUID;
    v_cargo_dev_sr UUID;
    v_genero_m UUID;
    v_genero_f UUID;
    v_geracao_z UUID;
    v_geracao_millennial UUID;
    v_tempo_1a2 UUID;
    v_tempo_2a5 UUID;
    v_local_sp UUID;
    v_local_remoto UUID;
    v_func_1 UUID;
    v_func_2 UUID;
    v_func_3 UUID;
    v_aval_1 UUID;
    v_aval_2 UUID;
    v_aval_3 UUID;
    v_dim_lideranca UUID;
    v_dim_ambiente UUID;
    v_dim_reconhecimento UUID;
    v_dim_desenvolvimento UUID;
    v_dim_remuneracao UUID;
    v_dim_equilibrio UUID;
    v_dim_enps UUID;
BEGIN
    -- Buscar IDs necessários
    SELECT id_area_detalhe INTO v_area_apis FROM area_detalhe WHERE nome_area_detalhe = 'APIs e Microserviços';
    SELECT id_area_detalhe INTO v_area_web FROM area_detalhe WHERE nome_area_detalhe = 'Web Applications';
    SELECT id_cargo INTO v_cargo_dev_jr FROM cargo WHERE nome_cargo = 'Desenvolvedor Júnior';
    SELECT id_cargo INTO v_cargo_dev_pl FROM cargo WHERE nome_cargo = 'Desenvolvedor Pleno';
    SELECT id_cargo INTO v_cargo_dev_sr FROM cargo WHERE nome_cargo = 'Desenvolvedor Sênior';
    SELECT id_genero_catgo INTO v_genero_m FROM genero_catgo WHERE nome_genero = 'Masculino';
    SELECT id_genero_catgo INTO v_genero_f FROM genero_catgo WHERE nome_genero = 'Feminino';
    SELECT id_geracao_catgo INTO v_geracao_z FROM geracao_catgo WHERE nome_geracao = 'Geração Z';
    SELECT id_geracao_catgo INTO v_geracao_millennial FROM geracao_catgo WHERE nome_geracao = 'Millennials';
    SELECT id_tempo_empresa_catgo INTO v_tempo_1a2 FROM tempo_empresa_catgo WHERE nome_tempo_empresa = '1 a 2 anos';
    SELECT id_tempo_empresa_catgo INTO v_tempo_2a5 FROM tempo_empresa_catgo WHERE nome_tempo_empresa = '2 a 5 anos';
    SELECT id_localidade INTO v_local_sp FROM localidade WHERE nome_localidade = 'São Paulo - Matriz';
    SELECT id_localidade INTO v_local_remoto FROM localidade WHERE nome_localidade = 'Remoto - Brasil';
    
    -- Funcionários
    INSERT INTO funcionario (nome_funcionario, email, email_corporativo, id_area_detalhe, id_cargo, id_genero_catgo, id_geracao_catgo, id_tempo_empresa_catgo, id_localidade, data_admissao, tipo_contratacao)
    VALUES ('João Silva', 'joao.silva@email.com', 'joao.silva@techcorp.com', v_area_apis, v_cargo_dev_pl, v_genero_m, v_geracao_millennial, v_tempo_2a5, v_local_sp, '2022-01-15', 'CLT')
    RETURNING id_funcionario INTO v_func_1;
    
    INSERT INTO funcionario (nome_funcionario, email, email_corporativo, id_area_detalhe, id_cargo, id_genero_catgo, id_geracao_catgo, id_tempo_empresa_catgo, id_localidade, data_admissao, tipo_contratacao)
    VALUES ('Maria Santos', 'maria.santos@email.com', 'maria.santos@techcorp.com', v_area_web, v_cargo_dev_sr, v_genero_f, v_geracao_millennial, v_tempo_2a5, v_local_remoto, '2021-06-10', 'CLT')
    RETURNING id_funcionario INTO v_func_2;
    
    INSERT INTO funcionario (nome_funcionario, email, email_corporativo, id_area_detalhe, id_cargo, id_genero_catgo, id_geracao_catgo, id_tempo_empresa_catgo, id_localidade, data_admissao, tipo_contratacao)
    VALUES ('Pedro Oliveira', 'pedro.oliveira@email.com', 'pedro.oliveira@techcorp.com', v_area_apis, v_cargo_dev_jr, v_genero_m, v_geracao_z, v_tempo_1a2, v_local_sp, '2023-03-20', 'CLT')
    RETURNING id_funcionario INTO v_func_3;
    
    -- Buscar dimensões
    SELECT id_dimensao_avaliacao INTO v_dim_lideranca FROM dimensao_avaliacao WHERE nome_dimensao = 'Liderança';
    SELECT id_dimensao_avaliacao INTO v_dim_ambiente FROM dimensao_avaliacao WHERE nome_dimensao = 'Ambiente de Trabalho';
    SELECT id_dimensao_avaliacao INTO v_dim_reconhecimento FROM dimensao_avaliacao WHERE nome_dimensao = 'Reconhecimento';
    SELECT id_dimensao_avaliacao INTO v_dim_desenvolvimento FROM dimensao_avaliacao WHERE nome_dimensao = 'Desenvolvimento Profissional';
    SELECT id_dimensao_avaliacao INTO v_dim_remuneracao FROM dimensao_avaliacao WHERE nome_dimensao = 'Remuneração e Benefícios';
    SELECT id_dimensao_avaliacao INTO v_dim_equilibrio FROM dimensao_avaliacao WHERE nome_dimensao = 'Equilíbrio Trabalho-Vida';
    SELECT id_dimensao_avaliacao INTO v_dim_enps FROM dimensao_avaliacao WHERE nome_dimensao = 'Expectativa de Permanência (eNPS)';
    
    -- Avaliações e Respostas - Funcionário 1 (Satisfeito)
    INSERT INTO avaliacao (id_funcionario, data_avaliacao, periodo_avaliacao, comentario_geral)
    VALUES (v_func_1, '2024-12-01', '2024-S2', 'Muito satisfeito com o ambiente e oportunidades')
    RETURNING id_avaliacao INTO v_aval_1;
    
    INSERT INTO resposta_dimensao (id_avaliacao, id_dimensao_avaliacao, valor_resposta, comentario) VALUES
    (v_aval_1, v_dim_lideranca, 5, 'Excelente liderança'),
    (v_aval_1, v_dim_ambiente, 5, 'Ambiente colaborativo'),
    (v_aval_1, v_dim_reconhecimento, 4, 'Reconhecimento adequado'),
    (v_aval_1, v_dim_desenvolvimento, 5, 'Muitas oportunidades'),
    (v_aval_1, v_dim_remuneracao, 4, 'Salário justo'),
    (v_aval_1, v_dim_equilibrio, 5, 'Ótimo equilíbrio'),
    (v_aval_1, v_dim_enps, 9, 'Recomendaria fortemente');
    
    -- Avaliações e Respostas - Funcionário 2 (Muito Satisfeito)
    INSERT INTO avaliacao (id_funcionario, data_avaliacao, periodo_avaliacao, comentario_geral)
    VALUES (v_func_2, '2024-12-01', '2024-S2', 'Empresa excelente, ambiente incrível')
    RETURNING id_avaliacao INTO v_aval_2;
    
    INSERT INTO resposta_dimensao (id_avaliacao, id_dimensao_avaliacao, valor_resposta, comentario) VALUES
    (v_aval_2, v_dim_lideranca, 5, 'Liderança inspiradora'),
    (v_aval_2, v_dim_ambiente, 5, 'Melhor ambiente que já trabalhei'),
    (v_aval_2, v_dim_reconhecimento, 5, 'Sempre reconhecida'),
    (v_aval_2, v_dim_desenvolvimento, 5, 'Crescimento constante'),
    (v_aval_2, v_dim_remuneracao, 5, 'Remuneração excelente'),
    (v_aval_2, v_dim_equilibrio, 5, 'Trabalho remoto é perfeito'),
    (v_aval_2, v_dim_enps, 10, 'Já indiquei vários amigos');
    
    -- Avaliações e Respostas - Funcionário 3 (Neutro/Insatisfeito)
    INSERT INTO avaliacao (id_funcionario, data_avaliacao, periodo_avaliacao, comentario_geral)
    VALUES (v_func_3, '2024-12-01', '2024-S2', 'Algumas coisas poderiam melhorar')
    RETURNING id_avaliacao INTO v_aval_3;
    
    INSERT INTO resposta_dimensao (id_avaliacao, id_dimensao_avaliacao, valor_resposta, comentario) VALUES
    (v_aval_3, v_dim_lideranca, 3, 'Liderança poderia ser melhor'),
    (v_aval_3, v_dim_ambiente, 3, 'Ambiente ok'),
    (v_aval_3, v_dim_reconhecimento, 2, 'Não me sinto reconhecido'),
    (v_aval_3, v_dim_desenvolvimento, 3, 'Poucas oportunidades para júnior'),
    (v_aval_3, v_dim_remuneracao, 2, 'Salário abaixo do mercado'),
    (v_aval_3, v_dim_equilibrio, 4, 'Equilíbrio razoável'),
    (v_aval_3, v_dim_enps, 6, 'Talvez recomendaria');
END $$;
