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


headers = {
    "Accept" : "application/json, text/javascript, */*; q=0.01",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
}
"""
url = "https://motoallegro.net/ru/b-catalog/a-class/"
driver.get(url=url)
time.sleep(1)

with open(f"first.html", "w", encoding="utf-8") as file:
    file.write(driver.page_source)

with open(f"first.html", encoding="utf-8") as file:
    src = file.read()
soup = BeautifulSoup(src, 'html.parser')
href_first_page = soup.find_all("div", class_="categories-item__header")

zapchast_and_href = {}
two_zapchast_and_href = {}
#print(href_first_page)
nomer = 1
for item in href_first_page:
    item = str(item)
    href = item[item.find("href")+6 : item.find('/">')]
    name_href = item[item.find('/">')+3 : item.find('</a>')]
    print(href, name_href, nomer)

    zapchast_and_href[nomer] = href
    nomer += 1


with open("first_href.json", "a", encoding="utf-8") as file:
    json.dump(zapchast_and_href, file, indent=4, ensure_ascii=False)

input_number = input("Введи номер подраздела, который тебя интересует -  ")

with open("first_href.json", encoding="utf-8") as file:
    first_pars = json.load(file)

for num, href_categoria in first_pars.items():
    if input_number == num:
        #print(num)
        href_href = href_categoria
        

number = 1
#print(number)    
driver.get(url=href_href)
time.sleep(1)
with open(f"first.html", "w", encoding="utf-8") as file:
    file.write(driver.page_source)

with open(f"first.html", encoding="utf-8") as file:
    src = file.read()
soup = BeautifulSoup(src, 'html.parser')
href_second_page = str(soup.find_all("div", class_="categories-item__collapse active js--collapse-categories-item"))
list_second = href_second_page.split("</a>")
for item_two in list_second:
    href_second = item_two[item_two.find("href")+6 : item_two.find('/">') +1]
    name_href_second = item_two[item_two.find('/">')+3 : item.find('</a>')]
    print(href_second, name_href_second, number)
    two_zapchast_and_href[href_second] = number
    number += 1

with open("second_href.json", "a", encoding="utf-8") as file:
    json.dump(two_zapchast_and_href, file, indent=4, ensure_ascii=False)

input_number_second = int(input("Введи номер подраздела(в последней части), который тебя интересует -  "))

with open("second_href.json", encoding="utf-8") as file:
    second_pars = json.load(file)
#print(input_number_second)
for last_categoria, num_2 in second_pars.items():
    #print(input_number_second, num_2)
    if input_number_second == int(num_2):
        print(f"Ты выбрал категорию {last_categoria}")
        url = last_categoria

os.remove("first.html")
os.remove("first_href.json")
os.remove("second_href.json")

driver.get(url=url)
time.sleep(1)
with open(f"three.html", "w", encoding="utf-8") as file:
    file.write(driver.page_source)

with open(f"three.html", encoding="utf-8") as file:
    src = file.read()
soup = BeautifulSoup(src, 'html.parser')
href_three_page = soup.find_all("div", class_="card item-card-link products__card")

#print(href_three_page)
for item in href_three_page:
    #print(item)
    item = str(item)
    href_part = item[item.find("<a href")+9 : item.find('/">')+1]
    print(href_part)"""
href_part = "https://motoallegro.net/ru/detail/prod-15483426354/"

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
info = soup_one.find_all("div", class_="characteristic__item")
#print(info)
for item in info:
    
    #print(item.text, "Здесь текст!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    item = str(item)
    if "cостояние:" in item:
        print(item, "&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
        item = item.replace("  ","").replace("\n"," ").replace("/r"," ")
        print(item)
        status = item[item.find('characteristic__value">') + 23 : item.find(' </span> ')].replace(" ","")
print(status)
    


a = input("Введи любое число, чтобы закончить - ")
