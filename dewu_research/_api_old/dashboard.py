# -*- coding: utf-8 -*-
"""数据看板 API"""
import random
from datetime import datetime, timedelta
from flask import Blueprint, jsonify
from models import ResearchProject
from extensions import db

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/dashboard')
def dashboard():
    """获取完整看板数据"""
    kpi_cards = [
        {'title': 'CTR相对提升', 'value': '+8.2%', 'icon': '📈', 'trend': 'up',
         'change': '+1.3% vs上月', 'color': '#10b981'},
        {'title': '人均浏览深度', 'value': '+15%', 'icon': '📊', 'trend': 'up',
         'change': '+3.2% vs上月', 'color': '#3b82f6'},
        {'title': '冷品曝光提升', 'value': '+40%', 'icon': '🚀', 'trend': 'up',
         'change': '+8.5% vs上月', 'color': '#f59e0b'},
        {'title': '库存周转缩短', 'value': '5.2天', 'icon': '📦', 'trend': 'down',
         'change': '-1.8天 vs上月', 'color': '#8b5cf6'},
        {'title': '日均处理请求', 'value': '8.6亿', 'icon': '⚡', 'trend': 'up',
         'change': '+12% vs上月', 'color': '#ef4444'},
        {'title': '模型在线数', 'value': '28个', 'icon': '🤖', 'trend': 'up',
         'change': '+5个 vs上月', 'color': '#06b6d4'},
    ]

    days = [(datetime.now() - timedelta(days=i)).strftime('%m-%d') for i in range(30, 0, -1)]
    ctr_trend = {
        'labels': days,
        'values': [round(4.2 + random.uniform(-0.3, 0.5) + i * 0.01, 2) for i in range(30)],
        'baseline': [round(3.8 + random.uniform(-0.1, 0.2), 2) for _ in range(30)],
    }

    recall_sources = [
        {'name': '序列召回(SASRec)', 'value': 25, 'color': '#3b82f6'},
        {'name': 'Item-CF协同', 'value': 22, 'color': '#10b981'},
        {'name': '热门召回', 'value': 18, 'color': '#f59e0b'},
        {'name': '语义召回(KG)', 'value': 15, 'color': '#8b5cf6'},
        {'name': '冷启探索', 'value': 10, 'color': '#ef4444'},
        {'name': '其他', 'value': 10, 'color': '#6b7280'},
    ]

    category_ctr = [
        {'category': '球鞋', 'ctr_before': 4.1, 'ctr_after': 4.6, 'lift': 12.2},
        {'category': '服装', 'ctr_before': 3.8, 'ctr_after': 4.3, 'lift': 13.2},
        {'category': '配饰', 'ctr_before': 3.5, 'ctr_after': 3.9, 'lift': 11.4},
        {'category': '数码', 'ctr_before': 4.3, 'ctr_after': 4.7, 'lift': 9.3},
        {'category': '潮玩', 'ctr_before': 3.2, 'ctr_after': 3.6, 'lift': 12.5},
    ]

    experiments = [
        {'id': 'EXP_042', 'name': '兴趣建模v2.1', 'status': 'running',
         'ctr_lift': '+2.3%', 'confidence': '99.2%', 'days': 14},
        {'id': 'EXP_043', 'name': 'KG语义召回', 'status': 'running',
         'ctr_lift': '+1.8%', 'confidence': '97.5%', 'days': 10},
        {'id': 'EXP_044', 'name': '冷启Bandit调参', 'status': 'running',
         'ctr_lift': '+3.1%', 'confidence': '95.8%', 'days': 7},
        {'id': 'EXP_045', 'name': '多目标权重', 'status': 'paused',
         'ctr_lift': '+0.5%', 'confidence': '82.3%', 'days': 5},
        {'id': 'EXP_046', 'name': '重排多样性', 'status': 'planned',
         'ctr_lift': '-', 'confidence': '-', 'days': 0},
    ]

    timeline = [
        {'date': '2026-03', 'title': '入职 & 项目启动',
         'desc': '加入算法策略部推荐系统方向', 'type': 'milestone'},
        {'date': '2026-03', 'title': '兴趣建模方案设计',
         'desc': '完成多尺度兴趣提取模块设计', 'type': 'design'},
        {'date': '2026-04', 'title': '序列召回基线搭建',
         'desc': 'SASRec/BERT4Rec离线验证', 'type': 'dev'},
        {'date': '2026-04', 'title': '知识图谱构建',
         'desc': '商品属性数据爬取与KG搭建', 'type': 'dev'},
        {'date': '2026-04', 'title': '冷启动方案确定',
         'desc': 'LinUCB Bandit算法实现', 'type': 'design'},
        {'date': '2026-05', 'title': 'A/B实验上线',
         'desc': '多项目并行在线实验', 'type': 'milestone'},
        {'date': '2026-05', 'title': '序列召回全量',
         'desc': 'CTR提升8.2%，新增路权25%', 'type': 'milestone'},
        {'date': '2026-05', 'title': '评估体系搭建',
         'desc': '离线-在线指标对齐验证', 'type': 'dev'},
        {'date': '2026-06', 'title': '技术文档 & 分享',
         'desc': '产出2份技术文档+1次组内分享', 'type': 'milestone'},
    ]

    return jsonify({
        'kpi_cards': kpi_cards,
        'ctr_trend': ctr_trend,
        'recall_sources': recall_sources,
        'category_ctr': category_ctr,
        'experiments': experiments,
        'timeline': timeline,
        'updated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    })


@dashboard_bp.route('/metrics')
def metrics():
    """实时指标接口"""
    return jsonify({
        'online_metrics': {
            'ctr': round(4.52 + random.uniform(-0.1, 0.1), 2),
            'cvr': round(2.85 + random.uniform(-0.05, 0.05), 2),
            'browse_depth': round(3.8 + random.uniform(-0.2, 0.2), 1),
            'dwell_time': round(45 + random.uniform(-3, 3), 0),
            'add_cart_rate': round(8.2 + random.uniform(-0.3, 0.3), 1),
        },
        'model_performance': {
            'ctr_model_auc': round(0.782 + random.uniform(-0.005, 0.005), 4),
            'cvr_model_auc': round(0.734 + random.uniform(-0.005, 0.005), 4),
            'recall_hitrate': round(0.652 + random.uniform(-0.01, 0.01), 4),
            'recall_ndcg': round(0.418 + random.uniform(-0.01, 0.01), 4),
        },
        'updated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    })
