import sys, re
import pandas as p
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gp
df=p.read_csv(sys.argv[1], names=['date','zno','name','confirmed','recovered','hospitalized','deceased'])
df['positives']=np.insert(np.diff(df['confirmed']), 0, df['confirmed'][0])
df['hosp']=np.insert(np.diff(df['hospitalized']), 0, df['hospitalized'][0])
df['rec']=np.insert(np.diff(df['recovered']), 0, df['recovered'][0])
df['death']=np.insert(np.diff(df['deceased']), 0, df['deceased'][0])

zone=df['zno'].iloc[0].astype(str)
zonename=df['name'].iloc[0]
dates=re.sub(r'(\d\d)-0(\d)-2020',r'\1/\2',df['date'].iloc[0]) +'-'+re.sub(r'(\d\d)-0(\d)-2020',r'\1/\2',df['date'].iloc[-1])

#df['c-r']=df['confirmed']-df['recovered']
fig = plt.figure(facecolor="#001f3f")
fig.suptitle('Chennai Zone '+str(zone)+' - '+zonename.upper().replace('\\','')+' - '+dates, 
	color="#00efde", fontsize=16)

l2=gp.read_file('../chn-zones.json')
ax3 = fig.add_subplot(121, frameon=False)
l2.plot(ax=ax3, facecolor='#0099dd',edgecolor='blue', alpha=.78,linewidth=0)
ax3.get_xaxis().set_visible(False)
ax3.get_yaxis().set_visible(False)
ax3.set_facecolor("#002f4f")
ax3.set_alpha(0.3)
ax3.spines['bottom'].set_color('white')#'#ccc107')
ax3.spines['top'].set_color('white') 
ax3.spines['right'].set_color('white')
ax3.spines['left'].set_color('white')
l2[l2.Name==zonename].plot(ax=ax3,facecolor='#ffcc55',edgecolor='blue',alpha=.73, linewidth=0) 

# Divide the figure into a 2x1 grid, and give me the first section
ax1 = fig.add_subplot(212, frameon=False)
ax1.set_title('Daily', color="#00d0ff")
ax1.get_xaxis().set_visible(False)
ax1.set_facecolor('none')# has to be none to keep map visible
ax1.tick_params(axis='y', colors='#ffc107')
ax1.yaxis.label.set_color('#ffc107')

ax1.spines['bottom'].set_color('#001f3f') #'#ccc107')
ax1.spines['top'].set_color('#001f3f') 
ax1.spines['right'].set_color('#001f3f')
ax1.spines['left'].set_color('#001f3f')
# Divide the figure into a 2x1 grid, and give me the second section
ax2 = fig.add_subplot(211, frameon=False)
ax2.set_title('Cumulative', color="#00ddef")
ax2.set_facecolor('none')
ax2.get_xaxis().set_visible(False)
ax2.spines['bottom'].set_color('#001f3f')#'#ccc107')
ax2.spines['top'].set_color('#001f3f') 
ax2.spines['right'].set_color('#001f3f')
ax2.spines['left'].set_color('#001f3f')
#ax2.tick_params(axis='x', colors='red')
ax2.tick_params(axis='y', colors='#ffc107')
#ax2.yaxis.label.set_color('#ffc107')
ax2.xaxis.label.set_color('#004f3f')
#plt.subplots_adjust(bottom=0.2)

#df.positives.plot('bar',ax=ax1, color="#ffc107")
df[['positives','hosp','rec','death']].plot.bar(ax=ax1, color=["#ffc107","#00d0ff",'#00cc88','red'])
l=ax1.legend(loc='lower left', ncol=4, bbox_to_anchor=(0.0, -0.2), frameon=False, facecolor='none')
for text in l.get_texts():
    text.set_color("#00efde")
ax1.axhline(y=0, color='#ffcc07', linestyle='-', linewidth=0.5)
#df[['confirmed','c-r','hospitalized','recovered']].plot(ax=ax2, color=["#ffc107",'orange','red','green'])
df[['confirmed','hospitalized','recovered']].plot(legend=None, ax=ax2, color=["#ffc107","#00d0ff",'#00ff88'])
#ax2.legend(facecolor="#006f7f")

yticks = [int(i) for i in ax2.get_yticks().tolist()] # get list of ticks
for i in range(1,len(yticks)-2):
	yticks[i] = ''
ax2.set_yticklabels(yticks)

yticks = [int(i) for i in ax1.get_yticks().tolist()] # get list of ticks
for i in range(1,len(yticks)-2):
	yticks[i] = ''
ax1.set_yticklabels(yticks)

fig.savefig(sys.argv[1].replace('csv','png'),format='png',facecolor=fig.get_facecolor())