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
import re
import logging
import sys
import json
from collections import defaultdict
from os import path

def configure_logging():
    if not logging.getLogger().hasHandlers():
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s - %(levelname)s - %(threadName)s - %(funcName)s:%(lineno)d - %(name)s - %(message)s"
        )


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
        # Remover comentários de linha
        lines = sql_content.splitlines()
        cleaned_lines = []
        in_block_comment = False

        for line in lines:
            stripped_line = line.strip()
            if in_block_comment:
                if "*/" in stripped_line:
                    in_block_comment = False
                    stripped_line = stripped_line.split("*/", 1)[1].strip()
                else:
                    continue

            if stripped_line.startswith("/*"):
                in_block_comment = True
                if "*/" in stripped_line:
                    in_block_comment = False
                    stripped_line = stripped_line.split("*/", 1)[1].strip()
                else:
                    continue

            if not stripped_line or stripped_line.startswith("--"):
                continue

            cleaned_lines.append(stripped_line)

        cleaned_content = "\n".join(cleaned_lines)

        # Processar queries
        query = ''
        in_string = False
        escape_char = False
        for char in cleaned_content:
            if char == ';' and not in_string:
                query += char
                self.queries.append(query.strip())
                query = ''
            else:
                query += char
                if char == '"' or char == "'":
                    if not escape_char:
                        in_string = not in_string
                escape_char = (char == '\\' and not escape_char)

        if query.strip():
            self.queries.append(query.strip())

    def get_queries(self):
        logging.info("=== Função: %s ===" % (sys._getframe().f_code.co_name))
        return self.queries


class SQLQueryAnalyzer:
    def __init__(self, queries):
        logging.info("=== Função: %s ===" % (sys._getframe().f_code.co_name))
        self.queries = queries
        self.parsed_data = []
        self._analyze_queries()

    def _analyze_queries(self):
        logging.info("=== Função: %s ===" % (sys._getframe().f_code.co_name))
        for query in self.queries:
            query = query.strip()
            if query.upper().startswith("CREATE TABLE"):
                self._parse_create_query(query)

    def _parse_create_query(self, query):
        logging.info("=== Função: %s ===" % (sys._getframe().f_code.co_name))
        table_info = {}
        table_name_match = re.search(r"CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?(?:`?(\w+)`?\.)?`?(\w+)`?", query, re.IGNORECASE)
        if table_name_match:
            table_info["schema"] = table_name_match.group(1) if table_name_match.group(1) else ""
            table_info["table"] = table_name_match.group(2)

        columns = []
        primary_keys = []
        unique_keys = []
        foreign_keys = []

        column_definitions = re.findall(r"`(\w+)`\s+([A-Z]+(?:\(\d+(?:,\d+)?\))?)(.*?)(?:,|$)", query, re.IGNORECASE)
        for col in column_definitions:
            column_name = col[0]
            column_type = col[1].strip()
            constraints_part = col[2].strip()
            constraints = []
            if "AUTO_INCREMENT" in constraints_part.upper():
                constraints.append("AUTO_INCREMENT")
            if "NOT NULL" in constraints_part.upper():
                constraints.append("NOT NULL")
            if "DEFAULT" in constraints_part.upper():
                default_value = re.search(r"DEFAULT\s+([\w()'`]+)", constraints_part, re.IGNORECASE).group(1)
                constraints.append(f"DEFAULT {default_value}")
            if "ON UPDATE" in constraints_part.upper():
                on_update_value = re.search(r"ON UPDATE\s+([\w()'`]+)", constraints_part, re.IGNORECASE).group(1)
                constraints.append(f"ON UPDATE {on_update_value}")
            columns.append({
                "name": column_name,
                "type": column_type,
                "constraints": constraints
            })

        primary_key_match = re.search(r"PRIMARY KEY\s*\(([^)]+)\)", query, re.IGNORECASE)
        if primary_key_match:
            primary_keys = [col.strip().strip('`') for col in primary_key_match.group(1).split(',')]

        unique_key_matches = re.findall(r"UNIQUE\s*(?:INDEX\s*`?\w*`?\s*)?\(([^)]+)\)", query, re.IGNORECASE)
        for unique_key in unique_key_matches:
            unique_keys.append([col.strip().strip('`') for col in unique_key.split(',')])

        foreign_key_matches = re.findall(
            r"FOREIGN KEY\s*\(([^)]+)\)\s*REFERENCES\s*`?(\w+)`?\.`?(\w+)`?\s*\(([^)]+)\)\s*(ON DELETE\s+(\w+))?\s*(ON UPDATE\s+(\w+))?",
            query, re.IGNORECASE)
        for fk in foreign_key_matches:
            foreign_keys.append({
                "name": f"fk_{table_info['table']}_{fk[0].strip().strip('`')}",
                "column": fk[0].strip().strip('`'),
                "references": {
                    "table": f"{fk[1]}.{fk[2]}",
                    "column": fk[3].strip().strip('`'),
                    "on_delete": fk[5] if fk[5] else "NO ACTION",
                    "on_update": fk[7] if fk[7] else "NO ACTION"
                }
            })

        table_info["columns"] = columns
        table_info["primary_keys"] = primary_keys
        table_info["unique_keys"] = unique_keys
        table_info["foreign_keys"] = foreign_keys

        table_info["query"] = query  # Adiciona a query original ao table_info

        self.parsed_data.append(table_info)

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
            "name": self.table_name,
            "columns": self.columns,
            "primary key": [{"type": "INDEX", "columns": self.primary_keys}],
            "indexes": [{"name": "", "type": "INDEX", "columns": idx} for idx in self.indexes],
            "unique": [{"name": "", "type": "INDEX", "columns": uniq} for uniq in self.unique],
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
    line_number = 0
    for query in queries:
        line_number += 1
        logging.info(f"==>> LINE_NUMBER {line_number}")
        if not "CREATE TABLE" in query.upper():
            logging.info("Query line is not a CREATE TABLE query")
            continue
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
            logging.info(f"==> VAR: table_info_extracted TYPE: {type(table_info_extracted)}, CONTENT: {table_info_extracted}")

            database_name = extractor.database_name if extractor.database_name else "default"
            databases[database_name]["database"] = database_name
            databases[database_name]["tables"].append(table_info_extracted)

    database_list = [data for db, data in databases.items()]
    logging.info(f"==> VAR: database_list TYPE: {type(database_list)}, CONTENT: {database_list}")
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
