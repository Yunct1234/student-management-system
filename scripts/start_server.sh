#!/bin/bash
# 启动OceanBase服务

echo "启动OceanBase服务..."

# 检查OceanBase进程
if pgrep -x "observer" > /dev/null; then
    echo "OceanBase已经在运行"
else
    echo "启动Observer进程..."
    cd /opt/oceanbase
    ./bin/observer -d /data/oceanbase/store &
    sleep 10
    echo "OceanBase启动成功"
fi

# 检查连接
echo "检查数据库连接..."
mysql -h localhost -P 2881 -uroot@sys -e "SELECT 'Connected' as Status;"

echo "服务启动完成"
