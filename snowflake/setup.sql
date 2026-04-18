-- Create DB, Schema, Warehouse
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


CREATE OR REPLACE TABLE kpi_daily_campaign_performance (
    date TIMESTAMP,
    total_clicks NUMBER,
    total_impressions NUMBER,
    total_cost FLOAT,
    avg_ctr FLOAT,
    avg_roi FLOAT
);

CREATE OR REPLACE TABLE kpi_channel_performance (
    date TIMESTAMP,
    channel_used STRING,
    total_clicks NUMBER,
    total_impressions NUMBER,
    avg_ctr FLOAT,
    avg_roi FLOAT
);

CREATE OR REPLACE TABLE kpi_campaign_summary (
    campaign_id NUMBER,
    total_clicks NUMBER,
    total_impressions NUMBER,
    total_cost FLOAT,
    avg_roi FLOAT
);

CREATE OR REPLACE TABLE kpi_monthly_trends (
    year NUMBER,
    month NUMBER,
    total_clicks NUMBER,
    total_impressions NUMBER,
    avg_ctr FLOAT,
    avg_roi FLOAT
);


-- LOAD DATA FROM S3
TRUNCATE TABLE fact_campaign_performance;

COPY INTO fact_campaign_performance
FROM @marketing_stage/fact_campaign_performance/
FILE_FORMAT = (TYPE = PARQUET)
MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE
PATTERN = '.*\\.parquet'
ON_ERROR = SKIP_FILE;

TRUNCATE TABLE dim_campaign;

COPY INTO dim_campaign
FROM @marketing_stage/dim_campaign/
FILE_FORMAT = (TYPE = PARQUET)
MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE
PATTERN = '.*\\.parquet'
ON_ERROR = SKIP_FILE;

TRUNCATE TABLE dim_channel;

COPY INTO dim_channel
FROM @marketing_stage/dim_channel/
FILE_FORMAT = (TYPE = PARQUET)
MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE
PATTERN = '.*\\.parquet'
ON_ERROR = SKIP_FILE;

TRUNCATE TABLE dim_company;

COPY INTO dim_company
FROM @marketing_stage/dim_company/
FILE_FORMAT = (TYPE = PARQUET)
MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE
PATTERN = '.*\\.parquet'
ON_ERROR = SKIP_FILE;

TRUNCATE TABLE dim_location;

COPY INTO dim_location
FROM @marketing_stage/dim_location/
FILE_FORMAT = (TYPE = PARQUET)
MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE
PATTERN = '.*\\.parquet'
ON_ERROR = SKIP_FILE;

TRUNCATE TABLE dim_date;

COPY INTO dim_date
FROM @marketing_stage/dim_date/
FILE_FORMAT = (TYPE = PARQUET)
MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE
PATTERN = '.*\\.parquet'
ON_ERROR = SKIP_FILE;

TRUNCATE TABLE kpi_daily_campaign_performance;

COPY INTO kpi_daily_campaign_performance
FROM @marketing_stage/kpi_daily/
FILE_FORMAT = (TYPE = PARQUET)
MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE
PATTERN = '.*\\.parquet'
ON_ERROR = SKIP_FILE;

TRUNCATE TABLE kpi_channel_performance;

COPY INTO kpi_channel_performance
FROM @marketing_stage/kpi_channel/
FILE_FORMAT = (TYPE = PARQUET)
MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE
PATTERN = '.*\\.parquet'
ON_ERROR = SKIP_FILE;

TRUNCATE TABLE kpi_campaign_summary;

COPY INTO kpi_campaign_summary
FROM @marketing_stage/kpi_campaign/
FILE_FORMAT = (TYPE = PARQUET)
MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE
PATTERN = '.*\\.parquet'
ON_ERROR = SKIP_FILE;

TRUNCATE TABLE kpi_monthly_trends;
COPY INTO kpi_monthly_trends
FROM @marketing_stage/kpi_monthly/
FILE_FORMAT = (TYPE = PARQUET)
MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE
PATTERN = '.*\\.parquet'
ON_ERROR = SKIP_FILE;


-- VALIDATE
SELECT COUNT(*) FROM fact_campaign_performance;

SELECT * FROM kpi_daily_campaign_performance LIMIT 10;

SELECT * FROM dim_campaign LIMIT 10;


-- VIEWS
-- CORE ANALYTICS VIEW
CREATE OR REPLACE VIEW vw_campaign_performance AS
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
CREATE OR REPLACE VIEW vw_kpi_summary AS
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
CREATE OR REPLACE VIEW vw_daily_trends AS
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
CREATE OR REPLACE VIEW vw_channel_performance AS
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
CREATE OR REPLACE VIEW vw_campaign_summary AS
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
CREATE OR REPLACE VIEW vw_monthly_trends AS
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
