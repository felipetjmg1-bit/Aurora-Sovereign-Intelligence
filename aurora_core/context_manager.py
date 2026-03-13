# aurora_core/context_manager.py

import json
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
import uuid


class ContextManager:
    """
    Gerenciador de Contexto para manutenção de estado de sessão e contexto.
    Responsável por armazenar, recuperar e gerenciar contextos de execução.
    """

    def __init__(self, max_context_history: int = 100):
        self.sessions = {}
        self.context_history = []
        self.max_context_history = max_context_history
        print("Gerenciador de Contexto inicializado.")

    def create_session(self, user_id: str, metadata: Optional[Dict[str, Any]] = None) -> str:
        """Cria uma nova sessão."""
        session_id = str(uuid.uuid4())
        
        self.sessions[session_id] = {
            "session_id": session_id,
            "user_id": user_id,
            "created_at": datetime.now().isoformat(),
            "last_activity": datetime.now().isoformat(),
            "context_data": {},
            "metadata": metadata or {},
            "is_active": True
        }
        
        return session_id

    def set_context(self, session_id: str, key: str, value: Any) -> bool:
        """Define um valor no contexto da sessão."""
        if session_id not in self.sessions:
            return False
        
        self.sessions[session_id]["context_data"][key] = value
        self.sessions[session_id]["last_activity"] = datetime.now().isoformat()
        
        # Registrar no histórico
        self._record_context_change(session_id, key, value)
        
        return True

    def get_context(self, session_id: str, key: Optional[str] = None) -> Optional[Any]:
        """Recupera um valor do contexto da sessão."""
        if session_id not in self.sessions:
            return None
        
        session = self.sessions[session_id]
        
        if key is None:
            return session["context_data"]
        
        return session["context_data"].get(key)

    def update_context(self, session_id: str, context_updates: Dict[str, Any]) -> bool:
        """Atualiza múltiplos valores no contexto."""
        if session_id not in self.sessions:
            return False
        
        for key, value in context_updates.items():
            self.set_context(session_id, key, value)
        
        return True

    def get_session_info(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Retorna informações completas da sessão."""
        return self.sessions.get(session_id)

    def close_session(self, session_id: str) -> bool:
        """Fecha uma sessão."""
        if session_id not in self.sessions:
            return False
        
        self.sessions[session_id]["is_active"] = False
        self.sessions[session_id]["closed_at"] = datetime.now().isoformat()
        
        return True

    def get_active_sessions(self, user_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Retorna todas as sessões ativas."""
        active_sessions = [
            session for session in self.sessions.values()
            if session["is_active"]
        ]
        
        if user_id:
            active_sessions = [
                session for session in active_sessions
                if session["user_id"] == user_id
            ]
        
        return active_sessions

    def _record_context_change(self, session_id: str, key: str, value: Any) -> None:
        """Registra uma mudança de contexto no histórico."""
        record = {
            "timestamp": datetime.now().isoformat(),
            "session_id": session_id,
            "key": key,
            "value": value
        }
        
        self.context_history.append(record)
        
        # Limitar tamanho do histórico
        if len(self.context_history) > self.max_context_history:
            self.context_history = self.context_history[-self.max_context_history:]

    def get_context_history(self, session_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Retorna o histórico de mudanças de contexto."""
        if session_id is None:
            return self.context_history
        
        return [record for record in self.context_history if record["session_id"] == session_id]

    def cleanup_inactive_sessions(self, inactive_hours: int = 24) -> int:
        """Remove sessões inativas após o tempo especificado."""
        cutoff_time = datetime.now() - timedelta(hours=inactive_hours)
        
        sessions_to_remove = []
        for session_id, session in self.sessions.items():
            if not session["is_active"]:
                last_activity = datetime.fromisoformat(session["last_activity"])
                if last_activity < cutoff_time:
                    sessions_to_remove.append(session_id)
        
        for session_id in sessions_to_remove:
            del self.sessions[session_id]
        
        return len(sessions_to_remove)

    def export_context_state(self) -> Dict[str, Any]:
        """Exporta o estado atual do gerenciador de contexto."""
        return {
            "total_sessions": len(self.sessions),
            "active_sessions": len(self.get_active_sessions()),
            "history_size": len(self.context_history),
            "max_history": self.max_context_history
        }


if __name__ == "__main__":
    manager = ContextManager()
    
    # Exemplo de uso
    session_id = manager.create_session("user_001", {"role": "admin"})
    print(f"Sessão criada: {session_id}")
    
    # Definir contexto
    manager.set_context(session_id, "task_id", "task_123")
    manager.set_context(session_id, "status", "processing")
    
    # Obter contexto
    context = manager.get_context(session_id)
    print(f"\nContexto da sessão:")
    print(json.dumps(context, indent=2, ensure_ascii=False))
    
    # Informações da sessão
    session_info = manager.get_session_info(session_id)
    print(f"\nInformações da sessão:")
    print(json.dumps(session_info, indent=2, ensure_ascii=False, default=str))
