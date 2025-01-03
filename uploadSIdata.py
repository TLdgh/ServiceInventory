import pyodbc, psycopg2, os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# PostgreSQL connection details
host_pg = os.getenv("host_pg")
port_pg = os.getenv("port_pg")
dbname_pg = os.getenv("dbname_pg")
user_pg = os.getenv("user_pg")

# Azure SQL Database connection details
server_azure = os.getenv("server_azure")
database_azure = os.getenv("database_azure")
username_azure = os.getenv("username_azure")
password_azure = os.getenv("password_azure")
port_azure = os.getenv("port_azure")



# Connect to PostgreSQL
connect_pg = psycopg2.connect(
        host=host_pg,
        port=port_pg,
        dbname=dbname_pg,
        user=user_pg
)
# Create a cursor object to interact with the PostgreSQL database
cursor_pg = connect_pg.cursor()

# Connect to Azure SQL Database
connect_azure = pyodbc.connect(
    'DRIVER={ODBC Driver 18 for SQL Server};'
    'SERVER=' + server_azure + ',' + port_azure + ';'
    'DATABASE=' + database_azure + ';'
    'ENCRYPT=yes;TrustServerCertificate=yes;'
    'UID=' + username_azure + ';PWD=' + password_azure
)
cursor_azure = connect_azure.cursor()



# Step 1: Get column names from SIdata
cursor_pg.execute("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'SIdata' AND table_schema = 'public'")
columns_pg = cursor_pg.fetchall()

# Step 2: Create the empty table in Azure SQL
create_table_query = f"CREATE TABLE [Data].[SIdata] ("
clean_colname=[]
for col in columns_pg:
    col_name = col[0].replace('\ufeff', '') if col[0].startswith('\ufeff') else col[0]
    clean_colname.append(col_name)
    create_table_query += f"[{col_name}] NVARCHAR(MAX), "

create_table_query = create_table_query.rstrip(', ')  # Remove trailing comma
create_table_query += ")"

# Execute the query to create the table
cursor_azure.execute(create_table_query)
connect_azure.commit()



# Step 3: Fetch data from PostgreSQL and insert it into Azure
cursor_pg.execute("SELECT * FROM public.\"SIdata\"")
rows_pg = cursor_pg.fetchall()

# Insert data into Azure SQL
insert_query = "INSERT INTO [Data].[SIdata] (" + ", ".join([col for col in clean_colname]) + ") VALUES (" + ", ".join(["?" for _ in clean_colname]) + ")"
for row in rows_pg:
    cursor_azure.execute(insert_query, row)
# Commit the insert operation
connect_azure.commit()



# Close connections
cursor_pg.close()
connect_pg.close()
cursor_azure.close()
connect_azure.close()
