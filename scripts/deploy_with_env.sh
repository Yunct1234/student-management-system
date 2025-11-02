#!/bin/bash
# 自动配置环境并部署OceanBase

set -e

echo "======================================"
echo "OceanBase 自动部署脚本"
echo "======================================"

# 加载环境变量
source ~/.oceanbase-all-in-one/bin/env.sh

# 1. 清理旧部署
echo "清理旧部署..."
obd cluster destroy demo -f 2>/dev/null || true

obd demo
# 2. 使用obd自动配置系统参数
echo "自动配置系统参数..."
obd cluster init4env demo

# 3. 设置当前会话的ulimit（立即生效）
echo "设置当前会话参数..."
ulimit -n 65535
ulimit -c unlimited
ulimit -s unlimited


# 5. 检查状态
echo "检查部署状态..."
sleep 10
obd cluster list

echo ""
echo "======================================"
echo "部署流程完成！"
echo "======================================"
