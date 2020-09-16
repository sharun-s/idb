import pandas as p
import locale
import matplotlib.pyplot as plt
import subprocess
import common

#rm old files
try:
	subprocess.run(r'rm data/cag/viz/cagMainTabl*.png',shell=True)
except Exception as e:
	pass

title='Tamil Nadu Flow of Funds - Budget Estimate 2020-2021'

def newfig():
	fig = plt.figure(facecolor="#001f3f")#,figsize=(8.,6.4))
	fig.suptitle(title, color="#00efde", fontsize=16)
	ax = fig.add_subplot(111, frameon=False)
	ax.set_facecolor("#002f4f")
	ax.set_alpha(0.1)
	ax.spines['bottom'].set_color('white')#'#ccc107')
	ax.spines['top'].set_color('white') 
	ax.spines['right'].set_color('white')
	ax.spines['left'].set_color('white')
	ax.tick_params(axis='y', colors='#E6DB74')#FD971F')
	ax.tick_params(axis='x', colors='#E6DB74')#
	return fig,ax

locale.setlocale(locale.LC_NUMERIC, '')
c=p.read_csv('tn-cag-maintable.csv')#,comment='#',header=None,skiprows=1)
columns=['Rev','Tax','GST','Stamp','Land','Sales,Trade','Excise','Share of Union Tax','Other',
								'Non-Tax Rev',
								'Grants',
								'CapRec','CR-Recoveries','CR-Other','CR-Borrowing',
								'Total Inflow',
								'RevEx',
								'Expenditure','Interest','Salaries','Pension','Subsidy',
								'Investments','Capex','sal',
								"Sector Wise Expenditure",
								"General Sector","GS-Revenue","GS-Capital",
								"Social Sector","SS-Revenue","SS-Capital",
								"Economic Sector","ES-Revenue","ES-Capital","ES-Grants",
								'RevEx+CapEx',"Loans Disbursed",'RevDef','FiscalDef','PrimaryDef','Year','Month']

colours = {}
for i,name in enumerate(columns):
	colours[name]=plt.cm.tab20.colors[i%20]

# check map
#for i,j in enumerate(columns):
#  print(i,j,c.columns[i])
c.columns=columns
#c.Month.apply(locale.atof)
#c=c.drop([7,9,14]) # drop estimate rows month = 9999 and row for 2019 March which falls under fy 2018
c.set_index(['Year','Month'],inplace=True)
c.sort_values(['Year','Month'],inplace=True)

def dumpPie(cols, filename):
	fig,ax=newfig()
	w=c.loc[2020.0,9999.0][cols].plot.pie(ax=ax,labels=cols,colors=[colours[key] for key in cols])
	for t in w.texts:
		t.set_color("#efdecc")
	y=w.get_yaxis()
	y.label.set_visible(False)
	fig.savefig(filename,format='png',facecolor=fig.get_facecolor())

def dumpGroups(groups, filename):
	fig,ax=newfig()
	vals=[]
	labels=[]
	colors=[]#"#00d0ff","#ffc107",'#00ff88','#AE81FF','#A6E22E','#F92672'
	budget2020=c.loc[2020.0,9999.0]
	for group in groups:
		labels.append(group)
		colors.append(groups[group]['color'])
		if isinstance(groups[group]['columns'],list):
			amt=sum(budget2020[v] for v in groups[group]['columns'])
			labels[-1]=labels[-1]+"\n"+str(common.format_indian(amt*10000000))
			vals.append(amt)
		else:
			amt=budget2020[groups[group]['columns']]
			labels[-1]=labels[-1]+"\n"+str(common.format_indian(amt*10000000))
			vals.append(amt)
	print(labels)
	print(vals)
	_,wt,at=ax.pie(vals,labels=labels,colors=colors,autopct='%1.1f%%')
	#print(t)
	#print(at)
	ax.axis('equal')
	for t in wt:
		t.set_color("#efdecc")
	y=ax.get_yaxis()
	y.label.set_visible(False)
	fig.savefig(filename,format='png',facecolor=fig.get_facecolor())

