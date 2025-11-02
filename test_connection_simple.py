#!/usr/bin/env python3
"""
简单测试连接
"""
import pymysql

def test_connection():
    config = {
        'host': '127.0.0.1',
        'port': 2881,
        'user': 'root@sys',
        'password': 'u',
        'charset': 'utf8mb4'
    }
    
    try:
        print("测试连接到OceanBase...")
        conn = pymysql.connect(**config)
        print("✓ 连接成功！")
        
        cursor = conn.cursor()
        
        # 显示版本
        cursor.execute("SELECT VERSION()")
        version = cursor.fetchone()
        print(f"OceanBase版本: {version[0]}")
        
        # 显示数据库
        cursor.execute("SHOW DATABASES")
        databases = cursor.fetchall()
        print("\n现有数据库:")
        for db in databases:
            print(f"  - {db[0]}")
        
        # 创建student_management数据库
        print("\n创建student_management数据库...")
        cursor.execute("CREATE DATABASE IF NOT EXISTS student_management")
        print("✓ 数据库创建成功")
        
        # 切换到student_management
        cursor.execute("USE student_management")
        print("✓ 切换到student_management数据库")
        
        # 创建测试表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS test_table (
                id INT PRIMARY KEY,
                name VARCHAR(50)
            )
        """)
        print("✓ 测试表创建成功")
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print("\n所有测试通过！")
        
    except Exception as e:
        print(f"✗ 错误: {e}")

if __name__ == "__main__":
    test_connection()
