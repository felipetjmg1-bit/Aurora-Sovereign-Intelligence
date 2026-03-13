# prediction/predictive_models.py

import json
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import math


class PredictiveModel:
    """
    Modelo Preditivo para previsão de eventos e tendências.
    Implementa regressão linear simples e análise de série temporal.
    """

    def __init__(self, model_name: str = "default_model"):
        self.model_name = model_name
        self.training_data = []
        self.model_params = {}
        self.predictions = []
        print(f"Modelo Preditivo {model_name} inicializado.")

    def train_linear_regression(self, data: List[Tuple[float, float]]) -> Dict[str, Any]:
        """Treina um modelo de regressão linear."""
        if len(data) < 2:
            return {"error": "Dados insuficientes para treinamento"}

        self.training_data = data
        
        # Calcular parâmetros de regressão linear (y = mx + b)
        n = len(data)
        sum_x = sum(x for x, y in data)
        sum_y = sum(y for x, y in data)
        sum_xy = sum(x * y for x, y in data)
        sum_x2 = sum(x * x for x, y in data)

        denominator = n * sum_x2 - sum_x * sum_x
        
        if denominator == 0:
            return {"error": "Não é possível treinar o modelo"}

        m = (n * sum_xy - sum_x * sum_y) / denominator
        b = (sum_y - m * sum_x) / n

        self.model_params = {
            "slope": m,
            "intercept": b,
            "r_squared": self._calculate_r_squared(data, m, b),
            "trained_at": datetime.now().isoformat(),
            "data_points": n
        }

        return {
            "status": "trained",
            "model": self.model_name,
            "parameters": self.model_params
        }

    def predict(self, x_value: float) -> Dict[str, Any]:
        """Realiza uma previsão usando o modelo treinado."""
        if not self.model_params:
            return {"error": "Modelo não treinado"}

        m = self.model_params["slope"]
        b = self.model_params["intercept"]
        
        y_predicted = m * x_value + b
        
        prediction = {
            "input": x_value,
            "predicted_output": y_predicted,
            "confidence": self.model_params.get("r_squared", 0),
            "timestamp": datetime.now().isoformat()
        }
        
        self.predictions.append(prediction)
        return prediction

    def predict_batch(self, x_values: List[float]) -> List[Dict[str, Any]]:
        """Realiza previsões em lote."""
        return [self.predict(x) for x in x_values]

    def _calculate_r_squared(self, data: List[Tuple[float, float]], 
                            m: float, b: float) -> float:
        """Calcula o coeficiente de determinação (R²)."""
        y_values = [y for x, y in data]
        y_mean = sum(y_values) / len(y_values)
        
        ss_tot = sum((y - y_mean) ** 2 for y in y_values)
        ss_res = sum((y - (m * x + b)) ** 2 for x, y in data)
        
        if ss_tot == 0:
            return 0.0
        
        return 1 - (ss_res / ss_tot)

    def forecast_trend(self, periods: int = 5) -> List[Dict[str, Any]]:
        """Prevê tendências futuras."""
        if not self.model_params:
            return []

        forecasts = []
        
        if self.training_data:
            last_x = max(x for x, y in self.training_data)
        else:
            last_x = 0

        for i in range(1, periods + 1):
            x_future = last_x + i
            prediction = self.predict(x_future)
            forecasts.append(prediction)

        return forecasts

    def get_model_statistics(self) -> Dict[str, Any]:
        """Retorna estatísticas do modelo."""
        return {
            "model_name": self.model_name,
            "training_data_points": len(self.training_data),
            "total_predictions": len(self.predictions),
            "model_parameters": self.model_params,
            "model_quality": self.model_params.get("r_squared", 0)
        }

    def export_model(self) -> Dict[str, Any]:
        """Exporta o modelo treinado."""
        return {
            "model_name": self.model_name,
            "parameters": self.model_params,
            "training_data_count": len(self.training_data),
            "predictions_made": len(self.predictions)
        }


