import pandas as pd
import pymysql

#사용자 레시피 열람 데이터 호출 및 csv 저장

storage_connect = pymysql.connect(host = "ec2", user = "", passwd = "", db = "svdb", charset = "utf8")

user_select_db = "SELECT * FROM user_select_db"
user_select_df = pd.read_sql(user_select_db, storage_connect)

user_select_df["userid_code"] = user_select_df["userid"].apply(lambda x : int(''.join([str(ord(y)) for y in x])))#ALS 활용을위한 useid 숫자화
user_select_df.to_csv("./model_data/user_select_db.csv", mode='w', index = False)
