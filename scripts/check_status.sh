#!/bin/bash
# 检查OceanBase状态

echo "======================================"
echo "OceanBase 状态检查"
echo "======================================"

# 加载环境变量
if [ -f ~/.oceanbase-all-in-one/bin/env.sh ]; then
    source ~/.oceanbase-all-in-one/bin/env.sh
else
    echo "错误：未找到OceanBase环境"
    exit 1
fi

echo "1. 检查OBD版本："
obd --version

echo ""
echo "2. 检查集群列表："
obd cluster list

echo ""
echo "3. 检查端口占用："
netstat -tlnp 2>/dev/null | grep 2881 || echo "端口2881未被占用"

echo ""
echo "4. 检查observer进程："
ps aux | grep observer | grep -v grep || echo "未发现observer进程"

echo ""
echo "5. 测试数据库连接："
mysql -h127.0.0.1 -P2881 -uroot -e "SELECT 'Connection OK' as Status;" 2>/dev/null || echo "无法连接到数据库"

echo ""
echo "======================================"
