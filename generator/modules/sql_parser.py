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
            if query.upper().startswith("CREATE"):
                self._parse_create_query(query)

    def _parse_create_query(self, query):
        logging.info("=== Função: %s ===" % (sys._getframe().f_code.co_name))
        query_type = None
        if re.match(r"CREATE\s+SCHEMA", query, re.IGNORECASE):
            query_type = "SCHEMA"
        elif re.match(r"CREATE\s+DATABASE", query, re.IGNORECASE):
            query_type = "DATABASE"
        elif re.match(r"CREATE\s+TABLE", query, re.IGNORECASE):
            query_type = "TABLE"

        if query_type:
            info = {
                "type": query_type,
                "query": query
            }
            if query_type == "TABLE":
                info.update(self._parse_create_table_query(query))
            self.parsed_data.append(info)

    def _parse_create_table_query(self, query):
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

        foreign_key_matches = re.findall(r"FOREIGN KEY\s*\(([^)]+)\)\s*REFERENCES\s*`?(\w+)`?\.`?(\w+)`?\s*\(([^)]+)\)",
                                         query, re.IGNORECASE)
        for fk in foreign_key_matches:
            foreign_keys.append({
                "columns": [col.strip().strip('`') for col in fk[0].split(',')],
                "referenced_table": f"{fk[1]}.{fk[2]}",
                "referenced_columns": [col.strip().strip('`') for col in fk[3].split(',')]
            })

        table_info["columns"] = columns
        table_info["primary_keys"] = primary_keys
        table_info["unique_keys"] = unique_keys
        table_info["foreign_keys"] = foreign_keys

        return table_info

    def get_parsed_data(self):
        logging.info("=== Função: %s ===" % (sys._getframe().f_code.co_name))
        return self.parsed_data


