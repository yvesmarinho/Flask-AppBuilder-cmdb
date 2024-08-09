# -*- coding: utf-8 -*-
"""
-------------------------------------------------------------------------
NOME..: app_generator.py
LANG..: Python3
TITULO: Program to generate app.py code
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
import jinja2
import logging
import sys
from config_reader import load_config
from os import path


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


def render_template(template_path, output_path, context):
    """
    Renderiza um template Jinja2 e salva o resultado em um arquivo.

    :param template_path: Caminho do template Jinja2.
    :type template_path: str
    :param output_path: Caminho de saída do arquivo gerado.
    :type output_path: str
    :param context: Contexto para renderização do template.
    :type context: dict
    :return: True se a renderização for bem-sucedida, False caso contrário.
    :rtype: bool
    """
    try:
        logging.info("=== Função: %s ===" % (sys._getframe().f_code.co_name))
        logging.info("=== Parâmetros recebidos ===")
        logging.info(f"==> VAR: template_path TYPE: {type(template_path)}, CONTENT: {template_path}")
        logging.info(f"==> VAR: output_path TYPE: {type(output_path)}, CONTENT: {output_path}")
        logging.info(f"==> VAR: context TYPE: {type(context)}, CONTENT: {context}")
        
        logging.info(f"===> Validando se o template existe")
        if not path.exists(template_path):
            logging.error(f"Template {template_path} não encontrado")
            return False
        
        logging.info(f"===> Abrindo arquivo do template")
        with open(template_path) as file_:
            template = jinja2.Template(file_.read())
        
        output_from_parsed_template = template.render(context)
        
        ## inserir validação
        if not output_from_parsed_template:
            logging.error("Falha ao renderizar o template. O conteúdo está vazio.")
            return False
        
        logging.info(f"===> Gerando o arquivo {output_path}")
        with open(output_path, "w") as fh:
            fh.write(output_from_parsed_template)
        
        if not path.exists(output_path):
            logging.error(f"Template {output_path} não gerado")
            return False
        
        logging.info(f"Código gerado com sucesso em {output_path}")
        return True
    except Exception as errorMsg:
        logging.error(f"Erro ao renderizar o template: {errorMsg}")
        logging.error("Exception occurred", exc_info=True)
        
        return False


def generate_app_py(config):
    """
    Gera o arquivo app.py utilizando o template Jinja2 e as configurações fornecidas.

    :param config: Configurações carregadas do arquivo INI.
    :type config: configparser.ConfigParser
    :return: True se a geração for bem-sucedida, False caso contrário.
    :rtype: bool
    """
    try:
        logging.info("=== Função: %s ===" % (sys._getframe().f_code.co_name))
        logging.info("=== Parâmetros recebidos ===")
        logging.info(f"==> VAR: config TYPE: {type(config)}, CONTENT: {config}")
        
        template_path = path.join(config['generator']['generator_path'], config['generator']['templates_path'],
                                  'app_template.jinja2')
        output_path = path.join(config['generator']['generator_path'], 'app.py')
        
        logging.info(f"==> VAR: template_path TYPE: {type(template_path)}, CONTENT: {template_path}")
        logging.info(f"==> VAR: output_path TYPE: {type(output_path)}, CONTENT: {output_path}")
        
        context = {
                'config': {
                        'db_type'    : config['database']['db_type'],
                        'db_host'    : config['database']['db_host'],
                        'db_port'    : config['database']['db_port'],
                        'db_name'    : config['database']['db_name'],
                        'db_user'    : config['database']['db_user'],
                        'db_password': config['database']['db_password'],
                        'HOST'       : config['flask']['HOST'],
                        'PORT'       : config['flask']['PORT'],
                        'DEBUG'      : config['flask']['DEBUG']
                }
        }
        logging.info(f"==> VAR: context TYPE: {type(context)}, CONTENT: {context}")
        
        render_result = render_template(template_path, output_path, context)
        
        if not render_result:
            logging.error("Falha ao gerar o arquivo app.py. A função render_template retornou False.")
            return False
        
        return render_result
    
    except Exception as errorMsg:
        logging.error(f"Erro ao gerar o arquivo app.py: {errorMsg}")
        logging.error("Exception occurred", exc_info=True)
        return False


def app_generator(path_config_ini: str, file_config_ini: str) -> bool:
    """
    Função principal para orquestrar a geração do app.py.

    :param path_config_ini: Caminho do diretório onde o config.ini está localizado.
    :type path_config_ini: str
    :param file_config_ini: Nome do arquivo config.ini.
    :type file_config_ini: str
    :return: None
    """
    try:
        logging.info("=== Função: %s ===" % (sys._getframe().f_code.co_name))
        logging.info("=== Parâmetros recebidos ===")
        logging.info(f"==> VAR: path_config_ini TYPE: {type(path_config_ini)}, CONTENT: {path_config_ini}")
        logging.info(f"==> VAR: file_config_ini TYPE: {type(file_config_ini)}, CONTENT: {file_config_ini}")
        
        config = load_config(path_config_ini, file_config_ini)
        
        if config:
            generate_app_py(config)
        else:
            logging.error("Error on load_config: Config is None")
            return False
    
    except Exception as errorMsg:
        logging.error(f"Error on app_generator: {errorMsg}")
        logging.error("Exception occurred", exc_info=True)
        return False


if __name__ == "__main__":
    config_logging()
    
    path_config_ini = r"C:\Users\info\Documents\Projetos sysdev\Vya-Jobs\Flask-AppBuilder-cmdb\generator"
    file_config_ini = "config.ini"
    
    app_generator(path_config_ini, file_config_ini)
