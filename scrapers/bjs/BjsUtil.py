"""
Utility functions for Bjs scripts.
"""

import sys
sys.path.append("..")

from Model import BjsProduct

LOG_INFO = "INFO"
LOG_WARN = "WARN"
LOG_ERROR = "ERROR"
LOG_DEBUG = "DEBUG"

def bjs_dict_to_model(item_dict):
    id=None
    sku=None
    model=None
    name=None
    availability_stores=None
    availability_prices=None
    online_price=None
    image_url=None
    product_url=None

    if "id" in item_dict:
        id = item_dict["id"]

    if "sku" in item_dict:
        sku = item_dict["sku"]

    if "model" in item_dict:
        model = item_dict["model"]
    
    if "name" in item_dict:
        name = item_dict["name"]
    
    if "availabilityStores" in item_dict:
        availability_stores = item_dict["availabilityStores"]
    
    if "availabilityPrices" in item_dict:
        availability_prices = item_dict["availabilityPrices"]
    
    if "onlinePrice" in item_dict:
        online_price = item_dict["onlinePrice"]

    if "imageUrl" in item_dict:
        image_url = item_dict["imageUrl"]
    
    if "productUrl" in item_dict:
        product_url = item_dict["productUrl"]

    return BjsProduct(
                    id=id,
                    sku=sku,
                    model=model,
                    name=name,
                    availabilityStores=availability_stores,
                    availabilityPrices=availability_prices,
                    onlinePrice=online_price,
                    imageUrl=image_url,
                    productUrl=product_url)

def log(logfile, level, message, console_out=False):
    message = message.encode('ascii','ignore')
    with open(logfile, "a") as f:
        line = "%-15s | %s\n" % (level, message) 
        f.write(line)

    if console_out:
        print message