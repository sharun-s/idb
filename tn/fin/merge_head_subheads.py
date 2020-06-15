import pandas as p
import json
import locale
locale.setlocale(locale.LC_NUMERIC, '')

import csv

f=open('meta_Heads.json')  
h=json.load(f)
f.close()

df=p.read_csv('rev_details.csv')
len(df)
#5971

# get all sub heads and values
#iterate over json and check
def walk(node,parent=None,level=0):
	for key in node.keys():
		print(level*'\t',key)
		if isinstance(node[key],dict):
			walk(node[key],parent=key,level=level+1)
		else:
			k=node[key]
			idx=df[df['head'].str.startswith(key,na=False)].index
			if not idx.empty and len(idx)==2:
				genTree(idx[0],idx[1])
			else:
				print('CHECK ',key)

from pprint import pprint
#walk(h)

def next(i,root):
	head=df.iloc[i]['head'].split('-')[0]
	print(i,head,root)
	#input('?')
	if root==None:
		return -1
	if head!=root:
		return i+1
	else:
		return -1
#df[df['head'].str.startswith('77777',na=False)].index
#traverse list make tree
#"if node has children" was an test in json traversal 
#"is node child" is test in list trav
def genTree(i, dict_parent={}, root=None):
	while True:
		head=df.iloc[i]['head'].split('-')[0]
		data=df.iloc[i][['2018', '2019Est', '2019Rev', '2020Est']]
		#if node is parent
		if data.isnull().all():
			#this is parent[head][head]
			dict_parent[head]={'desc':df.iloc[i]['desc']}
			#print(dict_parent)
			i,t=genTree(i+1,dict_parent[head],head)
			dict_parent[head].update(t)
		else:
			#node is child
			dict_parent[head]={'desc':df.iloc[i]['desc']}
			dict_parent[head].update(data.to_dict())
		#pprint(dict_parent)
		
		if next(i,root) == -1:
			break;
		else:
			i=i+1
	return i,dict_parent

i=3685
l=genTree(i)
f=open('dairy.csv','w')
tmp=json.dumps(l[1])
tmp.replace('NaN','')
json.dump(l[1],f)
f.close()


def dict_generator(indict, pre=None):
    pre = pre[:] if pre else []
    if isinstance(indict, dict):
        for key, value in indict.items():
            if isinstance(value, dict):
                for d in dict_generator(value, pre + [key]):
                    yield d
            elif isinstance(value, list) or isinstance(value, tuple):
                for v in value:
                    for d in dict_generator(v, pre + [key]):
                        yield d
            else:
                yield pre + [key, value]
    else:
        yield pre + [indict]