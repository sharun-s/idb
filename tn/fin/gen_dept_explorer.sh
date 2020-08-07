This file is outdated - was useful for prototyping - now use pythin dept-summary2html.py

rm dept_explorer/*.html
#for each income detail file in data/revenue generate a html summary
parallel './summary2html.py {.} > SOMEDIR/{.}.html'  ::: `find data/revenue/*.csv -printf "%f "`
# from the html produces dump Titles and Filenames into index
ls SOMEDIR/*.html | parallel  'grep -HPo2 "h3>\K(.*?)(?=  Year)"'|sort > index
# convert index to html
python3 gen_index.py
# remove tmp file
rm index
