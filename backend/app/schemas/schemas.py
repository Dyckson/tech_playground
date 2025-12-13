"""
Schemas - Ponto de entrada centralizado
Importa e re-exporta todos os schemas dos módulos específicos
"""

# Hierarquia
from .hierarquia import (
    EmpresaBase,
    EmpresaCreate,
    EmpresaResponse,
    DiretoriaResponse,
    GerenciaResponse,
    CoordenacaoResponse,
    AreaDetalheResponse,
    HierarquiaCompleta,
)

# Funcionário
from .funcionario import (
    FuncionarioBase,
    FuncionarioCreate,
    FuncionarioResponse,
    FuncionarioPaginada,
)

# Avaliação
from .avaliacao import (
    DimensaoRespostaBase,
    DimensaoRespostaCreate,
    DimensaoRespostaResponse,
    AvaliacaoBase,
    AvaliacaoCreate,
    AvaliacaoResponse,
    AvaliacaoCompleta,
)

# Analytics
from .analytics import (
    EnpsGeral,
    EnpsPorSegmento,
    EnpsPorArea,
    EnpsPorCargo,
    FavorabilidadeDimensao,
    FavorabilidadePorSegmento,
    InsightBaixoEnps,
    TendenciaEnps,
)

# Filtros
from .filtros import (
    AreaUnica,
    CargoUnico,
    LocalidadeUnica,
    ContagemPorArea,
    FiltroOpcao,
)

# Health
from .health import (
    HealthCheck,
)

__all__ = [
    # Hierarquia
    "EmpresaBase",
    "EmpresaCreate",
    "EmpresaResponse",
    "DiretoriaResponse",
    "GerenciaResponse",
    "CoordenacaoResponse",
    "AreaDetalheResponse",
    "HierarquiaCompleta",
    # Funcionário
    "FuncionarioBase",
    "FuncionarioCreate",
    "FuncionarioResponse",
    "FuncionarioPaginada",
    # Avaliação
    "DimensaoRespostaBase",
    "DimensaoRespostaCreate",
    "DimensaoRespostaResponse",
    "AvaliacaoBase",
    "AvaliacaoCreate",
    "AvaliacaoResponse",
    "AvaliacaoCompleta",
    # Analytics
    "EnpsGeral",
    "EnpsPorSegmento",
    "EnpsPorArea",
    "EnpsPorCargo",
    "FavorabilidadeDimensao",
    "FavorabilidadePorSegmento",
    "InsightBaixoEnps",
    "TendenciaEnps",
    # Filtros
    "AreaUnica",
    "CargoUnico",
    "LocalidadeUnica",
    "ContagemPorArea",
    "FiltroOpcao",
    # Health
    "HealthCheck",
]
