# data_ingestion/api_collectors.py

import json
from typing import Dict, List, Any, Optional
from datetime import datetime


class APICollector:
    """
    Coletor de API para integração com fontes de dados externas.
    Responsável por requisições, tratamento de erros e cache.
    """

    def __init__(self, api_name: str, base_url: str):
        self.api_name = api_name
        self.base_url = base_url
        self.cache = {}
        self.collection_history = []
        self.rate_limit = 100
        self.requests_made = 0
        print(f"Coletor de API {api_name} inicializado.")

    def collect_data(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Coleta dados de um endpoint da API."""
        # Verificar rate limit
        if self.requests_made >= self.rate_limit:
            return {
                "error": "Rate limit excedido",
                "requests_made": self.requests_made
            }

        # Construir URL
        url = f"{self.base_url}/{endpoint}"
        cache_key = f"{url}:{json.dumps(params or {})}"

        # Verificar cache
        if cache_key in self.cache:
            return {
                "status": "cached",
                "data": self.cache[cache_key],
                "timestamp": datetime.now().isoformat()
            }

        # Simular requisição
        response = self._simulate_api_request(url, params)

        # Armazenar em cache
        if response.get("status") == "success":
            self.cache[cache_key] = response["data"]

        self.requests_made += 1

        # Registrar no histórico
        self.collection_history.append({
            "timestamp": datetime.now().isoformat(),
            "endpoint": endpoint,
            "status": response.get("status"),
            "records_collected": len(response.get("data", []))
        })

        return response

    def _simulate_api_request(self, url: str, params: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Simula uma requisição de API."""
        # Simulação básica
        return {
            "status": "success",
            "url": url,
            "params": params,
            "data": [
                {
                    "id": f"record_{i}",
                    "api": self.api_name,
                    "timestamp": datetime.now().isoformat(),
                    "value": f"Dado {i} de {self.api_name}"
                }
                for i in range(3)
            ]
        }

    def batch_collect(self, endpoints: List[str]) -> List[Dict[str, Any]]:
        """Coleta dados de múltiplos endpoints."""
        results = []
        for endpoint in endpoints:
            result = self.collect_data(endpoint)
            results.append(result)
        return results

    def clear_cache(self) -> None:
        """Limpa o cache."""
        self.cache.clear()

    def get_statistics(self) -> Dict[str, Any]:
        """Retorna estatísticas do coletor."""
        return {
            "api_name": self.api_name,
            "requests_made": self.requests_made,
            "rate_limit": self.rate_limit,
            "cache_size": len(self.cache),
            "collections": len(self.collection_history)
        }

    def export_collection_history(self) -> List[Dict[str, Any]]:
        """Exporta histórico de coleta."""
        return self.collection_history


class MultiSourceCollector:
    """
    Coletor Multi-Fonte para integração de múltiplas APIs.
    """

    def __init__(self):
        self.collectors = {}
        self.aggregated_data = []
        print("Coletor Multi-Fonte inicializado.")

    def register_api(self, api_name: str, base_url: str) -> bool:
        """Registra uma nova API."""
        if api_name not in self.collectors:
            self.collectors[api_name] = APICollector(api_name, base_url)
            return True
        return False

    def collect_from_all(self, endpoint: str) -> Dict[str, Any]:
        """Coleta dados de todas as APIs registradas."""
        aggregated = {
            "timestamp": datetime.now().isoformat(),
            "endpoint": endpoint,
            "sources": {},
            "total_records": 0
        }

        for api_name, collector in self.collectors.items():
            result = collector.collect_data(endpoint)
            aggregated["sources"][api_name] = result
            
            if result.get("status") == "success":
                aggregated["total_records"] += len(result.get("data", []))

        self.aggregated_data.append(aggregated)
        return aggregated

    def get_aggregated_statistics(self) -> Dict[str, Any]:
        """Retorna estatísticas agregadas."""
        stats = {
            "total_apis": len(self.collectors),
            "total_collections": len(self.aggregated_data),
            "apis": {}
        }

        for api_name, collector in self.collectors.items():
            stats["apis"][api_name] = collector.get_statistics()

        return stats

    def export_aggregated_data(self) -> Dict[str, Any]:
        """Exporta dados agregados."""
        return {
            "collections": self.aggregated_data,
            "statistics": self.get_aggregated_statistics()
        }


if __name__ == "__main__":
    # Exemplo com coletor único
    collector = APICollector("news_api", "https://api.example.com")

    result = collector.collect_data("latest", {"category": "tech"})
    print("Coleta de Dados:")
    print(json.dumps(result, indent=2, ensure_ascii=False, default=str))

    print("\nEstatísticas:")
    print(json.dumps(collector.get_statistics(), indent=2, ensure_ascii=False))

    # Exemplo com multi-fonte
    multi_collector = MultiSourceCollector()
    multi_collector.register_api("news_api", "https://newsapi.example.com")
    multi_collector.register_api("social_api", "https://social.example.com")

    aggregated = multi_collector.collect_from_all("trending")
    print("\nDados Agregados:")
    print(json.dumps(aggregated, indent=2, ensure_ascii=False, default=str))

    print("\nEstatísticas Agregadas:")
    print(json.dumps(multi_collector.get_aggregated_statistics(), indent=2, ensure_ascii=False))
