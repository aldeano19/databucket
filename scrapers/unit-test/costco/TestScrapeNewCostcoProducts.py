import unittest
import sys
import os

new_modules = "%s/../../costco" % (os.path.dirname(os.path.realpath(__file__)))
sys.path.append(new_modules)

from ScrapeNewCostcoProducts import *

class TestCostcoPageWizard(unittest.TestCase):

    def test_get_items_from_store_website(self):
        costco_main_product_page = "https://www.costco.com/grocery-household.html"

        driver = webdriver.Firefox()
        wizard = CostcoPageWizard()

        result = get_items_from_store_website(driver, wizard, costco_main_product_page)

        EXPECTED_1 = "Grocery, Household & Pet"
        
        self.assertEqual(EXPECTED_1, result.text.strip())

        
        


if __name__ == '__main__':
    unittest.main()
