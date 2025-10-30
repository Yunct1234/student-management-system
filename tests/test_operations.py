"""
功能测试模块
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from datetime import date, datetime
from config.db_config import DBConfig
from utils.db_connection import DatabaseConnection
from models.student import Student
from models.course import Course
from models.enrollment import Enrollment

class TestDatabaseOperations(unittest.TestCase):
    """数据库操作测试类"""
    
    @classmethod
    def setUpClass(cls):
        """设置测试环境"""
        print("\n初始化测试环境...")
        config = DBConfig.get_local_config()
        cls.db_connection = DatabaseConnection(config)
        cls.student_model = Student(cls.db_connection)
        cls.course_model = Course(cls.db_connection)
        cls.enrollment_model = Enrollment(cls.db_connection)
        
    @classmethod
    def tearDownClass(cls):
        """清理测试环境"""
        print("\n清理测试环境...")
        if cls.db_connection:
            cls.db_connection.disconnect()
            
    def test_01_database_connection(self):
        """测试数据库连接"""
        print("\n测试数据库连接...")
        self.assertTrue(self.db_connection.test_connection())
        print("✓ 数据库连接成功")
        
    def test_02_student_operations(self):
        """测试学生信息操作"""
        print("\n测试学生信息操作...")
        
        # 创建测试学生
        test_student = {
            'student_id': 'TEST001',
            'name': '测试学生',
            'gender': '男',
            'age': 20,
            'major': '计算机科学与技术',
            'class_name': '测试班',
            'phone': '13800000000',
            'email': 'test@test.com',
            'enrollment_date': date(2024, 9, 1),
            'status': '在读'
        }
        
        # 测试创建
        result = self.student_model.create(test_student)
        self.assertTrue(result)
        print("  ✓ 创建学生成功")
        
        # 测试查询
        student = self.student_model.get_by_id('TEST001')
        self.assertIsNotNone(student)
        self.assertEqual(student['name'], '测试学生')
        print("  ✓ 查询学生成功")
        
        # 测试更新
        update_data = {'phone': '13900000000', 'email': 'new@test.com'}
        result = self.student_model.update('TEST001', update_data)
        self.assertTrue(result)
        
        updated_student = self.student_model.get_by_id('TEST001')
        self.assertEqual(updated_student['phone'], '13900000000')
        print("  ✓ 更新学生成功")
        
        # 测试搜索
        students = self.student_model.search(major='计算机')
        self.assertIsInstance(students, list)
        print("  ✓ 搜索学生成功")
        
        # 测试删除
        result = self.student_model.delete('TEST001')
        self.assertTrue(result)
        print("  ✓ 删除学生成功")
        
    def test_03_course_operations(self):
        """测试课程信息操作"""
        print("\n测试课程信息操作...")
        
        # 创建测试课程
        test_course = {
            'course_id': 'TEST101',
            'course_name': '测试课程',
            'credits': 3.0,
            'teacher': '测试教师',
            'department': '计算机学院',
            'semester': '2024-1',
            'course_type': '选修',
            'max_students': 50,
            'classroom': '测试教室',
            'schedule': '周一1-2节'
        }
        
        # 测试创建
        result = self.course_model.create(test_course)
        self.assertTrue(result)
        print("  ✓ 创建课程成功")
        
        # 测试查询
        course = self.course_model.get_by_id('TEST101')
        self.assertIsNotNone(course)
        self.assertEqual(course['course_name'], '测试课程')
        print("  ✓ 查询课程成功")
        
        # 测试更新
        update_data = {'max_students': 60, 'classroom': '新教室'}
        result = self.course_model.update('TEST101', update_data)
        self.assertTrue(result)
        print("  ✓ 更新课程成功")
        
        # 测试获取可选课程
        available = self.course_model.get_available_courses('2024-1')
        self.assertIsInstance(available, list)
        print("  ✓ 获取可选课程成功")
        
        # 测试删除
        result = self.course_model.delete('TEST101')
        self.assertTrue(result)
        print("  ✓ 删除课程成功")
        
    def test_04_enrollment_operations(self):
        """测试选课操作"""
        print("\n测试选课操作...")
        
        # 准备测试数据
        test_student = {
            'student_id': 'TEST002',
            'name': '选课测试学生',
            'gender': '女',
            'major': '软件工程',
            'status': '在读'
        }
        
        test_course = {
            'course_id': 'TEST102',
            'course_name': '选课测试课程',
            'credits': 2.0,
            'course_type': '必修',
            'semester': '2024-1',
            'max_students': 30
        }
        
        # 创建测试数据
        self.student_model.create(test_student)
        self.course_model.create(test_course)
        
        # 测试选课
        enrollment_data = {
            'student_id': 'TEST002',
            'course_id': 'TEST102',
            'semester': '2024-1'
        }
        
        result = self.enrollment_model.enroll(enrollment_data)
        self.assertTrue(result)
        print("  ✓ 选课成功")
        
        # 测试查询学生选课
        courses = self.enrollment_model.get_student_courses('TEST002')
        self.assertIsInstance(courses, list)
        self.assertTrue(len(courses) > 0)
        print("  ✓ 查询学生选课成功")
        
        # 测试查询课程选课名单
        students = self.enrollment_model.get_course_students('TEST102', '2024-1')
        self.assertIsInstance(students, list)
        print("  ✓ 查询课程选课名单成功")
        
        # 测试退选
        result = self.enrollment_model.drop_course('TEST002', 'TEST102', '2024-1')
        self.assertTrue(result)
        print("  ✓ 退选成功")
        
        # 清理测试数据
        self.student_model.delete('TEST002')
        self.course_model.delete('TEST102')
        
    def test_05_statistics(self):
        """测试统计功能"""
        print("\n测试统计功能...")
        
        # 测试学生统计
        stats = self.student_model.get_statistics()
        self.assertIsInstance(stats, dict)
        self.assertIn('total_students', stats)
        print("  ✓ 学生统计成功")
        
        # 测试课程统计
        stats = self.course_model.get_statistics()
        self.assertIsInstance(stats, dict)
        self.assertIn('total_courses', stats)
        print("  ✓ 课程统计成功")
        
        # 测试选课统计
        stats = self.enrollment_model.get_statistics()
        self.assertIsInstance(stats, dict)
        self.assertIn('total_enrollments', stats)
        print("  ✓ 选课统计成功")
        
    def test_06_remote_access(self):
        """测试远程访问权限"""
        print("\n测试远程访问...")
        
        # 测试远程连接配置
        remote_config = DBConfig.get_remote_config()
        self.assertIsNotNone(remote_config)
        self.assertIn('host', remote_config)
        self.assertIn('user', remote_config)
        print("  ✓ 远程配置获取成功")
        
        # 注意：实际远程连接测试需要配置好远程数据库
        # 这里只测试配置是否正确
        
    def test_07_transaction_support(self):
        """测试事务支持"""
        print("\n测试事务支持...")
        
        # 创建测试数据
        test_student = {
            'student_id': 'TRANS001',
            'name': '事务测试学生',
            'gender': '男',
            'major': '信息安全',
            'status': '在读'
        }
        
        try:
            # 开始事务
            with self.db_connection.get_cursor() as cursor:
                # 插入学生
                query = """
                    INSERT INTO students (student_id, name, gender, major, status)
                    VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(query, (
                    test_student['student_id'],
                    test_student['name'],
                    test_student['gender'],
                    test_student['major'],
                    test_student['status']
                ))
                
                # 验证插入
                cursor.execute("SELECT * FROM students WHERE student_id = %s", 
                             (test_student['student_id'],))
                result = cursor.fetchone()
                self.assertIsNotNone(result)
                
                # 事务会自动提交（在with块结束时）
                
            print("  ✓ 事务提交成功")
            
            # 清理测试数据
            self.student_model.delete('TRANS001')
            
        except Exception as e:
            print(f"  ✗ 事务测试失败: {e}")
            self.fail("事务测试失败")
            
def run_tests():
    """运行所有测试"""
    # 创建测试套件
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestDatabaseOperations)
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # 返回测试结果
    return result.wasSuccessful()

if __name__ == "__main__":
    success = run_tests()
    if success:
        print("\n" + "="*50)
        print("所有测试通过！")
        print("="*50)
    else:
        print("\n" + "="*50)
        print("测试失败，请检查错误信息")
        print("="*50)
