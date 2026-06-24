# Retail Streaming Lakehouse

An end-to-end real-time retail analytics platform built on Azure Databricks and Apache Kafka (Redpanda), demonstrating modern data engineering practices including streaming pipelines, data quality, Unity Catalog governance, and CI/CD automation.

---

## Architecture

```text
Python Producer (Faker)
→ Redpanda (Kafka-compatible)
→ Lakeflow Spark Declarative Pipelines
   ├── Bronze  — raw events from Kafka
   ├── Silver  — cleaned, typed, data quality expectations
   └── Gold    — aggregated business metrics
→ Unity Catalog (RLS + Column Masking)
→ Declarative Automation Bundles (DABs)
→ GitHub Actions CI/CD
```

---

## Tech Stack

| Layer | Technology |
|--------|------------|
| Message Broker | Redpanda (Kafka-compatible) |
| Stream Processing | Lakeflow Spark Declarative Pipelines (SDP) |
| Storage | Delta Lake on Azure ADLS Gen2 |
| Governance | Unity Catalog — Row-Level Security, Column Masking |
| Orchestration | Lakeflow Jobs |
| CI/CD | Declarative Automation Bundles + GitHub Actions |
| Platform | Azure Databricks |

---

## Project Structure

```text
retail-streaming-lakehouse/
├── producer/
│   ├── generate_events.py
│   └── send_to_redpanda.py
├── pipeline/
│   ├── bronze.py
│   ├── silver.py
│   └── gold.py
├── governance/
│   └── uc_setup.sql
├── bundle/
│   └── databricks.yml
├── .github/
│   └── workflows/
│       └── deploy.yml
└── requirements.txt
```

---

## Data Pipeline

### Bronze

- Reads raw JSON events from Redpanda `retail-orders` topic via Kafka connector
- Stores raw payload with Kafka metadata (offset, timestamp)
- No transformations — preserves source fidelity

### Silver

- Reads from Bronze as a stream
- Applies type casting, timestamp parsing, status normalization

#### Data Quality Expectations

- `valid_order_id` — order_id must not be null
- `valid_customer_id` — customer_id must not be null
- `valid_total_amount` — total_amount must be greater than 0
- `valid_quantity` — quantity must be between 1 and 100
- `valid_order_status` — must be PLACED, CONFIRMED, or CANCELLED (drops invalid records)
- `valid_product_id` — must not be null (fails pipeline if violated)

### Gold

- `gold_sales_by_store` — revenue and order metrics per store per hour
- `gold_sales_by_category` — revenue breakdown by product category per hour
- `gold_payment_method_summary` — payment method distribution per hour
- Revenue calculations include only CONFIRMED orders

---

## Unity Catalog Governance

- Row-Level Security (RLS) — store managers can access only their store's data
- Column Masking — customer email and phone fields masked for non-admin users
- Separate `dev` and `prod` schemas with identical governance policies

---

## CI/CD

- Databricks resources defined as code using Declarative Automation Bundles
- GitHub Actions executes `databricks bundle deploy`
- `dev` target deploys from feature branches
- `prod` target deploys when changes are merged into `main`

---

## Local Setup

### Clone Repository

```bash
git clone https://github.com/rajitnair9/retail-streaming-lakehouse.git
cd retail-streaming-lakehouse
python -m pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file:

```env
REDPANDA_PASSWORD=your_password_here
```

### Run Producer

```bash
cd producer
python send_to_redpanda.py
```

---

## Status

| Component | Status |
|------------|--------|
| Producer | ✅ Complete |
| Bronze Pipeline | ✅ Complete |
| Silver Pipeline | ✅ Complete |
| Gold Pipeline | ✅ Complete |
| Unity Catalog Governance | ✅ Complete |
| DABs Config | 🔲 Pending Databricks Workspace |
| GitHub Actions | 🔲 Pending Databricks Workspace |
| End-to-End Deployment | 🔲 Pending Azure Setup |

---

## Key Features

- Real-time retail event streaming using Redpanda
- Medallion Architecture (Bronze → Silver → Gold)
- Lakeflow Spark Declarative Pipelines
- Data Quality Expectations and Validation
- Delta Lake Storage
- Unity Catalog Governance
- Row-Level Security (RLS)
- Column Masking
- Infrastructure as Code with DABs
- Automated CI/CD with GitHub Actions
- Azure Databricks Native Implementation