# -*- coding: utf-8 -*-
"""
-------------------------------------------------------------------------
NOME..: config_ini_handler.py
LANG..: Python3
TITULO: programa para manipulação de arquivos de configuração INI
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
 Date          Rev    Author            Description
 31/07/2024     0     Yves Marinho      Elaboração
                      Chatgpt
-------------------------------------------------------------------------
PARÂMETROS (informar os parâmetros necessários no exemplo de utilização)
-
STATUS: (status emn que se encontra o código DEV/PROD)
DEV - pode adicionar dados adicionais para informar a fase
"""
from os import path
import configparser
import logging
import sys

logging.info(f"=== Programa: {__name__} ===")


def load_config(file_path, file_name):
    """
    Loads the entire configuration file.

    :param file_path: The path to the config file.
    :type file_path: str
    :param file_name: The name of the config file.
    :type file_name: str
    :return: ConfigParser object containing the configuration, or False if an error occurs.
    :rtype: configparser.ConfigParser or bool

    :example:
    >>> config = load_config('.', 'config.ini')
    >>> config['database']['db_user']
    'user'
    """
    try:
        logging.info(f"=== Função: {__name__} ===")
        logging.info("=== Parâmetros recebidos ===")
        logging.info(f"==> VAR: file_path TYPE: {type(file_path)}, CONTENT: {file_path}")
        logging.info(f"==> VAR: file_name TYPE: {type(file_name)}, CONTENT: {file_name}")
        
        # Validate parameters
        if not all(isinstance(param, str) for param in [file_path, file_name]):
            logging.error("Invalid parameter type. Both path and file should be strings.")
            return False
        if not path.exists(path.join(file_path,file_name)):
            logging.error("Path does not exist.")
            return False
        if not path.isfile(path.join(file_path,file_name)):
            logging.error("File does not exist")
            return False
        
        config = configparser.ConfigParser()
        config.read(path.join(file_path,file_name))
        
        logging.debug("Config file loaded successfully.")
        return config
    except Exception as errorMsg:
        logging.error(f"Error loading config file: {errorMsg}")
        logging.error("Exception occurred", exc_info=True)
        return False
