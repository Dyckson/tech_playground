#!/bin/bash
set -e

echo "Aguardando banco de dados..."
until PGPASSWORD=$DB_PASSWORD psql -h "$DB_HOST" -U "$DB_USER" -d "$DB_NAME" -c '\q' 2>/dev/null; do
  sleep 1
done

echo "Banco de dados disponível!"

# Criar tabela de controle de migrations
echo "Criando tabela de controle de migrations..."
PGPASSWORD=$DB_PASSWORD psql -h "$DB_HOST" -U "$DB_USER" -d "$DB_NAME" <<-EOSQL
    CREATE TABLE IF NOT EXISTS migration_history (
        id SERIAL PRIMARY KEY,
        filename VARCHAR(255) UNIQUE NOT NULL,
        executed_at TIMESTAMP DEFAULT NOW()
    );
EOSQL

echo "Executando migrações..."
if [ -d "/app/database/migrations" ]; then
    for f in /app/database/migrations/*.sql; do
        if [ -f "$f" ]; then
            filename=$(basename "$f")
            
            # Verificar se migration já foi executada
            already_run=$(PGPASSWORD=$DB_PASSWORD psql -h "$DB_HOST" -U "$DB_USER" -d "$DB_NAME" -t -c \
                "SELECT COUNT(*) FROM migration_history WHERE filename='$filename'" | xargs)
            
            if [ "$already_run" -eq 0 ]; then
                echo "▶️  Executando $filename..."
                PGPASSWORD=$DB_PASSWORD psql -h "$DB_HOST" -U "$DB_USER" -d "$DB_NAME" -f "$f"
                
                # Registrar migration executada
                PGPASSWORD=$DB_PASSWORD psql -h "$DB_HOST" -U "$DB_USER" -d "$DB_NAME" -c \
                    "INSERT INTO migration_history (filename) VALUES ('$filename')" > /dev/null
                echo "✅ $filename concluída"
            else
                echo "⏭️  $filename já executada, pulando..."
            fi
        fi
    done
    echo "Migrações concluídas!"
fi

# Importar dados do CSV se habilitado
if [ "$IMPORT_CSV" = "true" ] && [ -f "/app/data.csv" ]; then
    echo "Importando dados do CSV..."
    python /app/scripts/import_csv.py /app/data.csv
    echo "Importação do CSV concluída!"
fi

echo "Iniciando aplicação..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
