"""
课程模型类
"""
from typing import Optional, List, Dict, Any
from utils.db_connection import DatabaseConnection

class Course:
    """课程信息管理类"""
    
    def __init__(self, db_connection: DatabaseConnection):
        """
        初始化课程管理类
        
        Args:
            db_connection: 数据库连接对象
        """
        self.db = db_connection
        
    def create(self, course_data: Dict[str, Any]) -> bool:
        """
        创建新课程
        
        Args:
            course_data: 课程信息字典
            
        Returns:
            是否创建成功
        """
        query = """
            INSERT INTO courses (course_id, course_name, credits, teacher, 
                               department, semester, course_type, max_students, 
                               classroom, schedule, description)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (
            course_data['course_id'],
            course_data['course_name'],
            course_data['credits'],
            course_data.get('teacher'),
            course_data.get('department'),
            course_data.get('semester'),
            course_data['course_type'],
            course_data.get('max_students', 100),
            course_data.get('classroom'),
            course_data.get('schedule'),
            course_data.get('description')
        )
        
        try:
            rows_affected = self.db.execute_update(query, params)
            return rows_affected > 0
        except Exception as e:
            print(f"创建课程失败: {e}")
            return False
            
    def get_by_id(self, course_id: str) -> Optional[Dict[str, Any]]:
        """
        根据课程编号获取课程信息
        
        Args:
            course_id: 课程编号
            
        Returns:
            课程信息字典或None
        """
        query = "SELECT * FROM courses WHERE course_id = %s"
        results = self.db.execute_query(query, (course_id,))
        return results[0] if results else None
        
    def get_all(self, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        """
        获取所有课程信息
        
        Args:
            limit: 每页记录数
            offset: 偏移量
            
        Returns:
            课程信息列表
        """
        query = "SELECT * FROM courses ORDER BY course_id LIMIT %s OFFSET %s"
        return self.db.execute_query(query, (limit, offset))
        
    def get_available_courses(self, semester: str) -> List[Dict[str, Any]]:
        """
        获取指定学期可选课程
        
        Args:
            semester: 学期
            
        Returns:
            可选课程列表
        """
        query = """
            SELECT * FROM courses 
            WHERE semester = %s AND current_students < max_students
            ORDER BY course_id
        """
        return self.db.execute_query(query, (semester,))
        
    def update(self, course_id: str, update_data: Dict[str, Any]) -> bool:
        """
        更新课程信息
        
        Args:
            course_id: 课程编号
            update_data: 更新数据字典
            
        Returns:
            是否更新成功
        """
        set_clauses = []
        params = []
        
        for key, value in update_data.items():
            if key != 'course_id':  # 课程编号不能更新
                set_clauses.append(f"{key} = %s")
                params.append(value)
                
        if not set_clauses:
            return False
            
        params.append(course_id)
        query = f"UPDATE courses SET {', '.join(set_clauses)} WHERE course_id = %s"
        
        try:
            rows_affected = self.db.execute_update(query, tuple(params))
            return rows_affected > 0
        except Exception as e:
            print(f"更新课程失败: {e}")
            return False
            
    def delete(self, course_id: str) -> bool:
        """
        删除课程
        
        Args:
            course_id: 课程编号
            
        Returns:
            是否删除成功
        """
        query = "DELETE FROM courses WHERE course_id = %s"
        
        try:
            rows_affected = self.db.execute_update(query, (course_id,))
            return rows_affected > 0
        except Exception as e:
            print(f"删除课程失败: {e}")
            return False
            
    def update_enrollment_count(self, course_id: str, delta: int) -> bool:
        """
        更新课程选课人数
        
        Args:
            course_id: 课程编号
            delta: 人数变化（正数为增加，负数为减少）
            
        Returns:
            是否更新成功
        """
        query = """
            UPDATE courses 
            SET current_students = current_students + %s
            WHERE course_id = %s AND current_students + %s >= 0 
                  AND current_students + %s <= max_students
        """
        
        try:
            rows_affected = self.db.execute_update(
                query, (delta, course_id, delta, delta)
            )
            return rows_affected > 0
        except Exception as e:
            print(f"更新选课人数失败: {e}")
            return False
            
    def search(self, **kwargs) -> List[Dict[str, Any]]:
        """
        根据条件搜索课程
        
        Args:
            **kwargs: 搜索条件
            
        Returns:
            符合条件的课程列表
        """
        where_clauses = []
        params = []
        
        for key, value in kwargs.items():
            if value is not None:
                if key in ['course_name', 'teacher', 'department']:
                    where_clauses.append(f"{key} LIKE %s")
                    params.append(f"%{value}%")
                else:
                    where_clauses.append(f"{key} = %s")
                    params.append(value)
                    
        query = "SELECT * FROM courses"
        if where_clauses:
            query += f" WHERE {' AND '.join(where_clauses)}"
            
        return self.db.execute_query(query, tuple(params))
        
    def get_statistics(self) -> Dict[str, Any]:
        """
        获取课程统计信息
        
        Returns:
            统计信息字典
        """
        stats = {}
        
        # 总课程数
        query = "SELECT COUNT(*) as total FROM courses"
        result = self.db.execute_query(query)
        stats['total_courses'] = result[0]['total'] if result else 0
        
        # 按类型统计
        query = """
            SELECT course_type, COUNT(*) as count 
            FROM courses 
            GROUP BY course_type
        """
        stats['by_type'] = self.db.execute_query(query)
        
        # 按学期统计
        query = """
            SELECT semester, COUNT(*) as count 
            FROM courses 
            GROUP BY semester 
            ORDER BY semester DESC
        """
        stats['by_semester'] = self.db.execute_query(query)
        
        # 选课率统计
        query = """
            SELECT 
                AVG(current_students * 100.0 / max_students) as avg_enrollment_rate,
                MAX(current_students * 100.0 / max_students) as max_enrollment_rate,
                MIN(current_students * 100.0 / max_students) as min_enrollment_rate
            FROM courses
            WHERE max_students > 0
        """
        result = self.db.execute_query(query)
        stats['enrollment_rate'] = result[0] if result else {}
        
        return stats
