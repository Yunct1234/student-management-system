#!/usr/bin/env python3
"""
db_init.py
数据库初始化脚本 - 自动创建数据库和表结构
"""
import pymysql
from pymysql.cursors import DictCursor


class DatabaseInitializer:
    """数据库初始化器"""
    
    def __init__(self, config):
        """
        初始化
        :param config: 数据库配置（不含database，因为可能还不存在）
        """
        self.config = config.copy()
        self.database_name = self.config.pop('database', 'student_management')
        
    def init_database(self):
        """初始化数据库（主入口）"""
        print("=" * 50)
        print("数据库初始化")
        print("=" * 50)
        
        # 1. 创建数据库
        if not self._create_database():
            return False
            
        # 2. 创建表结构
        if not self._create_tables():
            return False
            
        # 3. 插入初始数据
        if not self._insert_initial_data():
            return False
            
        print("\n✓ 数据库初始化完成！")
        return True
        
    def _get_connection(self, use_database=True):
        """获取数据库连接"""
        config = self.config.copy()
        if use_database:
            config['database'] = self.database_name
        config['cursorclass'] = DictCursor
        return pymysql.connect(**config)
        
    def _create_database(self):
        """创建数据库"""
        print(f"\n[1/3] 创建数据库 {self.database_name}...")
        try:
            conn = self._get_connection(use_database=False)
            cursor = conn.cursor()
            
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.database_name} "
                          f"DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci")
            conn.commit()
            
            cursor.close()
            conn.close()
            print(f"  ✓ 数据库 {self.database_name} 已就绪")
            return True
        except Exception as e:
            print(f"  ✗ 创建数据库失败: {e}")
            return False
            
    def _create_tables(self):
        """创建表结构"""
        print("\n[2/3] 创建表结构...")
        
        tables_sql = {
            'students': """
                CREATE TABLE IF NOT EXISTS students (
                    student_id VARCHAR(20) PRIMARY KEY COMMENT '学号',
                    name VARCHAR(50) NOT NULL COMMENT '姓名',
                    gender ENUM('男', '女') DEFAULT '男' COMMENT '性别',
                    age INT COMMENT '年龄',
                    major VARCHAR(100) COMMENT '专业',
                    class_name VARCHAR(50) COMMENT '班级',
                    phone VARCHAR(20) COMMENT '电话',
                    email VARCHAR(100) COMMENT '邮箱',
                    address VARCHAR(200) COMMENT '地址',
                    enrollment_date DATE COMMENT '入学日期',
                    status ENUM('在读', '休学', '退学', '毕业') DEFAULT '在读' COMMENT '状态',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    INDEX idx_name (name),
                    INDEX idx_major (major),
                    INDEX idx_status (status)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='学生信息表'
            """,
            
            'teachers': """
                CREATE TABLE IF NOT EXISTS teachers (
                    teacher_id VARCHAR(20) PRIMARY KEY COMMENT '教师工号',
                    name VARCHAR(50) NOT NULL COMMENT '姓名',
                    gender ENUM('男', '女') DEFAULT '男' COMMENT '性别',
                    title VARCHAR(50) COMMENT '职称',
                    department VARCHAR(100) COMMENT '所属学院',
                    phone VARCHAR(20) COMMENT '电话',
                    email VARCHAR(100) COMMENT '邮箱',
                    status ENUM('在职', '离职', '退休') DEFAULT '在职' COMMENT '状态',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='教师信息表'
            """,
            
            'courses': """
                CREATE TABLE IF NOT EXISTS courses (
                    course_id VARCHAR(20) PRIMARY KEY COMMENT '课程编号',
                    course_name VARCHAR(100) NOT NULL COMMENT '课程名称',
                    credits DECIMAL(3,1) DEFAULT 2.0 COMMENT '学分',
                    hours INT DEFAULT 32 COMMENT '学时',
                    teacher_id VARCHAR(20) COMMENT '授课教师ID',
                    department VARCHAR(100) COMMENT '开课学院',
                    semester VARCHAR(20) COMMENT '学期',
                    course_type ENUM('必修', '选修', '实践') DEFAULT '选修' COMMENT '课程类型',
                    max_students INT DEFAULT 100 COMMENT '最大选课人数',
                    classroom VARCHAR(50) COMMENT '上课地点',
                    schedule VARCHAR(100) COMMENT '上课时间',
                    description TEXT COMMENT '课程描述',
                    status ENUM('开课', '停课') DEFAULT '开课' COMMENT '状态',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    INDEX idx_teacher (teacher_id),
                    INDEX idx_semester (semester)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='课程信息表'
            """,
            
            'enrollments': """
                CREATE TABLE IF NOT EXISTS enrollments (
                    enrollment_id INT AUTO_INCREMENT PRIMARY KEY COMMENT '选课记录ID',
                    student_id VARCHAR(20) NOT NULL COMMENT '学号',
                    course_id VARCHAR(20) NOT NULL COMMENT '课程编号',
                    semester VARCHAR(20) NOT NULL COMMENT '学期',
                    score DECIMAL(5,2) COMMENT '成绩',
                    grade VARCHAR(10) COMMENT '等级',
                    enrollment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '选课时间',
                    score_date TIMESTAMP NULL COMMENT '成绩录入时间',
                    status ENUM('已选', '已退', '已修') DEFAULT '已选' COMMENT '状态',
                    UNIQUE KEY uk_student_course_semester (student_id, course_id, semester),
                    INDEX idx_student (student_id),
                    INDEX idx_course (course_id),
                    INDEX idx_semester (semester)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='选课记录表'
            """,
            
            'system_users': """
                CREATE TABLE IF NOT EXISTS system_users (
                    user_id INT AUTO_INCREMENT PRIMARY KEY COMMENT '用户ID',
                    username VARCHAR(50) NOT NULL UNIQUE COMMENT '用户名',
                    password_hash VARCHAR(255) NOT NULL COMMENT '密码哈希',
                    role ENUM('admin', 'teacher', 'student') NOT NULL COMMENT '角色',
                    related_id VARCHAR(20) COMMENT '关联ID',
                    real_name VARCHAR(50) COMMENT '真实姓名',
                    is_active TINYINT(1) DEFAULT 1 COMMENT '是否启用',
                    last_login TIMESTAMP NULL COMMENT '最后登录时间',
                    login_count INT DEFAULT 0 COMMENT '登录次数',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    INDEX idx_role (role),
                    INDEX idx_related (related_id)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='系统用户表'
            """,
            
            'operation_logs': """
                CREATE TABLE IF NOT EXISTS operation_logs (
                    log_id INT AUTO_INCREMENT PRIMARY KEY COMMENT '日志ID',
                    user_id INT COMMENT '操作用户ID',
                    username VARCHAR(50) COMMENT '用户名',
                    role VARCHAR(20) COMMENT '用户角色',
                    operation VARCHAR(200) NOT NULL COMMENT '操作描述',
                    table_name VARCHAR(50) COMMENT '操作表',
                    record_id VARCHAR(50) COMMENT '记录ID',
                    ip_address VARCHAR(50) COMMENT 'IP地址',
                    operation_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '操作时间',
                    INDEX idx_user (user_id),
                    INDEX idx_time (operation_time)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='操作日志表'
            """
        }
        
        try:
            conn = self._get_connection(use_database=True)
            cursor = conn.cursor()
            
            for table_name, create_sql in tables_sql.items():
                print(f"  创建表 {table_name}...")
                cursor.execute(create_sql)
                
            conn.commit()
            cursor.close()
            conn.close()
            
            print("  ✓ 所有表创建完成")
            return True
        except Exception as e:
            print(f"  ✗ 创建表失败: {e}")
            return False
            
    def _insert_initial_data(self):
        """插入初始数据"""
        print("\n[3/3] 插入初始数据...")
        
        try:
            conn = self._get_connection(use_database=True)
            cursor = conn.cursor()
            
            # 检查是否已有管理员账号
            cursor.execute("SELECT COUNT(*) as cnt FROM system_users WHERE role = 'admin'")
            result = cursor.fetchone()
            
            if result['cnt'] > 0:
                print("  - 已存在管理员账号，跳过初始数据插入")
                cursor.close()
                conn.close()
                return True
                
            # 插入教师数据
            print("  插入教师数据...")
            teachers_data = [
                ('T001', '张教授', '男', '教授', '计算机学院', '13800000001', 'zhang@edu.cn'),
                ('T002', '李副教授', '女', '副教授', '计算机学院', '13800000002', 'li@edu.cn'),
                ('T003', '王讲师', '男', '讲师', '数学学院', '13800000003', 'wang@edu.cn'),
            ]
            cursor.executemany(
                "INSERT IGNORE INTO teachers (teacher_id, name, gender, title, department, phone, email) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s)",
                teachers_data
            )
            
            # 插入学生数据
            print("  插入学生数据...")
            students_data = [
                ('2024001', '张三', '男', 20, '计算机科学与技术', '计科2401', '13900000001', 'zhangsan@stu.edu.cn'),
                ('2024002', '李四', '女', 19, '计算机科学与技术', '计科2401', '13900000002', 'lisi@stu.edu.cn'),
                ('2024003', '王五', '男', 21, '软件工程', '软工2401', '13900000003', 'wangwu@stu.edu.cn'),
                ('2024004', '赵六', '女', 20, '软件工程', '软工2401', '13900000004', 'zhaoliu@stu.edu.cn'),
                ('2024005', '钱七', '男', 19, '数据科学', '数科2401', '13900000005', 'qianqi@stu.edu.cn'),
            ]
            cursor.executemany(
                "INSERT IGNORE INTO students (student_id, name, gender, age, major, class_name, phone, email) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                students_data
            )
            
            # 插入课程数据
            print("  插入课程数据...")
            courses_data = [
                ('CS101', 'Python程序设计', 3.0, 48, 'T001', '计算机学院', '2024-1', '必修', 120, 'A101', '周一 1-2节'),
                ('CS102', '数据结构', 4.0, 64, 'T001', '计算机学院', '2024-1', '必修', 100, 'A102', '周二 3-4节'),
                ('CS103', '数据库原理', 3.0, 48, 'T002', '计算机学院', '2024-1', '必修', 100, 'A103', '周三 1-2节'),
                ('CS201', '机器学习', 3.0, 48, 'T002', '计算机学院', '2024-1', '选修', 60, 'B201', '周四 5-6节'),
                ('MA101', '高等数学', 4.0, 64, 'T003', '数学学院', '2024-1', '必修', 150, 'C101', '周五 1-2节'),
            ]
            cursor.executemany(
                "INSERT IGNORE INTO courses (course_id, course_name, credits, hours, teacher_id, "
                "department, semester, course_type, max_students, classroom, schedule) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                courses_data
            )
            
            # 插入选课数据
            print("  插入选课数据...")
            enrollments_data = [
                ('2024001', 'CS101', '2024-1', 85.5, 'B+'),
                ('2024001', 'CS102', '2024-1', 92.0, 'A'),
                ('2024001', 'MA101', '2024-1', 78.0, 'C+'),
                ('2024002', 'CS101', '2024-1', 88.0, 'B+'),
                ('2024002', 'CS103', '2024-1', 95.0, 'A'),
                ('2024003', 'CS101', '2024-1', 76.0, 'C+'),
                ('2024003', 'CS201', '2024-1', None, None),
                ('2024004', 'CS102', '2024-1', 82.0, 'B'),
                ('2024005', 'MA101', '2024-1', 90.0, 'A-'),
            ]
            cursor.executemany(
                "INSERT IGNORE INTO enrollments (student_id, course_id, semester, score, grade) "
                "VALUES (%s, %s, %s, %s, %s)",
                enrollments_data
            )
            
            # 插入系统用户（使用MD5作为简单哈希）
            print("  插入系统用户...")
            # 密码: admin123, teacher123, student123
            users_data = [
                ('admin', '0192023a7bbd73250516f069df18b500', 'admin', None, '系统管理员'),
                ('teacher1', '7a33a5654d9e6a34dc0c2e44ea2f7bc9', 'teacher', 'T001', '张教授'),
                ('teacher2', '7a33a5654d9e6a34dc0c2e44ea2f7bc9', 'teacher', 'T002', '李副教授'),
                ('student1', 'e3b0b6e41cdca1a3b3f1d46f3c9a30f3', 'student', '2024001', '张三'),
                ('student2', 'e3b0b6e41cdca1a3b3f1d46f3c9a30f3', 'student', '2024002', '李四'),
            ]
            cursor.executemany(
                "INSERT IGNORE INTO system_users (username, password_hash, role, related_id, real_name) "
                "VALUES (%s, %s, %s, %s, %s)",
                users_data
            )
            
            conn.commit()
            cursor.close()
            conn.close()
            
            print("  ✓ 初始数据插入完成")
            return True
        except Exception as e:
            print(f"  ✗ 插入初始数据失败: {e}")
            return False
            
    def check_database_exists(self):
        """检查数据库是否已初始化"""
        try:
            conn = self._get_connection(use_database=True)
            cursor = conn.cursor()
            
            # 检查关键表是否存在
            cursor.execute("SHOW TABLES LIKE 'system_users'")
            result = cursor.fetchone()
            
            if result:
                # 检查是否有用户数据
                cursor.execute("SELECT COUNT(*) as cnt FROM system_users")
                count = cursor.fetchone()
                cursor.close()
                conn.close()
                return count['cnt'] > 0
                
            cursor.close()
            conn.close()
            return False
        except:
            return False


def init_database(db_config):
    """初始化数据库的便捷函数"""
    initializer = DatabaseInitializer(db_config)
    return initializer.init_database()


def check_database(db_config):
    """检查数据库是否已初始化"""
    initializer = DatabaseInitializer(db_config)
    return initializer.check_database_exists()


# 独立运行时
if __name__ == '__main__':
    config = {
        'host': '192.168.1.91',
        'port': 2883,
        'user': 'root@test',
        'password': '',
        'database': 'student_management',
        'charset': 'utf8mb4'
    }
    
    init_database(config)