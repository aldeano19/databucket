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

		self.post_items_url = "/items"
		self.update_items_url = "/items/%s"
		self.get_items_url = "/items"
		self.patch_items_availability_url = "/items/availability/%s"
		self.get_items_with_name_url = "/items/withName/%s"
		self.get_items_by_id_url = "/items/%s"

	def create_new_item(self, item):
		item_dict = item.__dict__

		url = self.domain + \
				self.port + \
				self.base_path + \
				self.post_items_url 

		return requests.post(url, params=item_dict)

	def get_items(self):
		url = self.domain + \
				self.port + \
				self.base_path + \
				self.get_items_url

		return requests.get(url)

	def update_item(self, item):
		item_dict = item.__dict__
		
		url = self.domain + \
				self.port + \
				self.base_path + \
				self.update_items_url % (item.id) 

		return requests.put(url, params=item_dict)

