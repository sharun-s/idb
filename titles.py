import re
# usualful when stripping title from name
titles='Judge |Giani |Syed |Subedar Major |Hony Capt\.? |Dada |Mir |Bibi |Baba |Rana |Rt. \(Rev.?\) |Raasacharya Swami |Mian |Rear Adm\.? |Dafadar |Lt\.Gen\.\(Rtd\.\) |Col.\(Retd\.\) |Col |Seth |Kazi |Haji |Aayu. |Bhai |Ashtavaidyan |Brahmasree |Mahashay |Mother |Pt\.? |Swami |Sardar |Sheikh? |Father |Fr. |Most Venerable |Her Royal Highness Princess |Hon. Commodore |Bishop |Nawab |Rear Admiral |Admiral |Prof.\(Smt\.?\) |Prof\.\(Mrs\.\) |His Holiness |Congressman |Sir |Card. |Maulana |Air Chief Marshal |Air Com\. |Wing Cdr |Lt\.Gen\.\(Rt\.\) |Late\. \(Gen\.\) |His Excellency |Acharya |Vaidya |Vaidyan |Yogacharya |Muni |Lord |Maharaj |Kumar |Rajmata |Rajkumari |Rani |Hakim |Sant |Guru |Air Marshal |Air Mar\. |Air Vice Marshal |Air Vice Mar\. |Ar\.V\.Mar\. |Br\. |Dr\. Rm\. |Dr\.\(Kum.\) |Dr\. \(Kum.\) |Dr\.\(Ms.\) |Dr\.\(Mrs.\) |Dr\. \(Mrs\.\) |Dr\. \(Ms.\) |Dr\. \(Smt.\) |\(Dr\.\) |Dr\. |Dr\.|Isai |Kumari |Kum\. |Late Shri |Late Smt\. |Late \(Shri\) |Late \(Smt\) |Late |Major |Maj\. Gen\. |Maj\. |Lt\. |Gen\. |Nartaki |Prof\.\(Dr\) |Prof\. \(Dr.\) |Prof\. |Prof |Sadhguru |Sheik |Shri |Vice Adm\. |Adm\. |\(Miss\) |\(Smt\.\) |Smt\. |Smt |Mrs\. |Grp\.Capt\. |Hon\. Capt\. |Capt\. |Ustad |Begum |Begam |Sister |Rev\. |Rev |Pandit |Pandita |Pt\. |Justice |Mr\. |Col\. |Brig\.\(Retd\) |Brig\. |Late\. \(Gen\.\) |Miss |Ms\. |Ms '

Labels='''Giani 

Syed
Sayyid 
Dada 
Mir 
Bibi 
Mian
Kazi 
Haji 
Hakeem
Imam
Sheikh?
Nawab 
Maulana 
Hakim 

Sant 
Guru 

Card. 
Bishop 
Rt. \(Rev.?\) 
Rev\.? 
Mother 
Sister
Sr.
Father 
Fr. 
Pastor
Pr.

Rabbi

His Holiness 
His Eminence
H\.Em\.
Most Venerable 
Her Royal Highness Princess 
His Excellency 

Lord 
Maharaj 
Kumar 
Rajmata 
Rajkumari 
Rani 
Sir 

Justice 
Just.
Judge

Begum 
Begam 

Ustad
Isai 
Isai Mani
Nartaki 

Congressman 
Senator

Raasacharya Swami
Baba 
Rana 
Seth 
Aayu. 
Bhai 
Ashtavaidyan 
Brahmasree 
Mahashay
Pandit 
Pandita
Pt\.? 
Swami 
Sardar 
Acharya 
Vaidya 
Vaidyan 
Yogacharya 
Muni 
Sadhguru
Satguru
(Maha)?Rishi 

Subedar Major 
Hony Capt\.? 
Rear Adm\.? 
Dafadar 
Lt\.Gen\.\(Rtd\.\) 
Col.\(Retd\.\) 
Col 
Hon. Commodore 
Rear Admiral 
Admiral 
Air Chief Marshal 
Air Com\. 
Wing Cdr 
Lt\.Gen\.\(Rt\.\) 
Late\. \(Gen\.\) 
Air Marshal 
Air Mar\. 
Air Vice Marshal 
Air Vice Mar\. 
Ar\.V\.Mar\. 
Br\. 
Major 
Maj\. Gen\. 
Maj\. 
Lt\. 
Gen\. 

Dr\. Rm\. 
Dr\.\(Kum.\) 
Dr\. \(Kum.\) 
Dr\.\(Ms.\) 
Dr\.\(Mrs.\) 
Dr\. \(Mrs\.\) 
Dr\. \(Ms.\) 
Dr\. \(Smt.\) 
\(Dr\.\) 
Dr\. 
Dr\.

Late Shri 
Late Smt\. 
Late \(Shri\) 
Late \(Smt\) 
Late\.
Late 
\(Late\)
[Pp]osth.?
Posthumous
Posthmous

Prof.\(Smt\.?\) 
Prof\.\(Mrs\.\) 
Prof\.\(Dr\) 
Prof\. \(Dr.\) 
Prof\. 
Prof 

Vice Adm\. 
Adm\. 
Grp\.Capt\. 
Hon\. Capt\. 
Capt\. 
Col\. 
Brig\.\(Retd\) 
Brig\. 
Late\. \(Gen\.\) 

Shriman
Shri\.?
Mr\.? 
Th?iru
Thiruvalar
Thirumathi
Babu
Moshai
Mohashoi

Kumwari
Kumari 
Kum\. 
Sushri
Sushree
Chi.
Chiranjeevini
Srimathi
\(Miss\) 
\(Smt\.\) 
Smt\. 
Smt 
Mrs\. 
Miss 
Ms\. 
Ms '''


