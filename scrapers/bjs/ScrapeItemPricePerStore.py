"""
The script gets the prices for all items for all individual stores.
 

@author: eriel marimon
@created: aug 19, 2017
@updated: aug 19, 2017
"""
import sys
sys.path.append("..")

from ProductRepository import BjsProductRepository
from LocationRepository import BjsLocationRepository
from PageIdentifier import BjsPageWizard

from Model import BjsLocation

import BjsUtil

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import re
import json
import time
import os

LOGFILE = ("bjs-logs/%s.log" % (os.path.basename(__file__))).replace(".py","")

def match_price(string):
    price_regex_str = "(\$\d+\.\d{2})"

    match = re.search(price_regex_str, string)

    if not match:
        print "No match for %s in %s" % (price_regex_str, string)
        exit()
        return None

    price = match.group(1)
    return price

def get_all_text_from_element_list(element):
    string = ""
    for e in element:
        string += e.text
    return string

##########
## main ##
##########

location_repository = BjsLocationRepository()
product_repository = BjsProductRepository()

driver = webdriver.Firefox()
wizard = BjsPageWizard()

clubs_url_map = location_repository.get_locations_urls().json()

items_url_map = product_repository.get_products_urls().json()

item_club_errors = {}

for item_name in items_url_map:
    
    club_price_map = {}

    i = 0

    for club in clubs_url_map:
        i+=1
        found_club = BjsUtil.change_club(driver, clubs_url_map[club])
        time.sleep(1)
        if not found_club:
            message = "Couldn't find club %s at %s." % (club, clubs_url_map[club])
            BjsUtil.log(LOGFILE, BjsUtil.LOG_ERROR, message, console_out=True)
            continue

        driver.get(items_url_map[item_name])

        mxpath = '//*[@id="containerLeft"]/div/div[2]'

        try:
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, mxpath))
            )
        except:
            item_club_errors[item_name]=club
            continue
        
        """ 
        Necessary delay to let the text load. For some reason waiting for its 
        xpath presence is not enough, there is a delay from xpath appearance 
        to text appearance.
        """
        time.sleep(3)

        """
        Some times this expath returns a list, only one of those elements 
        contains the pricing info. Add their strings with 
        get_all_text_from_element_list() and pass it to match_price()
        """
        ele = driver.find_elements_by_xpath(mxpath)
        price_string = match_price(get_all_text_from_element_list(ele))
        
        club_price_map[club] = price_string
        
    
    product_repository.patch_availability(item_name, club_price_map).content
    print "updated item %s."

print "ERRORS:"
print item_club_errors
    




