# -*- coding: utf-8 -*-
"""
得物研究型实习生 - 一体化AI学者信息平台
推荐系统方向 · 算法策略部

入口文件：应用工厂模式创建 Flask App
"""
import os
import sys

# 确保当前目录在 sys.path 中
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from flask import Flask, render_template
from config import config_map
from extensions import db, cors
from api import register_blueprints
from data.seed import seed_all


def create_app(config_name=None):
    """应用工厂：创建并配置 Flask 应用"""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'default')

    app = Flask(__name__)
    app.config.from_object(config_map.get(config_name, config_map['default']))

    # 初始化扩展
    db.init_app(app)
    cors.init_app(app, resources={r'/api/*': {'origins': '*'}})

    # 数据库初始化（在应用上下文内执行）
    with app.app_context():
        db.create_all()
        seed_all()

    # 注册蓝图
    register_blueprints(app)

    # ---- 路由 ----
    @app.route('/')
    def index():
        return render_template('index.html')

    # ---- 错误处理 ----
    @app.errorhandler(404)
    def not_found(e):
        return {'error': '资源不存在', 'code': 404}, 404

    @app.errorhandler(500)
    def server_error(e):
        return {'error': '服务器内部错误', 'code': 500}, 500

    return app


# ================================================================
# 直接运行入口
# ================================================================
if __name__ == '__main__':
    app = create_app('development')

    print('=' * 60)
    print('  得物研究型实习生 - 一体化AI学者信息平台')
    print('  推荐系统方向 · 算法策略部')
    print('  数据库: SQLite (dewu_research.db)')
    print('=' * 60)
    print('  访问地址: http://localhost:5001')
    print('  API 基础路径: /api/*')
    print('=' * 60)

    app.run(debug=True, host='0.0.0.0', port=5001)
