"""
student.py
学生数据模型
"""
from typing import Dict, Any, List, Optional
from utils.db_connection import DatabaseConnection

class Student:
    """学生模型类"""
    
    def __init__(self, db_connection: DatabaseConnection):
        """初始化学生模型"""
        self.db = db_connection
        
    def create(self, student_data: Dict[str, Any]) -> bool:
        """创建学生"""
        query = """
            INSERT INTO students (
                student_id, name, gender, age, major, 
                class_name, phone, email, enrollment_date, status
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        try:
            params = (
                student_data['student_id'],
                student_data['name'],
                student_data.get('gender', '男'),
                student_data.get('age', 18),
                student_data.get('major', ''),
                student_data.get('class_name', ''),
                student_data.get('phone', ''),
                student_data.get('email', ''),
                student_data.get('enrollment_date'),
                student_data.get('status', '在读')
            )
            result = self.db.execute_update(query, params)
            return result > 0
        except Exception as e:
            print(f"创建学生失败: {e}")
            return False
            
    def get_by_id(self, student_id: str) -> Optional[Dict[str, Any]]:
        """根据学号获取学生"""
        query = "SELECT * FROM students WHERE student_id = %s"
        try:
            results = self.db.execute_query(query, (student_id,))
            return results[0] if results else None
        except Exception as e:
            print(f"查询学生失败: {e}")
            return None
            
    def get_all(self) -> List[Dict[str, Any]]:
        """获取所有学生"""
        query = "SELECT * FROM students ORDER BY student_id"
        try:
            return self.db.execute_query(query)
        except Exception as e:
            print(f"查询所有学生失败: {e}")
            return []
            
    def update(self, student_id: str, update_data: Dict[str, Any]) -> bool:
        """更新学生信息"""
        if not update_data:
            return False
            
        # 构建UPDATE语句
        set_clauses = []
        params = []
        
        for field, value in update_data.items():
            set_clauses.append(f"{field} = %s")
            params.append(value)
            
        params.append(student_id)
        
        query = f"""
            UPDATE students 
            SET {', '.join(set_clauses)}
            WHERE student_id = %s
        """
        
        try:
            result = self.db.execute_update(query, tuple(params))
            return result > 0
        except Exception as e:
            print(f"更新学生失败: {e}")
            return False
            
    def delete(self, student_id: str) -> bool:
        """删除学生"""
        query = "DELETE FROM students WHERE student_id = %s"
        try:
            result = self.db.execute_update(query, (student_id,))
            return result > 0
        except Exception as e:
            print(f"删除学生失败: {e}")
            return False
            
    def search(self, keyword: str = None, major: str = None, 
               class_name: str = None) -> List[Dict[str, Any]]:
        """搜索学生"""
        query = "SELECT * FROM students WHERE 1=1"
        params = []
        
        if keyword:
            query += " AND (student_id LIKE %s OR name LIKE %s OR major LIKE %s)"
            keyword_pattern = f"%{keyword}%"
            params.extend([keyword_pattern, keyword_pattern, keyword_pattern])
            
        if major:
            query += " AND major LIKE %s"
            params.append(f"%{major}%")
            
        if class_name:
            query += " AND class_name = %s"
            params.append(class_name)
            
        query += " ORDER BY student_id"
        
        try:
            return self.db.execute_query(query, tuple(params) if params else None)
        except Exception as e:
            print(f"搜索学生失败: {e}")
            return []
            
    def get_statistics(self) -> Dict[str, Any]:
        """获取学生统计信息"""
        stats = {}
        
        try:
            # 总人数
            query = "SELECT COUNT(*) as total FROM students"
            result = self.db.execute_query(query)
            stats['total_students'] = result[0]['total'] if result else 0
            
            # 按状态统计
            query = """
                SELECT status, COUNT(*) as count 
                FROM students 
                GROUP BY status
            """
            result = self.db.execute_query(query)
            stats['by_status'] = {row['status']: row['count'] for row in result}
            
            # 按专业统计
            query = """
                SELECT major, COUNT(*) as count 
                FROM students 
                WHERE major IS NOT NULL AND major != ''
                GROUP BY major
                ORDER BY count DESC
            """
            result = self.db.execute_query(query)
            stats['by_major'] = {row['major']: row['count'] for row in result}
            
            # 按性别统计
            query = """
                SELECT gender, COUNT(*) as count 
                FROM students 
                GROUP BY gender
            """
            result = self.db.execute_query(query)
            stats['by_gender'] = {row['gender']: row['count'] for row in result}
            
        except Exception as e:
            print(f"获取统计信息失败: {e}")
            
        return stats
