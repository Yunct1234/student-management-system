"""
统一客户端 - 支持本地和远程连接
"""
import os
import sys
from typing import Dict, Any
from colorama import Fore, Style
from tabulate import tabulate
from datetime import datetime, date

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.db_connection import DatabaseConnection
from models.student import Student
from models.course import Course
from models.enrollment import Enrollment

class UnifiedClient:
    """统一客户端类"""
    
    def __init__(self, config: Dict[str, Any], mode: str = 'local'):
        """
        初始化客户端
        
        Args:
            config: 数据库配置
            mode: 连接模式 ('local' 或 'remote')
        """
        self.mode = mode
        self.db_connection = DatabaseConnection(config)
        self.student_model = Student(self.db_connection)
        self.course_model = Course(self.db_connection)
        self.enrollment_model = Enrollment(self.db_connection)
        
    def test_connection(self) -> bool:
        """测试数据库连接"""
        return self.db_connection.test_connection()
        
    def clear_screen(self):
        """清屏"""
        os.system('cls' if os.name == 'nt' else 'clear')
        
    def pause(self):
        """暂停"""
        input(f"\n{Fore.YELLOW}按Enter键继续...{Style.RESET_ALL}")
        
    def print_header(self, title: str):
        """打印标题"""
        print(f"\n{Fore.CYAN}{'='*50}")
        print(f"  {title}")
        print(f"{'='*50}{Style.RESET_ALL}")
        
    def run(self):
        """运行客户端主循环"""
        while True:
            self.show_main_menu()
            choice = input(f"\n{Fore.GREEN}请选择功能 [0-4]: {Style.RESET_ALL}")
            
            if choice == '0':
                print(f"{Fore.YELLOW}退出系统...")
                self.db_connection.disconnect()
                break
            elif choice == '1':
                self.student_menu()
            elif choice == '2':
                self.course_menu()
            elif choice == '3':
                self.enrollment_menu()
            elif choice == '4':
                self.statistics_menu()
            else:
                print(f"{Fore.RED}无效选择！{Style.RESET_ALL}")
                
    def show_main_menu(self):
        """显示主菜单"""
        self.clear_screen()
        mode_text = "本地模式" if self.mode == 'local' else "远程模式"
        self.print_header(f"学生管理系统 - {mode_text}")
        
        menu = """
        1. 学生信息管理
        2. 课程信息管理
        3. 选课管理
        4. 统计分析
        0. 退出系统
        """
        print(menu)
        
    def student_menu(self):
        """学生管理菜单"""
        while True:
            self.clear_screen()
            self.print_header("学生信息管理")
            
            menu = """
            1. 查看所有学生
            2. 添加学生
            3. 查找学生
            4. 更新学生信息
            5. 删除学生
            0. 返回上级菜单
            """
            print(menu)
            
            choice = input(f"\n{Fore.GREEN}请选择操作 [0-5]: {Style.RESET_ALL}")
            
            if choice == '0':
                break
            elif choice == '1':
                self.view_all_students()
            elif choice == '2':
                self.add_student()
            elif choice == '3':
                self.search_student()
            elif choice == '4':
                self.update_student()
            elif choice == '5':
                self.delete_student()
            else:
                print(f"{Fore.RED}无效选择！{Style.RESET_ALL}")
            
            self.pause()
            
    def view_all_students(self):
        """查看所有学生"""
        self.print_header("学生列表")
        
        try:
            students = self.student_model.get_all()
            
            if not students:
                print(f"{Fore.YELLOW}暂无学生信息{Style.RESET_ALL}")
                return
                
            # 准备表格数据
            headers = ['学号', '姓名', '性别', '年龄', '专业', '班级', '状态']
            rows = []
            
            for student in students:
                rows.append([
                    student.get('student_id'),
                    student.get('name'),
                    student.get('gender'),
                    student.get('age'),
                    student.get('major'),
                    student.get('class_name'),
                    student.get('status')
                ])
                
            print(tabulate(rows, headers=headers, tablefmt='grid'))
            print(f"\n共 {len(students)} 名学生")
            
        except Exception as e:
            print(f"{Fore.RED}查询失败: {e}{Style.RESET_ALL}")
            
    def add_student(self):
        """添加学生"""
        self.print_header("添加新学生")
        
        try:
            print("请输入学生信息（留空使用默认值）：")
            
            student_data = {
                'student_id': input("学号: ").strip(),
                'name': input("姓名: ").strip(),
                'gender': input("性别 [男/女]: ").strip() or '男',
                'age': int(input("年龄: ").strip() or "18"),
                'major': input("专业: ").strip(),
                'class_name': input("班级: ").strip(),
                'phone': input("电话: ").strip(),
                'email': input("邮箱: ").strip(),
                'enrollment_date': date.today(),
                'status': '在读'
            }
            
            # 验证必填字段
            if not student_data['student_id'] or not student_data['name']:
                print(f"{Fore.RED}学号和姓名为必填项！{Style.RESET_ALL}")
                return
                
            # 添加学生
            if self.student_model.create(student_data):
                print(f"{Fore.GREEN}✓ 学生添加成功！{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}✗ 学生添加失败！{Style.RESET_ALL}")
                
        except ValueError as e:
            print(f"{Fore.RED}输入格式错误: {e}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}操作失败: {e}{Style.RESET_ALL}")
            
    def search_student(self):
        """搜索学生"""
        self.print_header("搜索学生")
        
        keyword = input("请输入搜索关键字（学号/姓名/专业）: ").strip()
        
        if not keyword:
            print(f"{Fore.YELLOW}搜索关键字不能为空{Style.RESET_ALL}")
            return
            
        try:
            students = self.student_model.search(keyword)
            
            if not students:
                print(f"{Fore.YELLOW}未找到相关学生{Style.RESET_ALL}")
                return
                
            # 显示搜索结果
            headers = ['学号', '姓名', '性别', '专业', '班级', '电话', '状态']
            rows = []
            
            for student in students:
                rows.append([
                    student.get('student_id'),
                    student.get('name'),
                    student.get('gender'),
                    student.get('major'),
                    student.get('class_name'),
                    student.get('phone'),
                    student.get('status')
                ])
                
            print(f"\n找到 {len(students)} 个结果：")
            print(tabulate(rows, headers=headers, tablefmt='grid'))
            
        except Exception as e:
            print(f"{Fore.RED}搜索失败: {e}{Style.RESET_ALL}")
            
    def update_student(self):
        """更新学生信息"""
        self.print_header("更新学生信息")
        
        student_id = input("请输入要更新的学号: ").strip()
        
        if not student_id:
            print(f"{Fore.YELLOW}学号不能为空{Style.RESET_ALL}")
            return
            
        try:
            # 先查询学生是否存在
            student = self.student_model.get_by_id(student_id)
            if not student:
                print(f"{Fore.RED}未找到该学生{Style.RESET_ALL}")
                return
                
            print(f"\n当前学生信息：")
            print(f"姓名: {student['name']}")
            print(f"专业: {student['major']}")
            print(f"班级: {student['class_name']}")
            
            print("\n请输入要更新的信息（留空保持原值）：")
            
            update_data = {}
            
            phone = input("新电话: ").strip()
            if phone:
                update_data['phone'] = phone
                
            email = input("新邮箱: ").strip()
            if email:
                update_data['email'] = email
                
            major = input("新专业: ").strip()
            if major:
                update_data['major'] = major
                
            class_name = input("新班级: ").strip()
            if class_name:
                update_data['class_name'] = class_name
                
            status = input("新状态 [在读/休学/毕业]: ").strip()
            if status:
                update_data['status'] = status
                
            if not update_data:
                print(f"{Fore.YELLOW}没有要更新的内容{Style.RESET_ALL}")
                return
                
            # 执行更新
            if self.student_model.update(student_id, update_data):
                print(f"{Fore.GREEN}✓ 更新成功！{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}✗ 更新失败！{Style.RESET_ALL}")
                
        except Exception as e:
            print(f"{Fore.RED}操作失败: {e}{Style.RESET_ALL}")
            
    def delete_student(self):
        """删除学生"""
        self.print_header("删除学生")
        
        student_id = input("请输入要删除的学号: ").strip()
        
        if not student_id:
            print(f"{Fore.YELLOW}学号不能为空{Style.RESET_ALL}")
            return
            
        try:
            # 先查询学生是否存在
            student = self.student_model.get_by_id(student_id)
            if not student:
                print(f"{Fore.RED}未找到该学生{Style.RESET_ALL}")
                return
                
            print(f"\n将要删除学生：{student['name']} ({student_id})")
            confirm = input("确认删除？(y/n): ").strip().lower()
            
            if confirm == 'y':
                if self.student_model.delete(student_id):
                    print(f"{Fore.GREEN}✓ 删除成功！{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}✗ 删除失败！{Style.RESET_ALL}")
            else:
                print(f"{Fore.YELLOW}已取消删除{Style.RESET_ALL}")
                
        except Exception as e:
            print(f"{Fore.RED}操作失败: {e}{Style.RESET_ALL}")
            
    def course_menu(self):
        """课程管理菜单"""
        while True:
            self.clear_screen()
            self.print_header("课程信息管理")
            
            menu = """
            1. 查看所有课程
            2. 添加课程
            3. 查找课程
            4. 更新课程信息
            5. 删除课程
            0. 返回上级菜单
            """
            print(menu)
            
            choice = input(f"\n{Fore.GREEN}请选择操作 [0-5]: {Style.RESET_ALL}")
            
            if choice == '0':
                break
            elif choice == '1':
                self.view_all_courses()
            elif choice == '2':
                self.add_course()
            elif choice == '3':
                self.search_course()
            elif choice == '4':
                self.update_course()
            elif choice == '5':
                self.delete_course()
            else:
                print(f"{Fore.RED}无效选择！{Style.RESET_ALL}")
            
            self.pause()
            
    def view_all_courses(self):
        """查看所有课程"""
        self.print_header("课程列表")
        
        try:
            courses = self.course_model.get_all()
            
            if not courses:
                print(f"{Fore.YELLOW}暂无课程信息{Style.RESET_ALL}")
                return
                
            headers = ['课程编号', '课程名称', '学分', '教师', '学期', '类型', '最大人数']
            rows = []
            
            for course in courses:
                rows.append([
                    course.get('course_id'),
                    course.get('course_name'),
                    course.get('credits'),
                    course.get('teacher'),
                    course.get('semester'),
                    course.get('course_type'),
                    course.get('max_students')
                ])
                
            print(tabulate(rows, headers=headers, tablefmt='grid'))
            print(f"\n共 {len(courses)} 门课程")
            
        except Exception as e:
            print(f"{Fore.RED}查询失败: {e}{Style.RESET_ALL}")
            
    def add_course(self):
        """添加课程"""
        self.print_header("添加新课程")
        
        try:
            print("请输入课程信息：")
            
            course_data = {
                'course_id': input("课程编号: ").strip(),
                'course_name': input("课程名称: ").strip(),
                'credits': float(input("学分: ").strip() or "2.0"),
                'teacher': input("教师: ").strip(),
                'department': input("开课学院: ").strip(),
                'semester': input("学期 [如: 2024-1]: ").strip(),
                'course_type': input("类型 [必修/选修]: ").strip() or '选修',
                'max_students': int(input("最大人数: ").strip() or "50"),
                'classroom': input("教室: ").strip(),
                'schedule': input("上课时间: ").strip()
            }
            
            # 验证必填字段
            if not course_data['course_id'] or not course_data['course_name']:
                print(f"{Fore.RED}课程编号和名称为必填项！{Style.RESET_ALL}")
                return
                
            # 添加课程
            if self.course_model.create(course_data):
                print(f"{Fore.GREEN}✓ 课程添加成功！{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}✗ 课程添加失败！{Style.RESET_ALL}")
                
        except ValueError as e:
            print(f"{Fore.RED}输入格式错误: {e}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}操作失败: {e}{Style.RESET_ALL}")
            
    def search_course(self):
        """搜索课程"""
        self.print_header("搜索课程")
        
        keyword = input("请输入搜索关键字（课程编号/名称/教师）: ").strip()
        
        if not keyword:
            print(f"{Fore.YELLOW}搜索关键字不能为空{Style.RESET_ALL}")
            return
            
        try:
            courses = self.course_model.search(keyword)
            
            if not courses:
                print(f"{Fore.YELLOW}未找到相关课程{Style.RESET_ALL}")
                return
                
            headers = ['课程编号', '课程名称', '学分', '教师', '学期', '类型']
            rows = []
            
            for course in courses:
                rows.append([
                    course.get('course_id'),
                    course.get('course_name'),
                    course.get('credits'),
                    course.get('teacher'),
                    course.get('semester'),
                    course.get('course_type')
                ])
                
            print(f"\n找到 {len(courses)} 个结果：")
            print(tabulate(rows, headers=headers, tablefmt='grid'))
            
        except Exception as e:
            print(f"{Fore.RED}搜索失败: {e}{Style.RESET_ALL}")
            
    def update_course(self):
        """更新课程信息"""
        self.print_header("更新课程信息")
        
        course_id = input("请输入要更新的课程编号: ").strip()
        
        if not course_id:
            print(f"{Fore.YELLOW}课程编号不能为空{Style.RESET_ALL}")
            return
            
        try:
            # 先查询课程是否存在
            course = self.course_model.get_by_id(course_id)
            if not course:
                print(f"{Fore.RED}未找到该课程{Style.RESET_ALL}")
                return
                
            print(f"\n当前课程信息：")
            print(f"名称: {course['course_name']}")
            print(f"教师: {course['teacher']}")
            print(f"学分: {course['credits']}")
            
            print("\n请输入要更新的信息（留空保持原值）：")
            
            update_data = {}
            
            teacher = input("新教师: ").strip()
            if teacher:
                update_data['teacher'] = teacher
                
            classroom = input("新教室: ").strip()
            if classroom:
                update_data['classroom'] = classroom
                
            max_students = input("新最大人数: ").strip()
            if max_students:
                update_data['max_students'] = int(max_students)
                
            schedule = input("新上课时间: ").strip()
            if schedule:
                update_data['schedule'] = schedule
                
            if not update_data:
                print(f"{Fore.YELLOW}没有要更新的内容{Style.RESET_ALL}")
                return
                
            # 执行更新
            if self.course_model.update(course_id, update_data):
                print(f"{Fore.GREEN}✓ 更新成功！{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}✗ 更新失败！{Style.RESET_ALL}")
                
        except Exception as e:
            print(f"{Fore.RED}操作失败: {e}{Style.RESET_ALL}")
            
    def delete_course(self):
        """删除课程"""
        self.print_header("删除课程")
        
        course_id = input("请输入要删除的课程编号: ").strip()
        
        if not course_id:
            print(f"{Fore.YELLOW}课程编号不能为空{Style.RESET_ALL}")
            return
            
        try:
            # 先查询课程是否存在
            course = self.course_model.get_by_id(course_id)
            if not course:
                print(f"{Fore.RED}未找到该课程{Style.RESET_ALL}")
                return
                
            print(f"\n将要删除课程：{course['course_name']} ({course_id})")
            confirm = input("确认删除？(y/n): ").strip().lower()
            
            if confirm == 'y':
                if self.course_model.delete(course_id):
                    print(f"{Fore.GREEN}✓ 删除成功！{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}✗ 删除失败！{Style.RESET_ALL}")
            else:
                print(f"{Fore.YELLOW}已取消删除{Style.RESET_ALL}")
                
        except Exception as e:
            print(f"{Fore.RED}操作失败: {e}{Style.RESET_ALL}")
            
    def enrollment_menu(self):
        """选课管理菜单"""
        while True:
            self.clear_screen()
            self.print_header("选课管理")
            
            menu = """
            1. 学生选课
            2. 学生退选
            3. 查看学生选课
            4. 查看课程选课名单
            5. 录入成绩
            6. 查询成绩
            0. 返回上级菜单
            """
            print(menu)
            
            choice = input(f"\n{Fore.GREEN}请选择操作 [0-6]: {Style.RESET_ALL}")
            
            if choice == '0':
                break
            elif choice == '1':
                self.enroll_course()
            elif choice == '2':
                self.drop_course()
            elif choice == '3':
                self.view_student_courses()
            elif choice == '4':
                self.view_course_students()
            elif choice == '5':
                self.input_score()
            elif choice == '6':
                self.query_score()
            else:
                print(f"{Fore.RED}无效选择！{Style.RESET_ALL}")
            
            self.pause()
            
    def enroll_course(self):
        """学生选课"""
        self.print_header("学生选课")
        
        try:
            student_id = input("请输入学号: ").strip()
            if not student_id:
                print(f"{Fore.YELLOW}学号不能为空{Style.RESET_ALL}")
                return
                
            # 验证学生是否存在
            student = self.student_model.get_by_id(student_id)
            if not student:
                print(f"{Fore.RED}未找到该学生{Style.RESET_ALL}")
                return
                
            print(f"\n学生: {student['name']} ({student_id})")
            
            # 显示可选课程
            semester = input("请输入学期 [如: 2024-1]: ").strip()
            courses = self.course_model.get_available_courses(semester)
            
            if not courses:
                print(f"{Fore.YELLOW}该学期暂无可选课程{Style.RESET_ALL}")
                return
                
            print("\n可选课程列表：")
            headers = ['序号', '课程编号', '课程名称', '学分', '教师', '类型']
            rows = []
            
            for i, course in enumerate(courses, 1):
                rows.append([
                    i,
                    course.get('course_id'),
                    course.get('course_name'),
                    course.get('credits'),
                    course.get('teacher'),
                    course.get('course_type')
                ])
                
            print(tabulate(rows, headers=headers, tablefmt='grid'))
            
            # 选择课程
            try:
                choice = int(input("\n请选择要选的课程序号: ").strip())
                if 1 <= choice <= len(courses):
                    selected_course = courses[choice - 1]
                    
                    enrollment_data = {
                        'student_id': student_id,
                        'course_id': selected_course['course_id'],
                        'semester': semester
                    }
                    
                    if self.enrollment_model.enroll(enrollment_data):
                        print(f"{Fore.GREEN}✓ 选课成功！{Style.RESET_ALL}")
                    else:
                        print(f"{Fore.RED}✗ 选课失败！可能已经选过该课程{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}无效的选择{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED}请输入有效的数字{Style.RESET_ALL}")
                
        except Exception as e:
            print(f"{Fore.RED}操作失败: {e}{Style.RESET_ALL}")
            
    def drop_course(self):
        """学生退选"""
        self.print_header("学生退选")
        
        try:
            student_id = input("请输入学号: ").strip()
            if not student_id:
                print(f"{Fore.YELLOW}学号不能为空{Style.RESET_ALL}")
                return
                
            # 获取学生已选课程
            courses = self.enrollment_model.get_student_courses(student_id)
            
            if not courses:
                print(f"{Fore.YELLOW}该学生未选任何课程{Style.RESET_ALL}")
                return
                
            print("\n已选课程列表：")
            headers = ['序号', '课程编号', '课程名称', '学分', '教师', '学期', '成绩']
            rows = []
            
            for i, course in enumerate(courses, 1):
                rows.append([
                    i,
                    course.get('course_id'),
                    course.get('course_name'),
                    course.get('credits'),
                    course.get('teacher'),
                    course.get('semester'),
                    course.get('score', '未录入')
                ])
                
            print(tabulate(rows, headers=headers, tablefmt='grid'))
            
            # 选择要退选的课程
            try:
                choice = int(input("\n请选择要退选的课程序号: ").strip())
                if 1 <= choice <= len(courses):
                    selected_course = courses[choice - 1]
                    
                    confirm = input(f"确认退选 {selected_course['course_name']}？(y/n): ").strip().lower()
                    
                    if confirm == 'y':
                        if self.enrollment_model.drop_course(
                            student_id, 
                            selected_course['course_id'],
                            selected_course['semester']
                        ):
                            print(f"{Fore.GREEN}✓ 退选成功！{Style.RESET_ALL}")
                        else:
                            print(f"{Fore.RED}✗ 退选失败！{Style.RESET_ALL}")
                    else:
                        print(f"{Fore.YELLOW}已取消退选{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}无效的选择{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED}请输入有效的数字{Style.RESET_ALL}")
                
        except Exception as e:
            print(f"{Fore.RED}操作失败: {e}{Style.RESET_ALL}")
            
    def view_student_courses(self):
        """查看学生选课"""
        self.print_header("查看学生选课")
        
        student_id = input("请输入学号: ").strip()
        
        if not student_id:
            print(f"{Fore.YELLOW}学号不能为空{Style.RESET_ALL}")
            return
            
        try:
            # 获取学生信息
            student = self.student_model.get_by_id(student_id)
            if not student:
                print(f"{Fore.RED}未找到该学生{Style.RESET_ALL}")
                return
                
            print(f"\n学生: {student['name']} ({student_id})")
            print(f"专业: {student['major']}")
            print(f"班级: {student['class_name']}")
            
            # 获取选课列表
            courses = self.enrollment_model.get_student_courses(student_id)
            
            if not courses:
                print(f"\n{Fore.YELLOW}该学生未选任何课程{Style.RESET_ALL}")
                return
                
            print("\n选课列表：")
            headers = ['课程编号', '课程名称', '学分', '教师', '学期', '成绩', '等级']
            rows = []
            total_credits = 0
            
            for course in courses:
                rows.append([
                    course.get('course_id'),
                    course.get('course_name'),
                    course.get('credits'),
                    course.get('teacher'),
                    course.get('semester'),
                    course.get('score', '-'),
                    course.get('grade', '-')
                ])
                total_credits += float(course.get('credits', 0))
                
            print(tabulate(rows, headers=headers, tablefmt='grid'))
            print(f"\n总学分: {total_credits}")
            
        except Exception as e:
            print(f"{Fore.RED}查询失败: {e}{Style.RESET_ALL}")
            
    def view_course_students(self):
        """查看课程选课名单"""
        self.print_header("查看课程选课名单")
        
        course_id = input("请输入课程编号: ").strip()
        semester = input("请输入学期 [如: 2024-1]: ").strip()
        
        if not course_id or not semester:
            print(f"{Fore.YELLOW}课程编号和学期不能为空{Style.RESET_ALL}")
            return
            
        try:
            # 获取课程信息
            course = self.course_model.get_by_id(course_id)
            if not course:
                print(f"{Fore.RED}未找到该课程{Style.RESET_ALL}")
                return
                
            print(f"\n课程: {course['course_name']} ({course_id})")
            print(f"教师: {course['teacher']}")
            print(f"学期: {semester}")
            
            # 获取选课学生名单
            students = self.enrollment_model.get_course_students(course_id, semester)
            
            if not students:
                print(f"\n{Fore.YELLOW}该课程暂无学生选课{Style.RESET_ALL}")
                return
                
            print("\n选课学生名单：")
            headers = ['序号', '学号', '姓名', '专业', '班级', '成绩', '等级']
            rows = []
            
            for i, student in enumerate(students, 1):
                rows.append([
                    i,
                    student.get('student_id'),
                    student.get('name'),
                    student.get('major'),
                    student.get('class_name'),
                    student.get('score', '-'),
                    student.get('grade', '-')
                ])
                
            print(tabulate(rows, headers=headers, tablefmt='grid'))
            print(f"\n选课人数: {len(students)}")
            
        except Exception as e:
            print(f"{Fore.RED}查询失败: {e}{Style.RESET_ALL}")
            
    def input_score(self):
        """录入成绩"""
        self.print_header("录入成绩")
        
        try:
            course_id = input("请输入课程编号: ").strip()
            semester = input("请输入学期: ").strip()
            
            if not course_id or not semester:
                print(f"{Fore.YELLOW}课程编号和学期不能为空{Style.RESET_ALL}")
                return
                
            # 获取选课学生名单
            students = self.enrollment_model.get_course_students(course_id, semester)
            
            if not students:
                print(f"{Fore.YELLOW}该课程暂无学生选课{Style.RESET_ALL}")
                return
                
            print(f"\n共有 {len(students)} 名学生，请依次输入成绩：")
            
            for student in students:
                print(f"\n{student['name']} ({student['student_id']})")
                
                while True:
                    score_str = input("成绩 (0-100): ").strip()
                    
                    if not score_str:
                        print(f"{Fore.YELLOW}跳过该学生{Style.RESET_ALL}")
                        break
                        
                    try:
                        score = float(score_str)
                        if 0 <= score <= 100:
                            # 录入成绩
                            if self.enrollment_model.input_score(
                                student['student_id'],
                                course_id,
                                semester,
                                score
                            ):
                                print(f"{Fore.GREEN}✓ 成绩录入成功{Style.RESET_ALL}")
                            else:
                                print(f"{Fore.RED}✗ 成绩录入失败{Style.RESET_ALL}")
                            break
                        else:
                            print(f"{Fore.RED}成绩必须在0-100之间{Style.RESET_ALL}")
                    except ValueError:
                        print(f"{Fore.RED}请输入有效的数字{Style.RESET_ALL}")
                        
            print(f"\n{Fore.GREEN}成绩录入完成！{Style.RESET_ALL}")
            
        except Exception as e:
            print(f"{Fore.RED}操作失败: {e}{Style.RESET_ALL}")
            
    def query_score(self):
        """查询成绩"""
        self.print_header("查询成绩")
        
        print("1. 查询学生成绩")
        print("2. 查询课程成绩分布")
        
        choice = input("\n请选择 [1-2]: ").strip()
        
        if choice == '1':
            self.query_student_score()
        elif choice == '2':
            self.query_course_score()
        else:
            print(f"{Fore.RED}无效选择{Style.RESET_ALL}")
            
    def query_student_score(self):
        """查询学生成绩"""
        student_id = input("请输入学号: ").strip()
        
        if not student_id:
            print(f"{Fore.YELLOW}学号不能为空{Style.RESET_ALL}")
            return
            
        try:
            scores = self.enrollment_model.get_student_scores(student_id)
            
            if not scores:
                print(f"{Fore.YELLOW}未找到成绩记录{Style.RESET_ALL}")
                return
                
            print("\n成绩单：")
            headers = ['课程名称', '学分', '成绩', '等级', '学期']
            rows = []
            total_credits = 0
            total_points = 0
            
            for score in scores:
                if score.get('score') is not None:
                    rows.append([
                        score.get('course_name'),
                        score.get('credits'),
                        score.get('score'),
                        score.get('grade'),
                        score.get('semester')
                    ])
                    
                    # 计算绩点
                    credit = float(score.get('credits', 0))
                    score_value = float(score.get('score', 0))
                    total_credits += credit
                    total_points += credit * score_value
                    
            print(tabulate(rows, headers=headers, tablefmt='grid'))
            
            if total_credits > 0:
                gpa = total_points / total_credits
                print(f"\n平均分: {gpa:.2f}")
                
        except Exception as e:
            print(f"{Fore.RED}查询失败: {e}{Style.RESET_ALL}")
            
    def query_course_score(self):
        """查询课程成绩分布"""
        course_id = input("请输入课程编号: ").strip()
        semester = input("请输入学期: ").strip()
        
        if not course_id or not semester:
            print(f"{Fore.YELLOW}课程编号和学期不能为空{Style.RESET_ALL}")
            return
            
        try:
            stats = self.enrollment_model.get_course_score_distribution(course_id, semester)
            
            if not stats:
                print(f"{Fore.YELLOW}未找到成绩数据{Style.RESET_ALL}")
                return
                
            print("\n成绩分布：")
            print(f"总人数: {stats.get('total', 0)}")
            print(f"最高分: {stats.get('max_score', 0)}")
            print(f"最低分: {stats.get('min_score', 0)}")
            print(f"平均分: {stats.get('avg_score', 0):.2f}")
            
            # 显示分数段分布
            if 'distribution' in stats:
                print("\n分数段分布：")
                headers = ['分数段', '人数', '占比']
                rows = []
                
                for range_name, count in stats['distribution'].items():
                    percentage = (count / stats['total']) * 100 if stats['total'] > 0 else 0
                    rows.append([range_name, count, f"{percentage:.1f}%"])
                    
                print(tabulate(rows, headers=headers, tablefmt='grid'))
                
        except Exception as e:
            print(f"{Fore.RED}查询失败: {e}{Style.RESET_ALL}")
            
    def statistics_menu(self):
        """统计分析菜单"""
        while True:
            self.clear_screen()
            self.print_header("统计分析")
            
            menu = """
            1. 学生统计
            2. 课程统计
            3. 选课统计
            4. 成绩统计
            0. 返回上级菜单
            """
            print(menu)
            
            choice = input(f"\n{Fore.GREEN}请选择操作 [0-4]: {Style.RESET_ALL}")
            
            if choice == '0':
                break
            elif choice == '1':
                self.student_statistics()
            elif choice == '2':
                self.course_statistics()
            elif choice == '3':
                self.enrollment_statistics()
            elif choice == '4':
                self.score_statistics()
            else:
                print(f"{Fore.RED}无效选择！{Style.RESET_ALL}")
            
            self.pause()
            
    def student_statistics(self):
        """学生统计"""
        self.print_header("学生统计")
        
        try:
            stats = self.student_model.get_statistics()
            
            print(f"\n总学生数: {stats.get('total_students', 0)}")
            
            # 按状态统计
            if 'by_status' in stats:
                print("\n按状态统计：")
                for status, count in stats['by_status'].items():
                    print(f"  {status}: {count} 人")
                    
            # 按专业统计
            if 'by_major' in stats:
                print("\n按专业统计：")
                headers = ['专业', '人数']
                rows = [[major, count] for major, count in stats['by_major'].items()]
                print(tabulate(rows, headers=headers, tablefmt='grid'))
                
            # 按性别统计
            if 'by_gender' in stats:
                print("\n按性别统计：")
                for gender, count in stats['by_gender'].items():
                    print(f"  {gender}: {count} 人")
                    
        except Exception as e:
            print(f"{Fore.RED}统计失败: {e}{Style.RESET_ALL}")
            
    def course_statistics(self):
        """课程统计"""
        self.print_header("课程统计")
        
        try:
            stats = self.course_model.get_statistics()
            
            print(f"\n总课程数: {stats.get('total_courses', 0)}")
            
            # 按类型统计
            if 'by_type' in stats:
                print("\n按类型统计：")
                for course_type, count in stats['by_type'].items():
                    print(f"  {course_type}: {count} 门")
                    
            # 按学期统计
            if 'by_semester' in stats:
                print("\n按学期统计：")
                headers = ['学期', '课程数']
                rows = [[semester, count] for semester, count in stats['by_semester'].items()]
                print(tabulate(rows, headers=headers, tablefmt='grid'))
                
            # 按学院统计
            if 'by_department' in stats:
                print("\n按学院统计：")
                headers = ['学院', '课程数']
                rows = [[dept, count] for dept, count in stats['by_department'].items()]
                print(tabulate(rows, headers=headers, tablefmt='grid'))
                
        except Exception as e:
            print(f"{Fore.RED}统计失败: {e}{Style.RESET_ALL}")
            
    def enrollment_statistics(self):
        """选课统计"""
        self.print_header("选课统计")
        
        try:
            stats = self.enrollment_model.get_statistics()
            
            print(f"\n总选课记录: {stats.get('total_enrollments', 0)}")
            
            # 热门课程
            if 'popular_courses' in stats:
                print("\n热门课程Top 10：")
                headers = ['排名', '课程名称', '选课人数']
                rows = []
                
                for i, course in enumerate(stats['popular_courses'][:10], 1):
                    rows.append([i, course['course_name'], course['count']])
                    
                print(tabulate(rows, headers=headers, tablefmt='grid'))
                
            # 学生选课数分布
            if 'student_course_count' in stats:
                print("\n学生选课数分布：")
                headers = ['选课数', '学生数']
                rows = []
                
                for count, students in stats['student_course_count'].items():
                    rows.append([f"{count} 门", students])
                    
                print(tabulate(rows, headers=headers, tablefmt='grid'))
                
        except Exception as e:
            print(f"{Fore.RED}统计失败: {e}{Style.RESET_ALL}")
            
    def score_statistics(self):
        """成绩统计"""
        self.print_header("成绩统计")
        
        semester = input("请输入学期 [留空查看所有]: ").strip()
        
        try:
            stats = self.enrollment_model.get_score_statistics(semester)
            
            if not stats:
                print(f"{Fore.YELLOW}暂无成绩数据{Style.RESET_ALL}")
                return
                
            print(f"\n整体成绩统计：")
            print(f"已录入成绩数: {stats.get('total_scores', 0)}")
            print(f"平均分: {stats.get('overall_avg', 0):.2f}")
            
            # 成绩分布
            if 'grade_distribution' in stats:
                print("\n成绩等级分布：")
                headers = ['等级', '人数', '占比']
                rows = []
                total = stats.get('total_scores', 1)
                
                for grade, count in stats['grade_distribution'].items():
                    percentage = (count / total) * 100
                    rows.append([grade, count, f"{percentage:.1f}%"])
                    
                print(tabulate(rows, headers=headers, tablefmt='grid'))
                
            # 不及格统计
            if 'failed_students' in stats:
                print(f"\n不及格人数: {len(stats['failed_students'])}")
                if stats['failed_students'] and len(stats['failed_students']) <= 10:
                    print("不及格学生：")
                    for student in stats['failed_students']:
                        print(f"  - {student['name']} ({student['student_id']})")
                        
        except Exception as e:
            print(f"{Fore.RED}统计失败: {e}{Style.RESET_ALL}")
