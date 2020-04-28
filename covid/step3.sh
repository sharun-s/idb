rm *.csv *.png *.out tnd.gif
cat ~/Downloads/covid/TNDistricts | parallel grep {} '~/Downloads/covid/pdf2txr/P > {}.out'
find -type f -empty -delete
#Generate csv files from the out 
cat ~/Downloads/covid/TNDistricts | parallel 'python3 txt2stats.py {}.out > {}.csv'
find -type f -empty -delete
#merge dups
tail -n1 Tirupathur.csv >> Thirupathur.csv ; rm Tirupathur.csv
tail -n1 Thirunelveli.csv >> Tirunelveli.csv ; rm Thirunelveli.csv
sed '1d' Tiruvannamalai.csv >> Thiruvannamalai.csv; rm Tiruvannamalai.csv
rm Sivagangai*
#Generate png bar graphs from the csv files
cat ~/Downloads/covid/TNDistricts | parallel 'python3 csv2g.py {}.csv'
convert -delay 110 *.png  tnd.gif