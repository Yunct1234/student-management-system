-- 配置远程访问权限
-- 在OceanBase中创建远程访问用户

-- 创建本地管理员用户
CREATE USER IF NOT EXISTS 'admin'@'localhost' IDENTIFIED BY 'Admin@123';
GRANT ALL PRIVILEGES ON student_management.* TO 'admin'@'localhost';

-- 创建远程访问用户（允许从任意主机访问）
CREATE USER IF NOT EXISTS 'remote_user'@'%' IDENTIFIED BY 'Remote@123';
GRANT SELECT, INSERT, UPDATE, DELETE ON student_management.* TO 'remote_user'@'%';

-- 创建只读用户
CREATE USER IF NOT EXISTS 'readonly_user'@'%' IDENTIFIED BY 'Readonly@123';
GRANT SELECT ON student_management.* TO 'readonly_user'@'%';

-- 刷新权限
FLUSH PRIVILEGES;

-- 查看用户权限
SELECT user, host, authentication_string FROM mysql.user;
SHOW GRANTS FOR 'remote_user'@'%';
