import pandas as pd

#수집한 레시피목록/이미지 데이터와, 세부정보 데이터 조인
recipe10k_info = pd.read_csv("./recipedb_csv/recipe10k_info.csv")
recipe10k_img = pd.read_csv("./recipedb_csv/recipe10k_img.csv")

recipe10k_df = pd.merge(left = recipe10k_info , right = recipe10k_img, how = "inner", on = "recipe_code")
recipe10k_df.to_csv("./recipedb_csv/recipe10k_db.csv", index=False, encoding='utf-8-sig')
