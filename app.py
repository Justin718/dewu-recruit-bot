"""
得物校招常见问题 AI 问答机器人 - 后端服务
支持关键词匹配 + TF-IDF 语义检索的智能问答
"""

import json
import os
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import jieba
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

app = Flask(__name__)
CORS(app)

# ============================================================
# 校招FAQ知识库 - 得物
# ============================================================
FAQ_KNOWLEDGE = [
    {
        "id": 1,
        "category": "投递须知",
        "keywords": ["投递", "网申", "简历", "申请", "报名", "注册", "填写", "提交", "职位", "网站", "官网"],
        "question_variants": [
            "如何进行网申投递？",
            "网申流程是什么？",
            "简历怎么投递？",
            "得物校招投递入口在哪？",
            "怎么投递得物校招？",
            "得物校招在哪里投简历？",
            "得物招聘官网地址是什么？"
        ],
        "answer": (
            "📝 得物校招网申投递流程：\n\n"
            "1️⃣ 访问得物校招官网：join.tencentmusic.com/campus\n"
            "2️⃣ 注册账号并登录\n"
            "3️⃣ 选择心仪岗位，仔细阅读职位JD\n"
            "4️⃣ 在线填写个人信息、教育背景、实习经历等\n"
            "5️⃣ 上传简历并提交申请\n\n"
            "💡 注意事项：\n"
            "• 每位同学只可投递1个岗位（与腾讯集团互不冲突，可同时分别投递）\n"
            "• 可选择最多3个感兴趣的业务线，提交后不可修改\n"
            "• 若没有特别倾向，可选择「无明确意向」，所有业务线面试官均可查看简历\n"
            "• 简历未在流程中时可随时修改是否服从调剂\n"
            "• 建议尽早投递，招满即止不设截止日期"
        )
    },
    {
        "id": 2,
        "category": "投递须知",
        "keywords": ["截止", "时间", "什么时候", "结束", "日期", "期限", "开始", "秋招", "春招"],
        "question_variants": [
            "得物校招什么时候截止？",
            "得物秋招什么时间结束？",
            "得物校招时间安排？",
            "得物春招什么时候开始？",
            "投递截止日期是哪天？",
            "得物校招还有多久截止？"
        ],
        "answer": (
            "📅 得物校招时间安排：\n\n"
            "【2026届秋招】\n"
            "• 网申开始：2025年8月7日\n"
            "• 线上面试：2025年8月上旬开始\n"
            "• Offer发放：预计2025年10月上旬开始\n"
            "• 截止时间：不设置网申截止时间，招满即止\n\n"
            "⚠️ 温馨提示：\n"
            "• 得物不设截止日期，但岗位先到先得\n"
            "• 建议尽早投递，前期HC更多\n"
            "• 具体时间以得物校招官网（join.tencentmusic.com/campus）公告为准\n"
            "• 建议关注「得物娱乐招聘」公众号获取最新动态"
        )
    },
    {
        "id": 3,
        "category": "招聘对象",
        "keywords": ["应届", "毕业生", "毕业时间", "届", "招聘对象", "毕业", "学历", "专业", "2026"],
        "question_variants": [
            "得物校招面向哪些人？",
            "什么样的毕业生可以参加得物校招？",
            "得物校招对毕业时间有什么要求？",
            "非应届可以投递吗？",
            "研究生可以投递吗？",
            "得物校招对学历和专业有限制吗？",
            "双非可以投递得物吗？"
        ],
        "answer": (
            "🎓 得物校招招聘对象：\n\n"
            "【2026届毕业生要求】\n"
            "面向2025年1月 - 2026年12月期间毕业的同学\n\n"
            "【毕业时间判定标准】\n"
            "• 中国大陆（内地）以毕业证日期为准\n"
            "• 中国港澳台及海外地区以学位证日期为准\n\n"
            "【学历与专业】\n"
            "• 开放本科、硕士、博士等多学历层次的岗位\n"
            "• 不同岗位有不同的专业偏好，具体以职位JD为准\n"
            "• 部分技术岗位对专业有一定要求\n"
            "• 设计、产品、市场等岗位对专业限制相对宽松\n\n"
            "【工作地点】\n"
            "主要城市：深圳（总部）、北京、上海、广州等\n"
        )
    },
    {
        "id": 4,
        "category": "岗位类别",
        "keywords": ["岗位", "职位", "方向", "类别", "职类", "开放", "有什么岗位", "技术", "产品", "设计", "内容", "市场"],
        "question_variants": [
            "得物校招有哪些岗位？",
            "得物开放了哪些职类？",
            "得物校招岗位类别有哪些？",
            "得物有哪些技术岗位？",
            "非技术类岗位有哪些？",
            "得物校招什么岗位比较多？"
        ],
        "answer": (
            "💼 得物校招开放岗位类别：\n\n"
            "💻 技术类：后端开发、前端开发、客户端开发、算法工程师、数据工程师、测试工程师、运维工程师、音视频技术等\n"
            "📱 产品类：产品经理、产品运营、数据产品等\n"
            "🎨 设计类：视觉设计、UI/UX设计、交互设计、多媒体设计等\n"
            "📝 内容类：内容运营、音乐编辑、音乐企划等\n"
            "📣 市场类：品牌营销、市场推广、商务拓展、品牌公关等\n"
            "⚙️ 专业类：安全策略、人力资源、财务管理、法务合规等\n\n"
            "💡 特色岗位：\n"
            "• 音乐生成算法工程师\n"
            "• 音质优化算法工程师\n"
            "• 语音合成算法工程师\n"
            "• 音频技术研究员\n\n"
            "💡 具体岗位信息请前往得物校招官网 join.tencentmusic.com/campus 查看"
        )
    },
    {
        "id": 5,
        "category": "内推",
        "keywords": ["内推", "推荐", "内部推荐", "referral", "内推码", "学长", "学姐", "校园大使", "优先筛选"],
        "question_variants": [
            "得物校招有内推吗？",
            "怎么参加得物内推？",
            "内推有什么作用？",
            "得物内推码在哪里获取？",
            "内推和普通投递有什么区别？",
            "可以内推多个岗位吗？",
            "已经网申了还能内推吗？",
            "内推流程被结束了怎么办？"
        ],
        "answer": (
            "🔗 得物校招内推详解：\n\n"
            "【内推的作用】\n"
            "参与内推的简历将获得优先筛选的资格，有助于更快进入面试环节\n\n"
            "【如何参加内推】\n"
            "1. 寻找周围在职得物的学长学姐或校园大使\n"
            "2. 在投递简历时填写内推码\n"
            "3. 完成内推后简历将获得优先筛选资格\n\n"
            "【内推规则】\n"
            "• 得物与腾讯集团的招聘相互独立，可同时投递\n"
            "• 每位同学只可投递1个岗位\n"
            "• 建议通过牛客网、知乎等平台寻找在职员工获取内推码\n"
            "• 也可以通过关注「得物娱乐招聘」公众号获取相关内推信息\n\n"
            "💡 内推不等于内定，最终录取仍需通过正常面试流程"
        )
    },
    {
        "id": 6,
        "category": "笔试与测评",
        "keywords": ["笔试", "测评", "在线", "考试", "题目", "准备", "测试", "行测", "coding", "算法题"],
        "question_variants": [
            "得物校招笔试考什么？",
            "得物笔试怎么准备？",
            "得物笔试是什么形式？",
            "得物有测评吗？",
            "得物笔试用什么平台？",
            "笔试需要注意什么？",
            "错过了笔试怎么办？",
            "笔试通过后多久面试？"
        ],
        "answer": (
            "📝 得物校招笔试与测评：\n\n"
            "【笔试形式】\n"
            "• 技术岗位：通常需要参加在线编程笔试，考察算法和编程能力\n"
            "• 非技术岗位：一般参加在线测评，考察逻辑、数理、语文等综合能力\n"
            "• 具体形式和平台以邮件和短信通知为准\n\n"
            "【考前准备】\n"
            "• 准备好带有摄像头的电脑设备\n"
            "• 下载谷歌最新版Chrome浏览器\n"
            "• 提前测试好网络环境，避免断网\n"
            "• 选择安静的环境参加考试\n"
            "• 技术岗提前刷LeetCode、牛客网等平台的算法题\n\n"
            "【笔试相关Q&A】\n"
            "• 笔试通过后一般1-2周内会通知面试\n"
            "• 部分岗位除了笔试还有测评环节，以邮件通知为准\n"
            "• 注意查收邮件和短信，不要错过笔试通知\n"
            "• 如有疑问可通过校招官网联系HR"
        )
    },
    {
        "id": 7,
        "category": "面试",
        "keywords": ["面试", "面经", "几轮", "流程", "HR", "技术面", "群面", "单面", "面试官", "线上"],
        "question_variants": [
            "得物校招面试有几轮？",
            "得物面试流程是什么？",
            "得物面试怎么准备？",
            "面试时间可以改吗？",
            "得物面试注意事项？",
            "面试结果多久出来？",
            "面试反馈怎么查？"
        ],
        "answer": (
            "🎯 得物校招面试详情：\n\n"
            "【面试形式】\n"
            "得物校招采用线上面试的形式，一般通过视频会议进行\n\n"
            "【面试轮次】\n"
            "• 技术岗位：一般为2-3轮技术面 + 1轮HR面\n"
            "  技术面考察项目经验、算法基础、专业知识和系统设计能力\n"
            "• 非技术岗位：一般为1-2轮业务面 + 1轮HR面\n"
            "  业务面考察逻辑思维、行业认知、沟通表达等综合能力\n\n"
            "【面试时间调整】\n"
            "接到面试邀请后，如需更改时间：\n"
            "查看邮件中的面试邀请详情，联系HR进行时间调整\n\n"
            "【面试注意事项】\n"
            "• 提前5-10分钟上线测试设备和网络\n"
            "• 保证安静良好的面试环境\n"
            "• 技术岗如进行在线coding，注意对题目严格保密\n"
            "• 准备2-3个向面试官提问的好问题\n\n"
            "【投递进度查询】\n"
            "同学可在校招官网中查看自己的投递进度。\n"
            "面试反馈一般在1-2周内，各职位招聘流程有所不同，请耐心等待。"
        )
    },
    {
        "id": 8,
        "category": "投递进度",
        "keywords": ["进度", "查询", "投递进展", "状态", "结果", "流程终止", "流程中", "等待"],
        "question_variants": [
            "怎么查询投递进度？",
            "我的投递进展怎么样？",
            "得物投递状态怎么看？",
            "流程终止了怎么办？",
            "投递后多久有消息？",
            "面试反馈多久出？"
        ],
        "answer": (
            "📋 得物校招投递进度查询：\n\n"
            "【查询方式】\n"
            "登录得物校招官网 join.tencentmusic.com/campus，\n"
            "进入个人中心即可查看投递进度\n\n"
            "【进度状态说明】\n"
            "• 简历筛选：简历正在被HR和业务部门查看\n"
            "• 面试中：已进入面试环节\n"
            "• Offer沟通：已通过面试，进入Offer阶段\n"
            "• 流程结束：该岗位的投递流程已结束\n\n"
            "【常见问题】\n"
            "• 投递后一般1-4周内有反馈，具体视岗位需求而定\n"
            "• 面试反馈尽量控制在1-2周内\n"
            "• 各职位招聘流程不同，无法给到统一的时间答复\n"
            "• 请耐心等待后续邮件和短信通知\n\n"
            "💡 建议保持手机畅通，及时查收邮件和短信"
        )
    },
    {
        "id": 9,
        "category": "工作城市",
        "keywords": ["城市", "地点", "工作地点", "深圳", "北京", "上海", "广州", "去哪里", "base", "总部"],
        "question_variants": [
            "得物校招有哪些工作城市？",
            "得物在哪些城市有岗位？",
            "得物总部在哪里？",
            "得物工作地点可以选择吗？",
            "得物校招开放了几个城市？"
        ],
        "answer": (
            "📍 得物校招工作地点：\n\n"
            "【主要办公城市】\n"
            "• 深圳（总部，南山区科兴科学园）\n"
            "• 北京\n"
            "• 上海\n"
            "• 广州\n\n"
            "【各业务分布】\n"
            "• QQ音乐：深圳、北京\n"
            "• 酷狗音乐：广州\n"
            "• 酷我音乐：北京\n"
            "• 全民K歌：深圳\n\n"
            "💡 具体岗位的工作地点以校招官网发布的职位JD为准。\n"
            "投递时可在系统中选择期望工作城市。"
        )
    },
    {
        "id": 10,
        "category": "关于得物",
        "keywords": ["得物", "公司", "介绍", "是什么", "做啥", "业务", "平台", "TME", "QQ音乐", "酷狗", "酷我", "全民K歌"],
        "question_variants": [
            "得物是什么公司？",
            "得物是做什么的？",
            "得物的业务模式是什么？",
            "得物公司怎么样？",
            "得物的公司规模？",
            "TME是什么？"
        ],
        "answer": (
            "🏢 关于得物娱乐集团（TME）：\n\n"
            "得物娱乐集团（NYSE: TME）是中国在线音乐娱乐服务领航者，\n"
            "提供在线音乐和以音乐为核心的社交娱乐两大服务。\n\n"
            "【旗下产品】\n"
            "🎵 QQ音乐 - 综合音乐流媒体平台\n"
            "🎵 酷狗音乐 - 国民级音乐平台\n"
            "🎵 酷我音乐 - 高品质音乐服务\n"
            "🎤 全民K歌 - 国民级在线K歌社交平台\n"
            "📚 懒人听书 - 有声阅读平台\n\n"
            "【公司实力】\n"
            "• 2018年12月于纽约证券交易所上市\n"
            "• 总月活用户数超过8亿\n"
            "• 拥有中国最大的音乐内容库\n"
            "• 总部位于深圳南山区科兴科学园\n\n"
            "【企业文化】\n"
            "• 使命：用音乐点亮生活\n"
            "• 注重技术驱动音乐产业创新\n"
            "• 开放、包容、创新的工程师文化\n"
            "• 为年轻人提供广阔的成长空间"
        )
    },
    {
        "id": 11,
        "category": "实习生招聘",
        "keywords": ["实习", "intern", "暑期实习", "日常实习", "转正", "实习offer"],
        "question_variants": [
            "得物有实习生招聘吗？",
            "得物暑期实习怎么投？",
            "得物实习可以转正吗？",
            "实习生校招流程？",
            "得物有实习岗位吗？"
        ],
        "answer": (
            "💼 得物实习生招聘：\n\n"
            "得物每年都会开放暑期实习生招聘，面向下一届毕业生。\n\n"
            "【暑期实习流程】\n"
            "• 面向对象：下一届毕业生（如2027届）\n"
            "• 投递时间：一般3月-5月\n"
            "• 面试时间：滚动面试\n"
            "• 实习入职：5月-7月\n"
            "• 转正答辩：8月-9月\n"
            "• 发放正式校招Offer：9月-10月\n\n"
            "【注意事项】\n"
            "• 暑期实习仅面向对应毕业时间的同学\n"
            "• 实习表现优异可获得转正机会\n"
            "• 通过得物校招官网 join.tencentmusic.com/campus 投递\n"
            "• 实习期间表现突出可免去部分校招流程\n\n"
            "💡 建议大三/研二的同学重点关注暑期实习机会"
        )
    },
    {
        "id": 12,
        "category": "简历准备",
        "keywords": ["简历", "模板", "格式", "写简历", "内容", "优化", "经历", "STAR"],
        "question_variants": [
            "得物校招简历怎么写？",
            "投递得物简历要注意什么？",
            "得物校招简历有什么要求？",
            "简历需要哪些内容？",
            "得物简历筛选看重什么？"
        ],
        "answer": (
            "📄 得物校招简历建议：\n\n"
            "【简历核心模块】\n"
            "1. 基本信息：姓名、联系方式、邮箱、意向城市\n"
            "2. 教育背景：学校、学历、专业、GPA（如优异可标注）\n"
            "3. 实习/项目经历：最重要的模块，占简历篇幅的40%-50%\n"
            "4. 专业技能：编程语言、开发工具、设计软件等\n"
            "5. 获奖/证书：有含金量的竞赛获奖或证书\n"
            "6. 作品集链接（设计/内容岗必备）\n\n"
            "【写在得物简历的加分项】\n"
            "• 对音乐行业有热情，了解旗下产品\n"
            "• 有音频/音乐相关项目经验\n"
            "• 使用STAR法则描述经历（情境-任务-行动-结果）\n"
            "• 用数据量化成果（如\u201c用户增长20%\u201d）\n"
            "• 展示与岗位直接相关的技能和作品\n\n"
            "💡 建议投递前去官网深入了解得物的业务和技术方向"
        )
    },
    {
        "id": 13,
        "category": "培养与发展",
        "keywords": ["培养", "发展", "晋升", "成长", "培训", "新人", "入职", "职业发展"],
        "question_variants": [
            "得物校招生培养体系怎么样？",
            "入职后有什么培训？",
            "得物晋升机制是怎样的？",
            "校招生在得物的发展前景？",
            "得物新人培训？"
        ],
        "answer": (
            "🌱 得物校招生培养与发展：\n\n"
            "得物为校招生提供了完善的成长体系：\n\n"
            "【入职培训】\n"
            "• 系统的新员工入职培训，了解公司业务和文化\n"
            "• 配备专属导师（Mentor），一对一指导\n"
            "• 技术培训、业务培训双线并行\n\n"
            "【成长路径】\n"
            "• 新人期（0-6个月）：熟悉业务，在导师指导下完成任务\n"
            "• 成长期（6-18个月）：独立负责模块，积累项目经验\n"
            "• 进阶期（1.5年后）：向高级工程师/资深产品等方向发展\n\n"
            "【职业发展双通道】\n"
            "• 专业通道（P序列）：初级→高级→资深→专家→科学家\n"
            "• 管理通道（M序列）：团队Leader→总监→VP\n\n"
            "💡 得物注重年轻人的成长，提供丰富的学习资源和晋升机会，\n"
            "鼓励创新，支持内部创业和技术探索。"
        )
    },
    {
        "id": 14,
        "category": "联系方式",
        "keywords": ["联系", "邮箱", "电话", "客服", "咨询", "hr", "校招邮箱", "公众号"],
        "question_variants": [
            "得物校招怎么联系？",
            "得物招聘邮箱是什么？",
            "有问题找谁？",
            "得物HR联系方式？",
            "得物校招咨询电话？"
        ],
        "answer": (
            "📬 得物校招联系方式：\n\n"
            "【校招官网】\n"
            "join.tencentmusic.com/campus\n\n"
            "【公众号】\n"
            "关注「得物娱乐招聘」公众号，获取最新招聘动态\n\n"
            "【其他渠道】\n"
            "• 牛客网：关注得物校招话题\n"
            "• 知乎：搜索「得物校招」获取面经\n"
            "• 各大高校BBS和就业信息网\n\n"
            "💡 建议优先通过校招官网和公众号获取信息，\n"
            "面试相关疑问可通过面试邀请邮件中的联系方式与HR沟通。"
        )
    },
    {
        "id": 15,
        "category": "Offer与签约",
        "keywords": ["offer", "签约", "三方", "薪资", "待遇", "工资", "薪酬", "福利"],
        "question_variants": [
            "得物校招offer什么时候发？",
            "得物校招薪资待遇怎么样？",
            "得物offer怎么签？",
            "得物校招薪资水平？",
            "得物福利怎么样？"
        ],
        "answer": (
            "📋 得物校招Offer与签约：\n\n"
            "【Offer发放时间】\n"
            "• 秋招：预计2025年10月上旬开始发放Offer\n"
            "• 滚动发放，先通过先发Offer\n\n"
            "【招聘全流程】\n"
            "网申/内推 → 笔试/测评 → 线上面试 → Offer发放 → 签约入职\n\n"
            "【薪酬福利（参考）】\n"
            "• 提供具有竞争力的薪酬待遇\n"
            "• 五险一金 + 补充商业保险\n"
            "• 免费早餐、下午茶、夜宵\n"
            "• 健身房、理疗室等配套设施\n"
            "• 丰富的员工活动和音乐相关福利\n\n"
            "💡 温馨提示：\n"
            "• 具体薪资待遇以Offer通知为准\n"
            "• 建议关注校招官网和邮件通知\n"
            "• 有任何疑问可通过校招官网联系HR"
        )
    },
    {
        "id": 16,
        "category": "面试准备",
        "keywords": ["自我介绍", "面试技巧", "怎么准备面试", "面试经验", "面经", "反问", "准备"],
        "question_variants": [
            "得物面试怎么准备？",
            "得物面试自我介绍怎么说？",
            "得物面试有什么技巧？",
            "得物面试要注意什么？",
            "面试最后可以问什么？"
        ],
        "answer": (
            "🎯 得物面试准备建议：\n\n"
            "【面试前准备】\n"
            "1. 深入了解得物的产品矩阵（QQ音乐、酷狗、酷我、全民K歌等）\n"
            "2. 体验得物各产品，思考产品体验和可优化点\n"
            "3. 了解在线音乐行业趋势、竞品分析\n"
            "4. 仔细阅读投递岗位的JD，梳理匹配的经历\n"
            "5. 准备1分钟/3分钟自我介绍（突出与岗位的匹配度）\n"
            "6. 用STAR法则梳理简历上的每个项目经历\n"
            "7. 技术岗：刷LeetCode热题100，复习基础知识\n"
            "8. 提前5-10分钟上线测试设备和网络\n\n"
            "【面试中注意】\n"
            "• 保证安静良好的面试环境\n"
            "• 技术岗如进行在线coding，注意对题目严格保密\n"
            "• 真诚回答，展现对音乐和技术的热爱\n"
            "• 提前准备2-3个有深度的问题反问面试官\n\n"
            "【时间调整】\n"
            "如需更改面试时间，查看邮件中的HR联系方式联系即可。"
        )
    },
    {
        "id": 17,
        "category": "投递规则",
        "keywords": ["几个职位", "投递几个", "最多投递", "改志愿", "改简历", "改职位", "业务线", "志愿", "调剂"],
        "question_variants": [
            "得物校招可以投几个岗位？",
            "最多能投几个职位？",
            "投递后能改简历吗？",
            "业务线志愿怎么选？",
            "投递后能改职位吗？",
            "得物和腾讯能不能同时投？"
        ],
        "answer": (
            "📋 得物校招投递规则：\n\n"
            "【投递数量】\n"
            "每位同学只可投递1个岗位\n\n"
            "【业务线志愿】\n"
            "• 可选择最多3个感兴趣的业务线\n"
            "• 提交简历后业务线志愿不可修改\n"
            "• 若没有特别倾向，选择「无明确意向」\n"
            "• 所选业务线的面试官会优先看到简历\n\n"
            "【岗位修改】\n"
            "• 如简历未在流程中，可以修改岗位\n"
            "• 简历进入流程后不可修改职位\n"
            "• 投递前请仔细确认岗位选择\n\n"
            "【与腾讯集团的关系】\n"
            "• 得物（TME）是独立上市公司\n"
            "• 得物与腾讯集团的招聘相互独立\n"
            "• 可同时分别投递得物和腾讯集团的岗位\n"
            "• 两边互不影响，多一次机会！\n\n"
            "【调剂】\n"
            "• 简历未在流程中时可随时修改是否服从调剂\n"
            "• 修改为「服从调剂」后，所有业务线面试官均可查看简历"
        )
    },
]

