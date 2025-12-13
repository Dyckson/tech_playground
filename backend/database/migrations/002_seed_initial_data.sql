-- 002_seed_initial_data.sql
-- Dados iniciais para o sistema

-- ===== EMPRESAS =====
INSERT INTO empresa (nome_empresa, cnpj) VALUES
('TechCorp Brasil', '12.345.678/0001-90'),
('InnovaSoft Ltda', '98.765.432/0001-10'),
('CloudServices XYZ', '11.222.333/0001-44')
ON CONFLICT (cnpj) DO NOTHING;

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

-- ===== HIERARQUIA - InnovaSoft Ltda =====
DO $$
DECLARE
    v_empresa_id UUID;
    v_diretoria_tech UUID;
    v_diretoria_product UUID;
    v_gerencia_eng UUID;
    v_gerencia_design UUID;
    v_coord_mobile UUID;
    v_coord_web UUID;
    v_coord_ux UUID;
BEGIN
    -- Empresa
    SELECT id_empresa INTO v_empresa_id FROM empresa WHERE nome_empresa = 'InnovaSoft Ltda';
    
    -- Diretorias
    INSERT INTO diretoria (id_empresa, nome_diretoria, sigla_diretoria) VALUES
    (v_empresa_id, 'Tecnologia', 'TECH') RETURNING id_diretoria INTO v_diretoria_tech;
    
    INSERT INTO diretoria (id_empresa, nome_diretoria, sigla_diretoria) VALUES
    (v_empresa_id, 'Produto', 'PROD') RETURNING id_diretoria INTO v_diretoria_product;
    
    -- Gerências
    INSERT INTO gerencia (id_diretoria, nome_gerencia, sigla_gerencia) VALUES
    (v_diretoria_tech, 'Engenharia de Software', 'ENG') RETURNING id_gerencia INTO v_gerencia_eng;
    
    INSERT INTO gerencia (id_diretoria, nome_gerencia, sigla_gerencia) VALUES
    (v_diretoria_product, 'Design e UX', 'DESIGN') RETURNING id_gerencia INTO v_gerencia_design;
    
    -- Coordenações
    INSERT INTO coordenacao (id_gerencia, nome_coordenacao) VALUES
    (v_gerencia_eng, 'Mobile Development') RETURNING id_coordenacao INTO v_coord_mobile;
    
    INSERT INTO coordenacao (id_gerencia, nome_coordenacao) VALUES
    (v_gerencia_eng, 'Web Development') RETURNING id_coordenacao INTO v_coord_web;
    
    INSERT INTO coordenacao (id_gerencia, nome_coordenacao) VALUES
    (v_gerencia_design, 'User Experience') RETURNING id_coordenacao INTO v_coord_ux;
    
    -- Áreas
    INSERT INTO area_detalhe (id_coordenacao, nome_area_detalhe) VALUES
    (v_coord_mobile, 'iOS'),
    (v_coord_mobile, 'Android'),
    (v_coord_web, 'Frontend'),
    (v_coord_web, 'Backend'),
    (v_coord_ux, 'UI Design'),
    (v_coord_ux, 'UX Research');
END $$;

-- ===== HIERARQUIA - CloudServices XYZ =====
DO $$
DECLARE
    v_empresa_id UUID;
    v_diretoria_ops UUID;
    v_gerencia_cloud UUID;
    v_gerencia_security UUID;
    v_coord_infra UUID;
    v_coord_sec UUID;
BEGIN
    -- Empresa
    SELECT id_empresa INTO v_empresa_id FROM empresa WHERE nome_empresa = 'CloudServices XYZ';
    
    -- Diretorias
    INSERT INTO diretoria (id_empresa, nome_diretoria, sigla_diretoria) VALUES
    (v_empresa_id, 'Operações', 'OPS') RETURNING id_diretoria INTO v_diretoria_ops;
    
    -- Gerências
    INSERT INTO gerencia (id_diretoria, nome_gerencia, sigla_gerencia) VALUES
    (v_diretoria_ops, 'Cloud Infrastructure', 'CLOUD') RETURNING id_gerencia INTO v_gerencia_cloud;
    
    INSERT INTO gerencia (id_diretoria, nome_gerencia, sigla_gerencia) VALUES
    (v_diretoria_ops, 'Security', 'SEC') RETURNING id_gerencia INTO v_gerencia_security;
    
    -- Coordenações
    INSERT INTO coordenacao (id_gerencia, nome_coordenacao) VALUES
    (v_gerencia_cloud, 'Infrastructure') RETURNING id_coordenacao INTO v_coord_infra;
    
    INSERT INTO coordenacao (id_gerencia, nome_coordenacao) VALUES
    (v_gerencia_security, 'Security Operations') RETURNING id_coordenacao INTO v_coord_sec;
    
    -- Áreas
    INSERT INTO area_detalhe (id_coordenacao, nome_area_detalhe) VALUES
    (v_coord_infra, 'AWS'),
    (v_coord_infra, 'Azure'),
    (v_coord_infra, 'GCP'),
    (v_coord_sec, 'Security Engineering'),
    (v_coord_sec, 'Compliance');
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
('Diretor', 'Diretoria')
ON CONFLICT (nome_cargo) DO NOTHING;

-- Gêneros
INSERT INTO genero_catgo (nome_genero) VALUES
('Masculino'),
('Feminino'),
('Não-binário'),
('Prefiro não informar')
ON CONFLICT (nome_genero) DO NOTHING;

-- Gerações
INSERT INTO geracao_catgo (nome_geracao, faixa_etaria) VALUES
('Baby Boomer', '1946-1964'),
('Geração X', '1965-1980'),
('Millennials', '1981-1996'),
('Geração Z', '1997-2012')
ON CONFLICT (nome_geracao) DO NOTHING;

-- Tempo de Empresa
INSERT INTO tempo_empresa_catgo (nome_tempo_empresa, meses_min, meses_max) VALUES
('Menos de 6 meses', 0, 5),
('6 meses a 1 ano', 6, 11),
('1 a 2 anos', 12, 23),
('2 a 5 anos', 24, 59),
('5 a 10 anos', 60, 119),
('Mais de 10 anos', 120, NULL)
ON CONFLICT (nome_tempo_empresa) DO NOTHING;

-- Localidades
INSERT INTO localidade (nome_localidade, cidade, estado, tipo) VALUES
('São Paulo - Matriz', 'São Paulo', 'SP', 'Escritório'),
('São Paulo - Filial Paulista', 'São Paulo', 'SP', 'Escritório'),
('Rio de Janeiro - Escritório', 'Rio de Janeiro', 'RJ', 'Escritório'),
('Belo Horizonte - Hub Tech', 'Belo Horizonte', 'MG', 'Escritório'),
('Remoto - Brasil', NULL, NULL, 'Remoto'),
('Remoto - Internacional', NULL, NULL, 'Remoto')
ON CONFLICT (nome_localidade) DO NOTHING;

