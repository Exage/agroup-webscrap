from bs4 import BeautifulSoup
import requests

import json
import datetime

from add_to_db import add_products_to_db
from urls import url_main

def parse_page(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    catalog = soup.find('v-catalog')
    catalog_dict = json.loads(catalog.get(':static-data-source'))['catalog']
    catalog_pages = catalog_dict['pages']
    catalog_items = catalog_dict['items']

    items = []

    for item in catalog_items:

        name = item['name'].replace('Ноутбук', '').replace('Игровой', '').replace('ноутбук', '').strip()
        images = { key: url_main + value for key, value in item['images'][0].items() }
        price = item['price']
        params = item['params']
        link = url_main + item['link']

        items.append({ 'name': name, 'images': images, 'price': price, 'params': params, 'link': link })

    return [catalog_pages, items]

def main(urls):

    catalog = ['', []]

    for _, url in enumerate(urls):
        items = parse_page(url)

        if not catalog[0]:
            catalog[0] = items[0]['count']

        catalog[1].extend(items[1])

    with open('result.txt', 'w') as file:
        file.write(str(catalog))

    add_products_to_db(catalog)

def run_sync(urls):
    main(urls)