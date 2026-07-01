# -*- coding: utf-8 -*-
"""学者个人资料 API"""
from flask import Blueprint, jsonify
from models import ScholarProfile

profile_bp = Blueprint('profile', __name__)


@profile_bp.route('/profile')
def get_profile():
    """获取学者个人信息"""
    profile = ScholarProfile.query.first()
    if not profile:
        return jsonify({'error': '学者信息未初始化'}), 404
    return jsonify(profile.to_dict())
