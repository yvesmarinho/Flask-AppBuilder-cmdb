# -*- coding: utf-8 -*-
"""
-------------------------------------------------------------------------
NOME..: db_handler.py
LANG..: Python3
TITULO: Manipulação do banco de dados e conversão para JSON
DATA..: 31/07/2024
VERSÃO: 0.1.00
HOST..: diversos
LOCAL.: diversos
OBS...: colocar nas linhas abaixo informações importantes sobre o programa

DEPEND: (informar nas linhas abaixo os recursos necessários para utilização)
sqlalchemy
-------------------------------------------------------------------------
Copyright (c) 2022 - Vya.Digital
This script is licensed under GNU GPL version 2.0 or above
-------------------------------------------------------------------------
Modifications.....:
 Date          Rev    Author           Description
 31/07/2024     0     Yves Marinho     Elaboração
                      Chatgpt
-------------------------------------------------------------------------
PARÂMETROS (informar os parâmetros necessários no exemplo de utilização)
-
STATUS: (status emn que se encontra o código DEV/PROD)
DEV - pode adicionar dados adicionais para informar a fase
"""
import logging
from sqlalchemy import create_engine, inspect
import traceback

logging.info("=== Programa: %s" % (__file__))

def read_db_and_convert_to_json(db_config: dict) -> dict:
    """
    Conecta ao banco de dados usando as configurações fornecidas e converte a estrutura do banco de dados para JSON.

    :param db_config: Configurações do banco de dados.
    :type db_config: dict
    :return: Estrutura do banco de dados em formato JSON.
    :rtype: dict
    :raises ValueError: Se a conexão com o banco de dados falhar.

    >>> db_config = {
    ...     "db_type": "mysql",
    ...     "db_host": "localhost",
    ...     "db_port": 3306,
    ...     "db_name": "test_db",
    ...     "db_user": "user",
    ...     "db_password": "password"
    ... }
    >>> db_structure = read_db_and_convert_to_json(db_config)
    >>> isinstance(db_structure, dict)
    True
    """
    logging.info("=== Função: read_db_and_convert_to_json ===")

    try:
        db_type = db_config['db_type']
        db_user = db_config['db_user']
        db_password = db_config['db_password']
        db_host = db_config['db_host']
        db_port = db_config['db_port']
        db_name = db_config['db_name']

        connection_string = f"{db_type}://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        engine = create_engine(connection_string)
        inspector = inspect(engine)

        db_structure = {}
        for table_name in inspector.get_table_names():
            table_info = {
                'columns': [],
                'foreign_keys': [],
                'indexes': []
            }

            for column in inspector.get_columns(table_name):
                table_info['columns'].append({
                    'name': column['name'],
                    'type': str(column['type']),
                    'nullable': column['nullable'],
                    'default': column['default']
                })

            for fk in inspector.get_foreign_keys(table_name):
                table_info['foreign_keys'].append({
                    'constrained_columns': fk['constrained_columns'],
                    'referred_schema': fk['referred_schema'],
                    'referred_table': fk['referred_table'],
                    'referred_columns': fk['referred_columns']
                })

            for index in inspector.get_indexes(table_name):
                table_info['indexes'].append({
                    'name': index['name'],
                    'unique': index['unique'],
                    'column_names': index['column_names']
                })

            db_structure[table_name] = table_info

        logging.info("=== Termino Função: read_db_and_convert_to_json ===")
        return db_structure
    except Exception as e:
        logging.error("Exception occurred", exc_info=True)
        logging.error(e)
        raise ValueError("Erro ao conectar e ler o banco de dados")

# Exemplo de uso:
# db_config = read_config_ini()
# db_structure = read_db_and_convert_to_json(db_config)
# print(json.dumps(db_structure, indent=4))