class BjsLocation():
    """docstring for BjsLocation"""
    def __init__(self, 
        retailer,
        name,
        streetAddress,
        state,
        city,
        zipcode,
        clubUrl,
        id=None):
        
        """The mongodb id for the item"""
        self.id = id
        
        """The name of the retailer"""
        self.retailer = retailer

        """String. The name of the Location. A unique name within the store/database"""
        self.name = name
        
        """String. The name of the Location. A unique name within the store/database"""
        self.streetAddress = streetAddress
        
        """String. The name of the Location. A unique name within the store/database"""
        self.state = state

        """String. The name of the Location. A unique name within the store/database"""
        self.city = city

        """String. The name of the Location. A unique name within the store/database"""
        self.zipcode = zipcode

        """String. The name of the Location. A unique name within the store/database"""
        self.clubUrl = clubUrl
        
        #################
        # TODO: need to send clubHours as json in the body of the update.
        #################

class BjsProduct():
    """docstring for BjsProduct"""
    def __init__(self, 
        sku, 
        model, 
        name, 
        imageUrl, 
        productUrl,
        availabilityStores, 
        availabilityPrices,
        onlinePrice=None,
        delivery=None,
        description=None,
        id=None):

        """The mongodb id for the item"""
        self.id = id
        
        """String. The sku of the item. One sku can represent many items. Labeled 'Item' on BJ's website"""
        self.sku = sku
        
        """String. Model of the item. A unique model within the sku. Labeled 'Model on BJ's website"""
        self.model = model
        
        """String. The name of the item. A unique name within the store/database"""
        self.name = name
        
        """List of strings. The stores this items could be available"""
        self.availabilityStores = availabilityStores
        
        """List of numbers. The prices for the stores. One to one indenx relationship with availability_stores"""
        self.availabilityPrices = availabilityPrices

        """String. Direct url to this image on the web."""
        self.imageUrl = imageUrl

        """String. Direct url to this product on BJ's website"""
        self.productUrl = productUrl

        """Number. Price shown for the item when bought online."""
        self.onlinePrice = onlinePrice

        """Estimated delivery if bought online."""
        self.delivery = delivery

        """Bjs description of this item."""
        self.description = description


    