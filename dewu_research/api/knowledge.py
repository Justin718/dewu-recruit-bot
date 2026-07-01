"""
知识图谱 API - 节点 + 边 数据
"""
from flask import Blueprint, jsonify

knowledge_bp = Blueprint('knowledge', __name__, url_prefix='/api/knowledge-graph')


@knowledge_bp.route('', methods=['GET'])
def get_knowledge_graph():
    """获取完整知识图谱数据（节点+边）"""
    from models import KnowledgeNode, KnowledgeEdge

    nodes = KnowledgeNode.query.all()
    edges = KnowledgeEdge.query.all()

    node_list = [{
        'id': n.node_id,
        'label': n.label,
        'type': n.node_type,
        'size': n.size,
        'color': n.color,
        'detail': n.detail,
        'x': n.x,
        'y': n.y,
    } for n in nodes]

    edge_list = [{
        'source': e.source,
        'target': e.target,
        'relation': e.relation,
        'confidence': e.confidence,
    } for e in edges]

    return jsonify({
        'nodes': node_list,
        'edges': edge_list,
        'stats': {
            'node_count': len(node_list),
            'edge_count': len(edge_list),
        }
    })
