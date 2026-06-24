# Retail Streaming Lakehouse

A real-time retail analytics platform built on Azure Databricks and Redpanda (Kafka-compatible), showcasing modern data engineering capabilities including streaming ingestion, Medallion Architecture, data quality enforcement, Unity Catalog governance, and automated CI/CD deployment.

---

## Architecture

```text
Python Producer (Faker)
        │
        ▼
Redpanda (Kafka-Compatible Broker)
        │
        ▼
Lakeflow Spark Declarative Pipelines
   ├── Bronze  — Raw event ingestion
   ├── Silver  — Data cleansing, standardization, and quality enforcement
   └── Gold    — Business-ready aggregations and KPIs
        │
        ▼
Unity Catalog
   ├── Row-Level Security (RLS)
   └── Column Masking
        │
        ▼
Databricks Asset Bundles (DABs)
        │
        ▼
GitHub Actions CI/CD
```

---

## Overview

This project simulates a production-grade retail streaming platform that ingests order events in real time, processes them through a Medallion Architecture, enforces data quality rules using Lakeflow expectations, and secures access through Unity Catalog governance.

Key capabilities include:

* Real-time event ingestion using Redpanda
* Streaming transformations with Lakeflow Spark Declarative Pipelines
* Bronze, Silver, and Gold Delta Lake layers
* Data Quality Expectations and pipeline enforcement
* Unity Catalog Row-Level Security and Column Masking
* Environment promotion using Databricks Asset Bundles
* Automated CI/CD deployment with GitHub Actions

---

## Environment Strategy

Two isolated catalogs are maintained within a single Databricks workspace to simulate enterprise environment separation:

| Environment | Catalog                 | Access                                      |
| ----------- | ----------------------- | ------------------------------------------- |
| Development | `dev_retail_lakehouse`  | Engineers – Read/Write                      |
| Production  | `prod_retail_lakehouse` | Engineers – Read Only, Analysts – Read Only |

> In a typical enterprise deployment, Development and Production environments would reside in separate Databricks workspaces with dedicated Unity Catalog metastores.
