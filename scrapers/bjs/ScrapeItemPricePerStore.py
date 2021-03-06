"""
The script gets the prices for all items for all individual stores.
 

@author: eriel marimon
@created: aug 19, 2017
@updated: aug 19, 2017
"""
import re
import json
import time
import os
import threading
import sys
new_modules = "%s/.." % (os.path.dirname(os.path.realpath(__file__)))
sys.path.append(new_modules)

from ProductRepository import ProductRepository
from LocationRepository import BjsLocationRepository
from PageIdentifier import BjsPageWizard

import GlobalUtil
import BjsUtil

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


CONSOLE_LOG_TRUE = True
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


def get_item_price_from_club(driver, item_name, items_url_map, club, clubs_url_map):
    found_club = BjsUtil.change_club(driver, clubs_url_map[club])
    time.sleep(1)
    if not found_club:
        message = "Couldn't find club %s at %s." % (club, clubs_url_map[club])
        GlobalUtil.log(LOGFILE, GlobalUtil.LOG_ERROR, message, console_out=True)
        return None

    driver.get(items_url_map[item_name])

    mxpath = '//*[@id="containerLeft"]/div/div[2]'

    #this exception needs  to be handled
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, mxpath))
    )

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
    return match_price(get_all_text_from_element_list(ele))

def process_items_subset(item_subset_list, items_url_map, clubs_url_map):
    start_time = time.time() * 1000

    driver = webdriver.Firefox()
    wizard = BjsPageWizard()

    rest_connection = get_rest_env()

    product_repository = ProductRepository(
        rest_connection["domain"], 
        rest_connection["port"], 
        rest_connection["base_path"])

    item_club_errors = {}

    item_counter = 0

    for item_name in items_url_map:
        """ Only process the items which names were given in the item_subset_list, ignore the rest."""
        if item_name not in item_subset_list:
            continue

        item_counter += 1

        club_price_map = {}
        i = 0
        for club_name in clubs_url_map:
            message = "Processing item=%s and club=%s." % (item_name, club_name)
            GlobalUtil.log(LOGFILE, GlobalUtil.LOG_ERROR, message, console_out=True)
            i+=1
            try:
                club_price_map[club_name] = get_item_price_from_club(driver, item_name, items_url_map, club_name, clubs_url_map)
            except:
                message = "No Update on item=%s with store=%s." % (item_name, club_name)
                GlobalUtil.log(LOGFILE, GlobalUtil.LOG_ERROR, message, console_out=True)
                pass
            
        product_repository.patch_availability(item_name, club_price_map).content
        message = "Updated item %s." % (item_name)
        GlobalUtil.log(LOGFILE, GlobalUtil.LOG_INFO, message, console_out=True)

        # CALC progress
        remaining = GlobalUtil.estimate_remaining_time(
                len(item_subset_list), item_counter, start_time)
        running_time = GlobalUtil.calculate_running_time(start_time)

        if (item_counter%1)==0:
            message = "%s %s/%s : %8s : %8s" \
                % (threading.current_thread().name, 
                    len(item_subset_list), 
                    item_counter, 
                    remaining,
                    running_time)

            GlobalUtil.log(LOGFILE, GlobalUtil.LOG_INFO, message, console_out=True)
            

    return item_club_errors

def ready_threads(items_url_map, clubs_url_map, payloads):


    threads = []
    for load in payloads:
        th = threading.Thread(target=process_items_subset, args=(load, items_url_map, clubs_url_map))
        th.daemon = True

        threads.append(th)

    return threads

def get_rest_env():
    DEFAULT_ENVS = {
        "localhost":{
            "domain":"localhost",
            "port":"8080",
            "base_path":""
        },
        "t2medium":{
            "domain":"http://13.58.52.4",
            "port":"8088",
            "base_path":"/rest-0.1.0"
        }
    }

    system_in = sys.argv

    if len(system_in) < 2:
        identifier = "t2medium"
    else:
        identifier = system_in[1]

    if identifier in DEFAULT_ENVS:
        message = "Using default env '%s'" % (identifier)
        GlobalUtil.log(LOGFILE, GlobalUtil.LOG_INFO, message, console_out=CONSOLE_LOG_TRUE)
        return DEFAULT_ENVS[identifier]


def divide_keys(keys, divisions):
    # TODO: there is an offset in the algorithm not being accounted for, fix it so no items get overlooked on any run.
    section_size = len(keys)/divisions

    payloads = []

    mi = 0
    ma = section_size

    for d in range(divisions):
        payloads.append(keys[mi:ma])
        mi = ma
        ma += section_size

    return payloads

def run():
    
    rest_connection = get_rest_env()

    product_repository = ProductRepository(
        rest_connection["domain"], 
        rest_connection["port"], 
        rest_connection["base_path"])

    location_repository = BjsLocationRepository(
        rest_connection["domain"], 
        rest_connection["port"], 
        rest_connection["base_path"])


    clubs_url_map = location_repository.get_locations_urls().json()

    # items_url_map = product_repository.get_products_urls().json()
    filters = {"store":"BJS"}
    items_url_map = product_repository.filter_items(filters).json()


    # TODO: uuuuuuuuuuuu divide items_url_map.keys() into many
    payloads = divide_keys(items_url_map, 4)

    print "TZ: ", len(items_url_map)

    for p in payloads:
        print "PZ: ", len(p)

    threads = ready_threads(items_url_map, clubs_url_map, payloads)

    for t in threads:
        t.start()

    thread_alive = True
    while thread_alive:
        """keep running untill all threads are done"""
        thread_alive = False
        for t in threads:
            if t.is_alive():
                thread_alive = True

        time.sleep(5)

##########
## main ##
##########

if __name__ == "__main__":
    run()




