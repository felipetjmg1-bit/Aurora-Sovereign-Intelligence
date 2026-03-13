# agents/analysis_agent.py

import json
from typing import Dict, List, Any, Optional
from datetime import datetime


class AnalysisAgent:
    """
    Agente de Análise para processamento profundo de dados e geração de insights.
    Responsável por análise estatística, detecção de anomalias e correlações.
    """

    def __init__(self, agent_id: str = "analysis_agent_001"):
        self.agent_id = agent_id
        self.analysis_results = []
        self.anomalies_detected = []
        print(f"Agente de Análise {agent_id} inicializado.")

    def statistical_analysis(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Realiza análise estatística dos dados."""
        if not data:
            return {"error": "Dados vazios"}

        analysis = {
            "timestamp": datetime.now().isoformat(),
            "total_records": len(data),
            "statistics": {},
            "distributions": {},
            "summary": ""
        }

        # Extrair valores numéricos
        numeric_fields = self._extract_numeric_fields(data)

        for field, values in numeric_fields.items():
            if values:
                analysis["statistics"][field] = {
                    "mean": sum(values) / len(values),
                    "min": min(values),
                    "max": max(values),
                    "count": len(values)
                }

        analysis["summary"] = f"Análise de {len(data)} registros com {len(numeric_fields)} campos numéricos"

        self.analysis_results.append(analysis)
        return analysis

    def _extract_numeric_fields(self, data: List[Dict[str, Any]]) -> Dict[str, List[float]]:
        """Extrai campos numéricos dos dados."""
        numeric_fields = {}

        for record in data:
            for key, value in record.items():
                if isinstance(value, (int, float)):
                    if key not in numeric_fields:
                        numeric_fields[key] = []
                    numeric_fields[key].append(value)

        return numeric_fields

    def detect_anomalies(self, data: List[Dict[str, Any]], 
                        threshold: float = 2.0) -> List[Dict[str, Any]]:
        """Detecta anomalias nos dados usando desvio padrão."""
        anomalies = []

        numeric_fields = self._extract_numeric_fields(data)

        for field, values in numeric_fields.items():
            if len(values) < 2:
                continue

            mean = sum(values) / len(values)
            variance = sum((x - mean) ** 2 for x in values) / len(values)
            std_dev = variance ** 0.5

            for i, record in enumerate(data):
                if field in record and isinstance(record[field], (int, float)):
                    value = record[field]
                    z_score = abs((value - mean) / std_dev) if std_dev > 0 else 0

                    if z_score > threshold:
                        anomalies.append({
                            "record_index": i,
                            "field": field,
                            "value": value,
                            "z_score": round(z_score, 2),
                            "expected_range": (
                                round(mean - threshold * std_dev, 2),
                                round(mean + threshold * std_dev, 2)
                            )
                        })

        self.anomalies_detected.extend(anomalies)
        return anomalies

    def find_correlations(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Encontra correlações entre campos numéricos."""
        correlations = []

        numeric_fields = self._extract_numeric_fields(data)
        field_names = list(numeric_fields.keys())

        for i, field1 in enumerate(field_names):
            for field2 in field_names[i+1:]:
                correlation = self._calculate_correlation(
                    numeric_fields[field1],
                    numeric_fields[field2]
                )

                if abs(correlation) > 0.5:  # Correlação significativa
                    correlations.append({
                        "field1": field1,
                        "field2": field2,
                        "correlation": round(correlation, 3),
                        "strength": "forte" if abs(correlation) > 0.7 else "moderada"
                    })

        return correlations

    def _calculate_correlation(self, values1: List[float], 
                              values2: List[float]) -> float:
        """Calcula correlação de Pearson entre dois conjuntos de valores."""
        if len(values1) != len(values2) or len(values1) < 2:
            return 0.0

        mean1 = sum(values1) / len(values1)
        mean2 = sum(values2) / len(values2)

        numerator = sum(
            (values1[i] - mean1) * (values2[i] - mean2)
            for i in range(len(values1))
        )

        denominator = (
            (sum((x - mean1) ** 2 for x in values1) ** 0.5) *
            (sum((y - mean2) ** 2 for y in values2) ** 0.5)
        )

        if denominator == 0:
            return 0.0

        return numerator / denominator

    def generate_analysis_report(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Gera um relatório completo de análise."""
        report = {
            "agent_id": self.agent_id,
            "generated_at": datetime.now().isoformat(),
            "data_summary": {
                "total_records": len(data),
                "fields": list(data[0].keys()) if data else []
            },
            "statistical_analysis": self.statistical_analysis(data),
            "anomalies": self.detect_anomalies(data),
            "correlations": self.find_correlations(data),
            "insights": []
        }

        # Gerar insights
        if report["anomalies"]:
            report["insights"].append(
                f"Detectadas {len(report['anomalies'])} anomalias nos dados"
            )

        if report["correlations"]:
            report["insights"].append(
                f"Encontradas {len(report['correlations'])} correlações significativas"
            )

        return report

    def get_analysis_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Retorna o histórico de análises."""
        return self.analysis_results[-limit:]

    def get_agent_status(self) -> Dict[str, Any]:
        """Retorna o status do agente."""
        return {
            "agent_id": self.agent_id,
            "analysis_count": len(self.analysis_results),
            "anomalies_found": len(self.anomalies_detected),
            "status": "operational"
        }


if __name__ == "__main__":
    agent = AnalysisAgent()

    # Dados de exemplo
    sample_data = [
        {"id": 1, "valor": 100, "score": 0.85},
        {"id": 2, "valor": 105, "score": 0.87},
        {"id": 3, "valor": 103, "score": 0.86},
        {"id": 4, "valor": 500, "score": 0.15},  # Anomalia
        {"id": 5, "valor": 102, "score": 0.88},
    ]

    # Gerar relatório
    report = agent.generate_analysis_report(sample_data)

    print("Relatório de Análise:")
    print(json.dumps(report, indent=2, ensure_ascii=False))

    print("\nStatus do Agente:")
    print(json.dumps(agent.get_agent_status(), indent=2, ensure_ascii=False))
