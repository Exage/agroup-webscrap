from pymongo.mongo_client import MongoClient
import datetime

url = 'mongodb://localhost:27017'

client = MongoClient(url)
db = client['agroupdb']
collection_products = db['products']
collection_date = db['date']

def get_last_parsing_date():
    return collection_date.find_one(sort=[('_id', -1)])

def get_parsing_dates():
    return [date for date in collection_date.find({})]

def get_products_by_number(parsing_number):
    return [product for product in collection_products.find({ 'parsing_number': parsing_number })]

def add_products_to_db(items):
    date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    products_in_catalog = items[0]
    last_parsing = get_last_parsing_date()

    if last_parsing:
        parsing_number = last_parsing['parsing_number'] + 1
    else:
        parsing_number = 1

    products = items[1]

    collection_date.insert_one({ 
        'date': date, 
        'parsing_number': parsing_number,
        'products_in_catalog': len(products)
    })

    for product in products:
        product['parsing_number'] = parsing_number

    collection_products.insert_many(products)