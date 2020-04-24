import sys
#print("files to process-", len(sys.argv)-1)
import pandas as p
import matplotlib.pyplot as plt
df=p.read_csv(sys.argv[1])

# fill in missing dates #####
filled=p.Series([i for i in range(323,332)]+[i for i in range(401,424)]).to_frame()
filled.columns=['d']
merged = p.merge(filled, df, on='d', how='left')
#############################

fig = plt.figure(facecolor="#001f3f")
fig.suptitle("COVID-19 - "+sys.argv[1].replace('.csv','').upper(), color="#00efde", fontsize=16)
# Divide the figure into a 2x1 grid, and give me the first section
ax1 = fig.add_subplot(211)
ax1.set_title('Daily Positives', color="#00d0ff")
ax1.get_xaxis().set_visible(False)
ax1.set_facecolor("#002f4f")
ax1.tick_params(axis='y', colors='#ffc107')
#ax1.yaxis.label.set_color('#ffc107')
ax1.spines['bottom'].set_color('#ccc107')
ax1.spines['top'].set_color('#001f3f') 
ax1.spines['right'].set_color('#001f3f')
ax1.spines['left'].set_color('#001f3f')
# Divide the figure into a 2x1 grid, and give me the second section
ax2 = fig.add_subplot(212)
ax2.set_title('Cumulative', color="#00ddef")
ax2.set_facecolor("#002f4f")
ax2.get_xaxis().set_visible(False)
ax2.spines['bottom'].set_color('#ccc107')
ax2.spines['top'].set_color('#001f3f') 
ax2.spines['right'].set_color('#001f3f')
ax2.spines['left'].set_color('#001f3f')
#ax2.tick_params(axis='x', colors='red')
ax2.tick_params(axis='y', colors='#ffc107')
#ax2.yaxis.label.set_color('#ffc107')
ax2.xaxis.label.set_color('#004f3f')

merged.groupby(['d']).tot.sum().plot('bar', ax=ax1, color="#ffc107")
merged.groupby(['d']).tot.sum().cumsum().plot('bar', ax=ax2, color="#ffc107")

fig.savefig(sys.argv[1].replace('csv','png'),format='png',facecolor=fig.get_facecolor())