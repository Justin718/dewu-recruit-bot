"""
Flask 扩展初始化（单例模式）
使用 init_app 模式，避免循环导入
"""
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

db = SQLAlchemy()
cors = CORS()
