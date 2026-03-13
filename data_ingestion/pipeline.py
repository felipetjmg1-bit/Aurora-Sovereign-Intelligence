# data_ingestion/pipeline.py

import json
from typing import Dict, List, Any, Callable, Optional
from datetime import datetime


class DataPipeline:
    """
    Pipeline de Processamento de Dados para limpeza, transformação e normalização.
    Implementa operações de ETL (Extract, Transform, Load).
    """

    def __init__(self, pipeline_name: str = "default_pipeline"):
        self.pipeline_name = pipeline_name
        self.stages = []
        self.processing_history = []
        self.transformations = {}
        print(f"Pipeline de Dados {pipeline_name} inicializado.")

    def add_stage(self, stage_name: str, processor: Callable) -> bool:
        """Adiciona um estágio ao pipeline."""
        self.stages.append({
            "name": stage_name,
            "processor": processor,
            "added_at": datetime.now().isoformat()
        })
        return True

    def clean_data(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Remove dados inválidos ou incompletos."""
        cleaned = []
        
        for record in data:
            if self._is_valid_record(record):
                cleaned.append(record)

        return cleaned

    def _is_valid_record(self, record: Dict[str, Any]) -> bool:
        """Verifica se um registro é válido."""
        if not isinstance(record, dict):
            return False
        
        if not record:  # Registro vazio
            return False
        
        return True

    def normalize_data(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Normaliza dados para formato padrão."""
        normalized = []
        
        for record in data:
            normalized_record = {
                "id": record.get("id", f"record_{len(normalized)}"),
                "timestamp": record.get("timestamp", datetime.now().isoformat()),
                "source": record.get("source", "unknown"),
                "data": record
            }
            normalized.append(normalized_record)

        return normalized

    def transform_data(self, data: List[Dict[str, Any]], 
                      transformations: Optional[Dict[str, Callable]] = None) -> List[Dict[str, Any]]:
        """Aplica transformações aos dados."""
        transformed = []
        
        for record in data:
            transformed_record = record.copy()
            
            if transformations:
                for field, transform_func in transformations.items():
                    if field in transformed_record:
                        try:
                            transformed_record[field] = transform_func(transformed_record[field])
                        except Exception as e:
                            print(f"Erro ao transformar {field}: {e}")
            
            transformed.append(transformed_record)

        return transformed

    def deduplicate_data(self, data: List[Dict[str, Any]], 
                        key_field: str = "id") -> List[Dict[str, Any]]:
        """Remove duplicatas baseado em um campo chave."""
        seen = set()
        deduplicated = []
        
        for record in data:
            key = record.get(key_field)
            if key not in seen:
                seen.add(key)
                deduplicated.append(record)

        return deduplicated

    def process(self, raw_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Executa o pipeline completo de processamento."""
        processing_result = {
            "pipeline_name": self.pipeline_name,
            "timestamp": datetime.now().isoformat(),
            "input_records": len(raw_data),
            "stages_executed": [],
            "output_records": 0,
            "output_data": []
        }

        current_data = raw_data

        # Estágio 1: Limpeza
        cleaned = self.clean_data(current_data)
        processing_result["stages_executed"].append({
            "stage": "clean",
            "input": len(current_data),
            "output": len(cleaned)
        })
        current_data = cleaned

        # Estágio 2: Normalização
        normalized = self.normalize_data(current_data)
        processing_result["stages_executed"].append({
            "stage": "normalize",
            "input": len(current_data),
            "output": len(normalized)
        })
        current_data = normalized

        # Estágio 3: Deduplicação
        deduplicated = self.deduplicate_data(current_data)
        processing_result["stages_executed"].append({
            "stage": "deduplicate",
            "input": len(current_data),
            "output": len(deduplicated)
        })
        current_data = deduplicated

        # Estágio 4: Transformações customizadas
        if self.transformations:
            transformed = self.transform_data(current_data, self.transformations)
            processing_result["stages_executed"].append({
                "stage": "transform",
                "input": len(current_data),
                "output": len(transformed)
            })
            current_data = transformed

        processing_result["output_records"] = len(current_data)
        processing_result["output_data"] = current_data

        self.processing_history.append(processing_result)

        return processing_result

    def add_transformation(self, field_name: str, transform_func: Callable) -> bool:
        """Registra uma transformação customizada."""
        self.transformations[field_name] = transform_func
        return True

    def get_pipeline_statistics(self) -> Dict[str, Any]:
        """Retorna estatísticas do pipeline."""
        if not self.processing_history:
            return {"error": "Nenhum processamento realizado"}

        total_input = sum(p["input_records"] for p in self.processing_history)
        total_output = sum(p["output_records"] for p in self.processing_history)

        return {
            "pipeline_name": self.pipeline_name,
            "total_executions": len(self.processing_history),
            "total_input_records": total_input,
            "total_output_records": total_output,
            "reduction_rate": round((1 - total_output / total_input) * 100, 2) if total_input > 0 else 0
        }

    def export_processing_history(self) -> List[Dict[str, Any]]:
        """Exporta histórico de processamento."""
        return self.processing_history


if __name__ == "__main__":
    pipeline = DataPipeline("data_cleaning_pipeline")

    # Dados de exemplo
    raw_data = [
        {"id": "1", "name": "Item 1", "value": 100},
        {"id": "2", "name": "Item 2", "value": 200},
        {"id": "1", "name": "Item 1", "value": 100},  # Duplicata
        {},  # Registro vazio
        {"id": "3", "name": "Item 3", "value": 300},
    ]

    # Adicionar transformação
    pipeline.add_transformation("value", lambda x: int(x) * 1.1)  # Aumentar 10%

    # Processar dados
    result = pipeline.process(raw_data)

    print("Resultado do Pipeline:")
    print(json.dumps(result, indent=2, ensure_ascii=False, default=str))

    print("\nEstatísticas:")
    print(json.dumps(pipeline.get_pipeline_statistics(), indent=2, ensure_ascii=False))
