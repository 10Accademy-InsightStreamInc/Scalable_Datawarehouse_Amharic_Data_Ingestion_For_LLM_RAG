from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from airflow.models import Variable
from api.controllers.data_controller import create_data, get_news
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

def scrape_news_from_api(**kwargs):
    logging.info("Starting scraping news from API")
    try:
        news_api_url = Variable.get("news_api_url")  # Assuming this variable holds the URL to fetch news from
        news_data = get_news(news_api_url)
        logging.info(f"Fetched {len(news_data)} articles from API")
        kwargs['ti'].xcom_push(key='news_data', value=news_data)
    except Exception as e:
        logging.error(f"Error in scraping news from API: {e}")
        raise

def save_to_database(**kwargs):
    ti = kwargs['ti']
    news_data = ti.xcom_pull(task_ids='scrape_news_task', key='news_data')
    if not news_data:
        logging.error("No news data found in XCom")
        return

    for article in news_data:
        try:
            create_data(article)  # Assuming create_data function inserts data using API
            logging.info(f"Article saved to database: {article['title']}")
        except Exception as e:
            logging.error(f"Error saving article to database: {e}")

# Define the DAG
with DAG('news_pipeline', default_args=default_args, schedule_interval='@daily', catchup=False) as dag:
    scrape_task = PythonOperator(
        task_id='scrape_news_task',
        python_callable=scrape_news_from_api,
        provide_context=True,
    )

    save_to_db_task = PythonOperator(
        task_id='save_to_db_task',
        python_callable=save_to_database,
        provide_context=True,
    )

    scrape_task >> save_to_db_task



