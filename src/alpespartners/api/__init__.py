import os

from flask import Flask, render_template, request, url_for, redirect, jsonify, session
from flask_swagger import swagger

# Identifica el directorio base
basedir = os.path.abspath(os.path.dirname(__file__))


def registrar_handlers():
    import alpespartners.modulos.marca.aplicacion
    import alpespartners.modulos.afiliaciones.aplicacion


def importar_modelos_alchemy():
    import alpespartners.modulos.marca.infraestructura.dto
    import alpespartners.modulos.afiliaciones.infraestructura.dto


def comenzar_consumidor():
    """
    Este es un código de ejemplo. Aunque esto sea funcional puede ser un poco peligroso tener 
    threads corriendo por si solos. Mi sugerencia es en estos casos usar un verdadero manejador
    de procesos y threads como Celery.
    """

    import threading
    import alpespartners.modulos.marca.infraestructura.consumidores as marca
    import alpespartners.modulos.afiliaciones.infraestructura.consumidores as afiliaciones

    # Suscripción a eventos
    threading.Thread(target=marca.suscribirse_a_eventos).start()
    threading.Thread(target=afiliaciones.suscribirse_a_eventos).start()

    # Suscripción a comandos
    threading.Thread(target=marca.suscribirse_a_comandos).start()
    threading.Thread(target=afiliaciones.suscribirse_a_comandos).start()


def get_standard_postgres_connection() -> str:
    db_user = os.environ["DB_USER"]
    db_password = os.environ["DB_PASSWORD"]
    db_host = os.environ["DB_HOST"]
    db_port = os.environ["DB_PORT"]
    db_name = os.environ["DB_NAME"]

    return f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"


def create_app(configuracion={}):
    app = Flask(__name__, instance_relative_config=True)

    app.config['SQLALCHEMY_DATABASE_URI'] = get_standard_postgres_connection()
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.secret_key = '9d58f98f-3ae8-4149-a09f-3a8c2012e32c'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['TESTING'] = configuracion.get('TESTING')

    # Inicializa la DB
    from alpespartners.config.db import init_db, db

    init_db(app)
    importar_modelos_alchemy()
    registrar_handlers()

    with app.app_context():
        db.create_all()
        if not app.config.get('TESTING'):
            comenzar_consumidor()

     # Importa Blueprints
    from . import marca
    from . import afiliaciones

    # Registro de Blueprints
    app.register_blueprint(marca.bp)
    app.register_blueprint(afiliaciones.bp)

    @app.route("/spec")
    def spec():
        swag = swagger(app)
        swag['info']['version'] = "1.0"
        swag['info']['title'] = "My API"
        return jsonify(swag)

    @app.route("/health")
    def health():
        return {"status": "up"}

    return app
