import time
import requests
from bs4 import BeautifulSoup
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# import xml.etree.ElementTree as 
import re


import time
browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

url = 'https://www.homegate.ch/rent/real-estate/country-switzerland/matching-list'
header = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
    'referer':'https://www.google.com/'
    }

res = browser.get(url, headers=header)
soup = BeautifulSoup(res.text, "html.parser")
links = []
ids = browser.find_element("xpath",
    '//*[@id="app"]/main/div/div[2]/div[1]/div[1]/div[1]/div[3]/section[1]/div[4]/dl/dd[5]'
    )
for a in soup.find_all('a',attrs = {'data-test':'result-list-item'}):
    links.append(a['href'])

res = []
for link in links:
    urli = "https://www.homegate.ch/rent/" + link[-10:]
    resi = browser.get(urli, headers=header)
    time.sleep(25)
    soupi = BeautifulSoup(resi.text, 'html5lib')
    dom = etree.HTML(str(soupi))
    one = dom.xpath('//html/head/title')[0].text
    # resa = soupi.find("div", class_="SpotlightAttributes_label_3ETFE")
    print(one)
    
# print(res)


    
