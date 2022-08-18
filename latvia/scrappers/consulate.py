import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


def get_consulate_info():
    url = 'https://www2.mfa.gov.lv/ru/vitebsk'
    req = requests.get(url)
    src = req.text
    soup = BeautifulSoup(src, 'html.parser')


    info_table = soup.find('div', class_='fulltext').find('table').find('tbody').find_all('tr')
    values = []
    for item in info_table:
        value = item.find_next('td').find_next('td').get_text().strip().replace('\n', '').replace('  ', '')
        values.append(value)

    consulate_info={}
    address = values[0]
    phone = values[1].replace(u'\xa0', u' ')
    time = values[3].split('(')[0].capitalize()

    #getting email
    website = 'https://www2.mfa.gov.lv/ru/vitebsk'
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(website)
    driver.maximize_window()
    driver.implicitly_wait(2)


    rows = driver.find_element(by=By.XPATH, value='//*[@id="main-content"]/div/div[2]/div[3]/div/div[2]/div/div/div[2]/table[1]/tbody/tr[3]/td[2]/p[1]/a/span/span')
    email = rows.text

    consulate_dict = {'country': 'Latvia', 'address': address, 'email': email, 'telephone1': phone, 'worktime': time}
    consulate = []
    consulate.append(consulate_dict)
    print(consulate)
    return consulate


def spark_consulate(dict):
    from pyspark.sql import SparkSession
    from pyspark.sql.functions import regexp_replace, col
    spark = SparkSession.builder.appName('consulate').getOrCreate()
    dataframe = spark.createDataFrame(data=dict)
    dataframe = dataframe.withColumn('telephone1', regexp_replace(col("telephone1"), " ", ""))
    dataframe = dataframe.withColumn('address', dataframe['address'].substr(28, 35))
    dataframe = dataframe.withColumn('city', dataframe['address'])
    dataframe = dataframe.withColumn('city', dataframe['city'].substr(1, 8))
    dataframe = dataframe.withColumn('city', regexp_replace(col("city"), " ", ""))
    dataframe.show(truncate=False)
    dataframe = dataframe.toPandas()
    res = dataframe.to_dict(orient='records')
    print(res)
    return res