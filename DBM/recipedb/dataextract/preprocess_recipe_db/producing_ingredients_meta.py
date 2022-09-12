import pandas as pd

def sort_ingredients_list(ingredients_colums):
    '''
        저장된 식재료 데이터 중 식재료 이름을 가져오는 함수
        :param
            recipe_df : 식재료 이름을 가져오기 위한 데이터 프레임
        :return
            중복을 제거한 식재료 리스트
    '''
    ingredient_list = []
    for i in ingredients_colums:
        ingredient_list.append(i)
    return list(set(ingredient_list) - {'nan'})

def get_prime(number_prime):
    '''
        식재료 코드 부여를 위한 소수 생성 함수
        :param
            number_prime : 필요한 소수 갯수
        :return
            인풋 값만큼의 소수 리스트
    '''
    count = 0
    result = []
    number =2
    
    while True:
        res = is_prime(number)
        if res:
            result.append(number)
            count += 1
        number += 1
        if count == number_prime:
            break
    return result

def is_prime(number):
    '''
        소수 판별 함수
        :param
            number : 소수인지 판별하기위 한 수 
        :return
            소수이면 값을 리턴, 아니면 False 값 리턴
    '''
    prime = True
    if number <2:
        prime = False
    else:
        for i in range(2, number):
            if number % i == 0:
                prime = False
                break
    return prime

#식재료 리스트 가져오기
recipe_df = pd.read_csv("./recipe10k_db_ud.csv").astype(str)
col = "ingredient_nm, ... " #식재료 colums 갯수에 따라 유동적으로 지정
recipe_df["ingredient_nm"] = recipe_df[col.split(sep=',')].apply(sort_ingredients_list, axis = 1)
ingredients_list = list(set(sum(recipe_df['ingredient_nm'].values.tolist(), [])))

#식재료 이름, 코드 매칭 및 저장
ingredients_meta = pd.DataFrame.from_dict({"ingredient":ingredients_list, "ingredient_code":get_prime(len(ingredients_list))})
ingredients_meta.to_csv("./ingredients_meta.csv", index=False)
