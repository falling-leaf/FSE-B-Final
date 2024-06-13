# FSE-B-Final
软件工程基础B组集成仓库

## 集成提示

大家可将尚未集成的子系统代码复制在`sub_system/`文件夹中以便其他组查看及使用。

在集成时，请在git commit中标注具体信息，其中包括集成模块及操作者，并在本README中进行日志的更新。

python manage.py makemigrations
python manage.py migrate

python manage.py runserver


## 更新日志

2024/6/7：创建仓库，并上传B1组前后端初步代码及前端登录界面 from B1

2024/6/8：加信用卡部分

2024/6/12: 贷款子模块完成系统管理员的上传以及本组审查员和贷款部门经理模块的上传

2024/6/12: 贷款子模块解决三个问题
1.解决user重命名问题 ——已解决
2.大组整合user，登录user之后的url跳转问题——已解决
3.解决user_id的传递，使用后端函数通过user_id获取identity_card——已解决

