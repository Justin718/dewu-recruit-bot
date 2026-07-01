# -*- coding: utf-8 -*-
"""数据库种子数据 — 初始化时写入所有预置内容"""
from models import (
    ScholarProfile,
    ResearchProject,
    ProjectTimeline,
    ArchitectureComponent,
    KnowledgeNode,
    KnowledgeEdge,
    FeishuFeature,
    FeishuMessage,
)
from extensions import db


def seed_scholar_profile():
    """写入学者个人信息"""
    if ScholarProfile.query.first():
        return
    profile = ScholarProfile(
        name='AI Scholar',
        title='研究型实习生',
        department='算法策略部 - 推荐系统方向',
        company='得物App',
        period='2026.03 - 2026.06',
        email='scholar@dewu.com',
        skills=[
            'PyTorch', 'Transformers', 'TensorFlow', 'Spark', 'Flink',
            'Redis', 'Hive', 'ClickHouse', 'Airflow', 'Docker',
            'K8s', 'SQL', 'Python',
        ],
        research_interests=[
            '用户行为建模', '序列推荐', '知识图谱增强',
            '冷启动策略', 'A/B实验平台',
        ],
        summary='独立负责商品推荐场景下的用户行为建模与序列化召回优化，处理亿级用户-商品交互数据，支撑核心推荐链路CTR提升8%+',
    )
    db.session.add(profile)
    db.session.commit()


def seed_research_projects():
    """写入研究项目"""
    if ResearchProject.query.first():
        return

    projects_data = [
        {
            'project_id': 'proj_001',
            'name': '用户长短期兴趣建模',
            'icon': '🧠',
            'category': '用户理解',
            'status': '已完成',
            'progress': 100,
            'description': '基于Transformer架构设计多尺度兴趣提取模块，分别捕获用户近期实时兴趣（短期窗口7天）与长期偏好画像（90天历史聚合），通过注意力门控机制自适应融合双塔表征输入下游排序模型',
            'tech_stack': ['Transformer', 'Attention Gate', 'PyTorch', '双塔模型'],
            'metrics': {'AUC提升': '+2.3%', '用户时长提升': '+11%', '模型参数量': '12M'},
            'timelines': [
                {'event_date': '2026-03-10', 'event': '方案设计完成'},
                {'event_date': '2026-04-05', 'event': '离线实验验证'},
                {'event_date': '2026-04-20', 'event': 'A/B实验上线'},
                {'event_date': '2026-05-15', 'event': '全量推全'},
            ],
        },
        {
            'project_id': 'proj_002',
            'name': '序列化召回优化',
            'icon': '🔗',
            'category': '召回算法',
            'status': '已完成',
            'progress': 100,
            'description': '引入SASRec/BERT4Rec等序列推荐范式，利用用户最近50次交互行为预测下一候选集，结合Item-CF协同信号进行多路召回融合，新增路权占比达25%',
            'tech_stack': ['SASRec', 'BERT4Rec', 'Item-CF', '多路融合'],
            'metrics': {'CTR提升': '+8.2%', '浏览深度增加': '+15%', '新增路权占比': '25%'},
            'timelines': [
                {'event_date': '2026-03-20', 'event': '基线模型搭建'},
                {'event_date': '2026-04-15', 'event': '多路融合策略确定'},
                {'event_date': '2026-05-01', 'event': '灰度上线验证'},
                {'event_date': '2026-05-28', 'event': '全量上线'},
            ],
        },
        {
            'project_id': 'proj_003',
            'name': '商品知识图谱增强',
            'icon': '🕸️',
            'category': '知识图谱',
            'status': '进行中',
            'progress': 78,
            'description': '爬取并清洗商品属性数据（品牌、品类、风格标签、发售时间、价格带），构建同款/相似款/替代品关系边，用于推理类query的语义召回与解释性推荐',
            'tech_stack': ['爬虫', '数据清洗', 'Neo4j', '图神经网络'],
            'metrics': {'实体数量': '200K+', '关系边': '1.2M+', '推理准确率': '89.3%'},
            'timelines': [
                {'event_date': '2026-04-01', 'event': '数据爬取管道搭建'},
                {'event_date': '2026-04-25', 'event': '知识图谱构建'},
                {'event_date': '2026-05-20', 'event': 'GNN模型训练'},
                {'event_date': '2026-06-10', 'event': '预期线上集成'},
            ],
        },
        {
            'project_id': 'proj_004',
            'name': '冷启动策略设计',
            'icon': '🚀',
            'category': '冷启动',
            'status': '已完成',
            'progress': 100,
            'description': '针对新上架潮品，基于内容特征（图片CNN Embedding+文本属性）计算与历史热门品的相似度，采用Bandit算法（LinUCB）进行探索-利用均衡分配初始流量',
            'tech_stack': ['CNN', 'LinUCB', 'Bandit', '多臂老虎机'],
            'metrics': {'冷品曝光提升': '+40%', '库存周转缩短': '5.2天', '新品首周GMV': '+28%'},
            'timelines': [
                {'event_date': '2026-04-10', 'event': 'CNN特征提取'},
                {'event_date': '2026-04-28', 'event': 'LinUCB算法实现'},
                {'event_date': '2026-05-12', 'event': '小流量实验'},
                {'event_date': '2026-05-30', 'event': '全量上线'},
            ],
        },
        {
            'project_id': 'proj_005',
            'name': '离线评估体系搭建',
            'icon': '📊',
            'category': '工程平台',
            'status': '进行中',
            'progress': 85,
            'description': '构建A/B测试平台对接线上实验，设计分层抽样与SRM检验流程，确保实验结论统计显著；同时完善离线指标（NDCG@K、HitRate、Coverage）与业务指标的对齐验证',
            'tech_stack': ['A/B Testing', 'SRM检验', 'NDCG@K', 'HitRate'],
            'metrics': {'实验并行数': '12组', '评估指标数': '15+', '离线在线一致性': '92%'},
            'timelines': [
                {'event_date': '2026-04-15', 'event': '评估框架搭建'},
                {'event_date': '2026-05-10', 'event': 'SRM检验集成'},
                {'event_date': '2026-05-25', 'event': '指标对齐验证'},
                {'event_date': '2026-06-15', 'event': '预期全面交付'},
            ],
        },
    ]

    for pd in projects_data:
        timelines = pd.pop('timelines')
        project = ResearchProject(**pd)
        db.session.add(project)
        db.session.flush()
        for tl in timelines:
            db.session.add(ProjectTimeline(
                project_id=project.id,
                event_date=tl['event_date'],
                event=tl['event'],
            ))
    db.session.commit()


