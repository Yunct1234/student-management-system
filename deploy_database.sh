#!/bin/bash

# 设置集群名称
CLUSTER_NAME="sms_database" 

echo "=========================================="
echo "部署OceanBase集群: $CLUSTER_NAME"
echo "=========================================="

# 1. 检查是否已存在同名集群
if obd cluster list | grep -q "$CLUSTER_NAME"; then
    echo "集群 $CLUSTER_NAME 已存在，正在清理..."
    obd cluster stop $CLUSTER_NAME 2>/dev/null
    obd cluster destroy $CLUSTER_NAME -f
fi

# 2. 创建最小配置文件
cat > /tmp/${CLUSTER_NAME}_config.yaml <<EOF
user:
  username: $USER
  
oceanbase-ce:
  servers:
    - name: server1
      ip: 127.0.0.1
  global:
    home_path: /home/$USER/${CLUSTER_NAME}/observer
    data_dir: /tmp/${CLUSTER_NAME}/data
    redo_dir: /tmp/${CLUSTER_NAME}/redo
    devname: lo
    mysql_port: 2881
    rpc_port: 2882
    zone: zone1
    cluster_id: 1
    memory_limit: 6G
    system_memory: 1G
    datafile_size: 10G
    log_disk_size: 10G
    cpu_count: 4
    production_mode: false
    enable_syslog_recycle: true
    root_password: u  # 设置初始密码
EOF

# 3. 部署集群
echo "正在部署集群..."
obd cluster deploy $CLUSTER_NAME -c /tmp/${CLUSTER_NAME}_config.yaml

if [ $? -eq 0 ]; then
    echo "部署成功，正在启动集群..."
    
    # 4. 启动集群
    obd cluster start $CLUSTER_NAME
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "=========================================="
        echo "集群 $CLUSTER_NAME 部署成功！"
        echo "=========================================="
        echo ""
        echo "连接信息："
        echo "  mysql -h127.0.0.1 -P2881 -uroot@sys -p'u' -Doceanbase -A"
        echo ""
        echo "管理命令："
        echo "  查看状态: obd cluster display $CLUSTER_NAME"
        echo "  停止集群: obd cluster stop $CLUSTER_NAME"
        echo "  启动集群: obd cluster start $CLUSTER_NAME"
        echo "  重启集群: obd cluster restart $CLUSTER_NAME"
        echo "  销毁集群: obd cluster destroy $CLUSTER_NAME"
    else
        echo "集群启动失败"
        obd cluster destroy $CLUSTER_NAME
    fi
else
    echo "部署失败"
fi
