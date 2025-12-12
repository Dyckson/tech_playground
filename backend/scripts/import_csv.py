#!/usr/bin/env python3
"""
Script para importar dados do CSV de funcionários para o banco de dados.
Cria empresa, hierarquias, lookups e funcionários com avaliações completas.
"""
import sys
import csv
import os
import psycopg2
from uuid import uuid4
from datetime import datetime
from collections import defaultdict

# Mapeamento dos campos do CSV para o schema
FIELD_MAPPING = {
    'nome': 'nome',
    'email': 'email',
    'email_corporativo': 'email_corporativo',
    'area': 'area',
    'cargo': 'cargo',
    'funcao': 'funcao',
    'localidade': 'localidade',
    'tempo_de_empresa': 'tempo_empresa',
    'genero': 'genero',
    'geracao': 'geracao',
    'n0_empresa': 'empresa',
    'n1_diretoria': 'diretoria',
    'n2_gerencia': 'gerencia',
    'n3_coordenacao': 'coordenacao',
    'n4_area': 'area_detalhe',
    'Data da Resposta': 'data_resposta'
}

# Dimensões de avaliação (colunas do CSV -> nome no banco)
# Usamos os nomes do CSV como estão para criar as dimensões
DIMENSOES = [
    ('Interesse no Cargo', 'Interesse no Cargo'),
    ('Contribuição', 'Contribuição'),
    ('Aprendizado e Desenvolvimento', 'Aprendizado e Desenvolvimento'),
    ('Feedback', 'Feedback'),
    ('Interação com Gestor', 'Interação com Gestor'),
    ('Clareza sobre Possibilidades de Carreira', 'Clareza sobre Possibilidades de Carreira'),
    ('Expectativa de Permanência', 'Expectativa de Permanência')
]

def get_db_connection():
    """Estabelece conexão com o banco de dados."""
    return psycopg2.connect(
        host=os.getenv('DB_HOST', 'db'),
        port=os.getenv('DB_PORT', '5432'),
        database=os.getenv('DB_NAME', 'tech_db'),
        user=os.getenv('DB_USER', 'tech_user'),
        password=os.getenv('DB_PASSWORD', 'tech_password')
    )

def normalize_text(text):
    """Normaliza texto para comparação (lowercase, strip)."""
    return text.lower().strip() if text else ''

def get_or_create_lookup(cursor, table, field, value, cache):
    """Busca ou cria entrada em tabela de lookup."""
    cache_key = (table, normalize_text(value))
    
    if cache_key in cache:
        return cache[cache_key]
    
    normalized = normalize_text(value)
    
    # Determinar nome da coluna ID baseado no nome da tabela
    id_col = f'id_{table}' if not table.endswith('_catgo') else f'id_{table}'
    
    # Buscar existente
    cursor.execute(f"SELECT {id_col} FROM {table} WHERE LOWER(TRIM({field})) = %s", (normalized,))
    result = cursor.fetchone()
    
    if result:
        cache[cache_key] = result[0]
        return result[0]
    
    # Criar novo
    new_id = str(uuid4())
    cursor.execute(f"INSERT INTO {table} ({id_col}, {field}) VALUES (%s, %s) RETURNING {id_col}", (new_id, value))
    cache[cache_key] = new_id
    return new_id

def get_or_create_empresa(cursor, nome_empresa, cache):
    """Busca ou cria empresa."""
    normalized = normalize_text(nome_empresa)
    
    if normalized in cache:
        return cache[normalized]
    
    cursor.execute("SELECT id_empresa FROM empresa WHERE LOWER(TRIM(nome_empresa)) = %s", (normalized,))
    result = cursor.fetchone()
    
    if result:
        cache[normalized] = result[0]
        return result[0]
    
    # Criar nova empresa
    empresa_id = str(uuid4())
    cursor.execute(
        "INSERT INTO empresa (id_empresa, nome_empresa, ativo) VALUES (%s, %s, true) RETURNING id_empresa",
        (empresa_id, nome_empresa)
    )
    cache[normalized] = empresa_id
    print(f"  ✓ Empresa criada: {nome_empresa}")
    return empresa_id

