import pandas as pd


def merge_ingredients_columns(ingredient_str):
    '''
        여러 식재료를 하나의 열에 리스트로 결합
        :param
            ingredient_str : 식재료 문자열
        :return
            식재료 문자열을 리스트 형태로 리턴
    '''    
    ingredient_list = []
    for i in x:
        ingredient_list.append(i)
    return list(set(ingredient_list) - {'nan'})

#각 열에 나뉘어 있는 식재료 이름을 하나의 열에 리스트 형태로 삽입
recipe_df = pd.read_csv("./recipe10k_db_ud.csv").astype(str)
col = "ingredient_nm, ... "
recipe_df["ingredient_nm"] = recipe_df[col.split(sep=',')].apply(totolist, axis = 1)
recipe_df["ingredient_nm"] = recipe_df["ingredient_nm"].apply(lambda x : str(x)[1:-1].replace("\'", ""))
col2 = "recipe_code,recipe_nm,ingredient_nm,qnt,cooking_time,level_nm,recipe_url,img_src"
recipe_df2 = recipe_df[col2.split(sep=',')]
recipe_df2.to_csv("./recipe10k_fdb.csv", index=False)

