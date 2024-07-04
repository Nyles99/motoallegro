import json
from turtle import pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import requests
from bs4 import BeautifulSoup
import os
import shutil
import csv
from PIL import Image, UnidentifiedImageError
import time

options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option('excludeSwitches', ['enable-logging'])
#options.add_experimental_option('useAutomationExtension', False)
options.add_argument('--ignore-certificate-errors')
options.add_argument("start-maximized") # // https://stackoverflow.com/a/26283818/1689770
options.add_argument("enable-automation")#  // https://stackoverflow.com/a/43840128/1689770
#options.add_argument("--headless")#  // only if you are ACTUALLY running headless
options.add_argument("--no-sandbox")# //https://stackoverflow.com/a/50725918/1689770
options.add_argument("--disable-dev-shm-usage")# //https://stackoverflow.com/a/50725918/1689770
options.add_argument("--disable-browser-side-navigation")# //https://stackoverflow.com/a/49123152/1689770
options.add_argument("--disable-gpu")
options.add_argument("--disable-infobars")# //https://stackoverflow.com/a/43840128/1689770
options.add_argument("--enable-javascript")

#options.add_argument("--proxy-server=91.237.180.78:24523")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    'source': '''
        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array:
        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise:
        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol:
    '''
})
with open("modelu.json", encoding="utf-8") as file:
    sravnenue = json.load(file)


headers = {
    "Accept" : "application/json, text/javascript, */*; q=0.01",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
}




href_part = "https://motoallegro.net/ru/detail/prod-15961190941/?attempt=1"
model = ''
kuzov = ''
year = ''
driver.get(url=href_part)
time.sleep(1)
with open(f"one_part.html", "w", encoding="utf-8") as file:
    file.write(driver.page_source)

with open(f"one_part.html", encoding="utf-8") as file:
    src_one_part = file.read()
soup_one = BeautifulSoup(src_one_part, 'html.parser')
title_name = str(soup_one.find_all("h1", class_="product-info__title"))
title_name = title_name.replace("  ","").replace("\n"," ").replace("/r"," ")
marka_and_model_and_num_zap = title_name[title_name.find('_title">  ')+10 : title_name.find('  </h1>')]
print(marka_and_model_and_num_zap)
all_words = marka_and_model_and_num_zap.replace('-',' ').lower().split()
print(all_words)
for kym, ma in sravnenue.items():
    
    
    
    
    if str(ma).lower() in all_words:
        kuz = kym[: kym.find(':')]
        print(kuz)
        m = kym[kym.find(';')+1 : kym.find(' ') ]
        print(m)
        marka = ma
        if (len(str(kuz))>0) and (str(kuz).lower() in all_words):
            kuzov = kuz
            year = kym[kym.find(':')+1 : kym.find(';')]
            model = m
        elif str(m).lower() in all_words:
            model = m
            year = kym[kym.find(':') : kym.find(';')]
        else:
            marka = "ничего"
            model = "не"
            kuzov = "нашлось"
            year = "!!!!!!!!"
        
info = soup_one.find_all("div", class_="characteristic__item")
#print(info)
status = "б/у"
side = ''
prouzbod_text = ''
nomer = ''
ka4estvo = ''
price = ''
number_lot = ''
zamena = ''
for item in info:
    
    #Статус запчасти - новая или бу
    item = str(item)
    if "cостояние:" in item:
        item = item.replace("  ","").replace("\n"," ").replace("/r"," ")
        #print(item)
        status = item[item.find('characteristic__value">') + 23 : item.find(' </span> ')]
        if ("новое" in status) or ("новый" in status) or ("новые" in status) or ("новая" in status) :
            status = "новая"
        else:
            status = 'б/у'
    if "производитель запчасти:" in item:
        item = item.replace("  ","").replace("\n"," ").replace("/r"," ")
        #print(item)
        prouzbod_text = item[item.find('characteristic__value">') + 24 : item.find(' </span> ')]
    if "сторона:" in item:
        item = item.replace("  ","").replace("\n"," ").replace("/r"," ")
        #print(item)
        side = item[item.find('characteristic__value">') + 24 : item.find(' </span> ')]
    if "номер каталожный запчасти:" in item:
        item = item.replace("  ","").replace("\n"," ").replace("/r"," ")
        #print(item)
        nomer = item[item.find('_blank') + 8 : item.find('</a>')]
    if "качество запчасти" in item:
        item = item.replace("  ","").replace("\n"," ").replace("/r"," ")
        #print(item)
        ka4estvo = item[item.find('"characteristic__value">') + 24 : item.find('</span> </div')].replace("pojazdu","на траспортном средстве")
    if "номери католожные заменителей:" in item:
        item = item.replace("  ","").replace("\n"," ").replace("/r"," ")
        #print(item)
        zamena = item[item.find('_blank') + 8 : item.find('</a>')]
price_obj = soup_one.find_all("span", class_="product-total__dollars")
for item in price_obj:
    price = item.text.replace("$","").replace(" ","")
number_lot_obj = soup_one.find_all("span", class_="product-info__lot-value")
for item in number_lot_obj:
    number_lot = item.text.replace("$","").replace(" ","")

print()
print(marka)
print(model)
print(year)
print(kuzov)
print(zamena)
print(ka4estvo)
print(number_lot)
print(price)
print(nomer)
print(side)    
print(prouzbod_text)
print(status)