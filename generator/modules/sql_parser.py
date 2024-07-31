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

        with open(sql_file_path, 'r') as file:
            sql_lines = file.readlines()

        logging.info(f"==> VAR: sql_lines TYPE: {type(sql_lines)}, LEN: {len(sql_lines)}")

        db_structure = {}
        current_table = None
        columns = {}
        primary_keys = []
        foreign_keys = {}

        for line in sql_lines:
            line = line.strip()
            if line.startswith("CREATE TABLE"):
                if current_table:
                    db_structure[current_table] = {
                        'columns': columns,
                        'primary_keys': primary_keys,
                        'foreign_keys': foreign_keys
                    }
                current_table = line.split()[2].strip('`')
                columns = {}
                primary_keys = []
                foreign_keys = {}
            elif line.startswith("`"):
                parts = line.split()
                if len(parts) < 2:
                    continue
                column_name = parts[0].strip('`')
                column_type = ' '.join(parts[1:])
                columns[column_name] = column_type

                if "PRIMARY KEY" in line:
                    primary_keys.append(column_name)

                if "FOREIGN KEY" in line:
                    fk_parts = line.split("REFERENCES")
                    if len(fk_parts) > 1:
                        fk_table = fk_parts[1].split()[0].strip('`')
                        fk_column = fk_parts[1].split()[1].strip('`').strip('()')
                        foreign_keys[column_name] = {
                            'referred_table': fk_table,
                            'referred_column': fk_column
                        }
            elif line.startswith("PRIMARY KEY"):
                keys = line.split("(")[1].strip(")").split(",")
                for key in keys:
                    primary_keys.append(key.strip('`'))

            elif line.startswith("FOREIGN KEY"):
                parts = line.split()
                if len(parts) < 6:
                    continue
                column_name = parts[2].strip('`')
                fk_table = parts[4].strip('`')
                fk_column = parts[5].strip('`').strip('()')
                foreign_keys[column_name] = {
                    'referred_table': fk_table,
                    'referred_column': fk_column
                }

        if current_table:
            db_structure[current_table] = {
                'columns': columns,
                'primary_keys': primary_keys,
                'foreign_keys': foreign_keys
            }

        logging.info(f"==> VAR: db_structure TYPE: {type(db_structure)}, CONTENT: {db_structure}")
        logging.debug("SQL file parsed successfully.")
        return db_structure
    except Exception as e:
        logging.error(f"Error parsing SQL file: {e}")
        logging.exception("Exception occurred")
        return False
