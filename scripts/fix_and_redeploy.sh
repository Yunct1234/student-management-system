#!/bin/bash
# 修复并重新部署OceanBase

set -e

echo "======================================"
echo "OceanBase 修复和重新部署脚本"
echo "======================================"

# 加载环境变量
source ~/.oceanbase-all-in-one/bin/env.sh

# 清理旧的部署
echo "清理旧的部署..."
obd cluster destroy demo -f 2>/dev/null || true

# 清理可能的残留进程
echo "清理残留进程..."
pkill -f observer 2>/dev/null || true
pkill -f obproxy 2>/dev/null || true

# 等待进程完全退出
sleep 5

# 清理数据目录
echo "清理数据目录..."
rm -rf ~/.obd/cluster/demo 2>/dev/null || true

# 重新部署
echo "开始重新部署..."
echo "选择部署模式："
echo "1. 最小规格（推荐，占用资源少）"
echo "2. 标准规格"
read -p "请选择 [1/2]: " choice

if [[ "$choice" == "2" ]]; then
    echo "执行标准规格部署..."
    obd demo -c max
else
    echo "执行最小规格部署..."
    obd demo
fi

# 等待服务启动
echo "等待服务完全启动（约30秒）..."
for i in {1..30}; do
    echo -n "."
    sleep 1
done
echo ""

# 检查部署状态
echo "检查部署状态..."
obd cluster list

# 显示连接信息
echo ""
echo "======================================"
echo "部署完成！"
echo "连接信息："
echo "  mysql -h127.0.0.1 -P2881 -uroot -p -A"
echo "  初始密码为空，直接回车即可"
echo "======================================"
