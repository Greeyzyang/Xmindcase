# -*- coding: utf-8 -*-
# @Time : 2022/5/13 16:31
# @Author : Greey
# @FileName: tapdfunc.py
# @Email : yangzhi@lingxing.com
# @Software: PyCharm
import re
# import pandas as pd
from Common.log import MyLog
import json
import requests
from Config.tapdapi import *
import requests.packages.urllib3.util.ssl_
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = 'ALL'
requests.packages.urllib3.disable_warnings()
requests.adapters.DEFAULT_RETRIES = 5   #增加重连次数


class Tapd:

    def __init__(self, excelpath):
        self.__excelpath = excelpath
        self.log = MyLog()
        self.__username = "yangzhi@lingxing.com"
        self.__password = "jCkTtQoU+UCoVPzSZN2fww=="
        self.__session = requests.session()
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36",
                       'Connection': 'keep-alive'}

    def tapd_login(self):
        data = {
            "data[Login][ref]": "https://www.tapd.cn/company/participant_projects?from=left_tree2",
            "data[Login][encrypt_key]": "cIAOpJatenCp7aQV/xOwHpdPrUW61SYrZLnT3p14/ZY=",
            "data[Login][encrypt_iv]": "jj6iYoJ/XYtVYsnF8Qm8Fw==",
            "data[Login][site]": "TAPD",
            "data[Login][via]": "encrypt_password",
            "data[Login][email]": self.__username,
            "data[Login][password]": self.__password,
            "data[Login][login]": "login",
            "dsc_token": "opPJmcyJnXjIXss4"}

        r = self.__session.post(url=API_LOGIN, headers=self.headers, data=data, verify=False)
        if "工作台" not in r.text:
            self.log.error("Login failed, please check whether the login information is normal!")
        self.log.info("Login successed")

    def tapd_importcase(self, testxmind_id, import_type, excle_path):
        '''

        :param testxmind_id: 测试xmind id
        :param import_type: 导入类型
        :param excle_path: 文件路劲
        :return: 确认导入接口url
        '''
        data = {
            "data[tcase][extra_params]": "",
            "data[tcase][import_type]": import_type,   #add  新增   #update  更新
            "data[tcase][selected_category_id]": testxmind_id,
            "data[tcase][Apply]": "下一步",
            "dsc_token": "opPJmcyJnXjIXss4"
        }
        file = {
            "content": open(str(excle_path), 'rb'),    #必须做字符串转换
        }
        r = self.__session.post(url=API_IMPORTTESTCASE, headers=self.headers, data=data, files=file, allow_redirects=False)
        if "Location" not in r.headers.keys():
            self.log.error(f"Import failed, please check whether the import information is normal! {testxmind_id}")
        else:
            self.log.info(f"{import_type} successed {testxmind_id}")
        return r.headers['Location']

    def tapd_confirmimport(self, url, testxmind_id):
        '''

        :param url: 确认导入接口url
        :param testxmind_id: 测试xmind id
        :return:
        '''
        data = {
            "data[tcase][selected_category_id]": testxmind_id,
            "data[tcase][Apply]": "确认导入",
            "dsc_token": "opPJmcyJnXjIXss4"
        }
        r = self.__session.post(url=url, headers=self.headers, data=data, verify=False)
        if "批量复制" not in r.text:
            self.log.error(f"Confirm import failed, please check whether the confirm import information is normal! {testxmind_id}")
        else:
            self.log.info(f"Confirm import successed {testxmind_id}")

        # f = open(r'1.txt', 'w')
        # print(r.text, file=f)


    def tapd_addparentdirectory(self, testsuite, testmoudle):
        '''

        :param testsuite: 测试套件id
        :param testmoudle: 测试模块
        :return: 目录id
        '''
        data = {
            "data[TcaseCategory][id]": "",
            "data[TcaseCategory][parent_id]": testsuite,      #测试用例父路径-如：物流(测试套件)
            "data[TcaseCategory][name]": testmoudle,
            "data[TcaseCategory][description]": ""
        }
        r = self.__session.post(url=API_ADDTESTCASE_PARENTDIR, headers=self.headers, data=data, verify=False)
        if "id" not in r.json().keys():
            self.log.error(f"Create testcase path failed, please check whether the testcase path information is normal!  {testmoudle}")
        else:
            self.log.info(f"Create testcase path successed {testmoudle}")
        return r.json()['id']

    def tapd_searchtestcase(self, testxmind_id, page: str = None):
        '''

        :param testxmind_id: 测试xmind ID
        :param page: 页数
        :return: 返回页数和ID的字典
        '''
        params = {
            "category_id": testxmind_id,
            "data[Filter][name]": "",
            "data[Filter][id]": "",
            "data[Filter][creator]": "",
            "fields": "%5B%22name%22%2C%22id%22%2C%22creator%22%5D",
            "Model_name": "Tcase",
            "perage": "50",
            "page": page
        }
        r = self.__session.get(url=API_SEARCHTESTCASE, headers=self.headers, params=params, verify=False)
        casenameid_list = re.findall('<span title=\"(\s*\d+)\">', r.text)
        pages = re.findall('<span class="current-page">\d+/(\d+)</span>', r.text)
        if casenameid_list[0] not in r.text:
            self.log.error(f"Search testcase  failed, please check whether the search testcase information is normal! {casenameid_list}")
        else:
            self.log.info(f"Search testcase  successed {casenameid_list}")
        if len(pages) > 0:
            return {
                'casenameid_list': casenameid_list,
                'pages': pages[0]
            }
        else:
            return {
                'casenameid_list': casenameid_list,
            }
        # f = open(r'1.txt', 'w')
        # print(r.text, file=f)


    def tapd_delete_testcase(self, casenameid_list: list):
        '''

        :param casenameid_list: 需求ID 列表
        :return:
        '''
        newcasenameid_list = ['112020273100' + x for x in casenameid_list]
        data = {
            "data[tcase_ids][]": newcasenameid_list
        }
        r = self.__session.post(url=API_DELETECASE, headers=self.headers, data=data, verify=False)
        if 'success' not in r.text:
            self.log.error(f"Delete testcase  failed, please check whether the delete testcase information is normal! {casenameid_list}")
        else:
            self.log.info(f"Delete testcase  successed {casenameid_list}")

    def tapd_delete_dir(self, testxmind_id):
        '''

        :param testxmind_id: 测试xmind id
        :return:
        '''
        r = self.__session.get(url=API_DELETEDIR + testxmind_id, headers=self.headers, verify=False)
        if 'success' not in r.text:
            self.log.error(f"Delete testdir  failed, please check whether the delete testcase information is normal! {testxmind_id}")
        else:
            self.log.info(f"Delete testdir  successed {testxmind_id}")

