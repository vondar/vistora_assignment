from fastapi import FastAPI, HTTPException, Query
from typing import List, Dict, Any, Optional
import mysql.connector
import json
from database_crawler import crawl_database_schema, generate_python_models

app = FastAPI(
    title="MySQL Database Crawler API",
    description="An API to retrieve database schema, query tables, and generate model representations.",
    version="1.0.0"
)

# Load database credentials from config file
with open("config.json", "r") as config_file:
    db_credentials = json.load(config_file)

@app.get("/schema", response_model=Dict[str, Any], summary="Retrieve database schema", description="Fetches metadata of the database schema including tables, columns, primary keys, foreign keys, and indexes.")
async def read_schema():
    schema_metadata = crawl_database_schema()
    if schema_metadata:
        return schema_metadata
    else:
        raise HTTPException(status_code=500, detail="Failed to retrieve database schema")

@app.get("/table/{table_name}", response_model=List[Dict[str, Any]], summary="Fetch data from a table", description="Retrieves all records from a specified table with optional filtering, sorting, and pagination.")
async def read_table(
    table_name: str,
    filter: Optional[str] = Query(None, description="Filter condition in 'column=value' format"),
    sort: Optional[str] = Query(None, description="Column to sort by, with optional ':desc' for descending order"),
    page: Optional[int] = Query(1, description="Page number for pagination"),
    limit: Optional[int] = Query(20, description="Number of records per page")
):
    schema_metadata = crawl_database_schema()
    if not schema_metadata or table_name not in schema_metadata['tables']:
        raise HTTPException(status_code=404, detail=f"Table '{table_name}' not found in schema")
    
    try:
        connection = mysql.connector.connect(**db_credentials)
        cursor = connection.cursor(dictionary=True)
        query = f"SELECT * FROM {table_name}"
        
        # Apply filter condition
        if filter:
            column, value = filter.split("=")
            query += f" WHERE {column} = '{value}'"
        
        # Apply sorting
        if sort:
            column, *order = sort.split(":")
            order = "DESC" if order and order[0].lower() == "desc" else "ASC"
            query += f" ORDER BY {column} {order}"
        
        # Apply pagination
        offset = (page - 1) * limit
        query += f" LIMIT {limit} OFFSET {offset}"
        
        cursor.execute(query)
        records = cursor.fetchall()
        return records
    except mysql.connector.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    finally:
        cursor.close()
        connection.close()

@app.get("/models", response_model=Dict[str, str], summary="Generate Python model classes", description="Dynamically generates Python model class definitions based on the database schema.")
async def get_models():
    schema_metadata = crawl_database_schema()
    if schema_metadata:
        return generate_python_models(schema_metadata)
    else:
        raise HTTPException(status_code=500, detail="Failed to generate models")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
