import sys
#print("files to process-", len(sys.argv)-1)
import pandas as p
import geopandas as gp
import matplotlib.pyplot as plt
df=p.read_csv(sys.argv[1])
if len(df) == 0:
	sys.exit()

fig = plt.figure(facecolor="#001f3f")

#l1=gp.read_file('../tn_boundary.json')
l2=gp.read_file('../tn_dist.json')
ax3 = fig.add_subplot(339, frameon=False)
l2.plot(ax=ax3, facecolor='#0099dd',edgecolor='blue',label='TN',alpha=.78, linewidth=0)
ax3.get_xaxis().set_visible(False)
ax3.get_yaxis().set_visible(False)
ax3.set_facecolor("#002f4f")
ax3.set_alpha(0.3)
ax3.spines['bottom'].set_color('white')#'#ccc107')
ax3.spines['top'].set_color('white') 
ax3.spines['right'].set_color('white')
ax3.spines['left'].set_color('white')
l2[l2.Name==sys.argv[1].replace('.csv','')].plot(ax=ax3,facecolor='#ffcc55',edgecolor='blue',alpha=.73, linewidth=0) 

df['d'] =  p.to_datetime(df['d'], format='%m%d')
df['d'] = df['d'].apply(lambda x: x.replace(year=2020))

filled = p.date_range('03-23-2020', '04-30-2020').to_frame()
filled.columns=['d']
merged = p.merge(filled, df, on='d', how='left')

# fill in missing dates #####
#filled=p.Series([i for i in range(323,332)]+[i for i in range(401,426)]).to_frame()
#filled.columns=['d']
#merged = p.merge(filled, df, on='d', how='left')
#############################

fig.suptitle("COVID-19 - "+sys.argv[1].replace('.csv','').upper(), color="#00efde", fontsize=16)
# Divide the figure into a 2x1 grid, and give me the first section
ax1 = fig.add_subplot(211, frameon=False)
ax1.set_title('Daily Positives', color="#00d0ff")
ax1.get_xaxis().set_visible(False)
ax1.set_facecolor('none')#"#002f4f")
#ax1.set_alpha(0.1)
ax1.tick_params(axis='y', colors='#ffc107')
#ax1.yaxis.label.set_color('#ffc107')
ax1.spines['bottom'].set_color('#001f3f')#'#ccc107')
ax1.spines['top'].set_color('#001f3f') 
ax1.spines['right'].set_color('#001f3f')
ax1.spines['left'].set_color('#001f3f')
# Divide the figure into a 2x1 grid, and give me the second section
ax2 = fig.add_subplot(212, frameon=False)
ax2.set_title('Cumulative', color="#00ddef")
ax2.set_facecolor('none')#"#002f4f")
ax2.set_alpha(0.1)
ax2.get_xaxis().set_visible(False)
ax2.spines['bottom'].set_color('#001f3f')#'ccc107')
ax2.spines['top'].set_color('#001f3f') 
ax2.spines['right'].set_color('#001f3f')
ax2.spines['left'].set_color('#001f3f')
#ax2.tick_params(axis='x', colors='red')
ax2.tick_params(axis='y', colors='#ffc107')
#ax2.yaxis.label.set_color('#ffc107')
ax2.xaxis.label.set_color('#004f3f')
#ax2.set_yscale("log")
merged.groupby(['d']).tot.sum().plot('bar', ax=ax1, color="#ffc107")
merged.groupby(['d']).tot.sum().cumsum().plot('line', ax=ax2, color="#ffc107")


fig.savefig(sys.argv[1].replace('csv','png'),format='png',facecolor=fig.get_facecolor())