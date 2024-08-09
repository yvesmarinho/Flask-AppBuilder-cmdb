# -*- coding: utf-8 -*-
"""
-------------------------------------------------------------------------
NOME..: app_creator.py
LANG..: Python3
TITULO: Program to generate code to app.py
DATA..: 08/08/2024
VERSÃO: 0.1.00
HOST..: diversos
LOCAL.: diversos
OBS...: colocar nas linhas abaixo informações importantes sobre o programa

DEPEND: (informar nas linhas abaixo os recursos necessários para utilização)

-------------------------------------------------------------------------
Copyright (c) 2022 - Vya.Digital
This script is licensed under GNU GPL version 2.0 or above
-------------------------------------------------------------------------
Modifications.....:
 Date          Rev    Author           Description
 08/08/2024     0     Yves Marinho      Elaboração
                      Chatgpt
-------------------------------------------------------------------------
PARÂMETROS (informar os parâmetros necessários no exemplo de utilização)
-
STATUS: (status emn que se encontra o código DEV/PROD)
DEV - pode adicionar dados adicionais para informar a fase
"""
import json
import logging
import sys
from os import path, makedirs
from jinja2 import Template


def configure_logging():
    if not logging.getLogger().hasHandlers():
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s - %(levelname)s - %(threadName)s - %(funcName)s:%(lineno)d - %(name)s - %(message)s"
        )

app_template = """
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_appbuilder import AppBuilder
from .database import db
from .views import register_views
from .models import {{ tables | join(', ') }}

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
"""

config_template = """
[parameters]
db_uri = sqlite:///%(here)s/app.db
"""

database_template = """
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
"""

models_template = """
import logging
from flask_sqlalchemy import SQLAlchemy

# Configuração do logging
logging = logging.getLogger(__name__)

try:
    db = SQLAlchemy()

    {% for table in tables %}
    class {{ table.class_name }}(db.Model):
        __tablename__ = '{{ table.name }}'
        {% for column in table.columns %}
        {{ column.name }} = db.Column(db.{{ column.type }}, {% if column.primary_key %}primary_key=True, {% endif %}{% if column.autoincrement %}autoincrement=True, {% endif %}{% if column.nullable is not none %}nullable={{ column.nullable }}, {% endif %}{% if column.default is not none %}default={{ column.default }}, {% endif %})
        {% endfor %}

    logging.info("Modelos criados com sucesso.")
    {% endfor %}

except Exception as e:
    logging.error("Erro ao criar os modelos: %s", e)
    raise
"""


def generate_app(db_structure: dict, project_folder: str) -> bool:
    try:
        configure_logging()
        logging.info("=== Função: %s ===" % (sys._getframe().f_code.co_name))
        logging.info("=== Parâmetros recebidos ===")
        logging.info(f"==> VAR: db_structure    TYPE: {type(db_structure)}, CONTENT: {db_structure}")
        logging.info(f"==> VAR: project_folder  TYPE: {type(project_folder)}, CONTENT: {project_folder}")
        
        if not db_structure or len(db_structure) == 0:
            logging.error("Parâmetro de entrada 'db_structure' não recebido ou incorreto.")
            return False
        
        if not project_folder or len(project_folder) == 0:
            logging.error("Parâmetro 'project_folder' não recebido.")
            return False
        
        if not path.exists(project_folder):
            makedirs(project_folder)
        
        tables = []
        for table in db_structure[0]['tables']:
            columns = []
            for column in table['columns']:
                columns.append({
                        'name'         : column['name'],
                        'type'         : column['type'],
                        'primary_key'  : 'PRIMARY KEY' in column.get('constraints', []),
                        'autoincrement': 'AUTO_INCREMENT' in column.get('constraints', []),
                        'nullable'     : 'NOT NULL' not in column.get('constraints', []),
                        'default'      : column.get('default', None)
                })
            tables.append({
                    'name'      : table['name'],
                    'class_name': table['name'].capitalize(),
                    'columns'   : columns
            })
        
        # Gerando o código dos arquivos do projeto
        template = Template(app_template)
        app_code = template.render(tables=[table['class_name'] for table in tables])
        template = Template(config_template)
        config_code = template.render()
        template = Template(database_template)
        database_code = template.render()
        template = Template(models_template)
        models_code = template.render(tables=tables)
        
        # Salvando os arquivos no diretório especificado
        with open(path.join(project_folder, 'app.py'), 'w') as file:
            file.write(app_code)
        
        with open(path.join(project_folder, 'config.ini'), 'w') as file:
            file.write(config_code)
        
        with open(path.join(project_folder, 'database.py'), 'w') as file:
            file.write(database_code)
        
        with open(path.join(project_folder, 'models.py'), 'w') as file:
            file.write(models_code)
        
        logging.info("Arquivos do projeto gerados com sucesso em %s", project_folder)
        return True
    
    except Exception as e:
        logging.error("Erro ao gerar os arquivos do projeto: %s", e)
        return False


if __name__ == "__main__":

    json_file_name = "db_structure.json"
    json_file_path = r"C:\Users\info\Documents\Projetos sysdev\Vya-Jobs\Flask-AppBuilder-cmdb\generator"
    json_file_path_name = path.join(json_file_path, json_file_name)
    
    with open(json_file_path_name) as json_file:
        db_structure = json.load(json_file)
    
    project_folder = r"C:\Users\info\Documents\Projetos sysdev\Vya-Jobs\Flask-AppBuilder-cmdb\flask_appbuilder"
    generate_app(db_structure, project_folder)
