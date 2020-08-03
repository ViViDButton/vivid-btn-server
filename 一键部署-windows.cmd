@echo off
echo 请在MySQL Command Line手动执行以下命令
echo ------------------------------------
echo     CREATE DATABASE vivid_btn_db"
echo ------------------------------------
pause
cls
echo 正在初始化配置文件
cd config
ren config-simple.ini config.ini
cd ..
echo -------------------------------------
echo 正在初始化数据库
python manage.py migrate
echo -------------------------------------
echo 正在初始化数据
python manage.py loaddata model_data.json
python manage.py loaddata user_data.json
echo -------------------------------------
echo 正在在8000端口启动服务
python manage.py runserver 0.0.0.0:8000
pause
