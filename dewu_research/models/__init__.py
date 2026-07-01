"""
ORM 数据模型 - 得物研究型实习生项目
定义8张核心表: 学者档案 / 研究项目 / 时间线 / 架构组件 / KG节点 / KG边 / 飞书功能 / 飞书消息
"""
from extensions import db


class ScholarProfile(db.Model):
    """学者/实习生个人档案"""
    __tablename__ = 'scholar_profile'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), nullable=False, default='AI Scholar')
    role_title = db.Column(db.String(128), nullable=False)
    company = db.Column(db.String(64), nullable=False, default='得物App')
    department = db.Column(db.String(128), nullable=False)
    project_direction = db.Column(db.String(128), nullable=False)

    # JSON 字段
    skills = db.Column(db.JSON, default=list)               # 技术栈列表
    research_interests = db.Column(db.JSON, default=list)     # 研究方向
    summary = db.Column(db.Text, default='')                # 项目概述

    # 时间范围
    start_date = db.Column(db.String(32), default='')
    end_date = db.Column(db.String(32), default='')

    created_at = db.Column(db.DateTime, server_default=db.func.now())


class ResearchProject(db.Model):
    """研究项目"""
    __tablename__ = 'research_projects'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    project_id = db.Column(db.String(64), unique=True, nullable=False)
    title = db.Column(db.String(256), nullable=False)
    category = db.Column(db.String(64), nullable=False)     # 分类: 建模/召回/KG/冷启动/评估
    description = db.Column(db.Text, default='')             # 详细描述
    tech_stack = db.Column(db.JSON, default=list)            # 技术栈标签
    metrics = db.Column(db.JSON, default=dict)               # 核心指标 {"CTR提升": "8.2%", ...}
    progress = db.Column(db.Integer, default=0)               # 进度 0-100
    status = db.Column(db.String(32), default='进行中')      # 进行中/已完成/规划中
    icon = db.Column(db.String(64), default='fa-flask')      # Font Awesome 图标类名
    color = db.Column(db.String(16), default='#3b82f6')      # 主题色
    order_idx = db.Column(db.Integer, default=0)


class ProjectTimeline(db.Model):
    """项目时间线事件"""
    __tablename__ = 'project_timelines'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    project_id = db.Column(db.String(64), nullable=False, index=True)
    event_date = db.Column(db.String(32), nullable=False)
    event = db.Column(db.Text, default='')
    event_type = db.Column(db.String(32), default='milestone')  # milestone/meeting/release
    order_idx = db.Column(db.Integer, default=0)


class ArchitectureComponent(db.Model):
    """技术架构组件"""
    __tablename__ = 'architecture_components'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    layer_name = db.Column(db.String(64), nullable=False, index=True)
    layer_icon = db.Column(db.String(64), default='')
    layer_desc = db.Column(db.Text, default='')
    layer_order = db.Column(db.Integer, default=0)
    comp_name = db.Column(db.String(128), nullable=False)
    comp_desc = db.Column(db.Text, default='')
    comp_tags = db.Column(db.JSON, default=list)
    order_in_layer = db.Column(db.Integer, default=0)


class KnowledgeNode(db.Model):
    """知识图谱节点"""
    __tablename__ = 'knowledge_nodes'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    node_id = db.Column(db.String(64), unique=True, nullable=False)
    label = db.Column(db.String(128), nullable=False)
    node_type = db.Column(db.String(32), nullable=False)   # domain / tech / tool
    size = db.Column(db.Integer, default=20)
    color = db.Column(db.String(16), default='#3b82f6')
    detail = db.Column(db.Text, default='')
    x = db.Column(db.Float, default=0)                      # 预计算布局位置
    y = db.Column(db.Float, default=0)


class KnowledgeEdge(db.Model):
    """知识图谱边"""
    __tablename__ = 'knowledge_edges'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    source = db.Column(db.String(64), nullable=False, index=True)
    target = db.Column(db.String(64), nullable=False, index=True)
    relation = db.Column(db.String(64), default='related_to')
    confidence = db.Column(db.Float, default=1.0)


class FeishuFeature(db.Model):
    """飞书集成功能"""
    __tablename__ = 'feishu_features'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text, default='')
    status = db.Column(db.String(16), default='active')       # active/planned/disabled
    icon = db.Column(db.String(64), default='fa-robot')


class FeishuMessage(db.Model):
    """飞书消息流"""
    __tablename__ = 'feishu_messages'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    time = db.Column(db.String(32), nullable=False)
    content = db.Column(db.Text, default='')
    msg_type = db.Column(db.String(16), default='info')        # alert/report/paper/info
