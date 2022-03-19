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
DATA_DIR = './data/phy_data'


def read_users(user_data_path):
    with open(user_data_path) as f:
        users = json.load(f)
    return users


def request(user_id, func_obj):
    # todo: 同步请求，而非异步！
    gateway = 'http://localhost:8081/gateway/request'
    data = {
        'svcId': f'service{func_obj["svcIndex"]}',
        'patternUrl': func_obj['patternUrl'],
        'userId': user_id,
        'timestamp': datetime.datetime.now().timestamp() * 1000,
        'callbackUrl': 'http://localhost:8082/callback',
        'params': {
            'status': 'Success',
            'valueMap': {}
        }
    }
    t1 = datetime.datetime.now().timestamp()
    logger.debug(f'==> {user_id}|{data["svcId"]}|{data["patternUrl"]}|{t1}')
    response = requests.post(gateway, json=json.dumps(data))
    t2 = datetime.datetime.now().timestamp()
    logger.debug(f'<== {user_id}|{data["svcId"]}|{data["patternUrl"]}|{t2}')

    if response.status_code == 200:
        status = response.json()['status']
        logger.debug(f'{user_id}|{data["svcId"]}|{data["patternUrl"]}|{status}|{t2 - t1}')
    else:
        logger.debug(f'{user_id}|{data["svcId"]}|{data["patternUrl"]}|Fail|{t2 - t1}')


class MyThread(threading.Thread):
    def __init__(self, thread_id, name, delay, user_id, user_data, func_map):
        threading.Thread.__init__(self)
        self.threadID = thread_id
        self.name = name
        self.delay = delay
        self.user_id = user_id
        self.user_data = user_data
        self.func_map = func_map
        self._running = True

    def run(self):
        print("开始模拟：" + self.name)
        self.simulate_user()
        print("退出模拟：" + self.name)

    def simulate_user(self):
        i = 1
        func_i = 0
        while self._running:
            func_i = func_i % len(self.func_list)
            request(f'{self.user_id}_{i}', self.func_map[self.func_list[func_i]])
            sleep(random.randint(0, 5))

    def stop(self):
        self._running = False


thread_list = []  # type: List[MyThread]


def start_simulate(users, func_map):
    for user_id in users:
        thread = MyThread(user_id, f'Thread-{user_id}', 0, user_id, users[user_id], func_map)
        thread.start()
        thread_list.append(thread)


@app.route('/simulate/start', methods=['POST'])
def start():
    if request.method == 'POST':
        data_json = json.loads(request.data.decode('utf-8'))
        data_index = data_json['index']
        group = data_json['group']
        user_data_path = os.path.join(DATA_DIR, group, f'users_{data_index}.json')
        users = read_users(user_data_path)

        with open(os.path.join(DATA_DIR, 'share', 'func_objs.json'), 'r') as f:
            func_objs = json.load(f, object_hook=lambda d: {int(k) if k.lstrip('-').isdigit() else k: v for k, v in
                        d.items()})
        start_simulate(users, func_objs)


@app.route('/simulate/start', methods=['POST'])
def end():
    for thread in thread_list:
        thread.stop()
    thread_list.clear()


if __name__ == '__main__':
    app.run('0.0.0.0', port=8082)
