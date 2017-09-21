"""
The script identifies new items in the website inventory and saves them to the
database. Items already in the database will be ignored. In-depth details for
items will be scrapped with another script.

Information captured about items:
- name
- imageUrl
- productUrl

@author: eriel marimon
@created: sept 9, 2017
"""

import re
import json
import time
import os
import sys
new_modules = "%s/.." % (os.path.dirname(os.path.realpath(__file__)))
sys.path.append(new_modules)

from ProductRepository import ProductRepository
from PageIdentifier import CostcoPageWizard

# import CostcoUtil
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
LOGFILE = ("costco-logs/%s.log" % (os.path.basename(__file__))).replace(".py","")

SEARCH_RESULT_ELEMENT_XPATH = '//*[@id="search-results"]/div[1]/div/div/div/h1'
def get_and_save_items_from_store_website(driver, wizard, url):

    rest_connection = GlobalUtil.get_rest_env()
    repository = ProductRepository(
        rest_connection["domain"], 
        rest_connection["port"], 
        rest_connection["base_path"])

    items_on_db = json.loads(repository.get_items().content)

    existing_item_names = []
    for item in items_on_db:
        existing_item_names.append(item["name"])

    driver.get(url)
    
    # Wait for a page identifier to appear
    category_name_element = WebDriverWait(driver, 3).until(
        EC.presence_of_element_located((By.XPATH, SEARCH_RESULT_ELEMENT_XPATH))
    )

    soup = BeautifulSoup(driver.page_source, "html.parser")

    categories_map = wizard.map_categories_to_urls(soup)

    new_items_responses = []

    for cat in categories_map:
        driver.get(categories_map[cat])

        soup = BeautifulSoup(driver.page_source, "html.parser")

        products = wizard.get_partial_products(soup)

        for item in products:
            if item["name"] in existing_item_names:
                message = "Item=%s already exists. Skipping." % (item["name"])
                GlobalUtil.log(LOGFILE, GlobalUtil.LOG_INFO, message, console_out=CONSOLE_LOG_TRUE)
                continue

            resp = repository.create_new_item(item)

            new_items_responses.append(resp.content)

            message = "Saved new item=%s" % (item["name"])
            GlobalUtil.log(LOGFILE, GlobalUtil.LOG_INFO, message, console_out=CONSOLE_LOG_TRUE)

    # return products

def main():
    costco_main_product_page = "https://www.costco.com/grocery-household.html"

    driver = webdriver.Firefox()
    wizard = CostcoPageWizard()

    products = get_and_save_items_from_store_website(driver, wizard, costco_main_product_page)

    

    # TODO: save products now



##########
## main ##
##########

if __name__ == '__main__':
    main()