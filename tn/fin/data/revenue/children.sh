#!/bin/bash 

# can be 2019Est,2019Rev,2020Est
year="${2:-2018}" 
echo \#"$1", `cat revrec-summary.json | jq --arg code "$1" '..| to_entries? |.[]| select(.value.code? ==$code) | .key '`
#cat revrec-summary.json | jq -r --arg code "$1" --arg year "$year" '..|select(.code? == $code )|to_entries[]| [(.key), (.value|.[$year]?)]|map(.)|@csv'

cat rev_details.json | jq -r --arg code "$1" --arg year "$year" '..|select(.code? == $code)|to_entries[]|[(.key),(.value | with_entries(select(.key|startswith("Total ")))? |.[]|.[$year]? )] | @csv' | sed '1d;$d'