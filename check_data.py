#!/usr/bin/env python3
"""快速检查数据"""
import pymysql

config = {
    'host': '127.0.0.1',
    'port': 2881,
    'user': 'root@sys',
    'password': 'uBSxMCBdTOR4D24mBHP1',
    'database': 'student_management',
    'charset': 'utf8mb4'
}

try:
    conn = pymysql.connect(**config)
    cursor = conn.cursor()
    
    # 检查学生数据
    cursor.execute("SELECT COUNT(*) FROM students")
    count = cursor.fetchone()[0]
    print(f"学生总数: {count}")
    
    if count > 0:
        cursor.execute("SELECT student_id, name, major FROM students LIMIT 3")
        print("\n学生示例:")
        for row in cursor.fetchall():
            print(f"  {row[0]} - {row[1]} - {row[2]}")
    
    # 检查课程数据
    cursor.execute("SELECT COUNT(*) FROM courses")
    count = cursor.fetchone()[0]
    print(f"\n课程总数: {count}")
    
    if count > 0:
        cursor.execute("SELECT course_id, course_name FROM courses LIMIT 3")
        print("\n课程示例:")
        for row in cursor.fetchall():
            print(f"  {row[0]} - {row[1]}")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"错误: {e}")
