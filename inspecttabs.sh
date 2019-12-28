#!/bin/bash
# reads open tabs and checks names against local zim or print infobox of name found in localzim

# This will print mapped name in zim
#while read x; do ./check.sh "$x"; done <<< `./fftabs.py | cut -d"(" -f1`

# This prints infobox
while read x; do ./ib "$x"; done <<< `./fftabs.py | cut -d"(" -f1`