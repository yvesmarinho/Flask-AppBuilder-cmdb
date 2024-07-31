# -*- coding: utf-8 -*-
"""
-------------------------------------------------------------------------
NOME..: logging_config.py
LANG..: Python3
TITULO: Configuração de logging
DATA..: 31/07/2024
VERSÃO: 0.1.00
HOST..: diversos
LOCAL.: diversos
OBS...: Configuração de logging para o aplicativo.

DEPEND: (nenhuma dependência específica)
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
STATUS: DEV
"""
import configparser
import logging
from os import path, makedirs

logging.info(f"=== Programa: {__name__} ===")

def configure_logging(config, app_name):
    """
    Configures logging for the application.

    :param config: The ConfigParser object containing the configuration.
    :type config: configparser.ConfigParser
    :param app_name: The ConfigParser object containing the configuration.
    :type app_name: str
    :return: True if logging is configured successfully, else False.
    :rtype: bool
    """
    try:
        logging.info(f"=== Função: {__name__} ===")
        logging.info("=== Parâmetros recebidos ===")
        logging.info(f"==> VAR: config   TYPE: {type(config)}, CONTENT: {config}")
        logging.info(f"==> VAR: app_name TYPE: {type(app_name)}, CONTENT: {app_name}")

        if not isinstance(config, configparser.ConfigParser):
            logging.error("Configuration must be a ConfigParser object.")
            return False

        log_file = app_name + ".log"
        log_path = config.get('logging', 'log_path')
        log_level = config.get('logging', 'log_level').upper()
        
        if not path.exists(log_path):
            makedirs(log_path)

        log_full_path = path.join(log_path, log_file)

        # Create a logger
        logger = logging.getLogger()
        logger.setLevel(log_level)
        
        # File handler
        file_handler = logging.FileHandler(log_full_path)
        file_handler.setLevel(log_level)
        file_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(threadName)s - %(funcName)s:%(lineno)d - %(name)s - %(message)s")
        file_handler.setFormatter(file_formatter)
        
        # Stream handler (console output)
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(log_level)
        stream_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(threadName)s - %(funcName)s:%(lineno)d - %(name)s - %(message)s")
        stream_handler.setFormatter(stream_formatter)
        
        # Add handlers to the logger
        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)
        
        logging.debug("Logging configured successfully.")
        return True
    except Exception as errorMsg:
        logging.error(f"Error configuring logging: {errorMsg}")
        logging.error("Exception occurred", exc_info=True)
        return False