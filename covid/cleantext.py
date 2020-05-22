import re
import sys
print("files to process-", len(sys.argv)-1, )
def remove_unrelated(l):
	l=l.replace('24*7 Control Room Landline: 044-29510400, 044-29510500 ','')
	l=l.replace("24*7 Control Room: 044-29510400, 044-29510500, 9444340496, 8754448477",'')
	l=l.replace("www.stopcorona.tn.gov.in ",'')
	l=l.replace("District Control Room – 1077. Toll Free Number – 1800 1205 55550 ",'')
	l=l.replace("Mobile Numbers: 9444340496, 8754448477 ",'')
	return l

for i in range(1,len(sys.argv)):
	f=open(sys.argv[i])
	lines=f.readlines()
	f.close()

	append=False
	with open(sys.argv[i].replace('.pdf.txt','.text'),'w') as g:
		#print(len(lines))
		newl=''
		for j in range(0,len(lines)):
			if re.match(r'\d+.pdf.tmp\s*:\s*Patient\s*\d+\s*:', lines[j]):
				if append == True:
					# dump prev line
					g.write(remove_unrelated(newl))
					append=False
				newl = re.sub(r'(\d+).pdf.tmp\s*:\s*Patient\s*(\d+)\s*:\s*(\.*)',r'\1,\2,\3',lines[j])
			elif re.match(r'\d+.pdf.tmp\s*-',lines[j]):
				if re.sub(r'\d+.pdf.tmp\s*-(.*)',r'\1',lines[j]).isspace():
					continue #print('empty')
				else:
					newl=newl.rstrip() +' '+ re.sub(r'\d+.pdf.tmp\s*-\s*(\.*)',r'\1',lines[j])
					append=True
			elif re.match(r'\d+.pdf.tmp\s*:\s*Patient\s*\d+\s*and\s*\d+\s*:', lines[j]):
				if append == True:
					# dump prev line
					g.write(remove_unrelated(newl))
					append=False
				newl = re.sub(r'(\d+).pdf.tmp\s*:\s*Patient\s*(\d+)\s*and\s*(\d+)\s*:\s*(\.*)',r'\1,\2-\3,\4',lines[j])
			elif re.match(r'\d+.pdf.tmp\s*:\s*Patient\s*\d+\s*to\s*\d+\s*:', lines[j]):
				if append == True:
					# dump prev line
					g.write(remove_unrelated(newl))
					append=False
				newl = re.sub(r'(\d+).pdf.tmp\s*:\s*Patient\s*(\d+)\s*to\s*(\d+)\s*:\s*(\.*)',r'\1,\2-\3,\4',lines[j])
			elif re.match(r'\d+.pdf.tmp\s*:\s*Patient\s*\d+\s*[&-]\s*\d+\s*:', lines[j]):
				if append == True:
					# dump prev line
					g.write(remove_unrelated(newl))
					append=False
				newl = re.sub(r'(\d+).pdf.tmp\s*:\s*Patient\s*(\d+)\s*[&-]\s*(\d+)\s*:\s*(\.*)',r'\1,\2-\3,\4',lines[j])
			elif re.match(r'\d+.pdf.tmp\s*:\s*•\s*Patient\s*\d+\s*[–&-]\s*\d+\s*:', lines[j]):
				if append == True:
					# dump prev line
					g.write(remove_unrelated(newl))
					append=False
				newl = re.sub(r'(\d+).pdf.tmp\s*:\s*•\s*Patient\s*(\d+)\s*[–&-]\s*(\d+)\s*:\s*(\.*)',r'\1,\2-\3,\4',lines[j])
			elif re.match(r'\d+.pdf.tmp\s*:\s*•\s*Patient\s*\d+\s*:', lines[j]):
				if append == True:
					# dump prev line
					g.write(remove_unrelated(newl))
					append=False
				newl = re.sub(r'(\d+).pdf.tmp\s*:\s*•\s*Patient\s*(\d+)\s*:\s*(\.*)',r'\1,\2,\3',lines[j])
			elif lines[j].strip() == "--":
				continue
			else:
				if lines[j].find('Patient') > 0:
					newl=newl.rstrip() +' '+ re.sub(r'\d+.pdf.tmp\s*:\s*(\.*)',r'\1',lines[j])
					append=True
				else:
					print('err?',sys.argv[i],j,lines[j])
					sys.exit(1)
			#print(newl)
		if append == True:
			# dump prev line
			g.write(remove_unrelated(newl).rstrip())
		g.write('\n')


# "^ Patient",
# "^\\n",
# "^--",
# "\f",
# "District",
# "District Wise ",
# "District Wise Report of passengers on follow-up for 28-day period for COVID-19 ",
# "^  ",
# "^\\n",
# "^ \\n",
# "•  ",
# "24*7 Control Room: 044-29510400, 044-29510500, 9444340496, 8754448477",
# "www.stopcorona.tn.gov.in ",
# "District Control Room – 1077. Toll Free Number – 1800 1205 55550 ",
# "Mobile Numbers: 9444340496, 8754448477 ",
# "24*7 Control Room Landline: 044-29510400, 044-29510500",
# "^\\n",
# "^--",
# 					"^\\n",