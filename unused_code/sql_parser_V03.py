# -*- coding: utf-8 -*-
"""
-------------------------------------------------------------------------
NOME..: sql_parser.py
LANG..: Python3
TITULO: Parses the SQL file to extract the database structure.
DATA..: 31/07/2024
VERSÃO: 0.1.00
HOST..: diversos
LOCAL.: diversos
OBS...: colocar nas linhas abaixo informações importantes sobre o programa

DEPEND: (informar nas linhas abaixo os recursos necessários para utilização)

-------------------------------------------------------------------------
Copyright (c) 2022 - Vya.Digital
This script is licensed under GNU GPL version 2.0 ou acima
-------------------------------------------------------------------------
Modifications.....:
 Date          Rev    Author           Description
 31/07/2024     0     Yves Marinho      Elaboração
                      Chatgpt
-------------------------------------------------------------------------
PARÂMETROS (informar os parâmetros necessários no exemplo de utilização)
-
STATUS: (status em que se encontra o código DEV/PROD)
DEV - pode adicionar dados adicionais para informar a fase
"""
import json
import logging
import re
import sqlparse
import sys
from collections import defaultdict
from os import path


def configure_logging():
    if not logging.getLogger().hasHandlers():
        logging.basicConfig(
                level=logging.DEBUG,
                format="%(asctime)s - %(levelname)s - %(threadName)s - %(funcName)s:%(lineno)d - %(name)s - %(message)s"
        )


def extract_definitions(token_list):
    """Extrai definições de colunas e outros elementos de dentro dos parênteses.

    :param token_list: Lista de tokens contidos nos parênteses.
    :type token_list: sqlparse.sql.Parenthesis
    :return: Lista de definições extraídas.
    :rtype: list
    """
    logging.info("=== Função: %s ===" % (sys._getframe().f_code.co_name))
    logging.info(f"=== Parâmetros recebidos ===")
    logging.info(f"==> VAR: token_list TYPE: {type(token_list)}, CONTENT: {token_list}")
    
    if token_list is None:
        logging.error("token_list is None, exiting extract_definitions.")
        return []
    
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


class SQLFileReader:
    def __init__(self, file_path):
        logging.info("=== Função: %s ===" % (sys._getframe().f_code.co_name))
        self.file_path = file_path
        self.queries = []
        self._read_file()
    
    def _read_file(self):
        logging.info("=== Função: %s ===" % (sys._getframe().f_code.co_name))
        with open(self.file_path, 'r', encoding='utf-8') as file:
            sql_content = file.read()
            self._parse_queries(sql_content)
    
    def _parse_queries(self, sql_content):
        logging.info("=== Função: %s ===" % (sys._getframe().f_code.co_name))
        statements = sqlparse.parse(sql_content)
        for statement in statements:
            if statement.get_type() == 'CREATE':
                self.queries.append(statement)
    
    def get_queries(self):
        logging.info("=== Função: %s ===" % (sys._getframe().f_code.co_name))
        return self.queries


