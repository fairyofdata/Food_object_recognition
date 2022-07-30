import pandas as pd
    
    
'''
수집 식재료 데이터 "식재료 이름" 전처리(토큰화)
'''    
def df_convertor(ingredients, toingre, noingre1, noingre2, noingre3):
    recipe_df = pd.read_csv("/./recipe10k_db_ud.csv").astype(str)
    for i in recipe_df.columns.tolist()[7:]:
        recipe_df[i]=recipe_df[i].apply(lambda x: toingre if (ingredients in x) and (noingre1 not in x) and (noingre2 not in x) and (noingre3 not in x) else x)
        recipe_df.to_csv("./recipe10k_db_ud.csv", index=False)

df_convertor("포함키워드", "변경키워드", "제외키워드", "제외키워드", "제외키워드")    