def get_or_create_hierarchy(cursor, empresa_id, diretoria, gerencia, coordenacao, area_detalhe, cache):
    """Busca ou cria hierarquia completa (diretoria → gerência → coordenação → área)."""
    # Normalizar valores
    dir_norm = normalize_text(diretoria)
    ger_norm = normalize_text(gerencia)
    coord_norm = normalize_text(coordenacao)
    area_norm = normalize_text(area_detalhe)
    
    cache_key = (empresa_id, dir_norm, ger_norm, coord_norm, area_norm)
    
    if cache_key in cache:
        return cache[cache_key]
    
    # 1. Diretoria
    cursor.execute(
        "SELECT id_diretoria FROM diretoria WHERE id_empresa = %s AND LOWER(TRIM(nome_diretoria)) = %s",
        (empresa_id, dir_norm)
    )
    result = cursor.fetchone()
    if result:
        diretoria_id = result[0]
    else:
        diretoria_id = str(uuid4())
        cursor.execute(
            "INSERT INTO diretoria (id_diretoria, id_empresa, nome_diretoria) VALUES (%s, %s, %s)",
            (diretoria_id, empresa_id, diretoria)
        )
    
    # 2. Gerência
    cursor.execute(
        "SELECT id_gerencia FROM gerencia WHERE id_diretoria = %s AND LOWER(TRIM(nome_gerencia)) = %s",
        (diretoria_id, ger_norm)
    )
    result = cursor.fetchone()
    if result:
        gerencia_id = result[0]
    else:
        gerencia_id = str(uuid4())
        cursor.execute(
            "INSERT INTO gerencia (id_gerencia, id_diretoria, nome_gerencia) VALUES (%s, %s, %s)",
            (gerencia_id, diretoria_id, gerencia)
        )
    
    # 3. Coordenação
    cursor.execute(
        "SELECT id_coordenacao FROM coordenacao WHERE id_gerencia = %s AND LOWER(TRIM(nome_coordenacao)) = %s",
        (gerencia_id, coord_norm)
    )
    result = cursor.fetchone()
    if result:
        coordenacao_id = result[0]
    else:
        coordenacao_id = str(uuid4())
        cursor.execute(
            "INSERT INTO coordenacao (id_coordenacao, id_gerencia, nome_coordenacao) VALUES (%s, %s, %s)",
            (coordenacao_id, gerencia_id, coordenacao)
        )
    
    # 4. Área
    cursor.execute(
        "SELECT id_area_detalhe FROM area_detalhe WHERE id_coordenacao = %s AND LOWER(TRIM(nome_area_detalhe)) = %s",
        (coordenacao_id, area_norm)
    )
    result = cursor.fetchone()
    if result:
        area_id = result[0]
    else:
        area_id = str(uuid4())
        cursor.execute(
            "INSERT INTO area_detalhe (id_area_detalhe, id_coordenacao, nome_area_detalhe) VALUES (%s, %s, %s)",
            (area_id, coordenacao_id, area_detalhe)
        )
    
    cache[cache_key] = area_id
    return area_id

def get_dimensao_id(cursor, nome_dimensao, cache):
    """Busca ID de dimensão de avaliação (deve existir no banco via migration)."""
    normalized = normalize_text(nome_dimensao)
    
    if normalized in cache:
        return cache[normalized]
    
    cursor.execute(
        "SELECT id_dimensao_avaliacao FROM dimensao_avaliacao WHERE LOWER(TRIM(nome_dimensao)) = %s",
        (normalized,)
    )
    result = cursor.fetchone()
    
    if result:
        cache[normalized] = result[0]
        return result[0]
    
    # Criar nova dimensão se não existir
    new_id = str(uuid4())
    cursor.execute(
        "INSERT INTO dimensao_avaliacao (id_dimensao_avaliacao, nome_dimensao, ativa) VALUES (%s, %s, true) RETURNING id_dimensao_avaliacao",
        (new_id, nome_dimensao)
    )
    result = cursor.fetchone()
    cache[normalized] = result[0]
    return result[0]

def parse_date(date_str):
    """Converte string de data DD/MM/YYYY para YYYY-MM-DD."""
    if not date_str or date_str.strip() == '-':
        return None
    try:
        dt = datetime.strptime(date_str.strip(), '%d/%m/%Y')
        return dt.strftime('%Y-%m-%d')
    except:
        return None

