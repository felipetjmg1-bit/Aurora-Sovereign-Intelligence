# prediction/risk_analysis.py

import json
from typing import Dict, List, Any, Optional
from datetime import datetime
from enum import Enum


class RiskLevel(Enum):
    """Níveis de risco."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class RiskAnalyzer:
    """
    Analisador de Risco para avaliação de cenários e mitigação de riscos.
    Implementa análise de risco, simulação de cenários e recomendações.
    """

    def __init__(self):
        self.risk_assessments = []
        self.scenarios = []
        self.mitigation_strategies = {}
        print("Analisador de Risco inicializado.")

    def assess_risk(self, risk_factors: Dict[str, float]) -> Dict[str, Any]:
        """Avalia o risco baseado em fatores."""
        assessment = {
            "timestamp": datetime.now().isoformat(),
            "risk_factors": risk_factors,
            "risk_scores": {},
            "overall_risk_level": None,
            "overall_risk_score": 0.0
        }

        # Calcular scores individuais
        for factor, value in risk_factors.items():
            # Normalizar valor entre 0 e 1
            normalized_value = min(max(value, 0), 1)
            assessment["risk_scores"][factor] = normalized_value

        # Calcular score geral
        if assessment["risk_scores"]:
            overall_score = sum(assessment["risk_scores"].values()) / len(assessment["risk_scores"])
            assessment["overall_risk_score"] = round(overall_score, 2)
            assessment["overall_risk_level"] = self._score_to_level(overall_score).value

        self.risk_assessments.append(assessment)
        return assessment

    def _score_to_level(self, score: float) -> RiskLevel:
        """Converte score numérico para nível de risco."""
        if score < 0.25:
            return RiskLevel.LOW
        elif score < 0.5:
            return RiskLevel.MEDIUM
        elif score < 0.75:
            return RiskLevel.HIGH
        else:
            return RiskLevel.CRITICAL

    def simulate_scenario(self, scenario_name: str, 
                         initial_conditions: Dict[str, Any],
                         risk_factors: Dict[str, float]) -> Dict[str, Any]:
        """Simula um cenário de risco."""
        scenario = {
            "name": scenario_name,
            "timestamp": datetime.now().isoformat(),
            "initial_conditions": initial_conditions,
            "risk_assessment": self.assess_risk(risk_factors),
            "outcomes": [],
            "probability": 0.0
        }

        # Gerar possíveis resultados
        scenario["outcomes"] = self._generate_outcomes(scenario_name, risk_factors)
        
        # Calcular probabilidade
        scenario["probability"] = self._calculate_probability(risk_factors)

        self.scenarios.append(scenario)
        return scenario

    def _generate_outcomes(self, scenario_name: str, 
                          risk_factors: Dict[str, float]) -> List[Dict[str, Any]]:
        """Gera possíveis resultados de um cenário."""
        outcomes = []
        
        # Resultado pessimista
        outcomes.append({
            "type": "pessimistic",
            "description": f"Cenário pessimista para {scenario_name}",
            "impact": "high",
            "probability": 0.2
        })
        
        # Resultado realista
        outcomes.append({
            "type": "realistic",
            "description": f"Cenário realista para {scenario_name}",
            "impact": "medium",
            "probability": 0.6
        })
        
        # Resultado otimista
        outcomes.append({
            "type": "optimistic",
            "description": f"Cenário otimista para {scenario_name}",
            "impact": "low",
            "probability": 0.2
        })
        
        return outcomes

    def _calculate_probability(self, risk_factors: Dict[str, float]) -> float:
        """Calcula a probabilidade de um cenário."""
        if not risk_factors:
            return 0.0
        
        avg_risk = sum(risk_factors.values()) / len(risk_factors)
        return round(avg_risk, 2)

    def recommend_mitigation(self, risk_assessment: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Recomenda estratégias de mitigação."""
        recommendations = []
        
        risk_level = risk_assessment.get("overall_risk_level")
        risk_score = risk_assessment.get("overall_risk_score", 0)

        if risk_level == RiskLevel.CRITICAL.value:
            recommendations.append({
                "priority": "critical",
                "action": "Implementar medidas de contenção imediatas",
                "timeline": "imediato"
            })
        
        if risk_level in [RiskLevel.HIGH.value, RiskLevel.CRITICAL.value]:
            recommendations.append({
                "priority": "high",
                "action": "Aumentar monitoramento e vigilância",
                "timeline": "24 horas"
            })
        
        if risk_score > 0.5:
            recommendations.append({
                "priority": "medium",
                "action": "Revisar e atualizar planos de contingência",
                "timeline": "1 semana"
            })
        
        recommendations.append({
            "priority": "low",
            "action": "Documentar lições aprendidas",
            "timeline": "contínuo"
        })

        return recommendations

    def analyze_risk_trends(self) -> Dict[str, Any]:
        """Analisa tendências de risco ao longo do tempo."""
        if not self.risk_assessments:
            return {"error": "Sem dados de avaliação"}

        risk_scores = [a["overall_risk_score"] for a in self.risk_assessments]
        
        trend = "stable"
        if len(risk_scores) > 1:
            if risk_scores[-1] > risk_scores[-2]:
                trend = "increasing"
            elif risk_scores[-1] < risk_scores[-2]:
                trend = "decreasing"

        return {
            "total_assessments": len(self.risk_assessments),
            "current_risk_score": risk_scores[-1] if risk_scores else 0,
            "average_risk_score": sum(risk_scores) / len(risk_scores) if risk_scores else 0,
            "trend": trend,
            "max_risk_score": max(risk_scores) if risk_scores else 0,
            "min_risk_score": min(risk_scores) if risk_scores else 0
        }

    def get_risk_report(self) -> Dict[str, Any]:
        """Gera um relatório completo de risco."""
        latest_assessment = self.risk_assessments[-1] if self.risk_assessments else None
        
        report = {
            "generated_at": datetime.now().isoformat(),
            "total_assessments": len(self.risk_assessments),
            "total_scenarios": len(self.scenarios),
            "current_assessment": latest_assessment,
            "trends": self.analyze_risk_trends(),
            "recent_scenarios": self.scenarios[-5:] if self.scenarios else [],
            "recommendations": self.recommend_mitigation(latest_assessment) if latest_assessment else []
        }

        return report

    def export_risk_analysis(self) -> Dict[str, Any]:
        """Exporta análise de risco completa."""
        return {
            "assessments": self.risk_assessments,
            "scenarios": self.scenarios,
            "trends": self.analyze_risk_trends(),
            "report": self.get_risk_report()
        }


if __name__ == "__main__":
    analyzer = RiskAnalyzer()

    # Exemplo de avaliação de risco
    risk_factors = {
        "market_volatility": 0.7,
        "operational_risk": 0.4,
        "security_risk": 0.3,
        "compliance_risk": 0.2
    }

    assessment = analyzer.assess_risk(risk_factors)
    print("Avaliação de Risco:")
    print(json.dumps(assessment, indent=2, ensure_ascii=False))

    # Simular cenário
    scenario = analyzer.simulate_scenario(
        "Falha de Sistema",
        {"uptime": 0.99, "redundancy": "ativa"},
        risk_factors
    )
    print("\nCenário Simulado:")
    print(json.dumps(scenario, indent=2, ensure_ascii=False, default=str))

    # Recomendações de mitigação
    recommendations = analyzer.recommend_mitigation(assessment)
    print("\nRecomendações de Mitigação:")
    print(json.dumps(recommendations, indent=2, ensure_ascii=False))

    # Relatório
    report = analyzer.get_risk_report()
    print("\nRelatório de Risco:")
    print(json.dumps(report, indent=2, ensure_ascii=False, default=str))
