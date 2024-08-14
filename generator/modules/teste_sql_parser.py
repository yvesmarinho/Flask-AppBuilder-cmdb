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
 00/00/0000    0      NOME DO AUTOR    Elaboração
-------------------------------------------------------------------------
PARÂMETROS (informar os parâmetros necessários no exemplo de utilização)
-
STATUS: (status emn que se encontra o código DEV/PROD)
DEV - pode adicionar dados adicionais para informar a fase
"""
import logging
import sqlparse
import sys
import json
from collections import defaultdict

def configure_logging():
    if not logging.getLogger().hasHandlers():
        logging.basicConfig(
                level=logging.DEBUG,
                format="%(asctime)s - %(levelname)s - %(threadName)s - %(funcName)s:%(lineno)d - %(name)s - %(message)s"
        )

def extract_definitions(token_list):
    definitions = []
    tmp = []
    par_level = 0
    for token in token_list.flatten():
        if token.is_whitespace:
            continue
        elif token.match(sqlparse.tokens.Punctuation, '('):
            par_level += 1
            continue
        if token.match(sqlparse.tokens.Punctuation, ')'):
            if par_level == 0:
                break
            else:
                par_level -= 1
        elif token.match(sqlparse.tokens.Punctuation, ','):
            if tmp:
                definitions.append(tmp)
            tmp = []
        else:
            tmp.append(token)
    if tmp:
        definitions.append(tmp)
    return definitions

def process_query(query, database_name, table_name):
    # Extrair colunas e outros detalhes da tabela
    _, par = query.token_next_by(i=sqlparse.sql.Parenthesis)
    if par is None:
        logging.info("Não foram encontradas definições de colunas.")
        return None

    columns = extract_definitions(par)

    # Montar estrutura JSON
    table_structure = {
        "database": database_name,
        "table": table_name,
        "columns": []
    }

    for column in columns:
        column_name = str(column[0]).strip("`")
        column_definition = ' '.join(str(t) for t in column[1:])
        table_structure["columns"].append({
            "name": column_name,
            "definition": column_definition
        })

    return table_structure

if __name__ == '__main__':
    configure_logging()
    file_path = r'C:\Users\info\Documents\Projetos sysdev\scripts\SQL\mysql\cmdb_small_lonly_20240801_1115.sql'

    databases = defaultdict(lambda: {"database": "", "tables": []})

    # Ler o arquivo SQL e processar linha por linha
    with open(file_path, 'r', encoding='utf-8') as file:
        sql_lines = file.readlines()

    json_output = []
    current_query = []

    for line in sql_lines:
        stripped_line = line.strip()
        # Filtrar linhas vazias e linhas que começam com "--", "SET", ou "USE"
        if not stripped_line or stripped_line.startswith('--') or stripped_line.upper().startswith('SET') or stripped_line.upper().startswith('USE'):
            continue

        current_query.append(stripped_line)

        # Se a linha termina com ponto e vírgula, significa que a query está completa
        if stripped_line.endswith(';'):
            complete_query = " ".join(current_query)
            parsed = sqlparse.parse(complete_query)[0]
            current_query = []

            if parsed.get_type() == "CREATE" and "TABLE" in complete_query.upper():
                table_name = None
                database_name = None

                for token in parsed.tokens:
                    if isinstance(token, sqlparse.sql.Identifier):
                        if "." in token.get_real_name():
                            database_name, table_name = token.get_real_name().split('.')
                        else:
                            table_name = token.get_real_name()

                # Processar a query para coletar definições
                table_structure = process_query(parsed, database_name, table_name)
                if table_structure:
                    json_output.append(table_structure)

    # Escrever a saída JSON
    output_file_path = r'C:\Users\info\Documents\Projetos sysdev\Vya-Jobs\Flask-AppBuilder-cmdb\generator\db_structure.json'
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        json.dump(json_output, output_file, indent=4)

    logging.info(f"Estrutura do banco de dados exportada para: {output_file_path}")
