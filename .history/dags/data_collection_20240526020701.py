from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from airflow.models import Variable
from db.connection.db_conn import DatabaseLoader
from models.base import Database
from sqlalchemy.orm import sessionmaker
from scrapper.news_sites.alain import AlainNewsScraper
from api.controllers.data_controller import create_data
import os
import logging

# Set default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 5, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Initialize database connection
db_loader = DatabaseLoader()
db_loader.set_connection_url_from_dbname(Variable.get("db_database"))
db_loader.connect()
SessionLocal = sessionmaker(bind=db_loader.engine)

def scrape_news(url, **kwargs):
    logging.info(f"Starting scraping news from {url}")
    scraper = AlainNewsScraper(url=url)
    news_data = scraper.get_full_news()
    logging.info(f"Scraped {len(news_data)} articles")
    # Push the result to XCom
    kwargs['ti'].xcom_push(key='news_data', value=news_data)

def save_to_database(**kwargs):
    # Pull the news data from XCom
    news_data = kwargs['ti'].xcom_pull(task_ids='scrape_news_task', key='news_data')
    if not news_data:
        logging.error("No news data found in XCom")
        return

    session = SessionLocal()
    try:
        for article in news_data:
            db_data = create_data(session, article)
            session.add(db_data)
        session.commit()
        logging.info("News data saved to database successfully")
    except Exception as e:
        session.rollback()
        logging.error(f"Error saving to database: {e}")
        raise e
    finally:
        session.close()

# Define the DAG
with DAG('news_pipeline', default_args=default_args, schedule_interval='@daily', catchup=False) as dag:
    scrape_task = PythonOperator(
        task_id='scrape_news_task',
        python_callable=scrape_news,
        op_kwargs={'url': Variable.get("news_scraper_url")},
        provide_context=True,
    )

    save_to_db_task = PythonOperator(
        task_id='save_to_db_task',
        python_callable=save_to_database,
        provide_context=True,
    )

    scrape_task >> save_to_db_task


