"""
user.py
用户数据模型 - 包含登录验证、密码加密、操作日志
"""
import hashlib
from typing import Dict, Any, List, Optional
from datetime import datetime
from utils.db_connection import DatabaseConnection


class User:
    """用户模型类"""
    
    def __init__(self, db_connection: DatabaseConnection):
        """初始化用户模型"""
        self.db = db_connection
        self.current_user = None
        
    def _encrypt_password(self, password: str) -> str:
        """MD5加密密码"""
        return hashlib.md5(password.encode()).hexdigest()
        
    def login(self, username: str, password: str) -> Optional[Dict[str, Any]]:
        """
        用户登录验证
        
        Args:
            username: 用户名
            password: 密码（明文）
            
        Returns:
            用户信息字典，失败返回None
        """
        password_hash = self._encrypt_password(password)
        
        query = """
            SELECT user_id, username, password, role, related_id, 
                   real_name, is_active, last_login
            FROM system_users 
            WHERE username = %s AND password = %s
        """
        
        try:
            results = self.db.execute_query(query, (username, password_hash))
            
            if results and results[0]['is_active']:
                self.current_user = results[0]
                # 更新最后登录时间
                self._update_last_login(results[0]['user_id'])
                # 记录登录日志
                self.log_operation("用户登录", "system_users", str(results[0]['user_id']))
                return results[0]
            elif results and not results[0]['is_active']:
                print("账号已被禁用，请联系管理员")
                return None
            else:
                return None
                
        except Exception as e:
            print(f"登录失败: {e}")
            return None
            
    def _update_last_login(self, user_id: int):
        """更新最后登录时间"""
        query = """
            UPDATE system_users 
            SET last_login = NOW(), login_count = login_count + 1
            WHERE user_id = %s
        """
        try:
            self.db.execute_update(query, (user_id,))
        except Exception as e:
            print(f"更新登录时间失败: {e}")
            
    def logout(self):
        """用户登出"""
        if self.current_user:
            self.log_operation("用户登出", "system_users", str(self.current_user['user_id']))
            self.current_user = None
            
    def log_operation(self, operation: str, table_name: str = None, 
                     record_id: str = None, ip_address: str = None):
        """
        记录操作日志
        
        Args:
            operation: 操作描述
            table_name: 操作的表名
            record_id: 操作的记录ID
            ip_address: IP地址
        """
        if not self.current_user:
            return
            
        query = """
            INSERT INTO operation_logs 
            (user_id, username, role, operation, table_name, record_id, ip_address)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        
        try:
            self.db.execute_update(query, (
                self.current_user['user_id'],
                self.current_user['username'],
                self.current_user['role'],
                operation,
                table_name,
                record_id,
                ip_address or 'localhost'
            ))
        except Exception as e:
            print(f"记录日志失败: {e}")
            
    def change_password(self, old_password: str, new_password: str) -> bool:
        """修改密码"""
        if not self.current_user:
            return False
            
        # 验证旧密码
        old_hash = self._encrypt_password(old_password)
        if old_hash != self.current_user['password']:
            print("原密码错误")
            return False
            
        # 更新新密码
        new_hash = self._encrypt_password(new_password)
        query = "UPDATE system_users SET password = %s WHERE user_id = %s"
        
        try:
            result = self.db.execute_update(query, (new_hash, self.current_user['user_id']))
            if result > 0:
                self.log_operation("修改密码", "system_users", str(self.current_user['user_id']))
                return True
            return False
        except Exception as e:
            print(f"修改密码失败: {e}")
            return False
            
    def create_user(self, user_data: Dict[str, Any]) -> bool:
        """创建用户（仅管理员）"""
        if not self.current_user or self.current_user['role'] != 'admin':
            print("权限不足")
            return False
            
        password_hash = self._encrypt_password(user_data.get('password', '123456'))
        
        query = """
            INSERT INTO system_users 
            (username, password, role, related_id, real_name, is_active)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        
        try:
            result = self.db.execute_update(query, (
                user_data['username'],
                password_hash,
                user_data['role'],
                user_data.get('related_id'),
                user_data.get('real_name', ''),
                user_data.get('is_active', True)
            ))
            
            if result > 0:
                self.log_operation(f"创建用户: {user_data['username']}", "system_users")
                return True
            return False
        except Exception as e:
            print(f"创建用户失败: {e}")
            return False
            
    def get_all_users(self) -> List[Dict[str, Any]]:
        """获取所有用户（仅管理员）"""
        if not self.current_user or self.current_user['role'] != 'admin':
            return []
            
        query = """
            SELECT user_id, username, role, related_id, real_name, 
                   is_active, last_login, login_count, created_at
            FROM system_users
            ORDER BY user_id
        """
        
        try:
            return self.db.execute_query(query)
        except Exception as e:
            print(f"查询用户失败: {e}")
            return []
            
    def toggle_user_status(self, user_id: int) -> bool:
        """切换用户启用/禁用状态"""
        if not self.current_user or self.current_user['role'] != 'admin':
            return False
            
        query = """
            UPDATE system_users 
            SET is_active = NOT is_active 
            WHERE user_id = %s AND user_id != %s
        """
        
        try:
            result = self.db.execute_update(query, (user_id, self.current_user['user_id']))
            if result > 0:
                self.log_operation(f"切换用户状态: {user_id}", "system_users", str(user_id))
                return True
            return False
        except Exception as e:
            print(f"切换状态失败: {e}")
            return False
            
    def reset_password(self, user_id: int, new_password: str = '123456') -> bool:
        """重置用户密码（仅管理员）"""
        if not self.current_user or self.current_user['role'] != 'admin':
            return False
            
        password_hash = self._encrypt_password(new_password)
        query = "UPDATE system_users SET password = %s WHERE user_id = %s"
        
        try:
            result = self.db.execute_update(query, (password_hash, user_id))
            if result > 0:
                self.log_operation(f"重置密码: {user_id}", "system_users", str(user_id))
                return True
            return False
        except Exception as e:
            print(f"重置密码失败: {e}")
            return False
            
    def get_operation_logs(self, limit: int = 100, 
                          filters: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """获取操作日志（仅管理员）"""
        if not self.current_user or self.current_user['role'] != 'admin':
            return []
            
        query = """
            SELECT log_id, username, role, operation, table_name, 
                   record_id, ip_address, operation_time
            FROM operation_logs
            WHERE 1=1
        """
        params = []
        
        if filters:
            if filters.get('username'):
                query += " AND username = %s"
                params.append(filters['username'])
            if filters.get('role'):
                query += " AND role = %s"
                params.append(filters['role'])
            if filters.get('date'):
                query += " AND DATE(operation_time) = %s"
                params.append(filters['date'])
                
        query += " ORDER BY operation_time DESC LIMIT %s"
        params.append(limit)
        
        try:
            return self.db.execute_query(query, tuple(params))
        except Exception as e:
            print(f"查询日志失败: {e}")
            return []
            
    def get_role(self) -> str:
        """获取当前用户角色"""
        return self.current_user['role'] if self.current_user else None
        
    def get_related_id(self) -> str:
        """获取关联ID（学号或教师工号）"""
        return self.current_user.get('related_id') if self.current_user else None