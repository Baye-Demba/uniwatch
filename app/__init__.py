from flask import Flask
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)

    import os
    app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev_secret")

    from app.models import init_db
    try:
        init_db()
    except Exception as e:
        print(f"Avertissement DB : {e}")

    from app.routes import main
    app.register_blueprint(main)

    return app