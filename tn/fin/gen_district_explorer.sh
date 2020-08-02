rm district_explorer/*.html
# create details
parallel -a ../TNDistricts "./findinExpenditure.sh {} | python3 -c 'import sys;import pandas as p;df=p.read_csv(sys.stdin,header=None);print(df.to_html(header=False,index=False,border=0,columns=[1,6]))' > district_explorer/{}.html"
# create index
parallel -a ../TNDistricts "printf '<div><a href=district_explorer/{}.html target=details >{}</a>';./findinExpenditure.sh {} | wc -l;printf '</div>'" > district_explorer.html