# ============================================================
# 构建检索系统
# ============================================================

# 准备TF-IDF语料：每个FAQ的question_variants作为训练数据
all_questions = []
question_to_faq_index = []

for idx, faq in enumerate(FAQ_KNOWLEDGE):
    for q in faq["question_variants"]:
        all_questions.append(q)
        question_to_faq_index.append(idx)

# 对问题文本进行分词处理（用于TF-IDF）
def tokenize_chinese(text):
    """中文分词"""
    return " ".join(jieba.cut(text))

# 构建TF-IDF向量器
tokenized_questions = [tokenize_chinese(q) for q in all_questions]
vectorizer = TfidfVectorizer(ngram_range=(1, 2), max_features=500)
tfidf_matrix = vectorizer.fit_transform(tokenized_questions)


def keyword_match_score(query, faq):
    """计算关键词匹配分数"""
    query_lower = query.lower()
    score = 0
    matched_keywords = []
    
    for kw in faq["keywords"]:
        if kw.lower() in query_lower:
            score += 3
            matched_keywords.append(kw)
    
    # 检查问题变体中是否有相似问题
    for variant in faq["question_variants"]:
        # 计算简单重叠度
        query_words = set(jieba.cut(query))
        variant_words = set(jieba.cut(variant))
        overlap = len(query_words & variant_words) / max(len(variant_words), 1)
        if overlap > 0.5:
            score += 2 * overlap
    
    return score, matched_keywords


