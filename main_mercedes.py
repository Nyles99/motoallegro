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


input_name = input("Как назовем файл? - ")
pricing = input("Введи цифру ценообразования от 1 до 5 - ")

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
with open("mercedes.json", encoding="utf-8") as file:
    sravnenue = json.load(file)


headers = {
    "Accept" : "application/json, text/javascript, */*; q=0.01",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
}

if os.path.exists(f"{input_name}_zzap.csv"):
    print("файл csv уже есть")
else:
    with open(f"{input_name}_zzap.csv", "w", encoding="utf-8") as file_data:
        writer = csv.writer(file_data)

        writer.writerow(
            (
                "ПРОИЗВОДИТЕЛЬ",
                "НОМЕР ДЕТАЛИ",
                "НАИМЕНОВАНИЕ ДЕТАЛИ",
                "ОПИСАНИЕ ZZAP",
                "ЦЕНА",
                "СОСТОЯНИЕ",
                "СРОК ДОСТАВКИ",
                "ФОТО",
            )
        )

if os.path.exists(f"{input_name}_drom.csv"):
    print("файл csv уже есть")
else:
    with open(f"{input_name}_drom.csv", "w", encoding="utf-8") as file_data:
        writer = csv.writer(file_data)

        writer.writerow(
            (
                "АРТИКУЛ",
                "НАИМЕНОВАНИЕ ДЕТАЛИ",
                "СОСТОЯНИЕ",
                "МАРКА",
                "МОДЕЛЬ",
                "ВЕРСИЯ",
                "НОМЕР ДЕТАЛИ",
                "ОБЪЕМ ДВИГАТЕЛЯ",
                "ГОД",
                "L_R",
                "F_R",
                "U_D",
                "ЦВЕТ",
                "ОПИСАНИЕ DROM",
                "КОЛИЧЕСТВО",
                "ЦЕНА",
                "НАЛИЧИЕ",
                "СРОК ДОСТАВКИ",
                "ФОТО",
                "Описание запчасти",
            )
        )



url = "https://motoallegro.net/ru/b-catalog/a-class/"
driver.get(url=url)
time.sleep(1)
marka = ''
model = ''
version = ''
year = ''

kuzova = []
for kym, ma in sravnenue.items():     
    kuz = kym[: kym.find(':')]
    if len(str(kuz))>0:
        kuzova.append(kuz)
