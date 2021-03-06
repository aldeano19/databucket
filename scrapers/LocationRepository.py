import requests
import json
import yaml
import urllib

import GlobalUtil

class BjsLocationRepository():
    """docstring for BjsLocationRepository"""
    def __init__(self, domain, port, base_path):

        """This config needs to go to ENVIRONMENT variables"""
        self.domain = domain
        self.port = ":"+str(port)
        self.base_path = base_path

        self.locations_base_url = "/locations"

        self.get_clubs_urls = "/getUrlsMap"

    def get_locations_urls(self):
        url = self.domain + \
                self.port + \
                self.base_path + \
                self.locations_base_url + \
                self.get_clubs_urls

        print url
        return requests.get(url=url)

    def update_locations(self, location):
        
        url = self.domain + \
                self.port + \
                self.base_path + \
                self.locations_base_url

        return requests.put(url, params=location)



