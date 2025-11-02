# OceanBase 学生管理系统

基于OceanBase数据库的分布式学生管理系统，支持本地和远程多主机访问。

## 项目结构

```
student_management_system/
├── main.py                    # 主程序入口
├── deploy_database.sh         # 数据库部署脚本
├── test_connection_simple.py  # 简单连接测试
├── requirements.txt           # Python依赖
├── .env                       # 环境变量配置
├── config/                    # 配置模块
│   ├── __init__.py
│   └── db_config.py          # 数据库配置
├── models/                   # 数据模型
│   ├── __init__.py
│   ├── student.py            # 学生模型
│   ├── course.py             # 课程模型
│   └── enrollment.py         # 选课模型
├── client/                   # 客户端
│   ├── __init__.py
│   └── unified_client.py     # 统一客户端
├── utils/                    # 工具类
│   ├── __init__.py
│   └── db_connection.py      # 数据库连接管理
├── sql/                      # SQL脚本
│   ├── init_db.sql           # 数据库初始化
│   └── setup_remote_access.sql # 远程访问配置
└── scripts/                  # 脚本文件
    └── setup_database.py     # 数据库初始化脚本
```

## 环境要求

- **服务器端（电脑A）**：Windows 11 + WSL2
- **客户端（电脑B）**：Windows 11
- Python 3.8+
- OceanBase Community Edition 4.x
- Python库：pymysql, colorama

## 部署步骤

### 电脑A（WSL服务器端）部署

#### 1. WSL环境准备

**重要：每次开启新的WSL窗口都需要设置会话限制**

```bash
# 修改当前会话限制
ulimit -n 20000

# 验证修改
ulimit -n
```

#### 2. 快速部署OceanBase

```bash
# 赋予执行权限并运行部署脚本
chmod +x deploy_database.sh
./deploy_database.sh
```

或者使用OBD命令：
```bash
obd demo
```

#### 3. 管理OceanBase集群

```bash
# 查看集群状态
obd cluster list

# 如果显示deployed状态，需要启动集群
obd cluster start demo
```

**注意：** 启动成功后会显示root密码，默认密码为 `u`

#### 4. 密码管理

查看当前密码：
```bash
cat ~/.obd/cluster/sms_database/config.yaml
```

修改密码（可选）：
```bash
# 连接到OceanBase
obclient -h127.0.0.1 -P2881 -uroot@sys -p'u'

# 修改密码
ALTER USER 'root'@'%' IDENTIFIED BY '新密码';
```

**重要：** 修改密码后需要同步更新 `config/db_config.py` 文件中的密码配置

#### 5. 测试本地连接

```bash
# 简单连接测试
python3 test_connection_simple.py
```

#### 6. 初始化数据库

```bash
# 运行数据库初始化脚本
python3 scripts/setup_database.py
```

#### 7. 创建远程访问用户

```bash
# 连接到数据库
mysql -h127.0.0.1 -P2881 -uroot@sys -p'u' -Doceanbase -A

# 查看现有用户
SELECT user, host FROM mysql.user;

# 创建远程访问用户
CREATE USER 'remote_user'@'%' IDENTIFIED BY 'remote@123456';

# 授予所有权限
GRANT ALL PRIVILEGES ON *.* TO 'remote_user'@'%';

# 刷新权限（OceanBase通常自动生效）
FLUSH PRIVILEGES;

# 退出
exit;
```

#### 8. 配置网络访问

1. **查看WSL的IP地址**：
```bash
# 在WSL中执行
ip addr show eth0
```

2. **查看Windows的WLAN IP**：
```cmd
# 在Windows CMD中执行
ipconfig
# 找到WLAN适配器的IPv4地址
```

3. **配置Windows防火墙**（在Windows PowerShell管理员模式下）：
```powershell
# 添加防火墙规则允许2881端口
New-NetFirewallRule -DisplayName "OceanBase Port 2881" -Direction Inbound -Protocol TCP -LocalPort 2881 -Action Allow
```

#### 9. 启动本地客户端

```bash
python3 main.py
```

### 电脑B（Windows客户端）部署

#### 1. 获取项目代码

```bash
git clone [项目地址]
cd student_management_system
```

#### 2. 安装Python依赖

```bash
pip install -r requirements.txt
# 或手动安装
pip install pymysql colorama
```

#### 3. 运行客户端

