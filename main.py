from bs4 import BeautifulSoup
import time
import csv
import re
from urllib.request import Request, urlopen
import mysql.connector
from urllib.parse import urlparse
from fake_useragent import UserAgent
ua = UserAgent()
#MYSQL CONNECTION PARAMS
cnx = mysql.connector.connect(host='localhost', user='python', password='password',database='homegatedb')
cursor = cnx.cursor(buffered=True)
start = time.time()

count = 0
def status(str):
    print(str)

def inc(): 
    global count 
    count += 1

def getAllSwitzerlandRentProperties():
    ids = []
    page = []
    page = getTimeRange()
    one = page[0]
    two = page[1]
    for page in range(one, two):    
        time.sleep(1)
        req = Request(
            url = 'https://www.homegate.ch/rent/real-estate/country-switzerland/matching-list?ep=' + str(page) + '&o=dateCreated-desc',
            headers={'User-Agent': ua.random}
        )
        try:
            html = urlopen(req).read()
        except:
            time.sleep(1)
            html = urlopen(req).read()
        soup = BeautifulSoup(html, "lxml")
        for a in soup.find_all('a',attrs = {'class':'ListItem_itemLink_30Did'}):
            href = a['href']
            inc()
            status("gotten list " + str(count) + ": " + href)
            ids.append(href)

        
        status("appended page " + str(page))
    return ids

def getAllSwitzerlandBuyProperties():
    ids = []
    page = []
    page = getTimeRange()
    one = page[0]
    two = page[1]
    for page in range(one, two):    
        time.sleep(1)
        req = Request(
            url = 'https://www.homegate.ch/buy/apartment/country-switzerland/matching-list?ep=' + str(page) + '&o=dateCreated-desc',
            headers={'User-Agent': ua.random}
        )
        try:
            html = urlopen(req).read()
        except:
            time.sleep(1)
            html = urlopen(req).read()
        soup = BeautifulSoup(html, "lxml")
        for a in soup.find_all('a',attrs = {'class':'ListItem_itemLink_30Did'}):
            href = a['href']
            inc()
            status("gotten list " + str(count) + ": " + href)
            ids.append(href)

        
        status("appended page " + str(page))
    return ids

def getTimeRange():
    arr = []
    timestamp = time.strftime('%H');
    hour = int(timestamp)
    arr = [1 + 2 * (hour - 1), 1 + 2 * (hour - 1) + 2]
    return arr

def getAllData(section, country, props):
    ids = props
    
    status("GETTING ALL DATA FOR SWITZERLAND RENT PROPERTIES USING THEIR UNIQUE IDS....")
    for id in ids:
            start = time.time()
            new_id = str(id)
            req = Request(
                url = 'https://www.homegate.ch' + new_id + '',
                headers={'User-Agent': ua.random}
            )
            try:
                html = urlopen(req).read()
            except:
                print("waiting for 3 minutes due to too many requests before continuing")
                time.sleep(180)
                html = urlopen(req).read()
            time.sleep(2)
            soup = BeautifulSoup(html, "lxml")
            street =""
            try:
                street = soup.find("address", attrs={'class':'AddressDetails_address_3Uq1m'}).text
                a = street.split()
                city = a[-1]
            except:
                street = ""
                city =""
            keys = list()
            vals = list()
            # CoreAttributes_coreAttributes_2UrTf
            try:
                attris = soup.find('div',attrs = {'class':'CoreAttributes_coreAttributes_2UrTf'})
                titles = attris.select('dl dt')
                values = attris.select('dl dd')
                for title in titles:
                    keys.append(title.text)
                for value in values:
                    vals.append(value.text)
            except: 
                attris = soup.find('div',attrs = {'class':'CoreAttributes_coreAttributes_2UrTf'})
                titles = attris.select('dl dt font font')
                values = attris.select('dl dd font font')
                for title in titles:
                    keys.append(title.text)
                for value in values:
                    vals.append(value.text)
            rentalpairs =  dict(zip(keys, vals))
            livingSpace = ""
            typeProp = ""
            roomsProp = ""
            floorsProp = ""
            try:
                typeProp += rentalpairs['Type:']
                roomsProp += rentalpairs['No. of rooms:']
                floorsProp += rentalpairs['Floor:']
                livingSpace += rentalpairs['Surface living:']         
            except KeyError:
                why = "some ppt not found"
                # Description_description_2w_d-
            des = soup.find('section',attrs = {'class':'Description_description_2w_d-'})
            description = des.find('h1').text
            try:
                phonenumber = soup.find('a',attrs = {'class':'HgPhoneButton_hgPhoneLink_2sHVG'})
                nom = phonenumber['href']
            except Exception as e:
                nom = ""
            outprice = soup.find('div',attrs = {'data-test':'costs'})
            innerprice = outprice.find('dl')
            price = innerprice.find('dd').text
           
            vals = (str(id),)
            cursor.execute('SELECT propertylink FROM properties WHERE propertylink = %s', vals)
            cnx.commit()
            newcount = cursor.rowcount
            if(newcount == 0):
                sql = 'INSERT INTO properties(section, country, street, city, typeProp, roomsProp, floorsProp, livingSpace, description, phonenumber,price,propertylink) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
                sql_vals =  (section, country, street,city, typeProp, roomsProp, floorsProp, livingSpace, description, nom, price,str(id))

                cursor.execute(sql, sql_vals)
                cnx.commit()
                print("affected rows = " + str(cursor.rowcount))
            else:
                print("Already in Database")

    end = time.time()
    print("time taken for  was :", end - start)

            
                

start = time.time()
getAllData("Rent", "Switzerland", getAllSwitzerlandRentProperties())
getAllData("Buy","Switzerland", getAllSwitzerlandBuyProperties())
cursor.close()

# print(getTimeRange())