"""
course.py
课程数据模型
"""
from typing import Dict, Any, List, Optional
from utils.db_connection import DatabaseConnection

class Course:
    """课程模型类"""
    
    def __init__(self, db_connection: DatabaseConnection):
        """初始化课程模型"""
        self.db = db_connection
        
    def create(self, course_data: Dict[str, Any]) -> bool:
        """创建课程"""
        query = """
            INSERT INTO courses (
                course_id, course_name, credits, hours, teacher_id, department,
                semester, course_type, max_students, classroom, schedule, description
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        try:
            params = (
                course_data['course_id'],
                course_data['course_name'],
                course_data.get('credits', 2.0),
                course_data.get('hours', 32),
                course_data.get('teacher_id', None),
                course_data.get('department', ''),
                course_data.get('semester', ''),
                course_data.get('course_type', '选修'),
                course_data.get('max_students', 100),
                course_data.get('classroom', ''),
                course_data.get('schedule', ''),
                course_data.get('description', '')
            )
            result = self.db.execute_update(query, params)
            return result > 0
        except Exception as e:
            print(f"创建课程失败: {e}")
            return False
            
    def get_by_id(self, course_id: str) -> Optional[Dict[str, Any]]:
        """根据课程编号获取课程"""
        query = """
            SELECT c.*, COALESCE(t.name, '-') as teacher
            FROM courses c
            LEFT JOIN teachers t ON c.teacher_id = t.teacher_id
            WHERE c.course_id = %s
        """
        try:
            results = self.db.execute_query(query, (course_id,))
            return results[0] if results else None
        except Exception as e:
            print(f"查询课程失败: {e}")
            return None
            
    def get_all(self) -> List[Dict[str, Any]]:
        """获取所有课程"""
        query = """
            SELECT c.*, COALESCE(t.name, '-') as teacher
            FROM courses c
            LEFT JOIN teachers t ON c.teacher_id = t.teacher_id
            ORDER BY c.course_id
        """
        try:
            return self.db.execute_query(query)
        except Exception as e:
            print(f"查询所有课程失败: {e}")
            return []
            
    def update(self, course_id: str, update_data: Dict[str, Any]) -> bool:
        """更新课程信息"""
        if not update_data:
            return False
            
        set_clauses = []
        params = []
        
        for field, value in update_data.items():
            set_clauses.append(f"{field} = %s")
            params.append(value)
            
        params.append(course_id)
        
        query = f"""
            UPDATE courses 
            SET {', '.join(set_clauses)}
            WHERE course_id = %s
        """
        
        try:
            result = self.db.execute_update(query, tuple(params))
            return result > 0
        except Exception as e:
            print(f"更新课程失败: {e}")
            return False
            
    def delete(self, course_id: str) -> bool:
        """删除课程"""
        query = "DELETE FROM courses WHERE course_id = %s"
        try:
            result = self.db.execute_update(query, (course_id,))
            return result > 0
        except Exception as e:
            print(f"删除课程失败: {e}")
            return False
            
    def search(self, keyword: str) -> List[Dict[str, Any]]:
        """搜索课程"""
        query = """
            SELECT c.*, COALESCE(t.name, '-') as teacher
            FROM courses c
            LEFT JOIN teachers t ON c.teacher_id = t.teacher_id
            WHERE c.course_id LIKE %s 
               OR c.course_name LIKE %s 
               OR t.name LIKE %s
            ORDER BY c.course_id
        """
        keyword_pattern = f"%{keyword}%"
        params = (keyword_pattern, keyword_pattern, keyword_pattern)
        
        try:
            return self.db.execute_query(query, params)
        except Exception as e:
            print(f"搜索课程失败: {e}")
            return []
            
    def get_available_courses(self, semester: str) -> List[Dict[str, Any]]:
        """获取可选课程"""
        query = """
            SELECT c.*, COALESCE(t.name, '-') as teacher,
                   (SELECT COUNT(*) FROM enrollments e 
                    WHERE e.course_id = c.course_id 
                      AND e.semester = %s) as enrolled_count
            FROM courses c
            LEFT JOIN teachers t ON c.teacher_id = t.teacher_id
            WHERE c.semester = %s
              AND c.max_students > (
                  SELECT COUNT(*) FROM enrollments e 
                  WHERE e.course_id = c.course_id 
                    AND e.semester = %s
              )
            ORDER BY c.course_id
        """
        
        try:
            return self.db.execute_query(query, (semester, semester, semester))
        except Exception as e:
            print(f"查询可选课程失败: {e}")
            return []
    
    def get_by_teacher(self, teacher_id: str) -> List[Dict[str, Any]]:
        """根据教师ID获取其授课课程"""
        query = """
            SELECT c.*, COALESCE(t.name, '-') as teacher
            FROM courses c
            LEFT JOIN teachers t ON c.teacher_id = t.teacher_id
            WHERE c.teacher_id = %s
            ORDER BY c.course_id
        """
        try:
            return self.db.execute_query(query, (teacher_id,))
        except Exception as e:
            print(f"查询教师课程失败: {e}")
            return []
            
    def get_statistics(self) -> Dict[str, Any]:
        """获取课程统计信息"""
        stats = {}
        
        try:
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
            result = self.db.execute_query(query)
            stats['by_type'] = {row['course_type']: row['count'] for row in result}
            
            # 按学期统计
            query = """
                SELECT semester, COUNT(*) as count 
                FROM courses 
                WHERE semester IS NOT NULL AND semester != ''
                GROUP BY semester
                ORDER BY semester DESC
            """
            result = self.db.execute_query(query)
            stats['by_semester'] = {row['semester']: row['count'] for row in result}
            
            # 按学院统计
            query = """
                SELECT department, COUNT(*) as count 
                FROM courses 
                WHERE department IS NOT NULL AND department != ''
                GROUP BY department
                ORDER BY count DESC
            """
            result = self.db.execute_query(query)
            stats['by_department'] = {row['department']: row['count'] for row in result}
            
        except Exception as e:
            print(f"获取统计信息失败: {e}")
            
        return stats
