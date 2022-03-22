#!/bin/bash

function scp_func
{
	while test $# -gt 0
	do
		scp -i ~/distributed-tokyo.pem ~/MSystemEvolution/MGateway/target/MGateway-1.0-SNAPSHOT.jar ubuntu@$1:/home/ubuntu
		shift
	done
}

list=$(kubectl get nodes -o wide | tail -5 | awk -F ' ' '{print $6}')
scp_func $list
