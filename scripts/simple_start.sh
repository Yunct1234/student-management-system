#!/bin/bash
# 简单启动脚本（避免管道问题）

echo "启动OceanBase服务..."

# 加载环境变量
source ~/.oceanbase-all-in-one/bin/env.sh

# 直接启动，避免管道
obd cluster start demo 2>&1

# 检查进程
echo "检查服务状态..."
ps aux | grep observer | grep -v grep

echo "测试连接..."
sleep 5
mysql -h127.0.0.1 -P2881 -uroot -e "SELECT 'OK' as Status;"

echo "服务启动完成"
