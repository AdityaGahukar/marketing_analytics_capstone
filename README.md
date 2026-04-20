# AdCentre — Marketing Analytics Data Engineering Pipeline

> **Organisation:** AdCentre | **Team:** Data Engineering  
> **Stack:** AWS S3 · FastAPI · Apache Airflow · Databricks · Delta Lake · Snowflake · OpenRouter LLM · Streamlit

---

## Team

| ID | Name |
|---|---|
| TSV780 | Aditya Rajesh Gahukar |
| TSV859 | Aditya Sah |
| TSV771 | Anshu |
| TSV781 | Arnav Gupta |

**Programme:** AWS Batch 1 — Capstone Project, Team 1

---

## Overview

AdCentre manages digital ad campaigns across **Facebook, Instagram, YouTube, and Google Ads**. Raw data from these platforms arrives in inconsistent formats — different date styles, cost units, column names — making reliable analysis impossible.

This pipeline ingests, cleans, validates, and organises that data into a structured warehouse, and exposes it through an AI chatbot for non-technical users.

**KPIs tracked:** Total Impressions · Total Clicks · CTR (Clicks ÷ Impressions) · Conversion Rate · ROI

---

## Architecture

```
Data Sources (Facebook · Instagram · YouTube · Google Ads)
         │
    FastAPI Backend  ──→  Airflow DAG 1 (incremental ingest)
         │
    AWS S3 — Raw Zone  (s3://marketing-analytics-capstone/raw/)
         │
    Airflow DAG 2 (orchestration)
         │
    ┌────▼────┐    ┌────────▼────────┐    ┌────▼────┐
    │ BRONZE  │───▶│     SILVER      │───▶│  GOLD   │
    │AutoLoader│   │ Clean · DQ Flag │    │Star Schema│
    └─────────┘   └─────────────────┘    └────┬────┘
                                              │
                             ┌────────────────┼─────────────────┐
                             │                                   │
                     S3 Gold Export                        AI Chatbot
                             │                             (InsyteAI)
                        Snowflake
                             │
                      BI Dashboards
```

---

## Repository Structure

```
marketing_analytics_capstone/
│
├── .github/workflows/deploy.yml       # CI/CD — auto deploy Airflow to EC2 on push
│
├── airflow/
│   ├── dags/
│   │   ├── dag1.py                    # Incremental API → S3 ingestion
│   │   ├── dag2.py                    # ETL orchestration: Bronze → Silver → Gold → Snowflake
│   │   └── sql/snowflake_transformations.sql
│   └── include/
│       ├── api_client.py              # HTTP client with retry logic
│       ├── config.py                  # Env variable config
│       ├── offset_manager.py          # Offset state tracking in S3
│       └── s3_utils.py                # S3 upload helpers
│
├── backend/
│   └── main.py                        # FastAPI — reads S3 CSVs, serves paginated batches
│
├── notebooks/
│   ├── bronze_layer.ipynb             # AutoLoader → Bronze Delta table
│   ├── silver_layer.ipynb             # Clean, cast, dedup, DQ flag → Silver Delta table
│   ├── Silver_dataquality_version2.ipynb  # Silver DQ checks + quarantine
│   ├── gold_layer.ipynb               # Star schema dim/fact/KPI → Gold Delta
│   ├── data_quality_check_gold_layer.ipynb  # Gold DQ checks + thresholds
│   ├── exportData_to_S3.ipynb         # Export Gold to S3 as Parquet
│   └── data_profiler.ipynb            # Data profiling utility
│
├── chatbot/
│   ├── backend/
│   │   ├── main.py                    # FastAPI /chat endpoint
│   │   ├── llm.py                     # OpenRouter LLM → SQL generation
│   │   ├── knowledgebase.py           # Data dictionary + business rules + query patterns
│   │   ├── snowflake_conn.py          # Snowflake query execution
│   │   └── validator.py               # SQL safety validator
│   └── frontend/
│       └── app.py                     # Streamlit UI — InsyteAI
│
└── snowflake/
    └── setup.sql                      # One-time setup: DB, schema, warehouse, tables, views
```

---

## Pipeline Stages

### Bronze
- Reads raw JSON from S3 using **Databricks AutoLoader** (`cloudFiles`)
- Adds metadata: `ingestion_timestamp`, `batch_id`, `source_file_name`, `source_month`
- Writes to Delta table partitioned by `source_month`
- No transformations — exact copy of source data

### Silver
Applies six transformation stages:
1. Column renaming → `snake_case` standard
2. Defensive type casting — strips `$`, `,`, handles nulls safely
3. Categorical standardisation — `lower(trim(col))`
4. CTR derived column — `clicks / impressions`
5. **5 DQ flag columns** per row — `dq_valid_cost`, `dq_valid_date`, `dq_valid_impressions`, `dq_valid_clicks`, `dq_valid_conversion_rate`
6. Delta MERGE on `(campaign_id, date)` — prevents duplicates on re-runs

