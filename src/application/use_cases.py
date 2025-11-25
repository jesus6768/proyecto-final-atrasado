from datetime import datetime
from uuid import uuid4
from typing import Optional
import os

from src.domain.models import BinaryFile
from src.infrastructure.file_repository import FileRepository
from src.infrastructure.json_repository import JsonRepository
from src.infrastructure.email_service import EmailService # Nueva importación
from src.domain.services import SigningService

class UploadBinaryUseCase:
    def __init__(self, file_repo, db_repo, email_service=None):
        self.file_repo = file_repo
        self.db_repo = db_repo
        self.email_service = email_service or EmailService()
        
    def execute(self, file, environment: str) -> BinaryFile:
        binary_id = str(uuid4())
        full_path = self.file_repo.save(file, binary_id)
        filename = os.path.basename(full_path)

        binary = BinaryFile(
            id=binary_id,
            filename=filename,
            environment=environment,
            status='pending' if environment == 'prod' else 'uploaded',
            uploaded_date=datetime.now().isoformat()
        )
        self.db_repo.add_record(binary.to_dict())

        # LOGICA NUEVA: Si es PROD, enviar correo
        if environment == 'prod':
            print("Production environment detected. Sending approval email...")
            self.email_service.send_approval_request(binary.id, binary.filename)

        return binary

class SignBinaryUseCase:
    # (Este se queda IGUAL que en el código anterior que ya funcionaba)
    def __init__(self, file_repo: FileRepository, json_repo: JsonRepository, signing_service: SigningService):
        self.file_repo = file_repo
        self.json_repo = json_repo
        self.signing_service = signing_service
            
    def execute(self, file_id: str) -> Optional[BinaryFile]:
        record = self.json_repo.get_record(file_id)
        if record is None: return None
        
        try:
            binary = BinaryFile.from_dict(record)
            signature, signed_path = self.signing_service.sign_file(binary)

            binary.status = "signed"
            binary.signed_path = signed_path
            binary.signature = signature
            
            self.json_repo.update_record(binary.id, binary.to_dict()) # Simplificado
            return binary
        except Exception as e:
            print(f"Error signing: {e}")
            return None

# NUEVO CASO DE USO: Aprobar y Firmar
class ApproveBinaryUseCase:
    def __init__(self, sign_use_case: SignBinaryUseCase):
        self.sign_use_case = sign_use_case

    def execute(self, file_id: str) -> bool:
        # Reutilizamos la lógica de firma existente
        result = self.sign_use_case.execute(file_id)
        return result is not None