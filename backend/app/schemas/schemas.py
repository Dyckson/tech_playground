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
    "AreaDetalheResponse",
    # Filtros
    "AreaUnica",
    "AvaliacaoBase",
    "AvaliacaoCompleta",
    "AvaliacaoCreate",
    "AvaliacaoResponse",
    "CargoUnico",
    "ContagemPorArea",
    "CoordenacaoResponse",
    # Avaliação
    "DimensaoRespostaBase",
    "DimensaoRespostaCreate",
    "DimensaoRespostaResponse",
    "DiretoriaResponse",
    # Hierarquia
    "EmpresaBase",
    "EmpresaCreate",
    "EmpresaResponse",
    # Analytics
    "EnpsGeral",
    "EnpsPorArea",
    "EnpsPorCargo",
    "EnpsPorSegmento",
    "FavorabilidadeDimensao",
    "FavorabilidadePorSegmento",
    "FiltroOpcao",
    # Funcionário
    "FuncionarioBase",
    "FuncionarioCreate",
    "FuncionarioPaginada",
    "FuncionarioResponse",
    "GerenciaResponse",
    # Health
    "HealthCheck",
    "HierarquiaCompleta",
    "InsightBaixoEnps",
    "LocalidadeUnica",
    "TendenciaEnps",
]