-- Dimensões de Avaliação
INSERT INTO dimensao_avaliacao (nome_dimensao, descricao, tipo_escala, valor_min, valor_max, ordem_exibicao) VALUES
('Liderança', 'Avaliação da qualidade da liderança imediata', 'Likert', 1, 5, 1),
('Ambiente de Trabalho', 'Satisfação com o ambiente físico e cultura organizacional', 'Likert', 1, 5, 2),
('Reconhecimento', 'Percepção sobre reconhecimento e valorização do trabalho', 'Likert', 1, 5, 3),
('Desenvolvimento Profissional', 'Oportunidades de crescimento e aprendizado', 'Likert', 1, 5, 4),
('Remuneração e Benefícios', 'Satisfação com pacote de remuneração total', 'Likert', 1, 5, 5),
('Equilíbrio Trabalho-Vida', 'Percepção sobre work-life balance', 'Likert', 1, 5, 6),
('Expectativa de Permanência (eNPS)', 'Probabilidade de recomendar a empresa como lugar para trabalhar', 'NPS', 0, 10, 7)
ON CONFLICT (nome_dimensao) DO NOTHING;

-- ===== FUNCIONÁRIOS DE EXEMPLO =====
DO $$
DECLARE
    v_area_apis UUID;
    v_area_web UUID;
    v_area_mobile UUID;
    v_area_db UUID;
    v_area_cicd UUID;
    v_area_cloud UUID;
    v_cargo_dev_jr UUID;
    v_cargo_dev_pl UUID;
    v_cargo_dev_sr UUID;
    v_cargo_tech_lead UUID;
    v_cargo_devops UUID;
    v_cargo_arquiteto UUID;
    v_genero_m UUID;
    v_genero_f UUID;
    v_genero_nb UUID;
    v_geracao_z UUID;
    v_geracao_millennial UUID;
    v_geracao_x UUID;
    v_tempo_6m1a UUID;
    v_tempo_1a2 UUID;
    v_tempo_2a5 UUID;
    v_tempo_5a10 UUID;
    v_local_sp UUID;
    v_local_rj UUID;
    v_local_bh UUID;
    v_local_remoto UUID;
    v_func_1 UUID;
    v_func_2 UUID;
    v_func_3 UUID;
    v_func_4 UUID;
    v_func_5 UUID;
    v_func_6 UUID;
    v_func_7 UUID;
    v_func_8 UUID;
    v_func_9 UUID;
    v_func_10 UUID;
    v_aval_1 UUID;
    v_aval_2 UUID;
    v_aval_3 UUID;
    v_aval_4 UUID;
    v_aval_5 UUID;
    v_aval_6 UUID;
    v_aval_7 UUID;
    v_aval_8 UUID;
    v_aval_9 UUID;
    v_aval_10 UUID;
    v_dim_lideranca UUID;
    v_dim_ambiente UUID;
    v_dim_reconhecimento UUID;
    v_dim_desenvolvimento UUID;
    v_dim_remuneracao UUID;
    v_dim_equilibrio UUID;
    v_dim_enps UUID;
