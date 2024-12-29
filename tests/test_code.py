import pyodbc

# Connection string
connection_string = (
    "Driver={ODBC Driver 18 for SQL Server};"
    "Server=fabric-database-fk7ycir775zejipdowbg4zkslu.database.fabric.microsoft.com,1433;"
    "Database=RAKEZ_BI_Works_SLVR_DS-2ad67706-924d-4326-b383-c891c62818e7;"
    "Encrypt=yes;"
    "TrustServerCertificate=no;"
    "Authentication=ActiveDirectoryInteractive;"
)

try:
    conn = pyodbc.connect(connection_string)
    print("Connection successful!")
    conn.close()
except Exception as e:
    print(f"Connection failed: {e}")


import pyodbc

# Connection string with Active Directory username and password
connection_string = (
    "Driver={ODBC Driver 18 for SQL Server};"
    "Server=fabric-database-fk7ycir775zejipdowbg4zkslu.database.fabric.microsoft.com,1433;"
    "Database=RAKEZ_BI_Works_SLVR_DS-2ad67706-924d-4326-b383-c891c62818e7;"
    "Encrypt=yes;"
    "TrustServerCertificate=no;"
    "Authentication=ActiveDirectoryPassword;"
    "UID=yourusername@rartg.com;"
    """PWD=yourpassword;"""
)

try:
    conn = pyodbc.connect(connection_string)
    print("Connection successful!")
    conn.close()
except Exception as e:
    print(f"Connection failed: {e}")

import pyodbc
from sqlalchemy import create_engine


# Working pyodbc connection string
pyodbc_connection_string = (
    "Driver={ODBC Driver 18 for SQL Server};"
    "Server=fabric-database-fk7ycir775zejipdowbg4zkslu.database.fabric.microsoft.com,1433;"
    "Database=RAKEZ_BI_Works_SLVR_DS-2ad67706-924d-4326-b383-c891c62818e7;"
    "Encrypt=yes;"
    "TrustServerCertificate=no;"
    "Authentication=ActiveDirectoryPassword;"
    "UID=yourusername@gmail.com;"
    """PWD=yourpassword;"""
)

# Create a pyodbc connection string for SQLAlchemy
sqlalchemy_connection_string = f"mssql+pyodbc:///?odbc_connect={pyodbc_connection_string.replace(';', '%3B')}"

# Create SQLAlchemy engine
engine = create_engine(sqlalchemy_connection_string)

# Test the connection
try:
    with engine.connect() as connection:
        print("Connection successful!")
except Exception as e:
    print(f"Connection failed: {e}")