def seed_architecture():
    """写入技术架构"""
    if ArchitectureComponent.query.first():
        return

    layers = [
        ('应用层', '📱', 1, [
            ('猜你喜欢', '首页推荐feed流'),
            ('相关推荐', '详情页关联推荐'),
            ('搭配推荐', '购物车交叉销售'),
            ('搜索推荐', '搜索无结果兜底'),
        ]),
        ('排序层', '⚙️', 2, [
            ('CTR预估模型', 'DeepFM / DCN V2'),
            ('多目标优化', 'MMOE / PLE'),
            ('实时特征', 'Redis在线特征服务'),
            ('重排策略', '多样性+业务约束'),
        ]),
        ('召回层', '🔍', 3, [
            ('序列召回', 'SASRec/BERT4Rec'),
            ('协同过滤', 'Item-CF/Swing'),
            ('语义召回', '知识图谱+向量检索'),
            ('冷启探索', 'LinUCB Bandit'),
        ]),
        ('数据层', '💾', 4, [
            ('离线数仓', 'Hive/ClickHouse'),
            ('实时计算', 'Spark/Flink'),
            ('特征存储', 'Redis Cluster'),
            ('模型训练', 'PyTorch + GPU集群'),
        ]),
        ('基础设施', '☁️', 5, [
            ('容器编排', 'Docker + K8s'),
            ('任务调度', 'Airflow'),
            ('A/B平台', '自研实验平台'),
            ('监控告警', 'Grafana + Prometheus'),
        ]),
    ]

    for layer_name, layer_icon, order, comps in layers:
        for comp_name, comp_desc in comps:
            db.session.add(ArchitectureComponent(
                layer_name=layer_name,
                layer_icon=layer_icon,
                layer_order=order,
                comp_name=comp_name,
                comp_desc=comp_desc,
            ))
    db.session.commit()