BEGIN
    -- Buscar IDs necessários - Áreas
    SELECT id_area_detalhe INTO v_area_apis FROM area_detalhe WHERE nome_area_detalhe = 'APIs e Microserviços';
    SELECT id_area_detalhe INTO v_area_web FROM area_detalhe WHERE nome_area_detalhe = 'Web Applications';
    SELECT id_area_detalhe INTO v_area_mobile FROM area_detalhe WHERE nome_area_detalhe = 'Mobile Apps';
    SELECT id_area_detalhe INTO v_area_db FROM area_detalhe WHERE nome_area_detalhe = 'Banco de Dados';
    SELECT id_area_detalhe INTO v_area_cicd FROM area_detalhe WHERE nome_area_detalhe = 'CI/CD';
    SELECT id_area_detalhe INTO v_area_cloud FROM area_detalhe WHERE nome_area_detalhe = 'Cloud Infrastructure';
    
    -- Buscar IDs - Cargos
    SELECT id_cargo INTO v_cargo_dev_jr FROM cargo WHERE nome_cargo = 'Desenvolvedor Júnior';
    SELECT id_cargo INTO v_cargo_dev_pl FROM cargo WHERE nome_cargo = 'Desenvolvedor Pleno';
    SELECT id_cargo INTO v_cargo_dev_sr FROM cargo WHERE nome_cargo = 'Desenvolvedor Sênior';
    SELECT id_cargo INTO v_cargo_tech_lead FROM cargo WHERE nome_cargo = 'Tech Lead';
    SELECT id_cargo INTO v_cargo_devops FROM cargo WHERE nome_cargo = 'DevOps Engineer';
    SELECT id_cargo INTO v_cargo_arquiteto FROM cargo WHERE nome_cargo = 'Arquiteto de Software';
    
    -- Buscar IDs - Gêneros
    SELECT id_genero_catgo INTO v_genero_m FROM genero_catgo WHERE nome_genero = 'Masculino';
    SELECT id_genero_catgo INTO v_genero_f FROM genero_catgo WHERE nome_genero = 'Feminino';
    SELECT id_genero_catgo INTO v_genero_nb FROM genero_catgo WHERE nome_genero = 'Não-binário';
    
    -- Buscar IDs - Gerações
    SELECT id_geracao_catgo INTO v_geracao_z FROM geracao_catgo WHERE nome_geracao = 'Geração Z';
    SELECT id_geracao_catgo INTO v_geracao_millennial FROM geracao_catgo WHERE nome_geracao = 'Millennials';
    SELECT id_geracao_catgo INTO v_geracao_x FROM geracao_catgo WHERE nome_geracao = 'Geração X';
    
    -- Buscar IDs - Tempo de Empresa
    SELECT id_tempo_empresa_catgo INTO v_tempo_6m1a FROM tempo_empresa_catgo WHERE nome_tempo_empresa = '6 meses a 1 ano';
    SELECT id_tempo_empresa_catgo INTO v_tempo_1a2 FROM tempo_empresa_catgo WHERE nome_tempo_empresa = '1 a 2 anos';
    SELECT id_tempo_empresa_catgo INTO v_tempo_2a5 FROM tempo_empresa_catgo WHERE nome_tempo_empresa = '2 a 5 anos';
    SELECT id_tempo_empresa_catgo INTO v_tempo_5a10 FROM tempo_empresa_catgo WHERE nome_tempo_empresa = '5 a 10 anos';
    
    -- Buscar IDs - Localidades
    SELECT id_localidade INTO v_local_sp FROM localidade WHERE nome_localidade = 'São Paulo - Matriz';
    SELECT id_localidade INTO v_local_rj FROM localidade WHERE nome_localidade = 'Rio de Janeiro - Escritório';
    SELECT id_localidade INTO v_local_bh FROM localidade WHERE nome_localidade = 'Belo Horizonte - Hub Tech';
    SELECT id_localidade INTO v_local_remoto FROM localidade WHERE nome_localidade = 'Remoto - Brasil';
    
    -- ===== FUNCIONÁRIOS TECHCORP =====
    
    -- 1. João Silva - Backend Pleno (Promotor - eNPS 9)
    INSERT INTO funcionario (nome_funcionario, email, email_corporativo, id_area_detalhe, id_cargo, id_genero_catgo, id_geracao_catgo, id_tempo_empresa_catgo, id_localidade, data_admissao, tipo_contratacao)
    VALUES ('João Silva', 'joao.silva@email.com', 'joao.silva@techcorp.com', v_area_apis, v_cargo_dev_pl, v_genero_m, v_geracao_millennial, v_tempo_2a5, v_local_sp, '2022-01-15', 'CLT')
    RETURNING id_funcionario INTO v_func_1;
    
    -- 2. Maria Santos - Frontend Sênior (Promotor - eNPS 10)
    INSERT INTO funcionario (nome_funcionario, email, email_corporativo, id_area_detalhe, id_cargo, id_genero_catgo, id_geracao_catgo, id_tempo_empresa_catgo, id_localidade, data_admissao, tipo_contratacao)
    VALUES ('Maria Santos', 'maria.santos@email.com', 'maria.santos@techcorp.com', v_area_web, v_cargo_dev_sr, v_genero_f, v_geracao_millennial, v_tempo_2a5, v_local_remoto, '2021-06-10', 'CLT')
    RETURNING id_funcionario INTO v_func_2;
    
    -- 3. Pedro Oliveira - Backend Júnior (Passivo - eNPS 6)
    INSERT INTO funcionario (nome_funcionario, email, email_corporativo, id_area_detalhe, id_cargo, id_genero_catgo, id_geracao_catgo, id_tempo_empresa_catgo, id_localidade, data_admissao, tipo_contratacao)
    VALUES ('Pedro Oliveira', 'pedro.oliveira@email.com', 'pedro.oliveira@techcorp.com', v_area_apis, v_cargo_dev_jr, v_genero_m, v_geracao_z, v_tempo_1a2, v_local_sp, '2023-03-20', 'CLT')
    RETURNING id_funcionario INTO v_func_3;
    
    -- 4. Ana Costa - Mobile Sênior (Promotor - eNPS 9)
    INSERT INTO funcionario (nome_funcionario, email, email_corporativo, id_area_detalhe, id_cargo, id_genero_catgo, id_geracao_catgo, id_tempo_empresa_catgo, id_localidade, data_admissao, tipo_contratacao)
    VALUES ('Ana Costa', 'ana.costa@email.com', 'ana.costa@techcorp.com', v_area_mobile, v_cargo_dev_sr, v_genero_f, v_geracao_millennial, v_tempo_5a10, v_local_rj, '2019-08-01', 'CLT')
    RETURNING id_funcionario INTO v_func_4;
    
    -- 5. Carlos Mendes - Tech Lead Backend (Promotor - eNPS 10)
    INSERT INTO funcionario (nome_funcionario, email, email_corporativo, id_area_detalhe, id_cargo, id_genero_catgo, id_geracao_catgo, id_tempo_empresa_catgo, id_localidade, data_admissao, tipo_contratacao)
    VALUES ('Carlos Mendes', 'carlos.mendes@email.com', 'carlos.mendes@techcorp.com', v_area_apis, v_cargo_tech_lead, v_genero_m, v_geracao_x, v_tempo_5a10, v_local_sp, '2018-03-10', 'CLT')
    RETURNING id_funcionario INTO v_func_5;
    
    -- 6. Juliana Ferreira - Frontend Pleno (Detrator - eNPS 4)
    INSERT INTO funcionario (nome_funcionario, email, email_corporativo, id_area_detalhe, id_cargo, id_genero_catgo, id_geracao_catgo, id_tempo_empresa_catgo, id_localidade, data_admissao, tipo_contratacao)
    VALUES ('Juliana Ferreira', 'juliana.ferreira@email.com', 'juliana.ferreira@techcorp.com', v_area_web, v_cargo_dev_pl, v_genero_f, v_geracao_z, v_tempo_1a2, v_local_remoto, '2023-05-20', 'CLT')
    RETURNING id_funcionario INTO v_func_6;
    
    -- 7. Rafael Almeida - DevOps Engineer (Promotor - eNPS 8)
    INSERT INTO funcionario (nome_funcionario, email, email_corporativo, id_area_detalhe, id_cargo, id_genero_catgo, id_geracao_catgo, id_tempo_empresa_catgo, id_localidade, data_admissao, tipo_contratacao)
    VALUES ('Rafael Almeida', 'rafael.almeida@email.com', 'rafael.almeida@techcorp.com', v_area_cicd, v_cargo_devops, v_genero_m, v_geracao_millennial, v_tempo_2a5, v_local_bh, '2022-09-15', 'CLT')
    RETURNING id_funcionario INTO v_func_7;
    
    -- 8. Beatriz Lima - Arquiteta de Software (Promotor - eNPS 9)
    INSERT INTO funcionario (nome_funcionario, email, email_corporativo, id_area_detalhe, id_cargo, id_genero_catgo, id_geracao_catgo, id_tempo_empresa_catgo, id_localidade, data_admissao, tipo_contratacao)
    VALUES ('Beatriz Lima', 'beatriz.lima@email.com', 'beatriz.lima@techcorp.com', v_area_cloud, v_cargo_arquiteto, v_genero_f, v_geracao_x, v_tempo_5a10, v_local_remoto, '2019-11-20', 'CLT')
    RETURNING id_funcionario INTO v_func_8;
    
    -- 9. Lucas Rocha - DBA Pleno (Passivo - eNPS 7)
    INSERT INTO funcionario (nome_funcionario, email, email_corporativo, id_area_detalhe, id_cargo, id_genero_catgo, id_geracao_catgo, id_tempo_empresa_catgo, id_localidade, data_admissao, tipo_contratacao)
    VALUES ('Lucas Rocha', 'lucas.rocha@email.com', 'lucas.rocha@techcorp.com', v_area_db, v_cargo_dev_pl, v_genero_m, v_geracao_millennial, v_tempo_2a5, v_local_sp, '2021-02-10', 'CLT')
    RETURNING id_funcionario INTO v_func_9;
    
    -- 10. Fernanda Souza - Mobile Júnior (Detrator - eNPS 5)
    INSERT INTO funcionario (nome_funcionario, email, email_corporativo, id_area_detalhe, id_cargo, id_genero_catgo, id_geracao_catgo, id_tempo_empresa_catgo, id_localidade, data_admissao, tipo_contratacao)
    VALUES ('Fernanda Souza', 'fernanda.souza@email.com', 'fernanda.souza@techcorp.com', v_area_mobile, v_cargo_dev_jr, v_genero_f, v_geracao_z, v_tempo_6m1a, v_local_rj, '2024-05-01', 'CLT')
    RETURNING id_funcionario INTO v_func_10;
    
    -- ===== BUSCAR DIMENSÕES =====
    SELECT id_dimensao_avaliacao INTO v_dim_lideranca FROM dimensao_avaliacao WHERE nome_dimensao = 'Liderança';
    SELECT id_dimensao_avaliacao INTO v_dim_ambiente FROM dimensao_avaliacao WHERE nome_dimensao = 'Ambiente de Trabalho';
    SELECT id_dimensao_avaliacao INTO v_dim_reconhecimento FROM dimensao_avaliacao WHERE nome_dimensao = 'Reconhecimento';
    SELECT id_dimensao_avaliacao INTO v_dim_desenvolvimento FROM dimensao_avaliacao WHERE nome_dimensao = 'Desenvolvimento Profissional';
    SELECT id_dimensao_avaliacao INTO v_dim_remuneracao FROM dimensao_avaliacao WHERE nome_dimensao = 'Remuneração e Benefícios';
    SELECT id_dimensao_avaliacao INTO v_dim_equilibrio FROM dimensao_avaliacao WHERE nome_dimensao = 'Equilíbrio Trabalho-Vida';
    SELECT id_dimensao_avaliacao INTO v_dim_enps FROM dimensao_avaliacao WHERE nome_dimensao = 'Expectativa de Permanência (eNPS)';
    
    -- ===== AVALIAÇÕES =====
    
    -- Funcionário 1: João Silva (Promotor - eNPS 9)
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
    
    -- Funcionário 2: Maria Santos (Promotor - eNPS 10)
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
    
    -- Funcionário 3: Pedro Oliveira (Passivo - eNPS 6)
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
    
    -- Funcionário 4: Ana Costa (Promotor - eNPS 9)
    INSERT INTO avaliacao (id_funcionario, data_avaliacao, periodo_avaliacao, comentario_geral)
    VALUES (v_func_4, '2024-12-01', '2024-S2', 'Empresa sólida, bom ambiente de trabalho')
    RETURNING id_avaliacao INTO v_aval_4;
    
    INSERT INTO resposta_dimensao (id_avaliacao, id_dimensao_avaliacao, valor_resposta, comentario) VALUES
    (v_aval_4, v_dim_lideranca, 5, 'Liderança presente e acessível'),
    (v_aval_4, v_dim_ambiente, 4, 'Ambiente profissional'),
    (v_aval_4, v_dim_reconhecimento, 5, 'Reconhecimento constante'),
    (v_aval_4, v_dim_desenvolvimento, 5, 'Muitas oportunidades de crescimento'),
    (v_aval_4, v_dim_remuneracao, 4, 'Remuneração competitiva'),
    (v_aval_4, v_dim_equilibrio, 5, 'Flexibilidade excelente'),
    (v_aval_4, v_dim_enps, 9, 'Certamente recomendaria');
    
    -- Funcionário 5: Carlos Mendes (Promotor - eNPS 10)
    INSERT INTO avaliacao (id_funcionario, data_avaliacao, periodo_avaliacao, comentario_geral)
    VALUES (v_func_5, '2024-12-01', '2024-S2', 'Melhor empresa que já trabalhei, excelente cultura')
    RETURNING id_avaliacao INTO v_aval_5;
    
    INSERT INTO resposta_dimensao (id_avaliacao, id_dimensao_avaliacao, valor_resposta, comentario) VALUES
    (v_aval_5, v_dim_lideranca, 5, 'Liderança exemplar'),
    (v_aval_5, v_dim_ambiente, 5, 'Cultura de inovação'),
    (v_aval_5, v_dim_reconhecimento, 5, 'Sempre valorizado'),
    (v_aval_5, v_dim_desenvolvimento, 5, 'Investimento em crescimento'),
    (v_aval_5, v_dim_remuneracao, 5, 'Pacote muito competitivo'),
    (v_aval_5, v_dim_equilibrio, 5, 'Equilíbrio perfeito'),
    (v_aval_5, v_dim_enps, 10, 'Já trouxe várias pessoas para cá');
    
    -- Funcionário 6: Juliana Ferreira (Detrator - eNPS 4)
    INSERT INTO avaliacao (id_funcionario, data_avaliacao, periodo_avaliacao, comentario_geral)
    VALUES (v_func_6, '2024-12-01', '2024-S2', 'Muita insatisfação com processos e reconhecimento')
    RETURNING id_avaliacao INTO v_aval_6;
    
    INSERT INTO resposta_dimensao (id_avaliacao, id_dimensao_avaliacao, valor_resposta, comentario) VALUES
    (v_aval_6, v_dim_lideranca, 2, 'Falta de direcionamento'),
    (v_aval_6, v_dim_ambiente, 2, 'Ambiente tóxico em alguns times'),
    (v_aval_6, v_dim_reconhecimento, 1, 'Não sinto que meu trabalho é valorizado'),
    (v_aval_6, v_dim_desenvolvimento, 2, 'Poucas oportunidades reais'),
    (v_aval_6, v_dim_remuneracao, 3, 'Salário abaixo do esperado'),
    (v_aval_6, v_dim_equilibrio, 3, 'Muita pressão e sobrecarga'),
    (v_aval_6, v_dim_enps, 4, 'Não recomendaria');
    
    -- Funcionário 7: Rafael Almeida (Promotor - eNPS 8)
    INSERT INTO avaliacao (id_funcionario, data_avaliacao, periodo_avaliacao, comentario_geral)
    VALUES (v_func_7, '2024-12-01', '2024-S2', 'Muito bom trabalhar aqui, infraestrutura top')
    RETURNING id_avaliacao INTO v_aval_7;
    
    INSERT INTO resposta_dimensao (id_avaliacao, id_dimensao_avaliacao, valor_resposta, comentario) VALUES
    (v_aval_7, v_dim_lideranca, 4, 'Boa liderança técnica'),
    (v_aval_7, v_dim_ambiente, 5, 'Ferramentas de ponta'),
    (v_aval_7, v_dim_reconhecimento, 4, 'Reconhecido pelo trabalho'),
    (v_aval_7, v_dim_desenvolvimento, 5, 'Sempre aprendendo coisas novas'),
    (v_aval_7, v_dim_remuneracao, 4, 'Salário justo'),
    (v_aval_7, v_dim_equilibrio, 4, 'Bom equilíbrio na maioria das vezes'),
    (v_aval_7, v_dim_enps, 8, 'Recomendaria com certeza');
    
    -- Funcionário 8: Beatriz Lima (Promotor - eNPS 9)
    INSERT INTO avaliacao (id_funcionario, data_avaliacao, periodo_avaliacao, comentario_geral)
    VALUES (v_func_8, '2024-12-01', '2024-S2', 'Excelente lugar para evoluir tecnicamente')
    RETURNING id_avaliacao INTO v_aval_8;
    
    INSERT INTO resposta_dimensao (id_avaliacao, id_dimensao_avaliacao, valor_resposta, comentario) VALUES
    (v_aval_8, v_dim_lideranca, 5, 'Liderança técnica forte'),
    (v_aval_8, v_dim_ambiente, 5, 'Ambiente desafiador'),
    (v_aval_8, v_dim_reconhecimento, 5, 'Reconhecimento adequado'),
    (v_aval_8, v_dim_desenvolvimento, 5, 'Projetos complexos e interessantes'),
    (v_aval_8, v_dim_remuneracao, 4, 'Remuneração boa'),
    (v_aval_8, v_dim_equilibrio, 5, 'Trabalho remoto funciona muito bem'),
    (v_aval_8, v_dim_enps, 9, 'Recomendaria fortemente');
    
    -- Funcionário 9: Lucas Rocha (Passivo - eNPS 7)
    INSERT INTO avaliacao (id_funcionario, data_avaliacao, periodo_avaliacao, comentario_geral)
    VALUES (v_func_9, '2024-12-01', '2024-S2', 'Empresa boa, mas alguns pontos a melhorar')
    RETURNING id_avaliacao INTO v_aval_9;
    
    INSERT INTO resposta_dimensao (id_avaliacao, id_dimensao_avaliacao, valor_resposta, comentario) VALUES
    (v_aval_9, v_dim_lideranca, 4, 'Liderança razoável'),
    (v_aval_9, v_dim_ambiente, 4, 'Ambiente ok'),
    (v_aval_9, v_dim_reconhecimento, 3, 'Poderia ter mais reconhecimento'),
    (v_aval_9, v_dim_desenvolvimento, 4, 'Algumas oportunidades'),
    (v_aval_9, v_dim_remuneracao, 3, 'Salário mediano'),
    (v_aval_9, v_dim_equilibrio, 4, 'Equilíbrio satisfatório'),
    (v_aval_9, v_dim_enps, 7, 'Talvez recomendaria');
    
    -- Funcionário 10: Fernanda Souza (Detrator - eNPS 5)
    INSERT INTO avaliacao (id_funcionario, data_avaliacao, periodo_avaliacao, comentario_geral)
    VALUES (v_func_10, '2024-12-01', '2024-S2', 'Experiência inicial não foi das melhores')
    RETURNING id_avaliacao INTO v_aval_10;
    
    INSERT INTO resposta_dimensao (id_avaliacao, id_dimensao_avaliacao, valor_resposta, comentario) VALUES
    (v_aval_10, v_dim_lideranca, 3, 'Falta mentoria'),
    (v_aval_10, v_dim_ambiente, 3, 'Ambiente competitivo demais'),
    (v_aval_10, v_dim_reconhecimento, 2, 'Pouco reconhecimento para júnior'),
    (v_aval_10, v_dim_desenvolvimento, 3, 'Treinamento insuficiente'),
    (v_aval_10, v_dim_remuneracao, 2, 'Salário baixo para a região'),
    (v_aval_10, v_dim_equilibrio, 3, 'Muita cobrança'),
    (v_aval_10, v_dim_enps, 5, 'Provavelmente não recomendaria');
