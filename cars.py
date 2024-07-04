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


spisok = {}
with open('cars.json', 'r', encoding="utf-8") as fcc_file:
    fcc_data = json.load(fcc_file)
    #print(fcc_data)

for i in fcc_data:
    #print(i)
    #print()
    for n,m in i.items():
        #print(n, m)
        #print()
        if n == 'name':
            marka = m
        if n == 'models':
            spisok_model = m
    #print (marka, spisok_model)
    if 'Mercedes-Benz' == marka:
        marka = 'Mercedes'
    for a in spisok_model:
        print(a)
        for odun, dva in a.items():
            if odun == "name":
                version = dva 
            if odun == "class":
                model = dva
            if odun == "year-from":
                year = dva
        stroka = str(version)+ ":" + str(year)+ ";" + str(model) + " " 
        spisok[stroka] = marka          
    

with open("modelu.json", "a", encoding="utf-8") as file:
    json.dump(spisok, file, indent=4, ensure_ascii=False)