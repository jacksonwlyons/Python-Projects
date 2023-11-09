# Jackson Lyons
# Webscraper for farmers markets using Selenium and BeautifulSoup

import time
import csv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from collections import OrderedDict

url = "https://givinggarden.io/farmers-markets?location=davis+ca+usa"
farmers_markets = []
driver = webdriver.Chrome()
driver.get(url)
ignored_exceptions=(NoSuchElementException,StaleElementReferenceException,)
# wait for search box to show
wait = WebDriverWait(driver, 2, ignored_exceptions=ignored_exceptions).until( 
        EC.visibility_of_element_located((By.XPATH, '//*[@id="app"]/div/div[2]/div/div[3]/input')) 
    )
# find search box
search_bar = driver.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div/div[3]/input')
search_bar.clear()
search_bar.send_keys("East Lansing, MI, USA")
time.sleep(2)
# Need to wait until new google suggestion page shows up
wait2 = WebDriverWait(driver, 5, ignored_exceptions=ignored_exceptions).until( 
        EC.visibility_of_element_located((By.CSS_SELECTOR, 'body > div.pac-container.pac-logo')) 
    )
search_bar.send_keys(Keys.ARROW_DOWN)
search_bar.send_keys(Keys.ENTER)
# Wait for new search results
market1 = driver.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div/div[3]/div/a[1]')
WebDriverWait(driver, 5).until(EC.staleness_of(market1))
WebDriverWait(driver, 5, ignored_exceptions=ignored_exceptions).until( 
        EC.visibility_of_element_located((By.XPATH, '//*[@id="app"]/div/div[2]/div/div[3]/div/a[1]')) 
    )
# Update to newly loaded market elements
markets = driver.find_elements(By.CSS_SELECTOR, '#app > div > div.daVCC > div > div.oFedV > div > a')
# loop through each market
for market in markets:
    ActionChains(driver).move_to_element(market).perform()
    market.click()
    # gather data- add new dict to list
    WebDriverWait(driver, 5, ignored_exceptions=ignored_exceptions).until( 
            EC.visibility_of_element_located((By.CSS_SELECTOR, '#app > div > div.daVCC > div > h2')) 
        )
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    name_element = soup.find(class_='_1AtRl')
    address_element = soup.find(class_='_1qeWG')
    hours_element = soup.find(class_='d-flex flex-column mb-2')
    moreinfo_element = soup.find(class_='col-6').find_next_sibling()
    if hours_element is not None:
        dates_hours = hours_element.findChildren()
        hours = dates_hours[1].text
    else:
        hours = "Not Listed"
    name = name_element.text
    address = address_element.text
    products = []
    products_element = moreinfo_element.findChildren()[1]
    for prod in products_element.findChildren():
        if "Yes" in str(prod):
            product_name = prod.text
            products.append(product_name)
    # using collections.OrderedDict.fromkeys() to remove duplicated from list
    products = list(OrderedDict.fromkeys(products))
    products.remove('')
    farmers_markets.append({'name': name, 'address': address, 'hours': hours, 'products': products})

    driver.back()


print(farmers_markets)
fields = ['name', 'address', 'hours', 'products']
with open('markets.csv', 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames = fields)
    writer.writeheader()
    writer.writerows(farmers_markets)