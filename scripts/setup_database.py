"""
数据库初始化脚本
"""
import os
import sys
import pymysql
from colorama import init, Fore, Style

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.db_config import DBConfig

init(autoreset=True)

def setup_database():
    """初始化数据库"""
    print(f"{Fore.CYAN}开始初始化数据库...")
    
    # 获取配置
    config = DBConfig.get_local_config()
    
    try:
        # 连接数据库
        conn = pymysql.connect(
            host=config['host'],
            port=config['port'],
            user=config['user'],
            password=config['password'],
            charset=config['charset']
        )
        cursor = conn.cursor()
        
        print(f"{Fore.GREEN}✓ 连接数据库成功")
        
        # 创建数据库
        cursor.execute("CREATE DATABASE IF NOT EXISTS student_management")
        cursor.execute("USE student_management")
        print(f"{Fore.GREEN}✓ 创建数据库成功")
        
        # 创建表的SQL语句
        sql_statements = [
            # 学生表
            """CREATE TABLE IF NOT EXISTS students (
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
            )""",
            
            # 课程表
            """CREATE TABLE IF NOT EXISTS courses (
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
            )""",
            
            # 选课表
            """CREATE TABLE IF NOT EXISTS enrollments (
                enrollment_id INT PRIMARY KEY AUTO_INCREMENT,
                student_id VARCHAR(20),
                course_id VARCHAR(20),
                semester VARCHAR(20),
                score DECIMAL(5,2),
                grade VARCHAR(10),
                status VARCHAR(20) DEFAULT '已选',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE KEY uk_enrollment (student_id, course_id, semester)
            )"""
        ]
        
        for sql in sql_statements:
            cursor.execute(sql)
            conn.commit()
        
        print(f"{Fore.GREEN}✓ 创建表结构成功")
        
        # 插入示例数据
        sample_data = [
            "INSERT IGNORE INTO students VALUES ('2021001', '张三', '男', 20, '计算机科学', '计科2101', '13800138001', 'zhangsan@example.com', '2021-09-01', '在读', DEFAULT)",
            "INSERT IGNORE INTO students VALUES ('2021002', '李四', '女', 21, '软件工程', '软件2101', '13800138002', 'lisi@example.com', '2021-09-01', '在读', DEFAULT)",
            "INSERT IGNORE INTO courses VALUES ('CS101', '数据结构', 4.0, '王教授', '计算机学院', '2024-1', '必修', 100, '教301', '周一1-2节', DEFAULT)",
            "INSERT IGNORE INTO courses VALUES ('CS102', '数据库系统', 3.0, '李教授', '计算机学院', '2024-1', '必修', 100, '教302', '周二3-4节', DEFAULT)"
        ]
        
        for sql in sample_data:
            try:
                cursor.execute(sql)
                conn.commit()
            except Exception as e:
                print(f"{Fore.YELLOW}⚠ 插入示例数据: {e}")
        
        print(f"{Fore.GREEN}✓ 插入示例数据成功")
        
        cursor.close()
        conn.close()
        
        print(f"\n{Fore.GREEN}数据库初始化完成！")
        
    except Exception as e:
        print(f"{Fore.RED}数据库初始化失败: {e}")
        
if __name__ == "__main__":
    setup_database()
