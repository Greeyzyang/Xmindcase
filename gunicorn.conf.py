# -*- coding: utf-8 -*-
# @Time : 2022/5/25 15:00
# @Author : Greey
# @FileName: gunicorn.conf.py
# @Email : yangzhi@lingxing.com
# @Software: PyCharm
import multiprocessing
workers = multiprocessing.cpu_count()       #worker推荐的数量为当前的CPU个数*2 + 1
#worker_class = "gevent"  # 采用gevent库，支持异步处理请求，提高吞吐量
bind = "0.0.0.0:5000"