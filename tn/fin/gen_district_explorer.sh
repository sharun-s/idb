rm district_explorer/*.html
# create details
parallel -a ../TNDistricts "./findinExpenditure.sh {} > district_explorer/{}.html"
# create index
parallel -a ../TNDistricts "printf '<div><a href=district_explorer/{}.html target=details >{}</a>';./findinExpenditure.sh {} | wc -l;printf '</div>'" > district_explorer.html

