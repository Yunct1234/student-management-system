#!/usr/bin/env python3
"""
完整的数据库初始化脚本 - 包含表结构和示例数据
"""
import pymysql
import sys
from datetime import datetime, date
import random

# OceanBase连接配置
DB_CONFIG = {
    'host': '127.0.0.1',
    'port': 2881,
    'user': 'root@sys',
    'password': 'uBSxMCBdTOR4D24mBHP1',
    'charset': 'utf8mb4'
}

def init_database():
    """初始化数据库和表结构"""
    conn = None
    try:
        print("=" * 60)
        print("OceanBase 学生管理系统 - 数据库初始化")
        print("=" * 60)
        
        # 连接数据库
        print("\n1. 连接到OceanBase...")
        conn = pymysql.connect(**DB_CONFIG)
        cursor = conn.cursor()
        print("   ✓ 连接成功")
        
        # 创建数据库
        print("\n2. 创建数据库...")
        cursor.execute("CREATE DATABASE IF NOT EXISTS student_management DEFAULT CHARACTER SET utf8mb4")
        cursor.execute("USE student_management")
        print("   ✓ 数据库创建成功")
        
        # 删除旧表（如果需要重新初始化）
        print("\n3. 清理旧数据...")
        cursor.execute("DROP TABLE IF EXISTS enrollments")
        cursor.execute("DROP TABLE IF EXISTS students")
        cursor.execute("DROP TABLE IF EXISTS courses")
        print("   ✓ 旧表已清理")
        
        # 创建学生表
        print("\n4. 创建表结构...")
        cursor.execute("""
            CREATE TABLE students (
                student_id VARCHAR(20) PRIMARY KEY,
                name VARCHAR(50) NOT NULL,
                gender VARCHAR(10),
                age INT,
                major VARCHAR(100),
                class_name VARCHAR(50),
                phone VARCHAR(20),
                email VARCHAR(100),
                enrollment_date DATE,
                status VARCHAR(20) DEFAULT '在读',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            ) DEFAULT CHARSET=utf8mb4
        """)
        print("   ✓ 学生表创建成功")
        
        # 创建课程表
        cursor.execute("""
            CREATE TABLE courses (
                course_id VARCHAR(20) PRIMARY KEY,
                course_name VARCHAR(100) NOT NULL,
                credits DECIMAL(3,1),
                teacher VARCHAR(50),
                department VARCHAR(100),
                semester VARCHAR(20),
                course_type VARCHAR(20),
                max_students INT DEFAULT 100,
                classroom VARCHAR(50),
                schedule VARCHAR(100),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            ) DEFAULT CHARSET=utf8mb4
        """)
        print("   ✓ 课程表创建成功")
        
        # 创建选课表
        cursor.execute("""
            CREATE TABLE enrollments (
                enrollment_id INT PRIMARY KEY AUTO_INCREMENT,
                student_id VARCHAR(20),
                course_id VARCHAR(20),
                semester VARCHAR(20),
                score DECIMAL(5,2),
                grade VARCHAR(10),
                status VARCHAR(20) DEFAULT '已选',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
                FOREIGN KEY (course_id) REFERENCES courses(course_id) ON DELETE CASCADE,
                UNIQUE KEY uk_enrollment (student_id, course_id, semester)
            ) DEFAULT CHARSET=utf8mb4
        """)
        print("   ✓ 选课表创建成功")
        
        # 插入学生示例数据
        print("\n5. 插入示例数据...")
        students_data = [
            ('2021001', '张三', '男', 20, '计算机科学与技术', '计科2101', '13800138001', 'zhangsan@example.com', '2021-09-01', '在读'),
            ('2021002', '李四', '女', 21, '计算机科学与技术', '计科2101', '13800138002', 'lisi@example.com', '2021-09-01', '在读'),
            ('2021003', '王五', '男', 20, '软件工程', '软件2101', '13800138003', 'wangwu@example.com', '2021-09-01', '在读'),
            ('2021004', '赵六', '女', 21, '软件工程', '软件2101', '13800138004', 'zhaoliu@example.com', '2021-09-01', '在读'),
            ('2021005', '钱七', '男', 22, '信息安全', '信安2101', '13800138005', 'qianqi@example.com', '2021-09-01', '在读'),
            ('2022001', '孙八', '女', 19, '计算机科学与技术', '计科2201', '13800138006', 'sunba@example.com', '2022-09-01', '在读'),
            ('2022002', '周九', '男', 20, '人工智能', 'AI2201', '13800138007', 'zhoujiu@example.com', '2022-09-01', '在读'),
            ('2022003', '吴十', '女', 19, '数据科学', '数据2201', '13800138008', 'wushi@example.com', '2022-09-01', '在读'),
            ('2023001', '郑十一', '男', 18, '计算机科学与技术', '计科2301', '13800138009', 'zheng11@example.com', '2023-09-01', '在读'),
            ('2023002', '陈十二', '女', 19, '网络工程', '网络2301', '13800138010', 'chen12@example.com', '2023-09-01', '在读')
        ]
        
        for student in students_data:
            cursor.execute("""
                INSERT INTO students (student_id, name, gender, age, major, class_name, phone, email, enrollment_date, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, student)
        print(f"   ✓ 插入 {len(students_data)} 条学生数据")
        
        # 插入课程示例数据
        courses_data = [
            ('CS101', '数据结构', 4.0, '王教授', '计算机学院', '2024-1', '必修', 100, '教301', '周一1-2节,周三3-4节'),
            ('CS102', '数据库系统', 3.0, '李教授', '计算机学院', '2024-1', '必修', 100, '教302', '周二3-4节,周四5-6节'),
            ('CS103', '操作系统', 4.0, '张教授', '计算机学院', '2024-1', '必修', 80, '教303', '周一5-6节,周三7-8节'),
            ('CS104', '计算机网络', 3.0, '刘教授', '计算机学院', '2024-1', '必修', 80, '教304', '周二7-8节,周五1-2节'),
            ('CS201', '算法设计', 3.0, '陈教授', '计算机学院', '2024-1', '选修', 60, '教401', '周一7-8节,周四1-2节'),
            ('CS202', '人工智能基础', 3.0, '赵教授', '计算机学院', '2024-1', '选修', 60, '教402', '周三5-6节,周五3-4节'),
            ('CS203', '机器学习', 3.0, '周教授', '计算机学院', '2024-1', '选修', 50, '教403', '周二1-2节,周四7-8节'),
            ('MATH101', '高等数学', 4.0, '孙教授', '数学学院', '2024-1', '必修', 120, '理101', '周一3-4节,周三1-2节'),
            ('ENG101', '大学英语', 2.0, '外教Tom', '外语学院', '2024-1', '必修', 30, '外201', '周二5-6节'),
            ('PE101', '体育', 1.0, '体育组', '体育学院', '2024-1', '必修', 50, '体育馆', '周五7-8节')
        ]
        
        for course in courses_data:
            cursor.execute("""
                INSERT INTO courses (course_id, course_name, credits, teacher, department, semester, course_type, max_students, classroom, schedule)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, course)
        print(f"   ✓ 插入 {len(courses_data)} 条课程数据")
        
        # 插入选课示例数据
        enrollments_data = []
        # 为每个学生随机选择3-5门课
        for student in students_data:
            student_id = student[0]
            num_courses = random.randint(3, 5)
            selected_courses = random.sample(courses_data, num_courses)
            
            for course in selected_courses:
                course_id = course[0]
                # 随机生成成绩（60-100分）
                score = round(random.uniform(60, 100), 1) if random.random() > 0.2 else None
                
                # 根据成绩计算等级
                if score is None:
                    grade = None
                elif score >= 90:
                    grade = 'A'
                elif score >= 80:
                    grade = 'B'
                elif score >= 70:
                    grade = 'C'
                elif score >= 60:
                    grade = 'D'
                else:
                    grade = 'F'
                
                enrollments_data.append((student_id, course_id, '2024-1', score, grade, '已选'))
        
        for enrollment in enrollments_data:
            try:
                cursor.execute("""
                    INSERT INTO enrollments (student_id, course_id, semester, score, grade, status)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, enrollment)
            except pymysql.IntegrityError:
                # 忽略重复选课
                pass
        
        print(f"   ✓ 插入 {len(enrollments_data)} 条选课记录")
        
        # 提交事务
        conn.commit()
        
        # 显示统计信息
        print("\n6. 数据统计...")
        cursor.execute("SELECT COUNT(*) FROM students")
        student_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM courses")
        course_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM enrollments")
        enrollment_count = cursor.fetchone()[0]
        
        print(f"   • 学生总数: {student_count}")
        print(f"   • 课程总数: {course_count}")
        print(f"   • 选课记录: {enrollment_count}")
        
        # 创建用户（用于远程访问）
        print("\n7. 创建访问用户...")
        try:
            cursor.execute("CREATE USER IF NOT EXISTS 'student_user'@'%' IDENTIFIED BY 'Student@123'")
            cursor.execute("GRANT ALL PRIVILEGES ON student_management.* TO 'student_user'@'%'")
            cursor.execute("FLUSH PRIVILEGES")
            print("   ✓ 创建用户 student_user (密码: Student@123)")
        except:
            print("   ⚠ 用户可能已存在")
        
        print("\n" + "=" * 60)
        print("✓ 数据库初始化完成！")
        print("=" * 60)
        print("\n可以使用以下命令连接数据库：")
        print(f"  mysql -h127.0.0.1 -P2881 -uroot@sys -p'{DB_CONFIG['password']}' -Dstudent_management")
        print("\n或者运行主程序：")
        print("  python3 main.py")
        
    except Exception as e:
        print(f"\n✗ 错误: {e}")
        if conn:
            conn.rollback()
        sys.exit(1)
    finally:
        if conn:
            cursor.close()
            conn.close()

def verify_data():
    """验证数据是否正确插入"""
    try:
        conn = pymysql.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("USE student_management")
        
        print("\n验证数据...")
        
        # 查询示例学生
        cursor.execute("SELECT student_id, name, major FROM students LIMIT 5")
        students = cursor.fetchall()
        print("\n学生示例：")
        for s in students:
            print(f"  {s[0]} - {s[1]} ({s[2]})")
        
        # 查询示例课程
        cursor.execute("SELECT course_id, course_name, teacher FROM courses LIMIT 5")
        courses = cursor.fetchall()
        print("\n课程示例：")
        for c in courses:
            print(f"  {c[0]} - {c[1]} ({c[2]})")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"验证失败: {e}")

if __name__ == "__main__":
    # 确认执行
    print("此脚本将重新初始化数据库，所有现有数据将被删除！")
    confirm = input("确认执行？(yes/no): ")
    
    if confirm.lower() == 'yes':
        init_database()
        verify_data()
    else:
        print("已取消")
