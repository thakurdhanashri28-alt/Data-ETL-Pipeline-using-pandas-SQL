import mysql.connector
import pandas as pd                                                              
from pathlib import Path
from sqlalchemy import URL, create_engine                                                                                                                                                                                                    

# ==============================
# 1. EXTRACT - Connect to MySQL
# ==============================

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Rinu@1234",
    database="customer"
)

sql_engine = create_engine(
    URL.create(
        "mysql+mysqlconnector",
        username="root",
        password="Rinu@1234",
        host="localhost",
        database="customer"
    )
)

print("MySQL Connection Successful!")

# Create the source table from the bundled CSV when it is not in the database.
cursor = connection.cursor()
cursor.execute("SHOW TABLES LIKE 'mall_customers'")
if cursor.fetchone() is None:
    csv_file = Path(__file__).resolve().parent.parent / "Mall_Customers (1).csv"
    source_df = pd.read_csv(csv_file)
    create_source_table = """
    CREATE TABLE mall_customers (
        CustomerID INT,
        Genre VARCHAR(20),
        Age INT,
        `Annual_Income_(k$)` INT,
        Spending_Score INT
    )
    """
    cursor.execute(create_source_table)
    insert_source = """
    INSERT INTO mall_customers
    (CustomerID, Genre, Age, `Annual_Income_(k$)`, Spending_Score)
    VALUES (%s, %s, %s, %s, %s)
    """
    cursor.executemany(
        insert_source,
        [tuple(row) for row in source_df.itertuples(index=False, name=None)]
    )
    connection.commit()
    print("Source CSV loaded into mall_customers")
cursor.close()

# Read MySQL table using Pandas
query = "SELECT * FROM mall_customers"

df = pd.read_sql(query, connection)

print("\nOriginal Data:")
print(df.head())           


# ==============================
# 2. TRANSFORM - Data Cleaning
# ==============================

print("\nChecking Missing Values:")
print(df.isnull().sum())

# Remove duplicate rows
df = df.drop_duplicates()

# Remove extra spaces from Genre column
df["Genre"] = df["Genre"].astype(str).str.strip()

# Convert Gender values to uppercase
df["Genre"] = df["Genre"].str.upper()

# Remove invalid ages
df = df[(df["Age"] > 0) & (df["Age"] <= 100)]

# Remove invalid income values
df = df[df["Annual_Income_(k$)"] >= 0]

# Remove invalid spending scores
df = df[
    (df["Spending_Score"] >= 0) &
    (df["Spending_Score"] <= 100)
]

print("\nCleaned Data:")
print(df.head())

print("\nTotal Rows After Cleaning:", len(df))


# ==============================
# 3. LOAD - Create New Table
# ==============================

cursor = connection.cursor()

# Create cleaned table
create_table_query = """
CREATE TABLE IF NOT EXISTS mall_customers_cleaned (
    CustomerID INT PRIMARY KEY,
    Genre VARCHAR(20),
    Age INT,
    Annual_Income INT,
    Spending_Score INT
)
"""

cursor.execute(create_table_query)

# Clear old data
cursor.execute("TRUNCATE TABLE mall_customers_cleaned")


# ==============================
# 4. Insert Cleaned Data
# ==============================

insert_query = """
INSERT INTO mall_customers_cleaned
(CustomerID, Genre, Age, Annual_Income, Spending_Score)
VALUES (%s, %s, %s, %s, %s)
"""

for _, row in df.iterrows():
    values = (
        int(row["CustomerID"]),
        row["Genre"],
        int(row["Age"]),
        int(row["Annual_Income_(k$)"]),
        int(row["Spending_Score"])
    )
                       
    cursor.execute(insert_query, values)

connection.commit()

print("\nData Successfully Loaded into mall_customers_cleaned!")


# ==============================
# 5. SQL QUERIES
# ==============================

def save_query_result(query, table_name):
    result = pd.read_sql(query, connection)
    result.to_sql(
        table_name,
        sql_engine,
        if_exists="replace",
        index=False
    )
    return result

print("\n--- ALL CUSTOMERS ---")

all_customers = save_query_result(
    "SELECT * FROM mall_customers_cleaned",
    "query_all_customers"
)
print(all_customers.to_string(index=False))


print("\n--- CUSTOMERS ABOVE 30 ---")

customers_above_30 = save_query_result(
    """
    SELECT * FROM mall_customers_cleaned
    WHERE Age > 30
    """,
    "query_customers_above_30"
)
print(customers_above_30.to_string(index=False))


print("\n--- HIGH SPENDING CUSTOMERS ---")

high_spending_customers = save_query_result(
    """
    SELECT *
    FROM mall_customers_cleaned
    WHERE Spending_Score > 70
    """,
    "query_high_spending_customers" 
)
print(high_spending_customers.to_string(index=False))


print("\n--- AVERAGE AGE ---")

average_age = save_query_result(
    """
    SELECT AVG(Age) AS Average_Age
    FROM mall_customers_cleaned
    """,
    "query_average_age"
)
print(average_age.to_string(index=False))


print("\n--- GENDER-WISE CUSTOMER COUNT ---")

gender_wise_count = save_query_result(
    """
    SELECT Genre, COUNT(*) AS Total_Customers
    FROM mall_customers_cleaned
    GROUP BY Genre
    """,
    "query_gender_wise_count"
)
print(gender_wise_count.to_string(index=False))

print("\n--- TOP 5 HIGHEST INCOME CUSTOMERS ---")

top_5_income = save_query_result(
    """
    SELECT *
    FROM mall_customers_cleaned
    ORDER BY Annual_Income DESC
    LIMIT 5
    """,
    "query_top_5_highest_income"
)
print(top_5_income.to_string(index=False))


# ==============================
# CLOSE CONNECTION
# ==============================

cursor.close()
connection.close()
sql_engine.dispose()

print("\nETL Pipeline Completed Successfully!")