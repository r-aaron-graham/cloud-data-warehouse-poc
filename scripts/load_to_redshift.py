import yaml
import psycopg2

def load_redshift(config_path='scripts/configs.yaml'):
    cfg = yaml.safe_load(open(config_path))['redshift']
    data_file = '../data/sample.csv'

    conn = psycopg2.connect(
        dbname=cfg['dbname'], host=cfg['host'],
        port=cfg['port'], user=cfg['user'], password=cfg['password']
    )
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS sample_data (
            col1 VARCHAR,
            col2 INTEGER,
            col3 REAL
        );
        """
    )
    conn.commit()

    with open(data_file, 'r') as f:
        cur.copy_expert("COPY sample_data FROM STDIN CSV HEADER", f)
    conn.commit()
    cur.close()
    conn.close()
    print('Data loaded into Redshift successfully.')

if __name__ == '__main__':
    load_redshift()
