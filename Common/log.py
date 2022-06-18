# -*- coding: utf-8 -*-
# @Time : 2022/5/25 11:15
# @Author : Greey
# @FileName: log.py
# @Email : yangzhi@lingxing.com
# @Software: PyCharm
import logging
import os
import time
import datetime
import sys

LEVELS = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warning': logging.WARNING,
    'error': logging.ERROR,
    'critical': logging.CRITICAL
}

logger = logging.getLogger()
level = 'default'


def create_file(filename):
    path = filename[0:filename.rfind('/')]
    if not os.path.isdir(path):
        os.makedirs(path)
    if not os.path.isfile(filename):
        fd = open(filename, mode='w')
        fd.close()
    else:
        pass

def set_handler(levels):
    if levels == 'error':
        logger.addHandler(MyLog.err_handler)
    logger.addHandler(MyLog.handler)


def remove_handler(levels):
    if levels == 'error':
        logger.removeHandler(MyLog.err_handler)
    logger.removeHandler(MyLog.handler)


def get_current_time():
    return time.strftime(MyLog.date, time.localtime(time.time()))


def regularclean_log(delta_day):
    path = MyLog.path + '/Log'
    file_list = os.listdir(path)
    for file in file_list:
        cur_path = os.path.join(path, file)
        file_create_timestamp = int(os.path.getctime(cur_path))
        delta_days = (datetime.datetime.now() - datetime.timedelta(days=int(delta_day)))
        timestamp = int(time.mktime(delta_days.timetuple()))
        if file_create_timestamp < timestamp:  # 创建时间在n天前的文件删除
            os.remove(os.path.join(cur_path))

class MyLog:
    # path = os.getcwd()
    path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    currentdate = datetime.datetime.now().strftime('%Y-%m-%d')
    log_file = path + '/Log/' + currentdate + '.log'
    err_file = path + '/Log/' + currentdate + '_error.log'
    logger.setLevel(LEVELS.get(level, logging.NOTSET))
    create_file(log_file)
    create_file(err_file)
    date = '%Y-%m-%d %H:%M:%S'
    handler = logging.FileHandler(log_file, encoding='utf-8', mode='a')
    err_handler = logging.FileHandler(err_file, encoding='utf-8', mode='a')


    @staticmethod
    def debug(log_meg):
        set_handler('debug')
        logger.debug("[DEBUG " + get_current_time() + "]" + log_meg)
        remove_handler('debug')

    @staticmethod
    def info(log_meg):
        set_handler('info')
        logger.info("[INFO " + get_current_time() + "]" + log_meg)
        remove_handler('info')

    @staticmethod
    def warning(log_meg):
        set_handler('warning')
        logger.warning("[WARNING " + get_current_time() + "]" + log_meg)
        remove_handler('warning')

    @staticmethod
    def error(log_meg):
        set_handler('error')
        logger.error("[ERROR " + get_current_time() + "]" + log_meg)
        remove_handler('error')

    @staticmethod
    def critical(log_meg):
        set_handler('critical')
        logger.critical("[CRITICAL " + get_current_time() + "]" + log_meg)
        remove_handler('critical')



