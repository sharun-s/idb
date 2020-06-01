echo "pos actives rec deaths"
python3 getstats.py > tmp
grep "$1" tmp