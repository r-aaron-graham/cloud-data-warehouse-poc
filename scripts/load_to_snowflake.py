import yaml
import snowflake.connector

def load_snowflake(config_path='scripts/configs.yaml'):
    cfg = yaml.safe_load(open(config_path))['snowflake']
    data_file = '../data/sample.csv'

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
        cs.execute(f"PUT file://{data_file} @%sample_data AUTO_COMPRESS=TRUE")
        cs.execute(
            """
            COPY INTO sample_data
            FROM @%sample_data
            FILE_FORMAT = (TYPE = 'CSV' FIELD_OPTIONALLY_ENCLOSED_BY='"')
            """
        )
        print('Data loaded into Snowflake successfully.')
    finally:
        cs.close()
        ctx.close()

if __name__ == '__main__':
    load_snowflake()