### Silver DQ Check
- Records where `dq_pass = false` → written to Quarantine table with `dq_failure_reason`
- If failure rate > **5%** → pipeline raises exception, downstream stops

### Gold
Reads only `dq_pass = true` records and builds a **Star Schema**:

**Dimension tables:** `dim_campaign` · `dim_channel` · `dim_date` · `dim_location` · `dim_company`

**Fact table:** `fact_campaign_performance` — one row per (campaign_id, date) with total_clicks, total_impressions, total_cost, avg_ctr, avg_roi

**KPI tables (pre-aggregated):** `kpi_daily_campaign_performance` · `kpi_channel_performance` · `kpi_campaign_summary` · `kpi_monthly_trends`

### Gold DQ Check
Six rules checked on the Fact table:

| # | Rule |
|---|---|
| 1 | No negative values (clicks, impressions, cost) |
| 2 | CTR between 0 and 1 |
| 3 | Clicks ≤ Impressions |
| 4 | KPI totals match Silver (no data loss in aggregation) |
| 5 | Referential integrity — every campaign_id exists in dim_campaign |
| 6 | No missing dates |

**Thresholds:** `MAX_TOTAL_ISSUES = 10` · `MAX_CRITICAL_ISSUES = 1`  
On breach → exception raised, Airflow fails the task, Snowflake load does not run.

### Snowflake Load
Gold Parquet files exported to `s3://marketing-analytics-capstone/gold/` then loaded via `COPY INTO`:
```sql
TRUNCATE TABLE fact_campaign_performance;
COPY INTO fact_campaign_performance
FROM @marketing_stage/fact_campaign_performance/
FILE_FORMAT = (TYPE = PARQUET)
MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE;
```

Six analytical views created post-load: `vw_campaign_performance` · `vw_kpi_summary` · `vw_daily_trends` · `vw_channel_performance` · `vw_campaign_summary` · `vw_monthly_trends`

---

## AI Chatbot — InsyteAI

Natural language → SQL interface on top of the Snowflake Gold layer.

```
User question → LLM (OpenRouter) → SQL → Validator → Snowflake → Table + Chart
```

- **LLM:** OpenRouter (`elephant-alpha` / `gemini-2.0-flash`), temperature 0
- **Knowledge base:** Full data dictionary, business rules, and 6 query pattern examples injected into system prompt
- **Validator:** Allows SELECT only · requires LIMIT · blocks DROP/DELETE/INSERT/ALTER
- **Frontend:** Streamlit — renders results as interactive table + line/bar chart

---

## Orchestration & CI/CD

**Airflow DAG 2 task order:**
```
run_bronze → run_silver → run_silver_dq → run_gold → run_gold_dq → snowflake_step
```

**GitHub Actions** (`deploy.yml`): Any push to `main` that changes `airflow/**` automatically SSHes into EC2 and runs `git pull && astro dev restart`.

---

## Environment Variables

**Backend** (`backend/.env`)
```
AWS_ACCESS_KEY, AWS_SECRET_KEY, AWS_REGION
S3_BUCKET=marketing-analytics-capstone
S3_FILE_KEY=raw/
BATCH_SIZE=100
```

**Airflow** (Astro connections)
```
API_URL=http://<ec2-ip>:8000
S3_BUCKET=marketing-analytics-capstone
Connections: databricks_default, snowflake_default
```

**Chatbot** (`chatbot/backend/.env`)
```
OPENROUTER_API_KEY
SNOWFLAKE_ACCOUNT, SNOWFLAKE_USER, SNOWFLAKE_PASSWORD
SNOWFLAKE_DATABASE=MARKETING_ANALYTICS
SNOWFLAKE_SCHEMA=GOLD
SNOWFLAKE_WAREHOUSE=COMPUTE_WH
```

---

## How to Run

**1. FastAPI Backend**
```bash
cd backend && pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

**2. Airflow**
```bash
cd airflow && astro dev start
# UI → http://localhost:8080
# Add databricks_default and snowflake_default connections
```

**3. Databricks Notebooks**  
Upload `notebooks/` to your workspace. Update notebook paths in `dag2.py`. Trigger DAG 2 from Airflow UI.

**4. Snowflake Setup**  
Run `snowflake/setup.sql` once in a Snowflake worksheet.

**5. AI Chatbot**
```bash
cd chatbot/backend && uvicorn main:app --reload --port 8000
cd chatbot/frontend && streamlit run app.py
# UI → http://localhost:8501
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| Raw Storage | AWS S3 |
| Data Serving | FastAPI + Uvicorn on AWS EC2 |
| Orchestration | Apache Airflow 2.x (Astronomer) |
| Processing | Databricks + PySpark |
| Table Format | Delta Lake (Unity Catalog) |
| Warehouse | Snowflake (GOLD schema, XSMALL warehouse) |
| CI/CD | GitHub Actions |
| Chatbot Backend | FastAPI + OpenRouter LLM |
| Chatbot Frontend | Streamlit |
| Language | Python 3.9+ |
