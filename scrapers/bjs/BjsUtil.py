"""
Utility functions for Bjs scripts.
"""

import sys
sys.path.append("..")

import os

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


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

