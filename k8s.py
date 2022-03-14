#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
@Project ：k8s-python 
@File ：k8s.py
@Author ：septemberhx
@Date ：2022/3/14
@Description:
"""
from typing import Dict

import yaml

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


if __name__ == '__main__':
    # Configs can be set in Configuration class directly or using helper utility
    config.load_kube_config()
    create_namespace_if_not_exist('hx-test', client)
    create_pod_with_scheme(
        scheme={
            'k8s-master': {
                'service1': 3
            }
        },
        namespace='hx-test',
        c=client
    )
