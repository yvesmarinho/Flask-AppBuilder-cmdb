
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_appbuilder import AppBuilder
from .database import db
from .views import register_views
from .models import App_type, Application, Customers, Device_app_dns, Device_type, Devices, Dns_a_register, Ip_address, Network_interface, Operationalsystem_type, Organization, Provider, Services, Test, Test_app_server, Test_execution_control, Test_result, Test_status, Test_title, Test_topic

# Configuração do logging
logging = logging.getLogger(__name__)

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.ini')

    # Configuração do SQLAlchemy
    db.init_app(app)

    with app.app_context():
        db.create_all()

    # Registro das views
    register_views(app)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)