def seed_knowledge_graph():
    """写入知识图谱"""
    if KnowledgeNode.query.first():
        return

    nodes = [
        ('rec_sys', '推荐系统', 'domain', 40, '#3b82f6'),
        ('user_model', '用户建模', 'domain', 30, '#10b981'),
        ('recall', '召回算法', 'domain', 30, '#f59e0b'),
        ('ranking', '排序模型', 'domain', 30, '#8b5cf6'),
        ('kg', '知识图谱', 'domain', 28, '#ef4444'),
        ('cold_start', '冷启动', 'domain', 25, '#06b6d4'),
        ('ab_test', 'A/B实验', 'domain', 25, '#ec4899'),
        ('transformer', 'Transformer', 'tech', 20, '#6366f1'),
        ('sasrec', 'SASRec', 'tech', 18, '#14b8a6'),
        ('bert4rec', 'BERT4Rec', 'tech', 18, '#14b8a6'),
        ('item_cf', 'Item-CF', 'tech', 16, '#f97316'),
        ('linucb', 'LinUCB', 'tech', 16, '#f97316'),
        ('deepfm', 'DeepFM', 'tech', 16, '#6366f1'),
        ('mmoe', 'MMOE', 'tech', 16, '#6366f1'),
        ('cnn_embed', 'CNN Embedding', 'tech', 14, '#a855f7'),
        ('gnn', '图神经网络', 'tech', 14, '#a855f7'),
        ('pytorch', 'PyTorch', 'tool', 16, '#ec4899'),
        ('spark', 'Spark/Flink', 'tool', 14, '#f43f5e'),
        ('redis', 'Redis', 'tool', 12, '#0ea5e9'),
        ('hive', 'Hive/CH', 'tool', 12, '#0ea5e9'),
        ('k8s', 'Docker/K8s', 'tool', 12, '#84cc16'),
    ]

    for node_id, label, ntype, size, color in nodes:
        db.session.add(KnowledgeNode(
            node_id=node_id, label=label,
            node_type=ntype, size=size, color=color,
        ))

    edges = [
        ('rec_sys', 'user_model', '包含'),
        ('rec_sys', 'recall', '包含'),
        ('rec_sys', 'ranking', '包含'),
        ('rec_sys', 'kg', '增强'),
        ('rec_sys', 'cold_start', '专项'),
        ('rec_sys', 'ab_test', '验证'),
        ('user_model', 'transformer', '使用'),
        ('recall', 'sasrec', '使用'),
        ('recall', 'bert4rec', '使用'),
        ('recall', 'item_cf', '使用'),
        ('cold_start', 'linucb', '使用'),
        ('cold_start', 'cnn_embed', '使用'),
        ('ranking', 'deepfm', '使用'),
        ('ranking', 'mmoe', '使用'),
        ('kg', 'gnn', '使用'),
        ('transformer', 'pytorch', '框架'),
        ('sasrec', 'pytorch', '框架'),
        ('deepfm', 'pytorch', '框架'),
        ('user_model', 'redis', '在线特征'),
        ('recall', 'redis', '在线特征'),
        ('user_model', 'spark', '离线训练'),
        ('recall', 'hive', '数据源'),
        ('ab_test', 'k8s', '部署'),
    ]
    for src, tgt, rel in edges:
        db.session.add(KnowledgeEdge(source=src, target=tgt, relation=rel))

    db.session.commit()


def seed_feishu():
    """写入飞书配置"""
    if FeishuFeature.query.first():
        return

    features = [
        ('项目进度推送', '每周一自动推送研究项目进展到飞书群', 'active'),
        ('实验告警', 'A/B实验指标异常时实时告警', 'active'),
        ('日报生成', 'AI自动生成每日研究日报', 'testing'),
        ('论文速递', '每日推送推荐系统领域最新论文', 'planned'),
        ('数据看板', '飞书多维表格同步实验数据', 'planned'),
    ]
    for name, desc, status in features:
        db.session.add(FeishuFeature(name=name, description=desc, status=status))

    messages = [
        ('10分钟前', '🔔 EXP_042 兴趣建模v2.1 CTR提升达到99.2%置信度，建议推全', 'alert'),
        ('1小时前', '📊 今日日报已生成：CTR 4.52%（+0.3%），浏览深度3.8（+5.6%）', 'report'),
        ('3小时前', '📄 新论文速递：LLM4Rec - 大语言模型在推荐系统中的应用综述', 'paper'),
    ]
    for time, content, mtype in messages:
        db.session.add(FeishuMessage(time=time, content=content, msg_type=mtype))

    db.session.commit()


def seed_all():
    """执行全部种子数据写入（幂等：已存在则跳过）"""
    seed_scholar_profile()
    seed_research_projects()
    seed_architecture()
    seed_knowledge_graph()
    seed_feishu()
    print('[Seed] 数据库初始化完成')
