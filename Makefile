.PHONY: help run down logs restart test test-unit test-integration test-cov

# Cores para output
GREEN  := \033[0;32m
YELLOW := \033[0;33m
BLUE   := \033[0;34m
NC     := \033[0m # No Color

help: ## Mostra esta mensagem de ajuda
	@echo "$(BLUE)========================================$(NC)"
	@echo "$(GREEN)   Tech Playground - Comandos Make$(NC)"
	@echo "$(BLUE)========================================$(NC)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "$(YELLOW)%-20s$(NC) %s\n", $$1, $$2}'
	@echo ""

# ==================== DOCKER ====================

run: ## Sobe todos os containers do projeto
	@echo "$(GREEN)🚀 Subindo containers...$(NC)"
	docker-compose up -d
	@echo "$(GREEN)✅ Containers ativos!$(NC)"
	@echo "$(BLUE)📊 Backend: http://localhost:9876$(NC)"
	@echo "$(BLUE)📊 Docs API: http://localhost:9876/docs$(NC)"

down: ## Para e remove todos os containers
	@echo "$(YELLOW)🛑 Parando containers...$(NC)"
	docker-compose down
	@echo "$(GREEN)✅ Containers parados$(NC)"

logs: ## Mostra logs dos containers
	docker-compose logs -f

restart: ## Reinicia todos os containers
	@echo "$(YELLOW)🔄 Reiniciando containers...$(NC)"
	docker-compose restart
	@echo "$(GREEN)✅ Containers reiniciados$(NC)"

# ==================== TESTES ====================

test: ## Executa todos os testes
	@echo "$(BLUE)🧪 Executando todos os testes...$(NC)"
	docker exec -it tech_playground_backend pytest tests/ -v

test-unit: ## Executa apenas testes unitários
	@echo "$(BLUE)🧪 Executando testes unitários...$(NC)"
	docker exec -it tech_playground_backend pytest tests/unitarios/ -v

test-integration: ## Executa apenas testes de integração
	@echo "$(BLUE)🧪 Executando testes de integração...$(NC)"
	docker exec -it tech_playground_backend pytest tests/integracao/ -v --cov-fail-under=70

test-cov: ## Executa testes com cobertura de código
	@echo "$(BLUE)📊 Executando testes com cobertura...$(NC)"
	docker exec -it tech_playground_backend pytest tests/ --cov=app --cov-report=html --cov-report=term-missing:skip-covered
	@echo "$(GREEN)✅ Relatório gerado em backend/htmlcov/index.html$(NC)"

# ==================== DEFAULT ====================

.DEFAULT_GOAL := help
