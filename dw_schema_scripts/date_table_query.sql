-- Create the Date Table
CREATE TABLE Dim_Date (
    DateKey INT PRIMARY KEY, -- MMDDYYYY format
    Date NVARCHAR(10) NOT NULL, -- MM-DD-YYYY format
    Year INT NOT NULL,
    Quarter INT NOT NULL,
    Month INT NOT NULL,
    Day INT NOT NULL,
    Week INT NOT NULL,
    DayOfWeek INT NOT NULL, -- 1=Sunday, 2=Monday, ...
    DayName NVARCHAR(20) NOT NULL, -- Name of the day (e.g., Monday)
    MonthName NVARCHAR(20) NOT NULL, -- Name of the month (e.g., January)
    IsWeekend BIT NOT NULL, -- 1 = Saturday or Sunday
    IsHoliday BIT DEFAULT 0 -- Customizable field for marking holidays
);

-- Populate the Date Table
DECLARE @StartDate DATE = '2010-01-01'; -- Set your start date
DECLARE @EndDate DATE = '2030-12-31'; -- Set your end date

;WITH DateSequence AS (
    SELECT CAST(@StartDate AS DATE) AS DateValue
    UNION ALL
    SELECT DATEADD(DAY, 1, DateValue)
    FROM DateSequence
    WHERE DateValue < @EndDate
)
INSERT INTO Dim_Date
SELECT 
    CAST(FORMAT(DateValue, 'MMddyyyy') AS INT) AS DateKey, -- DateKey in MMDDYYYY format
    FORMAT(DateValue, 'MM-dd-yyyy') AS Date, -- Date in MM-DD-YYYY format
    YEAR(DateValue) AS Year,
    DATEPART(QUARTER, DateValue) AS Quarter,
    MONTH(DateValue) AS Month,
    DAY(DateValue) AS Day,
    DATEPART(WEEK, DateValue) AS Week,
    DATEPART(WEEKDAY, DateValue) AS DayOfWeek,
    DATENAME(WEEKDAY, DateValue) AS DayName,
    DATENAME(MONTH, DateValue) AS MonthName,
    CASE WHEN DATEPART(WEEKDAY, DateValue) IN (1, 7) THEN 1 ELSE 0 END AS IsWeekend,
    0 AS IsHoliday -- Default value; update later for specific holidays
FROM DateSequence
OPTION (MAXRECURSION 0);

-- Indexing for Performance
CREATE INDEX IDX_DimDate_Date ON Dim_Date (Date);
CREATE INDEX IDX_DimDate_Year ON Dim_Date (Year);
CREATE INDEX IDX_DimDate_Month ON Dim_Date (Month);
CREATE INDEX IDX_DimDate_Week ON Dim_Date (Week);