def import_csv_data(csv_file_path):
    """Importa dados do CSV para o banco de dados."""
    print(f"\n🚀 Iniciando importação do CSV: {csv_file_path}")
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Caches para evitar lookups repetidos
    lookup_cache = {}
    empresa_cache = {}
    hierarchy_cache = {}
    dimensao_cache = {}
    
    stats = {
        'empresas': 0,
        'funcionarios': 0,
        'avaliacoes': 0,
        'respostas': 0,
        'erros': 0
    }
    
    try:
        with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
            
            for row_num, row in enumerate(reader, start=2):  # Start at 2 (1 = header)
                try:
                    # 1. Empresa
                    empresa_nome = row.get('n0_empresa', '').strip() or 'Empresa'
                    empresa_id = get_or_create_empresa(cursor, empresa_nome, empresa_cache)
                    if empresa_id not in empresa_cache.values():
                        stats['empresas'] += 1
                    
                    # 2. Hierarquia
                    area_id = get_or_create_hierarchy(
                        cursor, empresa_id,
                        row.get('n1_diretoria', '').strip(),
                        row.get('n2_gerencia', '').strip(),
                        row.get('n3_coordenacao', '').strip(),
                        row.get('n4_area', '').strip(),
                        hierarchy_cache
                    )
                    
                    # 3. Lookups
                    cargo_id = get_or_create_lookup(cursor, 'cargo', 'nome_cargo', row.get('cargo', '').strip(), lookup_cache)
                    genero_id = get_or_create_lookup(cursor, 'genero_catgo', 'nome_genero', row.get('genero', '').strip(), lookup_cache)
                    geracao_id = get_or_create_lookup(cursor, 'geracao_catgo', 'nome_geracao', row.get('geracao', '').strip(), lookup_cache)
                    tempo_id = get_or_create_lookup(cursor, 'tempo_empresa_catgo', 'nome_tempo_empresa', row.get('tempo_de_empresa', '').strip(), lookup_cache)
                    localidade_id = get_or_create_lookup(cursor, 'localidade', 'nome_localidade', row.get('localidade', '').strip(), lookup_cache)
                    
                    # 4. Funcionário
                    funcionario_id = str(uuid4())
                    cursor.execute("""
                        INSERT INTO funcionario (
                            id_funcionario, nome_funcionario, email, email_corporativo,
                            id_area_detalhe, id_cargo, id_genero_catgo, id_geracao_catgo, 
                            id_tempo_empresa_catgo, id_localidade, data_admissao
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, CURRENT_DATE)
                    """, (
                        funcionario_id,
                        row.get('nome', '').strip(),
                        row.get('email', '').strip(),
                        row.get('email_corporativo', '').strip(),
                        area_id, cargo_id, genero_id, geracao_id, tempo_id, localidade_id
                    ))
                    stats['funcionarios'] += 1
                    
                    # 5. Avaliação
                    data_resposta = parse_date(row.get('Data da Resposta', ''))
                    enps_value = row.get('eNPS', '').strip()
                    enps_comentario = row.get('[Aberta] eNPS', '').strip() or None
                    
                    avaliacao_id = str(uuid4())
                    cursor.execute("""
                        INSERT INTO avaliacao (
                            id_avaliacao, id_funcionario, data_avaliacao, comentario_geral
                        ) VALUES (%s, %s, %s, %s)
                    """, (avaliacao_id, funcionario_id, data_resposta or 'CURRENT_DATE', enps_comentario))
                    stats['avaliacoes'] += 1
                    
                    # 6. Respostas das dimensões
                    for dimensao_csv, dimensao_key in DIMENSOES:
                        dimensao_id = get_dimensao_id(cursor, dimensao_key, dimensao_cache)
                        if not dimensao_id:
                            continue
                        
                        valor_str = row.get(dimensao_csv, '').strip()
                        valor = int(valor_str) if valor_str and valor_str.isdigit() else None
                        
                        comentario_col = f'Comentários - {dimensao_csv}'
                        comentario = row.get(comentario_col, '').strip() or None
                        if comentario == '-':
                            comentario = None
                        
                        if valor is not None:
                            resposta_id = str(uuid4())
                            cursor.execute("""
                                INSERT INTO resposta_dimensao (
                                    id_resposta_dimensao, id_avaliacao, id_dimensao_avaliacao, valor_resposta, comentario
                                ) VALUES (%s, %s, %s, %s, %s)
                            """, (resposta_id, avaliacao_id, dimensao_id, valor, comentario))
                            stats['respostas'] += 1
                    
                    # Commit a cada 50 registros
                    if row_num % 50 == 0:
                        conn.commit()
                        print(f"  ⏳ Processados {row_num - 1} funcionários...")
                
                except Exception as e:
                    stats['erros'] += 1
                    print(f"  ❌ Erro na linha {row_num}: {str(e)}")
                    continue
        
        # Commit final
        conn.commit()
        
        print(f"\n✅ Importação concluída com sucesso!")
        print(f"   📊 Estatísticas:")
        print(f"      - Empresas criadas: {stats['empresas']}")
        print(f"      - Funcionários importados: {stats['funcionarios']}")
        print(f"      - Avaliações criadas: {stats['avaliacoes']}")
        print(f"      - Respostas registradas: {stats['respostas']}")
        if stats['erros'] > 0:
            print(f"      - Erros encontrados: {stats['erros']}")
    
    except Exception as e:
        conn.rollback()
        print(f"\n❌ Erro fatal durante importação: {str(e)}")
        raise
    
    finally:
        cursor.close()
        conn.close()

def main():
    """Função principal."""
    if len(sys.argv) < 2:
        print("Uso: python import_csv.py <caminho_do_csv>")
        sys.exit(1)
    
    csv_path = sys.argv[1]
    
    if not os.path.exists(csv_path):
        print(f"❌ Arquivo não encontrado: {csv_path}")
        sys.exit(1)
    
    import_csv_data(csv_path)

if __name__ == '__main__':
    main()
