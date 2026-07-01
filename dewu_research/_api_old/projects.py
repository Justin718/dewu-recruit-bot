# -*- coding: utf-8 -*-
"""研究项目 API"""
from flask import Blueprint, jsonify, request
from models import ResearchProject

projects_bp = Blueprint('projects', __name__)


@projects_bp.route('/projects')
def get_projects():
    """获取项目列表或单个项目"""
    project_id = request.args.get('id')
    if project_id:
        project = ResearchProject.query.filter_by(project_id=project_id).first()
        if not project:
            return jsonify({'error': '项目未找到', 'code': 404}), 404
        return jsonify(project.to_dict())

    projects = ResearchProject.query.order_by(ResearchProject.id).all()
    return jsonify([p.to_dict() for p in projects])
