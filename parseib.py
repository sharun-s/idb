from bs4 import BeautifulSoup
import sys, pprint, unicodedata

html=  sys.stdin.read()

soup = BeautifulSoup(html, features="html.parser")
if soup.title == None:
	sys.exit()

def fulltext(soup):
	text = soup.body.get_text()

	# break into lines and remove leading and trailing space on each
	lines = (line.strip() for line in text.splitlines())
	# break multi-headlines into a line each
	chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
	#remove dups and preserve order
	seen = set()
	result = []
	for item in chunks:
		if item not in seen:
			seen.add(item)
			result.append(item)
	# drop blank lines
	text = ' '.join(chunk for chunk in result[2:5] if chunk)
	return text


def printtextfrom(soup):
	# kill all script and style elements
	#for script in soup(["script", "style"]):
	#    script.extract()    # rip it out
	table = soup.find('table', class_='infobox')
	if table:
		ib={}
		exceptional_row_count = 0
		for tr in table.find_all('tr'):
			if tr.find('th'):
				key = unicodedata.normalize('NFKD', tr.find('th').get_text()).strip()
				ib[key]=soup.title.string
				if tr.find('td'): 
					val = unicodedata.normalize('NFKD', tr.find('td').get_text()).strip().replace('\n','')
					ib[key]=val
		pprint.pprint(ib)
	else:
		pprint.pprint(fulltext(soup), width=sys.maxsize)

if soup.title.string == sys.argv[1]:
	printtextfrom(soup)	
else:
	print("Sorry found "+soup.title.string)	
