# 🧱 Data Ingestion & ETL Subsystem Framework

A modular, configuration-driven Python ingestion framework architected to pull raw, messy transactional datasets from local flat files (CSV) and public REST web APIs (Jikan Manga API), apply strict data validation rules, and bulk load normalized records into a relational PostgreSQL staging database layer.

## 🧭 System Architecture & Data Flow

```text
       Source Layer (CSV / REST API)
                       ↓
       Reader Layer (pandas / requests)
                       ↓
       Validation Gatekeeper (validate.py)
         /                                \
   (If Valid)                         (If Invalid)
       /                                    \
      ↓                                      ↓
Cleaner Layer (clean.py)           Database Load Engine (load.py)
      ↓                                      ↓
PostgreSQL Staging Upsert            stg_rejects Table (JSONB)
(stg_customers / stg_manga)
```

## 🧩 Key Architectural Features
Dynamic, Configuration-Driven Schema Mapping: Pipeline targets, paths, primary keys, and source parameters are loaded at runtime via config/sources.yml. Adding completely new pipelines does not require rewriting core application files.

Idempotent Ingestion Loops: Destructive data duplicates or tracking collisions are entirely prevented using bulk batch database updates backed by ON CONFLICT DO UPDATE (upsert) constraints.

Comprehensive Rejects Sandbox Logging: Broken payloads (such as records missing mandatory primary indicators or throwing casting constraints like invalid Pandas NaN types) are safely isolated from terminating the application execution. They are automatically routed into a unified database audit table (stg_rejects) as native binary JSONB data with specific error descriptions.

Structured Telemetry & Summary Reporting: Consolidated runtime metrics track exact processing milestones, providing real-time stdout summary tallies (total_rows, loaded, and rejected) for every source pipeline pass.

Decoupled Testing Boundaries: Business logic structures are written inside deterministic atomic utilities. This makes it possible to run unit tests using pytest instantly without spinning up local database engines or establishing real network connections.

## 📁 Repository Structural Blueprint
```text
ingestion-pipeline/
│
├── config/
│   └── sources.yml         # Global pipeline orchestrator configuration maps
│
├── data/
│   └── customers.csv       # Transactional tracking flat-file source data
│
├── src/
│   ├── readers/
│   │   ├── csv_reader.py   # Pandas-backed file extraction engine
│   │   └── api_reader.py   # Rate-limited REST API ingestion interface
│   ├── clean.py            # Reusable business logic data type normalizers
│   ├── validate.py         # True/False structural integrity validation gates
│   ├── load.py             # Database batch transactions and rejects manager
│   └── main.py             # Pipeline bootstrap executor and runtime manager
│
├── tests/
│   └── test_pipeline.py    # Automated unit monitoring testing suites
│
├── .env.example            # Layout template for local environmental secrets
├── .gitignore              # Tracking file exclusions whitelist
├── pytest.ini              # Custom test runner path configuration layout
├── requirements.txt        # Virtual environment third-party packages file
└── README.md
```
## 🚀 Installation & Local Environment Setup
1. Initialize Local Clone
Clone this source code layout from your remote GitHub instance and jump into the directory:

```bash
git clone [https://github.com/py94NJIT/ingestion-pipeline.git](https://github.com/py94NJIT/ingestion-pipeline.git)
cd ingestion-pipeline
```
2. Prepare Virtual Environment Stack
Build an isolated execution boundary on your computer and install the necessary dependencies:

```bash
python -m venv .venv
source .venv/Scripts/activate  # On Windows terminals use: .venv\Scripts\activate
pip install -r requirements.txt
```
3. Connect Environment Secrets
Copy the environment variable blueprint template and configure the variables to match your local PostgreSQL server setup:

```bash
cp .env.example .env
```
Open up your newly generated .env file and replace the values with your local connection variables:

```Ini, TOML
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=your_secure_password
DB_HOST=localhost
DB_PORT=5432
```

## ⚙️ Running the Framework
Run the Production ETL Jobs
To parse your configurations, ingest files, query the REST web API, and dump normalized logs into PostgreSQL, run:

```bash
python src/main.py
```
Example Output Runtime Telemetry:
```text
2026-06-25 00:15:01,858 - pipeline.main - INFO - ========== Initializing Configuration-Driven Pipeline Run ==========
2026-06-25 00:15:01,861 - pipeline.main - INFO - Triggering ingestion sequence: 'customers_csv'
2026-06-25 00:15:02,450 - pipeline.load - INFO - Loaded 96 rows successfully into table 'stg_customers'.
2026-06-25 00:15:02,452 - pipeline.main - INFO - Run Summary for 'customers_csv': total_rows=105 | loaded=96 | rejected=9
2026-06-25 00:15:02,452 - pipeline.main - INFO - ------------------------------------------------------------
2026-06-25 00:15:02,454 - pipeline.main - INFO - Triggering ingestion sequence: 'top_manga_api'
2026-06-25 00:15:05,210 - pipeline.readers.api - INFO - Fetching Jikan Manga API Page 1...
2026-06-25 00:15:06,844 - pipeline.load - INFO - Loaded 50 rows successfully into table 'stg_manga'.
2026-06-25 00:15:06,846 - pipeline.main - INFO - Run Summary for 'top_manga_api': total_rows=50 | loaded=50 | rejected=0
2026-06-25 00:15:06,846 - pipeline.main - INFO - ------------------------------------------------------------
2026-06-25 00:15:06,847 - pipeline.main - INFO - ========== Pipeline Operations Complete ==========
```
Run the Automated Unit Testing Suite
To verify data-type transformations and validation rule sets across your modules using pytest, execute:

```bash
pytest
```
