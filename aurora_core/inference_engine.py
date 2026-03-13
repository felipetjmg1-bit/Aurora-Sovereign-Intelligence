# aurora_core/inference_engine.py

import json
from typing import Dict, List, Any, Optional
from datetime import datetime


class InferenceEngine:
    """
    Motor de Inferência para processamento de linguagem natural e geração de insights.
    Utiliza modelos de linguagem para interpretação e geração de respostas.
    """

    def __init__(self, model_name: str = "aurora-v1"):
        self.model_name = model_name
        self.inference_cache = {}
        self.inference_history = []
        self.confidence_threshold = 0.6
        print(f"Motor de Inferência {model_name} inicializado.")

    def infer_from_text(self, text: str, task_type: str = "general") -> Dict[str, Any]:
        """
        Realiza inferência sobre um texto fornecido.
        """
        # Verificar cache
        cache_key = f"{task_type}:{text[:50]}"
        if cache_key in self.inference_cache:
            return self.inference_cache[cache_key]

        inference_result = {
            "input_text": text,
            "task_type": task_type,
            "timestamp": datetime.now().isoformat(),
            "entities": self._extract_entities(text),
            "sentiment": self._analyze_sentiment(text),
            "intent": self._classify_intent(text),
            "key_phrases": self._extract_key_phrases(text),
            "confidence": 0.0,
            "inferred_output": None
        }

        # Calcular confiança
        inference_result["confidence"] = self._calculate_inference_confidence(text)

        # Gerar saída inferida
        inference_result["inferred_output"] = self._generate_inference_output(
            text, task_type, inference_result
        )

        self.inference_cache[cache_key] = inference_result
        self.inference_history.append(inference_result)

        return inference_result

    def _extract_entities(self, text: str) -> List[Dict[str, str]]:
        """Extrai entidades nomeadas do texto."""
        entities = []
        
        # Simulação de extração de entidades
        words = text.split()
        for i, word in enumerate(words):
            if word[0].isupper() and len(word) > 2:
                entities.append({
                    "text": word,
                    "type": "ENTITY",
                    "position": i
                })
        
        return entities

    def _analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """Analisa o sentimento do texto."""
        text_lower = text.lower()
        
        positive_words = ["bom", "excelente", "ótimo", "maravilhoso", "sucesso"]
        negative_words = ["ruim", "péssimo", "horrível", "fracasso", "erro"]
        
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        if positive_count > negative_count:
            sentiment = "positive"
        elif negative_count > positive_count:
            sentiment = "negative"
        else:
            sentiment = "neutral"
        
        return {
            "sentiment": sentiment,
            "positive_score": positive_count,
            "negative_score": negative_count
        }

    def _classify_intent(self, text: str) -> str:
        """Classifica a intenção do texto."""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ["qual", "quando", "onde", "por que", "como"]):
            return "question"
        elif any(word in text_lower for word in ["fazer", "executar", "processar", "analisar"]):
            return "action"
        elif any(word in text_lower for word in ["informar", "avisar", "notificar"]):
            return "notification"
        else:
            return "statement"

    def _extract_key_phrases(self, text: str) -> List[str]:
        """Extrai frases-chave do texto."""
        # Simulação de extração de frases-chave
        words = text.split()
        key_phrases = [
            " ".join(words[i:i+2]) 
            for i in range(len(words)-1) 
            if len(words[i]) > 3
        ]
        return key_phrases[:5]  # Retorna as 5 primeiras

    def _calculate_inference_confidence(self, text: str) -> float:
        """Calcula a confiança da inferência."""
        # Baseado no comprimento e complexidade do texto
        word_count = len(text.split())
        complexity_score = min(word_count / 20, 1.0)
        return round(0.5 + (complexity_score * 0.5), 2)

    def _generate_inference_output(self, text: str, task_type: str, 
                                   inference_data: Dict[str, Any]) -> str:
        """Gera a saída inferida."""
        intent = inference_data["intent"]
        sentiment = inference_data["sentiment"]["sentiment"]
        
        output = f"Inferência ({task_type}): Intenção={intent}, Sentimento={sentiment}"
        return output

    def batch_infer(self, texts: List[str], task_type: str = "general") -> List[Dict[str, Any]]:
        """Realiza inferência em lote."""
        results = []
        for text in texts:
            results.append(self.infer_from_text(text, task_type))
        return results

    def get_inference_statistics(self) -> Dict[str, Any]:
        """Retorna estatísticas de inferência."""
        if not self.inference_history:
            return {"total_inferences": 0}
        
        total = len(self.inference_history)
        avg_confidence = sum(r["confidence"] for r in self.inference_history) / total
        
        return {
            "total_inferences": total,
            "average_confidence": round(avg_confidence, 2),
            "cache_size": len(self.inference_cache),
            "model": self.model_name
        }

    def clear_cache(self) -> None:
        """Limpa o cache de inferências."""
        self.inference_cache.clear()

    def export_inference_state(self) -> Dict[str, Any]:
        """Exporta o estado atual do motor de inferência."""
        return {
            "model": self.model_name,
            "statistics": self.get_inference_statistics(),
            "recent_inferences": self.inference_history[-5:] if self.inference_history else []
        }


if __name__ == "__main__":
    engine = InferenceEngine()
    
    # Exemplo de uso
    text = "Aurora é um sistema excelente de inteligência artificial para análise estratégica"
    result = engine.infer_from_text(text, task_type="analysis")
    
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    print("\nEstatísticas:")
    print(json.dumps(engine.get_inference_statistics(), indent=2, ensure_ascii=False))
