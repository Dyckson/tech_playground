#!/bin/bash
set -e

echo "Aguardando banco de dados..."
until PGPASSWORD=$DB_PASSWORD psql -h "$DB_HOST" -U "$DB_USER" -d "$DB_NAME" -c '\q' 2>/dev/null; do
  sleep 1
done

echo "Banco de dados disponível!"

echo "Executando migrações..."
if [ -d "/app/database/migrations" ]; then
    for f in /app/database/migrations/*.sql; do
        if [ -f "$f" ]; then
            echo "Executando $f..."
            PGPASSWORD=$DB_PASSWORD psql -h "$DB_HOST" -U "$DB_USER" -d "$DB_NAME" -f "$f"
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
