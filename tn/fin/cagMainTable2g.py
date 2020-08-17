import pandas as p
import locale
import matplotlib.pyplot as plt
import subprocess

#rm old files
try:
  subprocess.run(r'rm data/cag/viz/cagMainTabl*.png',shell=True)
except Exception as e:
  pass

title='Tamil Nadu Cash Flow BreakDown'

def newfig():
  fig = plt.figure(facecolor="#001f3f",figsize=(8.,6.4))
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
                'Expenditure','Intrest','Salaries','Pension','Subsidy',
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

tree={'Total Inflow':{
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
nodes={}
nodesAtlevel=defaultdict(list)
levelOf={}
cnt=0
#uptolevel=int(sys.argv[2])  
def parsetree(treedict, parent=None,level=0):
  for child in treedict.keys():
    if parent!=None:
      if parent not in nodes:
        nodes[parent]=[child]
        nodesAtlevel[level].append(parent)
        levelOf[parent]=level
      else:
        nodes[parent].append(child)
      if child not in nodes:
        nodes[child]=[]#str(level+1)+'_'+str(len(nodes))
        nodesAtlevel[level].append(child)
        levelOf[child]=level
      #edges.append((nodes[parent],nodes[child]))
    if isinstance(treedict[child], dict):
      parsetree(treedict[child], parent=child,level=level+1)

def bf_walk(name):
  if fam:
    children=list(fam.keys())
    #if parent==None:
    #  print(name,children)
    for child in fam:
      test=siblings(child,children)
      if test!=None:
        added,remaining=test
        try:
          if parent==None:
            parent=[]
            idx=children.index(child)
          else:
            idx=parent.index(name)
          if isinstance(added,list):
            for j in added.reverse():
              parent.insert(idx+1,j)
          else:
            parent.insert(idx+1,added)
          parent.extend(remaining)
          bf_walk(child,fam[child],parent)
        except Exception as e:
          #print("ERROR",child,name,parent, test)
          #print(e)
          pass
        print(parent)
      
 
#bf_walk('2020',tree,None)
b=r'data/cag/viz/cagMainTabl'
parsetree(tree,'2020')

# for i in nodes:
#   children=nodes[i]
#   l=levelOf[i]
#   if l==0:
#     dumpPie(children,b+str(l)+'.png')
#   else:
#     for c in children:
#       dumpPie(,b+str(l)+'.png')

dumpPie(['Total Inflow','RevEx+CapEx','Loans Disbursed'],b+'1.png')
dumpPie(['Rev','RevEx+CapEx','Loans Disbursed'],b+'1.png')
dumpPie(['Rev','CapRec','RevEx+CapEx','Loans Disbursed'],b+'2.png')
dumpPie(['Tax','Non-Tax Rev','Grants','CapRec','RevEx+CapEx','Loans Disbursed'],b+'3.png')
dumpPie(['GST','Stamp','Land','Sales,Trade','Excise','Share of Union Tax','Other','Non-Tax Rev','Grants','CapRec','RevEx+CapEx','Loans Disbursed'],b+'3.png')

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

