# -*- coding: utf-8 -*-
"""
-------------------------------------------------------------------------
NOME..: db_loader.py
LANG..: Python3
TITULO: Programa para carregar a estrutura de banco de dados de um arquivo SQL.
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
from sqlalchemy import create_engine

def load_db_structure(session, sql_file_path):
    """
    Loads the database structure from a SQL file.

    :param session: The SQLAlchemy session object.
    :type session: sqlalchemy.orm.session.Session
    :param sql_file_path: The path to the SQL file.
    :type sql_file_path: str
    :return: True if the structure is loaded successfully, else False.
    :rtype: bool
    """
    try:
        logging.info(f"=== Função: {__name__} ===")
        logging.info(f"=== Parâmetros recebidos ===")
        logging.info(f"==> VAR: session       TYPE: {type(session)}")
        logging.info(f"==> VAR: sql_file_path TYPE: {type(sql_file_path)}, CONTENT: {sql_file_path}")

        with open(sql_file_path, 'r') as file:
            sql = file.read()

        engine = session.bind
        with engine.connect() as connection:
            connection.execute(sql)

        logging.debug("Database structure loaded successfully from SQL file.")
        return True
    except Exception as e:
        logging.error(f"Error loading database structure from SQL file: {e}")
        logging.error("Exception occurred", exc_info=True)
        return False
