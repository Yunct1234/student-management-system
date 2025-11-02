@echo off
echo ======================================
echo 学生管理系统 - 远程客户端
echo ======================================

REM 激活虚拟环境（如果有）
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
)

REM 设置默认远程连接参数
set REMOTE_DB_HOST=192.168.31.35
set REMOTE_DB_PORT=2881
set REMOTE_DB_USER=remote_user

REM 运行Python程序
python main.py

pause
