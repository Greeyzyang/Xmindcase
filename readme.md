#使用说明
## 用户通过git命令上传测试用例（xmind）
* 上传命名如下：   
  `git config --global user.name "杨志"`
  
  `git config --global user.email yangzhi@lingxing.com`
  
  `git clone http://gitlab.ak.xyz/qa/xmindtestcase.git`
  
  `cd xmindtestcase`
  
  `将要上传的文件拖到对应的文件下`
  
  `git add .`
  
  `git commit -m "备注信息"`

  `git remote add origin http://gitlab.ak.xyz/qa/xmindtestcase.git`
  
  `git push -u origin master`
  
* 测试用例编写规范如下
  
  1. 限制4级目录
  2. 一级目录需要添加笔记类型
     
     用例类型：空/功能测试/安全性测试/性能测试/其他
     
     用例状态：空/正常/待更新/已废弃
     
     需求ID：空/系统存在的需求ID
     
     创建人：Tapd注册名
     
     迭代
  3. 四级目录添加笔记类型（前置条件）
    
  4. 禁止修改删除tapd目录名称（包含次级目录）
  
  5. 兼容以前的用例目录导入（xmind文件名称不可以和之前目录名称一样）   