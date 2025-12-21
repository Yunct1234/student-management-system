"""
models包初始化
导出所有模型类
"""
from .student import Student
from .course import Course
from .enrollment import Enrollment
from .user import User

__all__ = ['Student', 'Course', 'Enrollment', 'User']
