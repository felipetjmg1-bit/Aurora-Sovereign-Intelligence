# aurora_core/reasoning_engine.py

import json
from typing import Dict, List, Any, Optional
from datetime import datetime


class ReasoningEngine:
    """
    Motor de raciocínio contextual para análise e processamento lógico.
    Responsável por aplicar lógica dedutiva e indutiva aos dados.
    """

    def __init__(self):
        self.reasoning_history = []
        self.context_stack = []
        self.inference_rules = {}
        print("Motor de Raciocínio Contextual inicializado.")

    def add_context(self, context: Dict[str, Any]) -> None:
        """Adiciona contexto à pilha de contexto."""
        self.context_stack.append({
            "timestamp": datetime.now().isoformat(),
            "data": context
        })

    def get_current_context(self) -> Optional[Dict[str, Any]]:
        """Retorna o contexto atual."""
        if self.context_stack:
            return self.context_stack[-1]["data"]
        return None

    def add_inference_rule(self, rule_name: str, rule_logic: callable) -> None:
        """Registra uma regra de inferência."""
        self.inference_rules[rule_name] = rule_logic

    def apply_reasoning(self, premises: List[str], query: str) -> Dict[str, Any]:
        """
        Aplica raciocínio lógico sobre premissas para responder uma consulta.
        """
        reasoning_result = {
            "query": query,
            "premises": premises,
            "timestamp": datetime.now().isoformat(),
            "conclusion": None,
            "confidence": 0.0,
            "reasoning_steps": []
        }

        # Análise de premissas
        for i, premise in enumerate(premises):
            step = {
                "step": i + 1,
                "premise": premise,
                "analysis": self._analyze_premise(premise)
            }
            reasoning_result["reasoning_steps"].append(step)

        # Geração de conclusão
        conclusion = self._generate_conclusion(premises, query)
        reasoning_result["conclusion"] = conclusion
        reasoning_result["confidence"] = self._calculate_confidence(premises)

        self.reasoning_history.append(reasoning_result)
        return reasoning_result

    def _analyze_premise(self, premise: str) -> str:
        """Analisa uma premissa individual."""
        # Lógica simples de análise
        if any(keyword in premise.lower() for keyword in ["se", "então", "porque"]):
            return "Premissa lógica condicional detectada"
        elif any(keyword in premise.lower() for keyword in ["e", "ou", "não"]):
            return "Premissa lógica booleana detectada"
        else:
            return "Premissa factual detectada"

    def _generate_conclusion(self, premises: List[str], query: str) -> str:
        """Gera uma conclusão baseada nas premissas."""
        if not premises:
            return "Sem premissas suficientes para conclusão"

        # Lógica de geração de conclusão
        combined_premises = " ".join(premises).lower()
        if "não" in combined_premises:
            return f"Conclusão negativa para: {query}"
        else:
            return f"Conclusão afirmativa para: {query}"

    def _calculate_confidence(self, premises: List[str]) -> float:
        """Calcula o nível de confiança da conclusão."""
        # Quanto mais premissas, maior a confiança
        confidence = min(len(premises) * 0.2, 0.95)
        return round(confidence, 2)

    def get_reasoning_history(self) -> List[Dict[str, Any]]:
        """Retorna o histórico de raciocínios."""
        return self.reasoning_history

    def clear_context(self) -> None:
        """Limpa a pilha de contexto."""
        self.context_stack = []

    def export_reasoning_state(self) -> Dict[str, Any]:
        """Exporta o estado atual do motor de raciocínio."""
        return {
            "context_depth": len(self.context_stack),
            "reasoning_count": len(self.reasoning_history),
            "registered_rules": list(self.inference_rules.keys()),
            "last_reasoning": self.reasoning_history[-1] if self.reasoning_history else None
        }


if __name__ == "__main__":
    engine = ReasoningEngine()
    
    # Exemplo de uso
    engine.add_context({"user": "admin", "session_id": "sess_001"})
    
    premises = [
        "Se o sistema está operacional, então pode processar dados",
        "O sistema está operacional",
        "Portanto, o sistema pode processar dados"
    ]
    
    result = engine.apply_reasoning(premises, "O sistema pode processar dados?")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    print("\nEstado do Motor:")
    print(json.dumps(engine.export_reasoning_state(), indent=2, ensure_ascii=False))
