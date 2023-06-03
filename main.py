from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
service = Service("C:\Development\chromedriver.exe")
driver = webdriver.Chrome(service=service)
import re
import requests
from bs4 import BeautifulSoup

forms_url = "https://docs.google.com/forms/d/e/1FAIpQLSeJPNfr29RBhPQmXOMUMc1wHGvkI-5ZzhTLYLIAS8KSD_6APA/viewform?usp=sf_link"

url = "https://www.zillow.com/san-francisco-ca/rentals/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22mapBounds%22%3A%7B%22north%22%3A37.86126583902305%2C%22east%22%3A-122.32724276904297%2C%22south%22%3A37.68921797424968%2C%22west%22%3A-122.53941623095703%7D%2C%22mapZoom%22%3A12%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A20330%2C%22regionType%22%3A6%7D%5D%7D"

header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8,nl;q=0.7",
    "x-forwarded-proto":"https",
    "x-https":"on"
}

response = requests.get(url, headers=header)
soup = BeautifulSoup(response.content, "lxml")

########## prices ###########

prices_scrapped = soup.find_all(attrs={"data-test": "property-card-price"})
prices=[]
for price_element in prices_scrapped:
    price_text = price_element.getText()
    price_numeric = "$" + re.findall('\d+\,*\d*', price_text)[0].replace(',', '')
    prices.append(price_numeric)

# print(prices)

########## address ###########

address_scrapped = soup.find_all(attrs={"data-test": "property-card-addr"})
address = []
for address_element in address_scrapped:
    address.append(address_element.text)

# print(address)

########### links ###########

links_scrapped = soup.find_all(attrs={"data-test": "property-card-link"})
links=[]
for link in links_scrapped:
    href = link.get('href')
    if 'http' in href:
        links.append(href)
    else:
        links.append(f"https://www.zillow.com{href}")
links = list(set(links))

# print(links)

driver.get(forms_url)

for i in range(len(prices)):
    input_add = driver.find_element(By.XPATH,
                                    '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    time.sleep(1)
    input_add.send_keys(address[i - 1])
    time.sleep(1)

    input_price = driver.find_element(By.XPATH,
                                      '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    input_price.send_keys(prices[i - 1])

    input_link = driver.find_element(By.XPATH,
                                     '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    input_link.send_keys(links[i - 1])

    enter = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div')
    enter.click()

    time.sleep(1)

    siii = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/div/div[4]/a')
    siii.click()

    time.sleep(1)
