# Cloud Data Warehouse POC

## Overview
This proof-of-concept demonstrates loading a CSV file into AWS Redshift or Snowflake using Python. It includes:
- Schema creation and data load for Redshift
- Schema creation and data load for Snowflake

## Prerequisites
- Python 3.8+
- AWS credentials with Redshift access (or Snowflake account credentials)
- `psycopg2` for Redshift or `snowflake-connector-python` for Snowflake

## Setup
1. Create a Python virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
