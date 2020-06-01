import requests as r
from bs4 import BeautifulSoup
content={}
url=r'.nic.in/list-of-collectors'
with open(r'TNDistricts') as f:
	for name in f.read().split('\n'):
		if input(name.lower()+url) == 'y':
			g=r.get(r'https://'+name.lower()+url)
			print(g.content)
			content[name]=g.content