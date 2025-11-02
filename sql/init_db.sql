-- 创建学生管理数据库
CREATE DATABASE IF NOT EXISTS student_management DEFAULT CHARACTER SET utf8mb4;

USE student_management;

-- 创建学生信息表
DROP TABLE IF EXISTS students;
CREATE TABLE students (
    student_id VARCHAR(20) PRIMARY KEY COMMENT '学号',
    name VARCHAR(50) NOT NULL COMMENT '姓名',
    gender ENUM('男', '女') NOT NULL COMMENT '性别',
    age INT CHECK (age > 0 AND age < 150) COMMENT '年龄',
    major VARCHAR(100) NOT NULL COMMENT '专业',
    class_name VARCHAR(50) COMMENT '班级',
    phone VARCHAR(20) COMMENT '联系电话',
    email VARCHAR(100) COMMENT '邮箱',
    enrollment_date DATE COMMENT '入学日期',
    status ENUM('在读', '休学', '退学', '毕业') DEFAULT '在读' COMMENT '状态',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='学生信息表';

-- 创建课程信息表
DROP TABLE IF EXISTS courses;
CREATE TABLE courses (
    course_id VARCHAR(20) PRIMARY KEY COMMENT '课程编号',
    course_name VARCHAR(100) NOT NULL COMMENT '课程名称',
    credits DECIMAL(3,1) NOT NULL CHECK (credits > 0) COMMENT '学分',
    teacher VARCHAR(50) COMMENT '授课教师',
    department VARCHAR(100) COMMENT '开课学院',
    semester VARCHAR(20) COMMENT '开课学期',
    course_type ENUM('必修', '选修', '实践') NOT NULL COMMENT '课程类型',
    max_students INT DEFAULT 100 COMMENT '最大选课人数',
    current_students INT DEFAULT 0 COMMENT '当前选课人数',
    classroom VARCHAR(50) COMMENT '上课地点',
    schedule VARCHAR(100) COMMENT '上课时间',
    description TEXT COMMENT '课程描述',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='课程信息表';

-- 创建选课表
DROP TABLE IF EXISTS enrollments;
CREATE TABLE enrollments (
    enrollment_id INT PRIMARY KEY AUTO_INCREMENT COMMENT '选课记录ID',
    student_id VARCHAR(20) NOT NULL COMMENT '学号',
    course_id VARCHAR(20) NOT NULL COMMENT '课程编号',
    semester VARCHAR(20) NOT NULL COMMENT '学期',
    score DECIMAL(5,2) CHECK (score >= 0 AND score <= 100) COMMENT '成绩',
    grade VARCHAR(10) COMMENT '等级',
    status ENUM('正常', '退选', '重修') DEFAULT '正常' COMMENT '选课状态',
    enrollment_date DATE DEFAULT (CURRENT_DATE) COMMENT '选课日期',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
    FOREIGN KEY (course_id) REFERENCES courses(course_id) ON DELETE CASCADE,
    UNIQUE KEY uk_student_course_semester (student_id, course_id, semester)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='选课信息表';

-- 创建索引优化查询
CREATE INDEX idx_student_major ON students(major);
CREATE INDEX idx_student_class ON students(class_name);
CREATE INDEX idx_course_teacher ON courses(teacher);
CREATE INDEX idx_course_semester ON courses(semester);
CREATE INDEX idx_enrollment_semester ON enrollments(semester);
CREATE INDEX idx_enrollment_status ON enrollments(status);

-- 插入示例数据
INSERT INTO students (student_id, name, gender, age, major, class_name, phone, email, enrollment_date, status) VALUES
('2021001', '张三', '男', 20, '计算机科学与技术', '计科2101', '13800138001', 'zhangsan@example.com', '2021-09-01', '在读'),
('2021002', '李四', '女', 21, '软件工程', '软件2101', '13800138002', 'lisi@example.com', '2021-09-01', '在读'),
('2021003', '王五', '男', 20, '信息安全', '信安2101', '13800138003', 'wangwu@example.com', '2021-09-01', '在读'),
('2021004', '赵六', '女', 21, '计算机科学与技术', '计科2101', '13800138004', 'zhaoliu@example.com', '2021-09-01', '在读'),
('2021005', '钱七', '男', 22, '软件工程', '软件2101', '13800138005', 'qianqi@example.com', '2021-09-01', '在读');

INSERT INTO courses (course_id, course_name, credits, teacher, department, semester, course_type, max_students, classroom, schedule) VALUES
('CS101', '数据结构', 4.0, '王教授', '计算机学院', '2024-1', '必修', 120, '教301', '周一1-2节,周三3-4节'),
('CS102', '操作系统', 3.5, '李教授', '计算机学院', '2024-1', '必修', 100, '教302', '周二1-2节,周四3-4节'),
('CS103', '数据库系统', 3.0, '张教授', '计算机学院', '2024-1', '必修', 100, '教303', '周一5-6节,周三7-8节'),
('CS201', '人工智能', 3.0, '陈教授', '计算机学院', '2024-1', '选修', 80, '教401', '周二5-6节,周四7-8节'),
('CS202', '机器学习', 3.0, '刘教授', '计算机学院', '2024-1', '选修', 60, '教402', '周五1-4节');

INSERT INTO enrollments (student_id, course_id, semester, score, grade, status) VALUES
('2021001', 'CS101', '2024-1', 85.5, '良好', '正常'),
('2021001', 'CS102', '2024-1', 92.0, '优秀', '正常'),
('2021002', 'CS101', '2024-1', 78.0, '中等', '正常'),
('2021002', 'CS103', '2024-1', 88.5, '良好', '正常'),
('2021003', 'CS102', '2024-1', 95.0, '优秀', '正常');
