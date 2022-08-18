from bs4 import BeautifulSoup
import requests
import re


"""Consulate data scrap."""


def get_all_data_from_consulate_site():
    url = "http://thaiconsul.by/contact-us/"
    page = requests.get(url)
    allNews = []
    soup = BeautifulSoup(page.text, "html.parser")
    allNews = soup.findAll("div", class_="content-container")
    contacts = dict()
    list_phones = []
    for line in allNews:
        for word in line.text.split():
            if "@" in word:
                contacts["email"] = word
        for line_new in line.text.split("\n"):
            if "ул" in line_new:
                contacts["adress"] = line_new
    list_phones.append(
        re.findall("\+?[\d]{3}..[\d]{2}..[\d]{3}.[\d]{4}", str(allNews))[1]
    )
    list_phones.append(
        re.findall("\+?[\d]{3}..[\d]{2}..[\d]{3}.[\d]{4}", str(allNews))[2]
    )

    work_hours = ""
    work_hours_tags = soup.findAll("p", attrs={"style": "text-align: center;"})
    for i in work_hours_tags:
        if "Пн" in i.text:
            work_hours = i.text

    contacts["phone"] = list_phones
    data = dict()
    data["ADRESS"] = contacts["adress"]
    data["EMAIL"] = contacts["email"]
    data["WORKING_HOURS"] = work_hours
    data["PHONE_NUMBER_1"] = contacts["phone"][0]
    data["PHONE_NUMBER_2"] = contacts["phone"][1]
    return data


"""Visa-center data scrap."""


def get_email_and_phone_from_vfs(html):
    soup = BeautifulSoup(html, "html.parser")
    allNews = soup.findAll("div", class_="renderer-content")
    contacts = dict()

    for line in allNews:
        for word in line.text.split():
            if "@" in word:
                contacts["email"] = word
    phone = re.findall(r"\+?[\d]{3}.[\d]{2}.[\d]{3}.[\d]{2}.[\d]{2}", str(allNews))[0]
    contacts["phone"] = phone
    return contacts


def get_content_from_vfs_page(data):
    raw_news = data.find("div", class_="renderer-content")
    news = []
    for ns in raw_news.contents:
        ns_str = ns.contents[0]

        for symb in ["\r", "\n"]:
            ns_str = ns_str.replace(symb, "")
        news.append(" " + ns_str)

    news = "".join(news)
    return news


def get_adress(page):
    data = []
    soup = BeautifulSoup(page, "html.parser")
    for i in ["section_1", "section_2"]:
        news = soup.find(id=i)
        d = get_content_from_vfs_page(news)

        if "улица" in d:
            d = "улица" + d.split("улица")[1]
            d = d.replace(" Минск, Беларусь,", "")

        data.append(d)
    return data


def get_time_from_vfs(page):
    soup = BeautifulSoup(page, "html.parser")
    data_raw = soup.find_all("td", class_="attend-center-td")
    time = []
    for data in data_raw:
        s = data.contents[0]
        s = s[25:]
        s = s.split("\n")[0]
        time.append(s)

    time_s = []
    time_s.append(", ".join(time[1:3]))
    time_s.append(", ".join(time[4:]))
    return time_s


def get_all_data_from_fvs(loader):
    data = {}
    html_for_adress_info_time = loader.load_page(
        "https://visa.vfsglobal.com/blr/ru/tha/attend-centre/Minsk"
    )
    html_for_email_and_phone = loader.load_page(
        "https://visa.vfsglobal.com/blr/ru/tha/contact-us"
    )
    msgs = get_adress(html_for_adress_info_time)
    contacts = get_email_and_phone_from_vfs(html_for_email_and_phone)
    data["ADRESS"] = "г. Минск " + msgs[1]
    data["EMAIL"] = contacts["email"]
    data["APPLY_WORKING_HOURS"] = get_time_from_vfs(html_for_adress_info_time)[0]
    data["ISSUE_WORKING_HOURS"] = get_time_from_vfs(html_for_adress_info_time)[1]
    data["PHONE_NUMBER"] = contacts["phone"]
    return data


"""News scrappers."""


def get_news_links(page):
    soup = BeautifulSoup(page, "html.parser")
    data = soup.find_all("a", class_="news-link")

    news_links = []

    for link in data:
        news_links.append("https://visa.vfsglobal.com{}".format(link.get("href")))
    return news_links


def get_date_and_news(page):
    soup = BeautifulSoup(page, "html.parser")
    raw_date = soup.find("h5", class_="news-date")
    date = raw_date.contents[0]
    date = re.search("\d*\s\w*\s\d{4}", date)[0]
    raw_news = soup.find("div", class_="renderer-content")
    news = []
    for ns in raw_news.contents:
        ns_str = ns.contents[0]

        for symb in ["\r", "\n"]:
            ns_str = ns_str.replace(symb, "")

        news.append(" " + ns_str)

        if ns.find("a"):
            href = ns.find("a").get("href")
            if "mailto:" in href:
                href = href.replace("mailto:", "")
            news.append(" " + href)

    news = "".join(news)
    return date, news


RU_MONTH_VALUES = {
    "января": "01",
    "февраля": "02",
    "марта": "03",
    "апреля": "04",
    "мая": "05",
    "июня": "06",
    "июля": "07",
    "августа": "08",
    "сентября": "09",
    "октября": 10,
    "ноября": 11,
    "декабря": 12,
}


def convert_date(date_str):
    updated_date = str()
    try:
        int(date_str[0])
        int(date_str[1])
        updated_date = date_str
    except:
        new_date = "0" + date_str
        updated_date = new_date
    finally:
        for k, v in RU_MONTH_VALUES.items():
            updated_date = updated_date.replace(k, str(v))

        d = updated_date.split(" ")[::-1]
        s = "-".join(d)
        return s


def get_all_news(loader):
    main_page = loader.load_page("https://visa.vfsglobal.com/blr/ru/tha")
    news_links = get_news_links(main_page)
    data = []
    for link in news_links:
        page = loader.load_page(link)
        date, news = get_date_and_news(page)
        date = convert_date(date)
        one_news = {
            "TITLE": news[:66] + " ...",
            "BODY": news[:250],
            "LINK": link,
            "DATE": date,
        }
        data.append(one_news)
    return data
