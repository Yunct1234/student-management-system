"""
数据库连接管理模块
"""
import pymysql
from pymysql.cursors import DictCursor
from contextlib import contextmanager
import logging
from typing import Optional, Dict, Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseConnection:
    """数据库连接管理类"""
    
    def __init__(self, config: Dict[str, Any]):
        """
        初始化数据库连接
        
        Args:
            config: 数据库配置字典
        """
        self.config = config
        self.connection = None
        
    def connect(self) -> pymysql.Connection:
        """建立数据库连接"""
        try:
            if not self.connection or not self.connection.open:
                # 特殊处理student_management数据库
                config = self.config.copy()
                if config.get('database') == 'student_management':
                    # 先连接到oceanbase，再切换数据库
                    config['database'] = 'oceanbase'
                    
                self.connection = pymysql.connect(
                    **config,
                    cursorclass=DictCursor,
                    autocommit=False
                )
                
                # 如果目标是student_management，切换到该数据库
                if self.config.get('database') == 'student_management':
                    cursor = self.connection.cursor()
                    cursor.execute("USE student_management")
                    cursor.close()
                    
                logger.info(f"成功连接到数据库: {self.config['host']}:{self.config['port']}")
            return self.connection
        except pymysql.Error as e:
            logger.error(f"数据库连接失败: {e}")
            raise
                
    def disconnect(self):
        """关闭数据库连接"""
        if self.connection:
            try:
                self.connection.close()
                logger.info("数据库连接已关闭")
            except pymysql.Error as e:
                logger.error(f"关闭连接失败: {e}")
                
    @contextmanager
    def get_cursor(self):
        """获取数据库游标的上下文管理器"""
        connection = self.connect()
        cursor = connection.cursor()
        try:
            yield cursor
            connection.commit()
        except pymysql.Error as e:
            connection.rollback()
            logger.error(f"数据库操作失败: {e}")
            raise
        finally:
            cursor.close()
            
    def execute_query(self, query: str, params: Optional[tuple] = None) -> list:
        """
        执行查询语句
        
        Args:
            query: SQL查询语句
            params: 查询参数
            
        Returns:
            查询结果列表
        """
        with self.get_cursor() as cursor:
            cursor.execute(query, params)
            return cursor.fetchall()
            
    def execute_update(self, query: str, params: Optional[tuple] = None) -> int:
        """
        执行更新语句
        
        Args:
            query: SQL更新语句
            params: 更新参数
            
        Returns:
            影响的行数
        """
        with self.get_cursor() as cursor:
            cursor.execute(query, params)
            return cursor.rowcount
            
    def execute_many(self, query: str, params_list: list) -> int:
        """
        批量执行语句
        
        Args:
            query: SQL语句
            params_list: 参数列表
            
        Returns:
            影响的总行数
        """
        with self.get_cursor() as cursor:
            cursor.executemany(query, params_list)
            return cursor.rowcount
            
    def test_connection(self) -> bool:
        """测试数据库连接"""
        try:
            with self.get_cursor() as cursor:
                cursor.execute("SELECT 1")
                result = cursor.fetchone()
                return result is not None
        except:
            return False
