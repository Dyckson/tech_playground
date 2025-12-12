#!/bin/bash

# 🔍 Tech Playground - Diagnostic Script
# Verifica se tudo está configurado corretamente

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo ""
echo -e "${YELLOW}🔍 Tech Playground - Diagnóstico${NC}"
echo ""

# 1. Check Docker
echo "1️⃣  Docker:"
if command -v docker &> /dev/null; then
    VERSION=$(docker --version)
    echo -e "  ${GREEN}✅${NC} $VERSION"
else
    echo -e "  ${RED}❌ Docker não encontrado${NC}"
    exit 1
fi

# 2. Check Docker Compose
echo ""
echo "2️⃣  Docker Compose:"
if command -v docker-compose &> /dev/null; then
    VERSION=$(docker-compose --version)
    echo -e "  ${GREEN}✅${NC} $VERSION"
else
    echo -e "  ${RED}❌ Docker Compose não encontrado${NC}"
    exit 1
fi

# 3. Check .env
echo ""
echo "3️⃣  Configuração (.env):"
if [ -f .env ]; then
    echo -e "  ${GREEN}✅${NC} .env existe"
else
    echo -e "  ${RED}❌ .env não encontrado${NC}"
    echo "    Execute: cp .env.example .env"
fi

# 4. Check containers
echo ""
echo "4️⃣  Containers:"
if docker-compose ps | grep -q "Up"; then
    echo -e "  ${GREEN}✅${NC} Containers rodando:"
    docker-compose ps | tail -n +2 | awk '{print "     - " $1 " (" $6 ")"}'
else
    echo -e "  ${YELLOW}⚠️  Nenhum container rodando${NC}"
    echo "    Execute: make setup"
fi

# 5. Check API
echo ""
echo "5️⃣  API:"
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo -e "  ${GREEN}✅${NC} API respondendo"
    HEALTH=$(curl -s http://localhost:8000/health | python3 -c "import sys, json; print(json.load(sys.stdin)['status'])" 2>/dev/null || echo "unknown")
    echo "    Status: $HEALTH"
else
    echo -e "  ${RED}❌ API não respondendo${NC}"
fi

# 6. Check Frontend
echo ""
echo "6️⃣  Frontend:"
if curl -s http://localhost:3000 > /dev/null 2>&1; then
    echo -e "  ${GREEN}✅${NC} Frontend respondendo"
else
    echo -e "  ${RED}❌ Frontend não respondendo${NC}"
fi

# 7. Check Database
echo ""
echo "7️⃣  Database:"
if docker-compose ps | grep -q "postgres.*Up"; then
    CONN=$(docker-compose exec -T postgres psql -U tech_user -d tech_playground -c "SELECT COUNT(*) FROM funcionarios" 2>/dev/null || echo "0")
    echo -e "  ${GREEN}✅${NC} PostgreSQL conectado"
    echo "    Funcionários no BD: $CONN"
else
    echo -e "  ${RED}❌ PostgreSQL não respondendo${NC}"
fi

# 8. Check Redis
echo ""
echo "8️⃣  Cache (Redis):"
if docker-compose ps | grep -q "redis.*Up"; then
    echo -e "  ${GREEN}✅${NC} Redis conectado"
else
    echo -e "  ${RED}❌ Redis não respondendo${NC}"
fi

echo ""
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

# Summary
if curl -s http://localhost:8000/health > /dev/null 2>&1 && \
   curl -s http://localhost:3000 > /dev/null 2>&1 && \
   docker-compose ps | grep -q "postgres.*Up"; then
    echo -e "${GREEN}✅ Tudo OK! Sistema pronto para uso${NC}"
    echo ""
    echo "Próximos passos:"
    echo "  - Frontend: http://localhost:3000"
    echo "  - API: http://localhost:8000"
    echo "  - Docs: http://localhost:8000/docs"
else
    echo -e "${YELLOW}⚠️  Sistema incompleto${NC}"
    echo ""
    echo "Para completar setup:"
    echo "  make setup      # Setup inicial"
    echo "  make db-import  # Importar dados"
fi

echo ""
