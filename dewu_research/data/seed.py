"""
得物研究型实习生 - 种子数据初始化
面向得物App推荐系统方向 · 算法策略部
所有数据围绕电商推荐真实业务场景构建
"""
from extensions import db
from models import (
    ScholarProfile, ResearchProject, ProjectTimeline,
    ArchitectureComponent, KnowledgeNode, KnowledgeEdge,
    FeishuFeature, FeishuMessage,
)


def seed_scholar_profile():
    if ScholarProfile.query.first() is not None:
        return
    profile = ScholarProfile(
        name='AI Scholar',
        role_title='算法策略实习生 - 推荐系统方向',
        company='得物App',
        department='技术中台-算法策略部',
        project_direction='商品推荐系统优化',
        skills=[
            'PyTorch', 'Transformers', 'TensorFlow Serving', 'Spark/Flink',
            'Redis', 'Hive/ClickHouse', 'Airflow', 'Docker/K8s',
            'SQL', 'Python', 'SASRec', 'BERT4Rec', 'DeepFM',
        ],
        research_interests=[
            '序列推荐(Sequential Recommendation)',
            '用户多尺度兴趣建模(Multi-scale Interest Modeling)',
            '知识图谱增强推荐(KG-enhanced RecSys)',
            '冷启动与探索-利用(Cold Start & Bandit)',
            '因果推断与A/B实验平台',
        ],
        summary=(
            '独立负责得物商品推荐场景下的用户行为建模与序列化召回优化，'
            '处理亿级用户-商品交互数据，支撑核心推荐链路CTR提升8%+，'
            '服务DAU千万级用户的个性化推荐需求。'
        ),
        start_date='2026-03',
        end_date='2026-06',
    )
    db.session.add(profile)
    db.session.commit()
    print('  [seed] 学者档案已创建')


