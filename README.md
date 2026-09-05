


Customer Data ETL Pipeline & SQL Analysis
Project Overview
This project implements an end-to-end ETL (Extract, Transform, Load) pipeline for customer data using Python, Pandas, and MySQL.

The project takes customer data from a CSV file, loads it into MySQL, performs data cleaning and validation using Pandas, stores the cleaned data in a separate MySQL table, and then performs SQL-based customer analysis.

Project Flow
CSV File
↓
Extract Data into MySQL
↓
Read MySQL Data using Pandas
↓
Transform / Clean Data
↓
Load Cleaned Data into MySQL
↓
SQL Queries & Analysis

Technologies Used
Python

Pandas

MySQL

SQL

SQLAlchemy

mysql-connector-python

CSV

Dataset
The project uses the Mall Customers dataset with fields including:

CustomerID

Genre

Age

Annual Income (k$)

Spending Score

ETL Process
1. Extract
The pipeline connects to a MySQL database and checks whether the source table mall_customers exists.

If the table does not exist, the CSV dataset is read using Pandas and the source table is created in MySQL. The CSV records are then inserted into the table.

2. Transform
The data is read from MySQL into a Pandas DataFrame.

The following cleaning operations are performed:

Check for missing values

Remove duplicate rows

Remove extra spaces from the Genre column

Convert Genre values to uppercase

Remove invalid ages

Remove invalid annual income values

Remove invalid spending scores

Validation rules used:

Age must be greater than 0 and less than or equal to 100

Annual income must be greater than or equal to 0

Spending score must be between 0 and 100

3. Load
A cleaned table named mall_customers_cleaned is created in MySQL.

The cleaned DataFrame is inserted into this table.

CustomerID is used as the primary key.

SQL Analysis
The project performs several SQL analyses on the cleaned customer data.

All Customers
Retrieves all records from the cleaned table.

Customers Above 30
Finds customers whose age is greater than 30.

High Spending Customers
Finds customers with a spending score greater than 70.

Average Age
Calculates the average customer age using AVG().

Gender-wise Customer Count
Groups customers by Genre and calculates the number of customers in each group using COUNT() and GROUP BY.

Top 5 Highest Income Customers
Sorts customers by annual income in descending order and returns the top five using ORDER BY and LIMIT.

Project Structure
ETL Project/
│
├── Mall_Customers (1).csv
│
├── clean.all.vscode.py
│
└── README.md
How to Run
1. Install required Python libraries
pip install pandas mysql-connector-python sqlalchemy
2. Start MySQL
Make sure MySQL Server is running.

3. Configure the database
The Python script connects to the MySQL database named customer.

Update the MySQL username and password in the Python script according to your local MySQL setup.

4. Keep the CSV file in the expected project location
The script expects the Mall Customers CSV file to be available relative to the Python project structure.

5. Run the Python script
python clean.all.vscode.py
The script will:

Connect to MySQL

Load the source CSV data when required

Read the source data

Clean and validate the data

Create the cleaned MySQL table

Insert cleaned records

Execute SQL analysis queries

Save query results into MySQL tables

Close the database connections

Key Learning Outcomes
Understanding the ETL process

Connecting Python with MySQL

Reading CSV data using Pandas

Cleaning and validating real-world data

Removing duplicates and standardizing text

Loading transformed data into MySQL

Writing SQL filtering and aggregation queries

Using WHERE, AVG(), COUNT(), GROUP BY, ORDER BY, and LIMIT

Using SQLAlchemy to write query results back to MySQL

Resume Project Title
Customer Data ETL Pipeline & SQL Analysis

Resume Description
Developed an end-to-end customer data ETL pipeline using Python, Pandas, and MySQL. Extracted customer data from CSV, performed data cleaning and validation, removed duplicates and invalid records, standardized categorical values, loaded the transformed data into MySQL, and performed SQL-based customer analysis using filtering, aggregation, grouping, sorting, and ranking-style queries.

Author
Developed as a Python, SQL, and ETL practice project.