def semantic_search(query, top_k=5):
    """使用TF-IDF进行语义检索"""
    query_tokenized = tokenize_chinese(query)
    query_vector = vectorizer.transform([query_tokenized])
    similarities = cosine_similarity(query_vector, tfidf_matrix).flatten()
    
    # 获取top-k相似度的问题及其对应FAQ
    top_indices = np.argsort(similarities)[::-1][:top_k]
    
    results = []
    seen_faq_ids = set()
    
    for idx in top_indices:
        faq_idx = question_to_faq_index[idx]
        if faq_idx not in seen_faq_ids:
            seen_faq_ids.add(faq_idx)
            results.append({
                "faq": FAQ_KNOWLEDGE[faq_idx],
                "similarity": float(similarities[idx]),
                "matched_question": all_questions[idx]
            })
            if len(results) >= 3:
                break
    
    return results


def find_best_answer(query):
    """综合关键词匹配和语义检索找到最佳答案"""
    query = query.strip()
    
    # 1. 关键词匹配
    best_keyword_score = 0
    best_keyword_faq = None
    best_matched_kw = []
    
    for faq in FAQ_KNOWLEDGE:
        score, matched_kw = keyword_match_score(query, faq)
        if score > best_keyword_score:
            best_keyword_score = score
            best_keyword_faq = faq
            best_matched_kw = matched_kw
    
    # 2. 语义检索
    semantic_results = semantic_search(query)
    
    # 3. 综合判断
    # 如果关键词匹配很高（>=6），直接返回
    if best_keyword_score >= 6 and best_keyword_faq:
        return {
            "answer": best_keyword_faq["answer"],
            "category": best_keyword_faq["category"],
            "confidence": "high",
            "method": "keyword_match",
            "matched_keywords": best_matched_kw,
            "related_questions": []
        }
    
    # 如果语义检索有高相似度（>0.3）的结果
    if semantic_results and semantic_results[0]["similarity"] > 0.2:
        top_result = semantic_results[0]
        related = [r["faq"]["question_variants"][0] for r in semantic_results[1:3]] if len(semantic_results) > 1 else []
        
        return {
            "answer": top_result["faq"]["answer"],
            "category": top_result["faq"]["category"],
            "confidence": "high" if top_result["similarity"] > 0.4 else "medium",
            "method": f"semantic_search (similarity: {top_result['similarity']:.3f})",
            "matched_keywords": [],
            "related_questions": related
        }
    
    # 4. 关键词有一定匹配但不够高
    if best_keyword_score >= 2 and best_keyword_faq:
        return {
            "answer": best_keyword_faq["answer"],
            "category": best_keyword_faq["category"],
            "confidence": "medium",
            "method": "weak_keyword_match",
            "matched_keywords": best_matched_kw,
            "related_questions": []
        }
    
    # 5. 兜底回答：建议用户换种方式提问或给出通用建议
    return {
        "answer": get_fallback_answer(query),
        "category": "通用",
        "confidence": "low",
        "method": "fallback",
        "matched_keywords": [],
        "related_questions": get_suggested_questions()
    }


