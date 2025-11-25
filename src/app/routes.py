from flask import request, jsonify, render_template
from src.application.use_cases import UploadBinaryUseCase, SignBinaryUseCase, ApproveBinaryUseCase
from src.infrastructure.file_repository import FileRepository
from src.infrastructure.json_repository import JsonRepository
from src.infrastructure.email_service import EmailService
from src.domain.services import SigningService
from src.domain.models import BinaryFile

def register_routes(app):
    @app.route('/')
    def home():
        json_repo = JsonRepository()
        files = json_repo.list_records()
        return render_template('home.html', files=files[::-1])

    @app.route('/upload', methods=['POST'])
    def upload_binary():
        try:
            if 'file' not in request.files:
                return jsonify({"error": "No file part"}), 400
            file = request.files['file']
            environment = request.form.get('environment', 'dev')
            
            # Instanciamos con el servicio de email
            use_case = UploadBinaryUseCase(FileRepository(), JsonRepository(), EmailService())
            binary = use_case.execute(file, environment)
            
            return jsonify(binary.to_dict()), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/sign", methods=["POST"])
    def sign_file():
        # (Lógica existente para DEV)
        data = request.get_json()
        file_id = data.get("file_id")
        
        json_repo = JsonRepository()
        record = json_repo.get_record(file_id)
        if not record: return jsonify({"error": "Not found"}), 404
        
        binary = BinaryFile.from_dict(record)
        
        # Si es PROD, no firmamos aquí, solo avisamos
        if binary.environment == "prod":
            return jsonify({
                "status": binary.status, 
                "message": "Production file waiting for email approval."
            }), 200

        # Si es DEV, firmamos directo
        use_case = SignBinaryUseCase(FileRepository(), JsonRepository(), SigningService())
        signed = use_case.execute(file_id)
        return jsonify(signed.to_dict()), 200

    # NUEVA RUTA PARA EL LINK DEL CORREO
    @app.route('/approve/<file_id>')
    def approve_file(file_id):
        try:
            # Configurar dependencias
            file_repo = FileRepository()
            json_repo = JsonRepository()
            signing_service = SigningService()
            
            sign_use_case = SignBinaryUseCase(file_repo, json_repo, signing_service)
            approve_use_case = ApproveBinaryUseCase(sign_use_case)
            
            success = approve_use_case.execute(file_id)
            
            if success:
                return f"<h1>Success!</h1><p>File {file_id} has been APPROVED and SIGNED.</p><a href='/'>Go back home</a>"
            else:
                return "<h1>Error</h1><p>Could not approve file. Check logs.</p>"
                
        except Exception as e:
            return f"Error: {str(e)}"