import smtplib
from email.mime.text import MIMEText
from src.common.vars import SMTP_SERVER, SMTP_PORT, SENDER_EMAIL, SENDER_PASSWORD, BASE_URL

class EmailService:
    def send_approval_request(self, file_id: str, filename: str):
        subject = f"Approval Required: {filename}"
        
        # Link que activará la aprobación
        approval_link = f"{BASE_URL}/approve/{file_id}"
        
        body = f"""
        A new binary file has been uploaded to PRODUCTION environment.
        
        File ID: {file_id}
        Filename: {filename}
        
        Click the link below to APPROVE and SIGN this file:
        {approval_link}
        """

        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = SENDER_EMAIL
        msg['To'] = SENDER_EMAIL # Enviamos al mismo correo para pruebas, o usa ADMIN_EMAIL

        try:
            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                server.starttls()
                server.login(SENDER_EMAIL, SENDER_PASSWORD)
                server.send_message(msg)
            print(f"[EmailService] Approval email sent for {filename}")
        except Exception as e:
            print(f"[EmailService] FAILED to send email: {e}")