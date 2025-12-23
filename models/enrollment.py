"""
enrollment.py
选课数据模型
"""
from typing import Dict, Any, List, Optional
from utils.db_connection import DatabaseConnection

class Enrollment:
    """选课模型类"""
    
    def __init__(self, db_connection: DatabaseConnection):
        """初始化选课模型"""
        self.db = db_connection
        
    def enroll(self, enrollment_data: Dict[str, Any]) -> bool:
        """学生选课"""
        # 检查是否已选
        check_query = """
            SELECT COUNT(*) as count FROM enrollments 
            WHERE student_id = %s AND course_id = %s AND semester = %s
        """
        
        try:
            result = self.db.execute_query(check_query, (
                enrollment_data['student_id'],
                enrollment_data['course_id'],
                enrollment_data['semester']
            ))
            
            if result[0]['count'] > 0:
                print("该学生已选修此课程")
                return False
                
            # 执行选课
            insert_query = """
                INSERT INTO enrollments (student_id, course_id, semester, status)
                VALUES (%s, %s, %s, '已选')
            """
            
            result = self.db.execute_update(insert_query, (
                enrollment_data['student_id'],
                enrollment_data['course_id'],
                enrollment_data['semester']
            ))
            
            return result > 0
            
        except Exception as e:
            print(f"选课失败: {e}")
            return False
            
    def drop_course(self, student_id: str, course_id: str, semester: str) -> bool:
        """学生退选"""
        query = """
            DELETE FROM enrollments 
            WHERE student_id = %s AND course_id = %s AND semester = %s
        """
        
        try:
            result = self.db.execute_update(query, (student_id, course_id, semester))
            return result > 0
        except Exception as e:
            print(f"退选失败: {e}")
            return False
            
    def get_student_courses(self, student_id: str) -> List[Dict[str, Any]]:
        """获取学生选课列表"""
        # 修复：通过JOIN teachers表获取教师姓名
        query = """
            SELECT e.*, c.course_name, c.credits, c.course_type,
                   COALESCE(t.name, '-') as teacher
            FROM enrollments e
            JOIN courses c ON e.course_id = c.course_id
            LEFT JOIN teachers t ON c.teacher_id = t.teacher_id
            WHERE e.student_id = %s
            ORDER BY e.semester DESC, c.course_id
        """
        
        try:
            return self.db.execute_query(query, (student_id,))
        except Exception as e:
            print(f"查询选课失败: {e}")
            return []
            
    def get_course_students(self, course_id: str, semester: str) -> List[Dict[str, Any]]:
        """获取课程选课学生名单"""
        query = """
            SELECT e.*, s.name, s.major, s.class_name
            FROM enrollments e
            JOIN students s ON e.student_id = s.student_id
            WHERE e.course_id = %s AND e.semester = %s
            ORDER BY s.student_id
        """
        
        try:
            return self.db.execute_query(query, (course_id, semester))
        except Exception as e:
            print(f"查询选课名单失败: {e}")
            return []
            
    def input_score(self, student_id: str, course_id: str, 
                   semester: str, score: float) -> bool:
        """录入成绩"""
        # 计算等级
        if score >= 90:
            grade = '优秀'
        elif score >= 80:
            grade = '良好'
        elif score >= 70:
            grade = '中等'
        elif score >= 60:
            grade = '及格'
        else:
            grade = '不及格'
            
        query = """
            UPDATE enrollments 
            SET score = %s, grade = %s
            WHERE student_id = %s AND course_id = %s AND semester = %s
        """
        
        try:
            result = self.db.execute_update(query, 
                (score, grade, student_id, course_id, semester))
            return result > 0
        except Exception as e:
            print(f"录入成绩失败: {e}")
            return False
            
    def get_student_scores(self, student_id: str) -> List[Dict[str, Any]]:
        """获取学生成绩"""
        query = """
            SELECT e.*, c.course_name, c.credits
            FROM enrollments e
            JOIN courses c ON e.course_id = c.course_id
            WHERE e.student_id = %s AND e.score IS NOT NULL
            ORDER BY e.semester DESC, c.course_id
        """
        
        try:
            return self.db.execute_query(query, (student_id,))
        except Exception as e:
            print(f"查询成绩失败: {e}")
            return []
            
    def get_course_score_distribution(self, course_id: str, 
                                     semester: str) -> Dict[str, Any]:
        """获取课程成绩分布"""
        stats = {}
        
        try:
            # 基本统计
            query = """
                SELECT 
                    COUNT(*) as total,
                    AVG(score) as avg_score,
                    MAX(score) as max_score,
                    MIN(score) as min_score
                FROM enrollments
                WHERE course_id = %s AND semester = %s AND score IS NOT NULL
            """
            
            result = self.db.execute_query(query, (course_id, semester))
            if result:
                stats.update(result[0])
                
            # 分数段分布
            query = """
                SELECT 
                    CASE 
                        WHEN score >= 90 THEN '90-100'
                        WHEN score >= 80 THEN '80-89'
                        WHEN score >= 70 THEN '70-79'
                        WHEN score >= 60 THEN '60-69'
                        ELSE '0-59'
                    END as score_range,
                    COUNT(*) as count
                FROM enrollments
                WHERE course_id = %s AND semester = %s AND score IS NOT NULL
                GROUP BY score_range
                ORDER BY score_range DESC
            """
            
            result = self.db.execute_query(query, (course_id, semester))
            stats['distribution'] = {row['score_range']: row['count'] for row in result}
            
        except Exception as e:
            print(f"获取成绩分布失败: {e}")
            
        return stats
        
    def get_statistics(self) -> Dict[str, Any]:
        """获取选课统计信息"""
        stats = {}
        
        try:
            # 总选课记录数
            query = "SELECT COUNT(*) as total FROM enrollments"
            result = self.db.execute_query(query)
            stats['total_enrollments'] = result[0]['total'] if result else 0
            
            # 热门课程
            query = """
                SELECT c.course_name, COUNT(*) as count
                FROM enrollments e
                JOIN courses c ON e.course_id = c.course_id
                GROUP BY c.course_id, c.course_name
                ORDER BY count DESC
                LIMIT 10
            """
            result = self.db.execute_query(query)
            stats['popular_courses'] = result
            
            # 学生选课数分布
            query = """
                SELECT course_count, COUNT(*) as student_count
                FROM (
                    SELECT student_id, COUNT(*) as course_count
                    FROM enrollments
                    GROUP BY student_id
                ) t
                GROUP BY course_count
                ORDER BY course_count
            """
            result = self.db.execute_query(query)
            stats['student_course_count'] = {
                row['course_count']: row['student_count'] for row in result
            }
            
        except Exception as e:
            print(f"获取统计信息失败: {e}")
            
        return stats
        
    def get_score_statistics(self, semester: str = None) -> Dict[str, Any]:
        """获取成绩统计"""
        stats = {}
        
        try:
            # 构建查询条件
            where_clause = "WHERE score IS NOT NULL"
            params = []
            
            if semester:
                where_clause += " AND semester = %s"
                params.append(semester)
                
            # 总体统计
            query = f"""
                SELECT 
                    COUNT(*) as total_scores,
                    AVG(score) as overall_avg
                FROM enrollments
                {where_clause}
            """
            
            result = self.db.execute_query(query, tuple(params) if params else None)
            if result:
                stats.update(result[0])
                
            # 等级分布
            query = f"""
                SELECT grade, COUNT(*) as count
                FROM enrollments
                {where_clause}
                GROUP BY grade
            """
            
            result = self.db.execute_query(query, tuple(params) if params else None)
            stats['grade_distribution'] = {row['grade']: row['count'] for row in result}
            
            # 不及格学生
            query = f"""
                SELECT DISTINCT s.student_id, s.name
                FROM enrollments e
                JOIN students s ON e.student_id = s.student_id
                {where_clause} AND e.score < 60
            """
            
            result = self.db.execute_query(query, tuple(params) if params else None)
            stats['failed_students'] = result
            
        except Exception as e:
            print(f"获取成绩统计失败: {e}")
            
        return stats
