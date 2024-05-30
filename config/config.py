import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')

AIRFLOW_CONFIG = {
    'start_date': '2023-01-01',
    'schedule_interval': '@daily',
    'dag_id': 'data_pipeline',
}

DATABASE_CONFIG = {
    #'host': 'localhost',
    #'port': 5432,
    #'user': 'user',
    #'password': 'password',
    #'database': 'database',
}
