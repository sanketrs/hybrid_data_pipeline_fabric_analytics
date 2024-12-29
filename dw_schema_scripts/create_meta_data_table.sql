CREATE TABLE DataProcessingMetadata (
    id INT IDENTITY(1,1) PRIMARY KEY,
    file_name NVARCHAR(MAX),
    sheet_name NVARCHAR(MAX),
    row_count INT,
    last_processed_time DATETIME
);