def seed_research_projects():
    if ResearchProject.query.first() is not None:
        return

    projects_data = [
        {'project_id':'P001','title':'用户长短期兴趣建模 (Multi-Scale Interest Modeling)','category':'用户建模','progress':100,'status':'已完成','icon':'fa-brain','color':'#3b82f6','order_idx':1,
         'description':'基于Transformer架构设计多尺度兴趣提取模块：\n• 短期窗口(7天)：捕获用户近期实时兴趣\n• 长期画像(90天)：历史行为聚合稳定偏好\n• 门控融合(Gating)：自适应融合双塔表征输入下游排序模型\n核心技术：Self-Attention + Temporal Encoding + Gate Network',
         'tech_stack':['PyTorch','Transformers','Self-Attention','Gate Network'],'metrics':{'浏览深度提升':'+15.0%','User Embedding质量':'MRR@10: 0.682'}},
        {'project_id':'P002','title':'序列化召回优化 (SASRec/BERT4Rec)','category':'召回优化','progress':100,'status':'已完成','icon':'fa-route','color':'#10b981','order_idx':2,
         'description':'引入序列推荐范式替换传统Item-CF协同过滤召回：\n• 模型选型：SASRec作为基线，对比BERT4Rec\n• 输入：用户最近50次交互行为的item embedding序列\n• 输出：Top-K候选商品集(K=200)，送入粗排层\n• 多路召回融合占比已调至25%\n• 离线指标：NDCG@50: 0.623 | HitRate@20: 0.741 | Coverage@500: 0.892\n• 已上线，CTR相对提升8.2%',
         'tech_stack':['PyTorch','SASRec','BERT4Rec','Item-CF','FAISS/ANN'],'metrics':{'CTR提升':'+8.2%','召回路占比':'25%','NDCG@50':'0.623'}},
        {'project_id':'P003','title':'商品知识图谱增强 (KG Enhanced RecSys)','category':'知识图谱','progress':85,'status':'进行中','icon':'fa-project-diagram','color':'#8b5cf6','order_idx':3,
         'description':'构建商品属性知识图谱以增强语义理解与可解释性推荐：\n• 爬取并清洗得物商品属性数据（品牌/品类/风格/发售时间/价格带）\n• 图谱规模：200+品类节点，同款/相似款/替代品关系边\n• 应用：(1)推理类query语义召回 (2)解释性推荐理由 (3)长尾发现\n• 技术方案：TransE/RotatE嵌入 + GraphSAGE邻居聚合 + Attention打分\n• 长尾商品覆盖率从34.1%提升至48.7%，KG召回路占比14%',
         'tech_stack':['Neo4j/NetworkX','TransE','RotatE','GraphSAGE','DGL'],'metrics':{'长尾覆盖率':'+48.7%','KG召回路占比':'14%','图谱节点数':'200+'}},
        {'project_id':'P004','title':'冷启动流量分配策略 (LinUCB Bandit)','category':'冷启动','progress':70,'status':'进行中','icon':'fa-rocket','color':'#f59e0b','order_idx':4,
         'description':'针对新上架潮品的冷启动曝光优化：\n• 问题：新商品缺乏交互 → 无法协同召回 → 曝光不足 → 库存积压\n• 内容特征：CNN图像Embedding(R50) + BERT文本Embedding + 属性one-hot\n• LinUCB Contextual Bandit实现探索-利用均衡分配初始流量\n• A/B结果：新品首周有效曝光量提升40%，库存周转天数缩短',
         'tech_stack':['LinUCB','Bandit Algorithm','ResNet50','BERT'],'metrics':{'首周曝光量':'+40%','库存周转':'缩短','探索效率':'+35%'}},
        {'project_id':'P005','title':'离线评估体系 & A/B实验平台搭建','category':'评估体系','progress':90,'status':'进行中','icon':'fa-vial','color':'#ec4899','order_idx':5,
         'description':'构建完整的评估-实验闭环体系：\n• 离线指标集：NDCG@K / HitRate@K / Coverage / Diversity(ILS) / Novelty\n• 对齐验证：离线NDCG↑3% ≈ 在线CTR ↑8%（历史实验回测校准）\n• A/B实验平台：分层抽样(SRM检验) + 组隔离 + T-test显著性判断\n• 监控面板：实时CTR/QPS/延迟/GPU利用率 → 飞书告警推送\n• 框架已被组内复用为后续迭代标准基线',
         'tech_stack':['A/B Testing','SRM检验','T-test','Airflow','Grafana'],'metrics':{'实验周转':'-40%','复用团队数':'3+','文档产出':'2份'}},
    ]
    for p in projects_data:
        db.session.add(ResearchProject(**p))

    all_timelines = [
        ('P001','2026-03-15','完成用户行为数据分析，确定长短周期划分方案(短期7天/长期90天)','milestone',0),
        ('P001','2026-04-01','基于Transformer的多尺度门控融合机制设计评审通过','meeting',1),
        ('P001','2026-04-18','离线评测：User Embedding MRR@10达0.682，超基线12%','release',2),
        ('P001','2026-05-05','上线排序模型，浏览深度相对提升15%','milestone',3),
        ('P002','2026-03-20','完成SASRec基线模型复现，NDCG@50=0.589','milestone',0),
        ('P002','2026-04-05','引入BERT4Rec对比实验，推理成本高2x','meeting',1),
        ('P002','2026-04-20','SASRec离线评估达标 NDCG@50=0.623 HitRate@20=0.741','release',2),
        ('P002','2026-05-08','序列化召回路权占比调整至25%，CTR相对提升8.2%','milestone',3),
        ('P003','2026-04-15','商品属性数据爬取与清洗完成，覆盖200+品类','milestone',0),
        ('P003','2026-05-02','知识图谱Schema设计评审通过（同款/相似/替代三关系）','meeting',1),
        ('P003','2026-05-18','GraphSAGE邻居聚合+Attention打分模块开发完成','release',2),
        ('P003','2026-06-01','KG语义召回接入在线服务，长尾覆盖率提升至48.7%','milestone',3),
        ('P004','2026-04-25','LinUCB Bandit算法调研与原型验证完成','milestone',0),
        ('P004','2026-05-10','内容特征工程完成（CNN图像+BERT文本+属性one-hot）','meeting',1),
        ('P004','2026-05-28','LinUCB冷启动策略A/B实验启动','release',2),
        ('P005','2026-03-28','离线指标体系设计完成(NDCG/HitRate/Coverage/Diversity)','milestone',0),
        ('P005','2026-04-12','A/B实验平台SRM检验+统计显著性检验流程落地','meeting',1),
        ('P005','2026-05-22','离线-在线指标对齐校准完成，框架标准化文档输出','release',2),
        ('P005','2026-06-01','阶段总结：产出技术文档2份，做组内分享1次','milestone',3),
    ]
    for pid,date,event,etype,idx in all_timelines:
        db.session.add(ProjectTimeline(project_id=pid,event_date=date,event=event,event_type=etype,order_idx=idx))
    db.session.commit()
    print(f'  [seed] 5 个研究项目已创建 (含 {len(all_timelines)} 条时间线事件)')


