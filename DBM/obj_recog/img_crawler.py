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

def log_filter(log_):
    return (
        log_["method"] == "Network.responseReceived"
        and "image/jpeg" in log_["params"]["response"]["mimeType"]
    )

'''
구글 이미지 수집 크롤러
'''
def kw_deinfo(name, filename, start_num):    
    
    capabilities = DesiredCapabilities.CHROME
    capabilities["goog:loggingPrefs"] = {"performance": "ALL"}
    
    options = webdriver.ChromeOptions()
    options.add_argument('--headless') 
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), desired_capabilities=capabilities, options=options)
    
    if not os.path.isdir('./{}'.format(filename)):
        os.mkdir('./{}'.format(filename))
    url = f"https://www.google.com/search?q={name}&rlz=1C5CHFA_enKR1009KR1009&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjTueevy8P4AhXet1YBHRpJBE0Q_AUoAXoECAIQAw&biw=1440&bih=764&dpr=2"
    driver.get(url)
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