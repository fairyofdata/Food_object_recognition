from kafka import KafkaConsumer, KafkaProducer
from pyspark.sql import SparkSession
from pyspark.ml.recommendation import ALSModel
from pyspark.sql.types import IntegerType
import json
import pandas as pd
import pymysql

RECIPEINFOTOPIC = "RECIPEINFO"
RECOMMANDTOPIC = "RECOMMAND"
BROKERS = ["localhost:9091", "localhost:9092", "localhost:9093"]

consumer = KafkaConsumer(RECIPEINFOTOPIC, bootstrap_servers=BROKERS)
producer = KafkaProducer(bootstrap_servers=BROKERS)

MAX_MEMORY = "2g"
spark = SparkSession.builder.appName("recipe-recom")\
    .config("spark.executor.memory", MAX_MEMORY)\
    .config("spark.driver.memory", MAX_MEMORY)\
    .getOrCreate()
        
model_dir = "../Recommand/recipe_recommad_model_als"
model = ALSModel.load(model_dir)


#식재료 메타데이터 호출
conn = pymysql.connect(host = "localhost", user = "", passwd = "", db = "server_db", charset = "utf8")
cursor = conn.cursor()
sql_meta = "SELECT * FROM recipe_meta"
recipe_meta_df=pd.read_sql(sql_meta, conn)
recipe_meta_df_spk = spark.createDataFrame(recipe_meta_df)
recipe_meta_df_spk.cache()


for message in consumer:
    msg = json.loads(message.value.decode())
    
    #Spark ALS 모델로 유저별 레시피 추천
    idcode = int(''.join([str(ord(y)) for y in msg["userid"]])) #유저아이디 코드화
    users_df = spark.createDataFrame([idcode], IntegerType()).toDF("userid_code")
    user_recs_df = model.recommendForUserSubset(users_df, 10000)
    recs_list = user_recs_df.collect()[0].recommendations
    recs_df = spark.createDataFrame(recs_list)
    rec_dfn = recs_df.join(recipe_meta_df_spk, "recipe_code")
    mrec_list = rec_dfn.select("*").toPandas()["recipe_nm"].tolist()
    
    #레시피 추천 후 요리가능 레시피로 필터링
    frec_prep_recipe = list(filter(lambda x: x in msg["prep_recipe"], mrec_list))
    frec_lack_recipe = list(filter(lambda x: x in msg["lack_recipe"], mrec_list))
    msg["frec_prep_recipe"] = frec_prep_recipe
    msg["frec_lack_recipe"] = frec_lack_recipe
    
    producer.send(RECOMMANDTOPIC, json.dumps(msg).encode("utf-8"))
