# -*- coding: utf-8 -*-
# @Time : 2022/5/16 10:08
# @Author : Greey
# @FileName: tapdapi.py
# @Email : yangzhi@lingxing.com
# @Software: PyCharm


'''TAPD相关接口'''

API_LOGIN = "https://www.tapd.cn/cloud_logins/login?ref=https%3A%2F%2Fwww.tapd.cn%2Fcompany%2Fparticipant_projects%3Ffrom%3Dleft_tree2"
API_IMPORTTESTCASE = "https://www.tapd.cn/20202731/imports/import_tcase"
API_ADDTESTCASE_PARENTDIR = "https://www.tapd.cn/20202731/sparrow/tcase_categories/quick_add_category"
API_DELETECASE = "https://www.tapd.cn/20202731/sparrow/tcase/batch_delete?action_timestamp=90601273"
API_DELETEDIR = "https://www.tapd.cn/20202731/sparrow/tcase_categories/quick_delete_category/"
API_SEARCHTESTCASE = "https://www.tapd.cn/20202731/sparrow/tcase/tcase_list"
# API_GETTESTCASE_PARENTDIRECTORY =
# API_CONFIRMIMPORT = "http://www.tapd.cn/20202731/imports/import_preview_tcase/38158210/add/1120202731001000119"
API_GETCASELIST = "https://www.tapd.cn/20202731/sparrow/tcase/tcase_list?left_tree=1"