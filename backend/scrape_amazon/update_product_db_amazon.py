from scrape_objects_MVP import get_attributes, get_id
from pymongo import MongoClient
import os

DB_URL = os.environ['DB_URL']
CLIENT = MongoClient(DB_URL)
DB = CLIENT.compurator
PRODUCTS_COLLECTION = DB["products"]


def check_product_exists(url):
    '''
    :param url: url of amazon product
    :return: boolean of whether or not product already exists in products_collection
    '''
    p_id = get_id(url)

    if PRODUCTS_COLLECTION.find({'p_id': p_id}) is not None:
        return True
    return False


def add_product_amazon(url):
    '''
    :param PRODUCTS_COLLECTION, url:
    :return prod_document: dictionary containing attributes of product on amazon
    '''

    prod_document = get_attributes(url)
    PRODUCTS_COLLECTION.insert_one(prod_document)

    return prod_document
