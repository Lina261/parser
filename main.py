import argparse
import json
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup as bs

parser = argparse.ArgumentParser()

URL = 'https://shop.green-market.by/api/v1/products/search/'
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/90.0.4430.212 Safari/537.36',
}

ERROR = "Error! Something went wrong..."


def get_search_response(url, params=None):
    try:
        response = requests.get(url, headers=HEADERS, params=params)
        if response.ok:
            return response
        else:
            return ERROR
    except (requests.ConnectionError, requests.Timeout):
        print("Check your internet connection!")


def get_product_id(details):
    id_list = []
    for item in details:
        id_list.append(item.get('id'))
    return id_list


def get_info(product_id):
    url = urljoin('https://shop.green-market.by/product/', str(product_id))
    response = get_search_response(url)
    if response:
        page_info = get_search_response(url).text
        soup = bs(page_info, 'html.parser')
        info = {}
        name = soup.find('h2', class_="product-modal_productTitle__2Hyco")
        price = soup.find('span', class_="product-modal_productValue__jTrwS")
        items = soup.findAll('li', class_="product-modal_infoItem__3TCs0")
        info['Название'] = name.text
        info['Цена в рублях'] = price.text
        for item in items:
            info[f'{item.contents[0].contents[0].text}'] = item.contents[1].contents[0]
        print(info)
        return info


def parse():
    parser.add_argument("--json", nargs='?', const="results.json")
    parser.add_argument("-q", "--query", required=True)
    title = parser.parse_args().query
    file = parser.parse_args().json
    params = {
        'search': title,
        'storeId': 2
    }
    response = get_search_response(URL, params)
    if response:
        data_json = response.json()
        if not data_json:
            print("No search results")
        elif response != ERROR:
            product_ids = get_product_id(data_json)
            if len(product_ids) > 1:
                print("Found more than one product with the same name")
            a = list(map(get_info, product_ids))
        if file:
            with open(file, "w", encoding='utf-8') as f:
                data = json.dumps(a, sort_keys=False, indent=4, ensure_ascii=False, separators=(',', ': '))
                f.write(data)
        return response


if __name__ == "__main__":
    parse()
