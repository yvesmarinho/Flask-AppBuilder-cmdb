# -*- coding: utf-8 -*-
"""
-------------------------------------------------------------------------
NOME..: run_generator.py
LANG..: Python3
TITULO: Program to generate run.py code.
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
import logging
import sys
from os import path
from jinja2 import Environment, FileSystemLoader, TemplateNotFound
from config_reader import load_config


def config_logging():
    logger = logging.getLogger()
    if logger.hasHandlers():
        logger.handlers.clear()
    
    logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s - %(levelname)s - %(threadName)s - %(funcName)s:%(lineno)d - %(name)s - %(message)s"
    )
    logging.info(f"=== Função: {__name__} ===")
    return True


def generate_run_py(config):
    try:
        logging.info("=== Função: %s ===" % (sys._getframe().f_code.co_name))
        logging.info("=== Parâmetros recebidos ===")
        logging.info(f"==> VAR: config TYPE: {type(config)}, CONTENT: {config}")
        
        logging.info("Configurando o ambiente Jinja2 usando o path dos templates definido no config.ini")
        templates_path = path.join(config['generator']['generator_path'], config['generator']['templates_path'])
        logging.info(f"Templates path: {templates_path}")
        
        env = Environment(loader=FileSystemLoader(templates_path))
        
        logging.info("Carregando o template do run.py")
        try:
            template = env.get_template('run_template.py.jinja')
        except TemplateNotFound as e:
            logging.error(f"Template não encontrado: {e}")
            return False
        
        logging.info("Renderizando o template com os parâmetros de configuração")
        logging.info(f"==> VAR: HOST TYPE: {type(config['flask']['HOST'])}, CONTENT: {config['flask']['HOST']}")
        logging.info(f"==> VAR: PORT TYPE: {type(config['flask'].getint('PORT'))}, CONTENT: {config['flask'].getint('PORT')}")
        logging.info(f"==> VAR: DEBUG TYPE: {type(config['flask'].getboolean('DEBUG'))}, CONTENT: {config['flask'].getboolean('DEBUG')}")
        output_from_parsed_template = template.render(
                host=config['flask']['HOST'],
                port=config['flask'].getint('PORT'),
                debug=config['flask'].getboolean('DEBUG')
        )
        
        logging.info("Definindo o caminho completo do arquivo run.py que será gerado")
        output_path = path.join(config['project']['project_path'], 'run.py')
        
        logging.info("Escrevendo o conteúdo renderizado no arquivo run.py")
        with open(output_path, 'w') as run_file:
            run_file.write(output_from_parsed_template)
        
        logging.info(f"Arquivo run.py gerado com sucesso em: {output_path}")
        return True
    
    except Exception as errorMsg:
        logging.error(f"Erro ao gerar o arquivo run.py: {errorMsg}")
        logging.error("Exception occurred", exc_info=True)
        return False


def run_generator(path_config_ini: str, file_config_ini: str) -> bool:
    try:
        logging.info("=== Função: %s ===" % (sys._getframe().f_code.co_name))
        logging.info("=== Parâmetros recebidos ===")
        logging.info(f"==> VAR: path_config_ini    TYPE: {type(path_config_ini)}, CONTENT: {path_config_ini}")
        logging.info(f"==> VAR: file_config_ini    TYPE: {type(file_config_ini)}, CONTENT: {file_config_ini}")
        
        logging.info("Lendo as configurações do arquivo config.ini")
        config = load_config(path_config_ini, file_config_ini)
        
        logging.info("Iniciando a geração do arquivo run.py")
        if not generate_run_py(config):
            logging.error("Falha ao gerar o arquivo run.py")
            return False
        
        return True
    
    except Exception as errorMsg:
        logging.error(f"Erro na execução do run_generator.py: {errorMsg}")
        logging.error("Exception occurred", exc_info=True)
        return False


if __name__ == "__main__":
    config_logging()
    
    path_config_ini = r"C:\Users\info\Documents\Projetos sysdev\Vya-Jobs\Flask-AppBuilder-cmdb\generator"
    file_config_ini = "config.ini"
    
    run_generator(path_config_ini, file_config_ini)