tree={'root':{'Total Inflow':{
					'Rev':{
						'Tax':{'GST':None,'Stamp':None,'Land':None,'Sales,Trade':None,'Excise':None,'Share of Union Tax':None,'Other':None},
						'Non-Tax Rev':None,
						'Grants':None
					},
					'CapRec':{'CR-Recoveries':None,'CR-Other':None,'CR-Borrowing':None} 
				},
			'RevEx+CapEx':{
					'RevEx':{'Expenditure':None,'Intrest':None,'Salaries':None,'Pension':None,'Subsidy':None},
					'Investments':{'Capex':None,'sal':None}
				},
			'Loans Disbursed':None
			}
		}

def siblingsBeforeAfter(child,allchildren):
	idx=allchildren.index(child)
	if idx==0:
		return None,allchildren[idx+1:]
	if idx+1<len(allchildren):
		return allchildren[:idx],allchildren[idx+1:]
	if idx+1==len(allchildren):
		return allchildren[:idx],None
	print(idx)

from collections import defaultdict 

# class TreeNode(object):
#   """docstring for TreeNode"""
#   def __init__(self, arg):
#     #super(TreeNode, self).__init__()
#     self.arg = arg
#     self.childrenOf={}
#     self.parent=

nodesAtlevel=defaultdict(list)
levelOf={}
parentOf={}
cnt=0
#uptolevel=int(sys.argv[2])  
#convert flat csv into hierarchical json
def parsetree(treedict, parent=None,level=0):
	for child in treedict.keys():
		if parent!=None:
			if parent not in childrenOf:
				childrenOf[parent]=[child]
				parentOf[child]=parent
				nodesAtlevel[level].append(parent)
				levelOf[parent]=level
			else:
				childrenOf[parent].append(child)
				parentOf[child]=parent
			if child not in childrenOf:
				childrenOf[child]=[]#str(level+1)+'_'+str(len(nodes))
				nodesAtlevel[level].append(child)
				levelOf[child]=level
				parentOf[child]=parent
			#edges.append((nodes[parent],nodes[child]))
		if isinstance(treedict[child], dict):
			parsetree(treedict[child], parent=child,level=level+1)

def get_subtree(node,tree):
	for i in tree:
		if isinstance(tree[i],dict):
			if i == node:
				return tree[i]
			get_subtree(node,tree[i])
	return None
 
#bf_walk('2020',tree,None)
b=r'data/cag/viz/cagMainTabl'
#parsetree(tree,'2020')
#nodes=list[childrenOf.keys()]
#print('Is it ordered?', nodes)

#dumpPie(nodes[0],b+'0.png')
# for i in nodes[1:]:
#   p=parentOf[i]
#   gp=parentOf[p]
#   before,after = siblingsBeforeAfter(i,childrenOf(gp))
#   allprioirwedges=[]
#   for pb in before:
#     flattendlist of all children = get_subtree(pb,tree)
#   siblings=childrenOf(p)
#   before after = i siblings

# dumpPie(['Total Inflow','RevEx+CapEx','Loans Disbursed'],b+'1.png')
# dumpPie(['Total Inflow','Rev','Loans Disbursed'],b+'1.png')
# dumpPie(['Rev','RevEx+CapEx','Loans Disbursed'],b+'2.png')
# dumpPie(['Rev','CapRec','RevEx+CapEx','Loans Disbursed'],b+'3.png')
# dumpPie(['Tax','Non-Tax Rev','Grants','CapRec','RevEx+CapEx','Loans Disbursed'],b+'4.png')
# dumpPie(['GST','Stamp','Land','Sales,Trade','Excise','Share of Union Tax','Other','Non-Tax Rev','Grants','CapRec','RevEx+CapEx','Loans Disbursed'],b+'5.png')

# dumpPie(['Tax','Non-Tax Rev','Grants','CR-Recoveries','CR-Other','Investments','RevEx','Loans Disbursed','CR-Borrowing'],b+'6.png')

