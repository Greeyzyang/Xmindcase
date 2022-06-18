import xmindparser
from xmindparser import xmind_to_dict
import pandas as pd
from Common.log import MyLog
import os

xmindparser.config = {
    'showTopicId': False,  # 原有配置
    'hideEmptyValue': True,  # 原有配置
    'showStructure': False,  # 新增配置，是否展示结构值
    'showRelationship': True  # 新增配置，是否展示节点关系
}


class Xmind:

    def __init__(self, xmindpath):
        self.__xmindpath = xmindpath
        self.log = MyLog()

    def read_xmind(self):

        content = xmind_to_dict(self.__xmindpath)[0]['topic']
        title = content['title']
        notes = [note for note in content['note'].split('\n')]
        data_list = content['topics']
        return title, notes, data_list

    def parse_xmind(self, title, data_list, casedata_list: list, precontion_list: list,
                    casename=''):
        for branch in data_list:
            newcasename = casename + branch['title'] + '→'
            if 'topics' not in branch:
                if 'note' in branch:
                    precontion_list.append(branch['note'])
                else:
                    precontion_list.append('')
                newcasename = title + newcasename
                casedata_list.append(newcasename)
                continue
            new_data_list = branch['topics']
            self.parse_xmind(title, new_data_list, casedata_list, precontion_list, casename=newcasename)
        return casedata_list, precontion_list

    def list_to_pdformat(self, casedata_list, caselists=None):

        if caselists is None:
            caselists = []
        for casedata in casedata_list:
            casedata = [casedata for casedata in casedata.split('→')[:-1]]
            caselists.append(casedata)
        return caselists

    def caselevel_to_pdformat(self, caselists, level_keys=None, level_values=None):

        if level_values is None:
            level_values = []
        if level_keys is None:
            level_keys = []
        global level_value
        for list in caselists:
            if "#" not in list[1]:
                self.log.error(
                    "Please fill in the test case according to the specification and set the case level /eg '#1'")
                raise ValueError(
                    "Please fill in the test case according to the specification and set the case level /eg '#1'")
            level_keys.append(list[1].split('#')[1])
        for level_key in level_keys:
            if level_key == "0":
                level_value = "高"
            if level_key == '1':
                level_value = "中"
            if level_key == "2":
                level_value = "低"
            level_values.append(level_value)
        return level_values


class Excel(Xmind):

    def __init__(self, xmindpath):
        super().__init__(xmindpath)
        self.__xmindpath = xmindpath

    def __str__(self):
        excelname = self.__xmindpath.replace("xmind", "xlsx")
        return excelname

    @staticmethod
    def insert_col(df, col, colitems: dict):
        try:
            if col in colitems.keys():
                df.loc[:, col] = colitems[col]
        except:
            raise ValueError("请在xmind中添加--{}".format(col))

    def get_xmindnotes(self, notes: list, note_dict=None):
        if note_dict is None:
            note_dict = {}
        for note in notes:
            if "：" in note:
                note_dict[note.split("：")[0]] = note.split("：")[1].strip()
            elif ":" in note:
                note_dict[note.split(":")[0]] = note.split(":")[1].strip()
        if len(note_dict.keys()) < 5:
            raise ValueError("Please check whether the use case notes are entered completely")
        elif len(note_dict.keys()) == 5:
            if note_dict['用例类型'] not in ['', '功能测试', '性能测试', '安全性测试', '其他']:
                raise ValueError("Please check whether the use case type input is normal!")
            if note_dict['用例状态'] not in ['', '正常', '待更新', '已废弃']:
                raise ValueError("Please check whether the use case status input is normal!")
            if True:
                pass  # 需求ID的的校验，需要调用tapd接口获取已存在的需求id
        else:
            raise ValueError("Use case notes cannot exceed 5!!")
        return note_dict

    def create_excel(self):
        # 用例目录,用例名称,需求ID,前置条件,用例步骤,预期结果,用例类型,用例状态,用例等级,创建人,迭代
        title, notes, data_list = self.read_xmind()
        casedata_list, precontion_list = self.parse_xmind(title, data_list, [], [])
        pddata = self.list_to_pdformat(casedata_list)
        level_values = self.caselevel_to_pdformat(pddata)
        df = pd.DataFrame(pddata, columns=['用例目录', '用例名称', '用例步骤', '预期结果'])
        note_dict = self.get_xmindnotes(notes)
        if "需求ID" in note_dict.keys():
            df.insert(loc=2, column='需求ID', value=note_dict["需求ID"])
        else:
            raise ValueError("请在xmind中添加--用例类型")
        df.insert(loc=3, column='前置条件', value=precontion_list)
        self.insert_col(df, "用例类型", note_dict)
        self.insert_col(df, "用例状态", note_dict)
        df['用例等级'] = level_values
        self.insert_col(df, "创建人", note_dict)
        self.insert_col(df, "迭代", note_dict)
        df['用例名称'].replace("#\d+", "", regex=True, inplace=True)
        df.to_excel(self.__xmindpath.replace("xmind", "xlsx"), index=False)
        self.log.info("Generate Excel successed")

# Excel("多账号.xmind").create_excel()
