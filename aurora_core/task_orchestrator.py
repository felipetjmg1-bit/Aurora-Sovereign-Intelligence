# aurora_core/task_orchestrator.py

import json
from typing import Dict, List, Any, Callable, Optional
from datetime import datetime
from enum import Enum
import uuid


class TaskStatus(Enum):
    """Estados possíveis de uma tarefa."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class Task:
    """Representa uma tarefa individual."""
    
    def __init__(self, task_id: str, name: str, handler: Callable, 
                 dependencies: Optional[List[str]] = None, priority: int = 0):
        self.task_id = task_id
        self.name = name
        self.handler = handler
        self.dependencies = dependencies or []
        self.priority = priority
        self.status = TaskStatus.PENDING
        self.created_at = datetime.now().isoformat()
        self.started_at = None
        self.completed_at = None
        self.result = None
        self.error = None

    def to_dict(self) -> Dict[str, Any]:
        """Converte a tarefa para dicionário."""
        return {
            "task_id": self.task_id,
            "name": self.name,
            "status": self.status.value,
            "priority": self.priority,
            "dependencies": self.dependencies,
            "created_at": self.created_at,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "result": self.result,
            "error": self.error
        }


class TaskOrchestrator:
    """
    Orquestrador de Tarefas para coordenação de múltiplas operações.
    Responsável por agendamento, execução e monitoramento de tarefas.
    """

    def __init__(self):
        self.tasks = {}
        self.execution_history = []
        self.task_queue = []
        print("Orquestrador de Tarefas inicializado.")

    def register_task(self, name: str, handler: Callable, 
                     dependencies: Optional[List[str]] = None, 
                     priority: int = 0) -> str:
        """Registra uma nova tarefa."""
        task_id = str(uuid.uuid4())
        
        task = Task(task_id, name, handler, dependencies, priority)
        self.tasks[task_id] = task
        
        return task_id

    def submit_task(self, task_id: str) -> bool:
        """Submete uma tarefa para execução."""
        if task_id not in self.tasks:
            return False
        
        task = self.tasks[task_id]
        
        # Verificar dependências
        if not self._check_dependencies(task):
            return False
        
        self.task_queue.append(task_id)
        # Ordenar por prioridade
        self.task_queue.sort(
            key=lambda tid: self.tasks[tid].priority, 
            reverse=True
        )
        
        return True

    def execute_task(self, task_id: str) -> Dict[str, Any]:
        """Executa uma tarefa específica."""
        if task_id not in self.tasks:
            return {"success": False, "error": "Tarefa não encontrada"}
        
        task = self.tasks[task_id]
        
        try:
            task.status = TaskStatus.RUNNING
            task.started_at = datetime.now().isoformat()
            
            # Executar handler
            result = task.handler()
            
            task.status = TaskStatus.COMPLETED
            task.result = result
            task.completed_at = datetime.now().isoformat()
            
            execution_record = {
                "task_id": task_id,
                "status": "success",
                "result": result,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            task.status = TaskStatus.FAILED
            task.error = str(e)
            task.completed_at = datetime.now().isoformat()
            
            execution_record = {
                "task_id": task_id,
                "status": "failed",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
        
        self.execution_history.append(execution_record)
        return execution_record

    def execute_queue(self) -> List[Dict[str, Any]]:
        """Executa todas as tarefas na fila."""
        results = []
        
        while self.task_queue:
            task_id = self.task_queue.pop(0)
            result = self.execute_task(task_id)
            results.append(result)
        
        return results

    def _check_dependencies(self, task: Task) -> bool:
        """Verifica se as dependências da tarefa foram atendidas."""
        for dep_id in task.dependencies:
            if dep_id not in self.tasks:
                return False
            
            dep_task = self.tasks[dep_id]
            if dep_task.status != TaskStatus.COMPLETED:
                return False
        
        return True

    def get_task_status(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Retorna o status de uma tarefa."""
        if task_id not in self.tasks:
            return None
        
        return self.tasks[task_id].to_dict()

    def get_all_tasks(self) -> List[Dict[str, Any]]:
        """Retorna todas as tarefas."""
        return [task.to_dict() for task in self.tasks.values()]

    def get_pending_tasks(self) -> List[Dict[str, Any]]:
        """Retorna tarefas pendentes."""
        return [
            task.to_dict() for task in self.tasks.values()
            if task.status == TaskStatus.PENDING
        ]

    def cancel_task(self, task_id: str) -> bool:
        """Cancela uma tarefa."""
        if task_id not in self.tasks:
            return False
        
        task = self.tasks[task_id]
        if task.status == TaskStatus.PENDING:
            task.status = TaskStatus.CANCELLED
            return True
        
        return False

    def get_execution_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Retorna o histórico de execução."""
        return self.execution_history[-limit:]

    def get_statistics(self) -> Dict[str, Any]:
        """Retorna estatísticas do orquestrador."""
        total_tasks = len(self.tasks)
        completed = sum(1 for t in self.tasks.values() if t.status == TaskStatus.COMPLETED)
        failed = sum(1 for t in self.tasks.values() if t.status == TaskStatus.FAILED)
        pending = sum(1 for t in self.tasks.values() if t.status == TaskStatus.PENDING)
        
        return {
            "total_tasks": total_tasks,
            "completed": completed,
            "failed": failed,
            "pending": pending,
            "queue_size": len(self.task_queue),
            "execution_history_size": len(self.execution_history)
        }

    def export_orchestrator_state(self) -> Dict[str, Any]:
        """Exporta o estado atual do orquestrador."""
        return {
            "statistics": self.get_statistics(),
            "tasks": self.get_all_tasks(),
            "queue_size": len(self.task_queue)
        }


if __name__ == "__main__":
    orchestrator = TaskOrchestrator()
    
    # Exemplo de uso
    def sample_task_1():
        return "Tarefa 1 concluída"
    
    def sample_task_2():
        return "Tarefa 2 concluída"
    
    # Registrar tarefas
    task1_id = orchestrator.register_task("Tarefa 1", sample_task_1, priority=1)
    task2_id = orchestrator.register_task("Tarefa 2", sample_task_2, 
                                         dependencies=[task1_id], priority=2)
    
    # Submeter tarefas
    orchestrator.submit_task(task1_id)
    orchestrator.submit_task(task2_id)
    
    # Executar fila
    results = orchestrator.execute_queue()
    
    print("Resultados da execução:")
    print(json.dumps(results, indent=2, ensure_ascii=False))
    
    print("\nEstatísticas:")
    print(json.dumps(orchestrator.get_statistics(), indent=2, ensure_ascii=False))
