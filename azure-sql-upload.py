import pyodbc, psycopg2, os
from dotenv import load_dotenv

# Load environment variables from .env file for secure storage of sensitive information like database credentials
load_dotenv()

# PostgreSQL connection details - retrieved from the .env file
host_pg = os.getenv("host_pg")  
port_pg = os.getenv("port_pg")  
dbname_pg = os.getenv("dbname_pg")  
user_pg = os.getenv("user_pg")  

# Azure SQL Database connection details - retrieved from the .env file
server_azure = os.getenv("server_azure") 
database_azure = os.getenv("database_azure")  
username_azure = os.getenv("username_azure") 
password_azure = os.getenv("password_azure")  
port_azure = os.getenv("port_azure")  



try:
    # Connect to PostgreSQL database using psycopg2
    connect_pg = psycopg2.connect(
        host=host_pg,
        port=port_pg,
        dbname=dbname_pg,
        user=user_pg
    )
    # Create a cursor object to interact with the PostgreSQL database
    cursor_pg = connect_pg.cursor()
    
    # Test query to check connection and table access for PostgreSQL
    cursor_pg.execute('select * from "Data"."NQ_W";')
    result_pg = cursor_pg.fetchall()  # Fetch all rows from the query result
    columns = [desc[0] for desc in cursor_pg.description]  # Get the column names from the description of the result set
    print(f"Fetched {len(result_pg)} rows from PostgreSQL.")



    # Connect to Azure SQL Database using pyodbc
    connect_azure = pyodbc.connect(
        'DRIVER={ODBC Driver 18 for SQL Server};'
        'SERVER=' + server_azure + ',' + port_azure + ';'
        'DATABASE=' + database_azure + ';'
        'ENCRYPT=yes;TrustServerCertificate=yes;'  # Ensures encryption and avoids MITM attacks
        'UID=' + username_azure + ';PWD=' + password_azure
    )
    cursor_azure = connect_azure.cursor()

    # Create the 'Data' schema and the 'NQ_W' table in Azure SQL if they do not already exist
    create_table_query = """
        IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = 'Data' AND TABLE_NAME = 'NQ_W')
        BEGIN
            CREATE TABLE [Data].[NQ_W] (
                [Date] DATE,  -- Date field
                [Open] FLOAT,  -- Opening price
                [High] FLOAT,  -- Highest price
                [Low] FLOAT,  -- Lowest price
                [Close] FLOAT,  -- Closing price
                [Volume] BIGINT  -- Trading volume
            );
        END;
    """
    cursor_azure.execute(create_table_query)  # Execute the table creation query
    connect_azure.commit()  # Commit the changes to Azure SQL

    # Create the insert query dynamically, mapping columns and values
    insert_query = f"INSERT INTO [Data].[NQ_W] ({', '.join([f'[{col}]' for col in columns])}) VALUES ({', '.join(['?'] * len(columns))});"
    # Insert each row from PostgreSQL into Azure SQL
    for row in result_pg:
        cursor_azure.execute(insert_query, row)
    connect_azure.commit()  
    print(f"Uploaded {len(result_pg)} rows to Azure SQL Database table NQ_W.")

except Exception as error:
    print(f"Error: {error}")

finally:
    # Ensure all connections are closed
    if 'cursor_pg' in locals():
        cursor_pg.close() 
    if 'connect_pg' in locals():
        connect_pg.close() 
    if 'cursor_azure' in locals():
        cursor_azure.close() 
    if 'connect_azure' in locals():
        connect_azure.close()  