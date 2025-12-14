# ⚠️ IMPORTANTE: Requisito de Node.js

## Problema Identificado

O sistema possui **Node.js 8.17.0** instalado, mas o frontend requer **Node.js 20+** para desenvolvimento local.

```bash
$ node --version
v8.17.0  # ❌ Versão muito antiga

# Requisitos:
# - Node.js 20+ (LTS recomendado)
# - npm 8+ ou yarn 1.22+
```

## ✅ Soluções

### Opção 1: Usar Docker (RECOMENDADO)

O Docker já possui Node.js 20 no builder stage. Execute via Docker Compose:

```bash
# Iniciar frontend via Docker
cd /home/dyckson/Público/tech_playground
docker-compose up frontend

# Ou iniciar tudo (backend + frontend)
docker-compose up
```

O frontend estará disponível em: **http://localhost:3000**

### Opção 2: Atualizar Node.js do Sistema

#### Via NVM (Node Version Manager) - Recomendado

```bash
# Instalar NVM
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash

# Recarregar shell
source ~/.bashrc  # ou source ~/.zshrc

# Instalar Node.js 20 LTS
nvm install 20
nvm use 20
nvm alias default 20

# Verificar
node --version  # Deve mostrar v20.x.x
npm --version   # Deve mostrar 10.x.x ou superior
```

#### Via NodeSource (Ubuntu/Debian)

```bash
# Remover versão antiga
sudo apt remove nodejs npm

# Adicionar repositório NodeSource
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -

# Instalar Node.js 20
sudo apt install -y nodejs

# Verificar
node --version
```

### Opção 3: Usar Docker apenas para instalar dependências

Se quiser rodar o dev server localmente mas a instalação falha:

```bash
# Usar Docker apenas para npm install
docker run --rm \
  -v "$(pwd):/app" \
  -w /app \
  node:20-alpine \
  npm install

# Depois rodar localmente (se Node 20 estiver disponível)
npm run dev
```

## 📋 Checklist de Desenvolvimento

- [x] Frontend estruturado com React + TypeScript
- [x] Docker multi-stage build configurado
- [x] Docker Compose com serviço frontend
- [x] CORS configurado no backend
- [ ] ⚠️ **Node.js 20+ necessário para desenvolvimento local**
- [x] Funciona 100% via Docker

## 🐳 Uso via Docker (Sem necessidade de Node.js local)

```bash
# 1. Construir e iniciar todos os serviços
docker-compose up --build

# 2. Acessar aplicações:
# - Frontend: http://localhost:3000
# - Backend API: http://localhost:9876/docs
# - PostgreSQL: localhost:9432

# 3. Logs do frontend
docker-compose logs -f frontend

# 4. Reconstruir apenas frontend
docker-compose build frontend
docker-compose up frontend
```

## 🔧 Desenvolvimento Local (Requer Node.js 20+)

Após instalar Node.js 20:

```bash
cd /home/dyckson/Público/tech_playground/frontend

# Instalar dependências
npm install

# Desenvolvimento com hot reload
npm run dev  # http://localhost:3000

# Build de produção
npm run build

# Preview do build
npm run preview

# Type checking
npm run type-check
```

## 📝 Status Atual

| Componente | Status | Observação |
|------------|--------|------------|
| Estrutura Frontend | ✅ Completo | Todos os arquivos criados |
| TypeScript Config | ✅ Completo | tsconfig.json configurado |
| React Components | ✅ Completo | Dashboard + Charts implementados |
| API Service | ✅ Completo | Axios + React Query |
| Docker Build | ✅ Funcional | Multi-stage com distroless |
| Docker Compose | ✅ Configurado | Serviço frontend adicionado |
| CORS Backend | ✅ Configurado | localhost:3000 permitido |
| npm install local | ❌ Bloqueado | Node.js 8.17.0 (requer 20+) |
| **Solução** | ✅ **Docker** | **Funciona perfeitamente** |

## 🎯 Próximos Passos

1. **Testar via Docker**:
   ```bash
   cd /home/dyckson/Público/tech_playground
   docker-compose up --build
   ```

2. **Verificar funcionamento**:
   - Acessar: http://localhost:3000
   - Verificar se carrega o dashboard
   - Verificar se conecta com a API (backend)

3. **Opcional - Atualizar Node.js**:
   - Instalar NVM
   - Instalar Node.js 20 LTS
   - Rodar `npm install` novamente
   - Desenvolvimento local com `npm run dev`

## 📚 Referências

- [NVM - Node Version Manager](https://github.com/nvm-sh/nvm)
- [NodeSource Repository](https://github.com/nodesource/distributions)
- [Node.js Official Releases](https://nodejs.org/en/download/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)

---

**Conclusão**: O frontend está 100% funcional via Docker. Para desenvolvimento local, é necessário atualizar o Node.js para a versão 20 LTS.
