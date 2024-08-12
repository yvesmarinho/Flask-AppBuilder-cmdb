# -*- coding: utf-8 -*-
"""
-------------------------------------------------------------------------
NOME..: models_generator.py
LANG..: Python3
TITULO: Program to generate models.py code
DATA..: 09/08/2024
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
 09/08/2024     0     Yves Marinho      Elaboração
                      Chatgpt
-------------------------------------------------------------------------
PARÂMETROS (informar os parâmetros necessários no exemplo de utilização)
-
STATUS: (status emn que se encontra o código DEV/PROD)
DEV - pode adicionar dados adicionais para informar a fase
"""
import json
import logging
import re
from configparser import ConfigParser
from jinja2 import Environment, FileSystemLoader
from os import path


def config_logging():
    """
    Configura o logging para a aplicação.

    :return: True se a configuração foi bem-sucedida.
    :rtype: bool
    """
    logger = logging.getLogger()
    if logger.hasHandlers():
        logger.handlers.clear()
    
    logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s - %(levelname)s - %(threadName)s - %(funcName)s:%(lineno)d - %(name)s - %(message)s"
    )
    logging.info(f"=== Função: {__name__} ===")
    return True


def convert_sql_to_sqlalchemy_type(sql_type):
    """
    Converte o tipo de dado SQL para o tipo correspondente no SQLAlchemy.

    :param sql_type: Tipo de dado SQL.
    :type sql_type: str
    :return: Tipo de dado correspondente no SQLAlchemy.
    :rtype: str
    """
    logging.info(f"=== Starting: convert_sql_to_sqlalchemy_type ===")
    logging.info("=== Parâmetros recebidos ===")
    logging.info(f"==> VAR: sql_type TYPE: {type(sql_type)}, CONTENT: {sql_type}")
    sql_type = sql_type.upper()
    varchar_match = re.match(r"VARCHAR\((\d+)\)", sql_type)
    char_match = re.match(r"CHAR\((\d+)\)", sql_type)
    
    sql_type = sql_type.upper()

    # Regex para capturar tipos com parâmetros, como DECIMAL(10,2) ou INT(10)
    type_with_params = re.match(r"(\w+)\(([\d,]+)\)", sql_type)

    if type_with_params:
        base_type = type_with_params.group(1)
        params = type_with_params.group(2)

        if base_type in ["VARCHAR", "CHAR"]:
            return f"String({params})"
        elif base_type in ["INT", "INTEGER", "SMALLINT", "TINYINT", "MEDIUMINT", "BIGINT"]:
            return f"Integer({params})"
        elif base_type in ["DECIMAL", "NUMERIC"]:
            return f"DECIMAL({params})"
        elif base_type in ["FLOAT", "DOUBLE"]:
            return f"Float({params})"
    else:
        if "VARCHAR" in sql_type or "CHAR" in sql_type:
            return "String"
        elif "INT" in sql_type or "INTEGER" in sql_type:
            return "Integer"
        elif "SMALLINT" in sql_type:
            return "SmallInteger"
        elif "TINYINT" in sql_type:
            return "SmallInteger"
        elif "MEDIUMINT" in sql_type:
            return "Integer"
        elif "BIGINT" in sql_type:
            return "BigInteger"
        elif "TEXT" in sql_type:
            return "Text"
        elif "DECIMAL" in sql_type or "NUMERIC" in sql_type:
            return "DECIMAL"
        elif "FLOAT" in sql_type:
            return "Float"
        elif "DOUBLE" in sql_type:
            return "Float"
        elif "DATE" in sql_type and "TIME" not in sql_type:
            return "Date"
        elif "DATETIME" in sql_type or "TIMESTAMP" in sql_type:
            return "DateTime"
        elif "TIME" in sql_type:
            return "Time"
        elif "ENUM" in sql_type:
            return "Enum"
        elif "BOOLEAN" in sql_type or "BOOL" in sql_type:
            return "Boolean"
        elif "JSON" in sql_type:
            return "JSON"
        else:
            return sql_type  # Retorna o tipo original se não for mapeado
def load_json(json_file_path):
    """
    Carrega o arquivo JSON com a estrutura do banco de dados.

    :param json_file_path: Caminho completo do arquivo JSON.
    :type json_file_path: str
    :return: Dados carregados do arquivo JSON.
    :rtype: dict or bool
    """
    try:
        logging.info(f"=== Starting: load_json ===")
        logging.info(f"==> VAR: json_file_path TYPE: {type(json_file_path)}, CONTENT: {json_file_path}")
        with open(json_file_path, 'r', encoding='utf-8') as json_file:
            return json.load(json_file)
    except Exception as errorMsg:
        logging.error(f"Erro ao carregar o arquivo JSON: {errorMsg}")
        logging.error("Exception occurred", exc_info=True)
        return False


