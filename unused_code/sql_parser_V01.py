# -*- coding: utf-8 -*-
"""
-------------------------------------------------------------------------
NOME..: sql_parser.py
LANG..: Python3
TITULO: Parses the SQL file to extract the database structure.
DATA..: 31/07/2024
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
 31/07/2024     0     Yves Marinho      Elaboração
                      Chatgpt
-------------------------------------------------------------------------
PARÂMETROS (informar os parâmetros necessários no exemplo de utilização)
-
STATUS: (status emn que se encontra o código DEV/PROD)
DEV - pode adicionar dados adicionais para informar a fase
"""
import logging
import sqlparse
from sqlparse.sql import IdentifierList, Identifier
from sqlparse.tokens import Keyword, DML

def is_subselect(parsed):
    logging.info(f"=== Starting: {__name__} ===")
    logging.info("=== Parâmetros recebidos ===")
    logging.info(f"==> VAR: parsed TYPE: {type(parsed)}, CONTENT: {parsed}")
    if not parsed.is_group:
        return False
    for item in parsed.tokens:
        if item.ttype is DML and item.value.upper() == 'SELECT':
            return True
    return False

def extract_table_identifiers(token_stream):
    logging.info(f"=== Starting: {__name__} ===")
    logging.info("=== Parâmetros recebidos ===")
    logging.info(f"==> VAR: token_stream TYPE: {type(token_stream)}, CONTENT: {token_stream}")
    
    identifiers = []
    for item in token_stream:
        if isinstance(item, IdentifierList):
            for identifier in item.get_identifiers():
                identifiers.append(identifier.get_real_name())
        elif isinstance(item, Identifier):
            identifiers.append(item.get_real_name())
    return identifiers

def parse_sql_file(sql_file_path):
    """
    Parses the SQL file to extract the database structure.

    :param sql_file_path: The path to the SQL file.
    :type sql_file_path: str
    :return: A dictionary representing the database structure, or False if an error occurs.
    :rtype: dict or bool
    """
    try:
        logging.info("=== Starting: modules.sql_parser ===")
        logging.info("=== Parâmetros recebidos ===")
        logging.info(f"==> VAR: sql_file_path TYPE: {type(sql_file_path)}, CONTENT: {sql_file_path}")

        with open(sql_file_path, 'r', encoding='utf-8') as file:
            sql_lines = file.readlines()

        logging.info(f"==> VAR: sql_lines TYPE: {type(sql_lines)}, LEN: {len(sql_lines)}")

        db_structure = {}
        current_db = None
        current_table = None
        statement_lines = []
        collecting_statement = False

        for line in sql_lines:
            line = line.strip()
            logging.info(f"Processing line: {line}")

            if "CREATE" in line.upper():
                collecting_statement = True
                logging.info("Create found")

            if collecting_statement:
                statement_lines.append(line)
                if ";" in line:
                    statement = " ".join(statement_lines)
                    logging.info(f"Collected statement: {statement}")
                    parsed = sqlparse.parse(statement)[0]

                    if parsed.get_type() == 'CREATE':
                        logging.info(f"Collected statement: {statement}")
                        tokens = [token for token in parsed.tokens if not token.is_whitespace]
                        if tokens[0].value.upper() == 'CREATE':
                            if 'TABLE' in tokens[2].value.upper():
                                table_name = tokens[4].get_real_name()
                                schema_name = tokens[2].get_real_name()
                                if schema_name not in db_structure:
                                    db_structure[schema_name] = {}
                                current_table = table_name
                                columns = {}
                                primary_keys = []
                                foreign_keys = {}

                                for token in tokens:
                                    if token.ttype is None and isinstance(token, IdentifierList):
                                        for identifier in token.get_identifiers():
                                            column_definition = str(identifier)
                                            column_parts = column_definition.split()
                                            column_name = column_parts[0].strip('`')
                                            column_type = ' '.join(column_parts[1:])
                                            columns[column_name] = column_type
                                            if 'PRIMARY KEY' in column_type.upper():
                                                primary_keys.append(column_name)
                                            elif 'FOREIGN KEY' in column_type.upper():
                                                fk_info = column_type.split('REFERENCES')
                                                referenced_column = fk_info[1].strip().split()[0].strip('(),')
                                                foreign_keys[column_name] = referenced_column

                                db_structure[schema_name][current_table] = {
                                    'columns': columns,
                                    'primary_keys': primary_keys,
                                    'foreign_keys': foreign_keys
                                }
                                logging.info(f"Table added: {schema_name}.{current_table}")

                    statement_lines = []
                    collecting_statement = False

        logging.info(f"==> VAR: db_structure TYPE: {type(db_structure)}, CONTENT: {db_structure}")
        logging.debug("SQL file parsed successfully.")
        return db_structure
    except Exception as e:
        logging.error(f"Error parsing SQL file: {e}")
        logging.exception("Exception occurred")
        return False