```bash
python main.py
```

选择"远程连接"模式，输入：
- 服务器IP：电脑A的WLAN IP地址
- 端口：2881
- 用户名：remote_user
- 密码：remote@123456

## 常用命令速查

### OceanBase管理

| 功能 | 命令 |
|------|------|
| 查看集群列表 | `obd cluster list` |
| 启动集群 | `obd cluster start demo` |
| 停止集群 | `obd cluster stop demo` |
| 删除集群 | `obd cluster destroy demo` |
| 查看集群状态 | `obd cluster display demo` |

### 用户管理

| 功能 | SQL命令 |
|------|---------|
| 创建用户 | `CREATE USER 'username'@'%' IDENTIFIED BY 'password';` |
| 授予权限 | `GRANT ALL PRIVILEGES ON *.* TO 'username'@'%';` |
| 修改密码 | `ALTER USER 'username'@'%' IDENTIFIED BY 'newpassword';` |
| 删除用户 | `DROP USER 'username'@'%';` |
| 查看用户 | `SELECT user, host FROM mysql.user;` |

## 故障排除

### 1. WSL连接问题

**问题**：无法连接到OceanBase
- 检查ulimit设置：`ulimit -n` （应该为20000）
- 检查集群状态：`obd cluster list`
- 确认集群已启动：`obd cluster start demo`

### 2. 远程连接失败

**问题**：电脑B无法连接到电脑A
- 确认防火墙规则已添加
- 检查端口是否开放：`netstat -an | findstr 2881`
- 确认使用正确的IP地址（WLAN IP，不是WSL内部IP）
- 验证用户名和密码是否正确

### 3. 权限问题

**问题**：Access denied错误
- 确认用户已创建：`SELECT user, host FROM mysql.user;`
- 重新授权：`GRANT ALL PRIVILEGES ON *.* TO 'remote_user'@'%';`
- 刷新权限：`FLUSH PRIVILEGES;`

### 4. 密码问题

**问题**：忘记密码
- 查看配置文件：`cat ~/.obd/cluster/sms_database/config.yaml`
- 使用root用户重置其他用户密码

## 默认配置

| 配置项 | 默认值 |
|--------|--------|
| 数据库端口 | 2881 |
| root密码 | u |
| 远程用户 | remote_user |
| 远程用户密码 | remote@123456 |
| 数据库名 | student_management |

## 注意事项

1. **WSL会话限制**：每次打开新的WSL窗口都需要执行 `ulimit -n 20000`
2. **密码同步**：修改数据库密码后，记得更新 `config/db_config.py`
3. **IP地址**：远程连接使用Windows的WLAN IP，不是WSL的内部IP
4. **防火墙**：确保Windows防火墙允许2881端口

## 功能特性

### 核心功能

1. **学生信息管理**
   - 添加、删除、修改、查询学生信息
   - 按专业、班级筛选
   - 批量操作支持

2. **课程信息管理**
   - 课程的增删改查
   - 课程容量管理
   - 授课教师分配

3. **选课管理**
   - 学生选课/退课
   - 选课名单查询
   - 选课冲突检测

4. **成绩管理**
   - 成绩录入
   - 成绩统计分析
   - 成绩分布查询

5. **统计查询**
   - 多维度数据统计
   - 学生/课程/成绩报表

### 访问模式

- **本地模式**：直接连接本机OceanBase
- **远程模式**：通过网络连接其他主机的OceanBase

## 项目信息

- **数据库**：OceanBase Community Edition 4.x
- **开发环境**：Windows 11 + WSL2
- **Python版本**：3.8+
- **默认端口**：2881

## 常见错误代码

| 错误代码 | 说明 | 解决方法 |
|----------|------|----------|
| 2003 | Can't connect to MySQL server | 检查IP地址和端口 |
| 1045 | Access denied for user | 检查用户名密码 |
| 1049 | Unknown database | 运行数据库初始化脚本 |
| 1146 | Table doesn't exist | 执行init_db.sql |

## 快速启动指南

### 服务器端（电脑A）
```bash
# 1. 设置会话限制
ulimit -n 20000

# 2. 启动OceanBase
obd cluster start demo

# 3. 运行服务
python3 main.py
```

### 客户端（电脑B）
```bash
# 直接运行客户端
python main.py
# 选择远程连接，输入服务器IP
```