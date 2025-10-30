"""
远程客户端程序
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.db_config import DBConfig
from utils.db_connection import DatabaseConnection
from models.student import Student
from models.course import Course
from models.enrollment import Enrollment
from tabulate import tabulate
from colorama import init, Fore, Style
import getpass

# 初始化colorama
init(autoreset=True)

class RemoteClient:
    """远程客户端类"""
    
    def __init__(self):
        """初始化客户端"""
        self.db_connection = None
        self.student_model = None
        self.course_model = None
        self.enrollment_model = None
        
    def connect_database(self):
        """连接远程数据库"""
        print(Fore.CYAN + "\n=== 连接远程数据库 ===")
        
        # 获取远程数据库配置
        print("请输入远程数据库连接信息:")
        config = {
            'host': input("数据库主机IP: ").strip(),
            'port': int(input("端口 [2881]: ").strip() or '2881'),
            'user': input("用户名: ").strip(),
            'password': getpass.getpass("密码: ").strip(),
            'database': input("数据库名 [student_management]: ").strip() or 'student_management',
            'charset': 'utf8mb4'
        }
        
        try:
            self.db_connection = DatabaseConnection(config)
            if self.db_connection.test_connection():
                print(Fore.GREEN + "✓ 远程数据库连接成功!")
                print(f"已连接到: {config['host']}:{config['port']}")
                
                self.student_model = Student(self.db_connection)
                self.course_model = Course(self.db_connection)
                self.enrollment_model = Enrollment(self.db_connection)
                return True
            else:
                print(Fore.RED + "✗ 远程数据库连接失败!")
                return False
        except Exception as e:
            print(Fore.RED + f"✗ 连接错误: {e}")
            return False
            
    def show_menu(self):
        """显示主菜单"""
        menu = """
        ╔════════════════════════════════════╗
        ║     学生管理系统 - 远程客户端      ║
        ╠════════════════════════════════════╣
        ║  1. 查询学生信息                   ║
        ║  2. 查询课程信息                   ║
        ║  3. 查询选课信息                   ║
        ║  4. 学生选课操作                   ║
        ║  5. 成绩查询                       ║
        ║  6. 数据统计                       ║
        ║  7. 连接信息                       ║
        ║  0. 退出系统                       ║
        ╚════════════════════════════════════╝
        """
        print(Fore.YELLOW + menu)
        
    def query_students(self):
        """查询学生信息"""
        print(Fore.CYAN + "\n=== 查询学生信息 ===")
        print("1. 按学号查询")
        print("2. 按姓名查询")
        print("3. 按专业查询")
        print("4. 查看所有学生")
        
        choice = input("\n请选择: ").strip()
        
        if choice == '1':
            student_id = input("请输入学号: ").strip()
            student = self.student_model.get_by_id(student_id)
            if student:
                print(Fore.GREEN + "\n查询结果:")
                for key, value in student.items():
                    if key not in ['created_at', 'updated_at']:
                        print(f"  {key}: {value}")
            else:
                print(Fore.YELLOW + "未找到该学生")
                
        elif choice == '2':
            name = input("请输入姓名关键字: ").strip()
            students = self.student_model.search(name=name)
            self._display_students(students)
            
        elif choice == '3':
            major = input("请输入专业关键字: ").strip()
            students = self.student_model.search(major=major)
            self._display_students(students)
            
        elif choice == '4':
            students = self.student_model.get_all(limit=50)
            self._display_students(students)
            
    def _display_students(self, students):
        """显示学生列表"""
        if students:
            headers = ['学号', '姓名', '性别', '年龄', '专业', '班级', '状态']
            data = []
            for s in students:
                data.append([
                    s['student_id'], s['name'], s['gender'],
                    s.get('age', '-'), s['major'], 
                    s.get('class_name', '-'), s['status']
                ])
            print(tabulate(data, headers=headers, tablefmt='grid'))
            print(f"\n共找到 {len(students)} 条记录")
        else:
            print(Fore.YELLOW + "未找到符合条件的学生")
            
    def query_courses(self):
        """查询课程信息"""
        print(Fore.CYAN + "\n=== 查询课程信息 ===")
        print("1. 按课程编号查询")
        print("2. 按课程名称查询")
        print("3. 按教师查询")
        print("4. 查看当前学期课程")
        print("5. 查看所有课程")
        
        choice = input("\n请选择: ").strip()
        
        if choice == '1':
            course_id = input("请输入课程编号: ").strip()
            course = self.course_model.get_by_id(course_id)
            if course:
                print(Fore.GREEN + "\n查询结果:")
                for key, value in course.items():
                    if key not in ['created_at', 'updated_at']:
                        print(f"  {key}: {value}")
            else:
                print(Fore.YELLOW + "未找到该课程")
                
        elif choice == '2':
            name = input("请输入课程名称关键字: ").strip()
            courses = self.course_model.search(course_name=name)
            self._display_courses(courses)
            
        elif choice == '3':
            teacher = input("请输入教师姓名: ").strip()
            courses = self.course_model.search(teacher=teacher)
            self._display_courses(courses)
            
        elif choice == '4':
            semester = input("请输入学期 (如2024-1): ").strip()
            courses = self.course_model.get_available_courses(semester)
            self._display_courses(courses)
            
        elif choice == '5':
            courses = self.course_model.get_all(limit=50)
            self._display_courses(courses)
            
    def _display_courses(self, courses):
        """显示课程列表"""
        if courses:
            headers = ['课程编号', '课程名称', '学分', '教师', '类型', '选课情况']
            data = []
            for c in courses:
                data.append([
                    c['course_id'], c['course_name'], c['credits'],
                    c.get('teacher', '-'), c['course_type'],
                    f"{c.get('current_students', 0)}/{c.get('max_students', 100)}"
                ])
            print(tabulate(data, headers=headers, tablefmt='grid'))
            print(f"\n共找到 {len(courses)} 条记录")
        else:
            print(Fore.YELLOW + "未找到符合条件的课程")
            
    def query_enrollments(self):
        """查询选课信息"""
        print(Fore.CYAN + "\n=== 查询选课信息 ===")
        print("1. 查询学生选课")
        print("2. 查询课程选课名单")
        
        choice = input("\n请选择: ").strip()
        
        if choice == '1':
            student_id = input("请输入学号: ").strip()
            semester = input("学期（可选，直接回车查询所有）: ").strip()
            
            courses = self.enrollment_model.get_student_courses(
                student_id,
                semester if semester else None
            )
            
            if courses:
                headers = ['学期', '课程编号', '课程名称', '学分', '成绩', '等级']
                data = []
                for c in courses:
                    data.append([
                        c['semester'], c['course_id'], c['course_name'],
                        c['credits'], c.get('score', '-'), c.get('grade', '-')
                    ])
                print(tabulate(data, headers=headers, tablefmt='grid'))
            else:
                print(Fore.YELLOW + "未找到选课记录")
                
        elif choice == '2':
            course_id = input("请输入课程编号: ").strip()
            semester = input("学期: ").strip()
            
            students = self.enrollment_model.get_course_students(course_id, semester)
            
            if students:
                headers = ['学号', '姓名', '专业', '班级', '成绩', '等级']
                data = []
                for s in students:
                    data.append([
                        s['student_id'], s['name'], s['major'],
                        s['class_name'], s.get('score', '-'), s.get('grade', '-')
                    ])
                print(tabulate(data, headers=headers, tablefmt='grid'))
                print(f"\n选课人数: {len(students)}")
            else:
                print(Fore.YELLOW + "未找到选课学生")
                
    def enrollment_operations(self):
        """学生选课操作"""
        print(Fore.CYAN + "\n=== 学生选课操作 ===")
        print("1. 选课")
        print("2. 退选")
        
        choice = input("\n请选择: ").strip()
        
        if choice == '1':
            print("\n请输入选课信息:")
            enrollment_data = {
                'student_id': input("学号: ").strip(),
                'course_id': input("课程编号: ").strip(),
                'semester': input("学期: ").strip()
            }
            
            if self.enrollment_model.enroll(enrollment_data):
                print(Fore.GREEN + "✓ 选课成功!")
            else:
                print(Fore.RED + "✗ 选课失败! 可能已选该课程或课程已满")
                
        elif choice == '2':
            student_id = input("学号: ").strip()
            course_id = input("课程编号: ").strip()
            semester = input("学期: ").strip()
            
            confirm = input("确认退选? (y/n): ").strip().lower()
            if confirm == 'y':
                if self.enrollment_model.drop_course(student_id, course_id, semester):
                    print(Fore.GREEN + "✓ 退选成功!")
                else:
                    print(Fore.RED + "✗ 退选失败!")
                    
    def query_grades(self):
        """成绩查询"""
        print(Fore.CYAN + "\n=== 成绩查询 ===")
        student_id = input("请输入学号: ").strip()
        
        # 获取成绩单
        transcript = self.enrollment_model.get_transcript(student_id)
        
        if transcript:
            print(Fore.CYAN + f"\n{'='*70}")
            print(f"学生成绩单 - 学号: {student_id}")
            print('='*70)
            
            headers = ['学期', '课程编号', '课程名称', '学分', '类型', '成绩', '等级']
            data = []
            total_credits = 0
            total_score = 0
            
            for t in transcript:
                data.append([
                    t['semester'], t['course_id'], t['course_name'],
                    t['credits'], t['course_type'], 
                    t.get('score', '-'), t.get('grade', '-')
                ])
                
                if t.get('score'):
                    total_credits += float(t['credits'])
                    total_score += float(t['score']) * float(t['credits'])
                    
            print(tabulate(data, headers=headers, tablefmt='grid'))
            
            # 计算平均分和GPA
            if total_credits > 0:
                avg_score = total_score / total_credits
                gpa_info = self.enrollment_model.calculate_gpa(student_id)
                
                print(f"\n总学分: {total_credits}")
                print(f"加权平均分: {avg_score:.2f}")
                print(f"GPA: {gpa_info['gpa']}")
        else:
            print(Fore.YELLOW + "暂无成绩记录")
            
    def show_statistics(self):
        """数据统计"""
        print(Fore.CYAN + "\n=== 数据统计 ===")
        print("1. 学生统计")
        print("2. 课程统计")
        print("3. 选课统计")
        
        choice = input("\n请选择: ").strip()
        
        if choice == '1':
            stats = self.student_model.get_statistics()
            print(Fore.CYAN + "\n学生统计信息:")
            print(f"总学生数: {stats['total_students']}")
            
            if stats['by_major']:
                print("\n各专业人数:")
                headers = ['专业', '人数']
                data = [[s['major'], s['count']] for s in stats['by_major'][:10]]
                print(tabulate(data, headers=headers, tablefmt='grid'))
                
        elif choice == '2':
            stats = self.course_model.get_statistics()
            print(Fore.CYAN + "\n课程统计信息:")
            print(f"总课程数: {stats['total_courses']}")
            
            if stats['by_type']:
                print("\n各类型课程数:")
                headers = ['类型', '数量']
                data = [[s['course_type'], s['count']] for s in stats['by_type']]
                print(tabulate(data, headers=headers, tablefmt='grid'))
                
        elif choice == '3':
            stats = self.enrollment_model.get_statistics()
            print(Fore.CYAN + "\n选课统计信息:")
            print(f"总选课记录: {stats['total_enrollments']}")
            
            if stats['grade_distribution']:
                print("\n成绩分布:")
                headers = ['等级', '人数']
                data = [[g['grade'], g['count']] for g in stats['grade_distribution']]
                print(tabulate(data, headers=headers, tablefmt='grid'))
                
    def show_connection_info(self):
        """显示连接信息"""
        if self.db_connection and self.db_connection.test_connection():
            config = self.db_connection.config
            print(Fore.CYAN + "\n=== 远程数据库连接信息 ===")
            print(f"远程主机: {config['host']}")
            print(f"端口: {config['port']}")
            print(f"用户: {config['user']}")
            print(f"数据库: {config['database']}")
            print(f"连接状态: " + Fore.GREEN + "已连接")
            
            # 测试延迟
            import time
            start = time.time()
            self.db_connection.test_connection()
            latency = (time.time() - start) * 1000
            print(f"网络延迟: {latency:.2f} ms")
        else:
            print(Fore.RED + "远程数据库未连接")
            
    def run(self):
        """运行远程客户端"""
        print(Fore.CYAN + "="*50)
        print("欢迎使用学生管理系统 - 远程客户端")
        print("="*50)
        
        # 连接远程数据库
        if not self.connect_database():
            print(Fore.RED + "无法连接远程数据库，程序退出")
            return
            
        # 主循环
        while True:
            self.show_menu()
            choice = input("请选择功能: ").strip()
            
            if choice == '1':
                self.query_students()
            elif choice == '2':
                self.query_courses()
            elif choice == '3':
                self.query_enrollments()
            elif choice == '4':
                self.enrollment_operations()
            elif choice == '5':
                self.query_grades()
            elif choice == '6':
                self.show_statistics()
            elif choice == '7':
                self.show_connection_info()
            elif choice == '0':
                print(Fore.YELLOW + "\n感谢使用，再见!")
                break
            else:
                print(Fore.RED + "无效的选择，请重新输入")
                
        # 断开数据库连接
        if self.db_connection:
            self.db_connection.disconnect()

if __name__ == "__main__":
    client = RemoteClient()
    client.run()
