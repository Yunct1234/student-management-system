@echo off
echo ======================================
echo 学生管理系统 - 远程客户端安装
echo ======================================

echo 检查Python环境...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 错误: 未检测到Python，请先安装Python 3.8+
    pause
    exit /b 1
)

echo 创建虚拟环境...
python -m venv venv

echo 激活虚拟环境...
call venv\Scripts\activate.bat

echo 安装依赖包...
pip install -r requirements.txt

echo 配置环境变量...
copy .env.example .env >nul 2>&1

echo ======================================
echo 安装完成!
echo 请编辑 .env 文件配置远程数据库连接信息
echo 运行: python main.py 启动客户端
echo ======================================
pause
