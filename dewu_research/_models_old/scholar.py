# -*- coding: utf-8 -*-
"""得物研究型实习生 - 数据模型层"""
import json
from datetime import datetime
from extensions import db


class ScholarProfile(db.Model):
    """学者个人信息表"""
    __tablename__ = 'scholar_profile'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, default='AI Scholar')
    title = db.Column(db.String(128), default='研究型实习生')
    department = db.Column(db.String(256), default='算法策略部 - 推荐系统方向')
    company = db.Column(db.String(128), default='得物App')
    period = db.Column(db.String(64), default='2026.03 - 2026.06')
    email = db.Column(db.String(128), default='scholar@dewu.com')
    avatar = db.Column(db.String(512), default='')
    _skills = db.Column('skills', db.Text, default='[]')
    _research_interests = db.Column('research_interests', db.Text, default='[]')
    summary = db.Column(db.Text, default='')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    @property
    def skills(self):
        return json.loads(self._skills)

    @skills.setter
    def skills(self, value):
        self._skills = json.dumps(value, ensure_ascii=False)

    @property
    def research_interests(self):
        return json.loads(self._research_interests)

    @research_interests.setter
    def research_interests(self, value):
        self._research_interests = json.dumps(value, ensure_ascii=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'title': self.title,
            'department': self.department,
            'company': self.company,
            'period': self.period,
            'email': self.email,
            'avatar': self.avatar,
            'skills': self.skills,
            'research_interests': self.research_interests,
            'summary': self.summary,
        }

    def __repr__(self):
        return f'<ScholarProfile {self.name}>'


class ResearchProject(db.Model):
    """研究项目表"""
    __tablename__ = 'research_projects'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    project_id = db.Column(db.String(32), unique=True, nullable=False)
    name = db.Column(db.String(256), nullable=False)
    icon = db.Column(db.String(16), default='📌')
    category = db.Column(db.String(64), default='未分类')
    status = db.Column(db.String(32), default='进行中')
    progress = db.Column(db.Integer, default=0)
    description = db.Column(db.Text, default='')
    _tech_stack = db.Column('tech_stack', db.Text, default='[]')
    _metrics = db.Column('metrics', db.Text, default='{}')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    timelines = db.relationship('ProjectTimeline', backref='project',
                                lazy='dynamic', cascade='all, delete-orphan',
                                order_by='ProjectTimeline.event_date')

    @property
    def tech_stack(self):
        return json.loads(self._tech_stack)

    @tech_stack.setter
    def tech_stack(self, value):
        self._tech_stack = json.dumps(value, ensure_ascii=False)

    @property
    def metrics(self):
        return json.loads(self._metrics)

    @metrics.setter
    def metrics(self, value):
        self._metrics = json.dumps(value, ensure_ascii=False)

    def to_dict(self, include_timeline=True):
        result = {
            'id': self.project_id,
            'name': self.name,
            'icon': self.icon,
            'category': self.category,
            'status': self.status,
            'progress': self.progress,
            'description': self.description,
            'tech_stack': self.tech_stack,
            'metrics': self.metrics,
        }
        if include_timeline:
            result['timeline'] = [t.to_dict() for t in self.timelines.all()]
        return result

    def __repr__(self):
        return f'<ResearchProject {self.name}>'


class ProjectTimeline(db.Model):
    """项目时间线表"""
    __tablename__ = 'project_timelines'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    project_id = db.Column(db.Integer, db.ForeignKey('research_projects.id'), nullable=False)
    event_date = db.Column(db.String(32), nullable=False)
    event = db.Column(db.String(512), nullable=False)

    def to_dict(self):
        return {
            'date': self.event_date,
            'event': self.event,
        }

    def __repr__(self):
        return f'<ProjectTimeline {self.event_date} {self.event}>'


class ArchitectureComponent(db.Model):
    """技术架构组件表"""
    __tablename__ = 'architecture_components'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    layer_name = db.Column(db.String(64), nullable=False)
    layer_icon = db.Column(db.String(16), default='📦')
    layer_order = db.Column(db.Integer, default=0)
    comp_name = db.Column(db.String(128), nullable=False)
    comp_desc = db.Column(db.String(512), default='')

    def to_dict(self):
        return {
            'name': self.comp_name,
            'desc': self.comp_desc,
        }

    def __repr__(self):
        return f'<ArchitectureComponent {self.layer_name}/{self.comp_name}>'


class KnowledgeNode(db.Model):
    """知识图谱节点表"""
    __tablename__ = 'knowledge_nodes'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    node_id = db.Column(db.String(64), unique=True, nullable=False)
    label = db.Column(db.String(128), nullable=False)
    node_type = db.Column('type', db.String(32), default='tech')
    size = db.Column(db.Integer, default=20)
    color = db.Column(db.String(16), default='#3b82f6')

    def to_dict(self):
        return {
            'id': self.node_id,
            'label': self.label,
            'type': self.node_type,
            'size': self.size,
            'color': self.color,
        }

    def __repr__(self):
        return f'<KnowledgeNode {self.label}>'


class KnowledgeEdge(db.Model):
    """知识图谱边表"""
    __tablename__ = 'knowledge_edges'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    source = db.Column(db.String(64), nullable=False)
    target = db.Column(db.String(64), nullable=False)
    relation = db.Column(db.String(64), default='关联')

    def to_dict(self):
        return {
            'source': self.source,
            'target': self.target,
            'relation': self.relation,
        }

    def __repr__(self):
        return f'<KnowledgeEdge {self.source} -{self.relation}-> {self.target}>'


class FeishuFeature(db.Model):
    """飞书功能特性表"""
    __tablename__ = 'feishu_features'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(512), default='')
    status = db.Column(db.String(32), default='planned')

    def to_dict(self):
        return {
            'name': self.name,
            'desc': self.description,
            'status': self.status,
        }

    def __repr__(self):
        return f'<FeishuFeature {self.name}>'


class FeishuMessage(db.Model):
    """飞书消息记录表"""
    __tablename__ = 'feishu_messages'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    time = db.Column(db.String(64), default='')
    content = db.Column(db.Text, default='')
    msg_type = db.Column('type', db.String(32), default='report')

    def to_dict(self):
        return {
            'time': self.time,
            'content': self.content,
            'type': self.msg_type,
        }

    def __repr__(self):
        return f'<FeishuMessage {self.time}>'
