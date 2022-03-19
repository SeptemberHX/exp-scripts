#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
@Project ：AlgoGroupDeployment
@File ：logger.py
@Author ：septemberhx
@Date ：2021/4/8
@Description:
"""

import logging
import coloredlogs

fmt_str = '[%(asctime)s] [%(filename)s:%(lineno)s] [%(levelname)s] - %(message)s'
formatter = logging.Formatter(fmt_str)
logger_file_handler = logging.FileHandler('./log.log')
logger_terminal_handler = logging.StreamHandler()
logger_file_handler.setFormatter(formatter)
logger_terminal_handler.setFormatter(formatter)


def get_logger(name, level=logging.DEBUG):
    """
    :param name:
    :param level:
    :return:
    :rtype: logging.Logger
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(logger_file_handler)
    logger.addHandler(logger_terminal_handler)
    coloredlogs.install(fmt=fmt_str, logger=logger, level=level)
    return logger
