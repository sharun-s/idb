import pandas as p
import matplotlib.pyplot as plt 
from itertools import cycle
import matplotlib.dates as md
import random
import argparse

parser = argparse.ArgumentParser(description='District Evolution Timeline Grapher')
parser.add_argument('-csv', default="geo/Districts_Blocks.csv",help='input csv file default in geo directory District_blocks.csv')
#parser.add_argument('-dumpall',action="store_true", help='dump year wise as seperate graphs for anim')
parser.add_argument('--outfile', help='output filename specify extn')
args = parser.parse_args()

df=p.read_csv(args.csv, parse_dates=['FormationDate'])
df.sort_values(by=['FormationDate'], inplace=True)
fig, ax = plt.subplots(figsize=(8, 6.4))

ax.set(title='District Evolution Timeline')

prev=None
prevff=None
y=0
c=cycle([-2,2])
f={}
dead=[]
gap=-4
origgap=250
placeholder=10

def set_yloc(base=0, sameyear=0):
	print(base,sameyear,len(f),gap)
	if base:
		return base+(gap*len(f))+sameyear
	global placeholder
	placeholder=placeholder+1
	f[random.randint(0,10)]='dead district'
	return (origgap*placeholder)
	#return len(f)*gap

for date, dist, frm in df[['FormationDate','District','FormedFrom']].itertuples(index=False,name=None):	
	print(prev, date.year)
	if date.year==prev:
		sameyr=80#gap
	else:
		sameyr=0
	if prevff == frm:
		sameyr=80
	else:
		sameyr=0
	prev=date.year
	prevff=frm

	if frm.find("original") >-1:
		y=y+origgap
		ax.text( date,y, dist, fontsize=8, horizontalalignment='right')
	elif frm.find(' and ') > -1:
		pr=frm.split(' and ')
		print("m2one ",frm,dist)
		for i in pr:
				ax.annotate("",
                xy=(md.date2num(date), set_yloc(f[pr[1]][1],sameyr)), xycoords='data',
                xytext=(f[i][0],f[i][1]), textcoords='data',
                arrowprops=dict(arrowstyle="-", color='salmon',
                                alpha=1,
                                #connectionstyle="angle,angleA=0,angleB=90,rad=5"
                                connectionstyle="angle,angleA=75,angleB=0,rad=15"
                                ))
				#f[i].append(1)
			#ax.arrow(md.date2num(date), f[pr[0]][1], f[i][0]-md.date2num(date),f[i][1], alpha=0.1, width=.2)
		y=set_yloc(f[pr[1]][1],sameyr)
		ax.text( date,y, dist, fontsize=8, horizontalalignment='left')
	elif frm.find('Arcot') > -1:
		print("AR ",frm,dist)
		y=set_yloc(0,0)
		ax.text( date,y, dist, fontsize=8, horizontalalignment='right')
		#dead.append(1)
	elif frm.find('Chingle') > -1:
		print("Ch ",frm,dist)
		y=set_yloc(0,0)
		ax.text( date,y, dist, fontsize=8, horizontalalignment='right')
		#dead.append(1)
	else:
		print("-- ",frm,f[frm][1],dist) 
		#ax.arrow(md.date2num(date), f[frm][1]-1, f[frm][0]-md.date2num(date),1, alpha=0.1, width=.2,connectionstyle="angle,angleA=-90,angleB=180,rad=0")
		ax.annotate('',
                xy=(md.date2num(date), set_yloc(f[frm][1],sameyr)), xycoords='data',
                xytext=(f[frm][0],f[frm][1]), textcoords='data',
                arrowprops=dict(arrowstyle="-",
                                color="0.5",
                                connectionstyle="angle,angleA=90,angleB=0,rad=5",
                                ),
                )
		y=set_yloc(f[frm][1],sameyr)
		#f[frm].append(1)
		ax.text( date,y, dist, fontsize=8, horizontalalignment='left')

	ax.scatter(date, y, s=0)
	ax.scatter(date, 0, s=8*df.FormationDate.value_counts()[date], facecolor='red', edgecolor='k', alpha=0.5)
	f[dist]=[md.date2num(date), y]	
	print('    ',dist,y)

ax.plot((md.date2num(df.FormationDate.min()), md.date2num(df.FormationDate.max())), (0, 0), 'r', alpha=.31)
plt.setp((ax.get_yticklabels() + ax.get_yticklines() +
          list(ax.spines.values())), visible=False)

if args.outfile:
	fig.savefig(args.outfile,format='png',facecolor=fig.get_facecolor())			
else:
	plt.show()