END $$;

-- ===== FUNCIONÁRIOS INNOVASOFT LTDA =====
DO $$
DECLARE
    v_area_ios UUID;
    v_area_android UUID;
    v_area_frontend UUID;
    v_area_backend UUID;
    v_area_ui UUID;
    v_cargo_dev_jr UUID;
    v_cargo_dev_pl UUID;
    v_cargo_dev_sr UUID;
    v_genero_m UUID;
    v_genero_f UUID;
    v_genero_nb UUID;
    v_geracao_z UUID;
    v_geracao_millennial UUID;
    v_tempo_6m1a UUID;
    v_tempo_1a2 UUID;
    v_tempo_2a5 UUID;
    v_local_sp UUID;
    v_local_remoto UUID;
    v_func_1 UUID;
    v_func_2 UUID;
    v_func_3 UUID;
    v_func_4 UUID;
    v_func_5 UUID;
    v_aval_1 UUID;
    v_aval_2 UUID;
    v_aval_3 UUID;
    v_aval_4 UUID;
    v_aval_5 UUID;
    v_dim_lideranca UUID;
    v_dim_ambiente UUID;
    v_dim_reconhecimento UUID;
    v_dim_desenvolvimento UUID;
    v_dim_remuneracao UUID;
    v_dim_equilibrio UUID;
    v_dim_enps UUID;
