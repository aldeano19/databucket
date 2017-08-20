"""
The script scrapes the details for existing items in the database using their url.

Information captured about items:
- sku
- model
- onlinePrice
- delivery
- description
- specifications

@author: eriel marimon
@created: july 1, 2017
@updated: july 4, 2017
"""

import sys
sys.path.append("..")
sys.path.append("exceptions")

from ProductRepository import BjsProductRepository
from PageIdentifier import BjsPageWizard
from BjsExceptions import BjsScrapeException

import BjsUtil
import GlobalUtil

from bs4 import BeautifulSoup
from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.support.wait import TimeoutException

import json
import time
import os
import math
import Queue
import threading


PRINT_TO_CONSOLE = True

def get_items_from_database():
    # init database
    repository = BjsProductRepository()

    # get items from database
    items_on_db = json.loads(repository.get_items().content)

    items = []

    for item_dict in items_on_db:
        items.append(BjsUtil.bjs_dict_to_model(item_dict))

    return items

def scrape_details_for_item(wizard, soup, item):
    try:
        sku_and_model = wizard.get_sku_and_model_to_product(soup)
    except BjsScrapeException, e:
        print "!!!!"
        print e.error_code
        print e.error_message
        exit()

    
    if not sku_and_model:
        return None

    item.sku = sku_and_model[0]
    item.model = sku_and_model[1]

    item.onlinePrice = wizard.get_online_price(soup)
    item.delivery = wizard.get_estimated_delivery(soup)
    item.description = wizard.get_details(soup)

    return item

def divide_items_payload(items, total_divisions):
    total_items = len(items)
    base_total = int(math.floor(total_items/total_divisions))
    remainder = total_items%total_divisions

    datasets = [0]*total_divisions
    for d in range(total_divisions):
        datasets[d] = []

    """ignore the remainder items"""
    the_range = len(items) - (len(items)%total_divisions)

    for i in range(0, len(items), total_divisions):
        for j in range(total_divisions):
            if(j+i > len(items)-1):
                break

            datasets[j].append(items[j+i])
                        
        if(j+i > len(items)-1):
            break

    return datasets

def ready_threads(logfile, payloads):
    threads = []
    for load in payloads:
        th = threading.Thread(target=scrape_items, args=(logfile, load))
        th.daemon = True

        threads.append(th)


    return threads

def scrape_items(logfile, items):
    start_time = time.time() * 1000

    driver = webdriver.Firefox()

    wizard = BjsPageWizard()

    repository = BjsProductRepository()

    item_counter = 0
    message = "LAST item=%s" % (items[-1].id)
    BjsUtil.log(
        "DEBUG"+logfile, BjsUtil.LOG_DEBUG, message, console_out=PRINT_TO_CONSOLE)
    for item in items:
        message = "STARTING item=%s" % (item.id)
        BjsUtil.log(
            "DEBUG"+logfile, BjsUtil.LOG_DEBUG, message, console_out=PRINT_TO_CONSOLE)
        
        item_counter += 1
        driver.get(item.productUrl)

        try:
            name_element = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.ID, "itemNameID"))
            )
        except TimeoutException, e:
            message = "%-20s item=%s" % ("Item not available", item.id)
            BjsUtil.log(
                logfile, BjsUtil.LOG_INFO, message, console_out=PRINT_TO_CONSOLE)
            continue

        soup = BeautifulSoup(driver.page_source, "html.parser")

        if not wizard.is_item_details_page(soup):
            message = "%-20s item=%s" % ("No details for", item.id)
            BjsUtil.log(
                logfile, BjsUtil.LOG_INFO, message, console_out=PRINT_TO_CONSOLE)
            continue

        updated_item = scrape_details_for_item(wizard, soup, item)

        if not updated_item:
            message = "%-20s item=%s" % ("Cant scrape", item.id)
            BjsUtil.log(
                logfile, BjsUtil.LOG_INFO, message, console_out=PRINT_TO_CONSOLE)
            continue


        response = repository.update_item(updated_item)

        return_code = response.status_code

        new_name = name_element.text
        if new_name != item.name:
            updated_item.name = new_name
            message = "%-20s item=%s. New name=%s, old name=%s. Updating name." \
                % ("Names differ for", 
                    item.id, 
                    new_name, 
                    item.name)
            BjsUtil.log(
                logfile, BjsUtil.LOG_WARN, message, console_out=PRINT_TO_CONSOLE)
        else:
            message = "%-20s item=%s : %s" % ("Updating", item.id, return_code)

        BjsUtil.log(
            logfile, BjsUtil.LOG_INFO, message, console_out=PRINT_TO_CONSOLE)

        remaining = GlobalUtil.estimate_remaining_time(
                len(items), item_counter, start_time)
        running_time = GlobalUtil.calculate_running_time(start_time)

        if (item_counter%5)==0:
            thread_progress = "%s %s/%s : %8s : %8s" \
                % (threading.current_thread().name, 
                    len(items), 
                    item_counter, 
                    remaining,
                    running_time)

            print thread_progress
        

##########
## main ##
##########

# display = Display(visible=0, size=(800, 600))
# display.start()

items = get_items_from_database()

"""Uncomment for debugging purposes."""
for i in items:
    if i.id == "599675559a1e3406aa0f5ed0":
        items = [i]

divided_payload = divide_items_payload(items, 1)

LOGFILE = ("bjs-logs/%s.log" % (os.path.basename(__file__))).replace(".py","")


threads = ready_threads(LOGFILE, divided_payload)

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




