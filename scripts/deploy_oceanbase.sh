#!/bin/bash
# OceanBase 部署脚本

set -e

echo "======================================"
echo "OceanBase 部署配置"
echo "======================================"

# 配置参数
ZONE_NAME="zone1"
CLUSTER_NAME="student_cluster"
SERVER_IP=$(hostname -I | awk '{print $1}')
MYSQL_PORT=2881
RPC_PORT=2882
DATA_DIR="/data/oceanbase/store"
LOG_DIR="/data/oceanbase/log"

echo "服务器IP: $SERVER_IP"
echo "MySQL端口: $MYSQL_PORT"
echo "RPC端口: $RPC_PORT"

# 启动Observer
echo "启动OceanBase Observer..."
cd /opt/oceanbase

./bin/observer \
    -i $SERVER_IP \
    -p $MYSQL_PORT \
    -P $RPC_PORT \
    -z $ZONE_NAME \
    -d $DATA_DIR \
    -l INFO \
    -o "memory_limit=8G,system_memory=4G,stack_size=512K,cpu_count=4,cache_wash_threshold=1G,__min_full_resource_pool_memory=268435456,workers_per_cpu_quota=10,schema_history_expire_time=1d,net_thread_count=4,major_freeze_duty_time=Disable,minor_freeze_times=10,enable_separate_sys_clog=0,enable_merge_by_turn=False,datafile_disk_percentage=50,enable_syslog_wf=0,max_syslog_file_count=4" \
    -c $CLUSTER_NAME \
    -n $CLUSTER_NAME \
    -d $DATA_DIR \
    -l $LOG_DIR &

sleep 10

# 初始化集群
echo "初始化集群..."
mysql -h $SERVER_IP -P $MYSQL_PORT -uroot -e "
    ALTER SYSTEM BOOTSTRAP ZONE '$ZONE_NAME' SERVER '$SERVER_IP:$RPC_PORT';
"

echo "等待集群初始化..."
sleep 30

# 创建租户
echo "创建租户..."
mysql -h $SERVER_IP -P $MYSQL_PORT -uroot@sys -e "
    CREATE RESOURCE POOL IF NOT EXISTS sys_pool 
    UNIT = 'sys_unit', 
    UNIT_NUM = 1;
    
    CREATE TENANT IF NOT EXISTS sys 
    RESOURCE_POOL_LIST = ('sys_pool');
"

# 创建数据库
echo "创建student_management数据库..."
mysql -h $SERVER_IP -P $MYSQL_PORT -uroot@sys -e "
    CREATE DATABASE IF NOT EXISTS student_management;
"

# 导入数据库结构
echo "导入数据库结构..."
mysql -h $SERVER_IP -P $MYSQL_PORT -uroot@sys student_management < ../database/init_db.sql

# 设置远程访问权限
echo "配置远程访问权限..."
mysql -h $SERVER_IP -P $MYSQL_PORT -uroot@sys < ../database/setup_remote_access.sql

echo "======================================"
echo "OceanBase部署完成!"
echo "连接信息:"
echo "  主机: $SERVER_IP"
echo "  端口: $MYSQL_PORT"
echo "  用户: root@sys"
echo "  数据库: student_management"
echo "======================================"