def load_config(config_file_path):
    """
    Carrega o arquivo de configuração INI.

    :param config_file_path: Caminho completo do arquivo de configuração.
    :type config_file_path: str
    :return: Objeto ConfigParser carregado.
    :rtype: ConfigParser or bool
    """
    try:
        logging.info(f"=== Starting: load_config ===")
        logging.info(f"==> VAR: config_file_path TYPE: {type(config_file_path)}, CONTENT: {config_file_path}")
        config = ConfigParser()
        config.read(config_file_path)
        return config
    except Exception as errorMsg:
        logging.error(f"Erro ao carregar o arquivo de configuração: {errorMsg}")
        logging.error("Exception occurred", exc_info=True)
        return False


def generate_model(db_name, table_data, output_path, templates_path):
    """
    Gera uma parte do arquivo models.py para uma tabela específica.

    :param db_name: Nome do banco de dados.
    :type db_name: str
    :param table_data: Dados da tabela.
    :type table_data: dict
    :param output_path: Caminho onde o arquivo models.py será gerado.
    :type output_path: str
    :param templates_path: Caminho para a pasta contendo os templates Jinja2.
    :type templates_path: str
    :return: True se o arquivo for gerado com sucesso.
    :rtype: bool
    """
    try:
        logging.info(f"=== Starting: generate_model ===")
        logging.info(f"==> VAR: db_name TYPE: {type(db_name)}, CONTENT: {db_name}")
        logging.info(f"==> VAR: table_data TYPE: {type(table_data)}, CONTENT: {table_data}")
        logging.info(f"==> VAR: output_path TYPE: {type(output_path)}, CONTENT: {output_path}")
        logging.info(f"==> VAR: templates_path TYPE: {type(templates_path)}, CONTENT: {templates_path}")

        logging.info(f"==> Configura o ambiente Jinja2")
        env = Environment(loader=FileSystemLoader(templates_path))
        template = env.get_template('models_template.jinja2')

        logging.info(f"==> Construindo o código para a tabela {table_data['name']}")

        # Preparar as colunas
        columns = []
        repr_columns = []
        for column in table_data['columns']:
            column_type = convert_sql_to_sqlalchemy_type(column['type'])
            column_def = f"{column['name']} = Column({column_type}"
            if "NOT NULL" in column['constraints']:
                column_def += ", nullable=False"
            if "PRIMARY KEY" in column['constraints']:
                column_def += ", primary_key=True"
            if "AUTO_INCREMENT" in column['constraints']:
                column_def += ", autoincrement=True"
            column_def += ")"
            columns.append(column_def)

            repr_columns.append(f"{column['name']}={{ '{{' }} self.{column['name']} {{ '}}' }}")

        repr_str = f"<{table_data['name'].capitalize()}({', '.join(repr_columns)})>"

        # Preparar os índices
        indexes = []
        if 'indexes' in table_data:
            for idx in table_data['indexes']:
                index_def = f"Index('{idx['name']}', {', '.join(idx['columns'])})"
                indexes.append(index_def)

        # Preparar os índices únicos
        unique_indexes = []
        if 'unique' in table_data:
            for unique in table_data['unique']:
                unique_def = f"Index('{unique['name']}', {', '.join(unique['columns'])}, unique=True)"
                unique_indexes.append(unique_def)

        # Preparar as chaves estrangeiras
        foreign_keys = []
        if 'foreign_keys' in table_data:
            for fk in table_data['foreign_keys']:
                fk_def = f"{fk['column']} = Column(ForeignKey('{fk['references']['table']}.{fk['references']['column']}')"
                if 'on_delete' in fk['references']:
                    fk_def += f", ondelete='{fk['references']['on_delete']}'"
                if 'on_update' in fk['references']:
                    fk_def += f", onupdate='{fk['references']['on_update']}'"
                fk_def += ")"
                foreign_keys.append(fk_def)

        # Renderizar o template
        rendered_content = template.render(
            db_name=db_name,
            table_name=table_data['name'],
            columns=columns,
            indexes=indexes,
            unique_indexes=unique_indexes,
            foreign_keys=foreign_keys,
            repr_str=repr_str
        )

        # Escrever no arquivo models.py
        model_file_path = path.join(output_path, 'models.py')
        logging.info(f"==> Salvando o conteúdo renderizado no arquivo {model_file_path}")
        with open(model_file_path, 'a', encoding='utf-8') as file:  # Abrir no modo append
            file.write(rendered_content + "\n\n")  # Adiciona uma linha em branco após cada classe

        logging.info(f"Parte do arquivo models.py gerada com sucesso para a tabela {table_data['name']}")
        return True

    except Exception as errorMsg:
        logging.error(f"Erro ao gerar a parte do arquivo models.py: {errorMsg}")
        logging.error("Exception occurred", exc_info=True)
        return False


