import os
import pytest
from airflow.models import DagBag
from datetime import timedelta

# Define the path to your DAG file
DAGS_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'dags')

@pytest.fixture(scope='module')
def dagbag():
    return DagBag(dag_folder=DAGS_FOLDER, include_examples=False)

def test_dag_loaded_successfully(dagbag):
    assert len(dagbag.dags) == 1, "Expected one DAG to be loaded"
    assert 'data_collection' in dagbag.dags, "DAG 'data_collection' not found"

def test_data_collection_dag_structure(dagbag):
    dag_id = 'data_collection'
    dag = dagbag.get_dag(dag_id)
    assert dag is not None, f"DAG '{dag_id}' not found"
    
    # Define expected task ids
    expected_task_ids = ['scrape_news_task', 'save_to_db_task']

    # Check if all expected tasks are present in the DAG
    for task_id in expected_task_ids:
        assert dag.has_task(task_id), f"Task '{task_id}' not found in DAG '{dag_id}'"

    # Check task dependencies
    scrape_news_task = dag.get_task('scrape_news_task')
    save_to_db_task = dag.get_task('save_to_db_task')

    assert scrape_news_task.downstream_task_ids == {'save_to_db_task'}, \
        "'scrape_news_task' should have 'save_to_db_task' as downstream task"
    assert save_to_db_task.upstream_task_ids == {'scrape_news_task'}, \
        "'save_to_db_task' should have 'scrape_news_task' as upstream task"

def test_task_properties(dagbag):
    dag_id = 'data_collection'
    dag = dagbag.get_dag(dag_id)
    
    scrape_news_task = dag.get_task('scrape_news_task')
    save_to_db_task = dag.get_task('save_to_db_task')

    # Check task properties
    assert scrape_news_task.retries == 1, "'scrape_news_task' retries should be 1"
    assert scrape_news_task.retry_delay == timedelta(minutes=5), \
        "'scrape_news_task' retry delay should be 5 minutes"

    assert save_to_db_task.retries == 1, "'save_to_db_task' retries should be 1"
    assert save_to_db_task.retry_delay == timedelta(minutes=5), \
        "'save_to_db_task' retry delay should be 5 minutes"
