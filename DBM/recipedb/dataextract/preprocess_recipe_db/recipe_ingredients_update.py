import pandas as pd
    
    
def convert_ingredients_nm(including_ingredient, toingredient, noingredient1, noingredient2, noingredient3):
    '''
        같은 식재료여도 이름이 제각각이기에 같은 이름으로 맞춰주는 함수
        :param
            including_ingredient : 바꿀 식재료를 포함시킬 단어 
            toingredient : 바꿀 식재료 이름
            noingredient1,2,3 : 제외할 단어
        :action
            지정된 식져료 단어를 일정 규칙에 맞게 변경 후 저장
    '''    
    recipe_df = pd.read_csv("/./recipe10k_db_ud.csv").astype(str)
    for i in recipe_df.columns.tolist()[7:]:
        recipe_df[i] = recipe_df[i].apply(lambda x : toingredient if (including_ingredient in x) 
                                                                     and (noingredient1 not in x) 
                                                                     and (noingredient2 not in x) 
                                                                     and (noingredient3 not in x) 
                                                                     else x
                                                                     )
        recipe_df.to_csv("./recipe10k_db_ud.csv", index=False)

convert_ingredients_nm("포함키워드", "변경키워드", "제외키워드", "제외키워드", "제외키워드")    
