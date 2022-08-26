import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import json
from uszipcode import SearchEngine

from selenium.webdriver.chrome.options import Options
engine = SearchEngine()


start = time.time()
#webdriver options
opts = Options()
# opts.add_argument(' — headless')
#get the driver
opts.add_argument("--headless")
browser = webdriver.Chrome(ChromeDriverManager().install(), options=opts)


url = 'https://www.homegate.ch/rent/3002047552' 

browser.get(url)
c = browser.page_source
soup = BeautifulSoup(c, "html.parser")

time.sleep(3)
streetname = soup.find(attrs={'class':'AddressDetails_address_3Uq1m'}).text
# attris = soup.find('div',attrs = {'class':'CoreAttributes_coreAttributes_2UrTf'})
# prop = attris.find('dl').text
# des = soup.find('section',attrs = {'class':'Description_description_2w_d-'})
# description = des.find('h1').text
# phoneNumber = soup.find('span',attrs = {'class':'HgButton_content_m2Lkf'}).text
# outprice = soup.find('a',attrs = {'data-test':'costs'})
# innerprice = outprice.find('dl')
# price = innerprice.find('dd').text

# a = streetname.split()
# cityname = a[-1]
browser.quit()
end = time.time()
# print(streetname, " ", prop, " ", description, " ", phoneNumber, " ", price)
print(streetname)
# with open('links.txt', 'a') as f:
#     for row in links:
#         f.write('%s\n' % row)
#     f.close()
print(end-start)

