"""
安装配置文件
"""
from setuptools import setup, find_packages

setup(
    name="student_management_system",
    version="1.0.0",
    author="Your Name",
    description="基于OceanBase的学生管理系统",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "pymysql>=1.1.0",
        "cryptography>=41.0.5",
        "python-dotenv>=1.0.0",
        "tabulate>=0.9.0",
        "colorama>=0.4.6",
    ],
    entry_points={
        "console_scripts": [
            "sms-local=client.local_client:main",
            "sms-remote=client.remote_client:main",
        ],
    },
)
