# Introduction

This repository demonstrates a sample workflow in data analysis, covering data collection, storage, and transfer. It showcases how data can be managed and moved between systems for effective integration, analysis, and visualization, particularly focusing on the connection between PostgreSQL and Azure SQL databases.

# Prerequisites
Python 3.8+ installed on your system.
PostgreSQL and Azure SQL Database set up and running.
Required Python libraries installed (see requirements.txt for details).
Power BI installed for data visualization.

# Content
1. Data Collection
Data can be gathered through various methods:
- API Calls: Retrieve data programmatically using APIs.
- Direct Downloads: Data files downloaded directly from online sources.
- SQL Queries: Create or fetch data using database queries.

Example in the repository:
- Data.NQ_W table was gathered from API. 
- TestSchema.Employees table was queryed from scratch using test_upload.sql. 
- public.SIdata was downloaded from a website as a csv file and transformed into a PostgreSQL database.

2. Data Storage
Collected data can be stored either locally or on remote servers for further processing.
- Local Storage: Data saved on local machines or databases like PostgreSQL.
- Remote Servers: Data uploaded to cloud platforms like Azure SQL Database.

Example:
test_connect.py: Tests the connection to local PostgreSQL databases and checks if the data is stored there. It also verifies if a table can be created and properly stored in Azure SQL databases.

3. Data Transformation and Transfer
Data transfer is critical for integration, especially when direct transfers between systems are not possible (e.g., PostgreSQL to MS SQL Server).

Key files for data transfer:
azure-sql-upload.py: A template demonstrating how Python can overcome limitations in transferring data between incompatible database engines. Specifically, it transfers Data.NQ_W from PostgreSQL localhost to Azure.

uploadSIdata.py: A specific example of azure-sql-upload.py. This script transfers public.SIdata from a local PostgreSQL database to an Azure SQL database, ensuring data accessibility for further analysis in tools like Power BI.

4. Data Visualization and Analysis
After transferring public.SIdata to Azure SQL, it becomes accessible for tools like Power BI. This enables users to:
- Create interactive dashboards.
- Perform advanced data analysis to gain actionable insights.


# Additional Instructions

## Test Connections
Use test_connect.py and test_upload.sql to test your connection and full functionality for both a local PostgreSQL database and Azure SQL Database.

## Transfer Data
Configure azure-sql-upload.py to move data between PostgreSQL and Azure SQL in cases where direct transfer isn't possible.

## Analyze Data
Data can be accessed from Azure SQL Database through Power BI for further analysis. Note: This section isn't included in this repository.