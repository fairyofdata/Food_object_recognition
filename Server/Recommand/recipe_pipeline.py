from datetime import datetime
from airflow import DAG
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator

# from airflow.operators.python import PythonOperator
# import recipe_preprocess
# import recipe_train_als

#미완성
#주기적인 모델 업데이트를 위한 에어플로우 스케줄링 파이프라인
default_args = {
    'start_date': datetime(2022, 1, 1)
}

with DAG(
    dag_id="spark-recipe-recommand-pipeline",
    schedule_interval="@daily",
    default_args=default_args,
    tags=["spark", "ml", "recipe", "recommand"],
    catchup=False) as dag:
    
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
    
    recipe_preprocess >> recipe_train_als


    # recipe_preprocess_py = PythonOperator(
    #     task_id = "recipe_preprocess",
    #     python_callable = recipe_preprocess
    # )
    
    # recipe_train_als_py = PythonOperator(
    #     task_id = "recipe_train_als",
    #     python_callable = recipe_train_als
    # )
    
    # recipe_preprocess_py >> recipe_train_als_py
    
