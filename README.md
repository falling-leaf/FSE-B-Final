# FSE-B-Final

软件工程基础B组集成仓库

## 集成提示

大家可将尚未集成的子系统代码复制在 `sub_system/`文件夹中以便其他组查看及使用。

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

## 启动方法

前端：

1. 进入frontend/目录下
2. 命令行运行 `npm install`
3. 命令行运行 `npm run dev`
4. 访问 `localhost:5173`

后端：

1. 进入backend/onlinebank/目录下
2. （可选：使用新建的Python虚拟环境）
3. （对于新建的Python环境安装如下包应当足够支撑后端运行）命令行运行 `pip install pymysql django_apscheduler djangorestframework django-cors-headers python-dateutil pytz`
4. 在该目录下的onlinebank/settings.py中，修改DATABASES的内容：将密码改为自己的密码
5. 在backend/onlinebank/目录下运行 `./run.ps1`
