LINK = 'https://d2ab400qlgxn2g.cloudfront.net/dev/spaces/xxg4p8gt3sg6/environments/master/entries'

headers = {
    'Host': 'd2ab400qlgxn2g.cloudfront.net',
    'Sec-Ch-Ua': '"(Not(A:Brand";v="8", "Chromium";v="99"',
    'Accept': 'application/json, text/plain, */*',
    'Authorization': 'Bearer 5YpTBRikGN59YHwM18CyGr5F43bFuaak9U8FSMEDmb8',
    'Sec-Ch-Ua-Mobile': '?0',
    'X-Contentful-User-Agent': 'sdk contentful.js/0.0.0-determined-by-semantic-release; platform browser; os Windows;',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36',
    'Sec-Ch-Ua-Platform': '"Windows"',
    'Origin': 'https://visa.vfsglobal.com',
    'Sec-Fetch-Site': 'cross-site',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://visa.vfsglobal.com/',
    # 'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
}

address_params = {
    'content_type': 'resourceGroup',
    'fields.locale': 'vfs&ru&ltu&ltu > ru&ltu > blr&ltu > blr > ru',
    'limit': '500',
}


time_params = {
    'content_type': 'countryLocation',
    'fields.title[match]': 'ltu > blr > ru',
    'order': 'fields.vacName',
    'limit': '200',
}

news_params_1 = {
    'content_type': 'countryNews',
    'fields.locale': 'ltu > blr > ru&ltu > ru',
    'sys.updatedAt[gte]': '2022-05-11T21:00:00.000Z',
}

news_params_2 = {
    'content_type': 'countryNews',
    'fields.locale': 'ltu > blr > ru&ltu > ru',
    'fields.permanent': 'true',
}
