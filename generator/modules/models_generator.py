# -*- coding: utf-8 -*-
"""
-------------------------------------------------------------------------
NOME..: models_generator.py
LANG..: Python3
TITULO: Program to generate models.py code
DATA..: 09/08/2024
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
 09/08/2024     0     Yves Marinho      Elaboração
                      Chatgpt
-------------------------------------------------------------------------
PARÂMETROS (informar os parâmetros necessários no exemplo de utilização)
-
STATUS: (status emn que se encontra o código DEV/PROD)
DEV - pode adicionar dados adicionais para informar a fase
"""
import json
import logging
import sys
from config_reader import load_config
from jinja2 import Environment, FileSystemLoader
from os import path


def load_json(json_file_path):
    """
    Carrega o arquivo JSON com a estrutura do banco de dados.

    :param json_file_path: Caminho completo do arquivo JSON.
    :type json_file_path: str
    :return: Dados carregados do arquivo JSON.
    :rtype: dict or bool
    """
    try:
        logging.info(f"=== Starting: %s ===" % (sys._getframe().f_code.co_name))
        logging.info("=== Parâmetros recebidos ===")
        logging.info(f"==> VAR: json_file_path TYPE: {type(json_file_path)}, CONTENT: {json_file_path}")
        with open(json_file_path, 'r', encoding='utf-8') as json_file:
            return json.load(json_file)
    except Exception as errorMsg:
        logging.error(f"Erro ao carregar o arquivo JSON: {errorMsg}")
        logging.error("Exception occurred", exc_info=True)
        return False


def generate_models(json_data: list, output_path: str, templates_path: str) -> bool:
    """
    Gera um único arquivo models.py que contém as definições de todas as tabelas de todos os bancos de dados.

    :param json_data: Lista de dicionários carregados do arquivo JSON, onde cada dicionário representa um banco de dados.
    :type json_data: list
    :param output_path: Caminho onde o arquivo models.py será gerado.
    :type output_path: str
    :param templates_path: Caminho para a pasta contendo os templates Jinja2.
    :type templates_path: str
    :return: True se o arquivo for gerado com sucesso.
    :rtype: bool
    """
    try:
        logging.info(f"=== Starting: %s ===" % (sys._getframe().f_code.co_name))
        logging.info("=== Parâmetros recebidos ===")
        logging.info(f"==> VAR: json_data TYPE: {type(json_data)}, CONTENT: {json_data}")
        logging.info(f"==> VAR: output_path TYPE: {type(output_path)}, CONTENT: {output_path}")
        logging.info(f"==> VAR: templates_path TYPE: {type(templates_path)}, CONTENT: {templates_path}")

        logging.info(f"==> Configura o ambiente Jinja2")
        env = Environment(loader=FileSystemLoader(templates_path))
        template = env.get_template('models_template.jinja2')

        logging.info(f"==> Renderiza o template com os dados")
        rendered_content = template.render(databases=json_data)

        model_file_path = path.join(output_path, 'models.py')
        logging.info(f"==> Salvando o conteúdo renderizado no arquivo {model_file_path}")
        with open(model_file_path, 'w', encoding='utf-8') as file:
            file.write(rendered_content)

        logging.info(f"Arquivo models.py gerado com sucesso em {model_file_path}")
        return True

    except Exception as errorMsg:
        logging.error(f"Erro ao gerar o arquivo models.py: {errorMsg}")
        logging.error("Exception occurred", exc_info=True)
        return False


def models_generator(path_config_ini, file_config_ini, json_file_name, json_file_path):
    """
    Função principal que orquestra o carregamento do JSON e a geração do models.py.

    :param path_config_ini: Caminho para a pasta contendo o arquivo config.ini.
    :type path_config_ini: str
    :param file_config_ini: Nome do arquivo config.ini.
    :type file_config_ini: str
    :param json_file_name: Nome do arquivo json com a estrutura do banco de dados.
    :type json_file_name: str
    :param json_file_path: path do arquivo json.
    :type json_file_path: str
    :return: True se a geração do models.py for bem-sucedida.
    :rtype: bool
    """
    try:
        logging.info(f"=== Starting: %s ===" % (sys._getframe().f_code.co_name))
        logging.info("=== Parâmetros recebidos ===")
        logging.info(f"==> VAR: path_config_ini TYPE: {type(path_config_ini)}, CONTENT: {path_config_ini}")
        logging.info(f"==> VAR: file_config_ini TYPE: {type(file_config_ini)}, CONTENT: {file_config_ini}")
        logging.info(f"==> VAR: json_file_name  TYPE: {type(json_file_name)}, CONTENT: {json_file_name}")
        logging.info(f"==> VAR: json_file_path  TYPE: {type(json_file_path)}, CONTENT: {json_file_path}")
        
        logging.info(f"==>  Carrega a configuração")
        config = load_config(path_config_ini, file_config_ini)
        
        logging.info(f"==> Carrega os parâmetros do arquivo config.ini")
        json_path_file_name = path.join(json_file_path, json_file_name)
        output_path = config['project']['project_path']
        templates_path = path.join(config['generator']['generator_path'], config['generator']['templates_path'])
        
        logging.info(f"==> Valida os parâmetros recebidos do arquivo config.ini")
        if not path.exists(json_path_file_name):
            logging.error(f"Arquivo {json_file_name} não encontrado")
            return False
        
        if not path.exists(output_path):
            logging.error(f"Diretório {output_path} não encontrado")
            return False
        
        if not path.exists(templates_path):
            logging.error(f"Diretório {templates_path} não encontrado")
            return False
        
        logging.info(f"==>  Carrega o JSON")
        json_data = load_json(json_path_file_name)
        if not json_data:
            logging.error("Erro ao carregar o JSON")
            return False
        
        logging.info(f"==>  Gera o models.py ")
        result_generate = generate_models(json_data, output_path, templates_path)
        if not result_generate:
            logging.error("Erro ao gerar o models.py")
            return False
        else:
            logging.info("Código models.py gerado com sucesso ")
            return True
    except Exception as errorMsg:
        logging.error(f"Erro no models_generator: {errorMsg}")
        logging.error("Exception occurred", exc_info=True)
        return False


def config_logging():
    """
    Configura o logging para a aplicação.

    :return: True se a configuração foi bem-sucedida.
    :rtype: bool
    """
    logger = logging.getLogger()
    if logger.hasHandlers():
        logger.handlers.clear()
    
    logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s - %(levelname)s - %(threadName)s - %(funcName)s:%(lineno)d - %(name)s - %(message)s"
    )
    logging.info(f"=== Função: {__name__} ===")
    return True


if __name__ == "__main__":
    config_logging()
    
    path_config_ini = r"C:\Users\info\Documents\Projetos sysdev\Vya-Jobs\Flask-AppBuilder-cmdb\generator"
    file_config_ini = "config.ini"
    json_file_name = "db_structure.json"
    json_file_path = r"C:\Users\info\Documents\Projetos sysdev\Vya-Jobs\Flask-AppBuilder-cmdb\generator"
    
    models_generator(path_config_ini, file_config_ini, json_file_name, json_file_path)
    print("Fim do processo")
