#!/usr/bin/env python3
"""
main.py
学生信息管理系统 - 主程序入口
支持角色权限控制（管理员、教师、学生）
"""
import os
import sys

# 确保能正确导入模块
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from client.role_based_client import UnifiedClient, main

if __name__ == '__main__':
    main()
