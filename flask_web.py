# -*- coding: utf-8 -*-
# @Time : 2022/5/23 16:47
# @Author : Greey
# @FileName: flask_web.py
# # @Email : yangzhi@lingxing.com
# # @Software: PyCharm
from Common.log import *
from Common.tapdfunc import UploadTestcas
from Common.xmind import Excel
from flask import Flask, request, jsonify
import gitlab
import os
from Common.dingding import DingTalkRobot
import json
from functools import partial

app = Flask(__name__)

#172.18.19.247/callback

def get_xmindexcel(xmind):
    gl = gitlab.Gitlab("http://10.48.8.10/", "-ZELBW6fhdgm3cbdz6cv")
    project = gl.projects.get(1650)  # 项目对应id
    xmind_name = xmind.split("/")[2]
    f = project.files.get(file_path=xmind, ref='master')
    content = f.decode()  # 二进制写入文件
    with open(xmind_name, "wb") as f:
        f.write(content)
    xmindpath = os.path.abspath(xmind_name)
    Excel(xmindpath).create_excel()
    return {
        'xmind_name': xmind_name,
        'xmindpath': xmindpath
    }

@app.route('/callback', methods=['POST'])
def callback():
    global result, xmind_namelist
    xmind_namelist = []
    body = request.json
    print("Submit information:" + str(body))
    if body["commits"][0]['author']['name']:
        push_username = body["commits"][0]['author']['name']
        fun = partial(DingTalkRobot().send_message, push_username)
    else:
        raise ValueError("Please configure submission information,eg: git config --global user.name '杨志', git config --global user.email yangzhi@lingxing.com")
    try:
        if len(body["commits"][0]["added"]) > 0 and ".xmind" in ("".join(body["commits"][0]["added"])):
            xmind_path = body["commits"][0]["added"]
            for xmind in xmind_path:
                result = get_xmindexcel(xmind)
                UploadTestcas(Excel(result['xmindpath'])).uploadcase(xmind.split("/")[0], xmind.split("/")[1], xmind.split("/")[2].strip(".xmind"))
                xmind_namelist.append(result['xmind_name'])
                os.remove(str(result['xmindpath']))
                os.remove(str(Excel(result['xmindpath'])))
            fun(xmind_namelist, "已上传")
            MyLog.info(f"New documents submitted this time, eg {xmind_path}")

        elif len(body["commits"][0]["modified"]) > 0 and ".xmind" in ("".join(body["commits"][0]["modified"])):
            xmind_path = body["commits"][0]["modified"]
            for xmind in xmind_path:
                result = get_xmindexcel(xmind)
                UploadTestcas(Excel(result['xmindpath'])).updatecase(xmind.split("/")[2].strip(".xmind"))
                xmind_namelist.append(result['xmind_name'])
                os.remove(str(result['xmindpath']))
                os.remove(str(Excel(result['xmindpath'])))
            fun(xmind_namelist, "已修改")
            MyLog.info(f"New documents modified this time, eg {xmind_path}")

        elif len(body["commits"][0]["removed"]) > 0 and ".xmind" in ("".join(body["commits"][0]["removed"])):
            xmind_path = body["commits"][0]["removed"]
            for xmind in xmind_path:
                xmind_name = xmind.split("/")[2]
                UploadTestcas('').deletecase(xmind.split("/")[2].strip(".xmind"))
                xmind_namelist.append(xmind_name)
            fun(xmind_namelist, "已删除")
            MyLog.warning(f"Delete the entire XMIND file, ef {xmind_path}")

        elif len(body["commits"][0]["added"]) == 0 and len(body["commits"][0]["removed"]) and\
            len(body["commits"][0]["removed"]) == 0:
            MyLog.warning("User submitted information is empty, please check!")  #允许为空的提交

        else:
            MyLog.error(f"Please upload the file type of xmind")
            raise TypeError(f"Please upload the file type of xmind")

        if push_username:
            return jsonify({'code': 200, 'msg': '触发成功!', 'result': 'ok'})
        else:
            return jsonify({'code': 500, 'msg': '触发失败', 'result': 'fail'})

    except:
        MyLog.error("Please check “callback” method")
        raise("Please check “callback” method")

    finally:
        print("Currently submitted：" + push_username)
        regularclean_log(7)      #7天清理一次日志

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