def get_fallback_answer(query):
    """当无法精确匹配时的兜底回答"""
    # 检查是否在问校招相关
    campus_keywords = ["校招", "秋招", "春招", "应届", "招聘", "求职", "工作", "公司", "企业", "offer", "简历", "面试", "笔试"]
    is_campus_related = any(kw in query for kw in campus_keywords)
    
    if is_campus_related:
        return (
            "🤔 您的问题我已经收到了，但目前我还在学习中，暂时无法给出特别精准的回答。\n\n"
            "💡 建议您：\n"
            "• 尝试换一种方式描述您的问题\n"
            "• 选择更具体的关键词提问\n"
            "• 参考下面为您推荐的热门问题\n\n"
            "您也可以关注「得物娱乐招聘」公众号获取最新信息~"
        )
    else:
        return (
            "👋 您好！我是得物校招问答助手，专注于解答得物校园招聘相关问题。\n\n"
            "我可以帮您解答：\n"
            "📝 网申投递  📄 简历制作  ✍️ 笔试准备\n"
            "🎯 面试技巧  💰 Offer选择  💼 实习经验\n"
            "🔗 内推攻略  🏢 公司产品  📍 工作城市\n\n"
            "请向我提问校招相关问题，我会尽力为您解答！"
        )


def get_suggested_questions():
    """获取推荐问题列表"""
    return [
        "如何进行网申？",
        "校招面试一般有几轮？",
        "得物和腾讯可以同时投递吗？",
        "简历怎么写比较好？",
        "内推有用吗？",
        "得物有哪些岗位？"
    ]


