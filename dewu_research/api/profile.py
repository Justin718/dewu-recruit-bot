"""
学者个人资料 API
"""
from flask import Blueprint, jsonify
from models import ScholarProfile

profile_bp = Blueprint('profile', __name__, url_prefix='/api/profile')


@profile_bp.route('', methods=['GET'])
def get_profile():
    """获取学者/实习生个人资料"""
    profile = ScholarProfile.query.first()
    if not profile:
        return jsonify({'error': '暂无档案'}), 404

    return jsonify({
        'name': profile.name,
        'role_title': profile.role_title,
        'company': profile.company,
        'department': profile.department,
        'project_direction': profile.project_direction,
        'skills': profile.skills or [],
        'research_interests': profile.research_interests or [],
        'summary': profile.summary,
        'start_date': profile.start_date,
        'end_date': profile.end_date,
    })
