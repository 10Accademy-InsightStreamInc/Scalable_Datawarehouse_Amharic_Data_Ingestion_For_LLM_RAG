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
    assert 'news_cleaning_pipeline' in dagbag.dags, "DAG 'news_cleaning_pipeline' not found"

def test_data_cleaning_dag_structure(dagbag):
    dag_id = 'news_cleaning_pipeline'
    dag = dagbag.get_dag(dag_id)
    assert dag is not None, f"DAG '{dag_id}' not found"
    
    # Define expected task ids
    expected_task_ids = ['fetch_scraped_data_task', 'clean_data_task', 'save_to_cleaned_db_task']

    # Check if all expected tasks are present in the DAG
    for task_id in expected_task_ids:
        assert dag.has_task(task_id), f"Task '{task_id}' not found in DAG '{dag_id}'"

    # Check task dependencies
    fetch_scraped_data_task = dag.get_task('fetch_scraped_data_task')
    clean_data_task = dag.get_task('clean_data_task')
    save_to_cleaned_db_task = dag.get_task('save_to_cleaned_db_task')

    assert clean_data_task.upstream_list == [fetch_scraped_data_task], \
        "'clean_data_task' should depend on 'fetch_scraped_data_task'"
    assert save_to_cleaned_db_task.upstream_list == [clean_data_task], \
        "'save_to_cleaned_db_task' should depend on 'clean_data_task'"

def test_task_properties(dagbag):
    dag_id = 'news_cleaning_pipeline'
    dag = dagbag.get_dag(dag_id)
    
    fetch_scraped_data_task = dag.get_task('fetch_scraped_data_task')
    clean_data_task = dag.get_task('clean_data_task')
    save_to_cleaned_db_task = dag.get_task('save_to_cleaned_db_task')

    # Check task properties
    assert fetch_scraped_data_task.retries == 1, "'fetch_scraped_data_task' retries should be 1"
    assert fetch_scraped_data_task.retry_delay == timedelta(minutes=5), \
        "'fetch_scraped_data_task' retry delay should be 5 minutes"

    assert clean_data_task.retries == 1, "'clean_data_task' retries should be 1"
    assert clean_data_task.retry_delay == timedelta(minutes=5), \
        "'clean_data_task' retry delay should be 5 minutes"

    assert save_to_cleaned_db_task.retries == 1, "'save_to_cleaned_db_task' retries should be 1"
    assert save_to_cleaned_db_task.retry_delay == timedelta(minutes=5), \
        "'save_to_cleaned_db_task' retry delay should be 5 minutes"
