#!/usr/bin/env python3
"""
main.py
学生信息管理系统 - 主程序入口
自动检查并初始化数据库
"""
import os
import sys

# 确保能正确导入模块
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.db_init import check_database, init_database


def main():
    """主函数"""
    # 数据库配置 - 修改为正确的本地Docker配置
    db_config = {
        'host': '127.0.0.1',          # 本地Docker用127.0.0.1
        'port': 2881,                  # Docker映射端口是2881
        'user': 'root@test',           # OceanBase用户名
        'password': '',                # 默认空密码
        'database': 'student_management',
        'charset': 'utf8mb4'
    }

    print("\n" + "=" * 50)
    print("学生信息管理系统 v2.0".center(46))
    print("=" * 50)
    
    # 检查数据库是否已初始化
    print("\n正在检查数据库...")
    
    if not check_database(db_config):
        print("检测到数据库未初始化")
        choice = input("\n是否现在初始化数据库？(y/n): ").strip().lower()
        
        if choice == 'y':
            if not init_database(db_config):
                print("\n数据库初始化失败，程序退出")
                return
            print("\n" + "-" * 50)
        else:
            print("请先初始化数据库后再运行程序")
            print("可以运行: python utils/db_init.py")
            return
    else:
        print("✓ 数据库已就绪")
    
    # 导入并运行客户端
    from client.role_based_client import UnifiedClient
    
    print("\n正在启动系统...")
    client = UnifiedClient(db_config)
    
    if client.test_connection():
        print("✓ 数据库连接成功\n")
        client.run()
    else:
        print("✗ 数据库连接失败，请检查配置")


if __name__ == '__main__':
    main()