#group them
#figure out the order ^(?=.*Prof)(?=.*Smt)
#optional prefix = (
#optional suffix = ).

# prefix='\('
# suffix='[\.\)]'
# lookahead=lambda x:"(?=.*{0})".format(x)
# prefix_suffix_lookahead=lambda x:"(?=.*{1}?{0}{2}?)".format(x,prefix,suffix)
# acad=["Prof","Dr","Smt","Mrs","Miss","Ms"]
# def genlookaheadregex(tokenlist):
# 	r=''
# 	for i in tokenlist:
# 		r=r+lookahead(i)
# 	return r

# title honorific salutation

re_women=r'(M(i|r)?ss?\.?)|((Smt|Kum)(ari)?\.?)' #add begum sister rani lady etc
re_airforce=r'(Air (Vice )?Mar(\.|shal)?)|Ar\.V\.Mar\.|Wing Cdr|Air Com\.'
re_navy=r'Hon. Commodore |(Rear )?Admiral |(Vice )?Adm\. '
re_mil=r'Lt\.Gen\.\(Rt\.\) |Late\. \(Gen\.\) |Br\. |Lt\. |Maj(or|\.)? (Gen\.)?|Gen\. |Grp\.Capt\. |Hon\. Capt\. |Capt\. |Col\. |Brig\.(\(Retd\))? '
re_rel_h=r'Swami |Acharya |Vaidyan? |Yogacharya |Muni |Sant |Guru |Sadhguru |Pandita? |Pt\.? |His Holiness ' 
re_rel_m='Syed |Bibi |Mohammed |Mir |Sheikh? |Maulana |Hakim |Ustad |Begum |Begam '
re_rel_c='Mother |Sister |Rev\.? |Father |Fr\. |Card. |Bishop '
re_royal=r'Her Royal Highness Princess |Sardar |Nawab |Congressman |His Excellency |Lord |Lady |Sir |Maharaj |Kumar |Rajmata |Rajkumari |Rani |Most Venerable |Justice |Kazi '
re_dead='Late|Posthumus'
re_dr='Dr'
re_prof='Prof'
re_art=r'Isai |Nartaki |Ustad '
mr_or_miss=r'Mi?(r|s)s?\.?'
brckt=lambda x:r'\(?{0}\)?'.format(x)

def flatten(l):
    aaa=[]
    for i in l:
        aaa.extend(i)
    return aaa

