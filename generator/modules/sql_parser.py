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
from typing import List, Dict, Union, Optional


def configure_logging() -> None:
    if not logging.getLogger().hasHandlers():
        logging.basicConfig(
                level=logging.DEBUG,
                format="%(asctime)s - %(levelname)s - %(threadName)s - %(funcName)s:%(lineno)d - %(name)s - %(message)s"
        )


class SQLFileReader:
    def __init__(self, file_path: str) -> None:
        logging.info("=== Função: %s ===" % (sys._getframe().f_code.co_name))
        logging.info(f"=== Parâmetros recebidos ===")
        logging.info(f"==> VAR: file_path TYPE: {type(file_path)}, CONTENT: {file_path}")
        self.file_path = file_path
        self.queries: List[str] = []
        self._read_file()
    
    def _read_file(self) -> None:
        logging.info("=== Função: %s ===" % (sys._getframe().f_code.co_name))
        with open(self.file_path, 'r', encoding='utf-8') as file:
            sql_content = file.readlines()
            self._parse_queries(sql_content)
    
    def _parse_queries(self, sql_lines: List[str]) -> None:
        logging.info("=== Função: %s ===" % (sys._getframe().f_code.co_name))
        logging.info(f"=== Parâmetros recebidos ===")
        logging.info(f"==> VAR: sql_lines TYPE: {type(sql_lines)}, CONTENT: {sql_lines}")
        
        current_query = []
        for line in sql_lines:
            line = line.strip()
            if line.startswith("--") or line.upper().startswith(("SET", "USE")):
                continue
            
            # Remover comentários do tipo COMMENT='...' antes do ';'
            if "COMMENT" in line.upper():
                line = re.sub(r"COMMENT\s*=\s*(['\"]).*?\1\s*(?=;)", "", line)
            
            # Substituir vírgula por ponto nas definições de DECIMAL
            if "DECIMAL" in line.upper():
                line = re.sub(r"DECIMAL\((\d+),(\d+)\)", r"DECIMAL(\1.\2)", line)

            current_query.append(line)
            if line.endswith(";"):
                query = " ".join(current_query)
                if "CREATE" in query.upper():
                    self.queries.append(query)
                current_query = []
    
    def get_queries(self) -> List[str]:
        logging.info("=== Função: %s ===" % (sys._getframe().f_code.co_name))
        logging.info(f"==> VAR: queries TYPE: {type(self.queries)}, LEN: {len(self.queries)}")
        return self.queries


