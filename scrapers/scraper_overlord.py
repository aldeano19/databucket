import sys
import os
bjs_modules = "%s/bjs" % (os.path.dirname(os.path.realpath(__file__)))
costco_modules = "%s/costco" % (os.path.dirname(os.path.realpath(__file__)))
sys.path.append(bjs_modules)
sys.path.append(costco_modules)



import ScrapeNewBjsProducts
import ScrapeStoreInfo
import ScrapeDetailsOnBjsProducts
import ScrapeItemPricePerStore


while True:
	# Run ScrapeNewBjsProducts
	ScrapeNewBjsProducts.run()

	# Run ScrapeDetailsOnBjsProducts
	ScrapeDetailsOnBjsProducts.run(6)

	# Run ScrapeStoreInfo
	ScrapeStoreInfo.run()

	# Run ScrapeItemPricePerStore
	ScrapeItemPricePerStore.run()


