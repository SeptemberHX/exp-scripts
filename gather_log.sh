#!/bin/bash

function scp_func
{
	node=0
	mkdir ~/results
	while test $# -gt 0
	do
		scp -i ~/distributed-tokyo.pem ubuntu@$1:/home/ubuntu/exp-scripts/log.log ~/results/log_${node}.log

		node=$((node + 1))
		shift
	done
}

list=$(kubectl get nodes -o wide | tail -5 | awk -F ' ' '{print $6}')
scp_func $list
