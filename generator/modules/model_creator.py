# -*- coding: utf-8 -*-
"""
-------------------------------------------------------------------------
NOME..: model_generator.py
LANG..: Python3
TITULO: Programa que recebe uma lista com JSON e gera um modelo de dados
        para o sistema.
DATA..: 02/08/2024
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
import json
import logging
from os import getcwd, path, remove, mkdir


class ModelGenerator:
    def __init__(self, json_input):
        logging.info(f"==> VAR: json_input   TYPE: {type(json_input)}, LEN: {len(json_input)}")
        if isinstance(json_input, str):
            self.json_data = json.loads(json_input)
        else:
            self.json_data = json_input
    
    def generate_models(self):
        models_code = []
        
        # Add necessary imports once
        models_code.append("import datetime")
        models_code.append("from flask_appbuilder import Model")
        models_code.append(
            "from sqlalchemy import Column, DateTime, Date, ForeignKey, Integer, String, Table, Text, PrimaryKeyConstraint, UniqueConstraint, Index, Float")
        models_code.append("from sqlalchemy.orm import relationship")
        models_code.append("")
        
        logging.info(f"==> VAR: self.json_data   TYPE: {type(self.json_data)}, CONTENT: {self.json_data}")
        
        # Handle multiple databases
        databases = self.json_data if isinstance(self.json_data, list) else [self.json_data]
        
        for db_data in databases:
            logging.info(f"==> VAR: db_data   TYPE: {type(db_data)}, CONTENT: {db_data}")
            db_name = db_data['database']
            tables = db_data['tables']
            
            models_code.append(f"# Models for database: {db_name}\n")
            for table in tables:
                table_name = table['name']
                columns = table['columns']
                primary_key = table.get('primary key', [])
                indexes = table.get('indexes', [])
                unique_indexes = table.get('unique', [])
                foreign_keys = table.get('foreign_keys', [])
                
                models_code.append(f"class {table_name.capitalize()}(Model):")
                models_code.append(f"    __tablename__ = '{table_name}'")
                models_code.append(f"    __bind_key__ = '{db_name}'\n")
                
                fk_columns = {fk['column']: fk for fk in foreign_keys}
                
                for column in columns:
                    column_name = column['name']
                    column_type = self.get_column_type(column['type'])
                    constraints = self.get_constraints(column['constraints'])
                    
                    if column_name in fk_columns:
                        fk = fk_columns[column_name]
                        ref_table = fk['references']['table']
                        ref_column = fk['references']['column']
                        constraints += f", ForeignKey('{ref_table}.{ref_column}')"
                    
                    models_code.append(f"    {column_name} = Column({column_type}{constraints})")
                
                if primary_key:
                    pk_columns = ', '.join([f"'{col}'" for col in primary_key[0]['columns']])
                    models_code.append(f"    __table_args__ = (PrimaryKeyConstraint({pk_columns}),)")
                
                for index in indexes:
                    index_name = index['name']
                    index_columns = ', '.join([f"'{col}'" for col in index['columns']])
                    models_code.append(f"    Index('{index_name}', {index_columns}),")
                
                for unique in unique_indexes:
                    unique_name = unique['name']
                    unique_columns = ', '.join([f"'{col}'" for col in unique['columns']])
                    models_code.append(f"    UniqueConstraint('{unique_name}', {unique_columns}),")
                
                # Add __repr__ method
                repr_column = columns[1]['name'] if len(columns) > 1 else columns[0]['name']
                models_code.append(f"\n    def __repr__(self):")
                models_code.append(f"        return self.{repr_column}")
                
                models_code.append("\n")
        
        return "\n".join(models_code)
    
    def get_column_type(self, column_type):
        type_mapping = {
                'INT'     : 'Integer',
                'VARCHAR' : 'String',
                'DATETIME': 'DateTime',
                'TEXT'    : 'Text',
                'DECIMAL' : 'Float'
        }
        for key, value in type_mapping.items():
            if column_type.startswith(key):
                if key == 'VARCHAR' or key == 'DECIMAL':
                    return f"{value}{column_type[len(key):]}"
                return value
        return column_type
    
    def get_constraints(self, constraints):
        constraints_mapping = {
                'PRIMARY KEY'                : ', primary_key=True',
                'AUTO_INCREMENT'             : ', autoincrement=True',
                'NOT NULL'                   : ', nullable=False',
                'NULL'                       : ', nullable=True',
                'DEFAULT CURRENT_TIMESTAMP'  : ', default=datetime.datetime.now',
                'DEFAULT NULL'               : ', default=None',
                'ON UPDATE CURRENT_TIMESTAMP': ', onupdate=datetime.datetime.now'
        }
        result = ''
        for constraint in constraints:
            result += constraints_mapping.get(constraint, f', {constraint.lower()}')
        return result


def create_models(db_structure: list, project_folder: str) -> bool:
    if len(project_folder) == 0:
        project_folder = getcwd()
    
    if not db_structure:
        print("Database structure is empty")
        return False
    
    models_path_file = path.join(project_folder, "models.py")
    if path.exists(models_path_file):
        remove(models_path_file)
        logging.warning(f"File {models_path_file} already exists and will be overwritten")
    
    if not path.exists(project_folder):
        mkdir(project_folder)
    
    # Create the header with imports only once
    generator = ModelGenerator(db_structure[0])
    header_code = generator.generate_models().split('\n', 5)[:5]
    header_code = '\n'.join(header_code) + '\n\n'
    
    with open(models_path_file, "w") as f:
        f.write(header_code)
    
    # Generate models for each database
    for db_data in db_structure:
        logging.info(f"==> VAR: db_data   TYPE: {type(db_data)}, CONTENT: {db_data}")
        generator = ModelGenerator(db_data)
        models_code = generator.generate_models().split('\n', 5)[5:]
        models_code = '\n'.join(models_code)
        with open(models_path_file, "a") as f:
            f.write(models_code)
    
    return True


if __name__ == '__main__':
    # Example usage
    json_input = """
    [
      {
        "database": "your_database_name",
        "tables": [
          {
            "name": "profiles",
            "columns": [
              {
                "name": "id",
                "type": "INT",
                "constraints": [
                  "PRIMARY KEY",
                  "AUTO_INCREMENT"
                ]
              },
              {
                "name": "user_id",
                "type": "INT",
                "constraints": [
                  "NOT NULL"
                ]
              },
              {
                "name": "first_name",
                "type": "VARCHAR(50)",
                "constraints": [
                  "NOT NULL"
                ]
              },
              {
                "name": "last_name",
                "type": "VARCHAR(50)",
                "constraints": []
              },
              {
                "name": "birthdate",
                "type": "DATE",
                "constraints": []
              },
              {
                "name": "bio",
                "type": "TEXT",
                "constraints": []
              }
            ],
            "primary key": [
              {
                "type": "INDEX",
                "columns": ["user_id"]
              }
            ],
            "indexes": [
              {
                "name": "idx_user_first_last_name",
                "type": "INDEX",
                "columns": ["first_name", "last_name"]
              }
            ],
            "unique": [
              {
                "name": "idx_user_id",
                "type": "INDEX",
                "columns": ["user_id"]
              }
            ],
            "foreign_keys": [
              {
                "name": "fk_profiles_user_id",
                "column": "user_id",
                "references": {
                  "table": "users",
                  "column": "id",
                  "on_delete": "CASCADE",
                  "on_update": "CASCADE"
                }
              }
            ]
          }
        ]
      }
    ]
    """
    generator = ModelGenerator(json_input)
    models_code = generator.generate_models()
    print(models_code)
