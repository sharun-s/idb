import requests as r
import json

url=r'https://services9.arcgis.com/HwXIp55hAoiv6DE9/ArcGIS/rest/services/District_Wise_Covid_19_Status_view/FeatureServer/0/query?f=pjson&where=1%3D1&returnGeometry=false&outFields=Name%2CLocal_name%2C+State%2CPositive_Cases%2CActive_Cases%2CRecovered%2C+Death%2C+Home_Quarantine%2C+Last_Updated_Date'

g=r.get(url)
j=g.json()

for i in j['features']:
	a=i['attributes']
	print(','.join([a['Name'],str(a['Positive_Cases']),str(a['Active_Cases']),str(a['Recovered']),str(a['Death'])]))