class SQLQueryAnalyzer:
    def __init__(self, queries):
        logging.info("=== Função: %s ===" % (sys._getframe().f_code.co_name))
        logging.info(f"=== Parâmetros recebidos ===")
        logging.info(f"==> VAR: queries TYPE: {type(queries)}, CONTENT: {queries}")
        self.queries = [self._remove_comments(query) for query in queries]
        self.parsed_data = []
        self._analyze_queries()
    
    def _remove_comments(self, query):
        """Remove comentários de uma instrução SQL.

        :param query: Instrução SQL com comentários.
        :type query: sqlparse.sql.Statement
        :return: Instrução SQL sem comentários.
        :rtype: sqlparse.sql.Statement
        """
        logging.info("=== Função: %s ===" % (sys._getframe().f_code.co_name))
        logging.info(f"=== Parâmetros recebidos ===")
        logging.info(f"==> VAR: query TYPE: {type(query)}, CONTENT: {query}")
        tokens = []
        for token in query.tokens:
            if not token.ttype == sqlparse.tokens.Comment and not isinstance(token, sqlparse.sql.Comment):
                tokens.append(token)
        cleaned_query = sqlparse.sql.Statement(tokens)
        return cleaned_query
    
    def _analyze_queries(self):
        logging.info("=== Função: %s ===" % (sys._getframe().f_code.co_name))
        for query in self.queries:
            logging.info(f"=== Analisando query ===")
            logging.info(f"==> VAR: query TYPE: {type(query)}, CONTENT: {query}")
            if query.get_type() == 'CREATE':
                self._parse_create_query(query)
    
    def _parse_create_query(self, query):
        logging.info("=== Função: %s ===" % (sys._getframe().f_code.co_name))
        logging.info(f"=== Parâmetros recebidos ===")
        logging.info(f"==> VAR: query TYPE: {type(query)}, CONTENT: {query}")
        table_info = {}
        
        # Extrai o nome da tabela
        tokens = list(query.flatten())
        
        # Encontrar o nome da tabela
        for i, token in enumerate(tokens):
            if token.ttype == sqlparse.tokens.Name and tokens[i - 1].match(sqlparse.tokens.Keyword, 'TABLE'):
                table_info["table"] = token.value
                table_info["schema"] = tokens[i - 3].value if tokens[i - 2].match(sqlparse.tokens.Punctuation,
                                                                                  '.') else ""
                break
        
        # Extrai definições de colunas e constraints
        _, par = query.token_next_by(i=sqlparse.sql.Parenthesis)
        definitions = extract_definitions(par)
        
        columns = []
        primary_keys = []
        unique_keys = []
        foreign_keys = []
        indexes = []
        
        for definition in definitions:
            def_name = str(definition[0])
            def_content = ' '.join(str(t) for t in definition[1:])
            
            if def_name.startswith('`'):  # Definição de coluna
                column_info = self._parse_column_definition(def_name, def_content)
                columns.append(column_info)
            elif def_name.upper() == 'PRIMARY':
                primary_keys.extend(self._parse_primary_key(def_content))
            elif def_name.upper() == 'UNIQUE':
                unique_keys.append(self._parse_index(def_content))
            elif def_name.upper() == 'CONSTRAINT':
                fk_info = self._parse_foreign_key(def_content)
                if fk_info:
                    foreign_keys.append(fk_info)
            elif def_name.upper() == 'INDEX':
                indexes.append(self._parse_index(def_content))
        
        table_info["columns"] = columns
        table_info["primary_keys"] = primary_keys
        table_info["unique_keys"] = unique_keys
        table_info["foreign_keys"] = foreign_keys
        table_info["indexes"] = indexes
        table_info["query"] = str(query)
        
        self.parsed_data.append(table_info)
    
    def _parse_column_definition(self, name, definition):
        logging.info("=== Função: %s ===" % (sys._getframe().f_code.co_name))
        logging.info(f"=== Parâmetros recebidos ===")
        logging.info(f"==> VAR: name TYPE: {type(name)}, CONTENT: {name}")
        logging.info(f"==> VAR: definition TYPE: {type(definition)}, CONTENT: {definition}")
        
        if not definition.strip():  # Verifica se a definição está vazia
            logging.error(f"Definition is empty for column {name}")
            return {
                    "name"       : name.strip('`'),
                    "type"       : "",
                    "constraints": []
            }
        
        constraints = []
        if 'AUTO_INCREMENT' in definition:
            constraints.append("AUTO_INCREMENT")
        if 'NOT NULL' in definition:
            constraints.append("NOT NULL")
        if 'DEFAULT' in definition:
            default_value = re.search(r"DEFAULT\s+([\w()'`]+)", definition, re.IGNORECASE).group(1)
            constraints.append(f"DEFAULT {default_value}")
        if 'ON UPDATE' in definition:
            on_update_value = re.search(r"ON UPDATE\s+([\w()'`]+)", definition, re.IGNORECASE).group(1)
            constraints.append(f"ON UPDATE {on_update_value}")
        
        return {
                "name"       : name.strip('`'),
                "type"       : definition.split()[0] if definition.split() else "",
                "constraints": constraints
        }
    
    def _parse_primary_key(self, definition):
        logging.info("=== Função: %s ===" % (sys._getframe().f_code.co_name))
        logging.info(f"=== Parâmetros recebidos ===")
        logging.info(f"==> VAR: definition TYPE: {type(definition)}, CONTENT: {definition}")
        return [col.strip('`') for col in definition.split(',')]
    
    def _parse_foreign_key(self, definition):
        logging.info("=== Função: %s ===" % (sys._getframe().f_code.co_name))
        logging.info(f"=== Parâmetros recebidos ===")
        logging.info(f"==> VAR: definition TYPE: {type(definition)}, CONTENT: {definition}")
        match = re.search(
                r"FOREIGN KEY\s*\(([^)]+)\)\s*REFERENCES\s*`?(\w+)`?\.`?(\w+)`?\s*\(([^)]+)\)",
                definition, re.IGNORECASE)
        if match:
            return {
                    "name"      : match.group(0).strip(),
                    "column"    : match.group(1).strip('`'),
                    "references": {
                            "table" : f"{match.group(2)}.{match.group(3)}",
                            "column": match.group(4).strip('`')
                    }
            }
        return None
    
    def _parse_index(self, definition):
        logging.info("=== Função: %s ===" % (sys._getframe().f_code.co_name))
        logging.info(f"=== Parâmetros recebidos ===")
        logging.info(f"==> VAR: definition TYPE: {type(definition)}, CONTENT: {definition}")
        return [col.strip('`') for col in definition.split(',')]
    
    def get_parsed_data(self):
        logging.info("=== Função: %s ===" % (sys._getframe().f_code.co_name))
        return self.parsed_data


