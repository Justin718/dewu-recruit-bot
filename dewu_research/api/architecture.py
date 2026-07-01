"""
技术架构 API - 分层架构组件查询
"""
from flask import Blueprint, jsonify

architecture_bp = Blueprint('architecture', __name__, url_prefix='/api/architecture')


@architecture_bp.route('', methods=['GET'])
def get_architecture():
    """获取分层技术架构数据（按层聚合组件）"""
    from models import ArchitectureComponent

    components = ArchitectureComponent.query\
        .order_by(ArchitectureComponent.layer_order, ArchitectureComponent.order_in_layer).all()

    layers = {}
    layer_meta = {}

    for comp in components:
        lname = comp.layer_name
        if lname not in layers:
            layers[lname] = []
            layer_meta[lname] = {
                'icon': comp.layer_icon,
                'desc': comp.layer_desc,
                'order': comp.layer_order,
            }

        layers[lname].append({
            'name': comp.comp_name,
            'desc': comp.comp_desc,
            'tags': comp.comp_tags or [],
        })

    # 按 order 排序层
    sorted_layers = sorted(layers.items(), key=lambda x: layer_meta[x[0]]['order'])

    result = []
    for lname, comps in sorted_layers:
        meta = layer_meta[lname]
        result.append({
            'layer_name': lname,
            'layer_icon': meta['icon'],
            'layer_desc': meta['desc'],
            'components': comps,
        })

    return jsonify({'layers': result})
