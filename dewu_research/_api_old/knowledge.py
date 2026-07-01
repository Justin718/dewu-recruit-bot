# -*- coding: utf-8 -*-
"""知识图谱 API"""
from flask import Blueprint, jsonify
from models import KnowledgeNode, KnowledgeEdge

knowledge_bp = Blueprint('knowledge', __name__)


@knowledge_bp.route('/knowledge-graph')
def knowledge_graph():
    """获取知识图谱节点和边"""
    nodes = KnowledgeNode.query.all()
    edges = KnowledgeEdge.query.all()

    return jsonify({
        'nodes': [n.to_dict() for n in nodes],
        'edges': [e.to_dict() for e in edges],
    })
