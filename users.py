#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
@Project ：k8s-python 
@File ：users.py
@Author ：septemberhx
@Date ：2022/3/19
@Description:
"""
import datetime
import json
import os.path
import random
import threading
from time import sleep
from typing import List

from flask import Flask, request

import requests

from logger import get_logger

logger = get_logger('users')
app = Flask(__name__)
DATA_DIR = './data'


def read_users(user_data_path):
    with open(user_data_path) as f:
        users = json.load(f, object_hook=lambda d: {int(k) if k.lstrip('-').isdigit() else k: v for k, v in d.items()})
    return users


def send_request(user_id, func_obj):
    # todo: 同步请求，而非异步！
    gateway = 'http://localhost:8081/gateway/request'
    data = {
        'svcId': f'Service{func_obj["svcIndex"]}',
        'patternUrl': func_obj['patternUrl'],
        'userId': user_id,
        'timestamp': int(datetime.datetime.now().timestamp() * 1000),
        'callbackUrl': 'http://localhost:8082/callback',
        'params': {
            'status': 'Success',
            'valueMap': {
                'first': func_obj['index']
            }
        }
    }
    t1 = datetime.datetime.now().timestamp() * 1000  # ms
    logger.debug(f'==> {user_id}|{data["svcId"]}|{data["patternUrl"]}|{t1}|{threading.currentThread().name}')
    response = requests.post(gateway, json=data)
    t2 = datetime.datetime.now().timestamp() * 1000  # ms
    logger.debug(f'<== {user_id}|{data["svcId"]}|{data["patternUrl"]}|{t2}|{threading.currentThread().name}')

    if response.status_code == 200:
        if 'status' in response.json():
            status = response.json()['status']
            logger.debug(f'{user_id}|{data["svcId"]}|{data["patternUrl"]}|{status}|{t2 - t1}')
        else:
            logger.debug(response.json())
    else:
        logger.debug(f'{user_id}|{data["svcId"]}|{data["patternUrl"]}|Fail|{t2 - t1}')


class MyThread(threading.Thread):
    def __init__(self, thread_id, name, delay, user_id, user_data, func_objs):
        threading.Thread.__init__(self)
        self.threadID = thread_id
        self.name = name
        self.delay = delay
        self.user_id = user_id
        self.user_data = user_data
        self.func_objs = func_objs
        self._running = True

    def run(self):
        print("开始模拟：" + self.name)
        self.simulate_user()
        print("退出模拟：" + self.name)

    def simulate_user(self):
        i = 1
        func_i = 0
        while self._running:
            func_i = func_i % len(self.user_data)
            print(self.user_data)
            send_request(f'{self.user_id}_{i}', self.func_objs[self.user_data[func_i]])
            func_i += 1
            sleep(random.randint(0, 5))

    def stop(self):
        self._running = False


thread_list = []  # type: List[MyThread]


def start_simulate(users, func_objs):
    for user_id in users:
        thread = MyThread(user_id, f'Thread-{user_id}', 0, user_id, users[user_id], func_objs)
        thread.start()
        thread_list.append(thread)


@app.route('/simulate/start', methods=['POST'])
def start():
    if request.method == 'POST':
        data_json = json.loads(request.data.decode('utf-8'))
        data_index = data_json['index']
        group = data_json['group']
        node = data_json['node']
        user_data_path = os.path.join(DATA_DIR, 'phy_data', f'group0{group}', f'users_{data_index}.json')
        users = read_users(user_data_path)

        with open(os.path.join(DATA_DIR, 'share', 'func_objs.json'), 'r') as f:
            func_objs = json.load(f, object_hook=lambda d: {int(k) if k.lstrip('-').isdigit() else k: v for k, v in
                        d.items()})
        print(users)
        start_simulate(users[node], func_objs)
    return 'ok'


@app.route('/simulate/stop', methods=['POST'])
def end():
    for thread in thread_list:
        thread.stop()
    thread_list.clear()
    return 'ok'


if __name__ == '__main__':
    app.run('0.0.0.0', port=8082)
