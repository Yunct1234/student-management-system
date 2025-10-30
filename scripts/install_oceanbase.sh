#!/bin/bash
# OceanBase All in One 安装脚本

set -e

echo "======================================"
echo "OceanBase All in One 安装脚本"
echo "======================================"

# 检查是否已安装
if [ -d "$HOME/.oceanbase-all-in-one" ]; then
    echo "检测到已安装 OceanBase All in One"
    echo "是否重新安装? (y/n)"
    read -r response
    if [[ "$response" != "y" ]]; then
        echo "跳过安装"
        exit 0
    fi
fi

# 下载并安装 All in One 包
echo "下载并安装 OceanBase All in One..."
bash -c "$(curl -s https://obbusiness-private.oss-cn-shanghai.aliyuncs.com/download-center/opensource/oceanbase-all-in-one/installer.sh)"

# 加载环境变量
source ~/.oceanbase-all-in-one/bin/env.sh

# 验证安装
echo "验证安装..."
obd --version

echo "======================================"
echo "OceanBase All in One 安装完成!"
echo "请运行 deploy_oceanbase.sh 进行部署"
echo "======================================"
