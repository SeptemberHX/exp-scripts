#!/bin/bash

function scp_func
{
	node=0
	while test $# -gt 0
	do
		curl --location --request POST "$1:8082/simulate/start" \
			--header 'Content-Type: application/json' \
			--data-raw '{
		    "index": 0,
		    "group": 1,
	            "node": '$node'
		}
	    	'
		node=$((node + 1))
		shift
	done
}

list=$(kubectl get nodes -o wide | tail -5 | awk -F ' ' '{print $6}')
scp_func $list
