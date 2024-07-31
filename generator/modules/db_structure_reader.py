# -*- coding: utf-8 -*-
"""
-------------------------------------------------------------------------
NOME..: db_structure_reader.py
LANG..: Python3
TITULO: Programa para ler a estrutura do banco do dados.
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
from sqlalchemy import MetaData
from sqlalchemy.orm import Session

logging.info(f"=== Programa: {__name__} ===")

def read_db_structure(session):
    """
    Reads the structure of the database using SQLAlchemy.

    :param session: The SQLAlchemy session object.
    :type session: sqlalchemy.orm.session.Session
    :return: Metadata object containing database structure, or False if an error occurs.
    :rtype: sqlalchemy.MetaData or bool
    """
    try:
        logging.info(f"=== Função: {__name__} ===")
        logging.info("=== Parâmetros recebidos ===")
        logging.info(f"==> VAR: session TYPE: {type(session)}")

        if not isinstance(session, Session):
            logging.error("session must be a SQLAlchemy session object.")
            return False
        
        metadata = MetaData()
        metadata.reflect(bind=session.bind)
        logging.debug("Database structure read successfully.")
        return metadata
    except Exception as errorMsg:
        logging.error(f"Error reading database structure: {errorMsg}")
        logging.error("Exception occurred", exc_info=True)
        return False
