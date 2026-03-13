# security/encryption.py

import json
import hashlib
from typing import Dict, List, Any, Optional
from datetime import datetime
import base64


class EncryptionManager:
    """
    Gerenciador de Criptografia para proteção de dados.
    Implementa hash, encoding e simulação de criptografia.
    """

    def __init__(self):
        self.encryption_log = []
        self.key_store = {}
        print("Gerenciador de Criptografia inicializado.")

    def generate_key(self, key_id: str, key_size: int = 256) -> Dict[str, Any]:
        """Gera uma chave criptográfica."""
        key = {
            "key_id": key_id,
            "key_size": key_size,
            "algorithm": "AES",
            "created_at": datetime.now().isoformat(),
            "status": "active"
        }

        self.key_store[key_id] = key

        return key

    def hash_data(self, data: str, algorithm: str = "sha256") -> Dict[str, Any]:
        """Cria um hash de dados."""
        if algorithm == "sha256":
            hash_value = hashlib.sha256(data.encode()).hexdigest()
        elif algorithm == "sha512":
            hash_value = hashlib.sha512(data.encode()).hexdigest()
        else:
            hash_value = hashlib.md5(data.encode()).hexdigest()

        hash_result = {
            "original_length": len(data),
            "algorithm": algorithm,
            "hash": hash_value,
            "timestamp": datetime.now().isoformat()
        }

        self.encryption_log.append(hash_result)

        return hash_result

    def encrypt_data(self, data: str, key_id: str) -> Dict[str, Any]:
        """Criptografa dados (simulação)."""
        if key_id not in self.key_store:
            return {"error": "Chave não encontrada"}

        # Simulação de criptografia
        encrypted = base64.b64encode(data.encode()).decode()

        encryption_record = {
            "key_id": key_id,
            "original_size": len(data),
            "encrypted_size": len(encrypted),
            "encrypted_data": encrypted,
            "timestamp": datetime.now().isoformat(),
            "algorithm": "AES-256"
        }

        self.encryption_log.append(encryption_record)

        return encryption_record

    def decrypt_data(self, encrypted_data: str, key_id: str) -> Dict[str, Any]:
        """Descriptografa dados (simulação)."""
        if key_id not in self.key_store:
            return {"error": "Chave não encontrada"}

        try:
            # Simulação de descriptografia
            decrypted = base64.b64decode(encrypted_data).decode()

            decryption_record = {
                "key_id": key_id,
                "decrypted_data": decrypted,
                "timestamp": datetime.now().isoformat(),
                "status": "success"
            }

            self.encryption_log.append(decryption_record)

            return decryption_record

        except Exception as e:
            return {
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
                "status": "failed"
            }

    def verify_hash(self, data: str, hash_value: str, algorithm: str = "sha256") -> Dict[str, Any]:
        """Verifica se um hash corresponde aos dados."""
        if algorithm == "sha256":
            computed_hash = hashlib.sha256(data.encode()).hexdigest()
        elif algorithm == "sha512":
            computed_hash = hashlib.sha512(data.encode()).hexdigest()
        else:
            computed_hash = hashlib.md5(data.encode()).hexdigest()

        match = computed_hash == hash_value

        verification = {
            "data_length": len(data),
            "algorithm": algorithm,
            "match": match,
            "timestamp": datetime.now().isoformat()
        }

        self.encryption_log.append(verification)

        return verification

    def rotate_key(self, old_key_id: str, new_key_id: str) -> Dict[str, Any]:
        """Realiza rotação de chaves."""
        if old_key_id not in self.key_store:
            return {"error": "Chave antiga não encontrada"}

        # Desativar chave antiga
        self.key_store[old_key_id]["status"] = "rotated"

        # Gerar nova chave
        new_key = self.generate_key(new_key_id)

        rotation_record = {
            "old_key_id": old_key_id,
            "new_key_id": new_key_id,
            "timestamp": datetime.now().isoformat(),
            "status": "success"
        }

        self.encryption_log.append(rotation_record)

        return rotation_record

    def get_key_status(self, key_id: str) -> Optional[Dict[str, Any]]:
        """Retorna o status de uma chave."""
        return self.key_store.get(key_id)

    def get_encryption_statistics(self) -> Dict[str, Any]:
        """Retorna estatísticas de criptografia."""
        return {
            "total_keys": len(self.key_store),
            "active_keys": sum(1 for k in self.key_store.values() if k["status"] == "active"),
            "total_operations": len(self.encryption_log),
            "operations_by_type": self._count_operation_types()
        }

    def _count_operation_types(self) -> Dict[str, int]:
        """Conta operações por tipo."""
        types = {}
        for log in self.encryption_log:
            if "algorithm" in log:
                op_type = "hash"
            elif "encrypted_data" in log:
                op_type = "encryption"
            elif "decrypted_data" in log:
                op_type = "decryption"
            elif "match" in log:
                op_type = "verification"
            else:
                op_type = "other"

            types[op_type] = types.get(op_type, 0) + 1

        return types

    def export_encryption_log(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Exporta log de criptografia."""
        return self.encryption_log[-limit:]

    def clear_log(self) -> None:
        """Limpa o log de criptografia."""
        self.encryption_log.clear()


class DataProtection:
    """
    Proteção de Dados para implementar políticas de segurança.
    """

    def __init__(self):
        self.encryption_manager = EncryptionManager()
        self.access_policies = {}
        self.data_classifications = {}
        print("Sistema de Proteção de Dados inicializado.")

    def classify_data(self, data_id: str, classification: str, 
                     sensitivity: str) -> Dict[str, Any]:
        """Classifica dados por nível de sensibilidade."""
        classification_record = {
            "data_id": data_id,
            "classification": classification,
            "sensitivity": sensitivity,
            "classified_at": datetime.now().isoformat(),
            "encryption_required": sensitivity in ["high", "critical"]
        }

        self.data_classifications[data_id] = classification_record

        return classification_record

    def apply_protection(self, data: str, data_id: str) -> Dict[str, Any]:
        """Aplica proteção apropriada aos dados."""
        if data_id not in self.data_classifications:
            return {"error": "Dados não classificados"}

        classification = self.data_classifications[data_id]

        protection_result = {
            "data_id": data_id,
            "classification": classification,
            "protection_applied": False,
            "timestamp": datetime.now().isoformat()
        }

        if classification["encryption_required"]:
            key_id = f"key_{data_id}"
            self.encryption_manager.generate_key(key_id)
            encrypted = self.encryption_manager.encrypt_data(data, key_id)

            protection_result["protection_applied"] = True
            protection_result["method"] = "encryption"
            protection_result["encrypted"] = True

        return protection_result

    def get_protection_report(self) -> Dict[str, Any]:
        """Gera relatório de proteção de dados."""
        return {
            "total_classified_data": len(self.data_classifications),
            "encryption_statistics": self.encryption_manager.get_encryption_statistics(),
            "classifications": self.data_classifications,
            "timestamp": datetime.now().isoformat()
        }


if __name__ == "__main__":
    manager = EncryptionManager()

    # Gerar chave
    key = manager.generate_key("key_001")
    print("Chave gerada:")
    print(json.dumps(key, indent=2, ensure_ascii=False))

    # Hash de dados
    data = "Dados sensíveis para proteção"
    hash_result = manager.hash_data(data)
    print("\nHash dos dados:")
    print(json.dumps(hash_result, indent=2, ensure_ascii=False))

    # Criptografar
    encrypted = manager.encrypt_data(data, "key_001")
    print("\nDados criptografados:")
    print(json.dumps(encrypted, indent=2, ensure_ascii=False))

    # Descriptografar
    decrypted = manager.decrypt_data(encrypted["encrypted_data"], "key_001")
    print("\nDados descriptografados:")
    print(json.dumps(decrypted, indent=2, ensure_ascii=False))

    # Estatísticas
    print("\nEstatísticas:")
    print(json.dumps(manager.get_encryption_statistics(), indent=2, ensure_ascii=False))