#print(kuzova)
def pars_card(href_card, name_zap):
    name_zap1 = ''
    href_part = href_card
    #href_part = "https://motoallegro.net/ru/detail/prod-15733303377/"
    marka = ''
    model = ''
    version = ''
    year = ''
    volume = ''
    fuel = ''
    transmission = ''
    car_body = ''
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
    #print(marka_and_model_and_num_zap)
    marka_and_model_and_num_zap = marka_and_model_and_num_zap.lower().replace("amg","mercedes")
    if "крепления" in marka_and_model_and_num_zap:
        name_zap1 = "крепления" + ' для ' + name_zap
    elif "крепление" in marka_and_model_and_num_zap:
        name_zap1 = "крепление" + ' для ' + name_zap
    elif "pokrywa" in marka_and_model_and_num_zap:
        name_zap1 = "покрышка" + ' для ' + name_zap
    elif "заслонка жалюзи вентилятора" in marka_and_model_and_num_zap:
        name_zap1 = "заслонка жалюзи вентилятора"
    elif "заглушка омывателя фары" in marka_and_model_and_num_zap:
        name_zap1 = "заглушка омывателя фары"
    elif "рамка окуляр" in marka_and_model_and_num_zap:
        name_zap1 = "заглушка омывателя фары"
    elif "накладка" in marka_and_model_and_num_zap:
        name_zap1 = "накладка" + ' для ' + name_zap
    elif "заглушка фаркопа" in marka_and_model_and_num_zap:
        name_zap1 = "заглушка фаркопа"
    elif "датчики" in marka_and_model_and_num_zap:
        name_zap1 = "датчики"
    elif "капот" in marka_and_model_and_num_zap:
        name_zap1 = "капот"
    elif "дифузор" in marka_and_model_and_num_zap:
        name_zap1 = "дифузор"
    elif "спойлер" in marka_and_model_and_num_zap:
        name_zap1 = "спойлер"
    elif "угол бампера" in marka_and_model_and_num_zap:
        name_zap1 = "угол бампера"
    elif "зарядное устройство" in marka_and_model_and_num_zap:
        name_zap1 = "зарядное устройство"
    elif "радио" in marka_and_model_and_num_zap:
        name_zap1 = "магнитола"
    elif "замок зажигания" in marka_and_model_and_num_zap:
        name_zap1 = "замок зажигания"
    elif "шлейф" in marka_and_model_and_num_zap:
        name_zap1 = "шлейф"
    elif "корпус блока" in marka_and_model_and_num_zap:
        name_zap1 = "корпус блока"
    elif "вентилятор блока" in marka_and_model_and_num_zap:
        name_zap1 = "вентилятор блока"
    elif "модуль замка" in marka_and_model_and_num_zap:
        name_zap1 = "модуль замка"
    elif "дисплей" in marka_and_model_and_num_zap:
        name_zap1 = "дисплей"
    elif "камера заднего вида" in marka_and_model_and_num_zap:
        name_zap1 = "камера заднего вида"
    elif "усилитель радио" in marka_and_model_and_num_zap:
        name_zap1 = "усилитель радио"
    elif "датчик сенсор дождя" in marka_and_model_and_num_zap:
        name_zap1 = "датчик сенсор дождя"
    elif "декор панели" in marka_and_model_and_num_zap:
        name_zap1 = "декор панели"
    elif "переключатель управления" in marka_and_model_and_num_zap:
        name_zap1 = "переключатель управления" + ' для ' + name_zap
    elif "модуль" in marka_and_model_and_num_zap:
        name_zap1 = "модуль"
    elif "штекир" in marka_and_model_and_num_zap:
        name_zap1 = "штекир"
    elif "модуль реле свечей накаливания" in marka_and_model_and_num_zap:
        name_zap1 = "модуль реле свечей накаливания"
    elif "проигрыватель" in marka_and_model_and_num_zap:
        name_zap1 = "магнитола"
    elif "заглушка крышка фары" in marka_and_model_and_num_zap:
        name_zap1 = "заглушка крышка фары"
    elif "колпак стекло для фары" in marka_and_model_and_num_zap:
        name_zap1 = "колпак стекло для фары"      
    else:
        name_zap1 = name_zap
    all_words = marka_and_model_and_num_zap.replace('-',' ').split()

    #print(all_words)
    n = 0
    for kym, ma in sravnenue.items():
        #print(kym)
        
        if n != 1:
            ku = kym[: kym.find(':')]     
            if str(ma).lower() in all_words:
                
                m = kym[kym.find(';')+1 : kym.find(' ') ]
                #print(m)
                #print(m)
                marka = ma
                
                if len(str(ku))>0:
                    if str(ku).lower() in all_words:
                        if n !=1:
                            #print(ku)
                            #print(m)
                            version = ku
                            year = kym[kym.find(':')+1 : kym.find(';')]
                            model = m
                            n=1
                    else:
                        marka = ma
                        model = marka_and_model_and_num_zap
                        version = "!!!!!!!"
                        year = "!!!!!!!!"
            else:
                if (str(ma).lower() in all_words) or (str(ku).lower() in all_words):
                    m = kym[kym.find(';')+1 : kym.find(' ') ]
                    version = ku
                    year = kym[kym.find(':')+1 : kym.find(';')]
                    model = m
                    marka = ma

    foto = ''
    foto_obj = str(soup_one.find("div", class_="product-frame__frame js--init-product-frame"))
    #print(foto_obj)
    foto = foto_obj[foto_obj.find('data-img="1"')+19 : foto_obj.find('<picture class="product-frame__picture">')-3]
    print(foto)

    info = soup_one.find_all("div", class_="characteristic__item")
    #print(info)
    proizvoditel = ''
    status = "б/у"
    side = ''
    prouzbod_text = ''
    nomer = ''
    ka4estvo = ''
    price = ''
    number_lot = ''
    zamena = ''
    num_zap = ''
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
            proizvoditel = str(item[item.find('characteristic__value">') + 24 : item.find(' </span> ')]).replace(" с","")
        if "сторона:" in item:
            item = item.replace("  ","").replace("\n"," ").replace("/r"," ")
            #print(item)
            side = item[item.find('characteristic__value">') + 24 : item.find(' </span> ')]
        if "номер каталожный запчасти:" in item:
            item = item.replace("  ","").replace("\n"," ").replace("/r"," ")
            #print(item)
            num_zap = item[item.find('_blank') + 8 : item.find('</a>')]
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
        artical = item.text.replace("$","").replace(" ","")

    print()
    print(marka)
    print(model)
    print(year)
    print(version)
    print(zamena)
    print(ka4estvo)
    print(artical)
    print(price)
    print(num_zap)
    print(side)    
    print(proizvoditel)
    print(status)
    print(name_zap1)
    text_zzap = f"{marka} {model} {version} {year}г.в., {fuel}, {volume}, {transmission}, {car_body}. Будьте готовы назвать АРТИКУЛ: Z-{artical}.{num_zap} Склад: {pricing}_{price}_PL. {status}.".replace(",     "," ").replace("     ","").replace("    .",".").replace("   .",".").replace("  .",".").replace(" .",".").replace(",  ",", ")
                    
    text_drom = f'{name_zap1} {marka} {model} {version} {year}г.в., {fuel}, {volume}, {car_body}.' \
                f'Будьте готовы назвать АРТИКУЛ: D-{artical}.{num_zap} Склад: {pricing}_{price}_PL. {status}. ' \
                'Задавайте, пожалуйста, вопросы непосредственно перед заключением сделки, остатки меняются ежедневно. ' \
                'Доставку осуществляем ТК сразу в ваш город. Срок доставки до Москвы 2-4 дня, бывают исключения,' \
                'где сроки доставки могут увеличиться. Состояние вы оцениваете сами, по предоставленным фотографиям). ' \
                'Если деталь не понадобилась - возврат не рассматривается! По VIN автомобиля запчасти не подбираем, ' \
                f'строго по заводскому номеру, указанному на детали. С Уважением, компания REPPART!'.replace(",     "," ").replace("     ","").replace("    .",".").replace("   .",".").replace("  .",".").replace(" .",".").replace(",  ",", ")
    file = open(f"{input_name}_zzap.csv", "a", encoding="utf-8", newline='')
    writer = csv.writer(file)

    writer.writerow(
        (
            proizvoditel,
            num_zap,
            name_zap1,
            text_zzap,
            price,
            status,
            "10-14 дня",
            foto,
            href_card,                                  
        )
    )
    file.close()

    file = open(f"{input_name}_drom.csv", "a", encoding="utf-8", newline='')
    writer = csv.writer(file)

    writer.writerow(
        (
            f"АРТИКУЛ: D-{artical}",
            name_zap1,
            status,
            marka,
            model,
            version,
            num_zap,
            volume,
            year,
            "",
            "",
            "",
            "",
            text_drom,
            "1",
            price,
            "под заказ",
            "10-14 дня",
            foto,
            href_card,
            marka_and_model_and_num_zap,                                   
        )
    )
    file.close()
    return(marka, model, year, version, zamena, ka4estvo, number_lot, price, nomer, side, prouzbod_text, status)

