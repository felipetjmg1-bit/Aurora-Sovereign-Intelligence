# agents/research_agent.py

import json
from typing import Dict, List, Any, Optional
from datetime import datetime


class ResearchAgent:
    """
    Agente de Pesquisa para coleta, análise e síntese de informações.
    Responsável por buscar dados de múltiplas fontes e gerar relatórios.
    """

    def __init__(self, agent_id: str = "research_agent_001"):
        self.agent_id = agent_id
        self.research_history = []
        self.data_sources = []
        self.active_tasks = {}
        print(f"Agente de Pesquisa {agent_id} inicializado.")

    def register_data_source(self, source_name: str, source_config: Dict[str, Any]) -> bool:
        """Registra uma fonte de dados."""
        self.data_sources.append({
            "name": source_name,
            "config": source_config,
            "registered_at": datetime.now().isoformat()
        })
        return True

    def collect_data(self, query: str, sources: Optional[List[str]] = None) -> Dict[str, Any]:
        """Coleta dados de fontes especificadas."""
        collection_result = {
            "query": query,
            "timestamp": datetime.now().isoformat(),
            "sources_queried": sources or [s["name"] for s in self.data_sources],
            "data_collected": [],
            "total_records": 0
        }

        # Simular coleta de dados
        for source in self.data_sources:
            if sources is None or source["name"] in sources:
                # Simulação de coleta
                data = self._simulate_data_collection(query, source["name"])
                collection_result["data_collected"].append({
                    "source": source["name"],
                    "records": data,
                    "count": len(data)
                })
                collection_result["total_records"] += len(data)

        self.research_history.append(collection_result)
        return collection_result

    def _simulate_data_collection(self, query: str, source: str) -> List[Dict[str, Any]]:
        """Simula coleta de dados de uma fonte."""
        # Simulação básica
        return [
            {
                "id": f"{source}_{i}",
                "source": source,
                "query": query,
                "timestamp": datetime.now().isoformat(),
                "relevance": 0.8 - (i * 0.1)
            }
            for i in range(3)
        ]

    def analyze_data(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analisa dados coletados."""
        analysis = {
            "timestamp": datetime.now().isoformat(),
            "total_records": len(data),
            "sources": set(),
            "patterns": [],
            "insights": [],
            "quality_score": 0.0
        }

        if not data:
            return analysis

        # Extrair fontes
        analysis["sources"] = list(set(record.get("source") for record in data if "source" in record))

        # Detectar padrões
        analysis["patterns"] = self._detect_patterns(data)

        # Gerar insights
        analysis["insights"] = self._generate_insights(data, analysis["patterns"])

        # Calcular score de qualidade
        analysis["quality_score"] = self._calculate_quality_score(data)

        return analysis

    def _detect_patterns(self, data: List[Dict[str, Any]]) -> List[str]:
        """Detecta padrões nos dados."""
        patterns = []
        
        if len(data) > 5:
            patterns.append("Volume alto de dados")
        
        sources = set(record.get("source") for record in data if "source" in record)
        if len(sources) > 1:
            patterns.append(f"Dados de múltiplas fontes ({len(sources)})")
        
        return patterns

    def _generate_insights(self, data: List[Dict[str, Any]], patterns: List[str]) -> List[str]:
        """Gera insights a partir dos dados."""
        insights = []
        
        if patterns:
            insights.append(f"Padrões detectados: {', '.join(patterns)}")
        
        avg_relevance = sum(
            record.get("relevance", 0) for record in data
        ) / max(len(data), 1)
        
        insights.append(f"Relevância média: {avg_relevance:.2%}")
        
        return insights

    def _calculate_quality_score(self, data: List[Dict[str, Any]]) -> float:
        """Calcula o score de qualidade dos dados."""
        if not data:
            return 0.0
        
        avg_relevance = sum(
            record.get("relevance", 0.5) for record in data
        ) / len(data)
        
        return round(avg_relevance, 2)

    def generate_report(self, title: str, data: List[Dict[str, Any]], 
                       analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Gera um relatório de pesquisa."""
        report = {
            "title": title,
            "agent_id": self.agent_id,
            "generated_at": datetime.now().isoformat(),
            "summary": {
                "total_records": len(data),
                "quality_score": analysis.get("quality_score", 0),
                "sources": analysis.get("sources", []),
                "patterns": analysis.get("patterns", []),
                "insights": analysis.get("insights", [])
            },
            "data_sample": data[:5] if data else []
        }
        
        return report

    def get_research_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Retorna o histórico de pesquisas."""
        return self.research_history[-limit:]

    def get_agent_status(self) -> Dict[str, Any]:
        """Retorna o status do agente."""
        return {
            "agent_id": self.agent_id,
            "data_sources": len(self.data_sources),
            "research_count": len(self.research_history),
            "active_tasks": len(self.active_tasks),
            "status": "operational"
        }


if __name__ == "__main__":
    agent = ResearchAgent()
    
    # Registrar fontes de dados
    agent.register_data_source("api_news", {"url": "https://api.example.com/news"})
    agent.register_data_source("database", {"host": "localhost", "db": "aurora"})
    
    # Coletar dados
    collection = agent.collect_data("inteligência artificial")
    print("Coleta de dados:")
    print(json.dumps(collection, indent=2, ensure_ascii=False, default=str))
    
    # Analisar dados
    analysis = agent.analyze_data(collection["data_collected"][0]["records"])
    print("\nAnálise:")
    print(json.dumps(analysis, indent=2, ensure_ascii=False, default=str))
    
    # Gerar relatório
    report = agent.generate_report("Pesquisa sobre IA", 
                                  collection["data_collected"][0]["records"], 
                                  analysis)
    print("\nRelatório:")
    print(json.dumps(report, indent=2, ensure_ascii=False, default=str))