BEGIN
    -- Buscar áreas da InnovaSoft
    SELECT id_area_detalhe INTO v_area_ios FROM area_detalhe WHERE nome_area_detalhe = 'iOS';
    SELECT id_area_detalhe INTO v_area_android FROM area_detalhe WHERE nome_area_detalhe = 'Android';
    SELECT id_area_detalhe INTO v_area_frontend FROM area_detalhe WHERE nome_area_detalhe = 'Frontend';
    SELECT id_area_detalhe INTO v_area_backend FROM area_detalhe WHERE nome_area_detalhe = 'Backend';
    SELECT id_area_detalhe INTO v_area_ui FROM area_detalhe WHERE nome_area_detalhe = 'UI Design';
    
    -- Buscar lookups
    SELECT id_cargo INTO v_cargo_dev_jr FROM cargo WHERE nome_cargo = 'Desenvolvedor Júnior';
    SELECT id_cargo INTO v_cargo_dev_pl FROM cargo WHERE nome_cargo = 'Desenvolvedor Pleno';
    SELECT id_cargo INTO v_cargo_dev_sr FROM cargo WHERE nome_cargo = 'Desenvolvedor Sênior';
    SELECT id_genero_catgo INTO v_genero_m FROM genero_catgo WHERE nome_genero = 'Masculino';
    SELECT id_genero_catgo INTO v_genero_f FROM genero_catgo WHERE nome_genero = 'Feminino';
    SELECT id_genero_catgo INTO v_genero_nb FROM genero_catgo WHERE nome_genero = 'Não-binário';
    SELECT id_geracao_catgo INTO v_geracao_z FROM geracao_catgo WHERE nome_geracao = 'Geração Z';
    SELECT id_geracao_catgo INTO v_geracao_millennial FROM geracao_catgo WHERE nome_geracao = 'Millennials';
    SELECT id_tempo_empresa_catgo INTO v_tempo_6m1a FROM tempo_empresa_catgo WHERE nome_tempo_empresa = '6 meses a 1 ano';
    SELECT id_tempo_empresa_catgo INTO v_tempo_1a2 FROM tempo_empresa_catgo WHERE nome_tempo_empresa = '1 a 2 anos';
    SELECT id_tempo_empresa_catgo INTO v_tempo_2a5 FROM tempo_empresa_catgo WHERE nome_tempo_empresa = '2 a 5 anos';
    SELECT id_localidade INTO v_local_sp FROM localidade WHERE nome_localidade = 'São Paulo - Matriz';
    SELECT id_localidade INTO v_local_remoto FROM localidade WHERE nome_localidade = 'Remoto - Brasil';
    
    -- Funcionários InnovaSoft
    INSERT INTO funcionario (nome_funcionario, email, email_corporativo, id_area_detalhe, id_cargo, id_genero_catgo, id_geracao_catgo, id_tempo_empresa_catgo, id_localidade, data_admissao, tipo_contratacao)
    VALUES ('Thiago Martins', 'thiago.martins@email.com', 'thiago.martins@innovasoft.com', v_area_ios, v_cargo_dev_sr, v_genero_m, v_geracao_millennial, v_tempo_2a5, v_local_sp, '2022-03-10', 'CLT')
    RETURNING id_funcionario INTO v_func_1;
    
    INSERT INTO funcionario (nome_funcionario, email, email_corporativo, id_area_detalhe, id_cargo, id_genero_catgo, id_geracao_catgo, id_tempo_empresa_catgo, id_localidade, data_admissao, tipo_contratacao)
    VALUES ('Camila Souza', 'camila.souza@email.com', 'camila.souza@innovasoft.com', v_area_android, v_cargo_dev_pl, v_genero_f, v_geracao_millennial, v_tempo_1a2, v_local_remoto, '2023-06-15', 'CLT')
    RETURNING id_funcionario INTO v_func_2;
    
    INSERT INTO funcionario (nome_funcionario, email, email_corporativo, id_area_detalhe, id_cargo, id_genero_catgo, id_geracao_catgo, id_tempo_empresa_catgo, id_localidade, data_admissao, tipo_contratacao)
    VALUES ('Alex Ribeiro', 'alex.ribeiro@email.com', 'alex.ribeiro@innovasoft.com', v_area_frontend, v_cargo_dev_pl, v_genero_nb, v_geracao_z, v_tempo_1a2, v_local_remoto, '2023-04-20', 'PJ')
    RETURNING id_funcionario INTO v_func_3;
    
    INSERT INTO funcionario (nome_funcionario, email, email_corporativo, id_area_detalhe, id_cargo, id_genero_catgo, id_geracao_catgo, id_tempo_empresa_catgo, id_localidade, data_admissao, tipo_contratacao)
    VALUES ('Gabriela Nunes', 'gabriela.nunes@email.com', 'gabriela.nunes@innovasoft.com', v_area_backend, v_cargo_dev_sr, v_genero_f, v_geracao_millennial, v_tempo_2a5, v_local_sp, '2021-09-01', 'CLT')
    RETURNING id_funcionario INTO v_func_4;
    
    INSERT INTO funcionario (nome_funcionario, email, email_corporativo, id_area_detalhe, id_cargo, id_genero_catgo, id_geracao_catgo, id_tempo_empresa_catgo, id_localidade, data_admissao, tipo_contratacao)
    VALUES ('Leonardo Castro', 'leonardo.castro@email.com', 'leonardo.castro@innovasoft.com', v_area_ui, v_cargo_dev_jr, v_genero_m, v_geracao_z, v_tempo_6m1a, v_local_sp, '2024-06-01', 'CLT')
    RETURNING id_funcionario INTO v_func_5;
    
    -- Buscar dimensões
    SELECT id_dimensao_avaliacao INTO v_dim_lideranca FROM dimensao_avaliacao WHERE nome_dimensao = 'Liderança';
    SELECT id_dimensao_avaliacao INTO v_dim_ambiente FROM dimensao_avaliacao WHERE nome_dimensao = 'Ambiente de Trabalho';
    SELECT id_dimensao_avaliacao INTO v_dim_reconhecimento FROM dimensao_avaliacao WHERE nome_dimensao = 'Reconhecimento';
    SELECT id_dimensao_avaliacao INTO v_dim_desenvolvimento FROM dimensao_avaliacao WHERE nome_dimensao = 'Desenvolvimento Profissional';
    SELECT id_dimensao_avaliacao INTO v_dim_remuneracao FROM dimensao_avaliacao WHERE nome_dimensao = 'Remuneração e Benefícios';
    SELECT id_dimensao_avaliacao INTO v_dim_equilibrio FROM dimensao_avaliacao WHERE nome_dimensao = 'Equilíbrio Trabalho-Vida';
    SELECT id_dimensao_avaliacao INTO v_dim_enps FROM dimensao_avaliacao WHERE nome_dimensao = 'Expectativa de Permanência (eNPS)';
    
    -- Avaliações InnovaSoft
    -- Func 1: Thiago (Promotor - eNPS 8)
    INSERT INTO avaliacao (id_funcionario, data_avaliacao, periodo_avaliacao, comentario_geral)
    VALUES (v_func_1, '2024-12-01', '2024-S2', 'Empresa inovadora, ambiente criativo')
    RETURNING id_avaliacao INTO v_aval_1;
    
    INSERT INTO resposta_dimensao (id_avaliacao, id_dimensao_avaliacao, valor_resposta, comentario) VALUES
    (v_aval_1, v_dim_lideranca, 4, 'Liderança presente'),
    (v_aval_1, v_dim_ambiente, 5, 'Ambiente descontraído'),
    (v_aval_1, v_dim_reconhecimento, 4, 'Bom reconhecimento'),
    (v_aval_1, v_dim_desenvolvimento, 5, 'Muita autonomia'),
    (v_aval_1, v_dim_remuneracao, 4, 'Salário competitivo'),
    (v_aval_1, v_dim_equilibrio, 5, 'Flexibilidade excelente'),
    (v_aval_1, v_dim_enps, 8, 'Recomendaria');
    
    -- Func 2: Camila (Promotor - eNPS 9)
    INSERT INTO avaliacao (id_funcionario, data_avaliacao, periodo_avaliacao, comentario_geral)
    VALUES (v_func_2, '2024-12-01', '2024-S2', 'Adoro trabalhar aqui, time incrível')
    RETURNING id_avaliacao INTO v_aval_2;
    
    INSERT INTO resposta_dimensao (id_avaliacao, id_dimensao_avaliacao, valor_resposta, comentario) VALUES
    (v_aval_2, v_dim_lideranca, 5, 'Liderança inspiradora'),
    (v_aval_2, v_dim_ambiente, 5, 'Melhor time'),
    (v_aval_2, v_dim_reconhecimento, 5, 'Sempre reconhecida'),
    (v_aval_2, v_dim_desenvolvimento, 4, 'Boas oportunidades'),
    (v_aval_2, v_dim_remuneracao, 4, 'Salário justo'),
    (v_aval_2, v_dim_equilibrio, 5, 'Remoto é perfeito'),
    (v_aval_2, v_dim_enps, 9, 'Recomendo muito');
    
    -- Func 3: Alex (Passivo - eNPS 7)
    INSERT INTO avaliacao (id_funcionario, data_avaliacao, periodo_avaliacao, comentario_geral)
    VALUES (v_func_3, '2024-12-01', '2024-S2', 'Boa empresa, alguns pontos a melhorar')
    RETURNING id_avaliacao INTO v_aval_3;
    
    INSERT INTO resposta_dimensao (id_avaliacao, id_dimensao_avaliacao, valor_resposta, comentario) VALUES
    (v_aval_3, v_dim_lideranca, 4, 'Liderança ok'),
    (v_aval_3, v_dim_ambiente, 4, 'Ambiente bom'),
    (v_aval_3, v_dim_reconhecimento, 3, 'Poderia melhorar'),
    (v_aval_3, v_dim_desenvolvimento, 4, 'Algumas oportunidades'),
    (v_aval_3, v_dim_remuneracao, 3, 'PJ poderia ser melhor'),
    (v_aval_3, v_dim_equilibrio, 5, 'Flexibilidade total'),
    (v_aval_3, v_dim_enps, 7, 'Provavelmente recomendaria');
    
    -- Func 4: Gabriela (Promotor - eNPS 8)
    INSERT INTO avaliacao (id_funcionario, data_avaliacao, periodo_avaliacao, comentario_geral)
    VALUES (v_func_4, '2024-12-01', '2024-S2', 'Empresa sólida, bom crescimento')
    RETURNING id_avaliacao INTO v_aval_4;
    
    INSERT INTO resposta_dimensao (id_avaliacao, id_dimensao_avaliacao, valor_resposta, comentario) VALUES
    (v_aval_4, v_dim_lideranca, 5, 'Liderança técnica forte'),
    (v_aval_4, v_dim_ambiente, 4, 'Ambiente profissional'),
    (v_aval_4, v_dim_reconhecimento, 4, 'Reconhecimento adequado'),
    (v_aval_4, v_dim_desenvolvimento, 5, 'Cresci muito aqui'),
    (v_aval_4, v_dim_remuneracao, 4, 'Salário bom'),
    (v_aval_4, v_dim_equilibrio, 4, 'Equilíbrio satisfatório'),
    (v_aval_4, v_dim_enps, 8, 'Recomendaria');
    
    -- Func 5: Leonardo (Detrator - eNPS 6)
    INSERT INTO avaliacao (id_funcionario, data_avaliacao, periodo_avaliacao, comentario_geral)
    VALUES (v_func_5, '2024-12-01', '2024-S2', 'Início complicado, falta mentoria')
    RETURNING id_avaliacao INTO v_aval_5;
    
    INSERT INTO resposta_dimensao (id_avaliacao, id_dimensao_avaliacao, valor_resposta, comentario) VALUES
    (v_aval_5, v_dim_lideranca, 3, 'Pouca orientação'),
    (v_aval_5, v_dim_ambiente, 3, 'Ambiente acelerado demais'),
    (v_aval_5, v_dim_reconhecimento, 3, 'Reconhecimento básico'),
    (v_aval_5, v_dim_desenvolvimento, 3, 'Falta estrutura de onboarding'),
    (v_aval_5, v_dim_remuneracao, 2, 'Salário júnior baixo'),
    (v_aval_5, v_dim_equilibrio, 4, 'Flexibilidade boa'),
    (v_aval_5, v_dim_enps, 6, 'Incerto se recomendaria');
