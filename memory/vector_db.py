# memory/vector_db.py

import json
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import math


class VectorDB:
    """
    Banco de Dados Vetorial para armazenamento e recuperação de embeddings.
    Implementa operações de similaridade e indexação semântica.
    """

    def __init__(self, dimension: int = 384, max_vectors: int = 10000):
        self.dimension = dimension
        self.max_vectors = max_vectors
        self.vectors = {}
        self.metadata = {}
        self.index = []
        print(f"Banco de Dados Vetorial inicializado (dimensão: {dimension}).")

    def add_vector(self, vector_id: str, vector: List[float], 
                   metadata: Optional[Dict[str, Any]] = None) -> bool:
        """Adiciona um novo vetor ao banco."""
        if len(self.vectors) >= self.max_vectors:
            return False
        
        if len(vector) != self.dimension:
            return False
        
        self.vectors[vector_id] = vector
        self.metadata[vector_id] = metadata or {}
        self.metadata[vector_id]["added_at"] = datetime.now().isoformat()
        self.index.append(vector_id)
        
        return True

    def get_vector(self, vector_id: str) -> Optional[List[float]]:
        """Recupera um vetor pelo ID."""
        return self.vectors.get(vector_id)

    def get_metadata(self, vector_id: str) -> Optional[Dict[str, Any]]:
        """Recupera metadados de um vetor."""
        return self.metadata.get(vector_id)

    def similarity_search(self, query_vector: List[float], 
                         top_k: int = 5) -> List[Tuple[str, float]]:
        """
        Busca os k vetores mais similares a um vetor de consulta.
        Usa similaridade de cosseno.
        """
        if len(query_vector) != self.dimension:
            return []
        
        similarities = []
        
        for vector_id in self.index:
            stored_vector = self.vectors[vector_id]
            similarity = self._cosine_similarity(query_vector, stored_vector)
            similarities.append((vector_id, similarity))
        
        # Ordenar por similaridade decrescente
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        return similarities[:top_k]

    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """Calcula similaridade de cosseno entre dois vetores."""
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        
        magnitude1 = math.sqrt(sum(a * a for a in vec1))
        magnitude2 = math.sqrt(sum(b * b for b in vec2))
        
        if magnitude1 == 0 or magnitude2 == 0:
            return 0.0
        
        return dot_product / (magnitude1 * magnitude2)

    def delete_vector(self, vector_id: str) -> bool:
        """Remove um vetor do banco."""
        if vector_id not in self.vectors:
            return False
        
        del self.vectors[vector_id]
        del self.metadata[vector_id]
        self.index.remove(vector_id)
        
        return True

    def batch_add_vectors(self, vectors: Dict[str, Tuple[List[float], Dict[str, Any]]]) -> int:
        """Adiciona múltiplos vetores em lote."""
        count = 0
        for vector_id, (vector, metadata) in vectors.items():
            if self.add_vector(vector_id, vector, metadata):
                count += 1
        
        return count

    def get_statistics(self) -> Dict[str, Any]:
        """Retorna estatísticas do banco vetorial."""
        return {
            "total_vectors": len(self.vectors),
            "dimension": self.dimension,
            "max_capacity": self.max_vectors,
            "utilization": round(len(self.vectors) / self.max_vectors * 100, 2)
        }

    def export_vectors(self) -> Dict[str, Any]:
        """Exporta todos os vetores e metadados."""
        return {
            "vectors": self.vectors,
            "metadata": self.metadata,
            "statistics": self.get_statistics()
        }

    def clear(self) -> None:
        """Limpa o banco de dados."""
        self.vectors.clear()
        self.metadata.clear()
        self.index.clear()


if __name__ == "__main__":
    db = VectorDB(dimension=3)
    
    # Exemplo de uso
    db.add_vector("vec1", [1.0, 0.0, 0.0], {"label": "Vetor 1"})
    db.add_vector("vec2", [0.9, 0.1, 0.0], {"label": "Vetor 2"})
    db.add_vector("vec3", [0.0, 1.0, 0.0], {"label": "Vetor 3"})
    db.add_vector("vec4", [0.0, 0.0, 1.0], {"label": "Vetor 4"})
    
    # Busca por similaridade
    query = [1.0, 0.0, 0.0]
    results = db.similarity_search(query, top_k=3)
    
    print("Resultados da busca por similaridade:")
    for vector_id, similarity in results:
        metadata = db.get_metadata(vector_id)
        print(f"  {vector_id}: similaridade={similarity:.4f}, {metadata}")
    
    print("\nEstatísticas:")
    print(json.dumps(db.get_statistics(), indent=2, ensure_ascii=False))
