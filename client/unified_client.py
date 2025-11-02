"""
统一客户端实现
"""
import os
import sys
from typing import Dict, Any, Optional
from colorama import Fore, Style
from datetime import datetime

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import Student, Course, Enrollment
from utils import DatabaseConnection

class UnifiedClient:
    """统一客户端类"""
    
    def __init__(self, config: Dict[str, Any], mode: str = 'local'):
        """初始化客户端"""
        self.config = config
        self.mode = mode
        self.db_conn = DatabaseConnection(config)
        
        # 初始化数据模型
        self.student_model = Student(self.db_conn)
        self.course_model = Course(self.db_conn)
        self.enrollment_model = Enrollment(self.db_conn)
        
    def test_connection(self) -> bool:
        """测试数据库连接"""
        try:
            return self.db_conn.test_connection()
        except Exception as e:
            print(f"{Fore.RED}连接测试失败: {e}")
            return False
            
    def run(self):
        """运行客户端主循环"""
        while True:
            self.show_main_menu()
            choice = input(f"\n{Fore.GREEN}请选择功能 [0-5]: {Style.RESET_ALL}")
            
            if choice == '0':
                self.cleanup()
                print(f"{Fore.YELLOW}感谢使用，再见！")
                break
            elif choice == '1':
                self.student_management()
            elif choice == '2':
                self.course_management()
            elif choice == '3':
                self.enrollment_management()
            elif choice == '4':
                self.score_management()
            elif choice == '5':
                self.show_statistics()
            else:
                print(f"{Fore.RED}无效选择，请重试")
                
    def show_main_menu(self):
        """显示主菜单"""
        print(f"\n{Fore.CYAN}{'='*50}")
        print(f"{Fore.CYAN}主菜单 - {self.mode.upper()} 模式")
        print(f"{Fore.CYAN}{'='*50}")
        print("1. 学生信息管理")
        print("2. 课程信息管理")
        print("3. 选课管理")
        print("4. 成绩管理")
        print("5. 统计查询")
        print("0. 退出系统")
        
    def student_management(self):
        """学生信息管理"""
        while True:
            print(f"\n{Fore.YELLOW}学生信息管理")
            print("1. 查看所有学生")
            print("2. 添加学生")
            print("3. 查询学生")
            print("4. 修改学生信息")
            print("5. 删除学生")
            print("0. 返回主菜单")
            
            choice = input(f"{Fore.GREEN}请选择 [0-5]: {Style.RESET_ALL}")
            
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
                
    def course_management(self):
        """课程信息管理"""
        while True:
            print(f"\n{Fore.YELLOW}课程信息管理")
            print("1. 查看所有课程")
            print("2. 添加课程")
            print("3. 查询课程")
            print("4. 修改课程信息")
            print("5. 删除课程")
            print("0. 返回主菜单")
            
            choice = input(f"{Fore.GREEN}请选择 [0-5]: {Style.RESET_ALL}")
            
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
                
    def enrollment_management(self):
        """选课管理"""
        while True:
            print(f"\n{Fore.YELLOW}选课管理")
            print("1. 学生选课")
            print("2. 学生退课")
            print("3. 查看学生选课列表")
            print("4. 查看课程选课名单")
            print("0. 返回主菜单")
            
            choice = input(f"{Fore.GREEN}请选择 [0-4]: {Style.RESET_ALL}")
            
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
                
    def score_management(self):
        """成绩管理"""
        while True:
            print(f"\n{Fore.YELLOW}成绩管理")
            print("1. 录入成绩")
            print("2. 查看学生成绩")
            print("3. 查看课程成绩分布")
            print("0. 返回主菜单")
            
            choice = input(f"{Fore.GREEN}请选择 [0-3]: {Style.RESET_ALL}")
            
            if choice == '0':
                break
            elif choice == '1':
                self.input_score()
            elif choice == '2':
                self.view_student_scores()
            elif choice == '3':
                self.view_course_score_distribution()
                
    def show_statistics(self):
        """显示统计信息"""
        print(f"\n{Fore.CYAN}系统统计信息")
        print("="*50)
        
        # 学生统计
        student_stats = self.student_model.get_statistics()
        print(f"\n{Fore.YELLOW}学生统计：")
        print(f"总人数: {student_stats.get('total_students', 0)}")
        if 'by_major' in student_stats:
            print("各专业人数:")
            for major, count in student_stats['by_major'].items():
                print(f"  {major}: {count}")
                
        # 课程统计
        course_stats = self.course_model.get_statistics()
        print(f"\n{Fore.YELLOW}课程统计：")
        print(f"总课程数: {course_stats.get('total_courses', 0)}")
        
        # 选课统计
        enrollment_stats = self.enrollment_model.get_statistics()
        print(f"\n{Fore.YELLOW}选课统计：")
        print(f"总选课记录: {enrollment_stats.get('total_enrollments', 0)}")
        
        input(f"\n{Fore.GREEN}按回车键返回主菜单...")
        
    # 学生管理具体功能
    def view_all_students(self):
        """查看所有学生"""
        students = self.student_model.get_all()
        if students:
            print(f"\n{Fore.CYAN}学生列表：")
            print("-"*80)
            print(f"{'学号':<12} {'姓名':<10} {'性别':<6} {'专业':<20} {'班级':<15} {'状态':<8}")
            print("-"*80)
            for s in students:
                print(f"{s['student_id']:<12} {s['name']:<10} {s['gender']:<6} "
                      f"{s['major']:<20} {s.get('class_name', ''):<15} {s['status']:<8}")
        else:
            print(f"{Fore.YELLOW}暂无学生数据")
        input(f"\n{Fore.GREEN}按回车键返回...")
        
    def add_student(self):
        """添加学生"""
        print(f"\n{Fore.CYAN}添加新学生")
        student_data = {
            'student_id': input("学号: "),
            'name': input("姓名: "),
            'gender': input("性别 [男/女]: ") or '男',
            'age': int(input("年龄: ") or 18),
            'major': input("专业: "),
            'class_name': input("班级: "),
            'phone': input("电话: "),
            'email': input("邮箱: "),
            'enrollment_date': datetime.now().strftime('%Y-%m-%d')
        }
        
        if self.student_model.create(student_data):
            print(f"{Fore.GREEN}✓ 学生添加成功")
        else:
            print(f"{Fore.RED}✗ 学生添加失败")
            
    def search_student(self):
        """查询学生"""
        keyword = input("请输入查询关键词（学号/姓名/专业）: ")
        students = self.student_model.search(keyword=keyword)
        
        if students:
            print(f"\n{Fore.CYAN}查询结果：")
            for s in students:
                print(f"学号: {s['student_id']}, 姓名: {s['name']}, "
                      f"专业: {s['major']}, 状态: {s['status']}")
        else:
            print(f"{Fore.YELLOW}未找到相关学生")
            
    def update_student(self):
        """修改学生信息"""
        student_id = input("请输入要修改的学号: ")
        student = self.student_model.get_by_id(student_id)
        
        if not student:
            print(f"{Fore.RED}学生不存在")
            return
            
        print(f"\n当前信息: {student['name']} - {student['major']}")
        update_data = {}
        
        new_phone = input(f"新电话 [当前: {student.get('phone', '')}]: ")
        if new_phone:
            update_data['phone'] = new_phone
            
        new_email = input(f"新邮箱 [当前: {student.get('email', '')}]: ")
        if new_email:
            update_data['email'] = new_email
            
        if update_data:
            if self.student_model.update(student_id, update_data):
                print(f"{Fore.GREEN}✓ 更新成功")
            else:
                print(f"{Fore.RED}✗ 更新失败")
        else:
            print(f"{Fore.YELLOW}未进行任何修改")
            
    def delete_student(self):
        """删除学生"""
        student_id = input("请输入要删除的学号: ")
        confirm = input(f"{Fore.YELLOW}确认删除？(y/n): ")
        
        if confirm.lower() == 'y':
            if self.student_model.delete(student_id):
                print(f"{Fore.GREEN}✓ 删除成功")
            else:
                print(f"{Fore.RED}✗ 删除失败")
                
    # 课程管理具体功能
    def view_all_courses(self):
        """查看所有课程"""
        courses = self.course_model.get_all()
        if courses:
            print(f"\n{Fore.CYAN}课程列表：")
            print("-"*80)
            print(f"{'课程编号':<10} {'课程名称':<20} {'学分':<6} {'教师':<10} {'类型':<8}")
            print("-"*80)
            for c in courses:
                print(f"{c['course_id']:<10} {c['course_name']:<20} "
                      f"{c['credits']:<6} {c.get('teacher', ''):<10} {c['course_type']:<8}")
        else:
            print(f"{Fore.YELLOW}暂无课程数据")
        input(f"\n{Fore.GREEN}按回车键返回...")
        
    def add_course(self):
        """添加课程"""
        print(f"\n{Fore.CYAN}添加新课程")
        course_data = {
            'course_id': input("课程编号: "),
            'course_name': input("课程名称: "),
            'credits': float(input("学分: ") or 2.0),
            'teacher': input("授课教师: "),
            'department': input("开课学院: "),
            'semester': input("学期 (如2024-1): "),
            'course_type': input("类型 [必修/选修/实践]: ") or '选修',
            'max_students': int(input("最大人数: ") or 100),
            'classroom': input("上课地点: "),
            'schedule': input("上课时间: ")
        }
        
        if self.course_model.create(course_data):
            print(f"{Fore.GREEN}✓ 课程添加成功")
        else:
            print(f"{Fore.RED}✗ 课程添加失败")
            
    def search_course(self):
        """查询课程"""
        keyword = input("请输入查询关键词（课程编号/名称/教师）: ")
        courses = self.course_model.search(keyword)
        
        if courses:
            print(f"\n{Fore.CYAN}查询结果：")
            for c in courses:
                print(f"编号: {c['course_id']}, 名称: {c['course_name']}, "
                      f"教师: {c.get('teacher', '')}, 学分: {c['credits']}")
        else:
            print(f"{Fore.YELLOW}未找到相关课程")
            
    def update_course(self):
        """修改课程信息"""
        course_id = input("请输入要修改的课程编号: ")
        course = self.course_model.get_by_id(course_id)
        
        if not course:
            print(f"{Fore.RED}课程不存在")
            return
            
        print(f"\n当前信息: {course['course_name']} - {course.get('teacher', '')}")
        update_data = {}
        
        new_classroom = input(f"新教室 [当前: {course.get('classroom', '')}]: ")
        if new_classroom:
            update_data['classroom'] = new_classroom
            
        new_schedule = input(f"新时间 [当前: {course.get('schedule', '')}]: ")
        if new_schedule:
            update_data['schedule'] = new_schedule
            
        if update_data:
            if self.course_model.update(course_id, update_data):
                print(f"{Fore.GREEN}✓ 更新成功")
            else:
                print(f"{Fore.RED}✗ 更新失败")
        else:
            print(f"{Fore.YELLOW}未进行任何修改")
            
    def delete_course(self):
        """删除课程"""
        course_id = input("请输入要删除的课程编号: ")
        confirm = input(f"{Fore.YELLOW}确认删除？(y/n): ")
        
        if confirm.lower() == 'y':
            if self.course_model.delete(course_id):
                print(f"{Fore.GREEN}✓ 删除成功")
            else:
                print(f"{Fore.RED}✗ 删除失败")
                
    # 选课管理具体功能
    def enroll_course(self):
        """学生选课"""
        print(f"\n{Fore.CYAN}学生选课")
        enrollment_data = {
            'student_id': input("学号: "),
            'course_id': input("课程编号: "),
            'semester': input("学期 (如2024-1): ")
        }
        
        if self.enrollment_model.enroll(enrollment_data):
            print(f"{Fore.GREEN}✓ 选课成功")
        else:
            print(f"{Fore.RED}✗ 选课失败")
            
    def drop_course(self):
        """学生退课"""
        print(f"\n{Fore.CYAN}学生退课")
        student_id = input("学号: ")
        course_id = input("课程编号: ")
        semester = input("学期: ")
        
        confirm = input(f"{Fore.YELLOW}确认退课？(y/n): ")
        if confirm.lower() == 'y':
            if self.enrollment_model.drop_course(student_id, course_id, semester):
                print(f"{Fore.GREEN}✓ 退课成功")
            else:
                print(f"{Fore.RED}✗ 退课失败")
                
    def view_student_courses(self):
        """查看学生选课列表"""
        student_id = input("请输入学号: ")
        courses = self.enrollment_model.get_student_courses(student_id)
        
        if courses:
            print(f"\n{Fore.CYAN}选课列表：")
            for c in courses:
                print(f"课程: {c['course_name']}, 学期: {c['semester']}, "
                      f"学分: {c['credits']}, 成绩: {c.get('score', '未录入')}")
        else:
            print(f"{Fore.YELLOW}该学生暂无选课记录")
            
    def view_course_students(self):
        """查看课程选课名单"""
        course_id = input("请输入课程编号: ")
        semester = input("请输入学期: ")
        students = self.enrollment_model.get_course_students(course_id, semester)
        
        if students:
            print(f"\n{Fore.CYAN}选课名单：")
            for s in students:
                print(f"学号: {s['student_id']}, 姓名: {s['name']}, "
                      f"专业: {s['major']}, 成绩: {s.get('score', '未录入')}")
        else:
            print(f"{Fore.YELLOW}该课程暂无选课学生")
            
    # 成绩管理具体功能
    def input_score(self):
        """录入成绩"""
        print(f"\n{Fore.CYAN}录入成绩")
        student_id = input("学号: ")
        course_id = input("课程编号: ")
        semester = input("学期: ")
        score = float(input("成绩 (0-100): "))
        
        if self.enrollment_model.input_score(student_id, course_id, semester, score):
            print(f"{Fore.GREEN}✓ 成绩录入成功")
        else:
            print(f"{Fore.RED}✗ 成绩录入失败")
            
    def view_student_scores(self):
        """查看学生成绩"""
        student_id = input("请输入学号: ")
        scores = self.enrollment_model.get_student_scores(student_id)
        
        if scores:
            print(f"\n{Fore.CYAN}成绩单：")
            total_credits = 0
            total_points = 0
            
            for s in scores:
                print(f"课程: {s['course_name']}, 学期: {s['semester']}, "
                      f"成绩: {s['score']}, 等级: {s.get('grade', '')}")
                total_credits += float(s['credits'])
                total_points += float(s['score']) * float(s['credits'])
                
            if total_credits > 0:
                gpa = total_points / total_credits
                print(f"\n平均绩点: {gpa:.2f}")
        else:
            print(f"{Fore.YELLOW}该学生暂无成绩记录")
            
    def view_course_score_distribution(self):
        """查看课程成绩分布"""
        course_id = input("请输入课程编号: ")
        semester = input("请输入学期: ")
        
        dist = self.enrollment_model.get_course_score_distribution(course_id, semester)
        
        if dist:
            print(f"\n{Fore.CYAN}成绩统计：")
            print(f"选课人数: {dist.get('total', 0)}")
            print(f"平均分: {dist.get('avg_score', 0):.2f}")
            print(f"最高分: {dist.get('max_score', 0)}")
            print(f"最低分: {dist.get('min_score', 0)}")
            
            if 'distribution' in dist:
                print("\n成绩分布:")
                for range_name, count in dist['distribution'].items():
                    print(f"  {range_name}: {count}人")
        else:
            print(f"{Fore.YELLOW}暂无成绩数据")
            
    def cleanup(self):
        """清理资源"""
        if self.db_conn:
            self.db_conn.disconnect()
