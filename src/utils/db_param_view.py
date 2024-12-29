import os

# Connection string to SQL Server database
pyodbc_connection_string = (
    "Driver={ODBC Driver 18 for SQL Server};"
    "Server=fabric-database-fk7ycir775zejipdowbg4zkslu.database.fabric.microsoft.com,1433;"
    "Database=RAKEZ_BI_Works_SLVR_DS-2ad67706-924d-4326-b383-c891c62818e7;"
    "Encrypt=yes;"
    "TrustServerCertificate=no;"
    "Authentication=ActiveDirectoryPassword;"
    "UID=yourusername@gmail.com;"
    "PWD=yourpassword;"
)

# Create a pyodbc connection string for SQLAlchemy
sqlalchemy_connection_string = f"mssql+pyodbc:///?odbc_connect={pyodbc_connection_string.replace(';', '%3B')}"
SQL_SERVER_CONNECTION_STRING = sqlalchemy_connection_string
# Directory to store Parquet files for the Bronze layer
BRONZE_DIR = os.getenv('BRONZE_DIR')

# Mapping Pandas types to SQL Server types
PANDAS_TO_SQL_TYPE_MAPPING = {
    'object': 'NVARCHAR(MAX)',
    'int64': 'BIGINT',
    'float64': 'FLOAT',
    'datetime64[ns]': 'DATETIME',
    'bool': 'BIT',
}
