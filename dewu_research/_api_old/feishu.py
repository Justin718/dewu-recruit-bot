# -*- coding: utf-8 -*-
"""飞书集成 API"""
from flask import Blueprint, jsonify
from models import FeishuFeature, FeishuMessage

feishu_bp = Blueprint('feishu', __name__)


@feishu_bp.route('/feishu')
def feishu_config():
    """获取飞书集成配置"""
    features = FeishuFeature.query.all()
    messages = FeishuMessage.query.order_by(FeishuMessage.id.desc()).all()

    return jsonify({
        'enabled': True,
        'bot_name': '得物AI学者助手',
        'bot_avatar': '🤖',
        'features': [f.to_dict() for f in features],
        'recent_messages': [m.to_dict() for m in messages],
    })
