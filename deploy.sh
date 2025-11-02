#!/bin/bash
# OceanBase学生管理系统部署脚本

echo "================================================"
echo "OceanBase 学生管理系统 - 部署脚本"
echo "================================================"

# 检查Python环境
echo "检查Python环境..."
python3 --version

# 安装依赖
echo "安装Python依赖..."
pip install pymysql colorama

# 检查OceanBase服务
echo "检查OceanBase服务状态..."
systemctl status oceanbase || echo "OceanBase服务未运行，请先启动服务"

# 初始化数据库
echo "是否初始化数据库？(y/n)"
read -r init_db
if [ "$init_db" = "y" ]; then
    python3 scripts/setup_database.py
fi

# 测试连接
echo "测试数据库连接..."
python3 scripts/test_connection.py

echo "部署完成！"
echo "运行 'python3 main.py' 启动系统"
