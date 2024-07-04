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

url = "https://www.exist.ru/Catalog/Global/"
spisok = {}

headers = {
    "Accept" : "application/json, text/javascript, */*; q=0.01",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
}




req = requests.get(url=url, headers=headers)
src = req.text

soup = BeautifulSoup(src, 'html.parser')
mar = soup.find_all("li")
#print(mar)
for item in mar:
    
    item = str(item)
    if "/Catalog/" in item:
        item1 = item[item.find("href") :]
        #print(item1)
        item2 = item1[item1.find("href")+6 : item1.find('">')]
        #print(item2)
        if ("Cars" in str(item2)) or ("Trucks" in str(item2)) or ("Commercial" in str(item2)):
            url_mark = "https://www.exist.ru" + item2
            print(url_mark)
            if "Cars" in url_mark:
                marka = url_mark[url_mark.find("Cars") + 5 :]
            if "Trucks" in url_mark:
                marka = url_mark[url_mark.find("Trucks") + 7 :]
            if "Commercial" in url_mark:
                marka = url_mark[url_mark.find("Commercial") + 11 :]
            print(marka)
            req = requests.get(url=url_mark, headers=headers)
            src = req.text

            soup = BeautifulSoup(src, 'html.parser')
            
            mod = soup.find_all("div", class_="car-info__description")
            #print(mod)
            for item in mod:
                item = str(item)
                model_all = item[item.find('href') : item.find('</a>')]
                model = model_all[model_all.find('">')+2 :]
                version = item[item.find('car-info__car-models')+22 : item.find('car-info__car-years')-19]
                year = item[item.find('car-info__car-years')+24 : item.find('</b>')]
                print( model , version, year)
                stroka = str(version)+ ":" + str(year)+ ";" + str(model) + " "
                spisok[stroka] = marka

                

with open("modelu.json", "a", encoding="utf-8") as file:
    json.dump(spisok, file, indent=4, ensure_ascii=False)            
