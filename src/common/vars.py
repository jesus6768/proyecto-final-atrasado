import os

# =========================================================
# 1. Rutas del Sistema (Directorios)
# =========================================================
# Sube 3 niveles desde src/common/vars.py para llegar a la raíz
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

SRC_DIR = os.path.join(BASE_DIR, "src")
DATA_DIR = os.path.join(BASE_DIR, "data")
BINARIES_DIR = os.path.join(DATA_DIR, "binaries") # Donde se suben los originales
SIGNED_DIR = os.path.join(DATA_DIR, "signed")   # Donde van los firmados

# Frontend directories
TEMPLATES_DIR = os.path.join(SRC_DIR, "app", "templates")

# =========================================================
# 2. Configuración del Servidor
# =========================================================
HOME_HOST = 8080

# =========================================================
# 3. Inicialización de Carpetas
# =========================================================
# Asegurar que existan los directorios críticos al iniciar
for directory in [DATA_DIR, BINARIES_DIR, SIGNED_DIR]:
    if not os.path.exists(directory):
        try:
            os.makedirs(directory)
        except OSError:
            pass

# =========================================================
# 4. Configuración de Correo Electrónico
# =========================================================
# REEMPLAZA ESTO CON TUS DATOS REALES
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "jesuses565756@gmail.com"
SENDER_PASSWORD = "nalr wyiz xyjv cpnx" 
ADMIN_EMAIL = "jesuses565756@gmail.com"

# Esta línea fallaba antes porque HOME_HOST no existía arriba. Ahora ya existe.
BASE_URL = f"http://localhost:{HOME_HOST}"