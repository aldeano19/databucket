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

def get_location_ids(driver, locations_search_url):
    driver.get(locations_search_url)

    """
    Changelog:
        original:
            states_xpath = '//*[@id="locator_dropdown"]/table/tbody/tr[1]/td/em/select/option' 
                - The store id is the value property in this <a> (anchor tag)
        aug 19, 2017:
            location_elements = '//*[@id="left"]/ul/li/a'
                - The store id is the number on the href property before ".shtml"
                - User the regex pattern '(\d+)\.shtml' to get it
    """
    
    location_elements = '//*[@id="left"]/ul/li/a'
    all_location_elements = driver.find_elements(
        By.XPATH, location_elements)

    location_id_map = {}

    for anchortag_element in all_location_elements:
        href = anchortag_element.get_attribute("href")
        regex_str = "(\d+)\.shtml"
        match = re.search(regex_str, href)

        if match:
            location_id = match.group(1)
        else:
            message = "Can't extract store id from href=%s with regex=%s " % (href, regex_str)
            BjsUtil.log(LOGFILE, BjsUtil.LOG_ERROR, message, console_out=True)
            continue

        location_id_map[anchortag_element.text] = location_id
        
        message = "%-30s : %s" % (anchortag_element.text, location_id)
        BjsUtil.log(LOGFILE, BjsUtil.LOG_INFO, message, console_out=False)

    return location_id_map
        
def build_urls(info_map):
    """
    Changelog:
        aug 19, 2017: 
            store_info_url_tmpl = "https://www.bjs.com/locations/clubs/0199.shtml"
                - Introduced, but old url stil valid. 
                - Using old, since the location id doesnt need the extra 0 that this one needs
    """
    store_info_url_tmpl = "http://www.bjs.com/webapp/wcs/stores/servlet/LocatorMapDirectionsView?locationId=%s"
    
    for key in info_map:
        info_map[key] = store_info_url_tmpl % (info_map[key])

    return info_map
    
def get_address(driver):
    address_element_xpath = [
        '//*[@id="locator-results"]/div/div/div[2]/div[1]',
        '//*[@id="locator-results"]/div/div/div/div[1]'
    ]

    for xpath in address_element_xpath:
        try:
            address_element = driver.find_element(
                By.XPATH, xpath)
            return address_element.text
        except:
            pass

    return None


##########
## main ##
##########

locations_search_url = "http://www.bjs.com/webapp/wcs/stores/servlet/LocatorIndexView"

driver = webdriver.Firefox()

wizard = BjsPageWizard()

locationRepository = BjsLocationRepository()

locations_map = get_location_ids(driver, locations_search_url)

locations_map = build_urls(locations_map)

for key in locations_map:
    # print "%-30s : %s" % (key, change_club(driver, h[key]))
    # time.sleep(1)
    found_club = BjsUtil.change_club(driver, locations_map[key])
    if not found_club:
        # TODO: Log a warning message. This club's url is unreachable.
        continue

    name = key
    street_address = get_address(driver)

    if not street_address:
        message = "No address found for %s." % (key)
        BjsUtil.log(LOGFILE, BjsUtil.LOG_WARN, message, console_out=True)

    club_url = locations_map[key]

    location = BjsLocation(
        retailer="Bjs",
        name=name.replace(".", ""),
        streetAddress=street_address,
        state=None,
        city=None,
        zipcode=None,
        clubUrl=club_url)

    update_response = locationRepository.update_locations(location)

    message = "%s : %s" % (
        update_response.json()["id"], 
        update_response.status_code)
    BjsUtil.log(LOGFILE, BjsUtil.LOG_INFO, message, console_out=True)




