import pandas as pd
import pymysql
from pyspark.sql import SparkSession

'''
사용자 열람데이터 호출 및 ALS 모델 훈련 가능 형태로 데이터 가공 후 parqueet 파일로 저장
'''
conn = pymysql.connect(host = "ec2", user = "", passwd = "", db = "svdb", charset = "utf8")

sql_select = "SELECT * FROM user_select_db"
user_select_df = pd.read_sql(sql_select, conn)

user_select_df["userid_code"] = user_select_df["userid"].apply(lambda x : int(''.join([str(ord(y)) for y in x])))
# user_select_df.to_csv("./model_data/user_select_db.csv", mode='w', index = False)

MAX_MEMORY = "1g"
spark = SparkSession.builder.appName("recipe-recom")\
    .config("spark.executor.memory", MAX_MEMORY)\
    .config("spark.driver.memory", MAX_MEMORY)\
    .getOrCreate()

user_select_df_spk = spark.createDataFrame(user_select_df)
# directory = "../model_data"
# us_file = "user_select_db.csv"
# user_select_df_spk = spark.read.csv(f"file:///{directory}/{us_file}", inferSchema=True, header=True)
user_select_MLdf_spk = user_select_df_spk.select(["userid_code", "recipe_code"])
user_select_MLdf_spk_gb = user_select_MLdf_spk.groupBy("userid_code", "recipe_code").count()
user_select_MLdf_spk_gb.write.format("parquet").mode("overwrite").save("./model_data/traindata/")