def seed_architecture():
    if ArchitectureComponent.query.first() is not None:
        return
    arch_layers = [
        ('应用层 Application Layer','fa-desktop','得物App前端触点与业务场景入口',1,[('首页猜你喜欢','首页核心信息流推荐位千人千面个性化展示',['Flutter','个性化']),('详情页相关推荐','商品详情页底部基于当前商品语义扩展的推荐',['转化率']),('购物车搭配推荐','基于已有商品的场景化交叉销售Bundle推荐',['Bundle']),('搜索结果排序','Query意图识别后的个性化重排',['Query理解'])]),
        ('排序层 Ranking Layer','fa-sort-amount-down','预估CTR/CVR决定最终展示顺序',2,[('DNN双塔排序','User Tower x Item Tower内积打分',['PyTorch','Wide&Deep']),('多目标学习(MMoE/PESMM)','同时优化CTR/CVR/加购率共享底层表示',['ESMM','PLE']),('位置偏差修正','Position Embedding或IPW逆倾向加权',['Debias']),('实时特征更新','Redis分钟级刷新用户最近行为特征',['Redis','Flink'])]),
        ('召回层 Recall Layer','fa-filter','从亿级商品池筛选千级候选集',3,[('DNN双塔召回','User/Item ANN向量检索FAISS IVF-PQ，28%路权',['FAISS','ANN']),('SASRec序列召回','最近50次行为预测下一候选，25%路权',['SASRec','Transformer']),('Item-CF协同过滤','"买了还买"矩阵分解召回，18%路权',['ALS','Swing']),('KG语义召回','图谱路径推理+GraphSAGE聚合，14%路权',['GraphSAGE','TransE']),('向量检索(ANN)','图文Embedding相似度检索，10%路权',['Milvus','CLIP'])]),
        ('数据层 Data Layer','fa-database','特征工程与数据仓库基础设施',4,[('用户行为日志(CK)','亿级行为实时写入OLAP多维分析',['ClickHouse','Flink']),('商品属性数仓(Hive)','基础属性类目品牌结构化存储',['Hive','Spark']),('实时特征引擎(Redis)','用户实时状态特征KV缓存',['Redis']),('离线特征计算(Spark)','画像标签统计特征T+1批处理ETL',['Spark','Airflow'])]),
        ('基础设施 Infrastructure','fa-server','模型服务调度监控部署',5,[('TF Serving/TorchServe','深度学习模型gRPC高并发推理',['TF Serving']),('Kubernetes集群','容器化部署弹性扩缩容GPU调度',['K8s','Docker']),('Airflow工作流调度','特征ETL模型重训A/B实验DAG编排',['Airflow']),('Grafana监控大盘','CTR/QPS/延迟/GPU可视化告警',['Grafana'])]),
    ]
    for lname,licon,ldesc,lorder,components in arch_layers:
        for cidx,(cname,cdesc,ctags) in enumerate(components):
            db.session.add(ArchitectureComponent(layer_name=lname,layer_icon=licon,layer_desc=ldesc,layer_order=lorder,comp_name=cname,comp_desc=cdesc,comp_tags=ctags,order_in_layer=cidx))
    db.session.commit()
    print(f'  [seed] 技术架构 {len(arch_layers)} 层已创建')


