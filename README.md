# Restaurant Analytics Lakehouse on Azure Databricks

<!-- TODO: one sentence in your own words once the project works, e.g.:
An end-to-end data platform that ingests restaurant orders in real time and from an operational database,
refines them through Bronze, Silver and Gold layers, scores customer reviews with an LLM,
and serves the results in AI/BI dashboards. -->

![Architecture](docs/images/architecture.png)
<!-- TODO: add an architecture image to docs/images/ (draw.io or Excalidraw works well) -->

## Business questions this platform answers

- How are daily orders, revenue and average order value developing per restaurant?
- Which dishes sell best, and when are the peak hours?
- Who are our most valuable customers, and who hasn't ordered in 90+ days?
- What are customers complaining about: delivery, food quality, pricing or portion size?

## Tech stack

| Area | Tools |
| --- | --- |
| Sources | Azure SQL Database (batch, change tracking), Azure Event Hubs (streaming) |
| Ingestion | Lakeflow Connect (CDC), Spark Structured Streaming via the Kafka endpoint |
| Processing | Spark Declarative Pipelines (PySpark + SQL), Delta Lake |
| Governance | Unity Catalog |
| AI | `ai_query` with a Databricks-hosted foundation model |
| Orchestration | Lakeflow Jobs |
| Serving | Databricks SQL warehouse, AI/BI dashboards |
| Tooling | Python, Faker, pytest, Git/GitHub |

## Data flow

| Layer | Tables | What happens |
| --- | --- | --- |
| Bronze | `orders`, `historical_orders`, `customers`, `restaurants`, `menu_items`, `reviews` | Raw copies of source data, plus ingestion metadata |
| Silver | `fact_orders`, `fact_order_items`, `fact_reviews` | Typed and validated data, JSON items exploded to one row per dish, reviews enriched with LLM sentiment |
| Gold | `d_sales_summary`, `d_customer_360`, `d_restaurant_reviews` | Business aggregates for dashboards |

## Data quality

<!-- TODO: list your expectations and paste real numbers from the pipeline UI, e.g.
"valid_amount (total_amount > 0): 37 rows dropped out of 8,412" -->

## AI review analysis

<!-- TODO: describe your prompt, the model endpoint, how you forced valid JSON,
and how accurate it was when you checked ~20 reviews by hand. -->

## Dashboards

<!-- TODO: add screenshots to docs/images/ and link them here -->
<!-- ![Performance dashboard](docs/images/dashboard_performance.png) -->
<!-- ![Review insights dashboard](docs/images/dashboard_reviews.png) -->

## What I added beyond the tutorial

<!-- TODO: this is the most important section for recruiters. Examples:
- Unique order IDs (uuid) and pytest tests for the data generator
- `is_at_risk` flag in customer 360 (no order in 90+ days)
- Structured JSON output for the LLM step
- Job exported as code
-->

## Challenges and what I learned

<!-- TODO: be specific, e.g. vCPU quota limits on an Azure for Students subscription,
why the ingestion gateway needs classic compute, a bug you hit and how you fixed it -->

## Repository structure

```
data_generator/   Python scripts that create synthetic restaurants, customers, orders and reviews
pipelines/
  ingest/         Streaming ingestion from Event Hubs (Bronze)
  silver/         Fact tables, expectations and the AI review step
  gold/           Materialized views for dashboards
sql/              Azure SQL table definitions and change tracking setup
jobs/             Lakeflow Job definition exported as code
dashboards/       Dashboard exports
tests/            pytest tests for the data generator
docs/             Images and my learning log
```

## How to run it

1. Copy `.env.example` to `.env` and fill in your own values (never commit `.env`).
2. `python -m venv .venv`, activate it, then `pip install -r requirements.txt`.
3. Generate data: `python data_generator/generate_all.py`, then check it with `pytest`.
4. Create the Azure resources and Databricks objects as described in `sql/` and `pipelines/`.
5. Run the Lakeflow Job.

## Credits

This project is based on the
[Databricks End-To-End Project tutorial by Afaque Ahmad](https://www.youtube.com/watch?v=vy4G86q1rQY)
and its [reference code](https://github.com/afaqueahmad7117/databricks-masterclass).
I built it myself step by step; my own extensions are listed above.

## Contact

<!-- TODO: your name, LinkedIn URL -->