#dumpGroups({'Tax':None,'Non-Tax Rev':None,'Grants':None,},'7.png')

# dumpGroups({'Borrowing':{'columns':['CR-Borrowing'],'color':'red'},
# 			'Revenue Inflow':{'columns':['Tax','Non-Tax Rev','Grants'],'color':'green'},
# 			'Inflow from Investments':{'columns':['CR-Recoveries','CR-Other'],'color':'green'},
# 			'Expenditure':{'columns':['Investments','RevEx','Loans Disbursed'],'color':'yellow'}},
# 			b+'8.png')

#"#00d0ff","#ffc107",'#00ff88','#AE81FF','#A6E22E','#F92672'
dumpGroups({'Borrowing':{'columns':['CR-Borrowing'],'color':'red'},
			'Inflow':{'columns':['Tax','Non-Tax Rev','Grants','CR-Recoveries','CR-Other'],'color':'#00d0ff'},
			'Outflow':{'columns':['Investments','RevEx','Loans Disbursed'],'color':'#00ff88'}},
			b+'1.png')

dumpGroups({'Borrowing':{'columns':['CR-Borrowing'],'color':'red'},
			'Inflow':{'columns':['Tax','Non-Tax Rev','Grants','CR-Recoveries','CR-Other'],'color':'#00d0ff'},
			'Outflow':{'columns':['Investments','Expenditure','Salaries','Pension','Subsidy','Loans Disbursed'],'color':'#00ff88'},
			'Interest Dues':{'columns':['Interest'],'color':'#ffcc33'}},
			b+'2.png')

dumpGroups({'Borrowing':{'columns':['CR-Borrowing'],'color':'red'},
			'Inflow':{'columns':['Tax','Non-Tax Rev','Grants','CR-Recoveries','CR-Other'],'color':'#00d0ff'},
			'Outflow':{'columns':['Investments','Expenditure','Subsidy','Loans Disbursed'],'color':'#00ff88'},
			'Salaries+Pension':{'columns':['Salaries','Pension'],'color':'#00cc88'},
			'Interest Dues':{'columns':['Interest'],'color':'#ffcc33'},
			},
			b+'3.png')

dumpGroups({'Borrowing':{'columns':['CR-Borrowing'],'color':'red'},
			'Inflow':{'columns':['Tax','Non-Tax Rev','Grants','CR-Recoveries','CR-Other'],'color':'#00d0ff'},
			'Outflow':{'columns':['Investments','Expenditure','Loans Disbursed'],'color':'#00ff88'},
			'Subsidy':{'columns':['Subsidy'],'color':'#00cc66'},
			'Salaries+Pension':{'columns':['Salaries','Pension'],'color':'#00cc88'},
			'Interest Dues':{'columns':['Interest'],'color':'#ffcc33'},
			},
			b+'4.png')

dumpGroups({'Borrowing':{'columns':['CR-Borrowing'],'color':'red'},
			'Inflow':{'columns':['Tax','Non-Tax Rev','Grants','CR-Recoveries','CR-Other'],'color':'#00d0ff'},
			'Investments':{'columns':['Investments'],'color':'#44dd22'},
			'Outflow':{'columns':['Expenditure','Loans Disbursed'],'color':'#00ff88'},
			'Subsidy':{'columns':['Subsidy'],'color':'#00cc66'},
			'Salaries+Pension':{'columns':['Salaries','Pension'],'color':'#00cc88'},
			'Interest Dues':{'columns':['Interest'],'color':'#ffcc33'},
			},
			b+'5.png')

dumpGroups({'Borrowing':{'columns':['CR-Borrowing'],'color':'red'},
			'Inflow':{'columns':['Tax','Non-Tax Rev','Grants','CR-Recoveries','CR-Other'],'color':'#00d0ff'},
			'Investments':{'columns':['Investments'],'color':'#44dd22'},
			'Loans Disbursed':{'columns':['Loans Disbursed'],'color':'#eebb0c'},
			'Other Outflow':{'columns':['Expenditure'],'color':'#00ff88'},
			'Subsidy':{'columns':['Subsidy'],'color':'#00cc66'},
			'Salaries+Pension':{'columns':['Salaries','Pension'],'color':'#00cc88'},
			'Interest Dues':{'columns':['Interest'],'color':'#ffcc33'},
			},
			b+'6.png')