# uses positive lookahead (?=[A-Z]) which will not consume chars where multiple caps occur one after another
allcharsbforeUpperPL='(.)(?=[A-Z])'
allcharbforeSpacePL='(.)(?= )'
allcharbforeDot='(.)\.'
def charseqStats(df, prop):
	matches=flatten(dash[prop].apply(lambda x:re.findall(pat,x)).tolist())
	vc=p.value_counts(matches).value_counts()
	print('total', vc.count())
	print(vc)


# this adds () around each group in ops where its reqd to work out which title name has
gtitles="|".join("({0})".format(i) for i in titles.split('|'))

# repeating single Capital followed by period
is_initial=re.compile('([A-Z]\.)+?') 
def get_allinitials(listofnames, isinitial=re.compile('([A-Z]\.)+?')):
	allinitials=set()
	for fullname in listofnames:
		for token in fullname.split():
			initlist=re.findall(isinitial, token)
			if len(initlist)<2:
				allinitials.update(initlist)
			else:
				print(initlist)
	return allinitials


initial=lambda n: ' '.join([i[0]+'.' for i in n.split(' ')[:-1]]) +' '+ n.split(' ')[-1]
tightinitial=lambda n: ''.join([i[0]+'.' for i in n.split(' ')[:-1]]) +' '+ n.split(' ')[-1]

#name - dProps['label']
initlabels=lambda namelist:{initial(i):i for i in namelist }
tinitlabels=lambda namelist:{tightinitial(i):i for i in namelist }

def seperate(name):
	n=list(name)
	U=''.join(['U' if i.isupper()==True else '_' for i in n])
	s=''.join(['s' if i==' ' else '_' for i in n])
	d=''.join(['d' if i=='.' else '_' for i in n])
	print(name)
	pprint([U, s, d], width=len(U), compact=True)

def addU(name):
	m='';n=list(name)
	for i in n:
		if i.isupper()==True:
			o='U'
		elif i == ' ':
			o='s'
		elif i == '.':
			o='d'
		else:
			o='_'
		m=m+o
	return m

#pprint(sorted([add(dash.loc[i,'name']) for i in range(0,20)], reverse=True))

def subtract(name):
	m='';n=list(name)
	for i in n:
		if i.isupper()==True:
			o='_'
		elif i == ' ':
			o='_'
		elif i == '.':
			o='_'
		else:
			o=i
		m=m+o
	return m

def drawN(k):
	n=list(dash.loc[k,'name'])
	U=[1 if i.isupper()==True else 0 for i in n]
	s=[2 if i==' ' else 0 for i in n]
	d=[3 if i=='.' else 0 for i in n]
	print(dash.loc[k,'name'])
	pprint([U, s, d], compact=True)
	pprint([U[i]+s[i]+d[i] for i in range(0,len(n))], compact=True)
		
# NOTE - this is additive - each subseq pattern relies on what previous pattern has captured
# '[_]+','_'  >> 113 combos
# '(s_)+','b' >> 40
# '(_d)+','h' >> 27
# '(bd)+','I' >> 19
ub=dash['name'].apply(add).replace('[_]+','_',regex=True).replace('(s_)+','b',regex=True).replace('(_d)+','h',regex=True).replace('(bd)+','I',regex=True).replace('(hI)+','P',regex=True)
ub.value_counts().sort_index(ascending=False)
# hb       1808
# h_b        66
# h_Ihb       2
# h_Ib        3
# _b       2161
# _Ihb       65
# _Ih_b       1
# _Ih_        1
# _Ih         3
# _Ib       160
# _I_b       15
# _IPhb       1
# _IPb        2
# Phb        41
# Ph_b        3
# Pb        157
# P_b       117
# P_Ib        9

#without p
# _I_b        15
# _Ib        160
# _Ih          3
# _IhIb        2
# _IhIhb       1
# _Ih_         1
# _Ih_b        1
# _Ihb        65
# _b        2161
# hI_Ib        9
# hI_b       116
# hIb        157
# hIhI_b       1
# hIh_b        3
# hIhb        41
# h_Ib         3
# h_Ihb        2
# h_b         66
# hb        1808

# this will print the names matching a particular seq eg:h_b
#dash.iloc[ub[ub.str.contains('h_b')].index]['name']

#def merge():
	#U/s/d+_=U/s/d
	#_+_=_
