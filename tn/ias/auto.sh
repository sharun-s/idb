#!/bin/bash 
# to run 10 
# head -n37 CurrentCollectors-2020 | tail -10 | cut -d',' -f3 | grep -oE '[^ .]+$' | parallel './auto.sh {}'

curl 'https://easy.nic.in/civilListIAS/YrPrev/QryProcessCL.asp' -d 'HidQryNum=1&CboCadre=00&CboBatch=9999&txtName='"$1"'&Submit=Submit' -o "$1".html
if [ 0 -eq $? ]; then 
	python3 getCollectorInfoFromEasyNicIn.py "$1".html
fi
mv "$1".html html/
#grep "$1" "$1".csv