class TableInfoExtractor:
    def __init__(self, table_info):
        logging.info("=== Função: %s ===" % (sys._getframe().f_code.co_name))
        logging.info("=== Parâmetros recebidos ===")
        logging.info(f"==> VAR: table_info TYPE: {type(table_info)}, CONTENT: {table_info}")
        self.table_info = table_info
        self.database_name = table_info.get("schema", "")
        self.table_name = table_info.get("table", "")
        self.columns = table_info.get("columns", [])
        self.primary_keys = table_info.get("primary_keys", [])
        self.indexes = table_info.get("indexes", [])
        self.unique = table_info.get("unique_keys", [])
        self.foreign_keys = table_info.get("foreign_keys", [])
    
    def get_info(self):
        logging.info("=== Função: %s ===" % (sys._getframe().f_code.co_name))
        table_info = {
                "name"        : self.table_name,
                "columns"     : self.columns,
                "primary key" : [{"type": "INDEX", "columns": self.primary_keys}],
                "indexes"     : [{"name": "", "type": "INDEX", "columns": idx} for idx in self.indexes],
                "unique"      : [{"name": "", "type": "INDEX", "columns": uniq} for uniq in self.unique],
                "foreign_keys": self.foreign_keys
        }
        return table_info


def parse_sql_file(file_path: str) -> list:
    logging.info("=== Função: %s ===" % (sys._getframe().f_code.co_name))
    
    databases = defaultdict(lambda: {"database": "", "tables": []})
    
    # Ler o arquivo SQL
    sql_reader = SQLFileReader(file_path)
    queries = sql_reader.get_queries()
    
    # Listar as queries
    for query in queries:
        logging.info(f"==> VAR: query TYPE: {type(query)}, CONTENT: {query}")
        query_analyzer = SQLQueryAnalyzer([query])
        query_analyzer_data = query_analyzer.get_parsed_data()
        logging.info(f"==> VAR: query_analyzer_data TYPE: {type(query_analyzer_data)}, CONTENT: {query_analyzer_data}")
        
        if not query_analyzer_data:
            logging.error("Query not supported")
            continue
        if not isinstance(query_analyzer_data, list):
            logging.error("query_analyzer_data is not list")
            raise ValueError("query_analyzer_data is not list")
        
        for table_info in query_analyzer_data:
            extractor = TableInfoExtractor(table_info)
            logging.info(f"==> VAR: extractor TYPE: {type(extractor)}, CONTENT: {extractor}")
            table_info_extracted = extractor.get_info()
            logging.info(
                f"==> VAR: table_info_extracted TYPE: {type(table_info_extracted)}, CONTENT: {table_info_extracted}")
            
            database_name = extractor.database_name if extractor.database_name else "default"
            databases[database_name]["database"] = database_name
            databases[database_name]["tables"].append(table_info_extracted)
    
    database_list = [data for db, data in databases.items()]
    return database_list


if __name__ == "__main__":
    configure_logging()
    file_path = r'C:\Users\info\Documents\Projetos sysdev\scripts\SQL\mysql\cmdb_small_lonly_20240801_1115.sql'
    results = parse_sql_file(file_path)
    json_file_name = "db_structure.json"
    json_file_path = r"C:\Users\info\Documents\Projetos sysdev\Vya-Jobs\Flask-AppBuilder-cmdb\generator"
    json_file_path_name = path.join(json_file_path, json_file_name)
    
    with open(json_file_path_name, 'w') as json_file:
        json.dump(results, json_file, indent=2)
