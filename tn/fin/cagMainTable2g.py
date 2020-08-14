import pandas as p
import locale
import matplotlib.pyplot as plt

title='Tamil Nadu Monthly Key Indicators - CAG'

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

locale.setlocale(locale.LC_NUMERIC, '')
c=p.read_csv('tn-cag-maintable.csv',comment='#',header=None,skiprows=1)
c.columns=['Rev','Tax','GST','Stamp','Land','Sales,Trade','Excise','Share of Union Tax','Other','Non-Tax Rev','Grants','CapRec','CR-Recoveries','CR-Other','CR-Borrowing','RevEx','Expenditure','Intrest','Salaries','Pension','Subsidy','Investments','Capex','sal',"Sector Wise Expenditure","General Sector","GS-Revenue","GS-Capital","Social Sector","SS-Revenue","SS-Capital","Economic Sector","ES-Revenue","ES-Capital","ES-Grants",'RevEx+CapEx',"Loans Disbursed",'RevDef','FiscalDef','PrimaryDef','Year','Month']
c.sort_values(['Year','Month'],inplace=True)
#c.Month.apply(locale.atof)
c=c.drop([7,9,14]) # drop estimate rows month = 9999 and row for 2019 March which falls under fy 2018
c.set_index(['Year','Month'],inplace=True)

#c[['Rev','RevEx','Capex','CR-Borrowing']].plot()
#c[['Rev','RevEx','Capex','CR-Borrowing','Tax']].plot()
#c[['Rev','RevEx','Capex','CR-Borrowing','Tax','Non-Tax Rev','Grants']].plot()
c[['RevEx','Investments','CR-Borrowing']].plot(ax=ax,stacked=True)
fig.savefig(r'data/cag/viz/cagMainTabl.png',format='png',facecolor=fig.get_facecolor())
#c[['RevDef','FiscalDef']].plot()

