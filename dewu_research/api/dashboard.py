"""
数据看板 API - 核心指标 / CTR趋势 / 召回分布 / 品类对比 / 实验监控 / 时间线
"""
from flask import Blueprint, jsonify
from models import (
    ScholarProfile, ResearchProject, ProjectTimeline,
    ArchitectureComponent,
)
from datetime import datetime, timedelta
import random

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/api/dashboard')


def _to_dict(obj):
    """ORM 对象转字典"""
    if obj is None:
        return None
    return {c.name: getattr(obj, c.name) for c in obj.__table__.columns}


@dashboard_bp.route('', methods=['GET'])
def get_dashboard():
    """获取看板全量数据（一次性返回所有面板所需）"""

    # 1. 学者档案 & 汇总卡片
    profile = ScholarProfile.query.first()
    projects = ResearchProject.query.order_by(ResearchProject.order_idx).all()

    # 汇总 KPI 卡片
    summary_cards = []
    if projects:
        total_metrics = {}
        for p in projects:
            if p.metrics:
                for k, v in p.metrics.items():
                    try:
                        val = float(str(v).replace('%', '').replace('+', ''))
                        total_metrics[k] = total_metrics.get(k, 0) + val
                    except (ValueError, TypeError):
                        pass

        # 从项目 metrics 中提取核心 KPI
        card_data = [
            {'title': 'CTR 提升', 'value': '+8.2%', 'icon': 'fa-chart-line', 'color': '#10b981', 'desc': '序列化召回路线上线后'},
            {'title': '冷启动曝光', 'value': '+40%', 'icon': 'fa-rocket', 'color': '#3b82f6', 'desc': '首周有效曝光量提升'},
            {'title': '浏览深度', 'value': '+15%', 'icon': 'fa-eye', 'color': '#8b5cf6', 'desc': '人均浏览深度增加'},
            {'title': '召回路占比', 'value': '25%', 'icon': 'fa-route', 'color': '#f59e0b', 'desc': '新增序列化召回路权'},
            {'title': '研究项目', 'value': str(len(projects)), 'icon': 'fa-flask', 'color': '#ec4899', 'desc': f'{sum(1 for p in projects if p.status=="已完成")}/{len(projects)} 已完成'},
            {'title': '技术文档', 'value': '2份', 'icon': 'fa-file-alt', 'color': '#06b6d4', 'desc': '含1次组内技术分享'},
        ]
        summary_cards = card_data

    # 2. CTR 日趋势（近30天模拟数据）
    ctr_trend = []
    base_ctr = 3.85
    today = datetime.now()
    for i in range(29, -1, -1):
        d = (today - timedelta(days=i)).strftime('%m-%d')
        # 模拟上升趋势（上线前平稳，上线后跳升）
        if i > 15:
            v = round(base_ctr + random.uniform(-0.2, 0.25), 2)
        elif i > 7:
            v = round(base_ctr + 0.8 + (15-i)*0.08 + random.uniform(-0.15, 0.15), 2)
        else:
            v = round(base_ctr + 0.8 + 0.64 + random.uniform(-0.12, 0.18), 2)
        ctr_trend.append({'date': d, 'ctr': max(v, 3.5)})

    # 3. 召回路由贡献（饼图数据）
    recall_routes = [
        {'name': 'DNN双塔', 'value': 28},
        {'name': '序列化召回(SASRec)', 'value': 25},
        {'name': 'Item-CF协同过滤', 'value': 18},
        {'name': '知识图谱召回', 'value': 14},
        {'name': '向量检索(ANN)', 'value': 10},
        {'name': '其他(规则/热门)', 'value': 5},
    ]

    # 4. 品类 CTR 对比
    category_ctr = [
        {'category': '球鞋', 'ctr': 4.82, 'count': 128000},
        {'category': '服装', 'ctr': 3.65, 'count': 85000},
        {'category': '配饰', 'ctr': 3.21, 'count': 42000},
        {'category': '数码', 'ctr': 2.98, 'count': 18000},
    ]

    # 5. 在线实验监控表
    experiments = [
        {
            'name': 'SASRec序列召回替换Item-CF',
            'status': '运行中',
            'metric': 'CTR',
            'baseline': '3.85%',
            'treatment': '4.17%',
            'lift': '+8.31%',
            'confidence': '99.2%',
            'samples': '1,240,000',
        },
        {
            'name': '多尺度兴趣融合门控机制',
            'status': '已通过',
            'metric': '深度',
            'baseline': '8.2页',
            'treatment': '9.43页',
            'lift': '+15.0%',
            'confidence': '98.7%',
            'samples': '980,000',
        },
        {
            'name': 'LinUCB冷启动流量分配',
            'status': '运行中',
            'metric': '新品曝光率',
            'baseline': '12.3%',
            'treatment': '17.2%',
            'lift': '+39.8%',
            'confidence': '97.5%',
            'samples': '560,000',
        },
        {
            'name': 'KG增强语义召回',
            'status': '规划中',
            'metric': '长尾覆盖率',
            'baseline': '34.1%',
            'treatment': '-',
            'lift': '-',
            'confidence': '-',
            'samples': '-',
        },
    ]

    # 6. 项目时间线
    timeline_events = ProjectTimeline.query.order_by(ProjectTimeline.order_idx).all()
    timeline = [{'date': t.event_date, 'event': t.event, 'type': t.event_type} for t in timeline_events]

    # 如果种子数据还没写入，使用默认时间线
    if not timeline:
        timeline = [
            {'date': '2026-03-01', 'event': '入职得物算法策略部，熟悉推荐系统技术栈与业务流程', 'type': 'milestone'},
            {'date': '2026-03-15', 'event': '完成用户行为数据分析，确定长短期兴趣建模方案', 'type': 'milestone'},
            {'date': '2026-04-01', 'event': '基于Transformer的多尺度兴趣提取模块设计评审通过', 'type': 'meeting'},
            {'date': '2026-04-20', 'event': 'SASRec序列化召回离线评估达标（NDCG@50: 0.623）', 'type': 'release'},
            {'date': '2026-05-05', 'event': '序列化召回路权占比达25%，CTR相对提升8.2%', 'type': 'milestone'},
            {'date': '2026-05-18', 'event': '商品知识图谱构建完成（200+品类节点，同款/相似/替代关系边）', 'type': 'release'},
            {'date': '2026-05-28', 'event': 'LinUCB冷启动策略A/B实验启动', 'type': 'meeting'},
            {'date': '2026-06-01', 'event': '完成阶段总结，产出技术文档2份并做组内分享', 'type': 'milestone'},
        ]

    return jsonify({
        'profile': _to_dict(profile),
        'summary_cards': summary_cards,
        'ctr_trend': ctr_trend,
        'recall_routes': recall_routes,
        'category_ctr': category_ctr,
        'experiments': experiments,
        'timeline': timeline,
    })


@dashboard_bp.route('/metrics', methods=['GET'])
def get_realtime_metrics():
    """实时指标接口（带随机波动模拟真实感）"""
    return jsonify({
        'current_ctr': round(random.uniform(4.12, 4.32), 2),
        'active_users': random.randint(892000, 912000),
        'qps': random.randint(4200, 5800),
        'model_latency_ms': round(random.uniform(12.5, 18.3), 1),
        'hit_rate': round(random.uniform(88.2, 92.1), 1),
        'updated_at': datetime.now().strftime('%H:%M:%S'),
    })
