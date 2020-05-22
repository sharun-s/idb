import requests as r
import json
import datetime

posperday = r'https://services9.arcgis.com/HwXIp55hAoiv6DE9/ArcGIS/rest/services/TN_Covid_Date_Wise_PositiveCases/FeatureServer/0/query?where=1%3D1&resultType=none&outFields=*&f=pjson' 

g=r.get(posperday)
j=g.json()


for i in j['features']:
	a=i['attributes']
	s = a['Date']/ 1000.0
	dFormat = "%Y-%m-%d %H:%M:%S.%f"
	d = datetime.datetime.fromtimestamp(s).strftime('%d-%m')

	print(','.join([d,str(a['Positive_Cases'])]))

#widgeturls=r'https://nhmtn.maps.arcgis.com/sharing/rest/content/items/095ad0a1c0254b058fa36b32d1ab1977/data?f=json'
#g=r.get(widgeturls)
#4074ef37-a80a-4a1f-8114-4b4f2225a7a5#District_Wise_Covid_19_Status_view_7482
#"defaultSettings""textInfo""text"=="Confirmed Cases"
#datasets[data]