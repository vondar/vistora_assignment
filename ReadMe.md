# MySQL Database Crawler API - Detailed Documentation

## **Introduction**
This project is a **MySQL Database Crawler API** built using Python. The API connects to a MySQL database, extracts metadata, and provides dynamically generated Python model classes for the database schema. It also allows users to query table data with filtering, sorting, and pagination.



---

## **Tools & Technologies Used**
### 1. **FastAPI**
FastAPI is a modern web framework for building APIs with Python. It is fast, easy to use, and supports automatic OpenAPI and Swagger documentation.
- **Why FastAPI?**
  - Asynchronous support for better performance.
  - Automatic request validation.
  - In-built API documentation (Swagger UI & ReDoc).

**Reference:** [FastAPI Official Docs](https://fastapi.tiangolo.com/)

### 2. **MySQL**
MySQL is an open-source relational database management system used to store structured data.
- **Why MySQL?**
  - Scalable and widely used.
  - Supports indexing and relational data.
  - Integrates well with Python via `mysql-connector`.

**Reference:** [MySQL Official Docs](https://dev.mysql.com/doc/)

### 3. **MySQL Connector for Python**
`mysql-connector-python` is a Python library that allows direct communication with MySQL databases.
- **Why use MySQL Connector?**
  - Secure and efficient database connections.
  - Supports executing SQL queries directly from Python.

**Reference:** [MySQL Connector Docs](https://dev.mysql.com/doc/connector-python/en/)

### 4. **JSON Configuration**
The project uses a `config.json` file to store database credentials securely.
- **Why use JSON?**
  - Prevents hardcoding sensitive information.
  - Easily readable and modifiable format.

---

## **Algorithms & Functions Used**
### **1. Crawling Database Schema**
#### **Function: `crawl_database_schema()`**
This function retrieves metadata from a MySQL database, including tables, columns, primary keys, foreign keys, and indexes.
- **Steps Involved:**
  1. Establish a connection to MySQL.
  2. Execute `SHOW TABLES` to retrieve all table names.
  3. For each table, execute `SHOW COLUMNS` to get column details.
  4. Retrieve primary keys and foreign keys from `information_schema.KEY_COLUMN_USAGE`.
  5. Retrieve indexes using `SHOW INDEXES`.

### **2. Generating Python Model Classes**
#### **Function: `generate_python_models(schema)`**
This function dynamically creates Python classes representing the database tables.
- **Steps Involved:**
  1. Convert table names to CamelCase class names.
  2. Define `__init__` method with attributes for each column.
  3. Include relationships for foreign keys.

### **3. Fetching Table Data with Filtering & Sorting**
#### **Function: `read_table(table_name, filter, sort, page, limit)`**
This function retrieves table data with filtering, sorting, and pagination.
- **Steps Involved:**
  1. Validate if the table exists in the schema.
  2. Construct a `SELECT` query with optional `WHERE` (filtering).
  3. Apply `ORDER BY` for sorting.
  4. Apply `LIMIT` and `OFFSET` for pagination.

---

## **Database Schema & Structure**
The project supports **any MySQL database**, but for testing, it uses the `sakila` sample database.

- **Tables in Sakila Database:**
  - `actor`: Stores actor details.
  - `film`: Stores movie details.
  - `customer`: Stores customer details.

**Reference:** [Sakila Database Docs](https://dev.mysql.com/doc/sakila/en/)

---

## **API Endpoints & Usage**
### **1. Retrieve Database Schema**
**Endpoint:** `GET /schema`
- **Response:** Returns all tables, columns, and relationships.

### **2. Fetch Data from a Table**
**Endpoint:** `GET /table/{table_name}`
- **Query Parameters:**
  - `filter`: Apply conditions (e.g., `column=value`).
  - `sort`: Sort results (`column:desc`).
  - `page`: Pagination (default: `1`).
  - `limit`: Number of records (default: `20`).

### **3. Generate Python Models**
**Endpoint:** `GET /models`
- **Response:** Returns dynamically generated Python model classes for all tables.

---

## **How to Use the App**
### **1. Installation & Setup**
#### **Step 1: Install Dependencies**
```bash
pip install fastapi uvicorn mysql-connector-python
```

#### **Step 2: Configure Database Credentials**
- Create a `config.json` file with the following structure:
```json
{
    "host": "your-mysql-host",
    "user": "your-username",
    "password": "your-password",
    "database": "your-database-name",
    "port": 3306
}
```

#### **Step 3: Run the API**
```bash
uvicorn api:app --reload
```

### **2. Accessing API Documentation**
- Open a browser and go to:
  - Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
  - ReDoc UI: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

### **3. Making API Requests**
- Use **Swagger UI** or a tool like **Postman** to test the API.
- Example request using `curl`:
```bash
curl -X 'GET' 'http://127.0.0.1:8000/table/actor?filter=first_name=John&sort=actor_id:desc&page=1&limit=5' -H 'accept: application/json'
```

---

## **References**
1. FastAPI Docs - [https://fastapi.tiangolo.com/](https://fastapi.tiangolo.com/)
2. MySQL Docs - [https://dev.mysql.com/doc/](https://dev.mysql.com/doc/)
3. MySQL Connector - [https://dev.mysql.com/doc/connector-python/en/](https://dev.mysql.com/doc/connector-python/en/)
4. Sakila Sample Database - [https://dev.mysql.com/doc/sakila/en/](https://dev.mysql.com/doc/sakila/en/)

---

