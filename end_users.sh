#!/bin/bash

function scp_func
{
	while test $# -gt 0
	do
		curl --location --request POST "$1:8082/simulate/sotp" 
		shift
	done
}

list=$(kubectl get nodes -o wide | tail -5 | awk -F ' ' '{print $6}')
scp_func $list
