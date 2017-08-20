import requests
import json
import yaml
import urllib

import GlobalUtil

from Model import BjsLocation

class BjsLocationRepository():
    """docstring for BjsLocationRepository"""
    def __init__(self):

        """This config needs to go to ENVIRONMENT variables"""
        self.domain = "http://localhost"
        self.port = ":8080"
        self.base_path = ""

        self.locations_base_url = "/locations"

        self.get_clubs_urls = "/getUrlsMap"

    def get_locations_urls(self):
        url = self.domain + \
                self.port + \
                self.base_path + \
                self.locations_base_url + \
                self.get_clubs_urls

        return requests.get(url=url)

    def update_locations(self, location):
        location_dict = location.__dict__
        
        url = self.domain + \
                self.port + \
                self.base_path + \
                self.locations_base_url

        return requests.put(url, params=location_dict)


#### Test it
# l = BjsLocation(
#         name="Nashua",
#         streetAddress="123 n 23 ave",
#         state="NY",
#         city="Nashua",
#         zipcode="12312",
#         clubUrl="bjsnashua.com")

# a = BjsLocationRepository()

# print a.update_locations(l).text


