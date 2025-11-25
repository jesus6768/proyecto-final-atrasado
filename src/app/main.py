import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))

from flask import Flask
from src.app.routes import register_routes
from src.common.vars import HOME_HOST


def create_app():
    app = Flask(__name__, 
                
                template_folder='templates')
    register_routes(app)
    return app


app = create_app()


if __name__ == "__main__":
    # Run on all interfaces so it's accessible in containers; port taken from common vars
    app.run(host="0.0.0.0", port=HOME_HOST)
    
#transformar dev 8# y agregar descripcion