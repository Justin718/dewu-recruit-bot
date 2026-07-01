# -*- coding: utf-8 -*-
"""技术架构 API"""
from flask import Blueprint, jsonify
from models import ArchitectureComponent

architecture_bp = Blueprint('architecture', __name__)


@architecture_bp.route('/architecture')
def architecture():
    """获取分层技术架构"""
    components = ArchitectureComponent.query.order_by(
        ArchitectureComponent.layer_order,
        ArchitectureComponent.id,
    ).all()

    # 按层聚合
    layers_map = {}
    for comp in components:
        key = comp.layer_name
        if key not in layers_map:
            layers_map[key] = {
                'name': key,
                'icon': comp.layer_icon,
                'components': [],
            }
        layers_map[key]['components'].append(comp.to_dict())

    layers = sorted(layers_map.values(), key=lambda x: components[0].layer_order)

    return jsonify({'layers': layers})
