"""
数据库配置文件
"""
import os
from dotenv import load_dotenv
from typing import Dict, Any

load_dotenv()

class DBConfig:
    """数据库配置类"""
    
    @staticmethod
    def get_local_config() -> Dict[str, Any]:
        """
        获取本地数据库配置
        
        Returns:
            本地数据库连接配置字典
        """
        return {
            'host': os.getenv('DB_LOCAL_HOST', '127.0.0.1'),  # 改为127.0.0.1
            'port': int(os.getenv('DB_LOCAL_PORT', '2881')),
            'user': os.getenv('DB_LOCAL_USER', 'root'),  # 改为root（去掉@sys）
            'password': os.getenv('DB_LOCAL_PASSWORD', ''),  # 默认密码为空
            'database': os.getenv('DB_LOCAL_DATABASE', 'student_management'),
            'charset': 'utf8mb4',
            'autocommit': True
        }

    # OceanBase 默认配置
    DEFAULT_HOST = 'localhost'
    DEFAULT_PORT = 2881  # OceanBase默认端口
    DEFAULT_USER = 'root@sys'
    DEFAULT_PASSWORD = ''
    DEFAULT_DATABASE = 'student_management'
    DEFAULT_TENANT = 'sys'
    
    @classmethod
    def get_local_config(cls):
        """获取本地数据库配置"""
        return {
            'host': os.getenv('DB_LOCAL_HOST', cls.DEFAULT_HOST),
            'port': int(os.getenv('DB_LOCAL_PORT', cls.DEFAULT_PORT)),
            'user': os.getenv('DB_LOCAL_USER', cls.DEFAULT_USER),
            'password': os.getenv('DB_LOCAL_PASSWORD', cls.DEFAULT_PASSWORD),
            'database': os.getenv('DB_LOCAL_DATABASE', cls.DEFAULT_DATABASE),
            'charset': 'utf8mb4'
        }
    
    @classmethod
    def get_remote_config(cls):
        """获取远程数据库配置"""
        return {
            'host': os.getenv('DB_REMOTE_HOST', '192.168.1.100'),  # 根据实际IP修改
            'port': int(os.getenv('DB_REMOTE_PORT', cls.DEFAULT_PORT)),
            'user': os.getenv('DB_REMOTE_USER', 'remote_user@sys'),
            'password': os.getenv('DB_REMOTE_PASSWORD', 'remote_password'),
            'database': os.getenv('DB_REMOTE_DATABASE', cls.DEFAULT_DATABASE),
            'charset': 'utf8mb4'
        }
