#!/bin/bash
# 启动OceanBase服务

# 加载环境变量
source ~/.oceanbase-all-in-one/bin/env.sh

echo "检查OceanBase集群状态..."

# 检查集群是否存在
if ! obd cluster list | grep -q "demo"; then
    echo "错误: 未找到OceanBase集群，请先运行 deploy_oceanbase.sh"
    exit 1
fi

# 检查集群状态
STATUS=$(obd cluster list | grep "demo" | awk '{print $2}')

if [[ "$STATUS" == "running" ]]; then
    echo "OceanBase集群已经在运行"
else
    echo "启动OceanBase集群..."
    obd cluster start demo
    echo "等待服务启动..."
    sleep 20
fi

# 显示集群信息
echo "集群信息:"
obd cluster display demo

# 测试连接
echo "测试数据库连接..."
mysql -h 127.0.0.1 -P 2881 -uroot -p -e "SELECT 'Connected to OceanBase' as Status;"

echo "服务启动完成"
