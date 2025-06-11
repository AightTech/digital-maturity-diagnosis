from dotenv import load_dotenv
from flask import Flask
from src.presentation.routes import diagnostic_creation_bp

load_dotenv()

def create_app():
    app = Flask(__name__)

    # Registro do Bluprint da rota principal
    app.register_blueprint(diagnostic_creation_bp)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host= '0.0.0.0', port=5000, debug=True)