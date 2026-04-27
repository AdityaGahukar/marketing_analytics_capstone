CREATE DATABASE IF NOT EXISTS MARKETING_ANALYTICS;

USE DATABASE MARKETING_ANALYTICS;

CREATE SCHEMA IF NOT EXISTS GOLD;

USE SCHEMA GOLD;

CREATE WAREHOUSE IF NOT EXISTS COMPUTE_WH
WITH WAREHOUSE_SIZE = 'XSMALL'
AUTO_SUSPEND = 60
AUTO_RESUME = TRUE;

USE WAREHOUSE COMPUTE_WH;


-- Create S3 STAGE
CREATE OR REPLACE STAGE marketing_stage
URL = 's3://marketing-analytics-capstone/gold/'
FILE_FORMAT = (TYPE = PARQUET);


LIST @marketing_stage;


-- CREATE TABLES
CREATE OR REPLACE TABLE fact_campaign_performance (
    campaign_id NUMBER,
    date TIMESTAMP,
    channel_used STRING,
    company STRING,
    location STRING,
    total_clicks NUMBER,
    total_impressions NUMBER,
    total_cost FLOAT,
    avg_conversion_rate FLOAT,
    avg_roi FLOAT,
    avg_ctr FLOAT
);

CREATE OR REPLACE TABLE dim_campaign (
    campaign_id NUMBER,
    campaign_type STRING,
    target_audience STRING,
    customer_segment STRING
);

CREATE OR REPLACE TABLE dim_channel (
    channel_used STRING
);

CREATE OR REPLACE TABLE dim_company (
    company STRING
);

CREATE OR REPLACE TABLE dim_location (
    location STRING
);

CREATE OR REPLACE TABLE dim_date (
    date TIMESTAMP,
    year NUMBER,
    month NUMBER,
    month_name STRING,
    quarter NUMBER
);


-- CREATE OR REPLACE TABLE kpi_daily_campaign_performance (
--     date TIMESTAMP,
--     total_clicks NUMBER,
--     total_impressions NUMBER,
--     total_cost FLOAT,
--     avg_ctr FLOAT,
--     avg_roi FLOAT
-- );

-- CREATE OR REPLACE TABLE kpi_channel_performance (
--     date TIMESTAMP,
--     channel_used STRING,
--     total_clicks NUMBER,
--     total_impressions NUMBER,
--     avg_ctr FLOAT,
--     avg_roi FLOAT
-- );

-- CREATE OR REPLACE TABLE kpi_campaign_summary (
--     campaign_id NUMBER,
--     total_clicks NUMBER,
--     total_impressions NUMBER,
--     total_cost FLOAT,
--     avg_roi FLOAT
-- );

-- CREATE OR REPLACE TABLE kpi_monthly_trends (
--     year NUMBER,
--     month NUMBER,
--     total_clicks NUMBER,
--     total_impressions NUMBER,
--     avg_ctr FLOAT,
--     avg_roi FLOAT
-- );

CREATE TABLE IF NOT EXISTS stg_fact_campaign_performance LIKE fact_campaign_performance;
CREATE TABLE IF NOT EXISTS stg_dim_campaign LIKE dim_campaign;
CREATE TABLE IF NOT EXISTS stg_dim_channel LIKE dim_channel;
CREATE TABLE IF NOT EXISTS stg_dim_company LIKE dim_company;
CREATE TABLE IF NOT EXISTS stg_dim_location LIKE dim_location;
CREATE TABLE IF NOT EXISTS stg_dim_date LIKE dim_date;


-- FACT
COPY INTO stg_fact_campaign_performance
FROM @marketing_stage/fact_campaign_performance/
FILE_FORMAT = (TYPE = PARQUET)
MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE
PATTERN='.*\\.parquet'
ON_ERROR = SKIP_FILE;

-- DIMENSIONS
COPY INTO stg_dim_campaign
FROM @marketing_stage/dim_campaign/
FILE_FORMAT = (TYPE = PARQUET)
MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE
PATTERN='.*\\.parquet';

COPY INTO stg_dim_channel
FROM @marketing_stage/dim_channel/
FILE_FORMAT = (TYPE = PARQUET)
MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE
PATTERN='.*\\.parquet';

COPY INTO stg_dim_company
FROM @marketing_stage/dim_company/
FILE_FORMAT = (TYPE = PARQUET)
MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE
PATTERN='.*\\.parquet';

COPY INTO stg_dim_location
FROM @marketing_stage/dim_location/
FILE_FORMAT = (TYPE = PARQUET)
MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE
PATTERN='.*\\.parquet';

COPY INTO stg_dim_date
FROM @marketing_stage/dim_date/
FILE_FORMAT = (TYPE = PARQUET)
MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE
PATTERN='.*\\.parquet';


--  merge dim tables and then we move to fact tables


-- DIM CAMPAIGN
MERGE INTO dim_campaign tgt
USING stg_dim_campaign src
ON tgt.campaign_id = src.campaign_id
WHEN MATCHED THEN UPDATE SET
    campaign_type = src.campaign_type,
    target_audience = src.target_audience,
    customer_segment = src.customer_segment
WHEN NOT MATCHED THEN INSERT VALUES (
    src.campaign_id,
    src.campaign_type,
    src.target_audience,
    src.customer_segment
);

-- DIM CHANNEL
MERGE INTO dim_channel tgt
USING stg_dim_channel src
ON tgt.channel_used = src.channel_used
WHEN NOT MATCHED THEN INSERT VALUES (src.channel_used);

-- DIM COMPANY
MERGE INTO dim_company tgt
USING stg_dim_company src
ON tgt.company = src.company
WHEN NOT MATCHED THEN INSERT VALUES (src.company);

