from bs4 import BeautifulSoup
import time
import csv
import re
from urllib.request import Request, urlopen
import mysql.connector



#MYSQL CONNECTION PARAMS
cnx = mysql.connector.connect(host='localhost', user='python', password='password',database='homegatedb')
cursor = cnx.cursor()
start = time.time()

count = 0
def status(str):
    print(str)

def inc() : 
    global count 
    count += 1

def getAllSwitzerlandRentProperties():
    status("GETTING ALL SWITZERLAND RENT PROPERTIES.....")
    all_rent_switzerland = []
    for page in range(1,51):
        # url = 'https://www.homegate.ch/rent/real-estate/country-switzerland/matching-list?ep=
        # header = {
        # 'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
        # 'referer':'https://www.google.com/'
        # }
        req = Request(
            url = 'https://www.homegate.ch/rent/real-estate/country-switzerland/matching-list?ep=' + str(page) + '&o=dateCreated-desc',
            headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'}
        )
        # res = browser.get(url, headers=header)
        html = urlopen(req).read()
        time.sleep(1)
        soup = BeautifulSoup(html, "lxml")
        ids = []
        for a in soup.find_all('a',attrs = {'class':'ListItem_itemLink_30Did'}):
            href = a['href']
            inc()
            status("gotten list " + str(count) + ": " + href)
            ids.append(href)

        
        all_rent_switzerland.append(ids)
        status("appended page " + str(page))
    return ids

def getAllData(section, country):
    ids = getAllSwitzerlandRentProperties()
    
    status("GETTING ALL DATA FOR SWITZERLAND RENT PROPERTIES USING THEIR UNIQUE IDS....")
    for id in ids:
        # if(index < 20):
            start = time.time()

            req = Request(
                url = 'https://www.homegate.ch' + str(id),
                headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'}
            )
            html = urlopen(req).read()
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
            status("gotten data on property: " + description + " with unique id of ")
            end = time.time()
            print("time taken for  was :", end - start)
            sql = 'INSERT INTO properties(section, country, street, city, typeProp, roomsProp, floorsProp, livingSpace, description, phonenumber,price,property_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
            sql_vals =  (section, country, street,city, typeProp, roomsProp, floorsProp, livingSpace, description, nom, price,id)

            cursor.execute(sql, sql_vals)
            cnx.commit()
            print("affected rows = " + str(cursor.rowcount))



            
                

# start = time.time()
getAllData("Rent", "Switzerland")
cursor.close()

# end = time.time()
# print("Time taken to get all properties ids", end-start)
# print(streetname, " ", prop, " ", description, " ", phoneNumber, " ", price)
# with open('links.txt', 'a') as f:
#     for row in links:
#         f.write('%s\n' % row)
#     f.close()
# browser.get('https://api.scrapingdog.com/scrape', params=payload)
# browser.get(url)
# c = browser.page_source
# # print (resp.text)
# # response = requests.get(url)
# soup = BeautifulSoup(c, 'lxml')
# # jsonStr = soup.find('script', attrs={'type':'application/ld+json'})
# streetname = soup.find("address", attrs={'class':'AddressDetails_address_3Uq1m'}).text

# attris = soup.find('div',attrs = {'class':'CoreAttributes_coreAttributes_2UrTf'})
# prop = attris.find('dl').text
# des = soup.find('section',attrs = {'class':'Description_description_2w_d-'})
# description = des.find('h1').text
# phoneNumber = soup.find('a',attrs = {'class':'HgPhoneButton_hgPhoneLink_2sHVG'})
# nom = phoneNumber['href']
# outprice = soup.find('div',attrs = {'data-test':'costs'})
# innerprice = outprice.find('dl')
# price = innerprice.find('dd').text

# a = streetname.split()
# cityname = a[-1]
# browser.quit()
# end = time.time()
# header = []
# content = []
# header.append("street")
# header.append("city")
# content.append(streetname)
# content.append(cityname)
# one = re.findall(":(:?(\s\w+)|(\w+))", prop)
# for x in one:
#     content.append(x[0])
# two = re.findall("(\w+):", prop)
# for x in two:
#     header.append(x)
# header.append("description")
# header.append("phone_no")
# header.append("price")
# content.append(description)
# content.append(nom)
# content.append(price)
# # print(streetname, " ", prop, " ", description, " ", nom, " ", price)
# count = 0
# with open('data.csv', 'w', encoding='UTF8') as f:
#     writer = csv.writer(f)

#     # write the header
#     writer.writerow(header)

#     # write the data
#     writer.writerow(content)
#     f.close()

# # print(end-start)