def models_generator(path_config_ini, file_config_ini, json_file_name, json_file_path):
    """
    Função principal que orquestra o carregamento do JSON e a geração do models.py.

    :param path_config_ini: Caminho para a pasta contendo o arquivo config.ini.
    :type path_config_ini: str
    :param file_config_ini: Nome do arquivo config.ini.
    :type file_config_ini: str
    :param json_file_name: Nome do arquivo json com a estrutura do banco de dados.
    :type json_file_name: str
    :param json_file_path: path do arquivo json.
    :type json_file_path: str
    :return: True se a geração do models.py for bem-sucedida.
    :rtype: bool
    """
    try:
        logging.info(f"=== Starting: models_generator ===")
        logging.info(f"=== Parâmetros recebidos ===")
        logging.info(f"==> VAR: path_config_ini TYPE: {type(path_config_ini)}, CONTENT: {path_config_ini}")
        logging.info(f"==> VAR: file_config_ini TYPE: {type(file_config_ini)}, CONTENT: {file_config_ini}")
        logging.info(f"==> VAR: json_file_name  TYPE: {type(json_file_name)}, CONTENT: {json_file_name}")
        logging.info(f"==> VAR: json_file_path  TYPE: {type(json_file_path)}, CONTENT: {json_file_path}")
        
        logging.info(f"==> Carrega a configuração")
        config = load_config(path.join(path_config_ini, file_config_ini))
        if not config:
            logging.error("Erro ao carregar o arquivo de configuração")
            return False
        
        logging.info(f"==> Carrega os parâmetros do arquivo config.ini")
        json_path_file_name = path.join(json_file_path, json_file_name)
        logging.info(f"==> VAR: json_path_file_name TYPE: {type(json_path_file_name)}, CONTENT: {json_path_file_name}")
        output_path = config['project']['project_path']
        templates_path = path.join(config['generator']['generator_path'], config['generator']['templates_path'])
        
        logging.info(f"==> Valida os parâmetros recebidos do arquivo config.ini")
        if not path.exists(json_path_file_name):
            logging.error(f"Arquivo {json_file_name} não encontrado")
            return False
        
        if not path.exists(output_path):
            logging.error(f"Diretório {output_path} não encontrado")
            return False
        
        if not path.exists(templates_path):
            logging.error(f"Diretório {templates_path} não encontrado")
            return False
        
        logging.info(f"==> Carrega o JSON")
        json_data = load_json(json_path_file_name)
        if not json_data:
            logging.error("Erro ao carregar o JSON")
            return False
        
        logging.info(f"==> Inicia a geração do models.py para cada tabela de cada banco de dados")
        # Limpa o conteúdo anterior do arquivo models.py
        with open(path.join(output_path, 'models.py'), 'w', encoding='utf-8') as file:
            # Adiciona os imports necessários
            file.write(
                    "from sqlalchemy import Column, Integer, String, ForeignKey, Date, DECIMAL, Text, Index, DateTime, JSON, Enum\n"
                    "from sqlalchemy.orm import relationship\n"
                    "from flask_appbuilder import Model\n\n"
            )
        
        # Itera sobre cada banco de dados e suas tabelas
        for db in json_data:
            db_name = db['database']
            logging.info(f"==> Processando banco de dados: {db_name}")
            for table in db['tables']:
                logging.info(f"==> Processando tabela: {table['name']} do banco de dados: {db_name}")
                if not generate_model(db_name, table, output_path, templates_path):
                    return False
        
        logging.info("Geração do models.py concluída com sucesso")
        return True
    
    except Exception as errorMsg:
        logging.error(f"Erro no models_generator: {errorMsg}")
        logging.error("Exception occurred", exc_info=True)
        return False


if __name__ == "__main__":
    config_logging()
    
    path_config_ini = r"C:\Users\info\Documents\Projetos sysdev\Vya-Jobs\Flask-AppBuilder-cmdb\generator"
    file_config_ini = "config.ini"
    json_file_name = "db_structure.json"
    json_file_path = r"C:\Users\info\Documents\Projetos sysdev\Vya-Jobs\Flask-AppBuilder-cmdb\generator"
    
    models_generator(path_config_ini, file_config_ini, json_file_name, json_file_path)
    print("Fim do processo")
