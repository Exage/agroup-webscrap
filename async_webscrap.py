import aiohttp
import asyncio
from bs4 import BeautifulSoup

import json
import datetime

from add_to_db import add_products_to_db
from urls import url_main

async def fetch_page(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, ssl=False) as response:
            return await response.text()

async def parse_page(html):
    soup = BeautifulSoup(html, 'html.parser')
    
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

async def main(urls):

    catalog = ['', []]

    for _, url in enumerate(urls):
        html = await fetch_page(url)
        items = await parse_page(html)

        if not catalog[0]:
            catalog[0] = items[0]['count']

        catalog[1].extend(items[1])

    add_products_to_db(catalog)

def run_async(urls):
    asyncio.run(main(urls))