END $$;

-- ===== FUNCIONÁRIOS CLOUDSERVICES XYZ =====
DO $$
DECLARE
    v_area_aws UUID;
    v_area_azure UUID;
    v_area_gcp UUID;
    v_area_sec_eng UUID;
    v_cargo_devops UUID;
    v_cargo_dev_sr UUID;
    v_cargo_arquiteto UUID;
    v_genero_m UUID;
    v_genero_f UUID;
    v_geracao_millennial UUID;
    v_geracao_x UUID;
    v_tempo_2a5 UUID;
    v_tempo_5a10 UUID;
    v_local_remoto UUID;
    v_local_intl UUID;
    v_func_1 UUID;
    v_func_2 UUID;
    v_func_3 UUID;
    v_func_4 UUID;
    v_aval_1 UUID;
    v_aval_2 UUID;
    v_aval_3 UUID;
    v_aval_4 UUID;
    v_dim_lideranca UUID;
    v_dim_ambiente UUID;
    v_dim_reconhecimento UUID;
    v_dim_desenvolvimento UUID;
    v_dim_remuneracao UUID;
    v_dim_equilibrio UUID;
    v_dim_enps UUID;
BEGIN
    -- Buscar áreas da CloudServices
    SELECT id_area_detalhe INTO v_area_aws FROM area_detalhe WHERE nome_area_detalhe = 'AWS';
    SELECT id_area_detalhe INTO v_area_azure FROM area_detalhe WHERE nome_area_detalhe = 'Azure';
    SELECT id_area_detalhe INTO v_area_gcp FROM area_detalhe WHERE nome_area_detalhe = 'GCP';
    SELECT id_area_detalhe INTO v_area_sec_eng FROM area_detalhe WHERE nome_area_detalhe = 'Security Engineering';
    
    -- Buscar lookups
    SELECT id_cargo INTO v_cargo_devops FROM cargo WHERE nome_cargo = 'DevOps Engineer';
    SELECT id_cargo INTO v_cargo_dev_sr FROM cargo WHERE nome_cargo = 'Desenvolvedor Sênior';
    SELECT id_cargo INTO v_cargo_arquiteto FROM cargo WHERE nome_cargo = 'Arquiteto de Software';
    SELECT id_genero_catgo INTO v_genero_m FROM genero_catgo WHERE nome_genero = 'Masculino';
    SELECT id_genero_catgo INTO v_genero_f FROM genero_catgo WHERE nome_genero = 'Feminino';
    SELECT id_geracao_catgo INTO v_geracao_millennial FROM geracao_catgo WHERE nome_geracao = 'Millennials';
    SELECT id_geracao_catgo INTO v_geracao_x FROM geracao_catgo WHERE nome_geracao = 'Geração X';
    SELECT id_tempo_empresa_catgo INTO v_tempo_2a5 FROM tempo_empresa_catgo WHERE nome_tempo_empresa = '2 a 5 anos';
    SELECT id_tempo_empresa_catgo INTO v_tempo_5a10 FROM tempo_empresa_catgo WHERE nome_tempo_empresa = '5 a 10 anos';
    SELECT id_localidade INTO v_local_remoto FROM localidade WHERE nome_localidade = 'Remoto - Brasil';
    SELECT id_localidade INTO v_local_intl FROM localidade WHERE nome_localidade = 'Remoto - Internacional';
    
    -- Funcionários CloudServices
    INSERT INTO funcionario (nome_funcionario, email, email_corporativo, id_area_detalhe, id_cargo, id_genero_catgo, id_geracao_catgo, id_tempo_empresa_catgo, id_localidade, data_admissao, tipo_contratacao)
    VALUES ('Ricardo Santos', 'ricardo.santos@email.com', 'ricardo.santos@cloudservices.com', v_area_aws, v_cargo_arquiteto, v_genero_m, v_geracao_x, v_tempo_5a10, v_local_remoto, '2019-01-15', 'CLT')
    RETURNING id_funcionario INTO v_func_1;
    
    INSERT INTO funcionario (nome_funcionario, email, email_corporativo, id_area_detalhe, id_cargo, id_genero_catgo, id_geracao_catgo, id_tempo_empresa_catgo, id_localidade, data_admissao, tipo_contratacao)
    VALUES ('Patricia Lima', 'patricia.lima@email.com', 'patricia.lima@cloudservices.com', v_area_azure, v_cargo_devops, v_genero_f, v_geracao_millennial, v_tempo_2a5, v_local_intl, '2022-04-10', 'PJ')
    RETURNING id_funcionario INTO v_func_2;
    
    INSERT INTO funcionario (nome_funcionario, email, email_corporativo, id_area_detalhe, id_cargo, id_genero_catgo, id_geracao_catgo, id_tempo_empresa_catgo, id_localidade, data_admissao, tipo_contratacao)
    VALUES ('Rodrigo Fernandes', 'rodrigo.fernandes@email.com', 'rodrigo.fernandes@cloudservices.com', v_area_gcp, v_cargo_devops, v_genero_m, v_geracao_millennial, v_tempo_2a5, v_local_remoto, '2021-11-20', 'CLT')
    RETURNING id_funcionario INTO v_func_3;
    
    INSERT INTO funcionario (nome_funcionario, email, email_corporativo, id_area_detalhe, id_cargo, id_genero_catgo, id_geracao_catgo, id_tempo_empresa_catgo, id_localidade, data_admissao, tipo_contratacao)
    VALUES ('Vanessa Cardoso', 'vanessa.cardoso@email.com', 'vanessa.cardoso@cloudservices.com', v_area_sec_eng, v_cargo_dev_sr, v_genero_f, v_geracao_x, v_tempo_5a10, v_local_remoto, '2018-07-05', 'CLT')
    RETURNING id_funcionario INTO v_func_4;
    
    -- Buscar dimensões
    SELECT id_dimensao_avaliacao INTO v_dim_lideranca FROM dimensao_avaliacao WHERE nome_dimensao = 'Liderança';
    SELECT id_dimensao_avaliacao INTO v_dim_ambiente FROM dimensao_avaliacao WHERE nome_dimensao = 'Ambiente de Trabalho';
    SELECT id_dimensao_avaliacao INTO v_dim_reconhecimento FROM dimensao_avaliacao WHERE nome_dimensao = 'Reconhecimento';
    SELECT id_dimensao_avaliacao INTO v_dim_desenvolvimento FROM dimensao_avaliacao WHERE nome_dimensao = 'Desenvolvimento Profissional';
    SELECT id_dimensao_avaliacao INTO v_dim_remuneracao FROM dimensao_avaliacao WHERE nome_dimensao = 'Remuneração e Benefícios';
    SELECT id_dimensao_avaliacao INTO v_dim_equilibrio FROM dimensao_avaliacao WHERE nome_dimensao = 'Equilíbrio Trabalho-Vida';
    SELECT id_dimensao_avaliacao INTO v_dim_enps FROM dimensao_avaliacao WHERE nome_dimensao = 'Expectativa de Permanência (eNPS)';
    
    -- Avaliações CloudServices
    -- Func 1: Ricardo (Promotor - eNPS 9)
    INSERT INTO avaliacao (id_funcionario, data_avaliacao, periodo_avaliacao, comentario_geral)
    VALUES (v_func_1, '2024-12-01', '2024-S2', 'Excelente empresa, infraestrutura de ponta')
    RETURNING id_avaliacao INTO v_aval_1;
    
    INSERT INTO resposta_dimensao (id_avaliacao, id_dimensao_avaliacao, valor_resposta, comentario) VALUES
    (v_aval_1, v_dim_lideranca, 5, 'Liderança técnica forte'),
    (v_aval_1, v_dim_ambiente, 5, 'Tecnologia de ponta'),
    (v_aval_1, v_dim_reconhecimento, 5, 'Muito valorizado'),
    (v_aval_1, v_dim_desenvolvimento, 5, 'Sempre evoluindo'),
    (v_aval_1, v_dim_remuneracao, 5, 'Remuneração excelente'),
    (v_aval_1, v_dim_equilibrio, 5, 'Total flexibilidade'),
    (v_aval_1, v_dim_enps, 9, 'Recomendo fortemente');
    
    -- Func 2: Patricia (Promotor - eNPS 10)
    INSERT INTO avaliacao (id_funcionario, data_avaliacao, periodo_avaliacao, comentario_geral)
    VALUES (v_func_2, '2024-12-01', '2024-S2', 'Melhor empresa que já trabalhei')
    RETURNING id_avaliacao INTO v_aval_2;
    
    INSERT INTO resposta_dimensao (id_avaliacao, id_dimensao_avaliacao, valor_resposta, comentario) VALUES
    (v_aval_2, v_dim_lideranca, 5, 'Liderança exemplar'),
    (v_aval_2, v_dim_ambiente, 5, 'Ambiente global incrível'),
    (v_aval_2, v_dim_reconhecimento, 5, 'Sempre reconhecida'),
    (v_aval_2, v_dim_desenvolvimento, 5, 'Oportunidades globais'),
    (v_aval_2, v_dim_remuneracao, 5, 'Salário internacional'),
    (v_aval_2, v_dim_equilibrio, 5, 'Trabalho de qualquer lugar'),
    (v_aval_2, v_dim_enps, 10, 'Já indiquei muitos amigos');
    
    -- Func 3: Rodrigo (Promotor - eNPS 8)
    INSERT INTO avaliacao (id_funcionario, data_avaliacao, periodo_avaliacao, comentario_geral)
    VALUES (v_func_3, '2024-12-01', '2024-S2', 'Muito bom, desafios técnicos interessantes')
    RETURNING id_avaliacao INTO v_aval_3;
    
    INSERT INTO resposta_dimensao (id_avaliacao, id_dimensao_avaliacao, valor_resposta, comentario) VALUES
    (v_aval_3, v_dim_lideranca, 4, 'Boa liderança'),
    (v_aval_3, v_dim_ambiente, 5, 'Ambiente técnico forte'),
    (v_aval_3, v_dim_reconhecimento, 4, 'Reconhecimento adequado'),
    (v_aval_3, v_dim_desenvolvimento, 5, 'Muitos desafios'),
    (v_aval_3, v_dim_remuneracao, 4, 'Salário justo'),
    (v_aval_3, v_dim_equilibrio, 5, 'Flexibilidade total'),
    (v_aval_3, v_dim_enps, 8, 'Recomendaria');
    
    -- Func 4: Vanessa (Promotor - eNPS 9)
    INSERT INTO avaliacao (id_funcionario, data_avaliacao, periodo_avaliacao, comentario_geral)
    VALUES (v_func_4, '2024-12-01', '2024-S2', 'Empresa de referência em cloud')
    RETURNING id_avaliacao INTO v_aval_4;
    
    INSERT INTO resposta_dimensao (id_avaliacao, id_dimensao_avaliacao, valor_resposta, comentario) VALUES
    (v_aval_4, v_dim_lideranca, 5, 'Liderança forte'),
    (v_aval_4, v_dim_ambiente, 5, 'Cultura de segurança'),
    (v_aval_4, v_dim_reconhecimento, 5, 'Muito valorizada'),
    (v_aval_4, v_dim_desenvolvimento, 5, 'Crescimento constante'),
    (v_aval_4, v_dim_remuneracao, 5, 'Remuneração top'),
    (v_aval_4, v_dim_equilibrio, 4, 'Bom equilíbrio'),
    (v_aval_4, v_dim_enps, 9, 'Recomendo muito');
END $$;
