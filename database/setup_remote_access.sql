-- 配置远程访问权限
-- 适用于 OceanBase All in One 部署

-- 注意：OceanBase All in One 默认使用 root 用户，不带租户后缀

-- 创建远程访问用户
CREATE USER IF NOT EXISTS 'remote_user'@'%' IDENTIFIED BY 'Remote@123';

-- 授予权限
GRANT SELECT, INSERT, UPDATE, DELETE ON student_management.* TO 'remote_user'@'%';

-- 创建只读用户
CREATE USER IF NOT EXISTS 'readonly_user'@'%' IDENTIFIED BY 'ReadOnly@123';
GRANT SELECT ON student_management.* TO 'readonly_user'@'%';

-- 创建管理员用户（可选）
CREATE USER IF NOT EXISTS 'admin'@'%' IDENTIFIED BY 'Admin@123';
GRANT ALL PRIVILEGES ON student_management.* TO 'admin'@'%';

-- 刷新权限
FLUSH PRIVILEGES;

-- 显示创建的用户
SELECT user, host FROM mysql.user WHERE user IN ('remote_user', 'readonly_user', 'admin');
