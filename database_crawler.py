import os
import json
import mysql.connector
from mysql.connector import pooling

# Load database credentials from config file
with open("config.json", "r") as config_file:
    db_credentials = json.load(config_file)

db_pool = pooling.MySQLConnectionPool(
    pool_name="mypool",
    pool_size=5,
    **db_credentials
)

def crawl_database_schema():
    """
    Crawls a MySQL database schema and extracts metadata.

    Returns:
        dict: A dictionary containing the database schema metadata.
    """
    try:
        connection = db_pool.get_connection()
        cursor = connection.cursor()
        schema = {'tables': {}}

        cursor.execute("SHOW TABLES")
        for (table_name,) in cursor.fetchall():
            schema['tables'][table_name] = {'columns': [], 'primary_key': [], 'foreign_keys': [], 'indexes': []}
            
            # Get columns
            cursor.execute(f"SHOW COLUMNS FROM {table_name}")
            for column in cursor.fetchall():
                schema['tables'][table_name]['columns'].append({
                    'name': column[0], 'data_type': column[1], 'nullable': column[2] == 'YES',
                    'key': column[3], 'extra': column[4]
                })
                if column[3] == 'PRI':
                    schema['tables'][table_name]['primary_key'].append(column[0])
            
            # Get foreign keys
            cursor.execute(f"""
                SELECT COLUMN_NAME, REFERENCED_TABLE_NAME, REFERENCED_COLUMN_NAME
                FROM information_schema.KEY_COLUMN_USAGE
                WHERE TABLE_NAME = '{table_name}' AND REFERENCED_TABLE_NAME IS NOT NULL;
            """)
            for fk in cursor.fetchall():
                schema['tables'][table_name]['foreign_keys'].append({
                    'column_name': fk[0], 'referenced_table_name': fk[1], 'referenced_column_name': fk[2]
                })
            
            # Get indexes
            cursor.execute(f"SHOW INDEXES FROM {table_name}")
            for index in cursor.fetchall():
                if index[2] != 'PRIMARY':
                    schema['tables'][table_name]['indexes'].append({
                        'name': index[2], 'columns': index[4], 'type': index[3], 'unique': not bool(index[1])
                    })
        
        return schema
    except mysql.connector.Error as e:
        print("Database error:", e)
        return None
    finally:
        cursor.close()
        connection.close()

def generate_python_models(schema):
    """ Generates Python model classes from the database schema. """
    models = {}
    for table_name, table_schema in schema['tables'].items():
        class_name = ''.join(word.capitalize() for word in table_name.split('_'))
        model_code = f"class {class_name}:\n"
        model_code += f"    \"\"\" Model class for table: {table_name} \"\"\"\n"
        model_code += f"    def __init__(self, {', '.join(column['name'] for column in table_schema['columns'])}):\n"
        for column in table_schema['columns']:
            model_code += f"        self.{column['name']} = {column['name']}\n"

        # Add foreign key relationships
        for fk in table_schema['foreign_keys']:
            related_class_name = ''.join(word.capitalize() for word in fk['referenced_table_name'].split('_'))
            model_code += f"\n    # Relationship to {related_class_name} via {fk['column_name']}\n"

        models[table_name] = model_code
    return models

if __name__ == "__main__":
    schema_metadata = crawl_database_schema()
    if schema_metadata:
        print(json.dumps(schema_metadata, indent=4))
        python_models = generate_python_models(schema_metadata)
        for table_name, model_code in python_models.items():
            print(f"\n# Model for {table_name}:")
            print(model_code)
    else:
        print("Failed to crawl database schema.")