with open(f"first.html", "w", encoding="utf-8") as file:
    file.write(driver.page_source)

with open(f"first.html", encoding="utf-8") as file:
    src = file.read()
soup = BeautifulSoup(src, 'html.parser')
href_first_page = soup.find_all("div", class_="categories-item__header")

zapchast_and_href = {}
two_zapchast_and_href = {}
list_two_zapchast_and_href = {}
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
    list_two_zapchast_and_href[href_second] = name_href_second
    number += 1

with open("second_href.json", "a", encoding="utf-8") as file:
    json.dump(two_zapchast_and_href, file, indent=4, ensure_ascii=False)

with open("three_href.json", "a", encoding="utf-8") as file:
    json.dump(list_two_zapchast_and_href, file, indent=4, ensure_ascii=False)

input_number_second = int(input("Введи номер подраздела(в последней части), который тебя интересует -  "))

with open("second_href.json", encoding="utf-8") as file:
    second_pars = json.load(file)
#print(input_number_second)
for last_categoria, num_2 in second_pars.items():
    #print(input_number_second, num_2)
    if input_number_second == int(num_2):
        print(f"Ты выбрал категорию {last_categoria}")
        url_1 = last_categoria
for url_categoria, name_href_2 in list_two_zapchast_and_href.items():
    if url_1 == url_categoria:
        name_zap = name_href_2
os.remove("first.html")
os.remove("first_href.json")
os.remove("second_href.json")
os.remove("three_href.json")

for page in range(1,200):
    url = url_1 + f"{page}/"
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
        print(href_part)
        pars_card(href_part, name_zap)

os.remove("three.html")
os.remove("one_part.html")




#a = input("Введи любое число, чтобы закончить - ")
