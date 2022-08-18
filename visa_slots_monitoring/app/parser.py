import time
import schedule
import requests
from elasticsearch import Elasticsearch
from regist_data import EMAIL, PASSWORD
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import json
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import psycopg2


def check_connection():
    while True:
        try:
            es = Elasticsearch([{'host': 'elasticsearch', 'port': 9200, 'scheme': "http"}])
            return
        except Exception as e:
            print('Elasticsearch is not connection')
            print(e)
            time.sleep(5)
            continue


countresURL = {
    'Poland': 'pol',  #  1 Работал, но перестал, без поняти, что случилось
    'Latvia': 'lva',  #  2 Нет для нашей страны
    'Lithuania': 'ltu',# 3 работает, но мест для записи небыло ни разу
    'Spain': '-',  #     4 вообще без понятия
    'Norway': 'nor',  #  5 запись только по электронной почте
    'Thailand': 'tha', # 6 запись только по электронной почте
    'Austria': 'aut',
}


def check_index_exist(es, index_name):
    res = es.indices.exists(index=index_name)
    return res


def write_to_es(vac, category, sub_category, appointment, county):
    es = Elasticsearch([{'host': 'elasticsearch', 'port': 9200, 'scheme': "http"}])
    if not check_index_exist(es, "appointment"):
        return "Table is not exist"

    q = {
        "bool": {
            "must": [
                
                {"match" : {"country": county}},
                {"match" : {"address": vac}},
                {"match" : {"category": category}},
                {"match" : {"subcategory": sub_category}}
            ]
        }
    }

    res = es.search(index="appointment",query=q)#['hits']['total']['value']#['hits'][0]['_id']
    
    if res['hits']['total']['value'] == 0:
        es.index(
            index="appointment", 
            document={
                "country": county,
                "address": vac,
                "category": category,
                "subcategory": sub_category,
                "appointment": appointment
            })
        time.sleep(1)
        
    else:
        res_id = res['hits']['hits'][0]['_id']
        doc_up = {
            "appointment": appointment,
        }

        es.update(index='appointment', id=res_id, doc=doc_up)
        time.sleep(1)


def delete_doc(vac, category, sub_category, appointment, county):
    es = Elasticsearch([{'host': 'elasticsearch', 'port': 9200, 'scheme': "http"}])
    if not check_index_exist(es, "appointment"):
        return "Table is not exist"

    q = {
        "bool": {
            "must": [
                
                {"match" : {"country": county}},
                {"match" : {"address": vac}},
                {"match" : {"category": category}},
                {"match" : {"subcategory": sub_category}}
            ]
        }
    }

    res = es.search(index="appointment",query=q)#['hits']['total']['value']#['hits'][0]['_id']
    
    if res['hits']['total']['value'] == 0:
        return
    
    else:
        res_id = res['hits']['hits'][0]['_id']
        doc_up = {
            "appointment": appointment,
        }

        es.delete(index='appointment', id=res_id)
        time.sleep(1)


def conversion(sec):
    sec_val = sec % (24 * 3600)  # Number of seconds
    hour_val = sec_val // 3600  # Number of hours
    sec_val %= 3600
    min_val = sec_val // 60  # Number of minutes
    sec_val %= 60
    print(hour_val, "hours", min_val, "minutes", sec_val, "seconds")


def timer(sec):
    while not sec == 0:
        conversion(sec)
        time.sleep(1)
        sec -= 1
        if sec == 0:
            break


def check_exists_by_class(driver, by_class):
    try:
        driver.find_element(By.CLASS_NAME, by_class)
    except:
        return False
    return True


def vfs_login(driver):
    login = driver.find_elements(By.CLASS_NAME, 'mat-input-element')  # Найхожу поля ввода данных
    login[0].send_keys(EMAIL)  # EMAIL
    login[1].send_keys(PASSWORD)  # PASSWORD
    driver.find_elements(By.CLASS_NAME, 'mat-focus-indicator')[1].click()  # Клик по кнопке "Войти"

    # Check for error 429 (too many requests to the site)

    while check_exists_by_class(driver, 'c-brand-blue'):
        url_login = 'https://lift-api.vfsglobal.com/user/login'
        resp = requests.post(url_login)
        if resp.status_code == 429:
            timer(int(resp.headers['retry-after']))
        else:
            print("Нужно подождать сутьсуть. Ошибка:{}".format(resp.status_code))
            timer(10)
        driver.find_elements(By.CLASS_NAME, 'mat-focus-indicator')[1].click()  # Клик по кнопке "Войти"


