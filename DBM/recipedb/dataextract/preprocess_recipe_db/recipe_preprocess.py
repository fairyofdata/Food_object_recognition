import pandas as pd


def merge_ingredients_columns(x):
    '''
        여러 식재료를 하나의 열에 리스트로 결합
        :param
            including_ingredient : 바꿀 식재료를 포함시킬 단어 
            toingredient : 바꿀 식재료 이름
            noingredient1,2,3 : 제외할 단어
        :action
            지정된 식져료 단어를 일정 규칙에 맞게 변경 후 저장
    '''    
    tttlist = []
    for i in x:
        tttlist.append(i)
    return list(set(tttlist) - {'nan'})

#각 열에 나뉘어 있는 식재료 이름을 하나의 열에 리스트 형태로 삽입
recipe_df = pd.read_csv("./recipe10k_db_ud.csv").astype(str)
col = "ingredient_nm, ... "
recipe_df["ingredient_nm"] = recipe_df[col.split(sep=',')].apply(totolist, axis = 1)
recipe_df["ingredient_nm"] = recipe_df["ingredient_nm"].apply(lambda x : str(x)[1:-1].replace("\'", ""))
col2 = "recipe_code,recipe_nm,ingredient_nm,qnt,cooking_time,level_nm,recipe_url,img_src"
recipe_df2 = recipe_df[col2.split(sep=',')]
recipe_df2.to_csv("./recipe10k_fdb.csv", index=False)

