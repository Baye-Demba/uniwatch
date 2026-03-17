from flask import Flask
from dotenv import load_dotenv
import os

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev_secret")

    # Initialiser la base de données
    from app.models import init_db
    try:
        init_db()
    except Exception as e:
        print(f"Avertissement DB : {e}")

    # Initialiser Flask-Mail
    from app.email_service import init_mail
    init_mail(app)

    # Enregistrer les routes
    from app.routes import main
    app.register_blueprint(main)

    # Démarrer le thread de monitoring UNE SEULE FOIS
    # WERKZEUG_RUN_MAIN évite le double démarrage en mode debug
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true" or not app.debug:
        from app.monitor import demarrer_monitoring
        demarrer_monitoring(app)

    return app