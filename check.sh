#!/bin/bash
# check "m k gandhi"
# check m k gandhi
# somename | check - not supported do something like the following
# cut -d"," -f3 tn_awards.csv | cut -d" " -f2- > tn_names 
# while read in; do ./check.sh "$in"; done < cat tn_names > names_found
# while read in; do ./check.sh "$in"; done < cat tn_names > names_found

ZIM=/home/s/kiwix-html5/www/wikipedia_en_all_2016-12.zim

query () {
	TXT=`zimdump -f "$x" -i -t "$ZIM" | grep -Po "\s(title:|type:|idx:|redirect index:)\ +\K(.*)"`
}

#if [ $# -gt 1 ]
# below condition same as test ! -t 0 ie stdin is not open because of pipe 
#if [ ! -t 0 ]
#then
#	read x
#else
x="$*"
#fi 

if [ "$x" = "" ]; then
	exit 1; 
fi
#echo "Looking for $x"
query
readarray -t args <<< $TXT
#echo ${args[@]}

if [ "${args[2]}" = "redirect" ]
then
	#echo "Redirected and found $( zimdump -o "${args[3]}" -p "$ZIM" | grep -Po "<title>\K.*(?=<)" )"
	echo "$( zimdump -o "${args[3]}" -p "$ZIM" | grep -Po "<title>\K.*(?=<)" )"
#elif [ "${args[2]}" = "article" ]
else
	#echo "found" "$x"
	echo "$x"
fi
