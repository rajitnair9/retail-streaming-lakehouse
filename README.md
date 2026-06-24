```markdown
# Retail Streaming Lakehouse

An end-to-end real-time retail analytics platform built on Azure Databricks and Apache Kafka (Redpanda), demonstrating modern data engineering practices including streaming pipelines, data quality, Unity Catalog governance, and CI/CD automation.

---

## Architecture

```
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
|---|---|
| Message Broker | Redpanda (Kafka-compatible) |
| Stream Processing | Lakeflow Spark Declarative Pipelines (SDP) |
| Storage | Delta Lake on Azure ADLS Gen2 |
| Governance | Unity Catalog — Row-Level Security, Column Masking |
| Orchestration | Lakeflow Jobs |
| CI/CD | Declarative Automation Bundles + GitHub Actions |
| Platform | Azure Databricks |

---

## Project Structure

```
retail-streaming-lakehouse/
├── producer/
│   ├── generate_events.py      # Generates fake retail order events
│   └── send_to_redpanda.py     # Publishes events to Redpanda topic
├── pipeline/
│   ├── bronze.py               # Raw ingestion from Kafka
│   ├── silver.py               # Cleaning + data quality expectations
│   └── gold.py                 # Business aggregations
├── governance/
│   └── uc_setup.sql            # Unity Catalog DDL, RLS, column masking
├── bundle/
│   └── databricks.yml          # DABs config - dev + prod targets
├── .github/
│   └── workflows/
│       └── deploy.yml          # GitHub Actions CI/CD pipeline
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
- **Data quality expectations:**
  - `valid_order_id` — order_id must not be null
  - `valid_customer_id` — customer_id must not be null
  - `valid_total_amount` — total_amount must be > 0
  - `valid_quantity` — quantity must be between 1 and 100
  - `valid_order_status` — must be PLACED, CONFIRMED, or CANCELLED (drops invalid)
  - `valid_product_id` — must not be null (fails pipeline if violated)

### Gold
- `gold_sales_by_store` — revenue and order metrics per store per hour
- `gold_sales_by_category` — revenue breakdown by product category per hour
- `gold_payment_method_summary` — UPI vs Cash vs Card breakdown per hour
- Filters only CONFIRMED orders for revenue calculations

---

## Unity Catalog Governance

- **Row-Level Security** — store managers see only their store's data, admins see all
- **Column Masking** — `customer_email` and `customer_phone` masked for non-admin users
- Separate `dev` and `prod` schemas with identical governance policies

---

## CI/CD

- All Databricks resources defined as code in `bundle/databricks.yml`
- GitHub Actions triggers `databricks bundle deploy` on push to `main`
- `dev` target deploys on feature branch push
- `prod` target deploys on merge to `main`

---

## Local Setup

```bash
git clone https://github.com/rajitnair9/retail-streaming-lakehouse.git
cd retail-streaming-lakehouse
python -m pip install -r requirements.txt
```

Create `.env` file in root:
```
REDPANDA_PASSWORD=your_password_here
```

Run the producer:
```bash
cd producer
python send_to_redpanda.py
```

---

## Status

| Component | Status |
|---|---|
| Producer | ✅ Complete |
| Bronze Pipeline | ✅ Complete |
| Silver Pipeline | ✅ Complete |
| Gold Pipeline | ✅ Complete |
| Unity Catalog Governance | ✅ Complete |
| DABs Config | 🔲 Pending Databricks workspace |
| GitHub Actions | 🔲 Pending Databricks workspace |
| End-to-end deployment | 🔲 Pending Azure setup |
```