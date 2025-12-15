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

    def get_areas_scores_comparison(self, empresa_id: UUID | None = None) -> dict:
        """
        Retorna comparação de scores entre áreas por dimensão
        Task 7 - Visualização 1: Average Feedback Scores by Department
        """
        data = self.repository.get_areas_scores_comparison(empresa_id)
        
        # Organizar dados por área
        areas_dict = {}
        for row in data:
            area_id = str(row["id_area_detalhe"])
            if area_id not in areas_dict:
                areas_dict[area_id] = {
                    "area_id": area_id,
                    "area_nome": row["area_nome"],
                    "coordenacao": row["nome_coordenacao"],
                    "gerencia": row["nome_gerencia"],
                    "diretoria": row["nome_diretoria"],
                    "total_funcionarios": row["total_funcionarios"],
                    "dimensoes": [],
                    "score_medio_geral": 0,
                }
            
            if row["dimensao"]:  # Só adicionar se houver dimensão
                areas_dict[area_id]["dimensoes"].append({
                    "dimensao": row["dimensao"],
                    "score_medio": float(row["score_medio"]) if row["score_medio"] else None,
                    "total_respostas": row["total_respostas"],
                })
        
        # Calcular score médio geral por área
        areas_list = list(areas_dict.values())
        for area in areas_list:
            if area["dimensoes"]:
                scores_validos = [d["score_medio"] for d in area["dimensoes"] if d["score_medio"] is not None]
                area["score_medio_geral"] = round(sum(scores_validos) / len(scores_validos), 2) if scores_validos else 0
        
        return {
            "areas": areas_list,
            "total_areas": len(areas_list),
        }

    def get_areas_enps_comparison(self, empresa_id: UUID | None = None) -> dict:
        """
        Retorna comparação de eNPS entre áreas
        Task 7 - Visualização 2: eNPS Scores Segmented by Department
        """
        data = self.repository.get_areas_enps_comparison(empresa_id)
        
        # Calcular eNPS score para cada área
        areas_list = []
        for row in data:
            promotores_pct = float(row["promotores_percentual"]) if row["promotores_percentual"] else 0
            detratores_pct = float(row["detratores_percentual"]) if row["detratores_percentual"] else 0
            enps_score = promotores_pct - detratores_pct
            
            areas_list.append({
                "area_id": str(row["id_area_detalhe"]),
                "area_nome": row["area_nome"],
                "coordenacao": row["nome_coordenacao"],
                "gerencia": row["nome_gerencia"],
                "diretoria": row["nome_diretoria"],
                "promotores": row["promotores"],
                "neutros": row["neutros"],
                "detratores": row["detratores"],
                "promotores_percentual": promotores_pct,
                "neutros_percentual": float(row["neutros_percentual"]) if row["neutros_percentual"] else 0,
                "detratores_percentual": detratores_pct,
                "enps_score": round(enps_score, 2),
                "total_respostas": row["total_respostas"],
            })
        
        # Ordenar por eNPS score (decrescente)
        areas_list.sort(key=lambda x: x["enps_score"], reverse=True)
        
        # Calcular médias gerais
        if areas_list:
            avg_enps = sum(a["enps_score"] for a in areas_list) / len(areas_list)
            melhor_area = areas_list[0]
            pior_area = areas_list[-1]
        else:
            avg_enps = 0
            melhor_area = None
            pior_area = None
        
        return {
            "areas": areas_list,
            "total_areas": len(areas_list),
            "enps_medio": round(avg_enps, 2),
            "melhor_area": melhor_area,
            "pior_area": pior_area,
        }

    def get_area_detailed_metrics(self, area_id: UUID) -> dict:
        """
        Retorna métricas detalhadas de uma área específica
        Incluindo comparação com empresa e insights
        """
        data = self.repository.get_area_detailed_metrics(area_id)
        
        # Calcular eNPS
        enps_data = data["enps"]
        total_enps = enps_data["promotores"] + enps_data["neutros"] + enps_data["detratores"]
        
        if total_enps > 0:
            promotores_pct = (enps_data["promotores"] / total_enps) * 100
            detratores_pct = (enps_data["detratores"] / total_enps) * 100
            enps_score = promotores_pct - detratores_pct
        else:
            promotores_pct = 0
            detratores_pct = 0
            enps_score = 0
        
        # Construir comparação de scores
        scores_comparison = []
        area_scores_dict = {s["dimensao"]: s for s in data["area_scores"]}
        
        for company_avg in data["company_averages"]:
            dimensao = company_avg["dimensao"]
            area_score_data = area_scores_dict.get(dimensao, {})
            area_score = area_score_data.get("score_medio")
            company_score = company_avg["score_medio"]
            
            diff = None
            if area_score and company_score:
                diff = round(float(area_score) - float(company_score), 2)
            
            scores_comparison.append({
                "dimensao": dimensao,
                "area_score": float(area_score) if area_score else None,
                "company_score": float(company_score) if company_score else None,
                "diferenca": diff,
                "total_respostas": area_score_data.get("total_respostas", 0),
            })
        
        return {
            "area_info": data["area_info"],
            "scores_comparison": scores_comparison,
            "enps": {
                "promotores": enps_data["promotores"],
                "neutros": enps_data["neutros"],
                "detratores": enps_data["detratores"],
                "promotores_percentual": round(promotores_pct, 2),
                "detratores_percentual": round(detratores_pct, 2),
                "enps_score": round(enps_score, 2),
                "total_respostas": total_enps,
            },
        }
