import requests
import json
import yaml
import urllib

import GlobalUtil

from Model import BjsProduct

class BjsProductRepository():
	"""docstring for BjsProductRepository"""
	def __init__(self):

		self.domain = "http://localhost"
		self.port = ":8080"
		self.base_path = ""

		self.items_base_url = "/items"
		self.update_items_url = "/%s"
		self.patch_items_availability_url = "/availability/%s"
		self.get_items_with_name_url = "/withName/%s"
		self.get_items_by_id_url = "/%s" # takes an item's mongodb id
		self.get_items_urls = "/getUrlsMap"
		self.patch_items_availability = "/%s" # takes an item's name

	def create_new_item(self, item):
		item_dict = item.__dict__

		url = self.domain + \
				self.port + \
				self.base_path + \
				self.items_base_url 

		return requests.post(url, params=item_dict)

	def get_products_urls(self):
		url = self.domain + \
				self.port + \
				self.base_path + \
				self.items_base_url + \
				self.get_items_urls
				
		return requests.get(url)

	def get_items(self):
		url = self.domain + \
				self.port + \
				self.base_path + \
				self.items_base_url

		return requests.get(url)

	def update_item(self, item):
		item_dict = item.__dict__
		
		url = self.domain + \
				self.port + \
				self.base_path + \
				self.items_base_url + \
				self.update_items_url % (item.id) 

		return requests.put(url, params=item_dict)


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





