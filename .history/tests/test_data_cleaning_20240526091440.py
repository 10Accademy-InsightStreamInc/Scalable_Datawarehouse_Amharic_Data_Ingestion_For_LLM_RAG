import os
import pytest
from airflow.models import DagBag
from airflow.utils.dates import days_ago

# Define the path to your DAG file
DAGS_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'dags')

@pytest.fixture(scope='module')
def dagbag():
    return DagBag(dag_folder=DAGS_FOLDER, include_examples=False)

def test_dag_loaded_successfully(dagbag):
    assert len(dagbag.dags) == 1, "Expected one DAG to be loaded"

def test_data_cleaning_dag_structure(dagbag):
    dag_id = 'data_cleaning'
    dag = dagbag.get_dag(dag_id)
    assert dag is not None, f"DAG '{dag_id}' not found"
    
    # Define expected task ids
    expected_task_ids = ['fetch_scraped_data_task', 'clean_data_task', 'save_to_cleaned_db_task']

    # Check if all expected tasks are present in the DAG
    for task_id in expected_task_ids:
        assert dag.has_task(task_id), f"Task '{task_id}' not found in DAG '{dag_id}'"
