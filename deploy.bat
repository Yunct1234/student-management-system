@echo off
echo ================================================
echo OceanBase 学生管理系统 - 部署脚本
echo ================================================

REM 检查Python环境
echo 检查Python环境...
python --version

REM 安装依赖
echo 安装Python依赖...
pip install pymysql colorama

REM 初始化数据库
echo 是否初始化数据库？(y/n)
set /p init_db=
if "%init_db%"=="y" (
    python scripts\setup_database.py
)

REM 测试连接
echo 测试数据库连接...
python scripts\test_connection.py

echo 部署完成！
echo 运行 'python main.py' 启动系统
pause
