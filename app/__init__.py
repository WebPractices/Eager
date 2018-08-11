from flask import Flask
from flask_sqlalchemy import SQLAlchemy


# db = SQLAlchemy()

def create_app(flask_config):
    app = Flask(__name__)
    app.config.from_object('app.config.{}'.format(flask_config))
    # db.init_app(app)

    from app.api import api_bp
    from app.client import client_bp
    app.register_blueprint(api_bp)
    app.register_blueprint(client_bp)

    app.logger.info('>>> {}'.format(flask_config))
    return app
