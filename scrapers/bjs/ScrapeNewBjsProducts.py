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

import re
import json
import time
import os
import sys
new_modules = "%s/.." % (os.path.dirname(os.path.realpath(__file__)))
sys.path.append(new_modules)

from ProductRepository import ProductRepository
from PageIdentifier import BjsPageWizard

import BjsUtil
import GlobalUtil

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import json
import time
import os
import sys

CONSOLE_LOG_TRUE = True
LOGFILE = ("bjs-logs/%s.log" % (os.path.basename(__file__))).replace(".py","")

# CATEGORY_NAME_ELEMENT_XPATH = '//*[@id="listing-container"]/div[1]/section/header/h1'
# aug 17, 2017 : xpath update
CATEGORY_NAME_ELEMENT_XPATH = '//*[@id="listing-container"]/div[1]/div[1]/header/h1'

def get_items_from_store_website(driver, wizard, category, url):

    driver.get(url)

    # Try to wait for a page identifier to appear
    try:
        category_name_element = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.XPATH, CATEGORY_NAME_ELEMENT_XPATH))
        )
    except Exception, e:
        message = "Cant find category=%s at url=%s" % (category, url)
        GlobalUtil.log(LOGFILE, GlobalUtil.LOG_ERROR, message, console_out=CONSOLE_LOG_TRUE)
        return []

    soup = BeautifulSoup(driver.page_source, "html.parser")
    
    products = []


    if category_name_element.text != category:
        """Log warning message that names mismatched"""
        message = "Mismatch in category=%s and url=%s" % (category, url)
        GlobalUtil.log(LOGFILE, GlobalUtil.LOG_WARN, message, console_out=CONSOLE_LOG_TRUE)

    elif wizard.is_product_page(soup):
        """Get products on this page"""
        message = "Category=%s is a product page with url=%s." % (category, url)
        GlobalUtil.log(LOGFILE, GlobalUtil.LOG_INFO, message, console_out=CONSOLE_LOG_TRUE)

        return wizard.get_partial_products(soup)

    elif wizard.is_categories_page(soup):
        """Get categories on this page and recurse"""
        message = "Category=%s is a categories page with url=%s." % (category, url)
        GlobalUtil.log(LOGFILE, GlobalUtil.LOG_INFO, message, console_out=CONSOLE_LOG_TRUE)

        category_map = wizard.map_categories_to_urls(soup)
        products = []
        for key in category_map:
            products += get_items_from_store_website(driver, wizard, key, category_map[key])
        return products
    else:
        message = "This shouldn't be happening, category=%s, url=%s" % (category, url)
        GlobalUtil.log(LOGFILE, GlobalUtil.LOG_ERROR, message, console_out=CONSOLE_LOG_TRUE)

        return []




def get_and_save_new_items(
    bjs_main_product_category_name,
    bjs_main_product_page):

    message = "Getting TOP category=%s, url=%s" % (
        bjs_main_product_page, 
        bjs_main_product_category_name)
    GlobalUtil.log(LOGFILE, GlobalUtil.LOG_INFO, message, console_out=CONSOLE_LOG_TRUE)

    driver = webdriver.Firefox()
    driver.get(bjs_main_product_page)

    # CATEGORY_NAME_ELEMENT_XPATH = '//*[@id="listing-container"]/div[1]/section/header/h1'
    # aug 17, 2017 : xpath update
    CATEGORY_NAME_ELEMENT_XPATH = '//*[@id="listing-container"]/div[1]/div[1]/header/h1'
    
    name_element = WebDriverWait(driver, 3).until(
        EC.presence_of_element_located((By.XPATH, CATEGORY_NAME_ELEMENT_XPATH))
    )

    wizard = BjsPageWizard()

    soup = BeautifulSoup(driver.page_source, "html.parser")

    if wizard.is_categories_page(soup):
        message = "Category=%s is a categories page with url=%s." % (
            bjs_main_product_category_name, 
            bjs_main_product_page)
        GlobalUtil.log(LOGFILE, GlobalUtil.LOG_INFO, message, console_out=CONSOLE_LOG_TRUE)

        category_map = wizard.map_categories_to_urls(soup)
        
    else:
        message = "Not categories on page, category=%s, url=%s" % (
            bjs_main_product_category_name, 
            bjs_main_product_page)

        GlobalUtil.log(LOGFILE, GlobalUtil.LOG_INFO, message, console_out=CONSOLE_LOG_TRUE)
        raise Exception(message)

    rest_connection = GlobalUtil.get_rest_env()

    repository = ProductRepository(
        rest_connection["domain"], 
        rest_connection["port"], 
        rest_connection["base_path"])

    items_on_db = json.loads(repository.get_items().content)
    existing_item_names = []
    for item in items_on_db:
        existing_item_names.append(item["name"]) 
        
    items = []
    new_items_responses = []
    for key in category_map:
        new_items = get_items_from_store_website(driver, wizard, key, category_map[key])
        items += new_items

        for i in new_items:
            if i["name"] in existing_item_names:
                message = "Item=%s already exists. Skipping." % (i["name"])
                GlobalUtil.log(LOGFILE, GlobalUtil.LOG_INFO, message, console_out=CONSOLE_LOG_TRUE)
                continue

            resp = repository.create_new_item(i)
            
            new_items_responses.append(resp.content)
            
            message = "Saved new item=%s" % (i["name"])
            GlobalUtil.log(LOGFILE, GlobalUtil.LOG_INFO, message, console_out=CONSOLE_LOG_TRUE)

    return new_items_responses


##########
## main ##
##########

bjs_main_product_page = "http://www.bjs.com/grocery-household--pet.category.3000000000000117223.2001244"
bjs_main_product_category_name = "Grocery, Household & Pet"

get_and_save_new_items(
    bjs_main_product_category_name,
    bjs_main_product_page)
