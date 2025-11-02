"""
数据库配置管理
"""
import os
from typing import Dict, Any

class DBConfig:
    """数据库配置类"""
    
    @staticmethod
    def get_local_config() -> Dict[str, Any]:
        """获取本地连接配置"""
        return {
            'host': '127.0.0.1',
            'port': 2881,
            'user': 'root',
            'password': '',  # OceanBase All in One 默认无密码
            'database': 'student_management',
            'charset': 'utf8mb4'
        }
    
    @staticmethod
    def get_remote_config(host: str, user: str = 'remote_user', 
                         password: str = 'Remote@123') -> Dict[str, Any]:
        """获取远程连接配置"""
        return {
            'host': host,
            'port': 2881,
            'user': user,
            'password': password,
            'database': 'student_management',
            'charset': 'utf8mb4'
        }
