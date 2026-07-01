"""
API 蓝图统一注册入口
"""
from .dashboard import dashboard_bp
from .projects import projects_bp
from .architecture import architecture_bp
from .knowledge import knowledge_bp
from .feishu import feishu_bp
from .profile import profile_bp

BLUEPRINTS = [
    dashboard_bp,
    projects_bp,
    architecture_bp,
    knowledge_bp,
    feishu_bp,
    profile_bp,
]


def register_blueprints(app):
    """将所有蓝图注册到 Flask App，统一加 /api 前缀"""
    for bp in BLUEPRINTS:
        app.register_blueprint(bp)
