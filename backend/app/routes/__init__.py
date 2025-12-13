"""
Routes Handler
Centraliza o registro de todas as rotas da API
"""
from fastapi import APIRouter
from app.controllers import hierarquia_controller, funcionario_controller


def register_routes(app) -> None:
    """
    Registra todas as rotas da aplicação
    
    Args:
        app: Instância FastAPI
    """
    # API Router principal
    api_router = APIRouter(prefix="/api")
    
    # Hierarquia
    api_router.include_router(
        hierarquia_controller.router,
        prefix="/hierarquia",
        tags=["Hierarquia"]
    )
    
    # Funcionários
    api_router.include_router(
        funcionario_controller.router,
        prefix="/funcionarios",
        tags=["Funcionários"]
    )
    
    # Registra o router principal
    app.include_router(api_router)
