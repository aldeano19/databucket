# Databucket
## Overview
An application to scrape grocery information from online stores like Sam's Club, BJs, Walmart, etc. Make the data available through a REST interface.

## Tech used
* Java - Spring framework
* MongoDb
* python: Selenium, py-curl, requests
* Swagger-Ui

## Features
* (Done) Given the root page of a grocery website, crawl the entire domain collecting usefull information about Items.
* (Done) Items are stored with a base model, but data that is beyond the scope of that model will also be stored.
* Perform analytics on the Items collection to compare them by Stores. Ex, what store has chepper eggs: Publix, Costco, BJs, etc
* (Done) For optimization, use selenium only when `requests` can't capture the intended html.
