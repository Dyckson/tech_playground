"""
Tech Playground API
Sistema de análise de eNPS e feedback de funcionários
"""

import logging
import sys
from contextlib import asynccontextmanager
from datetime import datetime

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database.connection import DatabaseConnection
from app.routes import register_routes


# Logging
logging.basicConfig(level=settings.LOG_LEVEL, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


# Lifecycle
@asynccontextmanager
async def lifespan(app: FastAPI):
    # STARTUP
    try:
        DatabaseConnection.init_pool()
        logger.info("✅ Aplicação iniciada com sucesso")
        logger.info(f"📊 Database: {settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}")
        logger.info(f"⚙️  Environment: {settings.ENVIRONMENT}")
    except Exception as e:
        logger.error(f"❌ Erro ao iniciar: {e!s}")
        sys.exit(1)

    yield

    # SHUTDOWN
    DatabaseConnection.close_all()
    logger.info("✅ Aplicação finalizada")


# FastAPI App
app = FastAPI(
    title=settings.API_TITLE,
    description="""
    ## Tech Playground API - Sistema de eNPS e Feedback
    
    ### Funcionalidades:
    - 📊 **Hierarquia**: Gestão de estrutura organizacional (empresa → diretoria → gerência → coordenação → área)
    - 👥 **Funcionários**: CRUD completo com busca, filtros e paginação
    - 📝 **Avaliações**: Gestão de avaliações com 7 dimensões de feedback
    - 📈 **Analytics**: Cálculos de eNPS, favorabilidade e insights
    
    ### Métricas:
    - **eNPS**: Employee Net Promoter Score (-100 a +100)
    - **Favorabilidade**: % de respostas positivas (4-5 em escala Likert 1-5)
    - **Insights**: Análise de comentários e tendências
    """,
    version=settings.API_VERSION,
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health Check
@app.get("/health", tags=["Health"])
async def health_check():
    """Health check geral da API"""
    return {
        "status": "healthy",
        "environment": settings.ENVIRONMENT,
        "version": settings.API_VERSION,
        "database": settings.DB_NAME,
        "timestamp": datetime.now().isoformat(),
    }


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint com informações da API"""
    return {
        "message": "Tech Playground API",
        "version": settings.API_VERSION,
        "docs": "/docs",
        "redoc": "/redoc",
        "health": "/health",
    }


# Registra todas as rotas
register_routes(app)

if __name__ == "__main__":
    import uvicorn

    logger.info(f"🚀 Iniciando {settings.API_TITLE} v{settings.API_VERSION}")

    uvicorn.run(
        app,
        host=settings.API_HOST,
        port=settings.API_PORT,
        workers=1 if settings.ENVIRONMENT == "development" else 4,
        reload=settings.DEBUG,
    )
