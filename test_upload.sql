USE TBSproj;


-- Create a new schema named TestSchema
IF NOT EXISTS (SELECT * FROM sys.schemas where name = 'TestSchema')
BEGIN
    EXEC('CREATE SCHEMA TestSchema');
END;


-- Create a table in the TestSchema schema
IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = 'TestSchema' AND TABLE_NAME = 'Employees')
BEGIN
    CREATE TABLE TestSchema.Employees (
        Id INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
        Name NVARCHAR(50),
        Location NVARCHAR(50)
    );
END;

-- Empty the table Employees before inserting new data
DELETE FROM TestSchema.Employees;

-- Insert sample data into the Employees table
INSERT INTO TestSchema.Employees (Name, Location) 
VALUES
(N'Apple', N'Australia'),
(N'Nikita', N'India'),
(N'Tom', N'Germany');

-- Query the data to verify insertion
SELECT * FROM TestSchema.Employees;