dumpGroups({'Borrowing':{'columns':['CR-Borrowing'],'color':'red'},
			'Grants':{'columns':['Grants'],'color':'#5588d0'},
			'Other Inflow':{'columns':['Non-Tax Rev','Tax','CR-Recoveries','CR-Other'],'color':'#00d0ff'},
			'Outflow':{'columns':['Investments','RevEx','Loans Disbursed'],'color':'#00ff88'}},
			b+'12.png')

dumpGroups({'Borrowing':{'columns':['CR-Borrowing'],'color':'red'},
			'Grants':{'columns':['Grants'],'color':'#5588d0'},
			'Taxes':{'columns':['Tax'],'color':'#77d0cc'},
			'Other Inflow':{'columns':['Non-Tax Rev','CR-Recoveries','CR-Other'],'color':'#00d0ff'},
			'Outflow':{'columns':['Investments','RevEx','Loans Disbursed'],'color':'#00ff88'}},
			b+'13.png')

dumpGroups({'Borrowing':{'columns':['CR-Borrowing'],'color':'red'},
			'Grants':{'columns':['Grants'],'color':'#5588d0'},
			'GST':{'columns':['GST'],'color':'#77d0cc'},
			'Other Taxes':{'columns':['Share of Union Tax','Stamp','Land','Sales,Trade','Excise','Other'],'color':'#55d0cc'},
			'Other Inflow':{'columns':['Non-Tax Rev','CR-Recoveries','CR-Other'],'color':'#00d0ff'},
			'Outflow':{'columns':['Investments','RevEx','Loans Disbursed'],'color':'#00ff88'}},
			b+'14.png')

dumpGroups({'Borrowing':{'columns':['CR-Borrowing'],'color':'red'},
			'Grants':{'columns':['Grants'],'color':'#5588d0'},
			'GST':{'columns':['GST'],'color':'#77d0cc'},
			'Share of Union Tax':{'columns':['Share of Union Tax'],'color':'#99d0cc'},
			'Other Tax':{'columns':['Stamp','Land','Sales,Trade','Excise','Other'],'color':'#55d0cc'},
			'Other Inflow':{'columns':['Non-Tax Rev','CR-Recoveries','CR-Other'],'color':'#00d0ff'},
			'Outflow':{'columns':['Investments','RevEx','Loans Disbursed'],'color':'#00ff88'}},
			b+'15.png')

dumpGroups({'Borrowing':{'columns':['CR-Borrowing'],'color':'red'},
			'Grants':{'columns':['Grants'],'color':'#5588d0'},
			'GST':{'columns':['GST'],'color':'#77d0cc'},
			'Share of Union Tax':{'columns':['Share of Union Tax'],'color':'#99d0cc'},
			'VAT+Excise(TASMAC?)':{'columns':['Sales,Trade','Excise'],'color':'#aac0bc'},
			'Other Tax':{'columns':['Stamp','Land','Other'],'color':'#55d0cc'},
			'Other Inflow':{'columns':['Non-Tax Rev','CR-Recoveries','CR-Other'],'color':'#00d0ff'},
			'Outflow':{'columns':['Investments','RevEx','Loans Disbursed'],'color':'#00ff88'}},
			b+'16.png')

dumpGroups({"Administration":{'columns':["GS-Revenue","GS-Capital"],'color':'red'},
	"Other":{'columns':["SS-Revenue","SS-Capital","ES-Revenue","ES-Capital","ES-Grants"],'color':'blue'}},b+'17.png')

dumpGroups({"Administration":{'columns':["GS-Revenue"],'color':'red'},
	"Admin Investments":{'columns':["GS-Capital"],'color':'pink'},
	"Other":{'columns':["SS-Revenue","SS-Capital","ES-Revenue","ES-Capital","ES-Grants"],
	'color':'blue'}},b+'18.png')