class TimeSeriesPredictor:
    """
    Preditor de Série Temporal para análise de dados sequenciais.
    """

    def __init__(self):
        self.time_series = []
        self.forecasts = []
        print("Preditor de Série Temporal inicializado.")

    def add_data_point(self, timestamp: str, value: float) -> None:
        """Adiciona um ponto de dados à série temporal."""
        self.time_series.append({
            "timestamp": timestamp,
            "value": value
        })

    def calculate_moving_average(self, window_size: int = 3) -> List[Dict[str, Any]]:
        """Calcula a média móvel da série temporal."""
        if len(self.time_series) < window_size:
            return []

        moving_averages = []
        
        for i in range(len(self.time_series) - window_size + 1):
            window = self.time_series[i:i + window_size]
            avg_value = sum(point["value"] for point in window) / window_size
            
            moving_averages.append({
                "timestamp": window[-1]["timestamp"],
                "moving_average": avg_value,
                "window_size": window_size
            })

        return moving_averages

    def detect_trend(self) -> Dict[str, Any]:
        """Detecta tendências na série temporal."""
        if len(self.time_series) < 2:
            return {"error": "Dados insuficientes"}

        values = [point["value"] for point in self.time_series]
        
        # Calcular diferenças
        differences = [values[i+1] - values[i] for i in range(len(values)-1)]
        
        avg_difference = sum(differences) / len(differences)
        
        if avg_difference > 0:
            trend = "upward"
        elif avg_difference < 0:
            trend = "downward"
        else:
            trend = "stable"

        return {
            "trend": trend,
            "average_change": avg_difference,
            "data_points": len(self.time_series)
        }

    def forecast(self, periods: int = 5) -> List[Dict[str, Any]]:
        """Realiza previsão de série temporal."""
        if len(self.time_series) < 2:
            return []

        trend_info = self.detect_trend()
        last_value = self.time_series[-1]["value"]
        
        values = [point["value"] for point in self.time_series]
        avg_change = sum(values[i+1] - values[i] for i in range(len(values)-1)) / (len(values)-1)

        forecasts = []
        
        for i in range(1, periods + 1):
            forecasted_value = last_value + (avg_change * i)
            
            forecasts.append({
                "period": i,
                "forecasted_value": forecasted_value,
                "confidence": 0.7 - (i * 0.05),  # Confiança diminui com períodos
                "trend": trend_info["trend"]
            })

        self.forecasts.extend(forecasts)
        return forecasts

    def get_statistics(self) -> Dict[str, Any]:
        """Retorna estatísticas da série temporal."""
        if not self.time_series:
            return {"error": "Sem dados"}

        values = [point["value"] for point in self.time_series]
        
        return {
            "data_points": len(self.time_series),
            "min_value": min(values),
            "max_value": max(values),
            "average_value": sum(values) / len(values),
            "trend": self.detect_trend()["trend"]
        }


if __name__ == "__main__":
    # Exemplo com regressão linear
    model = PredictiveModel("sales_model")
    
    training_data = [(1, 2), (2, 4), (3, 5), (4, 7), (5, 9)]
    model.train_linear_regression(training_data)
    
    print("Modelo treinado:")
    print(json.dumps(model.get_model_statistics(), indent=2, ensure_ascii=False))
    
    # Fazer previsões
    prediction = model.predict(6)
    print(f"\nPrevisão para x=6: {prediction}")
    
    # Exemplo com série temporal
    ts_predictor = TimeSeriesPredictor()
    
    for i, value in enumerate([10, 12, 15, 14, 18, 20, 22]):
        ts_predictor.add_data_point(f"2024-01-{i+1:02d}", value)
    
    print("\nTendência detectada:")
    print(json.dumps(ts_predictor.detect_trend(), indent=2, ensure_ascii=False))
    
    print("\nPrevisões de série temporal:")
    forecasts = ts_predictor.forecast(periods=3)
    print(json.dumps(forecasts, indent=2, ensure_ascii=False))
