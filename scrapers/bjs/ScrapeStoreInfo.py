"""
The script get the information for all Bj's locations in the US

Information captured about stores:
- 

@author: eriel marimon
@created: july 8, 2017
@updated: july 8, 2017
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

def get_location_ids(driver, locations_search_url):
    driver.get(locations_search_url)

    states_xpath = '//*[@id="locator_dropdown"]/table/tbody/tr[1]/td/em/select/option'
    state_option_elements = driver.find_elements(
        By.XPATH, states_xpath)

    location_id_map = {}

    for state_element in state_option_elements:
        state_element.click()
        cities_xpath = '//*[@id="locator_dropdown"]/table/tbody/tr[2]/td/em/select/option'
        city_elements = driver.find_elements(
            By.XPATH, cities_xpath)

        for city_element in city_elements:
            key = "%s, %s" % (city_element.text, state_element.text)
            location_id_map[key] = city_element.get_attribute("value")

    return location_id_map
        
def build_urls(info_map):
    store_info_url_tmpl = "http://www.bjs.com/webapp/wcs/stores/servlet/LocatorMapDirectionsView?locationId=%s"
    for key in info_map:
        if "Select a Town" in key:
            continue
        info_map[key] = store_info_url_tmpl % (info_map[key])
    


def change_club(driver, club_id_url):

    driver.get(club_id_url)

    change_club_button_id = "shopClubBtn"
    change_button = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, change_club_button_id))
    )

    change_button.click()
    return True


##########
## main ##
##########
LOGFILE = ("%s.log" % (os.path.basename(__file__))).replace(".py","")

locations_search_url = "http://www.bjs.com/webapp/wcs/stores/servlet/LocatorIndexView"

driver = webdriver.Firefox()

h = get_location_ids(driver, locations_search_url)

build_urls(h)

for key in h:
    print change_club(driver, h[key])
    time.sleep(5)



