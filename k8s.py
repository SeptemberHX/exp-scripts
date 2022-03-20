#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
@Project ：k8s-python 
@File ：k8s.py
@Author ：septemberhx
@Date ：2022/3/14
@Description:
"""
import json
from typing import Dict

import yaml
import sys

from kubernetes import client, config


def create_namespace_if_not_exist(namespace, c: client):
    v1 = client.CoreV1Api()
    for ns in v1.list_namespace().items:
        if ns.metadata.name == namespace:
            return
    v1.create_namespace({
        'apiVersion': 'v1',
        'kind': 'Namespace',
        'metadata': {
            'name': namespace
        }
    })


def create_pod_on_node(name, image, node_selector_value, count, namespace, c: client):
    with open('./pod.yaml') as f:
        dep = yaml.safe_load(f)
        k8s_apps_v1 = c.CoreV1Api()
        dep['spec']['containers'][0]['name'] = name
        dep['spec']['containers'][0]['image'] = image
        dep['spec']['nodeSelector']['node'] = node_selector_value
        print(dep)

        for i in range(0, count):
            dep['metadata']['name'] = f'{name}-{i}'
            k8s_apps_v1.create_namespaced_pod(body=dep, namespace=namespace)


def create_pod_with_scheme(scheme: Dict[str, Dict[str, int]], namespace, c: client):
    for node in scheme:
        for svc, count in scheme[node].items():
            create_pod_on_node(
                name=svc,
                image=f'septemberhx/{svc}:latest',
                node_selector_value=node,
                count=count,
                namespace=namespace,
                c=c
            )


def read_scheme(file_path):
    with open(file_path) as f:
        scheme_raw = json.load(f)
        scheme = {}
        for node_index_str in scheme_raw:
            scheme[f'node{node_index_str}'] = {}
            for svc_index_str in scheme_raw[node_index_str]:
                scheme[f'node{node_index_str}'][f'service{svc_index_str}'] = scheme_raw[node_index_str][svc_index_str]
    return scheme


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('No scheme.json provided.')
        exit(0)

    # Configs can be set in Configuration class directly or using helper utility
    config.load_kube_config()
    create_namespace_if_not_exist('hx-test', client)
    create_pod_with_scheme(
        scheme=read_scheme(sys.argv),
        namespace='hx-test',
        c=client
    )
