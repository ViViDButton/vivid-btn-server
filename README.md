# <span style="color:red">本项目有严重的性能问题！！！！</span>
# vivid btn 后端服务器(临时版)
---
## 环境要求

- mysql
- python

## 使用

- 创建数据库
    - 打开MySql命令行
    - 输入以下命令
    ```sql
    create database vivid_btn_db; 
    ```

- 安装依赖
```shell script
pip install -r requirements.txt
```
- 配置数据库
    - 打开vividBtnAIO/settings.py
    - 找到DATABASES，配置以下数据库连接参数
    ```
    DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'vivid_btn_db',  # 数据库名
        'HOST': '127.0.0.1',  # 地址
        'PORT': 3306,  # 端口
        'USER': 'root',  # 用户
        'PASSWORD': '1234',  # 密码
      }
    }  
    ```
- 初始化数据表
```shell script
python3 manage.py migrate
python3 manage.py makemigrations DataBaseModel
python3 manage.py migrate DataBaseModel
```
- 启动服务
```shell script
python3 manage.py runserver 0.0.0.0:8000
```

---

开发:正義desu