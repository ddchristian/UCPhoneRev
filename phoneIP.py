

from suds.client import Client
from suds.transport.https import HttpAuthenticated
from suds.xsd.doctor import ImportDoctor, Import
from urllib.request import HTTPSHandler
import urllib.error
import urllib.request
import ssl


'''
import logging
logging.basicConfig(level=logging.INFO)
logging.getLogger('suds.client').setLevel(logging.DEBUG)
logging.getLogger('suds.transport').setLevel(logging.DEBUG)
logging.getLogger('suds.xsd.schema').setLevel(logging.DEBUG)
logging.getLogger('suds.wsdl').setLevel(logging.DEBUG)

'''


cucmIP = 'aa.bb.cc.dd'
user = 'usr'
pwd = 'pwd'


url = 'https://' + cucmIP + ':8443/realtimeservice/services/RisPort?wsdl'
print (url)

tns = 'http://schemas.cisco.com/ast/soap/'
imp = Import('http://schemas.xmlsoap.org/soap/encoding/', 'http://schemas.xmlsoap.org/soap/encoding/')
imp.filter.add(tns)


t = HttpAuthenticated(username=user, password=pwd)
t.handler=urllib.request.HTTPBasicAuthHandler(t.pm)

context = ssl.create_default_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_REQUIRED
context.load_verify_locations(cafile="mycertfile.pem")


t1=urllib.request.HTTPSHandler(context=context)
t.urlopener = urllib.request.build_opener(t.handler,t1)


c = Client(url, plugins=[ImportDoctor(imp)], transport=t)

result = c.service.SelectCmDevice('',{'SelectBy':'Name', 'Status':'Any', 'Class':'Any'})

print ('type result: ', type(result))
print (result)


print ('number of devices found', result['SelectCmDeviceResult']['TotalDevicesFound'])


for node in result['SelectCmDeviceResult']['CmNodes']:
    for device in node['CmDevices']:
        print (device['Name'], device['IpAddress'], device['DirNumber'], device['Description'], device['Model'])