class TableInfoExtractor:
    def __init__(self, create_query):
        logging.info("=== Função: %s ===" % (sys._getframe().f_code.co_name))
        logging.info("=== Parâmetros recebidos ===")
        logging.info(f"==> VAR: create_query TYPE: {type(create_query)}, CONTENT: {create_query}")
        self.create_query = create_query
        self.database_name = ""
        self.table_name = ""
        self.columns = []
        self.primary_keys = []
        self.indexes = []
        self.unique = []
        self.foreign_keys = []
        self.query_type = None
        self._extract_info()

    def _extract_info(self):
        logging.info("=== Função: %s ===" % (sys._getframe().f_code.co_name))
        if "CREATE TABLE" in self.create_query.upper():
            self.query_type = "TABLE"
            self._extract_table_name()
            self._extract_columns()
            self._extract_primary_keys()
            self._extract_indexes()
            self._extract_unique_keys()
            self._extract_foreign_keys()
        elif "CREATE SCHEMA" in self.create_query.upper():
            self.query_type = "SCHEMA"
            self._extract_schema_name()
        elif "CREATE DATABASE" in self.create_query.upper():
            self.query_type = "DATABASE"
            self._extract_database_name()

    def _extract_schema_name(self):
        logging.info("=== Função: %s ===" % (sys._getframe().f_code.co_name))
        schema_name_pattern = r"CREATE\s+SCHEMA\s+(?:IF\s+NOT\s+EXISTS\s+)?`?(\w+)`?"
        match = re.search(schema_name_pattern, self.create_query, re.IGNORECASE)
        if match:
            self.database_name = match.group(1)

    def _extract_database_name(self):
        logging.info("=== Função: %s ===" % (sys._getframe().f_code.co_name))
        database_name_pattern = r"CREATE\s+DATABASE\s+(?:IF\s+NOT\s+EXISTS\s+)?`?(\w+)`?"
        match = re.search(database_name_pattern, self.create_query, re.IGNORECASE)
        if match:
            self.database_name = match.group(1)

    def _extract_table_name(self):
        logging.info("=== Função: %s ===" % (sys._getframe().f_code.co_name))
        create_table_pattern = r"CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?(?:`?(\w+)`?\.)?`?(\w+)`?"
        match = re.search(create_table_pattern, self.create_query, re.IGNORECASE)
        if match:
            self.database_name = match.group(1) if match.group(1) else ""
            self.table_name = match.group(2)

    def _extract_columns(self):
        logging.info("=== Função: %s ===" % (sys._getframe().f_code.co_name))
        fields_section = re.search(r"\((.*)\)", self.create_query, re.DOTALL)
        if fields_section:
            fields = re.split(r',\s*(?![^()]*\))', fields_section.group(1))
            for field in fields:
                if field.upper().startswith('PRIMARY KEY'):
                    continue
                column_match = re.match(r"`(\w+)`\s+([A-Z]+(?:\(\d+(?:,\d+)?\))?)(.*)", field)
                if column_match:
                    column_name = column_match.group(1)
                    column_type = column_match.group(2)
                    constraints_part = column_match.group(3)
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
                    self.columns.append({
                        "name": column_name,
                        "type": column_type,
                        "constraints": constraints
                    })

    def _extract_primary_keys(self):
        logging.info("=== Função: %s ===" % (sys._getframe().f_code.co_name))
        primary_key_match = re.search(r"PRIMARY KEY\s*\(([^)]+)\)", self.create_query, re.IGNORECASE)
        if primary_key_match:
            primary_key_columns = [col.strip().strip('`') for col in primary_key_match.group(1).split(',')]
            self.primary_keys.append({
                "type": "INDEX",
                "columns": primary_key_columns
            })

    def _extract_indexes(self):
        logging.info("=== Função: %s ===" % (sys._getframe().f_code.co_name))
        index_matches = re.findall(r"INDEX\s*`?(\w*)`?\s*\(([^)]+)\)", self.create_query, re.IGNORECASE)
        for index in index_matches:
            index_name = index[0]
            index_columns = [col.strip().strip('`') for col in index[1].split(',')]
            self.indexes.append({
                "name": index_name,
                "type": "INDEX",
                "columns": index_columns
            })

    def _extract_unique_keys(self):
        logging.info("=== Função: %s ===" % (sys._getframe().f_code.co_name))
        unique_key_matches = re.findall(r"UNIQUE\s*INDEX\s*`?(\w*)`?\s*\(([^)]+)\)", self.create_query,
                                        re.IGNORECASE)
        for unique_key in unique_key_matches:
            unique_name = unique_key[0]
            unique_columns = [col.strip().strip('`') for col in unique_key[1].split(',')]
            self.unique.append({
                "name": unique_name,
                "type": "INDEX",
                "columns": unique_columns
            })

    def _extract_foreign_keys(self):
        logging.info("=== Função: %s ===" % (sys._getframe().f_code.co_name))
        foreign_key_matches = re.findall(
            r"FOREIGN KEY\s*\(([^)]+)\)\s*REFERENCES\s*`?(\w+)`?\.`?(\w+)`?\s*\(([^)]+)\)\s*(ON DELETE\s+(\w+))?\s*(ON UPDATE\s+(\w+))?",
            self.create_query, re.IGNORECASE)
        for fk in foreign_key_matches:
            fk_columns = [col.strip().strip('`') for col in fk[0].split(',')]
            referenced_table = f"{fk[1]}.{fk[2]}"
            referenced_columns = [col.strip().strip('`') for col in fk[3].split(',')]
            on_delete = fk[5] if fk[5] else "NO ACTION"
            on_update = fk[7] if fk[7] else "NO ACTION"
            self.foreign_keys.append({
                "name": f"fk_{self.table_name}_{fk_columns[0]}",
                "column": fk_columns[0],
                "references": {
                    "table": referenced_table,
                    "column": referenced_columns[0],
                    "on_delete": on_delete,
                    "on_update": on_update
                }
            })

    def get_info(self):
        logging.info("=== Função: %s ===" % (sys._getframe().f_code.co_name))
        if self.query_type == "TABLE":
            info = {
                "database": self.database_name,
                "tables": [
                    {
                        "name": self.table_name,
                        "columns": self.columns,
                        "primary key": self.primary_keys,
                        "indexes": self.indexes,
                        "unique": self.unique,
                        "foreign_keys": self.foreign_keys
                    }
                ]
            }
        else:
            info = {
                "database": self.database_name,
                "type": self.query_type
            }
        return json.dumps(info)


def parse_sql_file(file_path: str) -> list:
    logging.info("=== Função: %s ===" % (sys._getframe().f_code.co_name))

    parse_sql_results: list = []

    # Ler o arquivo SQL
    sql_reader = SQLFileReader(file_path)
    queries = sql_reader.get_queries()

    # Listar as queries
    line_number = 0
    for query in queries:
        line_number += 1
        logging.info(f"==>> LINE_NUMBER {line_number}")
        if not any(keyword in query.upper() for keyword in ["CREATE TABLE", "CREATE SCHEMA", "CREATE DATABASE"]):
            logging.info("Query line is not a CREATE TABLE, CREATE SCHEMA, or CREATE DATABASE query")
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

        for query_data in query_analyzer_data:
            extractor = TableInfoExtractor(query_data["query"])
            logging.info(f"==> VAR: extractor TYPE: {type(extractor)}, CONTENT: {extractor}")
            table_info = extractor.get_info()
            logging.info(f"==> VAR: table_info TYPE: {type(table_info)}, CONTENT: {table_info}")

            parse_sql_results.append(json.loads(table_info))

    logging.info(f"==> VAR: parse_sql_results TYPE: {type(parse_sql_results)}, LEN: {len(parse_sql_results)}")
    return parse_sql_results


if __name__ == "__main__":
    configure_logging()
    file_path = r'C:\Users\info\Documents\Projetos sysdev\scripts\SQL\mysql\cmdb_small_lonly_20240801_1115.sql'
    results = parse_sql_file(file_path)
    print(json.dumps(results, indent=2))
