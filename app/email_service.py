import os
from flask_mail import Mail, Message
from dotenv import load_dotenv

load_dotenv()

mail = Mail()

def init_mail(app):
    """Initialise Flask-Mail avec la configuration de l'app"""
    app.config['MAIL_SERVER']   = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    app.config['MAIL_PORT']     = int(os.getenv('MAIL_PORT', 587))
    app.config['MAIL_USE_TLS']  = True
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
    mail.init_app(app)

def envoyer_alerte(app, nom_camera, message):
    """Envoie un email d'alerte quand une caméra passe hors ligne"""
    try:
        with app.app_context():
            msg = Message(
                subject=f"[UniWatch] Alerte — {nom_camera}",
                sender=os.getenv('MAIL_USERNAME'),
                recipients=[os.getenv('MAIL_RECEIVER')],
                body=f"""
UniWatch — Alerte de surveillance

Caméra  : {nom_camera}
Message : {message}
Action  : Vérifiez la connexion de la caméra

---
UniWatch — Plateforme de surveillance vidéo
                """
            )
            mail.send(msg)
            return True
    except Exception as e:
        print(f"Erreur email : {e}")
        return False