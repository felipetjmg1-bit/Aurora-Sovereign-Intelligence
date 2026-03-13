# memory/knowledge_graph.py

import json
from typing import Dict, List, Any, Optional, Set, Tuple
from datetime import datetime


class KnowledgeGraph:
    """
    Grafo de Conhecimento para representação de relações entre entidades.
    Implementa operações de busca, traversal e análise de relações.
    """

    def __init__(self):
        self.nodes = {}  # {node_id: {"label": str, "properties": dict, "created_at": str}}
        self.edges = {}  # {edge_id: {"source": str, "target": str, "relation": str, "properties": dict}}
        self.adjacency_list = {}  # Para busca rápida
        print("Grafo de Conhecimento inicializado.")

    def add_node(self, node_id: str, label: str, 
                 properties: Optional[Dict[str, Any]] = None) -> bool:
        """Adiciona um nó ao grafo."""
        if node_id in self.nodes:
            return False
        
        self.nodes[node_id] = {
            "label": label,
            "properties": properties or {},
            "created_at": datetime.now().isoformat()
        }
        
        self.adjacency_list[node_id] = []
        
        return True

    def add_edge(self, source_id: str, target_id: str, relation: str,
                 properties: Optional[Dict[str, Any]] = None) -> str:
        """Adiciona uma aresta (relação) entre dois nós."""
        if source_id not in self.nodes or target_id not in self.nodes:
            return ""
        
        edge_id = f"{source_id}_{relation}_{target_id}"
        
        self.edges[edge_id] = {
            "source": source_id,
            "target": target_id,
            "relation": relation,
            "properties": properties or {},
            "created_at": datetime.now().isoformat()
        }
        
        self.adjacency_list[source_id].append({
            "target": target_id,
            "relation": relation,
            "edge_id": edge_id
        })
        
        return edge_id

    def get_node(self, node_id: str) -> Optional[Dict[str, Any]]:
        """Recupera informações de um nó."""
        return self.nodes.get(node_id)

    def get_edge(self, edge_id: str) -> Optional[Dict[str, Any]]:
        """Recupera informações de uma aresta."""
        return self.edges.get(edge_id)

    def get_neighbors(self, node_id: str, relation: Optional[str] = None) -> List[str]:
        """Retorna os vizinhos de um nó."""
        if node_id not in self.adjacency_list:
            return []
        
        neighbors = []
        for connection in self.adjacency_list[node_id]:
            if relation is None or connection["relation"] == relation:
                neighbors.append(connection["target"])
        
        return neighbors

    def find_path(self, source_id: str, target_id: str, max_depth: int = 5) -> Optional[List[str]]:
        """Encontra um caminho entre dois nós usando BFS."""
        if source_id not in self.nodes or target_id not in self.nodes:
            return None
        
        if source_id == target_id:
            return [source_id]
        
        queue = [(source_id, [source_id])]
        visited = {source_id}
        
        while queue:
            current, path = queue.pop(0)
            
            if len(path) > max_depth:
                continue
            
            for neighbor in self.get_neighbors(current):
                if neighbor == target_id:
                    return path + [neighbor]
                
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        
        return None

    def get_related_entities(self, node_id: str, relation_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """Retorna entidades relacionadas com suas propriedades."""
        related = []
        
        for connection in self.adjacency_list.get(node_id, []):
            if relation_type is None or connection["relation"] == relation_type:
                target_id = connection["target"]
                target_node = self.nodes[target_id]
                
                related.append({
                    "node_id": target_id,
                    "label": target_node["label"],
                    "relation": connection["relation"],
                    "properties": target_node["properties"]
                })
        
        return related

    def get_statistics(self) -> Dict[str, Any]:
        """Retorna estatísticas do grafo."""
        total_edges = len(self.edges)
        
        relation_types = {}
        for edge in self.edges.values():
            relation = edge["relation"]
            relation_types[relation] = relation_types.get(relation, 0) + 1
        
        return {
            "total_nodes": len(self.nodes),
            "total_edges": total_edges,
            "relation_types": relation_types,
            "average_connections": total_edges / max(len(self.nodes), 1)
        }

    def export_graph(self) -> Dict[str, Any]:
        """Exporta o grafo completo."""
        return {
            "nodes": self.nodes,
            "edges": self.edges,
            "statistics": self.get_statistics()
        }

    def delete_node(self, node_id: str) -> bool:
        """Remove um nó do grafo."""
        if node_id not in self.nodes:
            return False
        
        # Remover arestas conectadas
        edges_to_remove = [
            edge_id for edge_id, edge in self.edges.items()
            if edge["source"] == node_id or edge["target"] == node_id
        ]
        
        for edge_id in edges_to_remove:
            del self.edges[edge_id]
        
        # Remover do grafo de adjacência
        del self.adjacency_list[node_id]
        
        # Remover referências de outros nós
        for neighbors in self.adjacency_list.values():
            neighbors[:] = [n for n in neighbors if n["target"] != node_id]
        
        del self.nodes[node_id]
        
        return True

    def clear(self) -> None:
        """Limpa o grafo."""
        self.nodes.clear()
        self.edges.clear()
        self.adjacency_list.clear()


if __name__ == "__main__":
    graph = KnowledgeGraph()
    
    # Exemplo de uso
    graph.add_node("aurora", "Sistema", {"version": "1.0"})
    graph.add_node("engine", "Motor", {"type": "core"})
    graph.add_node("agent", "Agente", {"type": "inteligente"})
    graph.add_node("memory", "Memória", {"type": "cognitiva"})
    
    graph.add_edge("aurora", "engine", "contém")
    graph.add_edge("aurora", "agent", "utiliza")
    graph.add_edge("engine", "memory", "acessa")
    
    # Buscar vizinhos
    neighbors = graph.get_neighbors("aurora")
    print(f"Vizinhos de 'aurora': {neighbors}")
    
    # Encontrar caminho
    path = graph.find_path("aurora", "memory")
    print(f"Caminho de 'aurora' para 'memory': {path}")
    
    # Entidades relacionadas
    related = graph.get_related_entities("aurora")
    print(f"\nEntidades relacionadas a 'aurora':")
    print(json.dumps(related, indent=2, ensure_ascii=False))
    
    # Estatísticas
    print(f"\nEstatísticas do grafo:")
    print(json.dumps(graph.get_statistics(), indent=2, ensure_ascii=False))
