import os
import hashlib
from typing import Tuple
from src.domain.models import BinaryFile
from src.common.vars import BINARIES_DIR, SIGNED_DIR

class SigningService:
    
    def __init__(self, output_dir: str = SIGNED_DIR):
        self.output_dir = output_dir
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
    def sign_file(self, binary: BinaryFile) -> Tuple[str, str]:
        try:
            # Buscamos el archivo en la carpeta de binarios
            # (Asumimos que binary.filename es solo el nombre, ej: "foto.png")
            source_path = os.path.join(BINARIES_DIR, os.path.basename(binary.filename))
            
            # CORRECCIÓN: Definir nombre del archivo de salida
            signed_filename = f"signed_{os.path.basename(binary.filename)}"
            signed_path = os.path.join(self.output_dir, signed_filename)
        
            if not os.path.exists(source_path):
                raise FileNotFoundError(f"Source file not found at {source_path}")

            # 1. Calcular firma SHA-256
            sha256_hash = hashlib.sha256()
            with open(source_path, 'rb') as file:
                # Leer en bloques por eficiencia
                for block in iter(lambda: file.read(4096), b""):
                    sha256_hash.update(block)
            
            signature = sha256_hash.hexdigest()
            
            # 2. Crear copia firmada (Contenido original + Firma al final)
            with open(source_path, 'rb') as src, open(signed_path, 'wb') as dst:
                dst.write(src.read())
                # Agregamos la firma como metadata visible al final del archivo
                dst.write(b"\n\n# SIGNATURE: " + signature.encode("utf-8"))
            
            print(f"[SigningService] File '{binary.filename}' signed successfully.")            
            # Devolvemos la firma y la ruta absoluta del archivo firmado
            return signature, signed_path
        
        except Exception as e:
            print(f"[SigningService] Error while signing '{binary.filename}': {e}")
            raise