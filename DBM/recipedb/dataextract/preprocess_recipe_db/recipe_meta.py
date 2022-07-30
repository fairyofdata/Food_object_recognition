import pandas as pd

'''
레시피 메타 데이터 생성
'''    
recipe_df = pd.read_csv("./recipe10k_db_ud.csv").astype(str)
recipe_df = recipe_df[['recipe_nm','recipe_code']]

recipe_df.to_csv("./recipe_meta.csv", index=False)
