#!/bin/bash
# 停止OceanBase服务

# 加载环境变量
source ~/.oceanbase-all-in-one/bin/env.sh

echo "停止OceanBase集群..."
obd cluster stop demo

echo "集群已停止"