def seed_knowledge_graph():
    if KnowledgeNode.query.first() is not None:
        return
    nodes = [
        ('n1','电商推荐系统','domain',30,'#3b82f6','得物App核心业务场景，支撑千万级DAU个性化推荐',400,80),('n2','召回阶段','domain',26,'#3b82f6','从亿级商品池筛选千级候选集',250,180),
        ('n3','排序阶段','domain',26,'#3b82f6','精细化预估CTR/CVR决定最终顺序',550,180),('n4','用户建模','domain',24,'#3b82f6','理解用户兴趣偏好与行为模式',150,300),
        ('n5','商品理解','domain',24,'#3b82f6','提取商品语义表征与属性特征',650,300),('n6','冷启动问题','domain',22,'#3b82f6','新商品/新用户缺乏历史数据的挑战',800,420),
        ('n7','SASRec序列推荐','tech',22,'#10b981','自注意力序列推荐模型捕获行为依赖',120,420),('n8','Transformer注意力','tech',20,'#10b981','Self-Attention用于用户兴趣提取序列建模',280,380),
        ('n9','知识图谱增强','tech',21,'#10b981','利用商品关系图谱提升语义可解释性',700,420),('n10','Bandit(LinUCB)','tech',20,'#10b981','上下文老虎机冷启动探索-利用均衡',850,320),
        ('n11','多目标任务学习','tech',19,'#10b981','ESMM/MMoE/PLE多目标联合优化框架',520,80),('n12','双塔模型(DNN Twin-Tower)','tech',20,'#10b981','UserxItem内积打分经典召回范式',220,260),
        ('n13','图神经网络(GNN)','tech',18,'#10b981','GraphSAGE/GAT用于商品关系传播邻居聚合',720,260),('n14','因果推断','tech',17,'#10b981','反事实推断消除选择偏差提升可靠性',450,480),
        ('n15','PyTorch','tool',18,'#ec4899','深度学习训练与推理主要框架',100,130),('n16','FAISS/Milvus','tool',17,'#ec4899','高性能近似最近邻向量检索引擎',350,260),
        ('n17','Spark/Flink','tool',17,'#ec4899','大规模批处理与流式计算引擎',300,400),('n18','Redis','tool',16,'#ec4899','在线特征存储与实时状态缓存',600,140),
        ('n19','ClickHouse','tool',16,'#ec4899','OLAP分析型数据库行为日志存储查询',750,140),('n20','TF Serving','tool',16,'#ec4899','生产级模型推理服务支持gRPC高并发',550,60),
        ('n21','Airflow','tool',15,'#ec4899','工作流调度与DAG编排工具',750,240),('n22','Kubernetes','tool',15,'#ec4899','容器编排与弹性扩缩容平台',900,140),
        ('n23','A/B实验平台','tool',16,'#ec4899','分流SRM检验显著性的端到端实验框架',450,360),('n24','Neo4j/NetworkX','tool',15,'#ec4899','图数据库与图计算库图谱存储查询',820,340),
    ]
    edges = [('n1','n2','包含阶段',1.0),('n1','n3','包含阶段',1.0),('n1','n4','核心任务',1.0),('n1','n5','核心任务',1.0),('n1','n6','面临挑战',0.95),('n2','n4','依赖于',0.95),('n2','n5','依赖于',0.9),('n3','n4','依赖于',0.9),('n3','n5','依赖于',0.85),('n6','n10','解决方案',1.0),('n6','n9','辅助解决',0.85),('n2','n7','核心算法',1.0),('n2','n12','核心算法',0.95),('n2','n9','补充召回',0.85),('n2','n16','检索引擎',0.9),('n3','n11','排序优化',0.95),('n3','n12','精排变体',0.8),('n3','n14','去偏方法',0.85),('n4','n8','建模方法',1.0),('n4','n7','序列建模',0.92),('n5','n9','结构化表达',0.95),('n5','n13','关系建模',0.88),('n7','n8','基于',1.0),('n9','n13','基于',0.95),('n12','n8','使用',0.85),('n13','n8','借鉴',0.75),('n7','n15','实现于',0.95),('n8','n15','实现于',0.9),('n12','n16','加速于',0.9),('n4','n17','特征计算',0.85),('n3','n18','特征读取',0.9),('n1','n19','日志存储',0.85),('n3','n20','模型服务',0.9),('n1','n21','调度',0.8),('n1','n22','部署',0.85),('n3','n23','评估方法',0.95),('n9','n24','图存储',1.0),('n13','n24','图计算',0.9)]
    for nd in nodes:
        db.session.add(KnowledgeNode(node_id=nd[0],label=nd[1],node_type=nd[2],size=nd[3],color=nd[4],detail=nd[5],x=float(nd[6]),y=float(nd[7])))
    for ed in edges:
        db.session.add(KnowledgeEdge(source=ed[0],target=ed[1],relation=ed[2],confidence=ed[3]))
    db.session.commit()
    print(f'  [seed] 知识图谱已创建 ({len(nodes)} 节点, {len(edges)} 条边)')


