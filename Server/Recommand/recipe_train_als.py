from pyspark.ml.recommendation import ALS
from pyspark.sql import SparkSession


'''
ALS 모델훈련
'''
MAX_MEMORY = "1g"
spark = SparkSession.builder.appName("recipe-recom")\
    .config("spark.executor.memory", MAX_MEMORY)\
    .config("spark.driver.memory", MAX_MEMORY)\
    .getOrCreate()

data_dir = "./model_data/traindata/"
train_df = spark.read.parquet(data_dir)
train_df.cache()

als = ALS(
    maxIter=10,
    regParam=0.1,
    userCol="userid_code",
    itemCol="recipe_code",
    ratingCol="count",
    coldStartStrategy="drop"
)

model = als.fit(train_df)

simplemodeldir = "./recipe_recommad_model_als"
model.write().overwrite().save(simplemodeldir)
