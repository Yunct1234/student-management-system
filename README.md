# OceanBase 学生管理系统

基于OceanBase数据库的分布式学生管理系统，支持本地和远程多主机访问。

## 项目结构

```
student_management_system/
├── main.py                 # 主程序入口
├── config/                 # 配置模块
│   ├── __init__.py
│   └── db_config.py       # 数据库配置
├── models/                # 数据模型
│   ├── __init__.py
│   ├── student.py         # 学生模型
│   ├── course.py          # 课程模型
│   └── enrollment.py      # 选课模型
├── client/                # 客户端
│   ├── __init__.py
│   └── unified_client.py  # 统一客户端
├── utils/                 # 工具类
│   ├── __init__.py
│   └── db_connection.py   # 数据库连接管理
├── sql/                   # SQL脚本
│   ├── init_db.sql        # 数据库初始化
│   └── setup_remote_access.sql  # 远程访问配置
├── scripts/               # 部署脚本
│   ├── setup_database.py  # 数据库安装脚本
│   └── test_connection.py # 连接测试脚本
├── deploy.sh              # Linux部署脚本
├── deploy.bat             # Windows部署脚本
└── README.md              # 项目文档
```

## 环境要求

- Python 3.8+
- OceanBase Community Edition 4.x
- pymysql, colorama库

## 快速开始

### 1. 安装OceanBase

#### WSL/Linux环境：
```bash
# 下载并安装OceanBase All-in-One
wget https://obbusiness-private.oss-cn-shanghai.aliyuncs.com/download-center/opensource/oceanbase-all-in-one/7/x86_64/oceanbase-all-in-one-4.3.3.1-100000242024102216.el7.x86_64.tar.gz
tar -xzf oceanbase-all-in-one-*.tar.gz
cd oceanbase-all-in-one/bin/
./install.sh

# 初始化集群
obd cluster deploy demo -c ./example/mini-single-example.yaml
obd cluster start demo
```

### 2. 部署项目

#### Linux/WSL：
```bash
chmod +x deploy.sh
./deploy.sh
```

#### Windows：
```batch
deploy.bat
```

### 3. 运行系统

```bash
python main.py
```

## 配置说明

### 本地连接配置
默认配置在 `config/db_config.py`：
- Host: 127.0.0.1
- Port: 2881
- User: root
- Password: (空)

### 远程连接配置
支持三种用户角色：
- `remote_user`: 普通用户 (密码: Remote@123)
- `readonly_user`: 只读用户 (密码: ReadOnly@123)
- `admin`: 管理员 (密码: Admin@123)

### 配置远程访问

1. **服务器端（WSL/Linux）**：
```bash
# 修改OceanBase监听地址
mysql -h127.0.0.1 -P2881 -uroot
ALTER SYSTEM SET observer_tcp_invited_nodes='%';

# 配置防火墙
sudo ufw allow 2881/tcp
```

2. **客户端**：
运行程序选择"远程连接"模式，输入服务器IP地址。

## 主要功能

1. **学生管理**
   - 增删改查学生信息
   - 批量导入/导出

2. **课程管理**
   - 课程信息维护
   - 课程容量管理

3. **选课管理**
   - 学生选课/退课
   - 选课名单查询

4. **成绩管理**
   - 成绩录入
   - 成绩统计分析

5. **统计查询**
   - 多维度数据统计
   - 报表生成

## 故障排除

### 连接失败
1. 检查OceanBase服务状态：`obd cluster list`
2. 验证端口开放：`netstat -an | grep 2881`
3. 检查防火墙设置

### 权限问题
1. 确认用户权限：`SHOW GRANTS FOR 'user'@'host';`
2. 重新授权：运行 `sql/setup_remote_access.sql`

## 开发团队

- 项目负责人：[您的名字]
- 开发环境：Windows 11 + WSL2
- 数据库：OceanBase Community Edition 4.3.3



## 7. 项目部署步骤

### **在主机A（WSL环境）上部署：**

1. **安装OceanBase**
```bash
# 在WSL中执行
cd ~
wget https://obbusiness-private.oss-cn-shanghai.aliyuncs.com/download-center/opensource/oceanbase-all-in-one/7/x86_64/oceanbase-all-in-one-4.3.3.1-100000242024102216.el7.x86_64.tar.gz
tar -xzf oceanbase-all-in-one-*.tar.gz
cd oceanbase-all-in-one/bin/
sudo ./install.sh

# 初始化demo集群
obd cluster deploy demo -c ./example/mini-single-example.yaml
obd cluster start demo
```

2. **部署项目**
```bash
# 克隆或复制项目文件
cd ~/student_management_system
chmod +x deploy.sh
./deploy.sh
```

3. **配置远程访问**
```bash
# 获取WSL的IP地址
ip addr show eth0

# 配置Windows防火墙（在Windows PowerShell管理员模式下）
New-NetFirewallRule -DisplayName "OceanBase" -Direction Inbound -Protocol TCP -LocalPort 2881 -Action Allow
```

### **在主机B（Windows客户端）上连接：**

1. **安装Python依赖**
```batch
pip install pymysql colorama
```

2. **运行客户端**
```batch
python main.py
# 选择"2. 远程连接"
# 输入主机A的IP地址
```