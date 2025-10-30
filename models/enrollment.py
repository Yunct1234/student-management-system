"""
选课模型类
"""
from typing import Optional, List, Dict, Any
from datetime import date
from utils.db_connection import DatabaseConnection

class Enrollment:
    """选课信息管理类"""
    
    def __init__(self, db_connection: DatabaseConnection):
        """
        初始化选课管理类
        
        Args:
            db_connection: 数据库连接对象
        """
        self.db = db_connection
        
    def enroll(self, enrollment_data: Dict[str, Any]) -> bool:
        """
        学生选课
        
        Args:
            enrollment_data: 选课信息字典
            
        Returns:
        """
        # 检查是否已选该课程
        check_query = """
            SELECT * FROM enrollments 
            WHERE student_id = %s AND course_id = %s AND semester = %s
        """
        existing = self.db.execute_query(
            check_query, 
            (enrollment_data['student_id'], 
             enrollment_data['course_id'], 
             enrollment_data['semester'])
        )
        
        if existing:
            print("该学生已选择此课程")
            return False
            
        # 检查课程是否还有名额
        course_query = """
            SELECT max_students, current_students 
            FROM courses 
            WHERE course_id = %s
        """
        course_info = self.db.execute_query(course_query, (enrollment_data['course_id'],))
        
        if course_info:
            max_students = course_info[0]['max_students']
            current_students = course_info[0]['current_students']
            if current_students >= max_students:
                print("课程已满")
                return False
                
        # 开始事务处理
        try:
            # 插入选课记录
            insert_query = """
                INSERT INTO enrollments (student_id, course_id, semester, status, enrollment_date)
                VALUES (%s, %s, %s, %s, %s)
            """
            params = (
                enrollment_data['student_id'],
                enrollment_data['course_id'],
                enrollment_data['semester'],
                enrollment_data.get('status', '正常'),
                enrollment_data.get('enrollment_date', date.today())
            )
            
            self.db.execute_update(insert_query, params)
            
            # 更新课程选课人数
            update_query = """
                UPDATE courses 
                SET current_students = current_students + 1
                WHERE course_id = %s
            """
            self.db.execute_update(update_query, (enrollment_data['course_id'],))
            
            return True
            
        except Exception as e:
            print(f"选课失败: {e}")
            return False
            
    def drop_course(self, student_id: str, course_id: str, semester: str) -> bool:
        """
        退选课程
        
        Args:
            student_id: 学号
            course_id: 课程编号
            semester: 学期
            
        Returns:
            是否退选成功
        """
        try:
            # 更新选课状态为退选
            update_query = """
                UPDATE enrollments 
                SET status = '退选'
                WHERE student_id = %s AND course_id = %s AND semester = %s 
                      AND status = '正常'
            """
            rows_affected = self.db.execute_update(
                update_query, (student_id, course_id, semester)
            )
            
            if rows_affected > 0:
                # 更新课程选课人数
                course_update_query = """
                    UPDATE courses 
                    SET current_students = current_students - 1
                    WHERE course_id = %s AND current_students > 0
                """
                self.db.execute_update(course_update_query, (course_id,))
                
            return rows_affected > 0
            
        except Exception as e:
            print(f"退选失败: {e}")
            return False
            
    def update_score(self, enrollment_id: int, score: float) -> bool:
        """
        更新成绩
        
        Args:
            enrollment_id: 选课记录ID
            score: 成绩
            
        Returns:
            是否更新成功
        """
        # 计算等级
        grade = self._calculate_grade(score)
        
        query = """
            UPDATE enrollments 
            SET score = %s, grade = %s
            WHERE enrollment_id = %s
        """
        
        try:
            rows_affected = self.db.execute_update(query, (score, grade, enrollment_id))
            return rows_affected > 0
        except Exception as e:
            print(f"更新成绩失败: {e}")
            return False
            
    def _calculate_grade(self, score: float) -> str:
        """
        根据分数计算等级
        
        Args:
            score: 分数
            
        Returns:
            等级
        """
        if score >= 90:
            return '优秀'
        elif score >= 80:
            return '良好'
        elif score >= 70:
            return '中等'
        elif score >= 60:
            return '及格'
        else:
            return '不及格'
            
    def get_student_courses(self, student_id: str, semester: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        获取学生选课信息
        
        Args:
            student_id: 学号
            semester: 学期（可选）
            
        Returns:
            选课信息列表
        """
        query = """
            SELECT e.*, c.course_name, c.credits, c.teacher, c.classroom, c.schedule,
                   s.name as student_name
            FROM enrollments e
            JOIN courses c ON e.course_id = c.course_id
            JOIN students s ON e.student_id = s.student_id
            WHERE e.student_id = %s
        """
        
        params = [student_id]
        if semester:
            query += " AND e.semester = %s"
            params.append(semester)
            
        query += " ORDER BY e.semester DESC, c.course_id"
        
        return self.db.execute_query(query, tuple(params))
        
    def get_course_students(self, course_id: str, semester: str) -> List[Dict[str, Any]]:
        """
        获取课程选课学生列表
        
        Args:
            course_id: 课程编号
            semester: 学期
            
        Returns:
            选课学生列表
        """
        query = """
            SELECT e.*, s.name, s.major, s.class_name
            FROM enrollments e
            JOIN students s ON e.student_id = s.student_id
            WHERE e.course_id = %s AND e.semester = %s AND e.status = '正常'
            ORDER BY s.student_id
        """
        
        return self.db.execute_query(query, (course_id, semester))
        
    def get_transcript(self, student_id: str) -> List[Dict[str, Any]]:
        """
        获取学生成绩单
        
        Args:
            student_id: 学号
            
        Returns:
            成绩单列表
        """
        query = """
            SELECT e.semester, e.course_id, c.course_name, c.credits, 
                   c.course_type, e.score, e.grade, e.status
            FROM enrollments e
            JOIN courses c ON e.course_id = c.course_id
            WHERE e.student_id = %s AND e.score IS NOT NULL
            ORDER BY e.semester DESC, c.course_id
        """
        
        return self.db.execute_query(query, (student_id,))
        
    def calculate_gpa(self, student_id: str) -> Dict[str, Any]:
        """
        计算学生GPA
        
        Args:
            student_id: 学号
            
        Returns:
            GPA信息字典
        """
        query = """
            SELECT c.credits, e.score
            FROM enrollments e
            JOIN courses c ON e.course_id = c.course_id
            WHERE e.student_id = %s AND e.score IS NOT NULL AND e.status = '正常'
        """
        
        results = self.db.execute_query(query, (student_id,))
        
        if not results:
            return {'gpa': 0.0, 'total_credits': 0, 'total_points': 0.0}
            
        total_credits = 0
        total_points = 0
        
        for record in results:
            credits = float(record['credits'])
            score = float(record['score'])
            
            # 计算绩点（4.0制）
            if score >= 90:
                grade_point = 4.0
            elif score >= 85:
                grade_point = 3.7
            elif score >= 82:
                grade_point = 3.3
            elif score >= 78:
                grade_point = 3.0
            elif score >= 75:
                grade_point = 2.7
            elif score >= 72:
                grade_point = 2.3
            elif score >= 68:
                grade_point = 2.0
            elif score >= 64:
                grade_point = 1.5
            elif score >= 60:
                grade_point = 1.0
            else:
                grade_point = 0.0
                
            total_credits += credits
            total_points += credits * grade_point
            
        gpa = total_points / total_credits if total_credits > 0 else 0.0
        
        return {
            'gpa': round(gpa, 2),
            'total_credits': total_credits,
            'total_points': round(total_points, 2)
        }
        
    def get_statistics(self) -> Dict[str, Any]:
        """
        获取选课统计信息
        
        Returns:
            统计信息字典
        """
        stats = {}
        
        # 总选课记录数
        query = "SELECT COUNT(*) as total FROM enrollments"
        result = self.db.execute_query(query)
        stats['total_enrollments'] = result[0]['total'] if result else 0
        
        # 按学期统计
        query = """
            SELECT semester, COUNT(*) as count 
            FROM enrollments 
            WHERE status = '正常'
            GROUP BY semester 
            ORDER BY semester DESC
        """
        stats['by_semester'] = self.db.execute_query(query)
        
        # 成绩分布
        query = """
            SELECT grade, COUNT(*) as count 
            FROM enrollments 
            WHERE grade IS NOT NULL
            GROUP BY grade
            ORDER BY 
                CASE grade 
                    WHEN '优秀' THEN 1 
                    WHEN '良好' THEN 2 
                    WHEN '中等' THEN 3 
                    WHEN '及格' THEN 4 
                    WHEN '不及格' THEN 5 
                END
        """
        stats['grade_distribution'] = self.db.execute_query(query)
        
        # 平均分统计
        query = """
            SELECT 
                AVG(score) as avg_score,
                MAX(score) as max_score,
                MIN(score) as min_score,
                STDDEV(score) as std_dev
            FROM enrollments
            WHERE score IS NOT NULL
        """
        result = self.db.execute_query(query)
        stats['score_stats'] = result[0] if result else {}
        
        return stats

