#!/bin/bash
# WSL环境下修复ulimit限制

echo "======================================"
echo "修复WSL环境ulimit限制"
echo "======================================"

# 1. 设置当前会话的ulimit
echo "设置当前会话ulimit..."
ulimit -n 65535
ulimit -c unlimited
ulimit -s unlimited

# 2. 修改limits配置文件
echo "修改系统limits配置..."
sudo bash -c 'cat > /etc/security/limits.d/oceanbase.conf << EOF
* soft nofile 65535
* hard nofile 65535
* soft nproc 65535
* hard nproc 65535
* soft core unlimited
* hard core unlimited
* soft stack unlimited
* hard stack unlimited
EOF'

# 3. 修改WSL配置
echo "检查WSL配置..."
if [ ! -f /etc/wsl.conf ]; then
    echo "创建WSL配置文件..."
    sudo bash -c 'cat > /etc/wsl.conf << EOF
[boot]
systemd=true

[network]
generateResolvConf = false
EOF'
fi

# 4. 修改sysctl参数
echo "修改系统参数..."
sudo bash -c 'cat > /etc/sysctl.d/99-oceanbase.conf << EOF
# OceanBase requirements
fs.file-max = 6815744
fs.aio-max-nr = 1048576
net.core.somaxconn = 2048
net.core.netdev_max_backlog = 10000
net.core.rmem_default = 16777216
net.core.wmem_default = 16777216
net.core.rmem_max = 16777216
net.core.wmem_max = 16777216
net.ipv4.ip_local_port_range = 3500 65535
net.ipv4.tcp_fin_timeout = 30
net.ipv4.tcp_syncookies = 0
net.ipv4.tcp_timestamps = 1
net.ipv4.tcp_tw_reuse = 1
net.ipv4.tcp_tw_recycle = 0
vm.swappiness = 0
vm.max_map_count = 655360
EOF'

# 应用sysctl参数
sudo sysctl -p /etc/sysctl.d/99-oceanbase.conf

# 5. 显示当前限制
echo ""
echo "当前ulimit设置："
ulimit -a

echo ""
echo "======================================"
echo "修复完成！"
echo "注意：需要重新启动WSL才能完全生效"
echo "可以执行: wsl --shutdown (在Windows中)"
echo "然后重新进入WSL"
echo "======================================"
