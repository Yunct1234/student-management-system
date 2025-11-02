#!/usr/bin/env python3
"""快速测试连接"""
import pymysql

# OceanBase连接参数
config = {
    'host': '127.0.0.1',
    'port': 2881,
    'user': 'root@sys',
    'password': 'u',
    'charset': 'utf8mb4'
}

try:
    conn = pymysql.connect(**config)
    print("✓ 连接成功！")
    
    cursor = conn.cursor()
    cursor.execute("SELECT VERSION()")
    version = cursor.fetchone()
    print(f"OceanBase版本: {version[0]}")
    
    cursor.execute("SHOW DATABASES")
    databases = cursor.fetchall()
    print("\n现有数据库:")
    for db in databases:
        print(f"  - {db[0]}")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"✗ 连接失败: {e}")
