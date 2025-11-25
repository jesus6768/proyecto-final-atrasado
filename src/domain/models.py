# src/domain/models.py
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional, Dict, Any

@dataclass
class BinaryFile:
    id: str
    filename: str
    environment: str  # dev o prod (Nota: corregí 'enviroment' a 'environment' para consistencia)
    status: str  # pending, approved, signed, rejected
    uploaded_date: str  # Cambiado a str para facilitar serialización JSON por ahora, o mantener datetime y convertir.
    signed_path: Optional[str] = None
    signature: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls(
            id=data.get("id"),
            filename=data.get("filename"),
            environment=data.get("environment") or data.get("enviroment"), # Soporte para ambos por si acaso
            status=data.get("status"),
            uploaded_date=data.get("uploaded_date") or data.get("timestamp"),
            signed_path=data.get("signed_path"),
            signature=data.get("signature")
        )