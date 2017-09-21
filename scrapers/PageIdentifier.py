# Takes in a BeautifulSoup object and looks for specific contents in it

import os
import sys
exceptions_modules = "%s/exceptions" % (os.path.dirname(os.path.realpath(__file__)))
sys.path.append(exceptions_modules)

print "-"*50
print exceptions_modules

from BjsExceptions import BjsScrapeException

import re

import GlobalUtil

class CostcoPageWizard():
    """docstring for CostcoPageWizard"""
    def __init__(self):
        self.base_url = "http://www.costco.com"

    def map_categories_to_urls(self, soup):
        """
        Get all categories on page as a map of category name to url
        """
        category_list = soup.find_all("div",{"class":"col-xs-6 col-md-3 col-xl-3"})
        if category_list == None:
            raise Exception("No Categories grid on page=")

        category_url_map = {}
        costco_base_url = "https://www.costco.com"
        for cat in category_list:
            cat_url = cat.find("a", href=True)["href"]
            key = cat.text.strip()

            category_url_map[key] = costco_base_url + cat_url

        return category_url_map        
        
    def get_partial_products(self, soup):
        
        product_list = soup.find_all("div",{"class":"col-xs-6 col-md-4 col-xl-3 product"})

        products = []

        for product_element in product_list:

            # Get link to this product
            product_url = product_element.find("a",{"class":"thumbnail"})["href"]
            
            # Get product itemid
            anchortag = product_element.find("a",{"class":"thumbnail"})
            itemid = anchortag["itemid"]

            # Get link to image of this product
            image_elem = anchortag.find("img",{"class":"img-responsive"})
            image_url = ""
            if "src" in image_elem:
                image_url = image_elem["src"]
            elif "data-src" in image_elem:
                image_url = image_elem["data-src"]

            # Get price of this product
            price_elem = product_element.find("div",{"class":"price"})
            price = ""
            if price_elem:
                price = price_elem.text

            # Get name of this product
            name = product_element.find("p",{"class":"description"}).text
            
            products.append({
                "name":name,
                "onlinePrice":price,
                "imageUrl":image_url,
                "model":itemid,
                "productUrl":product_url,
                "store":"COSTCO"
            })

        return products
        

