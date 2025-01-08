import pyodbc, psycopg2, pytest, os
from dotenv import load_dotenv
import datetime

# Load environment variables from .env file
load_dotenv()

# PostgreSQL connection details
host_pg=os.getenv("host_pg")
port_pg=os.getenv("port_pg")
dbname_pg=os.getenv("dbname_pg")
user_pg=os.getenv("user_pg")
        
# Connect to Azure SQL Database
server_azure = os.getenv("server_azure")
database_azure = os.getenv("database_azure")
username_azure = os.getenv("username_azure")
password_azure = os.getenv("password_azure")
port_azure = os.getenv("port_azure")



@pytest.fixture
def pg_connection():
    connect_pg=psycopg2.connect(
        host=host_pg,
        port=port_pg,
        dbname=dbname_pg,
        user=user_pg
    )

    #Create a cursor object to interact with the database
    cursor_pg=connect_pg.cursor()
    yield cursor_pg #provide the cursor to the test
    cursor_pg.close()
    connect_pg.close()



@pytest.fixture
def azure_connection():
    # ENCRYPT defaults to yes starting in ODBC Driver 18. It's good to always specify ENCRYPT=yes on the client side to avoid MITM attacks.
    connect_azure = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};'
                                   'SERVER='+server_azure+','+port_azure+';'
                                   'DATABASE='+database_azure+';'
                                   'ENCRYPT=yes;TrustServerCertificate=yes;'
                                   'UID='+username_azure+';PWD='+ password_azure)
    cursor_azure = connect_azure.cursor()
    yield cursor_azure #provide the cursor to the test
    cursor_azure.close()
    connect_azure.close()


# Test function for extracting tables from local PostgreSQL database
def test_pgExtract(pg_connection):
    #Ground truth
    ground_truth=[(datetime.date(2021, 10, 11), 14810.25, 14897.25, 14585.5, 14653.25, 1104423)]
    
    #Query the sample data
    pg_connection.execute('select * from "Data"."NQ_W" limit 1;')
    result_pg=pg_connection.fetchall()
    
    # Assert the data matches ground truth
    assert result_pg==ground_truth, f"Data mismatch: {result_pg} != {ground_truth}"


# Test Azure resource connection
def test_azureSqlConnect(azure_connection):
    #Query to get the SQL Server version
    azure_connection.execute("SELECT @@version;") 
    version = azure_connection.fetchone() 
    print(version)
    #Assert the version is not None
    assert version is not None, "Azure SQL Database connected."



# Test function to load and run the SQL script file
def test_create_table_from_sql(azure_connection):
    # Read the SQL script file
    with open('test_upload.sql', 'r') as file:
        sql_script = file.read()

    # Execute the SQL script to create the schema, table, and insert data
    azure_connection.execute(sql_script)
    # Commit the transaction to the database
    azure_connection.commit()

    # Verify if the table was created and data was inserted by querying the table
    azure_connection.execute("SELECT * FROM TestSchema.Employees")
    result = azure_connection.fetchone()
    # Print the result for debugging purposes. Alternatively view the table in Schema_Data.sql
    print("Table 'TestSchema.Employees' created and verified:", result)
    
    # Check that the result is not None (meaning the table exists and data was inserted)
    assert result is not None, "TestSchema.Employees table was not created or no data inserted."
    
    