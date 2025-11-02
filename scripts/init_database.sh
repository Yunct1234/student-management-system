#!/bin/bash
# 初始化数据库和表结构

echo "======================================"
echo "初始化学生管理数据库"
echo "======================================"

MYSQL_HOST="127.0.0.1"
MYSQL_PORT="2881"
MYSQL_USER="root"

# 创建数据库
echo "1. 创建数据库..."
mysql -h$MYSQL_HOST -P$MYSQL_PORT -u$MYSQL_USER -e "
CREATE DATABASE IF NOT EXISTS student_management 
DEFAULT CHARACTER SET utf8mb4 
COLLATE utf8mb4_general_ci;"

# 创建表结构
echo "2. 创建表结构..."
mysql -h$MYSQL_HOST -P$MYSQL_PORT -u$MYSQL_USER student_management -e "
-- 学生表
CREATE TABLE IF NOT EXISTS students (
    student_id VARCHAR(20) PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    gender ENUM('男', '女') DEFAULT '男',
    age INT CHECK (age > 0 AND age < 150),
    major VARCHAR(100),
    class_name VARCHAR(50),
    phone VARCHAR(20),
    email VARCHAR(100),
    enrollment_date DATE,
    status ENUM('在读', '休学', '毕业', '退学') DEFAULT '在读',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_name (name),
    INDEX idx_major (major),
    INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 课程表
CREATE TABLE IF NOT EXISTS courses (
    course_id VARCHAR(20) PRIMARY KEY,
    course_name VARCHAR(100) NOT NULL,
    credits DECIMAL(3,1) DEFAULT 2.0,
    teacher VARCHAR(50),
    department VARCHAR(100),
    semester VARCHAR(20),
    course_type ENUM('必修', '选修', '公选') DEFAULT '选修',
    max_students INT DEFAULT 50,
    classroom VARCHAR(50),
    schedule VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_course_name (course_name),
    INDEX idx_teacher (teacher),
    INDEX idx_semester (semester)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 选课表
CREATE TABLE IF NOT EXISTS enrollments (
    enrollment_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id VARCHAR(20),
    course_id VARCHAR(20),
    semester VARCHAR(20),
    score DECIMAL(5,2),
    grade VARCHAR(10),
    status ENUM('已选', '已退', '已完成') DEFAULT '已选',
    enrolled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
    FOREIGN KEY (course_id) REFERENCES courses(course_id) ON DELETE CASCADE,
    UNIQUE KEY uk_enrollment (student_id, course_id, semester),
    INDEX idx_student (student_id),
    INDEX idx_course (course_id),
    INDEX idx_semester_enroll (semester)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;"

# 创建用户和权限
echo "3. 创建远程访问用户..."
mysql -h$MYSQL_HOST -P$MYSQL_PORT -u$MYSQL_USER -e "
-- 创建远程用户
CREATE USER IF NOT EXISTS 'remote_user'@'%' IDENTIFIED BY 'Ocean@2024';

-- 授予权限
GRANT SELECT, INSERT, UPDATE, DELETE ON student_management.* TO 'remote_user'@'%';

-- 创建只读用户
CREATE USER IF NOT EXISTS 'readonly'@'%' IDENTIFIED BY 'ReadOnly@2024';
GRANT SELECT ON student_management.* TO 'readonly'@'%';

-- 刷新权限
FLUSH PRIVILEGES;"

# 插入测试数据
echo "4. 插入测试数据..."
mysql -h$MYSQL_HOST -P$MYSQL_PORT -u$MYSQL_USER student_management -e "
-- 插入测试学生数据
INSERT IGNORE INTO students (student_id, name, gender, age, major, class_name, phone, email, enrollment_date) VALUES
('2024001', '张三', '男', 20, '计算机科学与技术', '计科2401', '13800138001', 'zhangsan@example.com', '2024-09-01'),
('2024002', '李四', '女', 19, '软件工程', '软件2401', '13800138002', 'lisi@example.com', '2024-09-01'),
('2024003', '王五', '男', 21, '人工智能', 'AI2401', '13800138003', 'wangwu@example.com', '2024-09-01');

-- 插入测试课程数据
INSERT IGNORE INTO courses (course_id, course_name, credits, teacher, department, semester, course_type, max_students, classroom, schedule) VALUES
('CS101', '数据结构', 3.0, '张教授', '计算机学院', '2024-1', '必修', 60, 'A101', '周一1-2节,周三3-4节'),
('CS102', '数据库系统', 3.0, '李教授', '计算机学院', '2024-1', '必修', 50, 'B201', '周二1-2节,周四3-4节'),
('CS103', '人工智能导论', 2.0, '王教授', '计算机学院', '2024-1', '选修', 40, 'C301', '周五1-2节');

-- 插入测试选课数据
INSERT IGNORE INTO enrollments (student_id, course_id, semester) VALUES
('2024001', 'CS101', '2024-1'),
('2024001', 'CS102', '2024-1'),
('2024002', 'CS101', '2024-1'),
('2024002', 'CS103', '2024-1');"

echo ""
echo "5. 显示数据库信息..."
mysql -h$MYSQL_HOST -P$MYSQL_PORT -u$MYSQL_USER -e "
SHOW DATABASES;
USE student_management;
SHOW TABLES;
SELECT COUNT(*) as student_count FROM students;
SELECT COUNT(*) as course_count FROM courses;
SELECT COUNT(*) as enrollment_count FROM enrollments;"

echo ""
echo "======================================"
echo "数据库初始化完成！"
echo "远程用户: remote_user / Ocean@2024"
echo "只读用户: readonly / ReadOnly@2024"
echo "======================================"
