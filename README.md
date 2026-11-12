# Cloud Data Warehouse POC

A two-row CSV fixture and separate loader examples for Redshift and Snowflake.
Use the offline check first to verify that Python can read the fixture and
parse its integer and floating-point columns.

```bash
python scripts/sample_data.py
```

Expected output is `Validated 2 sample rows`. This check uses the Python
standard library.

## Warehouse loaders

Install the connector dependencies with `python -m pip install -r requirements.txt`.
Copy `scripts/configs.yaml` outside the checkout and fill in the destination
warehouse settings there.
Run the corresponding loader from the repository root:

```bash
python scripts/load_to_redshift.py --config /path/to/local-config.yaml
python scripts/load_to_snowflake.py --config /path/to/local-config.yaml
```

Both examples write to a table named `sample_data`. The Redshift example
inserts the small fixture directly, so each run appends rows. The Snowflake
example uploads the CSV to the table stage and skips the CSV header.
