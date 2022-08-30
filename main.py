from bs4 import BeautifulSoup
import time
import csv
import re
from urllib.request import Request, urlopen
import mysql.connector
from urllib.parse import urlparse
#MYSQL CONNECTION PARAMS
cnx = mysql.connector.connect(host='localhost', user='python', password='password',database='homegatedb')
cursor = cnx.cursor(buffered=True)
start = time.time()

count = 0
def status(str):
    print(str)

def inc() : 
    global count 
    count += 1

def getAllSwitzerlandRentProperties():
    status("GETTING ALL SWITZERLAND RENT PROPERTIES.....")
    ids = []
    for page in range(1,51):
        
        time.sleep(2)

        req = Request(
            url = 'https://www.homegate.ch/rent/real-estate/country-switzerland/matching-list?ep=' + str(page) + '&o=dateCreated-desc',
            headers={'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2919.83 Safari/537.36'}
        )
        html = urlopen(req).read()
        soup = BeautifulSoup(html, "lxml")
        for a in soup.find_all('a',attrs = {'class':'ListItem_itemLink_30Did'}):
            href = a['href']
            inc()
            status("gotten list " + str(count) + ": " + href)
            ids.append(href)

        
        status("appended page " + str(page))
    return ids

def getAllData(section, country):
    ids = getAllSwitzerlandRentProperties()
    
    status("GETTING ALL DATA FOR SWITZERLAND RENT PROPERTIES USING THEIR UNIQUE IDS....")
    for id in ids:
            start = time.time()
            new_id = str(id)
            req = Request(
                url = 'https://www.homegate.ch' + new_id + '',
                headers={'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2919.83 Safari/537.36'}
            )
            html = urlopen(req).read()
            time.sleep(2)
            soup = BeautifulSoup(html, "lxml")
            street = soup.find("address", attrs={'class':'AddressDetails_address_3Uq1m'}).text
            keys = list()
            vals = list()
            attris = soup.find('div',attrs = {'class':'CoreAttributes_coreAttributes_2UrTf'})
            titles = attris.select('dl dt')
            values = attris.select('dl dd')
            for title in titles:
                keys.append(title.text)
            for value in values:
                vals.append(value.text)
            rentalpairs =  dict(zip(keys, vals))
            livingSpace = ""
            try:
                typeProp = rentalpairs['Type:']
                roomsProp = rentalpairs['No. of rooms:']
                floorsProp = rentalpairs['Floor:']
                livingSpace = rentalpairs['Surface living:']         
            except KeyError:
                print("error found")
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
            a = street.split()
            city = a[-1]
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

            
                

# start = time.time()
getAllData("Rent", "Switzerland")
cursor.close()

