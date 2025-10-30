# 学生管理系统 - 基于OceanBase

## 项目简介

本项目是一个基于OceanBase国产数据库的学生管理系统，支持多主机远程访问，实现了学生信息管理、课程管理、选课管理等核心功能。

## 系统架构

```
┌─────────────┐     ┌─────────────┐
│  本地客户端  │     │  远程客户端  │
└──────┬──────┘     └──────┬──────┘
       │                   │
       │    TCP/IP         │
       └────────┬──────────┘
                │
        ┌───────▼────────┐
        │   OceanBase    │
        │   数据库服务器  │
        └────────────────┘
```

## 功能特性

### 核心功能
- ✅ 学生信息管理（增删改查）
- ✅ 课程信息管理（增删改查）
- ✅ 选课管理（选课/退选）
- ✅ 成绩管理（录入/查询）
- ✅ 统计分析（各类统计报表）

### 技术特点
- 🔧 基于OceanBase社区版数据库
- 🌐 支持多主机远程访问
- 🔐 完善的权限管理机制
- 📊 丰富的数据统计功能
- 🎨 友好的命令行界面

## 环境要求

### 数据库服务器（WSL/Linux）
- 操作系统: Ubuntu 20.04+ / CentOS 7+
- 内存: 8GB以上
- 磁盘: 20GB以上
- OceanBase: 4.2.1社区版

### 客户端（Windows/Linux）
- Python: 3.8+
- pip: 最新版本
- 网络: 能够访问数据库服务器

## 快速开始

### 1. 部署数据库服务器（WSL环境）

```bash
# 进入WSL环境
wsl

# 克隆项目
git clone https://github.com/yourusername/student_management_system.git
cd student_management_system

# 安装OceanBase
cd scripts
chmod +x *.sh
./install_oceanbase.sh

# 部署数据库
./deploy_oceanbase.sh

# 启动服务
./start_server.sh
```

### 2. 配置本地客户端

```bash
# 安装Python依赖
pip install -r requirements.txt

# 配置数据库连接
cp .env.example .env
# 编辑.env文件，设置数据库连接参数

# 运行本地客户端
python main.py
# 选择1 - 本地客户端
```

### 3. 配置远程客户端（Windows）

```batch
# 在Windows PowerShell中
cd student_management_system

# 安装依赖
pip install -r requirements.txt

# 配置远程连接
copy .env.example .env
# 编辑.env文件，设置远程数据库IP和凭据

# 运行远程客户端
python main.py
# 选择2 - 远程客户端
```

## 数据库设计

### 学生信息表 (students)
| 字段 | 类型 | 说明 |
|------|------|------|
| student_id | VARCHAR(20) | 学号（主键） |
| name | VARCHAR(50) | 姓名 |
| gender | ENUM | 性别 |
| age | INT | 年龄 |
| major | VARCHAR(100) | 专业 |
| class_name | VARCHAR(50) | 班级 |
| phone | VARCHAR(20) | 电话 |
| email | VARCHAR(100) | 邮箱 |
| enrollment_date | DATE | 入学日期 |
| status | ENUM | 状态 |

### 课程信息表 (courses)
| 字段 | 类型 | 说明 |
|------|------|------|
| course_id | VARCHAR(20) | 课程编号（主键） |
| course_name | VARCHAR(100) | 课程名称 |
| credits | DECIMAL(3,1) | 学分 |
| teacher | VARCHAR(50) | 教师 |
| department | VARCHAR(100) | 开课学院 |
| semester | VARCHAR(20) | 学期 |
| course_type | ENUM | 课程类型 |
| max_students | INT | 最大人数 |
| classroom | VARCHAR(50) | 教室 |
| schedule | VARCHAR(100) | 上课时间 |

### 选课表 (enrollments)
| 字段 | 类型 | 说明 |
|------|------|------|
| enrollment_id | INT | 选课ID（主键） |
| student_id | VARCHAR(20) | 学号（外键） |
| course_id | VARCHAR(20) | 课程编号（外键） |
| semester | VARCHAR(20) | 学期 |
| score | DECIMAL(5,2) | 成绩 |
| grade | VARCHAR(10) | 等级 |
| status | ENUM | 选课状态 |

## 用户权限配置

### 管理员用户
- 用户名: admin@localhost
- 权限: 全部权限
- 说明: 本地管理员账户

### 远程用户
- 用户名: remote_user@%
- 权限: SELECT, INSERT, UPDATE, DELETE
- 说明: 远程客户端访问账户

### 只读用户
- 用户名: readonly_user@%
- 权限: SELECT
- 说明: 只读访问账户

## 安全配置

### 网络安全
1. 配置防火墙规则，仅开放必要端口（2881）
2. 使用强密码策略
3. 定期更新密码

### 数据安全
1. 定期备份数据
2. 使用事务保证数据一致性
3. 实施访问日志记录

## 测试

运行测试套件：
```bash
python -m pytest tests/
# 或
python tests/test_operations.py
```

## 常见问题

### Q1: 无法连接到OceanBase
- 检查OceanBase服务是否启动
- 检查防火墙设置
- 验证连接参数是否正确

### Q2: 远程访问被拒绝
- 确认远程用户权限已配置
- 检查网络连接
- 验证用户名和密码

### Q3: 中文显示乱码
- 设置数据库字符集为utf8mb4
- 客户端连接时指定charset='utf8mb4'

## 项目结构
```
student_management_system/
├── config/              # 配置文件
├── database/            # 数据库脚本
├── models/              # 数据模型
├── utils/               # 工具类
├── client/              # 客户端程序
├── tests/               # 测试代码
├── scripts/             # 部署脚本
├── requirements.txt     # Python依赖
├── .env                 # 环境变量
├── main.py             # 主程序入口
└── README.md           # 说明文档
```

## 许可证

MIT License

## 作者

Your Name - [your.email@example.com](mailto:your.email@example.com)

## 致谢

- OceanBase团队提供的优秀国产数据库
- Python社区的开源贡献者