dumpGroups({"Admin":{'columns':["GS-Revenue","GS-Capital"],'color':'red'},
	"Social":{'columns':["SS-Revenue","SS-Capital"],'color':'green'},
	"Other":{'columns':["ES-Revenue","ES-Capital","ES-Grants"],'color':'blue'}
	}
	,b+'19.png')

dumpGroups({"Admin":{'columns':["GS-Revenue","GS-Capital"],'color':'red'},
	"Social":{'columns':["SS-Revenue"],'color':'green'},
	"Social Investment":{'columns':["SS-Capital"],'color':'#22ee77'},
	"Other":{'columns':["ES-Revenue","ES-Capital","ES-Grants"],'color':'blue'}
	}
	,b+'20.png')


dumpGroups({"Admin":{'columns':["GS-Revenue","GS-Capital"],'color':'red'},
	"Social":{'columns':["SS-Revenue","SS-Capital"],'color':'green'},
	"Economic":{'columns':["ES-Revenue","ES-Capital","ES-Grants"],'color':'#2244ee'}
	}
	,b+'21.png')

dumpGroups({"Admin":{'columns':["GS-Revenue","GS-Capital"],'color':'red'},
	"Social":{'columns':["SS-Revenue","SS-Capital"],'color':'green'},
	"Economic":{'columns':["ES-Revenue"],'color':'#2244ee'},
	"Economic Investments":{'columns':["ES-Capital","ES-Grants"],'color':'#4466aa'}
	}
	,b+'22.png')


#dumpGroups({"General Sector":{columns:["GS-Revenue","GS-Capital"],'color':'red'},
#	"Others":{'columns':["SS-Revenue","SS-Capital","ES-Revenue","ES-Capital","ES-Grants"],'color':'blue'}},b+'17.png')

# dumpGroups({'Borrowing':{'columns':['CR-Borrowing'],'color':'red'},
# 			'Grants':{'columns':['Grants'],'color':'#5588d0'},
# 			'GST':{'columns':['GST'],'color':'#77d0cc'},
# 			'Share of Union Tax':{'columns':['Share of Union Tax'],'color':'#99d0cc'},
# 			'VAT+Excise(TASMAC?)':{'columns':['Sales,Trade','Excise'],'color':'#aac0bc'},
# 			'Other Inflow':{'columns':['Non-Tax Rev','Stamp','Land','Other','CR-Recoveries','CR-Other'],'color':'#00d0ff'},
# 			'Outflow':{'columns':['Investments','RevEx','Loans Disbursed'],'color':'#00ff88'}},
# 			b+'17.png')

#['Tot Inflow','RevEx+CapEx','Loans Disbursed']].pie(ax=ax)
# #for rev deficit
# c[['Rev','RevEx']].pie(ax=ax)
# #1+2a+2b - Inflows expluding borrowing - this is used in Fiscal Def
# c[['Rev','CR-Recoveries','CR-Other']].pie(ax=ax)
# #4 +5 +8 - Outflow
# c[['RevEx','Investments','Loans Disbursed']].pie(ax=ax)
# #Outflows exluding Interest payments - used in Primary Def
# #4(a)+(c)+(d)+(e)}+(5)+(8)
#c[['RevDef','FiscalDef']].plot()

# def bf_walk(name):
#   if fam:
#     children=list(fam.keys())
#     #if parent==None:
#     #  print(name,children)
#     for child in fam:
#       test=siblings(child,children)
#       if test!=None:
#         added,remaining=test
#         try:
#           if parent==None:
#             parent=[]
#             idx=children.index(child)
#           else:
#             idx=parent.index(name)
#           if isinstance(added,list):
#             for j in added.reverse():
#               parent.insert(idx+1,j)
#           else:
#             parent.insert(idx+1,added)
#           parent.extend(remaining)
#           bf_walk(child,fam[child],parent)
#         except Exception as e:
#           #print("ERROR",child,name,parent, test)
#           #print(e)
#           pass
#         print(parent)
