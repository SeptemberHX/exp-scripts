#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
@Project ：k8s-python 
@File ：k8s.py
@Author ：septemberhx
@Date ：2022/3/14
@Description:
"""

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


if __name__ == '__main__':
    # Configs can be set in Configuration class directly or using helper utility
    config.load_kube_config()
    create_namespace_if_not_exist('hx-test', client)
    create_pod_on_node('service1', 'service1:latest', 'k8s-master', 3, 'hx-test', client)
