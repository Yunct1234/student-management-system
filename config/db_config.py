"""
数据库配置模块
"""
import os
from typing import Dict, Any
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class DBConfig:
    """数据库配置类"""
    
    @staticmethod
    def get_local_config() -> Dict[str, Any]:
        """获取本地连接配置"""
        return {
            'host': os.getenv('DB_HOST', '127.0.0.1'),
            'port': int(os.getenv('DB_PORT', 2881)),
            'user': os.getenv('DB_USER', 'root'),
            'password': os.getenv('DB_PASSWORD', ''),
            'database': os.getenv('DB_DATABASE', 'student_management'),
            'charset': 'utf8mb4'
        }
        
    @staticmethod
    def get_remote_config() -> Dict[str, Any]:
        """获取远程连接配置"""
        return {
            'host': os.getenv('REMOTE_DB_HOST', '192.168.31.35'),
            'port': int(os.getenv('REMOTE_DB_PORT', 2881)),
            'user': os.getenv('REMOTE_DB_USER', 'remote_user'),
            'password': os.getenv('REMOTE_DB_PASSWORD', ''),
            'database': os.getenv('DB_DATABASE', 'student_management'),
            'charset': 'utf8mb4'
        }
