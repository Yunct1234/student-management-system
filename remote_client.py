#!/usr/bin/env python3
"""远程连接测试客户端"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from client.role_based_client import UnifiedClient

def main():
    # 远程连接配置 - 修改为服务器的IP
    remote_config = {
        'host': '192.168.31.35',  # 服务器Windows的局域网IP
        'port': 2881,
        'user': 'remote_user@test',  # 或 remote_user@sys
        'password': 'Remote@123',
        'database': 'student_management',
        'charset': 'utf8mb4'
    }
    
    print("=" * 50)
    print("远程连接测试".center(46))
    print("=" * 50)
    print(f"\n连接目标: {remote_config['host']}:{remote_config['port']}")
    
    client = UnifiedClient(remote_config, mode='remote')
    
    if client.test_connection():
        print("✓ 远程数据库连接成功！")
        client.run()
    else:
        print("✗ 远程连接失败，请检查网络和配置")

if __name__ == '__main__':
    main()