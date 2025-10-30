"""
学生模型类
"""
from typing import Optional, List, Dict, Any
from datetime import date
from utils.db_connection import DatabaseConnection

class Student:
    """学生信息管理类"""
    
    def __init__(self, db_connection: DatabaseConnection):
        """
        初始化学生管理类
        
        Args:
            db_connection: 数据库连接对象
        """
        self.db = db_connection
        
    def create(self, student_data: Dict[str, Any]) -> bool:
        """
        创建新学生记录
        
        Args:
            student_data: 学生信息字典
            
        Returns:
            是否创建成功
        """
        query = """
            INSERT INTO students (student_id, name, gender, age, major, 
                                 class_name, phone, email, enrollment_date, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (
            student_data['student_id'],
            student_data['name'],
            student_data['gender'],
            student_data.get('age'),
            student_data['major'],
            student_data.get('class_name'),
            student_data.get('phone'),
            student_data.get('email'),
            student_data.get('enrollment_date', date.today()),
            student_data.get('status', '在读')
        )
        
        try:
            rows_affected = self.db.execute_update(query, params)
            return rows_affected > 0
        except Exception as e:
            print(f"创建学生记录失败: {e}")
            return False
            
    def get_by_id(self, student_id: str) -> Optional[Dict[str, Any]]:
        """
        根据学号获取学生信息
        
        Args:
            student_id: 学号
            
        Returns:
            学生信息字典或None
        """
        query = "SELECT * FROM students WHERE student_id = %s"
        results = self.db.execute_query(query, (student_id,))
        return results[0] if results else None
        
    def get_all(self, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        """
        获取所有学生信息
        
        Args:
            limit: 每页记录数
            offset: 偏移量
            
        Returns:
            学生信息列表
        """
        query = "SELECT * FROM students ORDER BY student_id LIMIT %s OFFSET %s"
        return self.db.execute_query(query, (limit, offset))
        
    def update(self, student_id: str, update_data: Dict[str, Any]) -> bool:
        """
        更新学生信息
        
        Args:
            student_id: 学号
            update_data: 更新数据字典
            
        Returns:
            是否更新成功
        """
        # 构建动态更新语句
        set_clauses = []
        params = []
        
        for key, value in update_data.items():
            if key != 'student_id':  # 学号不能更新
                set_clauses.append(f"{key} = %s")
                params.append(value)
                
        if not set_clauses:
            return False
            
        params.append(student_id)
        query = f"UPDATE students SET {', '.join(set_clauses)} WHERE student_id = %s"
        
        try:
            rows_affected = self.db.execute_update(query, tuple(params))
            return rows_affected > 0
        except Exception as e:
            print(f"更新学生记录失败: {e}")
            return False
            
    def delete(self, student_id: str) -> bool:
        """
        删除学生记录
        
        Args:
            student_id: 学号
            
        Returns:
            是否删除成功
        """
        query = "DELETE FROM students WHERE student_id = %s"
        
        try:
            rows_affected = self.db.execute_update(query, (student_id,))
            return rows_affected > 0
        except Exception as e:
            print(f"删除学生记录失败: {e}")
            return False
            
    def search(self, **kwargs) -> List[Dict[str, Any]]:
        """
        根据条件搜索学生
        
        Args:
            **kwargs: 搜索条件
            
        Returns:
            符合条件的学生列表
        """
        where_clauses = []
        params = []
        
        for key, value in kwargs.items():
            if value is not None:
                if key in ['name', 'major', 'class_name']:
                    where_clauses.append(f"{key} LIKE %s")
                    params.append(f"%{value}%")
                else:
                    where_clauses.append(f"{key} = %s")
                    params.append(value)
                    
        query = "SELECT * FROM students"
        if where_clauses:
            query += f" WHERE {' AND '.join(where_clauses)}"
            
        return self.db.execute_query(query, tuple(params))
        
    def get_statistics(self) -> Dict[str, Any]:
        """
        获取学生统计信息
        
        Returns:
            统计信息字典
        """
        stats = {}
        
        # 总学生数
        query = "SELECT COUNT(*) as total FROM students"
        result = self.db.execute_query(query)
        stats['total_students'] = result[0]['total'] if result else 0
        
        # 按专业统计
        query = """
            SELECT major, COUNT(*) as count 
            FROM students 
            GROUP BY major 
            ORDER BY count DESC
        """
        stats['by_major'] = self.db.execute_query(query)
        
        # 按状态统计
        query = """
            SELECT status, COUNT(*) as count 
            FROM students 
            GROUP BY status
        """
        stats['by_status'] = self.db.execute_query(query)
        
        # 按性别统计
        query = """
            SELECT gender, COUNT(*) as count 
            FROM students 
            GROUP BY gender
        """
        stats['by_gender'] = self.db.execute_query(query)
        
        return stats
