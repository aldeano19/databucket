import requests
import json
import yaml
import urllib

import GlobalUtil

class ProductRepository():
    """docstring for ProductRepository"""
    def __init__(self, domain, port, base_path):

        self.domain = domain
        self.port = ":"+str(port)
        self.base_path = base_path

        self.items_base_url = "/items"
        self.update_items_url = "/%s"
        self.patch_items_availability_url = "/availability/%s"
        self.get_items_with_name_url = "/withName/%s"
        self.get_items_by_id_url = "/%s" # takes an item's mongodb id
        self.get_items_urls = "/getUrlsMap"
        self.patch_items_availability = "/%s" # takes an item's name
        self.filter_items_url = "/filter"

    def create_new_item(self, item):
        # item_dict = item.__dict__

        url = self.domain + \
                self.port + \
                self.base_path + \
                self.items_base_url 

        return requests.post(url, params=item)

    def get_products_urls(self):
        url = self.domain + \
                self.port + \
                self.base_path + \
                self.items_base_url + \
                self.get_items_urls
                
        return requests.get(url)

    def filter_items(self, filters):
        url = self.domain + \
                self.port + \
                self.base_path + \
                self.items_base_url + \
                self.filter_items_url

        return requests.get(url, params=filters)

    def get_items(self):
        url = self.domain + \
                self.port + \
                self.base_path + \
                self.items_base_url

        return requests.get(url)

    def update_item(self, item):
        # item_dict = item.__dict__
        
        url = self.domain + \
                self.port + \
                self.base_path + \
                self.items_base_url + \
                self.update_items_url % (item["id"]) 

        return requests.put(url, params=item)


    def patch_availability(self, item_name, price_update_map):
        url = self.domain + \
                self.port + \
                self.base_path + \
                self.items_base_url

        headers = {
            "Content-Type": "application/json"
        }

        params={
            "itemName":item_name
        }

        price_update_map = json.dumps(price_update_map)

        print "url:",url
        print "prams:",params
        print "data:",price_update_map

        return requests.patch(url, params=params, data=price_update_map, headers=headers)


# UNIT TEST CLASS #
import unittest

class TestProductRepository(unittest.TestCase):

    def setUp(self):
        self.rest_connection = GlobalUtil.get_rest_env()

        self.product_repository = ProductRepository(
            self.rest_connection["domain"], 
            self.rest_connection["port"], 
            self.rest_connection["base_path"])
        

    def test_filter_items(self):
        filters = {"store":"BJS"}
        results = self.product_repository.filter_items(filters).json()

        bad_results = self.product_repository.get_items().json()



        print len(bad_results)

        print len(results)

        self.assertNotEqual( len(results), len(bad_results))


if __name__ == '__main__':
    unittest.main()






