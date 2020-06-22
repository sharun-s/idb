import pandas as p
import json,csv,pprint
import locale
locale.setlocale(locale.LC_NUMERIC, '')

f=open('meta_Heads.json')  
h=json.load(f)
f.close()

df=p.read_csv('rev_details.csv')
len(df)
#5971

def endtree(i,root,overshoot):
	head=df.iloc[i]['head'].split('-')[0]
	#input('?')
	#print(i,head,root)
	if i > overshoot:
		print('overshot ',overshoot, i,root,head)
		raise ValueError 
	if root==None or head==root:
		return True
	return False


def findend(h,i):
	idx=df[df['head'].str.contains(h,na=False)].index.to_list()
	j=idx.index(i)+1
	while df.ix[idx[j]]['desc'] != 'Total '+h:
		j=j+1
	return idx[j]


#df[df['head'].str.startswith('77777',na=False)].index
#traverse list make tree
#"if node has children" was an test in json traversal 
#"is node child" is test in list trav
def genTree(i, overshoot, root=None,subgroup=False):
	parent_tree={}
	while True:
		try:
			head=df.iloc[i]['head'].split('-')[0]
		except AttributeError as e:
			print(i, df.iloc[i]['head'])
			raise e
		#print('p ',i, head,root,subgroup, df.iloc[i]['desc'])
		data=df.iloc[i][['2018', '2019Est', '2019Rev', '2020Est']]
		desc=df.iloc[i]['desc']
		dpcode=df.iloc[i]['dpcode']
		#node is a header
		#if data.isnull().all(): < this fails if single empty space exists
		if data.apply(lambda x:True if p.isnull(x) or x==' ' else False).all():
			#this is parent[head][head]			
			parent_tree[head]={'desc':desc}
			end=findend(head, i)
			i,t=genTree(i+1, end,head)#parent_tree[head]
			parent_tree[head].update(t)
		# group detected
		elif not p.isna(dpcode) and dpcode.endswith('00'):
			if subgroup: # this indicates end of prev subgroup
				#dprint('new sub found but prev subgrp needs to be added')
				return i-1,parent_tree
			#dprint('grouping',head)
			parent_tree[head]={'desc':desc}
			parent_tree[head].update(data.to_dict())
			i,t=genTree(i+1,overshoot,head,subgroup=True)
			parent_tree[head].update(t)
			#dprint('ungrouped')
		# end of group total
		elif p.isna(dpcode) and desc.startswith('Total'):
			if subgroup:
				#dprint('total found so prev sub needs to be added')
				return i-1,parent_tree
			#parent_tree[head]={'desc':desc}
			parent_tree[desc]=data.to_dict()
		else:
			#node is child
			#dprint('adding '+head)
			parent_tree[head]={'desc':desc}
			parent_tree[head].update(data.to_dict())
		#pprint(dict_parent)
		if endtree(i,root,overshoot):
			break;
		else:
			i=i+1
			#print(i)
	return i,parent_tree

def genTree_codestrip(i, overshoot, root=None,subgroup=False):
	parent_tree={}
	while True:
		try:
			head=df.iloc[i]['head'].split('-')[0]
			desc=df.iloc[i]['desc'] if not p.isnull(df.iloc[i]['desc']) else head+' MISSING Desc' 
		except AttributeError as e:
			print(i,df.iloc[i])
			raise e
		#print('p ',i, head,root,subgroup, df.iloc[i]['desc'])
		data=df.iloc[i][['2018', '2019Est', '2019Rev', '2020Est']]
		dpcode=df.iloc[i]['dpcode']
		#node is a header
		#if data.isnull().all(): < this fails if single empty space exists
		if data.apply(lambda x:True if p.isnull(x) or x==' ' else False).all():
			#this is parent[head][head]			
			parent_tree[desc]={'code':head}
			end=findend(head, i)
			i,t=genTree_codestrip(i+1, end,head)#parent_tree[head]
			parent_tree[desc].update(t)
		# group detected
		elif not p.isna(dpcode) and dpcode.endswith('00'):
			if subgroup: # this indicates end of prev subgroup
				#dprint('new sub found but prev subgrp needs to be added')
				return i-1,parent_tree
			#dprint('grouping',head)
			parent_tree[desc]={'code':head}
			parent_tree[desc].update(data.to_dict())
			i,t=genTree_codestrip(i+1,overshoot,head,subgroup=True)
			parent_tree[desc].update(t)
		# end of group total
		elif p.isna(dpcode) and desc.startswith('Total'):
			if subgroup:
				#dprint('total found so prev sub needs to be added')
				return i-1,parent_tree
			#parent_tree[head]={'desc':desc}
			parent_tree[desc]=data.to_dict()
		else:
			#node is child
			#dprint('adding '+head)
			parent_tree[desc]={'code':head}
			parent_tree[desc].update(data.to_dict())
		#pprint(dict_parent)
		if endtree(i,root,overshoot):
			break;
		else:
			i=i+1
			#print(i)
	return i,parent_tree

def dp2node(head,desc,data,dpcode):
	#1601 06 101 DG 13105
	mjr,sub,mnr,grp,subg=dpcode.split(' ')
	#subg[0],subg[1:3],sub[3:5]
	g1=subg[0:3]
	g2=subg[3:5]
	n={mjr:{sub:{mnr:{grp:{}}}}}

def df2json(start):
	root=df.iloc[start]['head'].split('-')[0]
	tmp=[]
	output={}
	while True:
		try:
			head=df.iloc[start]['head'].split('-')[0]
		except AttributeError as e:
			print(i, df.iloc[i]['head'])
			raise e
		desc=df.iloc[i]['desc']
		data=df.iloc[i][['2018', '2019Est', '2019Rev', '2020Est']]
		dpcode=df.iloc[i]['dpcode']
		#if node is just header
		if data.isnull().all() and p.isna(dpcode):
			tmp.append(head,desc)
		else:
			dp2node(head,desc,data,dpcode)

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
# get all sub heads and values
# iterate over json and check
def walk(node,parent=None,level=0):
	tree={}
	for key in node.keys():
		#print(level*'\t',key)
		if isinstance(node[key],dict):
			tree[key]={}
			t=walk(node[key],parent=key,level=level+1)
			tree[key].update(t)
		else:
			k=node[key]
			tree[k]={}
			idx=df[df['head'].str.startswith(key,na=False)].index
			if not idx.empty and len(idx)==2:
				i,t=genTree_codestrip(idx[0],overshoot=idx[1])
				tree[k].update(t)
				#print(i,)
				#dump(df.ix[idx[0]]['head']+'_'+df.ix[idx[0]]['desc'].replace(' ','_').capitalize()+'.json',t)
			else:
				print('CHECK ',key)
	return tree

from pprint import pprint
def dump(name,data):
	f=open(name,'w')
	tmp=json.dumps(data)
	json.dump(json.loads(tmp.replace('NaN','""')),f)
	f.close()


#l=genTree(3687,3721)
#dump('dairy.json',l[1])

t=walk(h)

