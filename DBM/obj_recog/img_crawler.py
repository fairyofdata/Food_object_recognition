import time
import json
from tqdm import tqdm
import urllib.request
import os

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.by import By

def crawl_googleimg_bylog(name, filename, start_num):    
    '''
        셀레니움 로그크롤링을 활용한 구글이미지 수집 함수
        :param
            name : 수집할 이미지 검색어
            filename : 수집 후 이미지 저장 폴더 및 파일 이름
            start_num : 파일 이름 저장 시, 넘버링 시작 번호(ex. 구글이미지51/동일한 객체를 다른 검색어로 수집 시 활용)
        :action
            이미지 주소값 수집 후, 저장
    '''
    capabilities = DesiredCapabilities.CHROME
    capabilities["goog:loggingPrefs"] = {"performance": "ALL"}
    
    options = webdriver.ChromeOptions()
    options.add_argument('--headless') 
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), desired_capabilities=capabilities, options=options)
    
    if not os.path.isdir('./{}'.format(filename)):
        os.mkdir('./{}'.format(filename))
    
    #이미지 검색        
    url = f"https://www.google.com/search?q={name}&rlz=1C5CHFA_enKR1009KR1009&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjTueevy8P4AhXet1YBHRpJBE0Q_AUoAXoECAIQAw&biw=1440&bih=764&dpr=2"
    driver.get(url)
    
    #스크롤 다운
    time.sleep(0.25) 
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            try:
                time.sleep(1.5)
                new_height = driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:  
                    driver.find_element(by=By.XPATH, value="/html/body/div[2]/c-wiz/div[3]/div[1]/div/div/div/div[1]/div[2]/div[2]/input").click()
                    time.sleep(1.5)
                    new_height = driver.execute_script("return document.body.scrollHeight")
            except:
                break
        last_height = new_height
    
    #쌓인 로그 크롤링 및 이미지 저장    
    logs_raw = driver.get_log("performance")
    logs = [json.loads(lr["message"])["message"] for lr in logs_raw]
    z = start_num
    for log in tqdm(filter(log_filter, logs)):
        rep_url = log["params"]["response"]["url"]
        saveUrl = "./" + filename +"/" + filename + format(z, '04')
        req = urllib.request.Request(rep_url)
        imgUrl = urllib.request.urlopen(req).read()
        with open(saveUrl + '.jpg', "wb") as f:
            f.write(imgUrl)
        z += 1
    driver.close()
    
def log_filter(log_):
    '''
        수집한 로그의 이미지 주소값만 추출하는 함수
        :param
            log_ : 수집한 로그
        :return
            이미지 주소 값
    '''
    return (
        log_["method"] == "Network.responseReceived" 
        and "image/jpeg" in log_["params"]["response"]["mimeType"]
    )