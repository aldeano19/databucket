"""
Utility functions for Bjs scripts.
"""

import sys
sys.path.append("..")

import os

from Model import BjsProduct

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

LOG_INFO = "INFO"
LOG_WARN = "WARN"
LOG_ERROR = "ERROR"
LOG_DEBUG = "DEBUG"

def change_club(driver, club_url):
    driver.get(club_url)
    """
    Changelog:
        original:
            change_club_button_id = "shopClubBtn"
                - id not present any more
        aug 19, 2017:
            change_club_button_xpaths = [
                '//*[@id="locator-results"]/div/div/div[2]/div[2]/button',
                '//*[@id="locator-results"]/div/div/div/div[2]/button'
            ]
    """
    change_club_button_xpaths = [
        '//*[@id="locator-results"]/div/div/div[2]/div[2]/button',
        '//*[@id="locator-results"]/div/div/div/div[2]/button' # only use when index 0 doesnt work
    ]
    for xpath in change_club_button_xpaths:
        """Try the different xpaths to look for the store switch button. Return True once found."""
        try:
            change_button = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
            change_button.click()
            return True
        except Exception, e:
            continue

    return False

def bjs_dict_to_model(item_dict):
    id=None
    sku=None
    model=None
    name=None
    availability_stores=None
    availability_prices=None
    online_price=None
    image_url=None
    product_url=None

    if "id" in item_dict:
        id = item_dict["id"]

    if "sku" in item_dict:
        sku = item_dict["sku"]

    if "model" in item_dict:
        model = item_dict["model"]
    
    if "name" in item_dict:
        name = item_dict["name"]
    
    if "availabilityStores" in item_dict:
        availability_stores = item_dict["availabilityStores"]
    
    if "availabilityPrices" in item_dict:
        availability_prices = item_dict["availabilityPrices"]
    
    if "onlinePrice" in item_dict:
        online_price = item_dict["onlinePrice"]

    if "imageUrl" in item_dict:
        image_url = item_dict["imageUrl"]
    
    if "productUrl" in item_dict:
        product_url = item_dict["productUrl"]

    return BjsProduct(
                    id=id,
                    sku=sku,
                    model=model,
                    name=name,
                    availabilityStores=availability_stores,
                    availabilityPrices=availability_prices,
                    onlinePrice=online_price,
                    imageUrl=image_url,
                    productUrl=product_url)

def log(logfile, level, message, console_out=False):
    logdir = os.path.dirname(logfile)
    if not os.path.exists(logdir):
        os.makedirs(logdir)

    message = message.encode('ascii','ignore')
    with open(logfile, "a") as f:
        line = "%-15s | %s\n" % (level, message) 
        f.write(line)

    if console_out:
        print message