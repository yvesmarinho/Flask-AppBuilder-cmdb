# app_template.jinja2

from flask import Flask
from flask_appbuilder import AppBuilder, SQLA
from mysql import Mysql

app = Flask(__name__)

# Configuração do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"mysql://cmdb_user:"
    f"pHi9rufesTlsTlC6OcHi@154.53.36.3:"
    f"3306/cmdb"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLA(app)
appbuilder = AppBuilder(app, db.session)

# Configurações adicionais podem ser adicionadas aqui

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)