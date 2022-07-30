import requests
from bs4 import BeautifulSoup
import pandas as pd

'''
레시피 목록 데이터 및 이미지 링크 크롤링
'''
RECIPE_ID_lst = []
img_src_lst = []

df = pd.DataFrame(columns=['recipe_code', 'img_src'])

for n in range(4539):
    print(n)
    n += 1
    
    URL = f'https://www.10000recipe.com/recipe/list.html?order=reco&page={n}'
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    recipe_list = soup.find_all('li', 'common_sp_list_li')

    for recipe in recipe_list:
        
        # 레시피 아이디 Data
        find_RECIPE_ID = recipe.find('a', 'common_sp_link')['href']
        RECIPE_ID_data = find_RECIPE_ID.split(sep='/')[-1]
        RECIPE_ID_lst.append(RECIPE_ID_data)
        
        # 이미지 주소 Data
        find_img_src = recipe.find('a', 'common_sp_link')('img')[-1]
        img_src_data = find_img_src.get('src')
        img_src_lst.append(img_src_data)

# DataFrame에 element 추가
df['recipe_code'] = RECIPE_ID_lst
df['img_src'] = img_src_lst

df.to_csv("./recipedb_csv/recipe10k_img.csv", index=False, encoding='utf-8-sig')