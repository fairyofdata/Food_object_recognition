import pandas as pd

#기존 등록되어 있는 레시피와 레시피코드 매칭 후 메타데이터 형태로 저장
recipe_df = pd.read_csv("./recipe10k_db_ud.csv").astype(str)
recipe_df = recipe_df[['recipe_nm','recipe_code']]

recipe_df.to_csv("./recipe_meta.csv", index=False)
