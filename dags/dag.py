from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
from scripts.weather_api import get_weather
from scripts.calendar_api import get_calendar
from scripts.inventory_etl import process_inventory
from scripts.database_etl import get_combinations
from scripts.recommendation_engine import make_recommendation
from scripts.statistics import calculate_statistics

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 12, 8),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'daily_clothing_recommendation',
    default_args=default_args,
    description='DAG para recomendar ropa diaria basada en el clima y eventos del calendario',
    schedule_interval='0 7 * * *',
    catchup=False,
)

weather_task = PythonOperator(
    task_id='get_weather',
    python_callable=get_weather,
    dag=dag,
)

calendar_task = PythonOperator(
    task_id='get_calendar',
    python_callable=get_calendar,
    dag=dag,
)

inventory_task = PythonOperator(
    task_id='process_inventory',
    python_callable=process_inventory,
    dag=dag,
)

combinations_task = PythonOperator(
    task_id='get_combinations',
    python_callable=get_combinations,
    dag=dag,
)

recommendation_task = PythonOperator(
    task_id='make_recommendation',
    python_callable=make_recommendation,
    dag=dag,
)

statistics_task = PythonOperator(
    task_id='calculate_statistics',
    python_callable=calculate_statistics,
    dag=dag,
)

[weather_task, calendar_task, inventory_task, combinations_task] >> recommendation_task >> statistics_task
