"""
role_based_client.py
基于角色的统一客户端实现
支持管理员、教师、学生三种角色
"""
import os
import sys
from typing import Dict, Any, Optional
from colorama import Fore, Style, init
from datetime import datetime

# 初始化colorama
init(autoreset=True)

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import Student, Course, Enrollment, User
from utils import DatabaseConnection


class UnifiedClient:
    """统一客户端类 - 支持角色权限控制"""
    
    def __init__(self, config: Dict[str, Any], mode: str = 'local'):
        """初始化客户端"""
        self.config = config
        self.mode = mode
        self.db_conn = DatabaseConnection(config)
        
        # 初始化数据模型
        self.student_model = Student(self.db_conn)
        self.course_model = Course(self.db_conn)
        self.enrollment_model = Enrollment(self.db_conn)
        self.user_model = User(self.db_conn)
        
    def test_connection(self) -> bool:
        """测试数据库连接"""
        try:
            return self.db_conn.test_connection()
        except Exception as e:
            print(f"{Fore.RED}连接测试失败: {e}")
            return False
            
    def run(self):
        """运行客户端主循环"""
        # 首先进行登录
        if not self._login():
            return
            
        # 根据角色运行对应菜单
        role = self.user_model.get_role()
        
        try:
            if role == 'admin':
                self._run_admin()
            elif role == 'teacher':
                self._run_teacher()
            elif role == 'student':
                self._run_student()
        finally:
            self.cleanup()
            
    def _login(self) -> bool:
        """用户登录"""
        print(f"\n{Fore.CYAN}{'='*50}")
        print(f"{Fore.CYAN}{'用户登录':^46}")
        print(f"{Fore.CYAN}{'='*50}")
        
        print(f"\n{Fore.YELLOW}提示：")
        print("  管理员: admin / admin123")
        print("  教师: teacher1 / teacher123")
        print("  学生: student1 / student123")
        print("-" * 30)
        
        max_attempts = 3
        for attempt in range(max_attempts):
            username = input(f"\n{Fore.GREEN}用户名: {Style.RESET_ALL}").strip()
            password = input(f"{Fore.GREEN}密  码: {Style.RESET_ALL}").strip()
            
            user = self.user_model.login(username, password)
            
            if user:
                role_names = {'admin': '管理员', 'teacher': '教师', 'student': '学生'}
                print(f"\n{Fore.GREEN}✓ 登录成功！")
                print(f"  欢迎, {user.get('real_name', username)} ({role_names.get(user['role'], user['role'])})")
                return True
            else:
                remaining = max_attempts - attempt - 1
                if remaining > 0:
                    print(f"{Fore.RED}✗ 用户名或密码错误，还有 {remaining} 次机会")
                else:
                    print(f"{Fore.RED}✗ 登录失败次数过多，程序退出")
                    
        return False
        
    # ==================== 管理员功能 ====================
    
    def _run_admin(self):
        """管理员主循环"""
        while True:
            self._show_admin_menu()
            choice = input(f"\n{Fore.GREEN}请选择功能 [0-8]: {Style.RESET_ALL}")
            
            if choice == '0':
                print(f"{Fore.YELLOW}感谢使用，再见！")
                break
            elif choice == '1':
                self._admin_student_management()
            elif choice == '2':
                self._admin_course_management()
            elif choice == '3':
                self._admin_enrollment_management()
            elif choice == '4':
                self._admin_score_management()
            elif choice == '5':
                self._admin_user_management()
            elif choice == '6':
                self._show_statistics()
            elif choice == '7':
                self._view_operation_logs()
            elif choice == '8':
                self._change_password()
            else:
                print(f"{Fore.RED}无效选择，请重试")
                
    def _show_admin_menu(self):
        """显示管理员菜单"""
        print(f"\n{Fore.CYAN}{'='*50}")
        print(f"{Fore.CYAN}{'管理员菜单':^46}")
        print(f"{Fore.CYAN}{'='*50}")
        print("1. 学生信息管理")
        print("2. 课程信息管理")
        print("3. 选课管理")
        print("4. 成绩管理")
        print("5. 用户管理")
        print("6. 统计查询")
        print("7. 操作日志")
        print("8. 修改密码")
        print("0. 退出系统")
        
    def _admin_student_management(self):
        """管理员-学生管理"""
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
                self._view_all_students()
            elif choice == '2':
                self._add_student()
            elif choice == '3':
                self._search_student()
            elif choice == '4':
                self._update_student()
            elif choice == '5':
                self._delete_student()
                
    def _admin_course_management(self):
        """管理员-课程管理"""
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
                self._view_all_courses()
            elif choice == '2':
                self._add_course()
            elif choice == '3':
                self._search_course()
            elif choice == '4':
                self._update_course()
            elif choice == '5':
                self._delete_course()
                
    def _admin_enrollment_management(self):
        """管理员-选课管理"""
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
                self._enroll_course()
            elif choice == '2':
                self._drop_course()
            elif choice == '3':
                self._view_student_courses()
            elif choice == '4':
                self._view_course_students()
                
    def _admin_score_management(self):
        """管理员-成绩管理"""
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
                self._input_score()
            elif choice == '2':
                self._view_student_scores()
            elif choice == '3':
                self._view_course_score_distribution()
                
    def _admin_user_management(self):
        """管理员-用户管理"""
        while True:
            print(f"\n{Fore.YELLOW}用户管理")
            print("1. 查看所有用户")
            print("2. 创建用户")
            print("3. 禁用/启用用户")
            print("4. 重置用户密码")
            print("0. 返回主菜单")
            
            choice = input(f"{Fore.GREEN}请选择 [0-4]: {Style.RESET_ALL}")
            
            if choice == '0':
                break
            elif choice == '1':
                self._view_all_users()
            elif choice == '2':
                self._create_user()
            elif choice == '3':
                self._toggle_user_status()
            elif choice == '4':
                self._reset_user_password()
                
    # ==================== 教师功能 ====================
    
    def _run_teacher(self):
        """教师主循环"""
        while True:
            self._show_teacher_menu()
            choice = input(f"\n{Fore.GREEN}请选择功能 [0-6]: {Style.RESET_ALL}")
            
            if choice == '0':
                print(f"{Fore.YELLOW}感谢使用，再见！")
                break
            elif choice == '1':
                self._view_all_students()  # 教师可查看学生
            elif choice == '2':
                self._teacher_my_courses()
            elif choice == '3':
                self._teacher_input_score()
            elif choice == '4':
                self._teacher_view_course_students()
            elif choice == '5':
                self._teacher_score_statistics()
            elif choice == '6':
                self._change_password()
            else:
                print(f"{Fore.RED}无效选择，请重试")
                
    def _show_teacher_menu(self):
        """显示教师菜单"""
        print(f"\n{Fore.CYAN}{'='*50}")
        print(f"{Fore.CYAN}{'教师菜单':^46}")
        print(f"{Fore.CYAN}{'='*50}")
        print("1. 查看学生信息")
        print("2. 我的课程")
        print("3. 成绩录入")
        print("4. 查看选课名单")
        print("5. 成绩统计")
        print("6. 修改密码")
        print("0. 退出系统")
        
    def _teacher_my_courses(self):
        """教师-查看我的课程"""
        teacher_id = self.user_model.get_related_id()
        query = "SELECT * FROM courses WHERE teacher_id = %s ORDER BY course_id"
        
        try:
            courses = self.db_conn.execute_query(query, (teacher_id,))
            if courses:
                print(f"\n{Fore.CYAN}我的课程：")
                print("-" * 70)
                print(f"{'课程编号':<10} {'课程名称':<20} {'学分':<6} {'学期':<10} {'类型':<8}")
                print("-" * 70)
                for c in courses:
                    print(f"{c['course_id']:<10} {c['course_name']:<20} "
                          f"{c['credits']:<6} {c.get('semester', ''):<10} {c['course_type']:<8}")
            else:
                print(f"{Fore.YELLOW}暂无课程")
        except Exception as e:
            print(f"{Fore.RED}查询失败: {e}")
            
        input(f"\n{Fore.GREEN}按回车键返回...")
        
    def _teacher_input_score(self):
        """教师-录入成绩（仅限自己的课程）"""
        teacher_id = self.user_model.get_related_id()
        
        # 显示教师的课程
        query = "SELECT course_id, course_name FROM courses WHERE teacher_id = %s"
        courses = self.db_conn.execute_query(query, (teacher_id,))
        
        if not courses:
            print(f"{Fore.YELLOW}您没有可录入成绩的课程")
            return
            
        print(f"\n{Fore.CYAN}您的课程：")
        for c in courses:
            print(f"  {c['course_id']}: {c['course_name']}")
            
        course_id = input(f"\n{Fore.GREEN}请选择课程编号: {Style.RESET_ALL}").strip()
        
        # 验证是否是教师的课程
        if not any(c['course_id'] == course_id for c in courses):
            print(f"{Fore.RED}您没有权限录入该课程的成绩")
            return
            
        semester = input(f"{Fore.GREEN}请输入学期 (如2024-1): {Style.RESET_ALL}").strip()
        
        # 获取选课学生
        students = self.enrollment_model.get_course_students(course_id, semester)
        
        if not students:
            print(f"{Fore.YELLOW}该课程暂无选课学生")
            return
            
        print(f"\n{Fore.CYAN}选课学生名单：")
        print("-" * 60)
        print(f"{'学号':<12} {'姓名':<10} {'当前成绩':<10} {'等级':<8}")
        print("-" * 60)
        
        for s in students:
            score = s.get('score', '未录入') or '未录入'
            grade = s.get('grade', '-') or '-'
            print(f"{s['student_id']:<12} {s['name']:<10} {str(score):<10} {grade:<8}")
            
        print("-" * 60)
        print(f"{Fore.YELLOW}输入成绩（直接回车跳过，输入q退出）")
        
        for s in students:
            score_input = input(f"{s['student_id']} {s['name']}: {Style.RESET_ALL}").strip()
            
            if score_input.lower() == 'q':
                break
            if not score_input:
                continue
                
            try:
                score = float(score_input)
                if 0 <= score <= 100:
                    if self.enrollment_model.input_score(s['student_id'], course_id, semester, score):
                        self.user_model.log_operation(
                            f"录入成绩: {s['student_id']} - {course_id} - {score}",
                            "enrollments"
                        )
                        print(f"{Fore.GREEN}  ✓ 成绩录入成功")
                    else:
                        print(f"{Fore.RED}  ✗ 成绩录入失败")
                else:
                    print(f"{Fore.RED}  成绩必须在0-100之间")
            except ValueError:
                print(f"{Fore.RED}  请输入有效的数字")
                
    def _teacher_view_course_students(self):
        """教师-查看课程选课名单"""
        teacher_id = self.user_model.get_related_id()
        
        course_id = input(f"{Fore.GREEN}请输入课程编号: {Style.RESET_ALL}").strip()
        
        # 验证权限
        query = "SELECT COUNT(*) as cnt FROM courses WHERE course_id = %s AND teacher_id = %s"
        result = self.db_conn.execute_query(query, (course_id, teacher_id))
        
        if not result or result[0]['cnt'] == 0:
            print(f"{Fore.RED}您没有权限查看该课程")
            return
            
        semester = input(f"{Fore.GREEN}请输入学期: {Style.RESET_ALL}").strip()
        students = self.enrollment_model.get_course_students(course_id, semester)
        
        if students:
            print(f"\n{Fore.CYAN}选课名单：")
            print("-" * 70)
            print(f"{'学号':<12} {'姓名':<10} {'专业':<20} {'成绩':<8} {'等级':<8}")
            print("-" * 70)
            for s in students:
                score = s.get('score', '未录入') or '未录入'
                grade = s.get('grade', '-') or '-'
                print(f"{s['student_id']:<12} {s['name']:<10} {s['major']:<20} "
                      f"{str(score):<8} {grade:<8}")
            print(f"\n共 {len(students)} 人")
        else:
            print(f"{Fore.YELLOW}该课程暂无选课学生")
            
        input(f"\n{Fore.GREEN}按回车键返回...")
        
    def _teacher_score_statistics(self):
        """教师-成绩统计"""
        teacher_id = self.user_model.get_related_id()
        
        course_id = input(f"{Fore.GREEN}请输入课程编号: {Style.RESET_ALL}").strip()
        
        # 验证权限
        query = "SELECT course_name FROM courses WHERE course_id = %s AND teacher_id = %s"
        result = self.db_conn.execute_query(query, (course_id, teacher_id))
        
        if not result:
            print(f"{Fore.RED}您没有权限查看该课程的统计")
            return
            
        course_name = result[0]['course_name']
        semester = input(f"{Fore.GREEN}请输入学期: {Style.RESET_ALL}").strip()
        
        dist = self.enrollment_model.get_course_score_distribution(course_id, semester)
        
        if dist and dist.get('total', 0) > 0:
            print(f"\n{Fore.CYAN}《{course_name}》成绩统计 - {semester}")
            print("=" * 50)
            print(f"选课人数: {dist.get('total', 0)}")
            print(f"平均分: {dist.get('avg_score', 0):.2f}")
            print(f"最高分: {dist.get('max_score', 0)}")
            print(f"最低分: {dist.get('min_score', 0)}")
            
            if 'distribution' in dist:
                print(f"\n{Fore.YELLOW}成绩分布:")
                for range_name, count in sorted(dist['distribution'].items(), reverse=True):
                    bar = '█' * count
                    print(f"  {range_name}: {bar} ({count}人)")
        else:
            print(f"{Fore.YELLOW}暂无成绩数据")
            
        input(f"\n{Fore.GREEN}按回车键返回...")
        
    # ==================== 学生功能 ====================
    
    def _run_student(self):
        """学生主循环"""
        while True:
            self._show_student_menu()
            choice = input(f"\n{Fore.GREEN}请选择功能 [0-6]: {Style.RESET_ALL}")
            
            if choice == '0':
                print(f"{Fore.YELLOW}感谢使用，再见！")
                break
            elif choice == '1':
                self._student_view_info()
            elif choice == '2':
                self._student_view_courses()
            elif choice == '3':
                self._student_enroll_course()
            elif choice == '4':
                self._student_drop_course()
            elif choice == '5':
                self._student_view_scores()
            elif choice == '6':
                self._change_password()
            else:
                print(f"{Fore.RED}无效选择，请重试")
                
    def _show_student_menu(self):
        """显示学生菜单"""
        print(f"\n{Fore.CYAN}{'='*50}")
        print(f"{Fore.CYAN}{'学生菜单':^46}")
        print(f"{Fore.CYAN}{'='*50}")
        print("1. 查看个人信息")
        print("2. 查看已选课程")
        print("3. 选课")
        print("4. 退课")
        print("5. 查看成绩")
        print("6. 修改密码")
        print("0. 退出系统")
        
    def _student_view_info(self):
        """学生-查看个人信息"""
        student_id = self.user_model.get_related_id()
        student = self.student_model.get_by_id(student_id)
        
        if student:
            print(f"\n{Fore.CYAN}个人信息")
            print("=" * 40)
            print(f"学    号: {student['student_id']}")
            print(f"姓    名: {student['name']}")
            print(f"性    别: {student['gender']}")
            print(f"年    龄: {student.get('age', '-')}")
            print(f"专    业: {student['major']}")
            print(f"班    级: {student.get('class_name', '-')}")
            print(f"电    话: {student.get('phone', '-')}")
            print(f"邮    箱: {student.get('email', '-')}")
            print(f"入学日期: {student.get('enrollment_date', '-')}")
            print(f"状    态: {student['status']}")
        else:
            print(f"{Fore.RED}无法获取个人信息")
            
        input(f"\n{Fore.GREEN}按回车键返回...")
        
    def _student_view_courses(self):
        """学生-查看已选课程"""
        student_id = self.user_model.get_related_id()
        courses = self.enrollment_model.get_student_courses(student_id)
        
        if courses:
            print(f"\n{Fore.CYAN}已选课程：")
            print("-" * 80)
            print(f"{'课程编号':<10} {'课程名称':<20} {'学分':<6} {'教师':<10} {'学期':<10} {'成绩':<8}")
            print("-" * 80)
            
            total_credits = 0
            for c in courses:
                score = c.get('score', '未出') or '未出'
                print(f"{c['course_id']:<10} {c['course_name']:<20} {c['credits']:<6} "
                      f"{c.get('teacher', '-'):<10} {c['semester']:<10} {str(score):<8}")
                total_credits += float(c['credits'])
                
            print("-" * 80)
            print(f"共 {len(courses)} 门课程，总学分: {total_credits}")
        else:
            print(f"{Fore.YELLOW}暂无选课记录")
            
        input(f"\n{Fore.GREEN}按回车键返回...")
        
    def _student_enroll_course(self):
        """学生-选课"""
        student_id = self.user_model.get_related_id()
        
        semester = input(f"{Fore.GREEN}请输入学期 (如2024-1): {Style.RESET_ALL}").strip()
        
        # 获取可选课程
        available = self.course_model.get_available_courses(semester)
        
        if not available:
            print(f"{Fore.YELLOW}当前学期暂无可选课程")
            return
            
        print(f"\n{Fore.CYAN}可选课程列表：")
        print("-" * 80)
        print(f"{'编号':<10} {'课程名称':<20} {'学分':<6} {'教师':<10} {'已选/容量':<12}")
        print("-" * 80)
        
        for c in available:
            enrolled = c.get('enrolled_count', 0)
            max_stu = c.get('max_students', 100)
            print(f"{c['course_id']:<10} {c['course_name']:<20} {c['credits']:<6} "
                  f"{c.get('teacher', '-'):<10} {enrolled}/{max_stu:<12}")
                  
        print("-" * 80)
        
        course_id = input(f"\n{Fore.GREEN}请输入要选的课程编号 (0取消): {Style.RESET_ALL}").strip()
        
        if course_id == '0':
            return
            
        enrollment_data = {
            'student_id': student_id,
            'course_id': course_id,
            'semester': semester
        }
        
        if self.enrollment_model.enroll(enrollment_data):
            self.user_model.log_operation(f"选课: {course_id}", "enrollments")
            print(f"{Fore.GREEN}✓ 选课成功")
        else:
            print(f"{Fore.RED}✗ 选课失败")
            
    def _student_drop_course(self):
        """学生-退课"""
        student_id = self.user_model.get_related_id()
        
        # 显示已选课程
        courses = self.enrollment_model.get_student_courses(student_id)
        
        if not courses:
            print(f"{Fore.YELLOW}暂无可退选的课程")
            return
            
        print(f"\n{Fore.CYAN}已选课程：")
        for c in courses:
            print(f"  {c['course_id']}: {c['course_name']} ({c['semester']})")
            
        course_id = input(f"\n{Fore.GREEN}请输入要退选的课程编号: {Style.RESET_ALL}").strip()
        semester = input(f"{Fore.GREEN}请输入学期: {Style.RESET_ALL}").strip()
        
        confirm = input(f"{Fore.YELLOW}确认退选？(y/n): {Style.RESET_ALL}")
        
        if confirm.lower() == 'y':
            if self.enrollment_model.drop_course(student_id, course_id, semester):
                self.user_model.log_operation(f"退课: {course_id}", "enrollments")
                print(f"{Fore.GREEN}✓ 退课成功")
            else:
                print(f"{Fore.RED}✗ 退课失败")
                
    def _student_view_scores(self):
        """学生-查看成绩"""
        student_id = self.user_model.get_related_id()
        scores = self.enrollment_model.get_student_scores(student_id)
        
        if scores:
            print(f"\n{Fore.CYAN}成绩单")
            print("=" * 70)
            print(f"{'课程编号':<10} {'课程名称':<20} {'学分':<6} {'成绩':<8} {'等级':<8} {'学期':<10}")
            print("-" * 70)
            
            total_credits = 0
            total_points = 0
            
            for s in scores:
                print(f"{s['course_id']:<10} {s['course_name']:<20} {s['credits']:<6} "
                      f"{s['score']:<8} {s.get('grade', '-'):<8} {s['semester']:<10}")
                total_credits += float(s['credits'])
                total_points += float(s['score']) * float(s['credits'])
                
            print("=" * 70)
            
            if total_credits > 0:
                gpa = total_points / total_credits
                print(f"总学分: {total_credits}  加权平均分: {gpa:.2f}")
        else:
            print(f"{Fore.YELLOW}暂无成绩记录")
            
        input(f"\n{Fore.GREEN}按回车键返回...")
        
    # ==================== 通用功能 ====================
    
    def _view_all_students(self):
        """查看所有学生"""
        students = self.student_model.get_all()
        if students:
            print(f"\n{Fore.CYAN}学生列表：")
            print("-" * 90)
            print(f"{'学号':<12} {'姓名':<10} {'性别':<6} {'专业':<20} {'班级':<15} {'状态':<8}")
            print("-" * 90)
            for s in students:
                print(f"{s['student_id']:<12} {s['name']:<10} {s['gender']:<6} "
                      f"{s['major']:<20} {s.get('class_name', '-'):<15} {s['status']:<8}")
            print(f"\n共 {len(students)} 名学生")
        else:
            print(f"{Fore.YELLOW}暂无学生数据")
        input(f"\n{Fore.GREEN}按回车键返回...")
        
    def _add_student(self):
        """添加学生"""
        print(f"\n{Fore.CYAN}添加新学生")
        print("-" * 40)
        
        student_data = {
            'student_id': input("学号: ").strip(),
            'name': input("姓名: ").strip(),
            'gender': input("性别 [男/女]: ").strip() or '男',
            'age': int(input("年龄 [18]: ").strip() or 18),
            'major': input("专业: ").strip(),
            'class_name': input("班级: ").strip(),
            'phone': input("电话: ").strip(),
            'email': input("邮箱: ").strip(),
            'enrollment_date': datetime.now().strftime('%Y-%m-%d')
        }
        
        if self.student_model.create(student_data):
            self.user_model.log_operation(f"添加学生: {student_data['student_id']}", "students")
            print(f"{Fore.GREEN}✓ 学生添加成功")
            
            # 询问是否创建账号
            create_account = input(f"\n{Fore.YELLOW}是否为该学生创建系统账号？(y/n): {Style.RESET_ALL}")
            if create_account.lower() == 'y':
                user_data = {
                    'username': f"stu_{student_data['student_id']}",
                    'password': '123456',
                    'role': 'student',
                    'related_id': student_data['student_id'],
                    'real_name': student_data['name']
                }
                if self.user_model.create_user(user_data):
                    print(f"{Fore.GREEN}✓ 账号创建成功")
                    print(f"  用户名: {user_data['username']}")
                    print(f"  初始密码: 123456")
        else:
            print(f"{Fore.RED}✗ 学生添加失败")
            
    def _search_student(self):
        """查询学生"""
        keyword = input("请输入查询关键词（学号/姓名/专业）: ").strip()
        students = self.student_model.search(keyword=keyword)
        
        if students:
            print(f"\n{Fore.CYAN}查询结果：")
            print("-" * 70)
            for s in students:
                print(f"学号: {s['student_id']}, 姓名: {s['name']}, "
                      f"专业: {s['major']}, 班级: {s.get('class_name', '-')}, 状态: {s['status']}")
            print(f"\n共找到 {len(students)} 条记录")
        else:
            print(f"{Fore.YELLOW}未找到相关学生")
            
        input(f"\n{Fore.GREEN}按回车键返回...")
        
    def _update_student(self):
        """修改学生信息"""
        student_id = input("请输入要修改的学号: ").strip()
        student = self.student_model.get_by_id(student_id)
        
        if not student:
            print(f"{Fore.RED}学生不存在")
            return
            
        print(f"\n当前信息: {student['name']} - {student['major']} - {student.get('class_name', '-')}")
        print(f"{Fore.YELLOW}(直接回车表示不修改)")
        
        update_data = {}
        
        new_phone = input(f"新电话 [{student.get('phone', '')}]: ").strip()
        if new_phone:
            update_data['phone'] = new_phone
            
        new_email = input(f"新邮箱 [{student.get('email', '')}]: ").strip()
        if new_email:
            update_data['email'] = new_email
            
        new_status = input(f"新状态 [{student['status']}] (在读/休学/退学/毕业): ").strip()
        if new_status:
            update_data['status'] = new_status
            
        if update_data:
            if self.student_model.update(student_id, update_data):
                self.user_model.log_operation(f"修改学生: {student_id}", "students", student_id)
                print(f"{Fore.GREEN}✓ 更新成功")
            else:
                print(f"{Fore.RED}✗ 更新失败")
        else:
            print(f"{Fore.YELLOW}未进行任何修改")
            
    def _delete_student(self):
        """删除学生"""
        student_id = input("请输入要删除的学号: ").strip()
        student = self.student_model.get_by_id(student_id)
        
        if not student:
            print(f"{Fore.RED}学生不存在")
            return
            
        print(f"\n将删除: {student['name']} ({student['student_id']}) - {student['major']}")
        confirm = input(f"{Fore.YELLOW}确认删除？此操作不可恢复！(yes/no): {Style.RESET_ALL}")
        
        if confirm.lower() == 'yes':
            if self.student_model.delete(student_id):
                self.user_model.log_operation(f"删除学生: {student_id} - {student['name']}", "students", student_id)
                print(f"{Fore.GREEN}✓ 删除成功")
            else:
                print(f"{Fore.RED}✗ 删除失败")
        else:
            print(f"{Fore.YELLOW}已取消删除")
            
    def _view_all_courses(self):
        """查看所有课程"""
        courses = self.course_model.get_all()
        if courses:
            print(f"\n{Fore.CYAN}课程列表：")
            print("-" * 90)
            print(f"{'课程编号':<10} {'课程名称':<20} {'学分':<6} {'教师':<10} {'类型':<8} {'学期':<10}")
            print("-" * 90)
            for c in courses:
                print(f"{c['course_id']:<10} {c['course_name']:<20} "
                      f"{c['credits']:<6} {c.get('teacher', '-'):<10} "
                      f"{c['course_type']:<8} {c.get('semester', '-'):<10}")
            print(f"\n共 {len(courses)} 门课程")
        else:
            print(f"{Fore.YELLOW}暂无课程数据")
        input(f"\n{Fore.GREEN}按回车键返回...")
        
    def _add_course(self):
        """添加课程"""
        print(f"\n{Fore.CYAN}添加新课程")
        print("-" * 40)
        
        course_data = {
            'course_id': input("课程编号: ").strip(),
            'course_name': input("课程名称: ").strip(),
            'credits': float(input("学分 [2.0]: ").strip() or 2.0),
            'teacher': input("授课教师: ").strip(),
            'department': input("开课学院: ").strip(),
            'semester': input("学期 (如2024-1): ").strip(),
            'course_type': input("类型 [必修/选修/实践]: ").strip() or '选修',
            'max_students': int(input("最大人数 [100]: ").strip() or 100),
            'classroom': input("上课地点: ").strip(),
            'schedule': input("上课时间: ").strip()
        }
        
        if self.course_model.create(course_data):
            self.user_model.log_operation(f"添加课程: {course_data['course_id']}", "courses")
            print(f"{Fore.GREEN}✓ 课程添加成功")
        else:
            print(f"{Fore.RED}✗ 课程添加失败")
            
    def _search_course(self):
        """查询课程"""
        keyword = input("请输入查询关键词（课程编号/名称/教师）: ").strip()
        courses = self.course_model.search(keyword)
        
        if courses:
            print(f"\n{Fore.CYAN}查询结果：")
            print("-" * 70)
            for c in courses:
                print(f"编号: {c['course_id']}, 名称: {c['course_name']}, "
                      f"教师: {c.get('teacher', '-')}, 学分: {c['credits']}, 类型: {c['course_type']}")
            print(f"\n共找到 {len(courses)} 条记录")
        else:
            print(f"{Fore.YELLOW}未找到相关课程")
            
        input(f"\n{Fore.GREEN}按回车键返回...")
        
    def _update_course(self):
        """修改课程信息"""
        course_id = input("请输入要修改的课程编号: ").strip()
        course = self.course_model.get_by_id(course_id)
        
        if not course:
            print(f"{Fore.RED}课程不存在")
            return
            
        print(f"\n当前信息: {course['course_name']} - {course.get('teacher', '-')}")
        print(f"{Fore.YELLOW}(直接回车表示不修改)")
        
        update_data = {}
        
        new_classroom = input(f"新教室 [{course.get('classroom', '')}]: ").strip()
        if new_classroom:
            update_data['classroom'] = new_classroom
            
        new_schedule = input(f"新时间 [{course.get('schedule', '')}]: ").strip()
        if new_schedule:
            update_data['schedule'] = new_schedule
            
        new_max = input(f"新容量 [{course.get('max_students', 100)}]: ").strip()
        if new_max:
            update_data['max_students'] = int(new_max)
            
        if update_data:
            if self.course_model.update(course_id, update_data):
                self.user_model.log_operation(f"修改课程: {course_id}", "courses", course_id)
                print(f"{Fore.GREEN}✓ 更新成功")
            else:
                print(f"{Fore.RED}✗ 更新失败")
        else:
            print(f"{Fore.YELLOW}未进行任何修改")
            
    def _delete_course(self):
        """删除课程"""
        course_id = input("请输入要删除的课程编号: ").strip()
        course = self.course_model.get_by_id(course_id)
        
        if not course:
            print(f"{Fore.RED}课程不存在")
            return
            
        print(f"\n将删除: {course['course_name']} ({course_id})")
        confirm = input(f"{Fore.YELLOW}确认删除？此操作不可恢复！(yes/no): {Style.RESET_ALL}")
        
        if confirm.lower() == 'yes':
            if self.course_model.delete(course_id):
                self.user_model.log_operation(f"删除课程: {course_id}", "courses", course_id)
                print(f"{Fore.GREEN}✓ 删除成功")
            else:
                print(f"{Fore.RED}✗ 删除失败")
        else:
            print(f"{Fore.YELLOW}已取消删除")
            
    def _enroll_course(self):
        """学生选课（管理员操作）"""
        print(f"\n{Fore.CYAN}学生选课")
        enrollment_data = {
            'student_id': input("学号: ").strip(),
            'course_id': input("课程编号: ").strip(),
            'semester': input("学期 (如2024-1): ").strip()
        }
        
        if self.enrollment_model.enroll(enrollment_data):
            self.user_model.log_operation(
                f"选课: {enrollment_data['student_id']} - {enrollment_data['course_id']}", 
                "enrollments"
            )
            print(f"{Fore.GREEN}✓ 选课成功")
        else:
            print(f"{Fore.RED}✗ 选课失败")
            
    def _drop_course(self):
        """学生退课（管理员操作）"""
        print(f"\n{Fore.CYAN}学生退课")
        student_id = input("学号: ").strip()
        course_id = input("课程编号: ").strip()
        semester = input("学期: ").strip()
        
        confirm = input(f"{Fore.YELLOW}确认退课？(y/n): {Style.RESET_ALL}")
        if confirm.lower() == 'y':
            if self.enrollment_model.drop_course(student_id, course_id, semester):
                self.user_model.log_operation(f"退课: {student_id} - {course_id}", "enrollments")
                print(f"{Fore.GREEN}✓ 退课成功")
            else:
                print(f"{Fore.RED}✗ 退课失败")
                
    def _view_student_courses(self):
        """查看学生选课列表"""
        student_id = input("请输入学号: ").strip()
        
        student = self.student_model.get_by_id(student_id)
        if not student:
            print(f"{Fore.RED}学生不存在")
            return
            
        courses = self.enrollment_model.get_student_courses(student_id)
        
        print(f"\n{Fore.CYAN}{student['name']} ({student_id}) 的选课列表：")
        
        if courses:
            print("-" * 70)
            print(f"{'课程编号':<10} {'课程名称':<20} {'学分':<6} {'学期':<10} {'成绩':<8}")
            print("-" * 70)
            for c in courses:
                score = c.get('score', '未录入') or '未录入'
                print(f"{c['course_id']:<10} {c['course_name']:<20} {c['credits']:<6} "
                      f"{c['semester']:<10} {str(score):<8}")
        else:
            print(f"{Fore.YELLOW}该学生暂无选课记录")
            
        input(f"\n{Fore.GREEN}按回车键返回...")
        
    def _view_course_students(self):
        """查看课程选课名单"""
        course_id = input("请输入课程编号: ").strip()
        semester = input("请输入学期: ").strip()
        
        course = self.course_model.get_by_id(course_id)
        if not course:
            print(f"{Fore.RED}课程不存在")
            return
            
        students = self.enrollment_model.get_course_students(course_id, semester)
        
        print(f"\n{Fore.CYAN}《{course['course_name']}》选课名单 - {semester}")
        
        if students:
            print("-" * 80)
            print(f"{'学号':<12} {'姓名':<10} {'专业':<20} {'班级':<15} {'成绩':<8}")
            print("-" * 80)
            for s in students:
                score = s.get('score', '未录入') or '未录入'
                print(f"{s['student_id']:<12} {s['name']:<10} {s['major']:<20} "
                      f"{s.get('class_name', '-'):<15} {str(score):<8}")
            print(f"\n共 {len(students)} 人选课")
        else:
            print(f"{Fore.YELLOW}该课程暂无选课学生")
            
        input(f"\n{Fore.GREEN}按回车键返回...")
        
    def _input_score(self):
        """录入成绩（管理员）"""
        print(f"\n{Fore.CYAN}成绩录入")
        
        course_id = input("课程编号: ").strip()
        semester = input("学期: ").strip()
        
        # 获取选课学生
        students = self.enrollment_model.get_course_students(course_id, semester)
        
        if not students:
            print(f"{Fore.YELLOW}该课程暂无选课学生")
            return
            
        print(f"\n{Fore.CYAN}选课学生名单：")
        print("-" * 60)
        print(f"{'学号':<12} {'姓名':<10} {'当前成绩':<10} {'等级':<8}")
        print("-" * 60)
        
        for s in students:
            score = s.get('score', '未录入') or '未录入'
            grade = s.get('grade', '-') or '-'
            print(f"{s['student_id']:<12} {s['name']:<10} {str(score):<10} {grade:<8}")
            
        print("-" * 60)
        print(f"{Fore.YELLOW}输入成绩（直接回车跳过，输入q退出）")
        
        for s in students:
            score_input = input(f"{s['student_id']} {s['name']}: {Style.RESET_ALL}").strip()
            
            if score_input.lower() == 'q':
                break
            if not score_input:
                continue
                
            try:
                score = float(score_input)
                if 0 <= score <= 100:
                    if self.enrollment_model.input_score(s['student_id'], course_id, semester, score):
                        self.user_model.log_operation(
                            f"录入成绩: {s['student_id']} - {course_id} - {score}",
                            "enrollments"
                        )
                        print(f"{Fore.GREEN}  ✓ 成绩录入成功")
                    else:
                        print(f"{Fore.RED}  ✗ 成绩录入失败")
                else:
                    print(f"{Fore.RED}  成绩必须在0-100之间")
            except ValueError:
                print(f"{Fore.RED}  请输入有效的数字")
                
    def _view_student_scores(self):
        """查看学生成绩"""
        student_id = input("请输入学号: ").strip()
        
        student = self.student_model.get_by_id(student_id)
        if not student:
            print(f"{Fore.RED}学生不存在")
            return
            
        scores = self.enrollment_model.get_student_scores(student_id)
        
        print(f"\n{Fore.CYAN}{student['name']} ({student_id}) 成绩单")
        
        if scores:
            print("=" * 80)
            print(f"{'课程编号':<10} {'课程名称':<20} {'学分':<6} {'成绩':<8} {'等级':<8} {'学期':<10}")
            print("-" * 80)
            
            total_credits = 0
            total_points = 0
            
            for s in scores:
                print(f"{s['course_id']:<10} {s['course_name']:<20} {s['credits']:<6} "
                      f"{s['score']:<8} {s.get('grade', '-'):<8} {s['semester']:<10}")
                total_credits += float(s['credits'])
                total_points += float(s['score']) * float(s['credits'])
                
            print("=" * 80)
            if total_credits > 0:
                gpa = total_points / total_credits
                print(f"总学分: {total_credits}  加权平均分: {gpa:.2f}")
        else:
            print(f"{Fore.YELLOW}暂无成绩记录")
            
        input(f"\n{Fore.GREEN}按回车键返回...")
        
    def _view_course_score_distribution(self):
        """查看课程成绩分布"""
        course_id = input("请输入课程编号: ").strip()
        semester = input("请输入学期: ").strip()
        
        course = self.course_model.get_by_id(course_id)
        if not course:
            print(f"{Fore.RED}课程不存在")
            return
            
        dist = self.enrollment_model.get_course_score_distribution(course_id, semester)
        
        print(f"\n{Fore.CYAN}《{course['course_name']}》成绩分布 - {semester}")
        
        if dist and dist.get('total', 0) > 0:
            print("=" * 50)
            print(f"选课人数: {dist.get('total', 0)}")
            print(f"平均分: {dist.get('avg_score', 0):.2f}")
            print(f"最高分: {dist.get('max_score', 0)}")
            print(f"最低分: {dist.get('min_score', 0)}")
            
            if 'distribution' in dist:
                print(f"\n{Fore.YELLOW}分数段分布:")
                for range_name, count in sorted(dist['distribution'].items(), reverse=True):
                    bar = '█' * count + '░' * (20 - count)
                    percentage = count / dist.get('total', 1) * 100
                    print(f"  {range_name}: {bar} {count}人 ({percentage:.1f}%)")
        else:
            print(f"{Fore.YELLOW}暂无成绩数据")
            
        input(f"\n{Fore.GREEN}按回车键返回...")
        
    def _show_statistics(self):
        """显示统计信息"""
        while True:
            print(f"\n{Fore.YELLOW}统计查询")
            print("1. 学生统计")
            print("2. 课程统计")
            print("3. 选课统计")
            print("4. 成绩统计")
            print("0. 返回主菜单")
            
            choice = input(f"{Fore.GREEN}请选择 [0-4]: {Style.RESET_ALL}")
            
            if choice == '0':
                break
            elif choice == '1':
                self._show_student_statistics()
            elif choice == '2':
                self._show_course_statistics()
            elif choice == '3':
                self._show_enrollment_statistics()
            elif choice == '4':
                self._show_score_statistics()
                
    def _show_student_statistics(self):
        """学生统计"""
        stats = self.student_model.get_statistics()
        
        print(f"\n{Fore.CYAN}学生统计")
        print("=" * 50)
        print(f"学生总数: {stats.get('total_students', 0)}")
        
        if 'by_status' in stats:
            print(f"\n{Fore.YELLOW}按状态分布:")
            for status, count in stats['by_status'].items():
                print(f"  {status}: {count}")
                
        if 'by_major' in stats:
            print(f"\n{Fore.YELLOW}按专业分布:")
            for major, count in stats['by_major'].items():
                print(f"  {major}: {count}")
                
        if 'by_gender' in stats:
            print(f"\n{Fore.YELLOW}按性别分布:")
            for gender, count in stats['by_gender'].items():
                print(f"  {gender}: {count}")
                
        input(f"\n{Fore.GREEN}按回车键返回...")
        
    def _show_course_statistics(self):
        """课程统计"""
        stats = self.course_model.get_statistics()
        
        print(f"\n{Fore.CYAN}课程统计")
        print("=" * 50)
        print(f"课程总数: {stats.get('total_courses', 0)}")
        
        if 'by_type' in stats:
            print(f"\n{Fore.YELLOW}按类型分布:")
            for type_name, count in stats['by_type'].items():
                print(f"  {type_name}: {count}")
                
        if 'by_semester' in stats:
            print(f"\n{Fore.YELLOW}按学期分布:")
            for semester, count in stats['by_semester'].items():
                print(f"  {semester}: {count}")
                
        if 'by_department' in stats:
            print(f"\n{Fore.YELLOW}按学院分布:")
            for dept, count in stats['by_department'].items():
                print(f"  {dept}: {count}")
                
        input(f"\n{Fore.GREEN}按回车键返回...")
        
    def _show_enrollment_statistics(self):
        """选课统计"""
        stats = self.enrollment_model.get_statistics()
        
        print(f"\n{Fore.CYAN}选课统计")
        print("=" * 50)
        print(f"选课记录总数: {stats.get('total_enrollments', 0)}")
        
        if 'popular_courses' in stats and stats['popular_courses']:
            print(f"\n{Fore.YELLOW}热门课程 TOP 10:")
            for i, course in enumerate(stats['popular_courses'][:10], 1):
                print(f"  {i}. {course['course_name']}: {course['count']}人")
                
        if 'student_course_count' in stats:
            print(f"\n{Fore.YELLOW}学生选课数分布:")
            for count, students in sorted(stats['student_course_count'].items()):
                print(f"  选{count}门课: {students}人")
                
        input(f"\n{Fore.GREEN}按回车键返回...")
        
    def _show_score_statistics(self):
        """成绩统计"""
        semester = input("请输入学期 (回车查看全部): ").strip() or None
        stats = self.enrollment_model.get_score_statistics(semester)
        
        print(f"\n{Fore.CYAN}成绩统计")
        print("=" * 50)
        print(f"成绩记录数: {stats.get('total_scores', 0)}")
        
        if stats.get('overall_avg'):
            print(f"整体平均分: {stats['overall_avg']:.2f}")
            
        if 'grade_distribution' in stats:
            print(f"\n{Fore.YELLOW}等级分布:")
            for grade, count in stats['grade_distribution'].items():
                print(f"  {grade}: {count}")
                
        if 'failed_students' in stats and stats['failed_students']:
            print(f"\n{Fore.RED}不及格学生:")
            for s in stats['failed_students'][:10]:
                print(f"  {s['student_id']}: {s['name']}")
            if len(stats['failed_students']) > 10:
                print(f"  ... 共 {len(stats['failed_students'])} 人")
                
        input(f"\n{Fore.GREEN}按回车键返回...")
        
    def _view_all_users(self):
        """查看所有用户"""
        users = self.user_model.get_all_users()
        
        if users:
            print(f"\n{Fore.CYAN}系统用户列表：")
            print("-" * 90)
            print(f"{'ID':<6} {'用户名':<15} {'角色':<10} {'关联ID':<12} {'真实姓名':<10} "
                  f"{'状态':<8} {'登录次数':<8}")
            print("-" * 90)
            
            role_names = {'admin': '管理员', 'teacher': '教师', 'student': '学生'}
            
            for u in users:
                status = '启用' if u['is_active'] else '禁用'
                role = role_names.get(u['role'], u['role'])
                print(f"{u['user_id']:<6} {u['username']:<15} {role:<10} "
                      f"{u.get('related_id', '-') or '-':<12} {u.get('real_name', '-') or '-':<10} "
                      f"{status:<8} {u.get('login_count', 0):<8}")
                      
            print(f"\n共 {len(users)} 个用户")
        else:
            print(f"{Fore.YELLOW}暂无用户数据")
            
        input(f"\n{Fore.GREEN}按回车键返回...")
        
    def _create_user(self):
        """创建用户"""
        print(f"\n{Fore.CYAN}创建新用户")
        print("-" * 40)
        
        user_data = {
            'username': input("用户名: ").strip(),
            'password': input("密码 [123456]: ").strip() or '123456',
            'role': input("角色 (admin/teacher/student): ").strip(),
            'related_id': input("关联ID (学号或教师工号，可选): ").strip() or None,
            'real_name': input("真实姓名: ").strip()
        }
        
        if user_data['role'] not in ['admin', 'teacher', 'student']:
            print(f"{Fore.RED}无效的角色类型")
            return
            
        if self.user_model.create_user(user_data):
            print(f"{Fore.GREEN}✓ 用户创建成功")
            print(f"  用户名: {user_data['username']}")
            print(f"  初始密码: {user_data['password']}")
        else:
            print(f"{Fore.RED}✗ 用户创建失败")
            
    def _toggle_user_status(self):
        """切换用户状态"""
        # 先显示用户列表
        self._view_all_users()
        
        user_id = input(f"\n{Fore.GREEN}请输入要切换状态的用户ID: {Style.RESET_ALL}").strip()
        
        try:
            user_id = int(user_id)
            if self.user_model.toggle_user_status(user_id):
                print(f"{Fore.GREEN}✓ 用户状态已切换")
            else:
                print(f"{Fore.RED}✗ 操作失败（可能是试图禁用自己或用户不存在）")
        except ValueError:
            print(f"{Fore.RED}请输入有效的用户ID")
            
    def _reset_user_password(self):
        """重置用户密码"""
        user_id = input("请输入用户ID: ").strip()
        new_password = input("新密码 [123456]: ").strip() or '123456'
        
        try:
            user_id = int(user_id)
            if self.user_model.reset_password(user_id, new_password):
                print(f"{Fore.GREEN}✓ 密码重置成功，新密码: {new_password}")
            else:
                print(f"{Fore.RED}✗ 密码重置失败")
        except ValueError:
            print(f"{Fore.RED}请输入有效的用户ID")
            
    def _view_operation_logs(self):
        """查看操作日志"""
        print(f"\n{Fore.YELLOW}日志查询条件（直接回车跳过）")
        
        filters = {}
        username = input("用户名: ").strip()
        if username:
            filters['username'] = username
            
        role = input("角色 (admin/teacher/student): ").strip()
        if role:
            filters['role'] = role
            
        date = input("日期 (YYYY-MM-DD): ").strip()
        if date:
            filters['date'] = date
            
        limit = input("显示条数 [50]: ").strip()
        limit = int(limit) if limit else 50
        
        logs = self.user_model.get_operation_logs(limit, filters if filters else None)
        
        if logs:
            print(f"\n{Fore.CYAN}操作日志：")
            print("-" * 100)
            print(f"{'时间':<20} {'用户':<12} {'角色':<8} {'操作':<30} {'表':<15} {'记录ID':<10}")
            print("-" * 100)
            
            role_names = {'admin': '管理员', 'teacher': '教师', 'student': '学生'}
            
            for log in logs:
                time_str = log['operation_time'].strftime('%Y-%m-%d %H:%M:%S') if log['operation_time'] else '-'
                role = role_names.get(log['role'], log['role'] or '-')
                print(f"{time_str:<20} {log['username']:<12} {role:<8} "
                      f"{log['operation'][:28]:<30} {log.get('table_name', '-') or '-':<15} "
                      f"{log.get('record_id', '-') or '-':<10}")
                      
            print(f"\n共 {len(logs)} 条日志")
        else:
            print(f"{Fore.YELLOW}暂无操作日志")
            
        input(f"\n{Fore.GREEN}按回车键返回...")
        
    def _change_password(self):
        """修改密码"""
        print(f"\n{Fore.CYAN}修改密码")
        print("-" * 40)
        
        old_password = input("请输入原密码: ").strip()
        new_password = input("请输入新密码: ").strip()
        confirm_password = input("请确认新密码: ").strip()
        
        if new_password != confirm_password:
            print(f"{Fore.RED}两次输入的密码不一致")
            return
            
        if len(new_password) < 6:
            print(f"{Fore.RED}密码长度至少6位")
            return
            
        if self.user_model.change_password(old_password, new_password):
            print(f"{Fore.GREEN}✓ 密码修改成功，下次登录请使用新密码")
        else:
            print(f"{Fore.RED}✗ 密码修改失败，请检查原密码是否正确")
            
    def cleanup(self):
        """清理资源"""
        self.user_model.logout()
        self.db_conn.disconnect()
        print(f"{Fore.GREEN}已安全退出系统")


# ==================== 主入口 ====================

def main():
    db_config = {
        'host': '127.0.0.1',
        'port': 2881,
        'user': 'root@test',
        'password': '',
        'database': 'student_management',
        'charset': 'utf8mb4'
    }

    
    print(f"\n{Fore.CYAN}{'='*60}")
    print(f"{Fore.CYAN}{'学生信息管理系统 v2.0':^56}")
    print(f"{Fore.CYAN}{'基于角色的权限控制版本':^56}")
    print(f"{Fore.CYAN}{'='*60}")
    
    # 创建客户端并运行
    client = UnifiedClient(db_config)
    
    # 测试连接
    print(f"\n{Fore.YELLOW}正在连接数据库...")
    if client.test_connection():
        print(f"{Fore.GREEN}✓ 数据库连接成功")
        client.run()
    else:
        print(f"{Fore.RED}✗ 数据库连接失败，请检查配置")
        

if __name__ == '__main__':
    main()
