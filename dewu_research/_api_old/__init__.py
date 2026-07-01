# -*- coding: utf-8 -*-
"""API - 统一注册所有 Blueprint"""
from .dashboard import dashboard_bp
from .projects import projects_bp
from .architecture import architecture_bp
from .knowledge import knowledge_bp
from .feishu import feishu_bp
from .profile import profile_bp


def register_blueprints(app):
    """在 Flask 应用上注册全部蓝图"""
    app.register_blueprint(dashboard_bp, url_prefix='/api')
    app.register_blueprint(projects_bp, url_prefix='/api')
    app.register_blueprint(architecture_bp, url_prefix='/api')
    app.register_blueprint(knowledge_bp, url_prefix='/api')
    app.register_blueprint(feishu_bp, url_prefix='/api')
    app.register_blueprint(profile_bp, url_prefix='/api')
