echo 正在升级数据库
python manage.py migrate
python manage.py makemigrations DataBaseModel
python manage.py migrate DataBaseModel
pause