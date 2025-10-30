#!/bin/bash
# OceanBase 社区版安装脚本 (For WSL/Linux)

set -e

echo "======================================"
echo "OceanBase 社区版安装脚本"
echo "======================================"

# 检查系统版本
if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS=$NAME
    VER=$VERSION_ID
else
    echo "无法检测操作系统版本"
    exit 1
fi

echo "检测到系统: $OS $VER"

# 安装依赖
echo "安装依赖包..."
if [[ "$OS" == "Ubuntu" ]] || [[ "$OS" == "Debian" ]]; then
    sudo apt-get update
    sudo apt-get install -y wget curl net-tools
elif [[ "$OS" == "CentOS"* ]] || [[ "$OS" == "Red Hat"* ]]; then
    sudo yum install -y wget curl net-tools
fi

# 下载OceanBase
echo "下载OceanBase社区版..."
OCEANBASE_VERSION="4.2.1"
DOWNLOAD_URL="https://obbusiness-private.oss-cn-shanghai.aliyuncs.com/download-center/opensource/oceanbase-ce/${OCEANBASE_VERSION}/oceanbase-ce-${OCEANBASE_VERSION}.el7.x86_64.rpm"

# 创建安装目录
sudo mkdir -p /opt/oceanbase
cd /opt/oceanbase

# 下载安装包（添加 sudo）
if [ ! -f "oceanbase-ce-${OCEANBASE_VERSION}.rpm" ]; then
    sudo wget --user-agent="Mozilla" $DOWNLOAD_URL -O oceanbase-ce-${OCEANBASE_VERSION}.rpm
fi

# 安装OceanBase
echo "安装OceanBase..."
if [[ "$OS" == "Ubuntu" ]] || [[ "$OS" == "Debian" ]]; then
    # 转换rpm为deb并安装
    sudo apt-get install -y alien
    sudo alien -i oceanbase-ce-${OCEANBASE_VERSION}.rpm
else
    sudo rpm -ivh oceanbase-ce-${OCEANBASE_VERSION}.rpm
fi

# 初始化OceanBase
echo "初始化OceanBase..."
sudo /opt/oceanbase/bin/observer --version

# 创建数据目录
sudo mkdir -p /data/oceanbase
sudo mkdir -p /data/oceanbase/store
sudo mkdir -p /data/oceanbase/log

# 设置权限
sudo chown -R admin:admin /data/oceanbase

echo "======================================"
echo "OceanBase安装完成!"
echo "请运行 deploy_oceanbase.sh 进行部署"
echo "======================================"
