import sys
import pandas as p
import matplotlib.pyplot as plt
df=p.read_csv(sys.argv[1], header=None, comment='#')
if len(df) == 0:
	sys.exit()
df.columns=header=['State','2017','2018','2019']
fig = plt.figure(facecolor="#001f3f",figsize=(8.,6.4))#272822")
fig.suptitle(r"Percentage of Rural Population getting Drinking Water", color="#ffcc33", fontsize=16)
ax1 = fig.add_subplot(111, frameon=False)
ax1.set_facecolor('none')#"#002f4f")
ax1.set_alpha(0.1)
ax1.tick_params(axis='y', colors='#E6DB74')#FD971F')
ax1.tick_params(axis='x', colors='#E6DB74')#FD971F')
ax1.spines['bottom'].set_color('#001f3f')#'#ccc107')
ax1.spines['top'].set_color('#001f3f') 
ax1.spines['right'].set_color('#001f3f')
ax1.spines['left'].set_color('#001f3f')
ax1.set_xticks(range(0,4))
ax1.set_xticklabels(['2017','2018','2019'])
df[df['State'].isin(['Andhra Pradesh','Karnataka','Kerala','Tamil Nadu','Telangana'])].set_index('State').T.plot(kind='line',style='o-', ax=ax1)
l=ax1.legend(loc='lower left', ncol=5, bbox_to_anchor=(-0.05, 1.01), frameon=False, facecolor='none')
for text in l.get_texts():
    text.set_color("#efdecc")
fig.savefig(sys.argv[1].rsplit('csv',1)[0]+'png',format='png',facecolor=fig.get_facecolor())