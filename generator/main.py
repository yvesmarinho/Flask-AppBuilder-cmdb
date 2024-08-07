# -*- coding: utf-8 -*-
"""
-------------------------------------------------------------------------
NOME..: nome_do_programa.py
LANG..: Python3
TITULO: <<< DESCRIÇÃO DA FUNCIONALIDADE >>>
DATA..: 00/00/0000
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
from os import path
from modules.logging_config import configure_logging
from modules.config_reader import load_config
from modules.sql_parser import parse_sql_file
from modules.model_creator import create_models
# from modules.view_creator import create_views
# from modules.form_creator import create_forms
# from modules.controller_creator import create_controllers

logging.info(f"=== Programa: {__name__} ===")


def display_config(config):
    """
    Displays the contents of the ConfigParser object.

    :param config: The ConfigParser object containing the configuration.
    :type config: configparser.ConfigParser
    """
    try:
        logging.info(f"=== Função: {__name__} ===")
        logging.info("=== Parâmetros recebidos ===")
        logging.info(f"==> VAR: config TYPE: {type(config)}, CONTENT: {config}")
        for section in config.sections():
            logging.info(f"Section[{section}]")
            for key, value in config.items(section):
                logging.info(f"KEY:{key} = {value}")
            logging.info("\n")
    except Exception as errorMsg:
        logging.error(f"Error displaying config: {errorMsg}")
        logging.error("Exception occurred", exc_info=True)
        return False


def config_logging():
    if not logging.getLogger().hasHandlers():
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s - %(levelname)s - %(threadName)s - %(funcName)s:%(lineno)d - %(name)s - %(message)s"
        )


def main(app_name='vya_system_generator',
         path_config_ini=r"C:\Users\info\Documents\Projetos sysdev\Vya-Jobs\Flask-Appbuilder-cmdb\generator",
         file_config_ini='config.ini'):
    """
    Main function to control the execution of modules.

    :param app_name: The name of the application.
    :type app_name: str
    :param path_config_ini: The path to the config file.
    :type path_config_ini: str
    :param file_config_ini: The name of the config file.
    :type file_config_ini: str
    :return: True if the process completes successfully, else False.
    :rtype: bool
    """
    try:
        config_logging()
        logging.info(f"=== Starting: {__name__} ===")
        logging.info("=== Parâmetros recebidos ===")
        logging.info(f"==> VAR: app_name        TYPE: {type(app_name)}, CONTENT: {app_name}")
        logging.info(f"==> VAR: path_config_ini TYPE: {type(path_config_ini)}, CONTENT: {path_config_ini}")
        logging.info(f"==> VAR: file_config_ini TYPE: {type(file_config_ini)}, CONTENT: {file_config_ini}")
        
        if not all(isinstance(param, str) for param in [app_name, path_config_ini, file_config_ini]):
            logging.error("Invalid parameter type. Both path and file should be strings.")
            return False
        
        if not path.isfile(path.join(path_config_ini, file_config_ini)):
            logging.error("Config.ini dont exist.")
            return False
        
        logging.info("===> Carregando parâmetros do config.ini...")
        config = load_config(path_config_ini, file_config_ini)
        
        if not config:
            raise Exception("Failed to load config file.")
        
        display_config(config)
        
        if not configure_logging(config, app_name):
            raise Exception("Failed to configure logging.")
        
        logging.info("===> Validando parâmetros de banco de dados...")
        db_config = config['database_file']
        required_keys = ["db_path", "db_filename"]
        if not all(key in db_config for key in required_keys):
            logging.error("Inexistent parameter in database configuration.")
            return False
        
        logging.info("===> Validando existencia do database file...")
        sql_file_path = path.join(db_config['db_path'], db_config['db_filename'])
        if not path.isfile(sql_file_path):
            logging.error(f"{db_config['db_filename']} dont exist.")
            return False
        
        logging.info("===> Enviando SQL file para o parser...")
        db_structure = parse_sql_file(sql_file_path)
        if not db_structure:
            raise Exception("Failed to parse SQL file.")
        
        if not db_structure or not isinstance(db_structure, list):
            raise Exception("Failed to generate JSON.")

        logging.info(f"==> VAR: db_structure TYPE: {type(db_structure)}, LEN: {len(db_structure)}")

        logging.info("===> Enviando JSON para o gerador de modelos...")
        projetc_folder = config['project']['project_path']
        if not path.exists(projetc_folder):
            raise Exception(f"{projetc_folder} folder not found.")

        if not create_models(db_structure, projetc_folder):
            raise Exception("Failed to create models.")

        return

        # if not create_views(db_structure):
        #     raise Exception("Failed to create views.")
        #
        # if not create_forms(db_structure):
        #     raise Exception("Failed to create forms.")
        #
        # if not create_controllers(db_structure):
        #     raise Exception("Failed to create controllers.")
        
        logging.debug("Main function completed successfully.")
        return True
    except Exception as e:
        logging.error(f"Error in main function: {e}")
        return False


if __name__ == "__main__":
    main()