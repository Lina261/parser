import argparse
import json
import pickle
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup as bs


parser = argparse.ArgumentParser()
parser.add_argument("--json", nargs='?', const="results.json")
parser.add_argument("-q", "--query", required=True)
title = parser.parse_args().__getattribute__("query")
file = parser.parse_args().__getattribute__("json")

URL = 'https://shop.green-market.by/api/v1/products/search/'
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/90.0.4430.212 Safari/537.36',
}

params = {
    'search': title,
    'storeId': 2
}

error = "Возникла ошибка!"


def get_product(url):
    try:
        response = requests.get(url, headers=HEADERS, params=params)
        if response.ok:
            return response
        else:
            return error
    except Exception:
        print('Что-то пошло не так :(')


def get_product_id(data):
    details = data.json()
    id_list = []
    for item in range(len(details)):
        id_list.append(details[item]['id'])
    print(id_list)
    return id_list


def get_info(product_id):
    url = urljoin('https://shop.green-market.by/product/', str(product_id))
    page_info = requests.get(url).text
    soup = bs(page_info, 'html.parser')
    info = {}
    item_count = len(soup.findAll('li', class_="product-modal_infoItem__3TCs0"))
    name = soup.find('h2', class_="product-modal_productTitle__2Hyco")
    price = soup.find('span', class_="product-modal_productValue__jTrwS")
    info['Название'] = name.text
    info['Цена в рублях'] = price.text
    info['Масса'] = \
        soup.find('ul', class_="product-modal_infoList__2ToS2").contents[item_count - 1].contents[1].contents[0]
    info['Производитель'] = \
        soup.find('ul', class_="product-modal_infoList__2ToS2").contents[item_count - 2].contents[1].contents[0]
    info['Артикул'] = \
        soup.find('ul', class_="product-modal_infoList__2ToS2").contents[item_count - 3].contents[1].contents[0]
    print(info)
    return info



def parse():
    response = get_product(URL)
    if len(response.json()) == 0:
        print("Товаров по вашему запросу не найдено")
    elif response != error:
        product_ids = get_product_id(response)
        if len(product_ids) > 1:
            print("Найдено более одного товара с таким названием")
        a = list(map(get_info, product_ids))
        if file:
            with open(file, "w", encoding='utf-8') as f:
                data = json.dumps(a, sort_keys=False, indent=4, ensure_ascii=False, separators=(',', ': '))
                f.write(data)
        return response
    else:
        print("К сожалению, возникли ошибки :(")


parse()
