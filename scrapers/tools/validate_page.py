from PageIdentifier import BjsPageWizard
from selenium import webdriver
from bs4 import BeautifulSoup

import time

url = "http://www.bjs.com/coffee-tea--creamers/cocoa.category.3000000000000117035.3000000000000117334.2001378.1"

driver = webdriver.Firefox()
driver.get(url)

time.sleep(3)

bjs_prod_ident = BjsPageWizard()

soup = BeautifulSoup(driver.page_source, "html.parser")

# print bjs_prod_ident.is_categories_page(soup)
print bjs_prod_ident.is_product_page(soup)
