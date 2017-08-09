"""
The script identifies new items in the website inventory and saves them to the
database. Items already in the database will be ignored. In-depth details for
items will be scrapped with another script.

Information captured about items:
- name
- imageUrl
- productUrl

@author: eriel marimon
@created: july 1, 2017
@updated: july 4, 2017
"""

import sys
sys.path.append("..")

from ProductRepository import BjsProductRepository
from PageIdentifier import BjsPageWizard

import BjsUtil

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import json
import time
import os


LOGFILE = ("%s.log" % (os.path.basename(__file__))).replace(".py","")

def get_items_from_store_website(driver, wizard, category, url):
    driver.get(url)

    category_name_element_xapth = '//*[@id="listing-container"]/div[1]/section/header/h1'
    try:
        category_name_element = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.XPATH, category_name_element_xapth))
        )
    except TimeoutException, e:
        message = "Cant find category=%s at url=%s" % (category, url)
        BjsUtil.log(LOGFILE, BjsUtil.LOG_ERROR, message, console_out=True)
        return

    soup = BeautifulSoup(driver.page_source, "html.parser")
    
    products = []


    if category_name_element.text != category:
        """Log warning message that names mismatched"""
        message = "Mismatch in category=%s and url=%s" % (category, url)
        BjsUtil.log(LOGFILE, BjsUtil.LOG_WARN, message, console_out=True)

    elif wizard.is_product_page(soup):
        """Get products on this page"""
        message = "Category=%s is a product page with url=%s." % (category, url)
        BjsUtil.log(LOGFILE, BjsUtil.LOG_INFO, message, console_out=True)

        return wizard.get_partial_products(soup)

    elif wizard.is_categories_page(soup):
        """Get categories on this page and recurse"""
        message = "Category=%s is a categories page with url=%s." % (category, url)
        BjsUtil.log(LOGFILE, BjsUtil.LOG_INFO, message, console_out=True)

        category_map = wizard.map_categories_to_urls(soup)
        products = []
        for key in category_map:
            products += get_items_from_store_website(driver, wizard, key, category_map[key])
        return products
    else:
        message = "This shouldn't be happening, category=%s, url=%s" % (category, url)
        BjsUtil.log(LOGFILE, BjsUtil.LOG_ERROR, message, console_out=True)

        return []


def get_and_save_new_items(
    bjs_main_product_category_name,
    bjs_main_product_page):

    message = "Getting TOP category=%s, url=%s" % (
        bjs_main_product_page, 
        bjs_main_product_category_name)
    BjsUtil.log(LOGFILE, BjsUtil.LOG_INFO, message, console_out=True)

    driver = webdriver.Firefox()
    driver.get(bjs_main_product_page)
    
    name_element_xpath = '//*[@id="listing-container"]/div[1]/section/header/h1'
    name_element = WebDriverWait(driver, 3).until(
        EC.presence_of_element_located((By.XPATH, name_element_xpath))
    )

    wizard = BjsPageWizard()

    soup = BeautifulSoup(driver.page_source, "html.parser")

    if wizard.is_categories_page(soup):
        message = "Category=%s is a categories page with url=%s." % (
            bjs_main_product_category_name, 
            bjs_main_product_page)
        BjsUtil.log(LOGFILE, BjsUtil.LOG_INFO, message, console_out=True)

        category_map = wizard.map_categories_to_urls(soup)
    else:
        message = "Not categories on page, category=%s, url=%s" % (
            bjs_main_product_category_name, 
            bjs_main_product_page)

        BjsUtil.log(LOGFILE, BjsUtil.LOG_INFO, message, console_out=True)
        raise Exception(message)

    repository = BjsProductRepository()

    items_on_db = json.loads(repository.get_items().content)
    existing_item_names = []
    for item in items_on_db:
        existing_item_names.append(item["name"]) 
        
    items = []
    for key in category_map:
        items += get_items_from_store_website(driver, wizard, key, category_map[key])

    new_items_responses = []
    for i in items:
        if i.name in existing_item_names:
            message = "Item=%s already exists. Skipping." % (i.name)
            BjsUtil.log(LOGFILE, BjsUtil.LOG_INFO, message, console_out=True)

            continue

        resp = repository.create_new_item(i)
        new_items_responses.append(resp.content)
        
        message = "Saved new item=%s" % (i.name)
        BjsUtil.log(LOGFILE, BjsUtil.LOG_INFO, message, console_out=True)

    return new_items_responses


##########
## main ##
##########

bjs_main_product_page = "http://www.bjs.com/grocery-household--pet.category.3000000000000117223.2001244"
bjs_main_product_category_name = "Grocery, Household & Pet"

get_and_save_new_items(
    bjs_main_product_category_name,
    bjs_main_product_page)
