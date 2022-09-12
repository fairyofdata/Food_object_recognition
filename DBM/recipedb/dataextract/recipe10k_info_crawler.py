import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv
from tqdm import tqdm

def crawl_10k(recipe_code):
    '''
        레시피 세부 정보 크롤링(만개의레시피)
        :param
            recipe_code : 세부정보를 수집할 레시피 코드
        :return
            인풋 레시피코드의 세부정보
    '''    
    URL = f'https://www.10000recipe.com/recipe/{recipe_code}'
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')

    # 레시피 이름 Data
    find_recipe_nm = soup.find('div', 'view2_summary st3')
    RECIPE_NM = find_recipe_nm.find('h3').get_text()
    RECIPE_NM_data = RECIPE_NM.strip()
    # 음식양 Data
    QNT_data = soup.find('span', 'view2_summary_info1').get_text()
    # 조리 시간 Data
    COOKING_TIME_data = soup.find('span', 'view2_summary_info2').get_text()
    # 난이도 Data
    LEVEL_data = soup.find('span', 'view2_summary_info3').get_text()
    # 식재료 추출
    a = soup.find('div', 'ready_ingre3')
    IRDNT = []
    for b in a.find_all('li'):
        IRDNTS_lst = b.get_text().split('\n')[0].strip().split(' '*84)[0]
        IRDNT.append(IRDNTS_lst)

    RESULT = [recipe_code, RECIPE_NM_data, str(IRDNT), QNT_data, COOKING_TIME_data, LEVEL_data, URL]
    return RESULT

#수집한 레시피 목록의 세부정보 수집 후 저장
recipe_code_list = pd.read_csv(".recipedb_csv/recipe10k_img.csv")["recipe_code"].values.tolist()
error_recipe_code = []
with open("./recipedb_csv/recipe10k_info.csv", 'a', newline='') as f: 
    for recipe_code in tqdm(recipe_code_list):
        try:
            result = crawl_10k(recipe_code)
            write = csv.writer(f)       
            write.writerow(result) 
        except:
            error_recipe_code.append(recipe_code)

    write.writerow(error_recipe_code)