class BjsPageWizard():
    """docstring for BjsPageWizard"""
    def __init__(self):
        self.base_url = "http://www.bjs.com"

    def has_description_tab(self, soup):
        """
        identifies if the html soup countains 'description', 'specifications', 
        'reviews ()', and 'shipping + returns' tabs
        """
        tab_titles = [
            "description", 
            "specifications", 
            "reviews", 
            "shipping + returns"]

        """
        This captures the name of the 4 tabs on an item:
            1- description
            2- specification
            3- reviews
            4- shipping + refunds
        
        changelog:
            original
                description_tabs = soup.find("div", {"class":"tabs"})

            aug 17, 2017:
                description_tabs = soup.find("ul", {"id":"qq0l09-responsiveaccordiontabs"}): 
                    DO NOT USE THIS ID, IS DYNAMIC
                description_tabs = soup.find("ul", {"class":"pdp-accordion tabs"})
        """

        description_tabs = soup.find("ul", {"class":"pdp-accordion tabs"})
        if not description_tabs:
            return False

        for title in tab_titles:
            if title not in description_tabs.text:
                return False

        return True

    def has_categories_block(self, soup):
        categories_block = soup.find("fieldset", {"class":"checklist -open"})

        if categories_block == None:
            return False

        regex_str = "Categories"
        match = re.search(regex_str, categories_block.text)

        return match != None # true if found match

    def has_item_filter_options(self, soup):
        """
        identifies if the html soup countains the bjs filter bar as off june 25, 2017
        """
        filter_bar = soup.find("div", {"class":"filter-options -in-page"})
        
        if filter_bar == None:
            """
            This page doesn't have the filter_bar element
            """
            return False

        """ 
        Match BJ's items filter block
        Example match: 
        43 Items | All (43) | Online (0) | In Club (43) | By Best Match | 40 per page
        """
        regex_str = "\d+\sItems.*All\s\(\d+\)\sOnline\s\(\d+\)\sIn\sClub\s\(\d+\).*By\sBest\sMatch.*40\sper\spage"
        match = re.search(regex_str, filter_bar.text)
        
        return match != None # true if found match

    def has_item_block(self, soup):
        """
        identifies if the html soup has at least one bjs item block
        """
        item_block = soup.find("li", {"class":"product ng-scope"})

        if item_block == None:
            """
            This page doesn't have the item_block element
            """
            return False
        """
        Match BJ's item display block
        """
        regex_str = "Compare"
        match = re.search(regex_str, item_block.text)

        return match != None # true if found match

    def has_brands_and_rating_block(self, soup):
        """
        identifies if the html soup has the Bj's brands block
        """
        brands_and_rating = soup.find_all("fieldset", {"class":"checklist -open"})

        if brands_and_rating == None:
            return False

        blocks = ""
        for block in brands_and_rating:
            blocks += block.text

        regex_str = "Brand.*Rating"
        match = re.search(regex_str, blocks)

        return match != None # true if found match


    def is_product_page(self, soup):
        """
        Identifies if a page has a list of products
        """
        return \
            self.has_item_filter_options(soup) and \
            self.has_item_block(soup)
            # and \
            # self.has_brands_and_rating_block(soup)

    def is_item_details_page(self, soup):
        return \
            self.has_description_tab(soup)

    def is_categories_page(self, soup):
        return \
            self.has_categories_block(soup) and \
            not \
                (self.has_item_filter_options(soup) or \
                self.has_item_block(soup) or \
                self.has_brands_and_rating_block(soup))


    def map_categories_to_urls(self, soup):
        """
        Get all categories on page as a map of category name to url
        """
        categories_grid = soup.find("ul",{"class":"categories"})
        if categories_grid == None:
            # TODO: set page= to an actual url
            raise Exception("No Categories grid on page=(define url)")

        category_list = categories_grid.find_all("li",{"class":"category"})
        if category_list == None:
            # TODO: set page= to an actual url
            raise Exception("Categories grid is empty on this page=(define url)")

        category_url_map = {}

        for cat_html in category_list:
            category_name = cat_html.find("h4",{"class":"name ng-binding"}).text
            category_url = cat_html.find("a", href=True)["href"]
            
            category_url_map[category_name] = self.base_url + category_url

        return category_url_map

    def get_partial_products(self, soup):
        """
        Gets all the products on a page. Information on this page is incomplete. 
        Fields provided: name, product_url, image_url.
        Call complete_product(Product) to fill all the fields for a specific product.
        """
        product_grid = soup.find_all("div", {"class":"productBox"})
        if product_grid == None:
            raise Exception("No product grid on this page="+url)

        products = []

        for product_html in product_grid:
            name = product_html.find("h4",{"class":"name"}).text
            product_url = self.base_url + product_html.find("a", href=True)["href"]
            image_url = product_html.find("img")["src"]

            products.append({
                "name":name,
                "imageUrl":image_url,
                "productUrl":product_url,
                "store":"BJS"
            })

        return products

    def get_a_match_for_item_and_model(self, string):
        regex_strings_prioritized = [
            "Item:\s(\d+).*\|\s*Model:\s*([#A-Z\d-]+)", # Item: 123 | Model: #AS-123
            "Item:\s(\d+)()",                             # Item: 123
            "Item:().*\|\s*Model:\s*([#A-Z\d-]+)"         # Item: | Model: #AS-123
        ]

        for regex_str in regex_strings_prioritized:
            match = re.search(regex_str, string)
            if match:
                return (match, regex_str)

    def get_sku_and_model_to_product(self, soup):
        """
        Returns the updated product.
        On the given soup, find value for sku and model. Add them to the given product.
        """
        sku_and_model = soup.find(id="productModel")
        
        if not sku_and_model:
            error = "No id=productModel"
            raise BjsScrapeException(100, error)
        
        sku_and_model_str = sku_and_model.text.replace("\n"," ")

        match = self.get_a_match_for_item_and_model(sku_and_model_str)

        if not match[0]:
            error = "No match for regex=%s on string=%s" % (
                match[1], sku_and_model_str)
            raise BjsScrapeException(101, error)

        sku = match[0].group(1)
        model = match[0].group(2)
            
        return sku, model

    def get_online_price(self, soup):
        """
        Change log:
            original:
                price = soup.find("div",{"class":"price4"})
            aug 18, 2017:
                price = soup.find("div",{"class":"price4"})
        """
        price = soup.find("div",{"class":"price-container"})
        if not price:
            return None
        
        """This regex leaves the dollar sign out of group 1"""
        regex_str = ".*\$([\d\.]+)"

        match = re.search(regex_str, price.text.strip())

        if match:
            return match.group(1)

        return None

    def get_estimated_delivery(self, soup):
        """
        Changelog:
            original:
                delivery_elem = soup.find(id="estimatedDelivery")
            aug 18, 2017:
                delivery_elem = soup.find("div":{"class":"est-delivery"})
        """
        delivery_elem = soup.find("div",{"class":"est-delivery"})

        if delivery_elem:
            delivery_regex_str = "Estimated Delivery:\s(.*)"
            match = re.search(delivery_regex_str, delivery_elem.text)
            if match:
                delivery = match.group(1)
                return delivery

        return None

    def get_details(self, soup):
        """ Gets the details panel for an item. """
        details_elem = soup.find(id="tab-1")

        if details_elem:
            return details_elem.text

        return None

# UNIT TEST CLASS #
import unittest

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestCostcoPageWizard(unittest.TestCase):

    def setUp(self):
        self.online = True
        self.wizard = CostcoPageWizard()

    def test_get_partial_products(self):

        grocery_organics_products_page = "https://www.costco.com/grocery-household.html?keyword=organic&COSTID=grocery_organic"
        driver = webdriver.Firefox()
        driver.get(grocery_organics_products_page)

        soup = BeautifulSoup(driver.page_source, "html.parser")
        
        partial_products = self.wizard.get_partial_products(soup)

        # Validate partial_product contains:
        #   name, product_url, image_url


        self.assertIsNotNone(partial_products)
        self.assertTrue(len(partial_products) > 0)

if __name__ == '__main__':
    unittest.main()



