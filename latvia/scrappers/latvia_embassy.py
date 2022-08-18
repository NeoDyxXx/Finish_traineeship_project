import requests, json
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By


def get_embassy_info():
    url_time_of_work = "https://www2.mfa.gov.lv/ru/belarus/posolstvo/vremya-raboty"
    url = "https://www2.mfa.gov.lv/ru/belarus"

    headers = {
    'Accept': '*/*',
    'User-agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)\
    Chrome/98.0.4758.102 Safari/537.36"
    }

    req_time_of_work = requests.get(url_time_of_work, headers=headers)
    src_time_of_work = req_time_of_work.text

    req = requests.get(url, headers=headers)
    src = req.text

    with open('embassy_information_time_of_work.html', 'w', encoding='utf-8') as file:
        soup = BeautifulSoup(src_time_of_work, 'lxml')
        file.write(soup.prettify())
    with open('embassy_information.html', 'w', encoding='utf-8') as file:
        soup = BeautifulSoup(src, 'lxml')
        file.write(soup.prettify())

    with open('embassy_information.html', 'r', encoding='utf-8') as file:
        src = file.read()
    with open('embassy_information_time_of_work.html', 'r', encoding='utf-8') as file_time_of_work:
        src_time_of_work = file_time_of_work.read()
    soup = BeautifulSoup(src, 'lxml').find('div', class_='fulltext')

    # address = soup.find_all('td')[1].get_text().strip().partition('(')[0]
    phone_number = soup.find_all('td')[4].find('span', class_="baec5a81-e4d6-4674-97f3-e9220f0136c1").get_text().strip()
    #email = soup.find_all('td')[8].find('p').get_text().strip()
    time_of_work = str(BeautifulSoup(src_time_of_work, 'lxml').find_all('p')[1].get_text().strip())+' '+str(BeautifulSoup(src_time_of_work, 'lxml').find_all('p')[2].get_text().strip())
    news_title = [i.get_text().strip() for i in BeautifulSoup(src, 'lxml').find_all('a', class_="title")]
    news_content = [i.get('href') for i in BeautifulSoup(src, 'lxml').find_all('a', class_="title")]
    #news = {i:j for i in news_title for j in news_content}

    news = []
    for i in news_title:
        j = 0
        news.append({'title': i, 'link': news_content[j]})
        j += 1

    #getting email via selenium
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager


    website = 'https://www2.mfa.gov.lv/ru/belarus'
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(website)
    driver.maximize_window()
    driver.implicitly_wait(2)

    addr = driver.find_element(by=By.XPATH, value='//*[@id="main-content"]/div/div[2]/div[3]/div/div[2]/div/div/div[2]/table[1]/tbody/tr[1]/td[2]')
    address = addr.text
    em = driver.find_element(by=By.XPATH, value='//*[@id="main-content"]/div/div[2]/div[3]/div/div[2]/div/div/div[2]/table[1]/tbody/tr[4]/td[2]')
    email = em.text

    embassy = {'country': 'Latvia', 'address': address, 'phone': phone_number, 'email': email, 'worktime': time_of_work, 'news': news}
    embassy_information = []
    embassy_information.append(embassy)
    print(embassy_information)
    return embassy_information

def spark_embassy(dict):
    from pyspark.sql import SparkSession
    from pyspark.sql.functions import regexp_replace, col, split
    from pyspark.sql.functions import concat, col, lit
    from pyspark.sql import functions as sf
    spark = SparkSession.builder.appName('embassy').getOrCreate()
    from pyspark.sql.types import StructType, StructField, StringType
    schema = StructType([StructField("address", StringType(), True), StructField("phone", StringType(), True),\
            StructField("country", StringType(), True), StructField("email", StringType(), True),\
            StructField("worktime", StringType(), True)])

    dataframe = spark.createDataFrame(data=dict, schema=schema)

    dataframe = dataframe.withColumn('street', split(dataframe['address'], ',').getItem(0)) \
        .withColumn('city', split(dataframe['address'], ',').getItem(1)) \
        .withColumn('country addr', split(dataframe['address'], ',').getItem(2))
    dataframe = dataframe.drop(col("address"))
    dataframe = dataframe.withColumn('building', split(dataframe['street'], ' ').getItem(2))
    dataframe = dataframe.withColumn('street', dataframe['street'].substr(0, 14))
    dataframe = dataframe.withColumn('city', dataframe['city'].substr(1, 6))
    dataframe = dataframe.withColumn('city', regexp_replace(col("city"), " ", ""))
    dataframe = dataframe.withColumn('address',
                       sf.concat(sf.col('city'), sf.lit(','), sf.col('street')))
    dataframe = dataframe.withColumn('address',
                                     sf.concat(sf.col('address'), sf.lit(','), sf.col('building')))
    dataframe = dataframe.drop(col("street"))
    dataframe = dataframe.drop(col("country addr"))
    dataframe = dataframe.drop(col("building"))

    dataframe = dataframe.withColumn('phone', regexp_replace(col("phone"), " ", ""))
    dataframe.show(truncate=False)
    dataframe = dataframe.toPandas()
    res = dataframe.to_dict(orient='records')
    print(res)
    return res