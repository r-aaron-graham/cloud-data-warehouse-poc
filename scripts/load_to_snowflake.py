from pathlib import Path

import yaml
import snowflake.connector

if __package__:
    from .sample_data import CONFIG_FILE, DATA_FILE
else:
    from sample_data import CONFIG_FILE, DATA_FILE


def load_snowflake(config_path=CONFIG_FILE):
    cfg = yaml.safe_load(Path(config_path).read_text(encoding='utf-8'))['snowflake']

    ctx = snowflake.connector.connect(
        account=cfg['account'], user=cfg['user'],
        password=cfg['password'], warehouse=cfg['warehouse'],
        database=cfg['database'], schema=cfg['schema']
    )
    cs = ctx.cursor()
    try:
        cs.execute(
            """
            CREATE TABLE IF NOT EXISTS sample_data (
                col1 VARCHAR,
                col2 INTEGER,
                col3 FLOAT
            );
            """
        )
        cs.execute(f"PUT '{DATA_FILE.as_uri()}' @%sample_data AUTO_COMPRESS=TRUE")
        cs.execute(
            """
            COPY INTO sample_data
            FROM @%sample_data
            FILE_FORMAT = (TYPE = 'CSV' SKIP_HEADER = 1 FIELD_OPTIONALLY_ENCLOSED_BY='"')
            """
        )
        print('Data loaded into Snowflake successfully.')
    finally:
        cs.close()
        ctx.close()

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Load the bundled CSV into snowflake.")
    parser.add_argument("--config", type=Path, default=CONFIG_FILE)
    load_snowflake(parser.parse_args().config)
