from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator

import recipe_mysqltocsv


#미완성
#주기적인 모델 업데이트를 위한 에어플로우 스케줄링 파이프라인
default_args = {
    'start_date': datetime(2022, 1, 1)
}

with DAG(
    dag_id="spark-recipe-rec-pipeline",
    schedule_interval="@daily",
    default_args=default_args,
    tags=["spark", "ml", "recipe", "rec"],
    catchup=False) as dag:

    recipe_load_mysqltocsv = PythonOperator(
        task_id = "recipe_mysqltocsv",
        python_callable = recipe_mysqltocsv
    )
    
    recipe_preprocess = SparkSubmitOperator(
        application="./recipe_preprocess.py",
        task_id='recipe_preprocess',
        conn_id="spark_local"
    )

    recipe_train_als = SparkSubmitOperator(
        application='./recipe_train_als.py',
        task_id="recipe_train_als",
        conn_id="spark_local"
    )

    recipe_load_mysqltocsv >> recipe_preprocess >> recipe_train_als