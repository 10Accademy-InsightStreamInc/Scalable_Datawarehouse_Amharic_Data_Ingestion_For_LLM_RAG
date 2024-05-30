import unittest
from airflow.models import DagBag, TaskInstance
from airflow.utils import timezone
from unittest.mock import patch, MagicMock
from airflow.dags.data_pipeline import save_to_database, scrape_news
from airflow.utils.dag_cycle_tester import test_cycle


class TestDAG(unittest.TestCase):
    def setUp(self):
        self.dagbag = DagBag(include_examples=False)

    def test_dag_loaded_successfully(self):
        self.assertTrue('news_pipeline' in self.dagbag.dags)
    
    def test_no_cyclic_dependencies(self):
        for dag_id, dag in self.dagbag.dags.items():
            self.assertFalse(test_cycle(dag))

    def test_number_of_tasks(self):
        expected_task_count = 2  # Adjust this based on your DAG definition
        for dag_id, dag in self.dagbag.dags.items():
            self.assertEqual(len(dag.tasks), expected_task_count)

    def test_task_dependencies(self):
        for dag_id, dag in self.dagbag.dags.items():
            for task in dag.tasks:
                for upstream_task_id in task.upstream_task_ids:
                    self.assertIn(upstream_task_id, dag.task_dict)
                for downstream_task_id in task.downstream_task_ids:
                    self.assertIn(downstream_task_id, dag.task_dict)

class TestIntegration(unittest.TestCase):
    @patch('airflow.dags.data_pipeline.save_to_database')
    @patch('airflow.dags.data_pipeline.scrape_news')
    def test_data_ingested_into_database(self, mock_scrape_news, mock_save_to_database):
        # Define the mocked data returned by scrape_news
        mocked_news_data = [{'title': 'Mocked Title', 'content': 'Mocked Content'}]

        # Set up the mock return value for scrape_news
        mock_scrape_news.return_value = mocked_news_data

        # Mock the task instance to return a known set of XCom data
        dagbag = DagBag(include_examples=False)
        dag = dagbag.get_dag('news_pipeline')
        ti = TaskInstance(task=dag.get_task('save_to_db_task'), execution_date=timezone.utcnow())
        ti.xcom_pull = MagicMock(return_value=mocked_news_data)

        # Call the function under test
        save_to_database(news_data=ti.xcom_pull())

        # Assert that save_to_database was called with the correct data
        mock_save_to_database.assert_called_once_with(news_data=mocked_news_data)
        
class TestEndToEndPipeline(unittest.TestCase):
    @patch('airflow.dags.data_pipeline.save_to_database')
    @patch('airflow.dags.data_pipeline.scrape_news')
    def test_end_to_end_pipeline(self, mock_scrape_news, mock_save_to_database):
        # Mocking the data passed between tasks for testing purposes
        # Define mocked news data that would be returned by scrape_news
        mocked_news_data = [{'title': 'Mocked Title', 'content': 'Mocked Content'}]

        # Set up the mock return value for scrape_news
        mock_scrape_news.return_value = mocked_news_data

        # Execute the DAG tasks
        dagbag = DagBag(include_examples=False)
        dag = dagbag.get_dag('news_pipeline')

        # Create task instances
        scrape_task_instance = TaskInstance(task=dag.get_task('scrape_news_task'), execution_date=timezone.utcnow())
        save_to_db_task_instance = TaskInstance(task=dag.get_task('save_to_db_task'), execution_date=timezone.utcnow())

        # Run the task instances
        scrape_task_instance.run(ignore_ti_state=True)
        save_to_db_task_instance.run(ignore_ti_state=True)

        # Assert that save_to_database was called with the correct data
        mock_save_to_database.assert_called_once_with(news_data=mocked_news_data)


if __name__ == '__main__':
    unittest.main()

