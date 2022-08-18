from bs4 import BeautifulSoup
import requests
from lxml import html

res = requests.get('https://pony-visa.by/ru/contacts', headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'})

soup = BeautifulSoup(res.text, 'lxml')

def get_minsk_visaac():
    # Minsk visaac
    adress_minsk = soup.find("h5").find_next('p').find_next('p').text
    #phone_number_minsk = soup.find("h4").find_next_sibling('p').find_next('span').find_next('a').text
    issue_worktime = soup.find_all("p")[13].text
    apply_worktime = soup.find_all("p")[15].text
    telephone1 = soup.find('h4').find_next_sibling('p').find_next('span').find_next('a').text
    visaac1_info = {'country': 'Latvia', 'address': adress_minsk, 'issue_worktime': issue_worktime,
               'apply_worktime': apply_worktime, 'telephone1': telephone1}
    visaac1 = []
    visaac1.append(visaac1_info)
    return visaac1

def get_vitebsk_visaac():
    # Vitebsk visaac
    address_vitebsk = soup.find("h5").find_next('p').find_next('p').find_next('p').text
    telephone2 = soup.find('h4').find_next_sibling('p').find_next('span').find_next('a').find_next_sibling('a').text
    issue_worktime = soup.find_all("p")[13].text
    apply_worktime = soup.find_all("p")[15].text
    visaac2_info = {'country': 'Latvia', 'address': address_vitebsk, 'issue_worktime': issue_worktime,
                    'apply_worktime': apply_worktime, 'telephone1': telephone2}
    visaac2 = []
    visaac2.append(visaac2_info)
    return visaac2


def spark_visaac(dict):
    from pyspark.sql import SparkSession
    from pyspark.sql.functions import regexp_replace, split, concat, col, lit

    spark = SparkSession.builder.appName('visa_centers').getOrCreate()
    dataframe = spark.createDataFrame(data=dict)
    dataframe = dataframe.withColumn('telephone1', regexp_replace(col("telephone1"), " ", ""))
    dataframe = dataframe.withColumn('address', regexp_replace(col("address"), " ", ""))
    dataframe = dataframe.withColumn('city', split(dataframe['address'], ',').getItem(0))
    dataframe = dataframe.toPandas()
    res = dataframe.to_dict(orient='records')
    print(res)
    return res

