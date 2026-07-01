"""
飞书集成 API - 功能配置 + 消息流
"""
from flask import Blueprint, jsonify

feishu_bp = Blueprint('feishu', __name__, url_prefix='/api/feishu')


@feishu_bp.route('', methods=['GET'])
def get_feishu_config():
    """获取飞书集成配置（功能特性列表 + 最近消息）"""
    from models import FeishuFeature, FeishuMessage

    features = FeishuFeature.query.all()
    messages = FeishuMessage.query.order_by(FeishuMessage.id.desc()).limit(20).all()

    feature_list = [{
        'name': f.name,
        'description': f.description,
        'status': f.status,
        'icon': f.icon,
    } for f in features]

    message_list = [{
        'time': m.time,
        'content': m.content,
        'type': m.msg_type,
    } for m in reversed(messages)]

    return jsonify({
        'features': feature_list,
        'messages': message_list,
        'bot_info': {
            'name': '得物AI学者助手',
            'description': '推荐系统方向 · 研究型实习生智能助理',
            'connected': True,
        }
    })
