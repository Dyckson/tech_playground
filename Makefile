.PHONY: help init setup db-import dev logs logs-api logs-frontend down clean diagnose status migrations generate-data validate

help:
	@echo "Tech Playground - Makefile Commands"
	@echo ""
	@echo "⚡ Quick Start (1 comando para subir TUDO):"
	@echo "  make init           Suba Backend + Frontend + DB (tudo automático!)"
	@echo ""
	@echo "Development:"
	@echo "  make dev            Modo desenvolvimento"
	@echo ""
	@echo "Database:"
	@echo "  make migrations     Executar migrations"
	@echo "  make generate-data  Gerar dados multi-empresa"
	@echo "  make validate       Validar integridade DB"
	@echo ""
	@echo "Docker:"
	@echo "  make logs           Ver logs (todos)"
	@echo "  make logs-api       Ver logs (API)"
	@echo "  make logs-frontend  Ver logs (Frontend)"
	@echo "  make status         Status containers"
	@echo "  make down           Parar containers"
	@echo "  make clean          Limpar tudo"
	@echo ""
	@echo "Debug:"
	@echo "  make diagnose       Diagnosticar"
	@echo ""

init:
	@echo "╔════════════════════════════════════════════════════════════╗"
	@echo "║         🚀 SUBINDO PROJETO DO ZERO (TUDO AUTOMÁTICO)      ║"
	@echo "╚════════════════════════════════════════════════════════════╝"
	@echo ""
	@echo "📋 Passo 1: Preparando arquivos..."
	@if [ ! -f .env ]; then cp .env.example .env; echo "✅ .env criado"; fi
	@echo ""
	@echo "🐳 Passo 2: Limpando containers antigos..."
	@docker-compose down --remove-orphans 2>/dev/null || true
	@echo "✅ Limpo"
	@echo ""
	@echo "🔨 Passo 3: Buildando imagens Docker..."
	@docker-compose build
	@echo "✅ Build completo"
	@echo ""
	@echo "📦 Passo 4: Subindo PostgreSQL + Redis..."
	@docker-compose up -d postgres redis
	@echo "⏳ Aguardando database ficar saudável..."
	@for i in 1 2 3 4 5 6 7 8 9 10; do \
		if docker exec tech_playground_db pg_isready -U tech_user > /dev/null 2>&1; then \
			echo "✅ PostgreSQL pronto!"; \
			break; \
		fi; \
		echo "  ⏳ Tentativa $$i/10..."; \
		sleep 3; \
	done
	@echo ""
	@echo "🔥 Passo 5: Subindo Backend (com migrations + seed automático)..."
	@docker-compose up -d api
	@echo "⏳ Aguardando Backend executar migrations..."
	@sleep 5
	@for i in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15; do \
		if curl -s http://localhost:9876/health > /dev/null 2>&1; then \
			echo "✅ Backend pronto (migrations + seed executados)!"; \
			break; \
		fi; \
		echo "  ⏳ Tentativa $$i/15..."; \
		sleep 2; \
	done
	@echo ""
	@echo "🎨 Passo 6: Subindo Frontend..."
	@docker-compose up -d frontend
	@echo "⏳ Aguardando Frontend..."
	@sleep 5
	@echo "✅ Frontend pronto!"
	@echo ""
	@echo "╔════════════════════════════════════════════════════════════╗"
	@echo "║                   ✨ PROJETO ONLINE! ✨                    ║"
	@echo "╚════════════════════════════════════════════════════════════╝"
	@echo ""
	@echo "📍 URLs de Acesso:"
	@echo "   🖥️  Frontend:  http://localhost:7654"
	@echo "   🔌 API:       http://localhost:9876"
	@echo "   💾 Database:  localhost:9432"
	@echo ""
	@echo "📊 Visualizar Dados:"
	@echo "   $ make validate      (verificar integridade DB)"
	@echo "   $ make logs-api      (ver logs da API)"
	@echo "   $ make logs-frontend (ver logs do Frontend)"
	@echo ""

setup:
	@echo "🚀 Setup inicial..."
	@if [ ! -f .env ]; then cp .env.example .env; echo "✅ .env criado"; fi
	@echo "📦 Iniciando containers..."
	@docker-compose down --remove-orphans 2>/dev/null || true
	@docker-compose up -d postgres redis
	@echo "⏳ Aguardando database..."
	@sleep 10
	@docker-compose up -d api frontend
	@echo "⏳ Aguardando API..."
	@for i in 1 2 3 4 5 6 7 8 9 10; do if curl -s http://localhost:9876/health > /dev/null 2>&1; then echo "✅ API pronta!"; exit 0; fi; echo "  Tentativa $$i/10..."; sleep 3; done
	@echo "✅ Setup completo!"

db-import:
	@echo "📥 Importando dados..."
	@if ! curl -s http://localhost:8000/health > /dev/null 2>&1; then echo "❌ API não pronta"; exit 1; fi
	@sleep 5
	@cd backend && python3 scripts/import_data.py
	@echo "✅ Dados importados!"
	@echo "🎉 Projeto pronto!"

dev:
	@echo "👨‍💻 Modo desenvolvimento"
	@docker-compose up

logs:
	@docker-compose logs -f

logs-api:
	@docker-compose logs -f api

logs-frontend:
	@docker-compose logs -f frontend

status:
	@echo "Status:"
	@docker-compose ps

down:
	@echo "⏸️  Parando..."
	@docker-compose down

clean:
	@echo "🧹 Limpando..."
	@docker-compose down -v --remove-orphans
	@echo "✅ Limpo!"

diagnose:
	@./diagnose.sh

migrations:
	@echo "⚙️  Executando migrations..."
	@docker cp backend/scripts/run_migrations.py tech_playground_api:/app/ 2>/dev/null || true
	@docker exec tech_playground_api python3 /app/run_migrations.py
	@echo "✅ Migrations executadas!"

generate-data:
	@echo "🔄 Gerando dados multi-empresa..."
	@docker cp backend/scripts/generate_multi_company_data.py tech_playground_api:/app/ 2>/dev/null || true
	@docker exec tech_playground_api python3 /app/generate_multi_company_data.py
	@echo "✅ Dados gerados!"

validate:
	@echo "✔️  Validando integridade do banco..."
	@docker cp backend/scripts/validate_and_report.py tech_playground_api:/app/ 2>/dev/null || true
	@docker exec tech_playground_api python3 /app/validate_and_report.py
	@echo "✅ Validação concluída!"