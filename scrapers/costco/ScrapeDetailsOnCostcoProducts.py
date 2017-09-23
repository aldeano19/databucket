"""
The script scrapes the details for existing costco items in the database using their url.

Information captured about items:


@author: eriel marimon
@created: september 21, 2017
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

def scrape_details_for_item(wizard, soup, item):
    sku = wizard.get_item_sku(soup)
    delivery = wizard.get_estimated_delivery(soup)
    description = wizard.get_details(soup)

    item["sku"] = sku
    item["delivery"] = delivery
    item["description"] = description

    return item

def scrape_items(logfile, items):
    start_time = time.time() * 1000

    driver = webdriver.Firefox()

    wizard = CostcoPageWizard()

    rest_connection = GlobalUtil.get_rest_env()

    repository = ProductRepository(
        rest_connection["domain"], 
        rest_connection["port"], 
        rest_connection["base_path"])

    item_counter = 0
    message = "LAST item=%s" % (items[-1]["id"])
    GlobalUtil.log(
        "DEBUG"+logfile, GlobalUtil.LOG_DEBUG, message, console_out=PRINT_TO_CONSOLE)

    for item in items:
        message = "STARTING item=%s" % (item["id"])
        GlobalUtil.log(
            "DEBUG"+logfile, GlobalUtil.LOG_DEBUG, message, console_out=PRINT_TO_CONSOLE)
        
        item_counter += 1

        try:
            driver.get(item["productUrl"])
        except Exception, e:
            message = "item=%s failed with e=%s" % (item["id"], e)
            GlobalUtil.log(
                logfile, GlobalUtil.LOG_INFO, message, console_out=PRINT_TO_CONSOLE)
            continue

        # TODO: make sure the page is loaded before continuing.


        soup = BeautifulSoup(driver.page_source, "html.parser")

        if not wizard.is_item_details_page(soup):
            message = "%-20s item=%s" % ("No details for", item["id"])
            GlobalUtil.log(
                logfile, GlobalUtil.LOG_INFO, message, console_out=PRINT_TO_CONSOLE)
            continue

        updated_item = scrape_details_for_item(wizard, soup, item)

        if not updated_item:
            message = "%-20s item=%s" % ("Cant scrape", item["id"])
            GlobalUtil.log(
                logfile, GlobalUtil.LOG_INFO, message, console_out=PRINT_TO_CONSOLE)
            continue

        response = repository.update_item(updated_item)

        return_code = response.status_code

        
        message = "%-20s item=%s : %s" % ("Updating", item["id"], return_code)

        GlobalUtil.log(
            logfile, GlobalUtil.LOG_INFO, message, console_out=PRINT_TO_CONSOLE)

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

def ready_threads(logfile, payloads):
    threads = []
    for load in payloads:
        th = threading.Thread(target=scrape_items, args=(logfile, load))
        th.daemon = True

        threads.append(th)

    return threads

PRINT_TO_CONSOLE = True
LOGFILE = ("costco-logs/%s.log" % (os.path.basename(__file__))).replace(".py","")

rest_connection = GlobalUtil.get_rest_env()

repository = ProductRepository(
    rest_connection["domain"], 
    rest_connection["port"], 
    rest_connection["base_path"])

items = GlobalUtil.get_items_from_database(repository, "COSTCO")

divided_payload = GlobalUtil.divide_items_payload(items, 1)

LOGFILE = ("costco-logs/%s.log" % (os.path.basename(__file__))).replace(".py","")

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