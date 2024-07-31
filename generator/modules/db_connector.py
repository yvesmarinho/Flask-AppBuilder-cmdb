# -*- coding: utf-8 -*-
"""
-------------------------------------------------------------------------
NOME..: db_connector.py
LANG..: Python3
TITULO: Programa para conectar o banco de dados.
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
import sqlalchemy
from sqlalchemy.orm import sessionmaker

logging.info(f"=== Programa: {__name__} ===")


def connect_db(db_type, db_user, db_password, db_host, db_port, db_name):
    """
    Connects to the database using SQLAlchemy.

    :param db_type: The type of the database (e.g., 'mysql', 'postgres').
    :type db_type: str
    :param db_user: The database user.
    :type db_user: str
    :param db_password: The database password.
    :type db_password: str
    :param db_host: The database host.
    :type db_host: str
    :param db_port: The database port.
    :type db_port: str
    :param db_name: The name of the database.
    :type db_name: str
    :return: SQLAlchemy session object if connection is successful, else False.
    :rtype: sqlalchemy.orm.session.Session or bool
    """
    try:
        logging.info(f"=== Função: {__name__} ===")
        logging.info("=== Parâmetros recebidos ===")
        logging.info(f"==> VAR: db_type     TYPE: {type(db_type)}, CONTENT: {db_type}")
        logging.info(f"==> VAR: db_user     TYPE: {type(db_user)}, CONTENT: {db_user}")
        logging.info(f"==> VAR: db_password TYPE: {type(db_password)}")
        logging.info(f"==> VAR: db_host     TYPE: {type(db_host)}, CONTENT: {db_host}")
        logging.info(f"==> VAR: db_port     TYPE: {type(db_port)}, CONTENT: {db_port}")
        logging.info(f"==> VAR: db_name     TYPE: {type(db_name)}, CONTENT: {db_name}")

        if not all(isinstance(param, str) for param in [db_type, db_user, db_password, db_host, db_port, db_name]):
            logging.error("Invalid parameter type or inexistent parameter.")
            return False

        if db_type == 'mysql':
            db_url = f'mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
        elif db_type == 'postgres':
            db_url = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
        else:
            logging.error(f"Unsupported database type: {db_type}")
            return False

        engine = sqlalchemy.create_engine(db_url)
        Session = sessionmaker(bind=engine)
        session = Session()

        logging.debug("Database connection successful.")
        return session
    except Exception as errorMsg:
        logging.error(f"Error connecting to database: {errorMsg}")
        logging.error("Exception occurred", exc_info=True)
        return False