# ============================================================
# 路由
# ============================================================

@app.route('/')
def index():
    """主页"""
    return render_template('index.html')


@app.route('/api/chat', methods=['POST'])
def chat():
    """聊天接口"""
    data = request.get_json()
    if not data or 'question' not in data:
        return jsonify({"error": "请提供question参数"}), 400
    
    question = data['question'].strip()
    if not question:
        return jsonify({"error": "问题不能为空"}), 400
    
    # 查找最佳答案
    result = find_best_answer(question)
    
    return jsonify({
        "question": question,
        "answer": result["answer"],
        "category": result["category"],
        "confidence": result["confidence"],
        "related_questions": result.get("related_questions", []),
        "suggested_questions": get_suggested_questions() if result["confidence"] == "low" else []
    })


@app.route('/api/suggestions', methods=['GET'])
def suggestions():
    """获取推荐问题"""
    return jsonify({
        "suggestions": get_suggested_questions(),
        "categories": list(set(faq["category"] for faq in FAQ_KNOWLEDGE))
    })


@app.route('/api/faq', methods=['GET'])
def get_faq():
    """获取FAQ列表"""
    category = request.args.get('category', '')
    if category:
        filtered = [faq for faq in FAQ_KNOWLEDGE if faq["category"] == category]
    else:
        filtered = FAQ_KNOWLEDGE
    
    # 只返回简要信息，不包含完整answer
    brief = [{"id": f["id"], "category": f["category"], "question": f["question_variants"][0]} for f in filtered]
    return jsonify({"faqs": brief, "total": len(brief)})


if __name__ == '__main__':
    import sys
    import io
    if sys.stdout.encoding != 'utf-8':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
    print("得物校招AI问答机器人启动中...")
    print("访问地址: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
