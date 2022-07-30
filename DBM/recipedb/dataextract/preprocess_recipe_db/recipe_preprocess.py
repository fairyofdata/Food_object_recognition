import pandas as pd

'''
시재료 토큰화 완료 데이터프레임 취합 가공
'''
recipe_df = pd.read_csv("./recipe10k_db_ud.csv").astype(str)

def totolist(x):
    tttlist = []
    for i in x:
        tttlist.append(i)
    return list(set(tttlist) - {'nan'})

col = "ingredients_nm, ... "
recipe_df["ingredients_nm"] = recipe_df[col.split(sep=',')].apply(totolist, axis = 1)
recipe_df["ingredients_nm"] = recipe_df["ingredients_nm"].apply(lambda x : str(x)[1:-1].replace("\'", ""))
col2 = "recipe_code,recipe_nm,ingredients_nm,qnt,cooking_time,level_nm,recipe_url,img_src"
recipe_df2 = recipe_df[col2.split(sep=',')]
recipe_df2.to_csv("./recipe10k_fdb.csv", index=False)