def get_visa_date(country, home='blr'):
    wait_sec = 5
    options = webdriver.FirefoxOptions()
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.517 Safari/537.36'
    options.add_argument(f'user-agent={user_agent}')

    driver = webdriver.Remote(
        "http://selenium:4444", options=options
    )
    #options.headless = True

    URL = 'https://visa.vfsglobal.com/{}/ru/{}/login'.format(home, countresURL[country])
    driver.get(URL)  # Страница аутентификации
    driver.implicitly_wait(10)
    time.sleep(5)
    # login and password input
    #login = driver.find_elements(By.CLASS_NAME, 'mat-input-element')  # Найхожу поля ввода данных
    #login[0].send_keys(EMAIL)  # EMAIL
    #login[1].send_keys(PASSWORD)  # PASSWORD
    #driver.find_elements(By.CLASS_NAME, 'mat-focus-indicator')[1].click()  # Клик по кнопке "Войти"
    vfs_login(driver)
    # Check for error 429 (too many requests to the site)
    if check_exists_by_class(driver, 'c-brand-blue'):
        url_login = 'https://lift-api.vfsglobal.com/user/login'
        resp = requests.post(url_login)
        try:
            timer(int(resp.headers['retry-after']))
        except:
            timer(30)
        driver.find_elements(By.CLASS_NAME, 'mat-focus-indicator')[1].click()  # Клик по кнопке "Войти"

    entry_butt = driver.find_elements(By.CLASS_NAME, 'mat-focus-indicator')[0]
    driver.execute_script("arguments[0].click();", entry_butt)  # Клик по кнопке "Записаться"

    butt_vis = driver.find_elements(By.CLASS_NAME, 'mat-form-field-infix')

    time.sleep(wait_sec)
    driver.execute_script("arguments[0].click();", butt_vis[0])  # Клик по полю выбора визовых центров

    visa_cent_list = driver.find_elements(By.CLASS_NAME, 'mat-option-text')
    visa_cent_text = []  # Массив всех визовых центров
    for i in visa_cent_list:
        visa_cent_text.append(i.text)
    list_result = ''  # Строка с данными

    for visa_cent_iter in range(len(visa_cent_list)):
        driver.execute_script("arguments[0].click();", visa_cent_list[visa_cent_iter])  # Клик по визовому центру

        time.sleep(wait_sec)
        driver.execute_script("arguments[0].click();", butt_vis[1])  # Клик по полю выбора категории записи

        visa_cat_list = driver.find_elements(By.CLASS_NAME, 'mat-option-text')
        visa_cat_text = []  # Массив категорий записи
        for i in visa_cat_list:
            visa_cat_text.append(i.text)

        for visa_cat_iter in range(len(visa_cat_list)):

            driver.execute_script("arguments[0].click();", visa_cat_list[visa_cat_iter])  # Клик по категории записи

            time.sleep(wait_sec)
            driver.execute_script("arguments[0].click();", butt_vis[2])  # Клик по полю выбора подкатегории записи

            visa_subcategory_list = driver.find_elements(By.CLASS_NAME, 'mat-option-text')
            visa_subcategory_text = []  # Массив подкаегорий записи
            for i in visa_subcategory_list:
                visa_subcategory_text.append(i.text)

            for visa_subcategory_iter in range(len(visa_subcategory_list)):

                driver.execute_script("arguments[0].click();", visa_subcategory_list[visa_subcategory_iter])  # Клик по подкатегории записи

                try:
                    result = driver.find_element(By.CLASS_NAME, 'border-info')  # Нужное нам поле с данными о наличии записи
                except:
                    visa_cat_iter -= 1
                    time.sleep(5)
                    break
                
                if result.text != 'В настоящее время нет свободных мест для записи':
                    res = result.text
                    res = res.split(':')
                    res = res[1].strip().replace('/','-')
                    #res = "to_timestamp('{}', 'dd-mm-yyyy')".format(res)
                    
                    write_to_es(
                        visa_cent_text[visa_cent_iter],
                        visa_cat_text[visa_cat_iter],
                        visa_subcategory_text[visa_subcategory_iter],
                        res,
                        country
                    )



                driver.execute_script("arguments[0].click();", butt_vis[2])  # Клик по полю выбора визовых центров
            driver.execute_script("arguments[0].click();", butt_vis[1])  # Клик по полю выбора категории записи
        driver.execute_script("arguments[0].click();", butt_vis[0])  # Клик по полю выбора подкатегории записи
    driver.quit()


def perform_every_day():
    Aut = get_visa_date("Austria", home='kaz')
    Lit = get_visa_date("Lithuania")


if __name__ == '__main__':
    check_connection()
    perform_every_day()

    schedule.every().day.at("15:00").do(perform_every_day)  # получение данных кажды день в 8:00
    while True:
        schedule.run_pending()
        time.sleep(60)
