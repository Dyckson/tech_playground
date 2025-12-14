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

    def get_employee_detailed_profile(self, funcionario_id: UUID) -> dict:
        """
        Retorna perfil detalhado do funcionário com analytics completo
        Formata dados para comparação visual (Radar Chart)
        """
        analytics = self.repository.get_employee_detailed_analytics(funcionario_id)
        
        # Construir estrutura para Radar Chart (employee vs company vs area)
        dimensoes_map = {}
        
        # Mapear scores do funcionário
        for item in analytics["employee_scores"]:
            dimensoes_map[item["dimensao"]] = {
                "dimensao": item["dimensao"],
                "employee_score": float(item["score"]) if item["score"] else None,
                "tipo_escala": item["tipo_escala"],
                "comentario": item["comentario"],
            }
        
        # Adicionar médias da empresa
        for item in analytics["company_averages"]:
            if item["dimensao"] in dimensoes_map:
                dimensoes_map[item["dimensao"]]["company_avg"] = float(item["score_medio"]) if item["score_medio"] else None
            else:
                dimensoes_map[item["dimensao"]] = {
                    "dimensao": item["dimensao"],
                    "employee_score": None,
                    "company_avg": float(item["score_medio"]) if item["score_medio"] else None,
                    "tipo_escala": None,
                    "comentario": None,
                }
        
        # Adicionar médias da área
        for item in analytics["area_averages"]:
            if item["dimensao"] in dimensoes_map:
                dimensoes_map[item["dimensao"]]["area_avg"] = float(item["score_medio"]) if item["score_medio"] else None
        
        # Converter para lista
        comparison_data = list(dimensoes_map.values())
        
        # Calcular diferenças (employee vs company)
        for item in comparison_data:
            if item["employee_score"] and item["company_avg"]:
                item["diff_company"] = round(item["employee_score"] - item["company_avg"], 2)
            else:
                item["diff_company"] = None
            
            if item["employee_score"] and item.get("area_avg"):
                item["diff_area"] = round(item["employee_score"] - item.get("area_avg", 0), 2)
            else:
                item["diff_area"] = None
        
        return {
            "comparison": comparison_data,
            "history": analytics["history"],
            "comments": analytics["comments"],
            "summary": {
                "total_evaluations": len(analytics["history"]),
                "has_comments": len(analytics["comments"]) > 0,
                "dimensions_evaluated": len([d for d in comparison_data if d["employee_score"] is not None]),
            },
        }
