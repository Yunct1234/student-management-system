"""
测试数据库连接脚本
"""
import sys
import os
from colorama import init, Fore

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.db_config import DBConfig
from utils.db_connection import DatabaseConnection

init(autoreset=True)

def test_local_connection():
    """测试本地连接"""
    print(f"{Fore.CYAN}测试本地连接...")
    config = DBConfig.get_local_config()
    
    db = DatabaseConnection(config)
    if db.test_connection():
        print(f"{Fore.GREEN}✓ 本地连接成功")
        
        # 测试查询
        try:
            result = db.execute_query("SELECT COUNT(*) as count FROM students")
            print(f"  学生表记录数: {result[0]['count']}")
        except:
            print(f"{Fore.YELLOW}  数据表可能未初始化")
    else:
        print(f"{Fore.RED}✗ 本地连接失败")
        
    db.disconnect()
    
def test_remote_connection():
    """测试远程连接"""
    print(f"\n{Fore.CYAN}测试远程连接...")
    
    host = input("请输入远程主机IP [默认: 192.168.31.35]: ") or "192.168.31.35"
    config = DBConfig.get_remote_config(host)
    
    db = DatabaseConnection(config)
    if db.test_connection():
        print(f"{Fore.GREEN}✓ 远程连接成功")
    else:
        print(f"{Fore.RED}✗ 远程连接失败")
        
    db.disconnect()

if __name__ == "__main__":
    print(f"{Fore.CYAN}数据库连接测试工具")
    print("="*50)
    
    test_local_connection()
    
    test_remote = input(f"\n{Fore.YELLOW}是否测试远程连接？(y/n): ")
    if test_remote.lower() == 'y':
        test_remote_connection()
        
    print(f"\n{Fore.CYAN}测试完成！")
