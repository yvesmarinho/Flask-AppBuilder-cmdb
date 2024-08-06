# -*- coding: utf-8 -*-
"""
-------------------------------------------------------------------------
NOME..: json_generator.py
LANG..: Python3
TITULO: programa para gerar arquivo JSON com a estrutura do banco de dados
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
import json
import logging

logging.info(f"=== Programa: {__name__} ===")

def generate_json(db_structure):
    """
    Generates a JSON representation of the database structure.

    :param metadata: The metadata object containing database structure.
    :type metadata: sqlalchemy.MetaData
    :return: JSON string representing the database structure, or False if an error occurs.
    :rtype: str or bool
    """
    try:
        logging.info(f"=== Função: {__name__} ===")
        logging.info("=== Parâmetros recebidos ===")
        logging.info(f"==> VAR: db_structure TYPE: {type(db_structure)}")

        if not isinstance(metadata, dict):
            logging.error("The metadata object must be of type sqlalchemy.MetaData.")
            return False
        
        db_structure_json = json.dumps(db_structure, indent=4)

        logging.debug("Database structure JSON generated successfully.")
        return db_structure_json
    except Exception as errorMsg:
        logging.error(f"Error generating JSON: {errorMsg}")
        logging.error("Exception occurred", exc_info=True)
        return False
