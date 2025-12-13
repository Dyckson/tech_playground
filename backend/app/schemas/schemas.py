"""
Schemas - Ponto de entrada centralizado
Importa e re-exporta todos os schemas dos módulos específicos
"""

# Hierarquia
# Analytics
from .analytics import (
    EnpsGeral,
    EnpsPorArea,
    EnpsPorCargo,
    EnpsPorSegmento,
    FavorabilidadeDimensao,
    FavorabilidadePorSegmento,
    InsightBaixoEnps,
    TendenciaEnps,
)

# Avaliação
from .avaliacao import (
    AvaliacaoBase,
    AvaliacaoCompleta,
    AvaliacaoCreate,
    AvaliacaoResponse,
    DimensaoRespostaBase,
    DimensaoRespostaCreate,
    DimensaoRespostaResponse,
)

# Filtros
from .filtros import (
    AreaUnica,
    CargoUnico,
    ContagemPorArea,
    FiltroOpcao,
    LocalidadeUnica,
)

# Funcionário
from .funcionario import (
    FuncionarioBase,
    FuncionarioCreate,
    FuncionarioPaginada,
    FuncionarioResponse,
)

# Health
from .health import (
    HealthCheck,
)
from .hierarquia import (
    AreaDetalheResponse,
    CoordenacaoResponse,
    DiretoriaResponse,
    EmpresaBase,
    EmpresaCreate,
    EmpresaResponse,
    GerenciaResponse,
    HierarquiaCompleta,
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
