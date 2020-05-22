import sys
import pandas as p
import matplotlib.pyplot as plt
df=p.read_csv(sys.argv[1], comment='#')
if len(df) == 0:
	sys.exit()
df['Excise on Producer']=df['Excise']
df['Sales Tax on Consumer']=df['VAT(Sales Tax)']

fig = plt.figure(facecolor="#001f3f")#272822")
fig.suptitle("Liquor Revenues To Tamil Nadu In Crores", color="#ffcc33", fontsize=16)
# Divide the figure into a 2x1 grid, and give me the first section
ax1 = fig.add_subplot(111, frameon=False)
#ax1.set_title('Excise on Producer & Sales Tax on Consumer In Crores', color="#00d0ff")
#ax1.get_xaxis().set_visible(False)
ax1.set_facecolor('none')#"#002f4f")
#ax1.set_alpha(0.1)
ax1.tick_params(axis='y', colors='#E6DB74')#FD971F')
ax1.tick_params(axis='x', colors='#E6DB74')#FD971F')
#ax1.yaxis.label.set_color('#ffc107')
ax1.spines['bottom'].set_color('#001f3f')#'#ccc107')
ax1.spines['top'].set_color('#001f3f') 
ax1.spines['right'].set_color('#001f3f')
ax1.spines['left'].set_color('#001f3f')

ax1.set_xticklabels(df.Year.str.split('-').str[1][::2], rotation=0)
df[['Excise on Producer','Sales Tax on Consumer','Total']].plot(kind='line', ax=ax1, color=["#00c107","#00d0ff",'#ffcc33'])#00cc88'])
l=ax1.legend(loc='lower left', ncol=3, bbox_to_anchor=(0.0, .95), frameon=False, facecolor='none')
for text in l.get_texts():
    text.set_color("#efdecc")
fig.savefig(sys.argv[1].replace('csv','png'),format='png',facecolor=fig.get_facecolor())