def seed_feishu():
    if FeishuFeature.query.first() is not None:
        return
    features = [('智能日报生成','每日自动汇总实验指标变化、项目进度、待办事项生成Markdown日报推送到指定群','active','fa-file-alt'),('实验异常告警','A/B实验关键指标出现显著负向漂移时即时推送卡片告警给负责人和mentor','active','fa-exclamation-triangle'),('论文追踪推送','基于RecSys/KDD/WWW顶会关键词匹配新论文摘要每周推送到群','planned','fa-book-open'),('模型性能监控','线上模型延迟/吞吐/QPS异常时自动触发告警附带诊断链接','active','fa-heartbeat'),('代码Review通知','Git MR/PR状态变更自动同步到飞书群支持快捷审批','disabled','fa-code-branch')]
    messages = [('2026-06-01 09:15','[实验告警] SASRec召回A/B组 CTR出现-1.2%负漂移(p<0.03)，请关注','alert'),('2026-05-31 18:00','[日报] 今日进展：KG语义召回接入完成，长尾覆盖率提升至48.7%；明日计划：完善冷启动A/B数据采集','report'),('2026-05-29 14:30','[论文推荐] KDD\'26 Spotlight: "Causal RecSys: Counterfactual Reasoning for Sequential Recommendation"','paper'),('2026-05-28 11:00','[项目更新] LinUCB冷启动策略A/B实验已启动预计运行2周当前分组均匀(SRMP=0.62)','info'),('2026-05-27 09:00','[日报] 序列化召回路权调至25%CTR累计+8.2%超出预期目标(+5%)','report'),('2026-05-25 16:45','[告警恢复] GPU集群利用率恢复正常(<85%)此前峰值持续约30分钟','alert'),('2026-05-24 10:20','[技术分享] 组内分享PPT已上传飞书云文档：《序列化召回在电商推荐中的实践》','info'),('2026-05-22 18:00','[周报汇总] 本周主要成果：(1)SASRec全量上线 (2)知识图谱构建完成 (3)离线评估框架标准化','report')]
    for fname,fdesc,fstatus,ficon in features:
        db.session.add(FeishuFeature(name=fname,description=fdesc,status=fstatus,icon=ficon))
    for mtime,mcontent,mtype in messages:
        db.session.add(FeishuMessage(time=mtime,content=mcontent,msg_type=mtype))
    db.session.commit()
    print(f'  [seed] 飞书集成已创建 ({len(features)} 功能, {len(messages)} 消息)')


def seed_all():
    print('[seed] 开始初始化种子数据...')
    seed_scholar_profile()
    seed_research_projects()
    seed_architecture()
    seed_knowledge_graph()
    seed_feishu()
    print('[seed] 全部种子数据初始化完成!')
