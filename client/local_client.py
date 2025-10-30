"""
本地客户端程序
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

class LocalClient:
    """本地客户端类"""
    
    def __init__(self):
        """初始化客户端"""
        self.db_connection = None
        self.student_model = None
        self.course_model = None
        self.enrollment_model = None
        
    def connect_database(self):
        """连接数据库"""
        print(Fore.CYAN + "\n=== 连接本地数据库 ===")
        config = DBConfig.get_local_config()
        
        # 允许用户修改连接参数
        host = input(f"数据库主机 [{config['host']}]: ").strip() or config['host']
        port = input(f"端口 [{config['port']}]: ").strip() or config['port']
        user = input(f"用户名 [{config['user']}]: ").strip() or config['user']
        password = getpass.getpass(f"密码: ").strip() or config['password']
        
        config.update({
            'host': host,
            'port': int(port),
            'user': user,
            'password': password
        })
        
        try:
            self.db_connection = DatabaseConnection(config)
            if self.db_connection.test_connection():
                print(Fore.GREEN + "✓ 数据库连接成功!")
                self.student_model = Student(self.db_connection)
                self.course_model = Course(self.db_connection)
                self.enrollment_model = Enrollment(self.db_connection)
                return True
            else:
                print(Fore.RED + "✗ 数据库连接失败!")
                return False
        except Exception as e:
            print(Fore.RED + f"✗ 连接错误: {e}")
            return False
            
    def show_menu(self):
        """显示主菜单"""
        menu = """
        ╔════════════════════════════════════╗
        ║     学生管理系统 - 本地客户端      ║
        ╠════════════════════════════════════╣
        ║  1. 学生信息管理                   ║
        ║  2. 课程信息管理                   ║
        ║  3. 选课管理                       ║
        ║  4. 成绩管理                       ║
        ║  5. 统计查询                       ║
        ║  6. 数据库连接信息                 ║
        ║  0. 退出系统                       ║
        ╚════════════════════════════════════╝
        """
        print(Fore.YELLOW + menu)
        
    def student_management(self):
        """学生信息管理"""
        while True:
            print(Fore.CYAN + "\n=== 学生信息管理 ===")
            print("1. 查看所有学生")
            print("2. 查询学生")
            print("3. 添加学生")
            print("4. 修改学生信息")
            print("5. 删除学生")
            print("0. 返回上级菜单")
            
            choice = input("\n请选择操作: ").strip()
            
            if choice == '1':
                self.view_all_students()
            elif choice == '2':
                self.search_student()
            elif choice == '3':
                self.add_student()
            elif choice == '4':
                self.update_student()
            elif choice == '5':
                self.delete_student()
            elif choice == '0':
                break
                
    def view_all_students(self):
        """查看所有学生"""
        students = self.student_model.get_all()
        if students:
            headers = ['学号', '姓名', '性别', '年龄', '专业', '班级', '状态']
            data = []
            for s in students:
                data.append([
                    s['student_id'], s['name'], s['gender'], 
                    s['age'], s['major'], s['class_name'], s['status']
                ])
            print(tabulate(data, headers=headers, tablefmt='grid'))
        else:
            print(Fore.YELLOW + "暂无学生数据")
            
    def search_student(self):
        """查询学生"""
        student_id = input("请输入学号（直接回车查询所有）: ").strip()
        if student_id:
            student = self.student_model.get_by_id(student_id)
            if student:
                print(Fore.GREEN + "\n学生信息:")
                for key, value in student.items():
                    if key not in ['created_at', 'updated_at']:
                        print(f"  {key}: {value}")
            else:
                print(Fore.RED + "未找到该学生")
        else:
            name = input("请输入姓名关键字: ").strip()
            major = input("请输入专业关键字: ").strip()
            students = self.student_model.search(name=name if name else None, 
                                                major=major if major else None)
            if students:
                headers = ['学号', '姓名', '性别', '专业', '班级']
                data = [[s['student_id'], s['name'], s['gender'], 
                        s['major'], s['class_name']] for s in students]
                print(tabulate(data, headers=headers, tablefmt='grid'))
            else:
                print(Fore.YELLOW + "未找到符合条件的学生")
                
    def add_student(self):
        """添加学生"""
        print(Fore.CYAN + "\n添加新学生:")
        student_data = {
            'student_id': input("学号: ").strip(),
            'name': input("姓名: ").strip(),
            'gender': input("性别(男/女): ").strip(),
            'age': int(input("年龄: ").strip()),
            'major': input("专业: ").strip(),
            'class_name': input("班级: ").strip(),
            'phone': input("电话: ").strip(),
            'email': input("邮箱: ").strip()
        }
        
        if self.student_model.create(student_data):
            print(Fore.GREEN + "✓ 学生添加成功!")
        else:
            print(Fore.RED + "✗ 学生添加失败!")
            
    def update_student(self):
        """修改学生信息"""
        student_id = input("请输入要修改的学生学号: ").strip()
        student = self.student_model.get_by_id(student_id)
        
        if not student:
            print(Fore.RED + "未找到该学生")
            return
            
        print(Fore.CYAN + "\n当前学生信息:")
        for key, value in student.items():
            if key not in ['created_at', 'updated_at', 'student_id']:
                print(f"  {key}: {value}")
                
        print("\n请输入要修改的信息（直接回车跳过）:")
        update_data = {}
        
        fields = ['name', 'gender', 'age', 'major', 'class_name', 'phone', 'email', 'status']
        for field in fields:
            value = input(f"{field}: ").strip()
            if value:
                if field == 'age':
                    update_data[field] = int(value)
                else:
                    update_data[field] = value
                    
        if update_data:
            if self.student_model.update(student_id, update_data):
                print(Fore.GREEN + "✓ 学生信息更新成功!")
            else:
                print(Fore.RED + "✗ 学生信息更新失败!")
        else:
            print(Fore.YELLOW + "未进行任何修改")
            
    def delete_student(self):
        """删除学生"""
        student_id = input("请输入要删除的学生学号: ").strip()
        confirm = input(f"确认删除学生 {student_id}? (y/n): ").strip().lower()
        
        if confirm == 'y':
            if self.student_model.delete(student_id):
                print(Fore.GREEN + "✓ 学生删除成功!")
            else:
                print(Fore.RED + "✗ 学生删除失败!")
                
    def course_management(self):
        """课程信息管理"""
        while True:
            print(Fore.CYAN + "\n=== 课程信息管理 ===")
            print("1. 查看所有课程")
            print("2. 查询课程")
            print("3. 添加课程")
            print("4. 修改课程信息")
            print("5. 删除课程")
            print("0. 返回上级菜单")
            
            choice = input("\n请选择操作: ").strip()
            
            if choice == '1':
                self.view_all_courses()
            elif choice == '2':
                self.search_course()
            elif choice == '3':
                self.add_course()
            elif choice == '4':
                self.update_course()
            elif choice == '5':
                self.delete_course()
            elif choice == '0':
                break
                
    def view_all_courses(self):
        """查看所有课程"""
        courses = self.course_model.get_all()
        if courses:
            headers = ['课程编号', '课程名称', '学分', '教师', '类型', '学期', '选课/容量']
            data = []
            for c in courses:
                data.append([
                    c['course_id'], c['course_name'], c['credits'], 
                    c['teacher'], c['course_type'], c['semester'],
                    f"{c['current_students']}/{c['max_students']}"
                ])
            print(tabulate(data, headers=headers, tablefmt='grid'))
        else:
            print(Fore.YELLOW + "暂无课程数据")
            
    def search_course(self):
        """查询课程"""
        course_id = input("请输入课程编号（直接回车按其他条件查询）: ").strip()
        if course_id:
            course = self.course_model.get_by_id(course_id)
            if course:
                print(Fore.GREEN + "\n课程信息:")
                for key, value in course.items():
                    if key not in ['created_at', 'updated_at']:
                        print(f"  {key}: {value}")
            else:
                print(Fore.RED + "未找到该课程")
        else:
            name = input("课程名称关键字: ").strip()
            teacher = input("教师姓名: ").strip()
            courses = self.course_model.search(
                course_name=name if name else None,
                teacher=teacher if teacher else None
            )
            if courses:
                headers = ['课程编号', '课程名称', '学分', '教师', '类型']
                data = [[c['course_id'], c['course_name'], c['credits'], 
                        c['teacher'], c['course_type']] for c in courses]
                print(tabulate(data, headers=headers, tablefmt='grid'))
            else:
                print(Fore.YELLOW + "未找到符合条件的课程")
                
    def add_course(self):
        """添加课程"""
        print(Fore.CYAN + "\n添加新课程:")
        course_data = {
            'course_id': input("课程编号: ").strip(),
            'course_name': input("课程名称: ").strip(),
            'credits': float(input("学分: ").strip()),
            'teacher': input("授课教师: ").strip(),
            'department': input("开课学院: ").strip(),
            'semester': input("学期: ").strip(),
            'course_type': input("课程类型(必修/选修/实践): ").strip(),
            'max_students': int(input("最大选课人数: ").strip()),
            'classroom': input("上课地点: ").strip(),
            'schedule': input("上课时间: ").strip()
        }
        
        if self.course_model.create(course_data):
            print(Fore.GREEN + "✓ 课程添加成功!")
        else:
            print(Fore.RED + "✗ 课程添加失败!")
            
    def update_course(self):
        """修改课程信息"""
        course_id = input("请输入要修改的课程编号: ").strip()
        course = self.course_model.get_by_id(course_id)
        
        if not course:
            print(Fore.RED + "未找到该课程")
            return
            
        print(Fore.CYAN + "\n当前课程信息:")
        for key, value in course.items():
            if key not in ['created_at', 'updated_at', 'course_id']:
                print(f"  {key}: {value}")
                
        print("\n请输入要修改的信息（直接回车跳过）:")
        update_data = {}
        
        fields = ['course_name', 'credits', 'teacher', 'classroom', 'schedule', 'max_students']
        for field in fields:
            value = input(f"{field}: ").strip()
            if value:
                if field == 'credits':
                    update_data[field] = float(value)
                elif field == 'max_students':
                    update_data[field] = int(value)
                else:
                    update_data[field] = value
                    
        if update_data:
            if self.course_model.update(course_id, update_data):
                print(Fore.GREEN + "✓ 课程信息更新成功!")
            else:
                print(Fore.RED + "✗ 课程信息更新失败!")
        else:
            print(Fore.YELLOW + "未进行任何修改")
            
    def delete_course(self):
        """删除课程"""
        course_id = input("请输入要删除的课程编号: ").strip()
        confirm = input(f"确认删除课程 {course_id}? (y/n): ").strip().lower()
        
        if confirm == 'y':
            if self.course_model.delete(course_id):
                print(Fore.GREEN + "✓ 课程删除成功!")
            else:
                print(Fore.RED + "✗ 课程删除失败!")
                
    def enrollment_management(self):
        """选课管理"""
        while True:
            print(Fore.CYAN + "\n=== 选课管理 ===")
            print("1. 学生选课")
            print("2. 退选课程")
            print("3. 查看学生选课")
            print("4. 查看课程选课名单")
            print("0. 返回上级菜单")
            
            choice = input("\n请选择操作: ").strip()
            
            if choice == '1':
                self.enroll_course()
            elif choice == '2':
                self.drop_course()
            elif choice == '3':
                self.view_student_courses()
            elif choice == '4':
                self.view_course_students()
            elif choice == '0':
                break
                
    def enroll_course(self):
        """学生选课"""
        print(Fore.CYAN + "\n学生选课:")
        enrollment_data = {
            'student_id': input("学号: ").strip(),
            'course_id': input("课程编号: ").strip(),
            'semester': input("学期: ").strip()
        }
        
        if self.enrollment_model.enroll(enrollment_data):
            print(Fore.GREEN + "✓ 选课成功!")
        else:
            print(Fore.RED + "✗ 选课失败!")
            
    def drop_course(self):
        """退选课程"""
        student_id = input("学号: ").strip()
        course_id = input("课程编号: ").strip()
        semester = input("学期: ").strip()
        
        confirm = input(f"确认退选? (y/n): ").strip().lower()
        if confirm == 'y':
            if self.enrollment_model.drop_course(student_id, course_id, semester):
                print(Fore.GREEN + "✓ 退选成功!")
            else:
                print(Fore.RED + "✗ 退选失败!")
                
    def view_student_courses(self):
        """查看学生选课"""
        student_id = input("请输入学号: ").strip()
        semester = input("学期（直接回车查看所有）: ").strip()
        
        courses = self.enrollment_model.get_student_courses(
            student_id, 
            semester if semester else None
        )
        
        if courses:
            headers = ['课程编号', '课程名称', '学分', '教师', '成绩', '等级', '状态']
            data = []
            for c in courses:
                data.append([
                    c['course_id'], c['course_name'], c['credits'],
                    c['teacher'], c.get('score', '-'), 
                    c.get('grade', '-'), c['status']
                ])
            print(tabulate(data, headers=headers, tablefmt='grid'))
        else:
            print(Fore.YELLOW + "该学生暂无选课记录")
            
    def view_course_students(self):
        """查看课程选课名单"""
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
        else:
            print(Fore.YELLOW + "该课程暂无选课学生")
            
    def grade_management(self):
        """成绩管理"""
        while True:
            print(Fore.CYAN + "\n=== 成绩管理 ===")
            print("1. 录入成绩")
            print("2. 查看成绩单")
            print("3. 计算GPA")
            print("0. 返回上级菜单")
            
            choice = input("\n请选择操作: ").strip()
            
            if choice == '1':
                self.input_grade()
            elif choice == '2':
                self.view_transcript()
            elif choice == '3':
                self.calculate_gpa()
            elif choice == '0':
                break
                
    def input_grade(self):
        """录入成绩"""
        student_id = input("学号: ").strip()
        course_id = input("课程编号: ").strip()
        semester = input("学期: ").strip()
        
        # 获取选课记录
        query = """
            SELECT enrollment_id FROM enrollments 
            WHERE student_id = %s AND course_id = %s AND semester = %s
        """
        result = self.db_connection.execute_query(query, (student_id, course_id, semester))
        
        if result:
            enrollment_id = result[0]['enrollment_id']
            score = float(input("成绩(0-100): ").strip())
            
            if 0 <= score <= 100:
                if self.enrollment_model.update_score(enrollment_id, score):
                    print(Fore.GREEN + "✓ 成绩录入成功!")
                else:
                    print(Fore.RED + "✗ 成绩录入失败!")
            else:
                print(Fore.RED + "成绩必须在0-100之间!")
        else:
            print(Fore.RED + "未找到该选课记录!")
            
    def view_transcript(self):
        """查看成绩单"""
        student_id = input("请输入学号: ").strip()
        transcript = self.enrollment_model.get_transcript(student_id)
        
        if transcript:
            print(Fore.CYAN + f"\n{'='*60}")
            print(f"学生成绩单 - 学号: {student_id}")
            print('='*60)
            
            headers = ['学期', '课程编号', '课程名称', '学分', '类型', '成绩', '等级']
            data = []
            for t in transcript:
                data.append([
                    t['semester'], t['course_id'], t['course_name'],
                    t['credits'], t['course_type'], t['score'], t['grade']
                ])
            print(tabulate(data, headers=headers, tablefmt='grid'))
        else:
            print(Fore.YELLOW + "暂无成绩记录")
            
    def calculate_gpa(self):
        """计算GPA"""
        student_id = input("请输入学号: ").strip()
        gpa_info = self.enrollment_model.calculate_gpa(student_id)
        
        print(Fore.CYAN + f"\n{'='*40}")
        print(f"GPA计算结果 - 学号: {student_id}")
        print('='*40)
        print(f"总学分: {gpa_info['total_credits']}")
        print(f"总绩点: {gpa_info['total_points']}")
        print(f"GPA: {gpa_info['gpa']}")
        print('='*40)
        
    def statistics_query(self):
        """统计查询"""
        while True:
            print(Fore.CYAN + "\n=== 统计查询 ===")
            print("1. 学生统计")
            print("2. 课程统计")
            print("3. 选课统计")
            print("0. 返回上级菜单")
            
            choice = input("\n请选择操作: ").strip()
            
            if choice == '1':
                self.student_statistics()
            elif choice == '2':
                self.course_statistics()
            elif choice == '3':
                self.enrollment_statistics()
            elif choice == '0':
                break
                
    def student_statistics(self):
        """学生统计"""
        stats = self.student_model.get_statistics()
        
        print(Fore.CYAN + "\n=== 学生统计信息 ===")
        print(f"总学生数: {stats['total_students']}")
        
        print("\n按专业分布:")
        if stats['by_major']:
            headers = ['专业', '人数']
            data = [[s['major'], s['count']] for s in stats['by_major']]
            print(tabulate(data, headers=headers, tablefmt='grid'))
            
        print("\n按状态分布:")
        if stats['by_status']:
            headers = ['状态', '人数']
            data = [[s['status'], s['count']] for s in stats['by_status']]
            print(tabulate(data, headers=headers, tablefmt='grid'))
            
        print("\n按性别分布:")
        if stats['by_gender']:
            headers = ['性别', '人数']
            data = [[s['gender'], s['count']] for s in stats['by_gender']]
            print(tabulate(data, headers=headers, tablefmt='grid'))
            
    def course_statistics(self):
        """课程统计"""
        stats = self.course_model.get_statistics()
        
        print(Fore.CYAN + "\n=== 课程统计信息 ===")
        print(f"总课程数: {stats['total_courses']}")
        
        print("\n按类型分布:")
        if stats['by_type']:
            headers = ['类型', '数量']
            data = [[s['course_type'], s['count']] for s in stats['by_type']]
            print(tabulate(data, headers=headers, tablefmt='grid'))
            
        print("\n按学期分布:")
        if stats['by_semester']:
            headers = ['学期', '数量']
            data = [[s['semester'], s['count']] for s in stats['by_semester']]
            print(tabulate(data, headers=headers, tablefmt='grid'))
            
        if stats['enrollment_rate']:
            print("\n选课率统计:")
            print(f"平均选课率: {stats['enrollment_rate'].get('avg_enrollment_rate', 0):.2f}%")
            print(f"最高选课率: {stats['enrollment_rate'].get('max_enrollment_rate', 0):.2f}%")
            print(f"最低选课率: {stats['enrollment_rate'].get('min_enrollment_rate', 0):.2f}%")
            
    def enrollment_statistics(self):
        """选课统计"""
        stats = self.enrollment_model.get_statistics()
        
        print(Fore.CYAN + "\n=== 选课统计信息 ===")
        print(f"总选课记录: {stats['total_enrollments']}")
        
        print("\n按学期分布:")
        if stats['by_semester']:
            headers = ['学期', '选课数']
            data = [[s['semester'], s['count']] for s in stats['by_semester']]
            print(tabulate(data, headers=headers, tablefmt='grid'))
            
        print("\n成绩分布:")
        if stats['grade_distribution']:
            headers = ['等级', '人数']
            data = [[g['grade'], g['count']] for g in stats['grade_distribution']]
            print(tabulate(data, headers=headers, tablefmt='grid'))
            
        if stats['score_stats']:
            print("\n成绩统计:")
            print(f"平均分: {stats['score_stats'].get('avg_score', 0):.2f}")
            print(f"最高分: {stats['score_stats'].get('max_score', 0):.2f}")
            print(f"最低分: {stats['score_stats'].get('min_score', 0):.2f}")
            print(f"标准差: {stats['score_stats'].get('std_dev', 0):.2f}")
            
    def show_connection_info(self):
        """显示数据库连接信息"""
        if self.db_connection and self.db_connection.test_connection():
            config = self.db_connection.config
            print(Fore.CYAN + "\n=== 数据库连接信息 ===")
            print(f"主机: {config['host']}")
            print(f"端口: {config['port']}")
            print(f"用户: {config['user']}")
            print(f"数据库: {config['database']}")
            print(f"字符集: {config['charset']}")
            print(f"连接状态: " + Fore.GREEN + "已连接")
        else:
            print(Fore.RED + "数据库未连接")
            
    def run(self):
        """运行客户端"""
        print(Fore.CYAN + "="*50)
        print("欢迎使用学生管理系统 - 本地客户端")
        print("="*50)
        
        # 连接数据库
        if not self.connect_database():
            print(Fore.RED + "无法连接数据库，程序退出")
            return
            
        # 主循环
        while True:
            self.show_menu()
            choice = input("请选择功能: ").strip()
            
            if choice == '1':
                self.student_management()
            elif choice == '2':
                self.course_management()
            elif choice == '3':
                self.enrollment_management()
            elif choice == '4':
                self.grade_management()
            elif choice == '5':
                self.statistics_query()
            elif choice == '6':
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
    client = LocalClient()
    client.run()

