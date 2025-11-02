"""
学生管理系统主入口
支持本地和远程客户端模式
"""
import sys
import os
from colorama import init, Fore, Style
from client.unified_client import UnifiedClient
from config.db_config import DBConfig

# 初始化colorama，支持Windows终端颜色
init(autoreset=True)

def print_banner():
    """打印系统横幅"""
    banner = """
    ╔════════════════════════════════════════════╗
    ║     学生管理系统 - OceanBase Edition       ║
    ║         Student Management System          ║
    ╚════════════════════════════════════════════╝
    """
    print(Fore.CYAN + banner)

def main():
    """主函数"""
    print_banner()
    
    print(f"\n{Fore.YELLOW}请选择连接模式：")
    print("1. 本地连接 (localhost)")
    print("2. 远程连接 (需要配置远程服务器)")
    print("0. 退出")
    
    while True:
        choice = input(f"\n{Fore.GREEN}请选择 [0-2]: {Style.RESET_ALL}")
        
        if choice == '0':
            print(f"{Fore.YELLOW}感谢使用，再见！")
            sys.exit(0)
        elif choice == '1':
            # 本地连接
            config = DBConfig.get_local_config()
            client = UnifiedClient(config, mode='local')
            break
        elif choice == '2':
            # 远程连接
            print(f"\n{Fore.YELLOW}远程连接配置")
            host = input("请输入服务器IP地址 [默认: 192.168.31.35]: ").strip() or "192.168.31.35"
            port = input("请输入端口号 [默认: 2881]: ").strip() or "2881"
            user = input("请输入用户名 [默认: remote_user]: ").strip() or "remote_user"
            password = input("请输入密码: ").strip()
            
            config = {
                'host': host,
                'port': int(port),
                'user': user,
                'password': password,
                'database': 'student_management',
                'charset': 'utf8mb4'
            }
            client = UnifiedClient(config, mode='remote')
            break
        else:
            print(f"{Fore.RED}无效选择，请重试")
    
    # 测试连接
    if client.test_connection():
        print(f"{Fore.GREEN}✓ 数据库连接成功！")
        client.run()
    else:
        print(f"{Fore.RED}✗ 数据库连接失败，请检查配置")
        
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}程序被用户中断")
        sys.exit(0)
    except Exception as e:
        print(f"{Fore.RED}发生错误: {e}")
        sys.exit(1)
