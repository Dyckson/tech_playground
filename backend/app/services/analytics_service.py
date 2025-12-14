"""
Analytics Service
Lógica de negócio para análises e métricas
"""

from uuid import UUID

from app.repositories.analytics_repository import AnalyticsRepository


class AnalyticsService:
    def __init__(self):
        self.repository = AnalyticsRepository()

    def get_enps_distribution(self, empresa_id: UUID | None = None) -> dict:
        """
        Retorna distribuição eNPS com cálculo do score
        eNPS Score = % Promotores - % Detratores
        """
        data = self.repository.get_enps_distribution(empresa_id)
        
        # Calcular eNPS Score
        enps_score = data["promotores_percentual"] - data["detratores_percentual"]
        
        return {
            **data,
            "enps_score": round(enps_score, 2),
            "total_respostas": data["promotores"] + data["neutros"] + data["detratores"],
        }

    def get_tenure_distribution(self, empresa_id: UUID | None = None) -> dict:
        """Retorna distribuição por tempo de casa"""
        data = self.repository.get_tenure_distribution(empresa_id)
        
        total = sum(item["quantidade"] for item in data)
        
        return {
            "distribuicao": data,
            "total_funcionarios": total,
        }

    def get_satisfaction_scores(self, empresa_id: UUID | None = None) -> dict:
        """
        Retorna scores médios das dimensões
        Com score geral médio
        """
        data = self.repository.get_satisfaction_scores(empresa_id)
        
        # Calcular score geral (média das médias)
        if data:
            scores_validos = [item["score_medio"] for item in data if item["score_medio"] is not None]
            score_geral = sum(scores_validos) / len(scores_validos) if scores_validos else 0
        else:
            score_geral = 0
        
        return {
            "dimensoes": data,
            "score_geral": round(score_geral, 2),
            "total_dimensoes": len(data),
        }