class SQLQueryAnalyzer:
    def __init__(self, queries: List[str]) -> None:
        logging.info("=== Função: %s ===" % (sys._getframe().f_code.co_name))
        logging.info(f"=== Parâmetros recebidos ===")
        logging.info(f"==> VAR: queries TYPE: {type(queries)}, CONTENT: {queries}")
        self.queries = queries
        self.parsed_data: defaultdict[str, Dict[str, Union[str, List[Dict[str, Union[str, List[str]]]]]]] = \
            defaultdict(lambda: {"database": "", "tables": []})
        self._analyze_queries()
    
    def _analyze_queries(self) -> None:
        logging.debug("==> Analisando as queries")
        for query in self.queries:
            logging.debug(f"=== Analisando query ===")
            logging.debug(f"==> VAR: query TYPE: {type(query)}, CONTENT: {query}")
            parsed = sqlparse.parse(query)[0]
            
            if parsed.get_type() == 'CREATE':
                if "CREATE SCHEMA" in query.upper() or "CREATE DATABASE" in query.upper():
                    self._parse_create_schema_database(parsed)
                elif "CREATE TABLE" in query.upper():
                    self._parse_create_table(parsed)
    
    def _parse_create_schema_database(self, query: sqlparse.sql.Statement) -> None:
        logging.debug("==> Identificar SCHEMA ou DATABASE")
        tokens = list(query.flatten())
        database_name = ""
        
        for i, token in enumerate(tokens):
            if token.ttype == sqlparse.tokens.Name:
                database_name = token.value
                break
        
        if database_name:
            logging.debug(f"==> Nome do schema ou database identificado: {database_name}")
            self.parsed_data[database_name]["database"] = database_name
        else:
            logging.warning("Nome do schema ou database não encontrado.")
    
    def _parse_create_table(self, query: sqlparse.sql.Statement) -> None:
        logging.debug("==> Encontrar o nome do banco de dados e da tabela")
        logging.debug("=== Parâmetros recebidos ===")
        logging.debug(f"==> VAR: query TYPE: {type(query)}, CONTENT: {query}")
        
        query_str = str(query)
        match = re.search(
                r"CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?(?:`?(\w+)`?\.)?`?(\w+)`?",
                query_str, re.IGNORECASE
        )
        
        if match:
            database_name = f"`{match.group(1)}`" if match.group(1) else "default"
            table_name = f"`{match.group(2)}`"
        else:
            logging.warning(f"Nome da tabela não encontrado na query: {query_str}")
            return
        
        logging.debug(
            f"==> Nome da tabela identificado: {table_name}, Nome do banco de dados identificado: {database_name}")
        
        table_info = {
                "table"       : table_name,
                "schema"      : database_name,
                "columns"     : [],
                "primary_keys": [],
                "unique_keys" : [],
                "foreign_keys": [],
                "indexes"     : [],
                "query"       : query_str
        }
        
        _, par = query.token_next_by(i=sqlparse.sql.Parenthesis)
        if par is not None:
            logging.debug("==> Extraindo definições das colunas e restrições")
            definitions = self._extract_definitions(par)
            
            for definition in definitions:
                def_name = str(definition[0])
                def_content = ' '.join(str(t) for t in definition[1:])
                
                if def_name.startswith('`'):
                    column_info = self._parse_column_definition(def_name, def_content)
                    table_info["columns"].append(column_info)
                elif def_name.upper() == 'PRIMARY':
                    table_info["primary_keys"].extend(self._parse_primary_key(def_content))
                elif def_name.upper() == 'UNIQUE':
                    table_info["unique_keys"].append(self._parse_index(def_content))
                elif def_name.upper() == 'CONSTRAINT':
                    fk_info = self._parse_foreign_key(def_content)
                    if fk_info:
                        table_info["foreign_keys"].append(fk_info)
                elif def_name.upper() == 'INDEX':
                    table_info["indexes"].append(self._parse_index(def_content))
        
        self.parsed_data[database_name]["tables"].append(table_info)
    
    def _extract_definitions(self, token_list: sqlparse.sql.Parenthesis) -> List[List[sqlparse.sql.Token]]:
        logging.debug("==> Extraindo definições das colunas")
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
    
    def _parse_column_definition(self, name: str, definition: str) -> Dict[str, Union[str, List[str]]]:
        logging.debug("==> Analisando definição da coluna")
        constraints = []
        column_type = ""
        
        parsed = sqlparse.parse(definition)
        if not parsed:
            logging.error("Erro ao analisar a definição da coluna com sqlparse.")
            return {
                    "name"       : name.strip('`'),
                    "type"       : "",
                    "constraints": []
            }
        
        tokens = parsed[0].tokens
        definition_tokens = []
        
        for token in tokens:
            if token.ttype not in (sqlparse.tokens.Punctuation, sqlparse.tokens.Whitespace):
                definition_tokens.append(token)
        
        if definition_tokens:
            column_type = definition_tokens[0].value
            for token in definition_tokens[1:]:
                # Verificar se o token é um parêntese que contém números (indica tamanho)
                if isinstance(token, sqlparse.sql.Parenthesis):
                    size = token.value
                    column_type += size  # Adiciona o tamanho ao tipo
                # Verificar se o tipo é VARCHAR, INT, DECIMAL seguido de dígitos e adicionar ao tipo
                elif re.match(r'^(VARCHAR|INT|DECIMAL)\(\d', token.value.upper()):
                    column_type += token.value
                else:
                    constraints.append(token.value.upper())
        
        return {
                "name"       : name.strip('`'),
                "type"       : column_type,
                "constraints": constraints
        }
    
    def _parse_primary_key(self, definition: str) -> List[str]:
        logging.debug("==> Analisando chave primária")
        return [col.strip('`') for col in definition.split(',')]
    
    def _parse_index(self, definition: str) -> List[str]:
        logging.debug("==> Analisando índice")
        columns = re.findall(r"`([^`]*)`", definition)
        return columns
    
    def _parse_foreign_key(self, definition: str) -> Optional[Dict[str, Union[str, Dict[str, str]]]]:
        logging.debug("==> Analisando chave estrangeira")
        match = re.search(
                r"FOREIGN KEY\s*\(([^)]+)\)\s*REFERENCES\s*`?(\w+)`?\.`?(\w+)`?\s*\(([^)]+)\)",
                definition, re.IGNORECASE
        )
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


def parse_sql_file(file_path: str) -> str:
    logging.info("=== Função: %s ===" % (sys._getframe().f_code.co_name))
    logging.info(f"=== Parâmetros recebidos ===")
    logging.info(f"==> VAR: file_path TYPE: {type(file_path)}, CONTENT: {file_path}")
    
    logging.debug("==> Ler o arquivo SQL")
    sql_reader = SQLFileReader(file_path)
    queries = sql_reader.get_queries()
    
    if not queries:
        logging.error("Nenhuma query CREATE identificada no arquivo SQL.")
        raise ValueError("Nenhuma query CREATE identificada no arquivo SQL.")
    
    logging.debug("==> Analisar as queries")
    query_analyzer = SQLQueryAnalyzer(queries)
    analyzed_data = query_analyzer.parsed_data  # Corrigido para acessar o atributo
    
    if not analyzed_data:
        logging.error("Os dados analisados estão vazios.")
        raise ValueError("Os dados analisados estão vazios.")
    
    logging.debug("==> Extrair informações das tabelas")
    extractor = TableInfoExtractor(analyzed_data)
    extracted_info = extractor.extract_info()
    
    if not extracted_info:
        logging.error("As informações extraídas estão vazias.")
        raise ValueError("As informações extraídas estão vazias.")
    
    logging.debug("==> Gerar JSON a partir dos dados extraídos")
    json_generator = SqlParserToJson(extracted_info)
    json_output = json_generator.generate_json()
    
    if not json_output:
        logging.error("Erro ao gerar o JSON, saída vazia.")
        raise ValueError("Erro ao gerar o JSON, saída vazia.")
    
    return json_output


