
#
# Script reads IP Addresses from a file and then makes a call
# to each IP, scrapes the web page and extract phone fields.
# Tested with Python 3.5 on MAC OSX against CUCM 11.5
#


import urllib.request
from bs4 import BeautifulSoup


with open('iplist.txt', 'r') as f:
    iplist = [line.strip() for line in f]

for ip in range(len(iplist)) :
    phoneIP = iplist[ip]
    print ('\nOutput for: ', phoneIP)
    url = 'http://' + phoneIP + '/CGI/Java/Serviceability?adapter=device.statistics.device'
    print (url)

    fhand = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(fhand, "html.parser")
    phoneData = soup.find_all('b')

    searchList = ['MAC Address', 'MAC address','Phone DN', 'UDI']


    for bTag in range(len(phoneData)) :
        bText = phoneData[bTag].text.strip()
        if bText in searchList :
            if bText != 'UDI' :
                print (bText, '\b: ', phoneData[bTag + 1].text)
            else    :
                print ('Phone Model: ', phoneData[bTag + 3].text)
                print ('Hardware Revision: ', phoneData[bTag + 7].text)
                print ('Serial Number: ', phoneData[bTag + 9].text)






