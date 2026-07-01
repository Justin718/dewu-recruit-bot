"""
研究项目 API - 项目列表 / 单项目详情
"""
from flask import Blueprint, jsonify, request

projects_bp = Blueprint('projects', __name__, url_prefix='/api/projects')


@projects_bp.route('', methods=['GET'])
def get_projects():
    """获取研究项目列表"""
    from ..models import ResearchProject
    projects = ResearchProject.query.order_by(ResearchProject.order_idx).all()

    result = []
    for p in projects:
        result.append({
            'project_id': p.project_id,
            'title': p.title,
            'category': p.category,
            'description': p.description,
            'tech_stack': p.tech_stack or [],
            'metrics': p.metrics or {},
            'progress': p.progress,
            'status': p.status,
            'icon': p.icon,
            'color': p.color,
        })

    return jsonify({'projects': result, 'total': len(result)})


@projects_bp.route('/<project_id>', methods=['GET'])
def get_project_detail(project_id):
    """获取单个项目详情（含时间线）"""
    from models import ResearchProject, ProjectTimeline

    project = ResearchProject.query.filter_by(project_id=project_id).first()
    if not project:
        return jsonify({'error': '项目不存在'}), 404

    timeline = ProjectTimeline.query.filter_by(project_id=project_id)\
        .order_by(ProjectTimeline.order_idx).all()

    detail = {
        'project_id': project.project_id,
        'title': project.title,
        'category': project.category,
        'description': project.description,
        'tech_stack': project.tech_stack or [],
        'metrics': project.metrics or {},
        'progress': project.progress,
        'status': project.status,
        'timeline': [{'date': t.event_date, 'event': t.event, 'type': t.event_type} for t in timeline],
    }
    return jsonify(detail)