class UploadTestcas(Tapd):

    def __init__(self, excelpath):
        super().__init__(excelpath)
        self.__excelpath = excelpath

    def create_casecatalog(self, testsuite, testmoudle, testxmind):
        with open('./Config/casetest_category.json', encoding='utf-8') as f:  # casetest_category文件和tapd目录保持一致
            casetest_directory = json.load(f)
        if testsuite not in casetest_directory.keys():
            testsuite_id = self.tapd_addparentdirectory(0, testsuite)  # 0,代表处在“所有的”这层路径
            testmoudle_id = self.tapd_addparentdirectory(testsuite_id, testmoudle)
            testxmind_id = self.tapd_addparentdirectory(testmoudle_id, testxmind)
            casetest_directory[testsuite] = testsuite_id
            casetest_directory[testmoudle] = testmoudle_id  # 新增的目录会记录到三级目录
            casetest_directory[testxmind] = testxmind_id
        elif testmoudle not in casetest_directory.keys():
            testmoudle_id = self.tapd_addparentdirectory(casetest_directory[testsuite], testmoudle)
            testxmind_id = self.tapd_addparentdirectory(testmoudle_id, testxmind)
            casetest_directory[testmoudle] = testmoudle_id
            casetest_directory[testxmind] = testxmind_id
        elif testxmind not in casetest_directory.keys():
            testxmind_id = self.tapd_addparentdirectory(casetest_directory[testmoudle], testxmind)
            casetest_directory[testxmind] = testxmind_id
        else:
            testxmind_id = casetest_directory[testxmind]
        json_str = json.dumps(casetest_directory, indent=4, ensure_ascii=False)
        with open('./Config/casetest_category.json', "w+", encoding="utf-8") as f:
            f.write(json_str)
        return testxmind_id

    def delete_by_page(self, testxmind_id, result_dict: dict):
        if "pages" in result_dict.keys():
            for i in range(1, int(result_dict['pages'])+1):
                result = self.tapd_searchtestcase(testxmind_id, page="1")
                self.tapd_delete_testcase(result['casenameid_list'])
        else:
            result = self.tapd_searchtestcase(testxmind_id, page="1")
            self.tapd_delete_testcase(result['casenameid_list'])

    def uploadcase(self, testsuite, testmoudle, testxmind):
        try:
            self.tapd_login()
            testxmind_id = self.create_casecatalog(testsuite, testmoudle, testxmind)
            url = self.tapd_importcase(testxmind_id, 'add', self.__excelpath)
            self.tapd_confirmimport(url, testxmind_id)
        except:
            self.log.error("Failed to upload Excel, Please check the relevant interfaces!")
            raise BaseException("Failed to uploadcase, Please check the relevant interfaces!")

    def updatecase(self, testxmind):
        try:
            self.tapd_login()
            with open('./Config/casetest_category.json', encoding='utf-8') as f:
                casetest_directory = json.load(f)
            testxmind_id = casetest_directory[testxmind]
            result = self.tapd_searchtestcase(testxmind_id)
            self.delete_by_page(testxmind_id, result)
            url = self.tapd_importcase(testxmind_id, 'add', self.__excelpath)
            self.tapd_confirmimport(url, testxmind_id)
        except:
            self.log.error("Failed to updatecase, Please check the relevant interfaces!")
            raise BaseException("Failed to updatecase, Please check the relevant interfaces!")

    def deletecase(self, testxmind):
        try:
            self.tapd_login()
            with open('./Config/casetest_category.json', encoding='utf-8') as f:
                casetest_directory = json.load(f)
            testxmind_id = casetest_directory[testxmind]      #最新的excel
            result = self.tapd_searchtestcase(testxmind_id)
            self.delete_by_page(testxmind_id, result)
            self.tapd_delete_dir(testxmind_id)  #删除xmind这层路径
            del casetest_directory[testxmind]
            json_str = json.dumps(casetest_directory, indent=4, ensure_ascii=False)
            with open('./Config/casetest_category.json', "w+", encoding="utf-8") as f:
                f.write(json_str)
        except:
            self.log.error("Failed to deletecase, Please check the relevant interfaces!")
            raise BaseException("Failed to deletecase, Please check the relevant interfaces!")