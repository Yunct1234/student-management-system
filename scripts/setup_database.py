"""
数据库初始化脚本
"""
import os
import sys
import pymysql
from colorama import init, Fore, Style

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.db_config import DBConfig

init(autoreset=True)

def setup_database():
    """初始化数据库"""
    print(f"{Fore.CYAN}开始初始化数据库...")
    
    # 获取配置
    config = DBConfig.get_local_config()
    
    # 连接数据库（不指定database）
    conn_config = config.copy()
    conn_config.pop('database', None)
    
    try:
        # 连接数据库
        conn = pymysql.connect(**conn_config)
        cursor = conn.cursor()
        
        # 读取SQL文件
        sql_file = os.path.join(os.path.dirname(__file__), '..', 'sql', 'init_db.sql')
        
        with open(sql_file, 'r', encoding='utf-8') as f:
            sql_commands = f.read()
            
        # 分割SQL语句并执行
        statements = sql_commands.split(';')
        
        for statement in statements:
            statement = statement.strip()
            if statement:
                try:
                    cursor.execute(statement)
                    conn.commit()
                    print(f"{Fore.GREEN}✓ 执行成功: {statement[:50]}...")
                except Exception as e:
                    print(f"{Fore.RED}✗ 执行失败: {e}")
                    
        print(f"\n{Fore.GREEN}数据库初始化完成！")
        
        # 设置远程访问权限
        setup_remote = input(f"\n{Fore.YELLOW}是否配置远程访问权限？(y/n): ")
        if setup_remote.lower() == 'y':
            setup_remote_access(cursor, conn)
            
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"{Fore.RED}数据库初始化失败: {e}")
        
def setup_remote_access(cursor, conn):
    """配置远程访问"""
    print(f"\n{Fore.CYAN}配置远程访问权限...")
    
    # 读取远程访问SQL
    sql_file = os.path.join(os.path.dirname(__file__), '..', 'sql', 'setup_remote_access.sql')
    
    with open(sql_file, 'r', encoding='utf-8') as f:
        sql_commands = f.read()
        
    statements = sql_commands.split(';')
    
    for statement in statements:
        statement = statement.strip()
        if statement:
            try:
                cursor.execute(statement)
                conn.commit()
                print(f"{Fore.GREEN}✓ 配置成功")
            except Exception as e:
                print(f"{Fore.YELLOW}⚠ 配置警告: {e}")
                
    print(f"\n{Fore.GREEN}远程访问配置完成！")
    print(f"{Fore.CYAN}远程用户信息：")
    print("  - 用户名: remote_user, 密码: Remote@123")
    print("  - 用户名: readonly_user, 密码: ReadOnly@123")
    print("  - 用户名: admin, 密码: Admin@123")

if __name__ == "__main__":
    setup_database()