class TableInfoExtractor:
    def __init__(self, database_data: defaultdict[
        str, Dict[str, Union[str, List[Dict[str, Union[str, List[str]]]]]]]) -> None:
        logging.info("=== Função: %s ===" % (sys._getframe().f_code.co_name))
        logging.info(f"=== Parâmetros recebidos ===")
        logging.info(f"==> VAR: database_data TYPE: {type(database_data)}, CONTENT: {database_data}")
        self.database_data = database_data
    
    def extract_info(self) -> defaultdict[str, Dict[str, Union[str, List[Dict[str, Union[str, List[str]]]]]]]:
        logging.info("=== Função: %s ===" % (sys._getframe().f_code.co_name))
        extracted_data = defaultdict(lambda: {"database": "", "tables": []})
        for db_name, db_content in self.database_data.items():
            extracted_data[db_name]["database"] = db_name
            for table_info in db_content["tables"]:
                extracted_data[db_name]["tables"].append(self._extract_table_info(table_info))
        return extracted_data
    
    def _extract_table_info(self, table_info: Dict[str, Union[str, List[str]]]) -> Dict[
        str, Union[str, List[Dict[str, Union[str, List[str]]]]]]:
        logging.info("=== Função: %s ===" % (sys._getframe().f_code.co_name))
        logging.info(f"=== Parâmetros recebidos ===")
        logging.info(f"==> VAR: table_info TYPE: {type(table_info)}, CONTENT: {table_info}")
        return {
                "name"        : table_info["table"],
                "columns"     : table_info["columns"],
                "primary key" : [{"type": "INDEX", "columns": table_info["primary_keys"]}],
                "indexes"     : [{"name": "", "type": "INDEX", "columns": idx} for idx in table_info["indexes"]],
                "unique"      : [{"name": "", "type": "INDEX", "columns": uniq} for uniq in table_info["unique_keys"]],
                "foreign_keys": table_info["foreign_keys"]
        }


class SqlParserToJson:
    def __init__(self, data: defaultdict[str, Dict[str, Union[str, List[Dict[str, Union[str, List[str]]]]]]]) -> None:
        logging.info("=== Função: %s ===" % (sys._getframe().f_code.co_name))
        logging.info(f"=== Parâmetros recebidos ===")
        logging.info(f"==> VAR: data TYPE: {type(data)}, CONTENT: {data}")
        self.data = data
    
    def generate_json(self) -> str:
        logging.info("=== Função: %s ===" % (sys._getframe().f_code.co_name))
        return json.dumps(self.data, indent=2)


def parse_sql_file(file_path: str) -> str:
    logging.info("=== Função: %s ===" % (sys._getframe().f_code.co_name))
    logging.info(f"=== Parâmetros recebidos ===")
    logging.info(f"==> VAR: file_path TYPE: {type(file_path)}, CONTENT: {file_path}")
    
    logging.debug("==> Ler o arquivo SQL")
    sql_reader = SQLFileReader(file_path)
    queries = sql_reader.get_queries()
    
    if not queries:
        logging.error("Nenhuma query CREATE identificada no arquivo SQL.")
        raise ValueError("Nenhuma query CREATE identificada no arquivo SQL.")
    
    logging.debug("==> Analisar as queries")
    query_analyzer = SQLQueryAnalyzer(queries)
    analyzed_data = query_analyzer.parsed_data  # Corrigido para acessar o atributo
    logging.info(f"==> VAR: analyzed_data TYPE: {type(analyzed_data)}, CONTENT: {analyzed_data}")
    exit()

    if not analyzed_data:
        logging.error("Os dados analisados estão vazios.")
        raise ValueError("Os dados analisados estão vazios.")
    
    logging.debug("==> Extrair informações das tabelas")
    extractor = TableInfoExtractor(analyzed_data)
    extracted_info = extractor.extract_info()
    
    if not extracted_info:
        logging.error("As informações extraídas estão vazias.")
        raise ValueError("As informações extraídas estão vazias.")
    
    logging.debug("==> Gerar JSON a partir dos dados extraídos")
    json_generator = SqlParserToJson(extracted_info)
    json_output = json_generator.generate_json()
    
    if not json_output:
        logging.error("Erro ao gerar o JSON, saída vazia.")
        raise ValueError("Erro ao gerar o JSON, saída vazia.")
    
    return json_output

if __name__ == "__main__":
    configure_logging()
    file_path = r'C:\Users\info\Documents\Projetos sysdev\scripts\SQL\mysql\cmdb_small_lonly_20240801_1115.sql'
    json_result = parse_sql_file(file_path)
    json_file_name = "db_structure.json"
    json_file_path = r"C:\Users\info\Documents\Projetos sysdev\Vya-Jobs\Flask-AppBuilder-cmdb\generator"
    json_file_path_name = path.join(json_file_path, json_file_name)
    
    with open(json_file_path_name, 'w') as json_file:
        json_file.write(json_result)
