#!/bin/bash
# OceanBase All in One 部署脚本

set -e

echo "======================================"
echo "OceanBase All in One 部署"
echo "======================================"

# 加载环境变量
source ~/.oceanbase-all-in-one/bin/env.sh

# 检查是否已有部署
if obd cluster list | grep -q "demo"; then
    echo "检测到已有部署，是否销毁重新部署? (y/n)"
    read -r response
    if [[ "$response" == "y" ]]; then
        echo "销毁现有部署..."
        obd cluster destroy demo -f
    else
        echo "使用现有部署"
        obd cluster display demo
        exit 0
    fi
fi

# 选择部署规格
echo "请选择部署规格:"
echo "1. 最小规格部署 (开发测试用，内存需求较小)"
echo "2. 最大规格部署 (生产环境，需要更多资源)"
read -p "请选择 [1/2]: " choice

if [[ "$choice" == "2" ]]; then
    echo "执行最大规格部署..."
    obd pref
else
    echo "执行最小规格部署..."
    obd demo
fi

# 等待服务启动
echo "等待服务完全启动..."
sleep 30

# 获取连接信息
echo "获取连接信息..."
obd cluster display demo

# 创建数据库和导入表结构
echo "创建student_management数据库..."

# 获取MySQL端口（通常是2881）
MYSQL_PORT=2881
MYSQL_HOST="127.0.0.1"

# 连接并创建数据库
mysql -h $MYSQL_HOST -P $MYSQL_PORT -uroot -p -A -e "
    CREATE DATABASE IF NOT EXISTS student_management DEFAULT CHARACTER SET utf8mb4;
    USE student_management;
"

# 导入数据库结构
echo "导入数据库结构..."
mysql -h $MYSQL_HOST -P $MYSQL_PORT -uroot -p -A student_management < ../database/init_db.sql

# 设置远程访问权限
echo "配置远程访问权限..."
mysql -h $MYSQL_HOST -P $MYSQL_PORT -uroot -p -A < ../database/setup_remote_access.sql

echo "======================================"
echo "OceanBase部署完成!"
echo "连接信息:"
echo "  主机: $MYSQL_HOST"
echo "  端口: $MYSQL_PORT" 
echo "  用户: root (初始密码为空)"
echo "  数据库: student_management"
echo ""
echo "管理命令:"
echo "  查看集群: obd cluster list"
echo "  查看状态: obd cluster display demo"
echo "  启动集群: obd cluster start demo"
echo "  停止集群: obd cluster stop demo"
echo "======================================"
