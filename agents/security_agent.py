# agents/security_agent.py

import json
from typing import Dict, List, Any, Optional
from datetime import datetime
from enum import Enum


class ThreatLevel(Enum):
    """Níveis de ameaça de segurança."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class SecurityAgent:
    """
    Agente de Segurança para monitoramento, detecção de ameaças e proteção.
    Responsável por firewall comportamental, detecção de intrusão e auditoria.
    """

    def __init__(self, agent_id: str = "security_agent_001"):
        self.agent_id = agent_id
        self.security_events = []
        self.threat_log = []
        self.access_control_rules = {}
        self.blocked_ips = set()
        print(f"Agente de Segurança {agent_id} inicializado.")

    def register_access_rule(self, rule_id: str, rule_config: Dict[str, Any]) -> bool:
        """Registra uma regra de controle de acesso."""
        self.access_control_rules[rule_id] = {
            "config": rule_config,
            "created_at": datetime.now().isoformat(),
            "enabled": True
        }
        return True

    def monitor_access(self, source_ip: str, resource: str, 
                      action: str) -> Dict[str, Any]:
        """Monitora tentativa de acesso."""
        event = {
            "timestamp": datetime.now().isoformat(),
            "source_ip": source_ip,
            "resource": resource,
            "action": action,
            "allowed": True,
            "reason": "Acesso permitido"
        }

        # Verificar se IP está bloqueado
        if source_ip in self.blocked_ips:
            event["allowed"] = False
            event["reason"] = "IP bloqueado"
            event["threat_level"] = ThreatLevel.HIGH.value

        # Verificar regras de acesso
        if event["allowed"]:
            for rule_id, rule in self.access_control_rules.items():
                if rule["enabled"]:
                    if not self._check_rule(source_ip, resource, action, rule["config"]):
                        event["allowed"] = False
                        event["reason"] = f"Violação de regra: {rule_id}"
                        event["threat_level"] = ThreatLevel.MEDIUM.value
                        break

        self.security_events.append(event)

        if not event["allowed"]:
            self.threat_log.append(event)

        return event

    def _check_rule(self, source_ip: str, resource: str, 
                   action: str, rule_config: Dict[str, Any]) -> bool:
        """Verifica se uma ação atende a uma regra."""
        # Simulação de verificação de regra
        allowed_actions = rule_config.get("allowed_actions", ["read"])
        allowed_resources = rule_config.get("allowed_resources", ["*"])

        if action not in allowed_actions:
            return False

        if allowed_resources != ["*"] and resource not in allowed_resources:
            return False

        return True

    def detect_intrusion(self, events: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Detecta padrões de intrusão."""
        intrusions = []

        # Contar tentativas falhadas por IP
        failed_attempts = {}
        for event in events:
            if not event.get("allowed", True):
                ip = event.get("source_ip")
                failed_attempts[ip] = failed_attempts.get(ip, 0) + 1

        # Identificar IPs suspeitos
        for ip, count in failed_attempts.items():
            if count > 3:
                intrusions.append({
                    "type": "brute_force",
                    "source_ip": ip,
                    "failed_attempts": count,
                    "threat_level": ThreatLevel.HIGH.value if count > 5 else ThreatLevel.MEDIUM.value,
                    "detected_at": datetime.now().isoformat()
                })

        return intrusions

    def block_ip(self, ip_address: str) -> bool:
        """Bloqueia um endereço IP."""
        self.blocked_ips.add(ip_address)
        
        event = {
            "timestamp": datetime.now().isoformat(),
            "action": "block_ip",
            "ip": ip_address,
            "status": "blocked"
        }
        
        self.security_events.append(event)
        return True

    def unblock_ip(self, ip_address: str) -> bool:
        """Desbloqueia um endereço IP."""
        if ip_address in self.blocked_ips:
            self.blocked_ips.remove(ip_address)
            
            event = {
                "timestamp": datetime.now().isoformat(),
                "action": "unblock_ip",
                "ip": ip_address,
                "status": "unblocked"
            }
            
            self.security_events.append(event)
            return True
        
        return False

    def generate_security_report(self) -> Dict[str, Any]:
        """Gera um relatório de segurança."""
        total_events = len(self.security_events)
        total_threats = len(self.threat_log)
        
        threat_levels = {}
        for threat in self.threat_log:
            level = threat.get("threat_level", "unknown")
            threat_levels[level] = threat_levels.get(level, 0) + 1

        report = {
            "agent_id": self.agent_id,
            "generated_at": datetime.now().isoformat(),
            "summary": {
                "total_events": total_events,
                "total_threats": total_threats,
                "blocked_ips": len(self.blocked_ips),
                "threat_distribution": threat_levels
            },
            "recent_threats": self.threat_log[-10:],
            "security_status": self._calculate_security_status()
        }

        return report

    def _calculate_security_status(self) -> str:
        """Calcula o status geral de segurança."""
        if len(self.threat_log) == 0:
            return "secure"
        elif len(self.threat_log) < 5:
            return "warning"
        else:
            return "alert"

    def get_security_events(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Retorna eventos de segurança recentes."""
        return self.security_events[-limit:]

    def get_threat_log(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Retorna log de ameaças."""
        return self.threat_log[-limit:]

    def get_agent_status(self) -> Dict[str, Any]:
        """Retorna o status do agente."""
        return {
            "agent_id": self.agent_id,
            "security_events": len(self.security_events),
            "threats_detected": len(self.threat_log),
            "blocked_ips": len(self.blocked_ips),
            "status": self._calculate_security_status()
        }


if __name__ == "__main__":
    agent = SecurityAgent()

    # Registrar regras
    agent.register_access_rule("rule_1", {
        "allowed_actions": ["read", "write"],
        "allowed_resources": ["/data", "/reports"]
    })

    # Monitorar acessos
    agent.monitor_access("192.168.1.1", "/data", "read")
    agent.monitor_access("192.168.1.2", "/admin", "write")
    agent.monitor_access("192.168.1.2", "/admin", "write")
    agent.monitor_access("192.168.1.2", "/admin", "write")
    agent.monitor_access("192.168.1.2", "/admin", "write")

    # Detectar intrusão
    intrusions = agent.detect_intrusion(agent.security_events)
    print("Intrusões detectadas:")
    print(json.dumps(intrusions, indent=2, ensure_ascii=False))

    # Bloquear IP
    if intrusions:
        agent.block_ip(intrusions[0]["source_ip"])

    # Gerar relatório
    report = agent.generate_security_report()
    print("\nRelatório de Segurança:")
    print(json.dumps(report, indent=2, ensure_ascii=False))
