import sys
#print("files to process-", len(sys.argv)-1)
import pandas as p
import numpy as np
import matplotlib.pyplot as plt
df=p.read_csv(sys.argv[1], names=['date','zno','name','confirmed','recovered','hospitalized','deceased'])
df['positives']=np.insert(np.diff(df['confirmed']), 0, df['confirmed'][0])
df['hosp']=np.insert(np.diff(df['hospitalized']), 0, df['hospitalized'][0])
df['rec']=np.insert(np.diff(df['recovered']), 0, df['recovered'][0])
df['death']=np.insert(np.diff(df['deceased']), 0, df['deceased'][0])

#df['c-r']=df['confirmed']-df['recovered']
fig = plt.figure(facecolor="#001f3f")
fig.suptitle("COVID-19 - "+sys.argv[1].replace('.csv','').upper().replace('\\',''), color="#00efde", fontsize=16)
# Divide the figure into a 2x1 grid, and give me the first section
ax1 = fig.add_subplot(211)
ax1.set_title('Daily', color="#00d0ff")
ax1.get_xaxis().set_visible(False)
ax1.set_facecolor("#002f4f")
ax1.tick_params(axis='y', colors='#ffc107')
ax1.yaxis.label.set_color('#ffc107')

ax1.spines['bottom'].set_color('#001f3f') #'#ccc107')
ax1.spines['top'].set_color('#001f3f') 
ax1.spines['right'].set_color('#001f3f')
ax1.spines['left'].set_color('#001f3f')
# Divide the figure into a 2x1 grid, and give me the second section
ax2 = fig.add_subplot(212)
ax2.set_title('Cumulative', color="#00ddef")
ax2.set_facecolor("#002f4f")
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
df[['positives','hosp','rec','death']].plot.bar(ax=ax1, color=["#ffc107","#00d0ff",'green','red'])
ax1.legend(loc='lower left', ncol=2, 
	bbox_to_anchor=(0., 0.7, 1, .85))
ax1.axhline(y=0, color='yellow', linestyle='-')
#df[['confirmed','c-r','hospitalized','recovered']].plot(ax=ax2, color=["#ffc107",'orange','red','green'])
df[['confirmed','hospitalized','recovered']].plot(ax=ax2, color=["#ffc107","#00d0ff",'green'])
#ax2.legend(facecolor="#006f7f")
fig.savefig(sys.argv[1].replace('csv','png'),format='png',facecolor=fig.get_facecolor())