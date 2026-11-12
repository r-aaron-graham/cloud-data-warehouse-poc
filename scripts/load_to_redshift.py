from contextlib import closing
from pathlib import Path

import psycopg2
import yaml

if __package__:
    from .sample_data import CONFIG_FILE, read_sample
else:
    from sample_data import CONFIG_FILE, read_sample


def load_redshift(config_path=CONFIG_FILE):
    cfg = yaml.safe_load(Path(config_path).read_text(encoding="utf-8"))["redshift"]
    rows = read_sample()
    with closing(psycopg2.connect(
        dbname=cfg["dbname"], host=cfg["host"], port=cfg["port"],
        user=cfg["user"], password=cfg["password"],
    )) as conn, conn, conn.cursor() as cursor:
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS sample_data "
            "(col1 VARCHAR, col2 INTEGER, col3 REAL)"
        )
        cursor.executemany(
            "INSERT INTO sample_data (col1, col2, col3) VALUES (%s, %s, %s)",
            rows,
        )
    print(f"Inserted {len(rows)} sample rows into Redshift.")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Load the bundled CSV into redshift.")
    parser.add_argument("--config", type=Path, default=CONFIG_FILE)
    load_redshift(parser.parse_args().config)
