'''
Final code to parse feed and return csv ordered by DateListed with:
- only properties listed from 2016 [DateListed]
- only properties that contain the word "and" in the Description field
Required fields: MlsId, MlsName, DateListed, StreetAddress, Price, Bedrooms, Bathrooms, 
Appliances (all sub-nodes comma joined), Rooms (all sub-nodes comma joined), Description (the first 200 characters)

Created by Lauren Hearn, 08.07.19 for booj testing purposes
'''

import csv
import requests
import xml.etree.ElementTree as ET

def loadRSS(url):
    resp = requests.get(url)
    with open('homesfeed.xml', 'wb') as f:
        f.write(resp.content)
        
def parseXML(xmlfile):  
    tree = ET.parse(xmlfile) 
    root = tree.getroot()
    
    #get rid of listings not from 2016
    parent_map = dict((c, p) for p in tree.getiterator() for c in p)
    iterator = list(root.getiterator('Listing'))

    for item in iterator:
        old = item.find('ListingDetails/DateListed')
        text = old.text
        if '2016' not in text:
            parent_map[item].remove(item)
            continue

    # get relevant info
    data = open('homes.csv', 'w')

    # create the csv writer object
    csvwriter = csv.writer(data)
    fields = ['MlsId', 'MlsName', 'DateListed', 'StreetAddress', 'Price',
                 'Bedrooms', 'Bathrooms', 'Appliances', 'Rooms', 'Description']
    homes_head = fields

    count = 0
    for parent in root.findall('Listing'):
        home = []
        if count == 0:
            csvwriter.writerow(homes_head)
            count = count + 1

        mls = parent.find('./ListingDetails/MlsId').text
        home.append(mls)

        name = parent.find('./ListingDetails/MlsName').text
        home.append(name)

        year = parent.find('./ListingDetails/DateListed').text
        home.append(year)

        address = parent.find('./Location/StreetAddress').text
        home.append(address)

        price = parent.find('./ListingDetails/Price').text
        home.append(price)

        br = parent.find('./BasicDetails/Bedrooms').text
        home.append(br)

        bath = parent.find('./BasicDetails/Bathrooms').text
        home.append(bath)

        for child in parent.find('./RichDetails/Appliances'):
            apps = []
            for appliance in child:
                apps.append(appliance.text)
            appsli = ','.join(apps)
        home.append(appsli)

    #     for child in parent.find('./RichDetails/Rooms'):
    #         rms = []
    #         for room in child:
    #             rms.append(room.text)
    #         rmsli = ','.join(rms)
    #     home.append(rmsli)
    
    ### issues with oython not finding 'Room' elements?

        desc = str(parent.find('./BasicDetails/Description').text)
        if 'and' in desc:
            new_desc = desc[:200]
        home.append(new_desc)

        csvwriter.writerow(home)
    data.close()
      
def main(): 
    loadRSS('http://syndication.enterprise.websiteidx.com/feeds/BoojCodeTest.xml') 
    listings = parseXML('homesfeed.xml')
            
if __name__ == "__main__":
    main() 