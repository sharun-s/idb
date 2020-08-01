rm basic_explorer/*.html
#for each income detail file in data/revenue generate a html summary
parallel './summary2html.py {.} > basic_explorer/{.}.html'  ::: `find data/revenue/*.csv -printf "%f "`
# from the html produces dump Titles and Filenames into index
ls basic_explorer/*.html | parallel  'grep -HPo2 "h3>\K(.*?)(?=  Year)"'|sort > index
# convert index to html
python3 gen_index.py
# remove tmp file
rm index
