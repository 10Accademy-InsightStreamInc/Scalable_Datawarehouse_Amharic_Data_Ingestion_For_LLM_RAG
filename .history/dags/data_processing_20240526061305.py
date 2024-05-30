from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from airflow.models import Variable
from api.controllers.data_controller import create_data, get_news
from scripts.clean_data import DataCleaner
from airflow.utils.dates import days_ago
import logging

# Set default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Function to fetch data from the database (assuming it's implemented elsewhere)
def get_data():
    pass

# Function to save cleaned data to the database (assuming it's implemented elsewhere)
def save_cleaned_data(df):
    pass

def scrape_news_from_api(**kwargs):
    logging.info("Starting scraping news from API")
    news_api_url = Variable.get("news_api_url")  # Assuming this variable holds the URL to fetch news from
    news_data = get_news(news_api_url)
    logging.info(f"Fetched {len(news_data)} articles from API")
    kwargs['ti'].xcom_push(key='news_data', value=news_data)

def clean_data(**kwargs):
    cleaner = DataCleaner()
    news_data = kwargs['ti'].xcom_pull(task_ids='scrape_news_task', key='news_data')
    if not news_data:
        logging.error("No news data found in XCom")
        return

    cleaned_data = []
    for record in news_data:
        cleaned_record = {
            'id': record['id'],
            'cleaned_content': cleaner.normalize_char_level_missmatch(record['content']),
            'cleaned_content_no_punc': cleaner.remove_punc_and_special_chars(record['content']),
            'cleaned_content_no_ascii': cleaner.remove_ascii_and_numbers(record['content']),
            'cleaned_content_no_extra_space': cleaner.remove_newline_and_extra_space(record['content']),
            'cleaned_time_published': cleaner.convert_to_datetime(record['time_published']),
            # Add more cleaning steps here as needed
        }
        cleaned_data.append(cleaned_record)
    
    kwargs['ti'].xcom_push(key='cleaned_data', value=cleaned_data)

def save_to_database(**kwargs):
    cleaned_data = kwargs['ti'].xcom_pull(task_ids='clean_data_task', key='cleaned_data')
    if not cleaned_data:
        logging.error("No cleaned data found in XCom")
        return

    for record in cleaned_data:
        try:
            save_cleaned_data(record)  # Assuming save_cleaned_data function saves data using API
        except Exception as e:
            logging.error(f"Error saving cleaned data to database: {e}")

# Define the DAG
with DAG('news_pipeline', default_args=default_args, schedule_interval='@daily', catchup=False) as dag:
    scrape_news_task = PythonOperator(
        task_id='scrape_news_task',
        python_callable=scrape_news_from_api,
        provide_context=True,
    )

    clean_data_task = PythonOperator(
        task_id='clean_data_task',
        python_callable=clean_data,
        provide_context=True,
    )

    save_to_db_task = PythonOperator(
        task_id='save_to_db_task',
        python_callable=save_to_database,
        provide_context=True,
    )

    # Define task dependencies
    scrape_news_task >> clean_data_task >> save_to_db_task
