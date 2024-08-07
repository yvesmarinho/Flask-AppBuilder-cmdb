# -*- coding: utf-8 -*-
"""
-------------------------------------------------------------------------
NOME..: views_creator.py
LANG..: Python3
TITULO: Program to generate flask views.py
DATA..: 07/08/2024
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
 07/08/2024     0     Yves Marinho      Elaboração
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
from jinja2 import Template
from os import path


# Configuração do logging
def configure_logging():
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    return logger


views_template = """
import logging
from flask import Flask, render_template
from flask_appbuilder import AppBuilder, expose, BaseView
from .models import db, {{ tables | join(', ') }}

# Configuração do logging
logger = logging.getLogger(__name__)

def register_views(app: Flask):
    try:
        appbuilder = AppBuilder(app, db.session)

        {% for table in tables %}
        class {{ table }}View(BaseView):
            default_view = 'list'

            @expose('/list/')
            def list(self):
                items = db.session.query({{ table }}).all()
                return render_template('{{ table.lower() }}_list.html', items=items)

        appbuilder.add_view({{ table }}View, "{{ table }}", icon="fa-folder-open-o", category="Admin")
        {% endfor %}

        logger.info("Views registradas com sucesso.")

    except Exception as e:
        logger.error("Erro ao registrar as views: %s", e)
        raise
"""


def generate_views(db_structure: dict, project_folder: str) -> bool:
    try:
        logger = configure_logging()
        logger.info("=== Função: %s ===" % (sys._getframe().f_code.co_name))
        logger.info("=== Parâmetros recebidos ===")
        logger.info(f"==> VAR: db_structure    TYPE: {type(db_structure)}, CONTENT: {db_structure}")
        logger.info(f"==> VAR: project_folder  TYPE: {type(project_folder)}, CONTENT: {project_folder}")
        
        if not db_structure or len(db_structure) == 0:
            logger.error("Parâmetro de entrada 'db_structure' não recebido ou incorreto.")
            return False
        
        if not project_folder or len(project_folder) == 0:
            logger.error("Parâmetro 'project_folder' não recebido.")
            return False
        
        tables = [table['name'].capitalize() for table in db_structure[0]['tables']]
        
        # Gerando o código do arquivo views.py
        template = Template(views_template)
        views_code = template.render(tables=tables)
        
        # Salvando o arquivo views.py no diretório especificado
        views_path = path.join(project_folder, 'views.py')
        with open(views_path, 'w') as file:
            file.write(views_code)
        
        logger.info("Arquivo views.py gerado com sucesso em %s", views_path)
        return True
    
    except Exception as e:
        logger.error("Erro ao gerar views.py: %s", e)
        return False

if __name__ == "__main__":
    # Example usage
    json_file_name = "db_structure.json"
    json_file_path = r"C:\Users\info\Documents\Projetos sysdev\Vya-Jobs\Flask-AppBuilder-cmdb\generator"
    json_file_path_name = path.join(json_file_path, json_file_name)
    
    with open(json_file_path_name) as json_file:
        db_structure = json.load(json_file)
    project_folder = r"C:\Users\info\Documents\Projetos sysdev\Vya-Jobs\Flask-AppBuilder-cmdb\flask_appbuilder"
    generate_views(db_structure, project_folder)