-- DIM LOCATION
MERGE INTO dim_location tgt
USING stg_dim_location src
ON tgt.location = src.location
WHEN NOT MATCHED THEN INSERT VALUES (src.location);

-- DIM DATE
MERGE INTO dim_date tgt
USING stg_dim_date src
ON tgt.date = src.date
WHEN MATCHED THEN UPDATE SET
    year = src.year,
    month = src.month,
    month_name = src.month_name,
    quarter = src.quarter
WHEN NOT MATCHED THEN INSERT VALUES (
    src.date,
    src.year,
    src.month,
    src.month_name,
    src.quarter
);

--  trunacte

TRUNCATE table stg_dim_channel;
TRUNCATE TABLE stg_dim_campaign;
TRUNCATE TABLE stg_dim_company;
truncate  table  stg_dim_date;
truncate table stg_dim_location;




MERGE INTO fact_campaign_performance tgt
USING stg_fact_campaign_performance src
ON tgt.campaign_id = src.campaign_id
AND tgt.date = src.date

WHEN MATCHED THEN UPDATE SET
    channel_used = src.channel_used,
    company = src.company,
    location = src.location,
    total_clicks = src.total_clicks,
    total_impressions = src.total_impressions,
    total_cost = src.total_cost,
    avg_conversion_rate = src.avg_conversion_rate,
    avg_roi = src.avg_roi,
    avg_ctr = src.avg_ctr

WHEN NOT MATCHED THEN INSERT VALUES (
    src.campaign_id,
    src.date,
    src.channel_used,
    src.company,
    src.location,
    src.total_clicks,
    src.total_impressions,
    src.total_cost,
    src.avg_conversion_rate,
    src.avg_roi,
    src.avg_ctr
);

truncate table stg_fact_campaign_performance;



CREATE OR REPLACE TABLE vw_campaign_performance AS
SELECT
    f.campaign_id,
    f.date,
    d.year,
    d.month,
    d.month_name,
    d.quarter,
    
    f.channel_used,
    f.company,
    f.location,
    
    dc.campaign_type,
    dc.target_audience,
    dc.customer_segment,

    f.total_clicks,
    f.total_impressions,
    f.total_cost,
    f.avg_conversion_rate,
    f.avg_roi,
    f.avg_ctr

FROM fact_campaign_performance f
LEFT JOIN dim_campaign dc 
    ON f.campaign_id = dc.campaign_id
LEFT JOIN dim_date d 
    ON f.date = d.date;

-- KPI SUMMARY VIEW (FOR QUICK DASHBOARD METRICS)


CREATE OR REPLACE TABLE vw_kpi_summary AS
SELECT
    SUM(total_clicks) AS total_clicks,
    SUM(total_impressions) AS total_impressions,
    SUM(total_cost) AS total_cost,

    -- Weighted CTR
    CASE 
        WHEN SUM(total_impressions) > 0 
        THEN SUM(total_clicks) / SUM(total_impressions)
        ELSE 0 
    END AS ctr,
    AVG(avg_roi) AS avg_roi

FROM fact_campaign_performance;

-- DAILY TREND VIEW

CREATE OR REPLACE TABLE vw_daily_trends AS
SELECT
    date,
    SUM(total_clicks) AS total_clicks,
    SUM(total_impressions) AS total_impressions,
    SUM(total_cost) AS total_cost,

    -- Weighted CTR
    CASE 
        WHEN SUM(total_impressions) > 0 
        THEN SUM(total_clicks) / SUM(total_impressions)
        ELSE 0 
    END AS ctr,

    AVG(avg_roi) AS avg_roi

FROM fact_campaign_performance
GROUP BY date
ORDER BY date;

-- CHANNEL PERFORMANCE VIEW

CREATE OR REPLACE TABLE vw_channel_performance AS
SELECT
    date,
    channel_used,
    SUM(total_clicks) AS total_clicks,
    SUM(total_impressions) AS total_impressions,

    -- Weighted CTR
    CASE 
        WHEN SUM(total_impressions) > 0 
        THEN SUM(total_clicks) / SUM(total_impressions)
        ELSE 0 
    END AS ctr,

    AVG(avg_roi) AS avg_roi

FROM fact_campaign_performance
GROUP BY date, channel_used;

-- CAMPAIGN PERFORMANCE VIEW

CREATE OR REPLACE TABLE vw_campaign_summary AS
SELECT
    campaign_id,
    SUM(total_clicks) AS total_clicks,
    SUM(total_impressions) AS total_impressions,
    SUM(total_cost) AS total_cost,

    -- Weighted CTR
    CASE 
        WHEN SUM(total_impressions) > 0 
        THEN SUM(total_clicks) / SUM(total_impressions)
        ELSE 0 
    END AS ctr,

    AVG(avg_roi) AS avg_roi

FROM fact_campaign_performance
GROUP BY campaign_id;

-- MONTHLY TRENDS VIEW

CREATE OR REPLACE TABLE vw_monthly_trends AS
SELECT
    d.year,
    d.month,

    SUM(f.total_clicks) AS total_clicks,
    SUM(f.total_impressions) AS total_impressions,

    -- Weighted CTR
    CASE 
        WHEN SUM(f.total_impressions) > 0 
        THEN SUM(f.total_clicks) / SUM(f.total_impressions)
        ELSE 0 
    END AS ctr,

    AVG(f.avg_roi) AS avg_roi

FROM fact_campaign_performance f
JOIN dim_date d 
    ON f.date = d.date
GROUP BY d.year, d.month
ORDER BY d.year, d.month;