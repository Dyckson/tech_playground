#!/usr/bin/env python3
"""
Entrypoint script for backend container
Compatible with both Windows and Linux
"""
import os
import sys
import time
import subprocess
import glob

def wait_for_database():
    """Wait for PostgreSQL to be ready"""
    print("Aguardando banco de dados...")
    
    db_host = os.environ.get('DB_HOST', 'postgres')
    db_user = os.environ.get('DB_USER', 'tech_user')
    db_password = os.environ.get('DB_PASSWORD', 'tech_password')
    db_name = os.environ.get('DB_NAME', 'tech_playground')
    
    env = os.environ.copy()
    env['PGPASSWORD'] = db_password
    
    cmd = f'psql -h {db_host} -U {db_user} -d {db_name} -c "SELECT 1"'
    
    while True:
        result = subprocess.run(
            cmd,
            shell=True,
            env=env,
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            break
        time.sleep(1)
    
    print("Banco de dados disponível!")

def create_migration_table():
    """Create migration history table"""
    print("Criando tabela de controle de migrations...")
    
    db_host = os.environ.get('DB_HOST', 'postgres')
    db_user = os.environ.get('DB_USER', 'tech_user')
    db_password = os.environ.get('DB_PASSWORD', 'tech_password')
    db_name = os.environ.get('DB_NAME', 'tech_playground')
    
    env = os.environ.copy()
    env['PGPASSWORD'] = db_password
    
    sql = """CREATE TABLE IF NOT EXISTS migration_history (
        id SERIAL PRIMARY KEY,
        filename VARCHAR(255) UNIQUE NOT NULL,
        executed_at TIMESTAMP DEFAULT NOW()
    )"""
    
    cmd = f'psql -h {db_host} -U {db_user} -d {db_name} -c "{sql}"'
    
    subprocess.run(cmd, shell=True, env=env, check=True, capture_output=True)

def run_migrations():
    """Execute SQL migrations"""
    print("Executando migrações...")
    
    db_host = os.environ.get('DB_HOST', 'postgres')
    db_user = os.environ.get('DB_USER', 'tech_user')
    db_password = os.environ.get('DB_PASSWORD', 'tech_password')
    db_name = os.environ.get('DB_NAME', 'tech_playground')
    
    env = os.environ.copy()
    env['PGPASSWORD'] = db_password
    
    migrations_dir = "/app/database/migrations"
    
    if not os.path.isdir(migrations_dir):
        print("⚠️  Diretório de migrations não encontrado")
        return
    
    migration_files = sorted(glob.glob(f"{migrations_dir}/*.sql"))
    
    for migration_file in migration_files:
        filename = os.path.basename(migration_file)
        
        # Check if migration was already executed
        check_cmd = f"psql -h {db_host} -U {db_user} -d {db_name} -t -c \"SELECT COUNT(*) FROM migration_history WHERE filename='{filename}'\""
        result = subprocess.run(check_cmd, shell=True, env=env, capture_output=True, text=True)
        
        already_run = int(result.stdout.strip())
        
        if already_run == 0:
            print(f"▶️  Executando {filename}...")
            
            # Execute migration
            exec_cmd = f'psql -h {db_host} -U {db_user} -d {db_name} -f {migration_file}'
            subprocess.run(exec_cmd, shell=True, env=env, check=True)
            
            # Register migration
            register_cmd = f"psql -h {db_host} -U {db_user} -d {db_name} -c \"INSERT INTO migration_history (filename) VALUES ('{filename}')\""
            subprocess.run(register_cmd, shell=True, env=env, capture_output=True)
            
            print(f"✅ {filename} concluída")
        else:
            print(f"⏭️  {filename} já executada, pulando...")
    
    print("Migrações concluídas!")

def import_csv():
    """Import data from CSV if enabled"""
    import_csv_enabled = os.environ.get('IMPORT_CSV', 'false').lower() == 'true'
    csv_file = "/app/data.csv"
    
    if import_csv_enabled and os.path.isfile(csv_file):
        print("Importando dados do CSV...")
        subprocess.run(
            f'python /app/scripts/import_csv.py {csv_file}',
            shell=True,
            check=True
        )
        print("Importação do CSV concluída!")

def start_application():
    """Start the FastAPI application"""
    print("Iniciando aplicação...")
    os.execvp("uvicorn", [
        "uvicorn",
        "app.main:app",
        "--host", "0.0.0.0",
        "--port", "8000",
        "--reload"
    ])

if __name__ == "__main__":
    try:
        wait_for_database()
        create_migration_table()
        run_migrations()
        import_csv()
        start_application()
    except KeyboardInterrupt:
        print("\n⚠️  Interrompido pelo usuário")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Erro: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)
