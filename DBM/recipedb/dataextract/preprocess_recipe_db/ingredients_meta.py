import pandas as pd
    
recipe_df = pd.read_csv("./recipe10k_db_ud.csv").astype(str)

'''
전체 식재료 리스트 정렬
'''
def totolist(x):
    tttlist = []
    for i in x:
        tttlist.append(i)
    return list(set(tttlist) - {'nan'})

col = "ingredients_nm, ... "
recipe_df["ingredients_nm"] = recipe_df[col.split(sep=',')].apply(totolist, axis = 1)
ingredients_list = list(set(sum(recipe_df['ingredients_nm'].values.tolist(), [])))

'''
소수 판별 함수
'''
def is_prime(n):
    prime = True
    if n <2:
        prime = False
    else:
        for i in range(2, n):
            if n % i == 0:
                prime = False
                break
    return prime


'''
식재료 코드화를 위한 소수 생성 함수
'''
def get_prime(n):
    count = 0
    result = []
    number =2
    
    while True:
        res = is_prime(number)
        if res:
            result.append(number)
            count += 1
        number += 1
        if count == n:
            break
    return result

'''
식재료 이름, 코드 매칭 및 저장
'''
ingredients_meta = pd.DataFrame.from_dict({"ingredients":ingredients_list, "ingredients_code":get_prime(len(ingredients_list))})
ingredients_meta.to_csv("./ingredients_meta.csv", index=False)
