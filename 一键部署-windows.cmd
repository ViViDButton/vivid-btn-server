@echo off
echo ����MySQL Command Line�ֶ�ִ����������
echo ------------------------------------
echo     CREATE DATABASE vivid_btn_db"
echo ------------------------------------
pause
cls
echo ���ڳ�ʼ�������ļ�
cd config
ren config-simple.ini config.ini
cd ..
echo -------------------------------------
echo ���ڳ�ʼ�����ݿ�
python manage.py migrate
echo -------------------------------------
echo ���ڳ�ʼ������
python manage.py loaddata model_data.json
python manage.py loaddata user_data.json
echo -------------------------------------
echo ������8000�˿���������
python manage.py runserver 0.0.0.0:8000
pause
