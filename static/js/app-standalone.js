/* ============================================ */
/* 得物校招AI问答机器人 - 纯前端版            */
/* FAQ知识库 + 关键词匹配 + 语义检索             */
/* ============================================ */

(function () {
    'use strict';

    // ============================================
    // FAQ 知识库
    // ============================================
    const var FAQ_KNOWLEDGE = [
    {
        id: 1,
        category: "投递须知",
        keywords: ["投递", "网申", "简历", "申请", "报名", "注册", "填写", "提交", "职位", "网站", "官网"],
        question_variants: [
            "如何进行网申投递？",
            "网申流程是什么？",
            "简历怎么投递？",
            "得物校招投递入口在哪？",
            "怎么投递得物校招？",
            "得物校招在哪里投简历？",
            "得物招聘官网地址是什么？"
        ],
        answer: "📝 得物校招网申投递流程：\n\n" +
            "1️⃣ 访问得物校招官网：campus.dewu.com\n" +
            "2️⃣ 注册账号并登录\n" +
            "3️⃣ 选择心仪岗位，仔细阅读职位JD\n" +
            "4️⃣ 在线填写个人信息、教育背景、实习经历等\n" +
            "5️⃣ 上传简历并提交申请\n\n" +
            "💡 注意事项：\n" +
            "• 每位同学最多可投递2个岗位\n" +
            "• 简历投递后请认真填写，提交后部分信息不可修改\n" +
            "• 建议使用电脑端进行投递，体验更好\n" +
            "• 提前准备好个人简历（PDF格式），确保信息准确完整\n" +
            "• 建议尽早投递，岗位招满即止"
    },
    {
        id: 2,
        category: "投递须知",
        keywords: ["截止", "时间", "什么时候", "结束", "日期", "期限", "开始", "秋招", "春招"],
        question_variants: [
            "得物校招什么时候截止？",
            "得物秋招什么时间结束？",
            "得物校招时间安排？",
            "得物春招什么时候开始？",
            "投递截止日期是哪天？",
            "得物校招还有多久截止？"
        ],
        answer: "📅 得物校招时间安排：\n\n" +
            "【2026届秋招】\n" +
            "• 网申开始：2025年8月中旬\n" +
            "• 在线笔试：2025年8月下旬 - 10月\n" +
            "• 面试安排：2025年9月上旬开始\n" +
            "• Offer发放：2025年9月下旬开始\n" +
            "• 截止时间：2025年10月底（具体以官网为准）\n\n" +
            "【2026届春招】\n" +
            "• 网申开始：2026年2月下旬\n" +
            "• 面试安排：2026年3月-4月\n" +
            "• Offer发放：滚动发放\n\n" +
            "⚠️ 温馨提示：\n" +
            "• 秋招是得物最大规模的校招，岗位最多\n" +
            "• 建议尽早投递，前期HC更多\n" +
            "• 具体时间以得物校招官网（campus.dewu.com）公告为准\n" +
            "• 关注「得物招聘」公众号获取最新动态"
    },
    {
        id: 3,
        category: "招聘对象",
        keywords: ["应届", "毕业生", "毕业时间", "届", "招聘对象", "毕业", "学历", "专业", "2026"],
        question_variants: [
            "得物校招面向哪些人？",
            "什么样的毕业生可以参加得物校招？",
            "得物校招对毕业时间有什么要求？",
            "非应届可以投递吗？",
            "研究生可以投递吗？",
            "得物校招对学历和专业有限制吗？",
            "双非可以投递得物吗？"
        ],
        answer: "🎓 得物校招招聘对象：\n\n" +
            "【2026届毕业生要求】\n" +
            "面向2025年9月 - 2026年8月期间毕业的同学\n\n" +
            "【毕业时间判定标准】\n" +
            "• 中国大陆（内地）以毕业证日期为准\n" +
            "• 中国港澳台及海外地区以学位证日期为准\n\n" +
            "【学历与专业】\n" +
            "• 开放本科、硕士、博士等多学历层次的岗位\n" +
            "• 不同岗位有不同的专业偏好，具体以职位JD为准\n" +
            "• 技术类岗位对计算机相关专业有一定要求\n" +
            "• 产品、运营、设计等岗位对专业限制相对宽松\n" +
            "• 得物更看重能力和潜力，不会因学校背景一刀切\n\n" +
            "【工作地点】\n" +
            "主要城市：上海（总部）、北京、杭州、广州等"
    },
    {
        id: 4,
        category: "岗位类别",
        keywords: ["岗位", "职位", "方向", "类别", "职类", "开放", "有什么岗位", "技术", "产品", "设计", "内容", "市场"],
        question_variants: [
            "得物校招有哪些岗位？",
            "得物开放了哪些职类？",
            "得物校招岗位类别有哪些？",
            "得物有哪些技术岗位？",
            "非技术类岗位有哪些？",
            "得物校招什么岗位比较多？"
        ],
        answer: "💼 得物校招开放岗位类别：\n\n" +
            "💻 技术类：后端开发、前端开发、客户端开发（iOS/Android）、算法工程师、数据工程师、测试工程师、运维工程师、安全工程师等\n" +
            "📱 产品类：产品经理、数据产品、策略产品等\n" +
            "🎨 设计类：视觉设计、UI/UX设计、交互设计、品牌设计等\n" +
            "📊 运营类：电商运营、内容运营、社区运营、用户运营等\n" +
            "📣 市场类：品牌营销、市场推广、商务拓展、公关传播等\n" +
            "🔍 供应链类：采购、仓储、物流、供应链管理等\n" +
            "⚙️ 职能类：人力资源、财务管理、法务合规、行政管理等\n\n" +
            "💡 特色岗位：\n" +
            "• 商品鉴定师（得物核心特色岗位）\n" +
            "• 图像识别算法工程师（AI鉴定方向）\n" +
            "• 供应链算法工程师\n" +
            "• 潮流趋势研究员\n\n" +
            "💡 具体岗位信息请前往得物校招官网 campus.dewu.com 查看"
    },
    {
        id: 5,
        category: "内推",
        keywords: ["内推", "推荐", "内部推荐", "referral", "内推码", "学长", "学姐", "校园大使", "优先筛选"],
        question_variants: [
            "得物校招有内推吗？",
            "怎么参加得物内推？",
            "内推有什么作用？",
            "得物内推码在哪里获取？",
            "内推和普通投递有什么区别？",
            "可以内推多个岗位吗？",
            "已经网申了还能内推吗？",
            "内推流程被结束了怎么办？"
        ],
        answer: "🔗 得物校招内推详解：\n\n" +
            "【内推的作用】\n" +
            "参与内推的简历将获得优先筛选的资格，有助于更快进入面试环节\n\n" +
            "【如何参加内推】\n" +
            "1. 寻找周围在得物工作的学长学姐或校园大使\n" +
            "2. 在投递简历时填写内推码\n" +
            "3. 完成内推后简历将获得优先筛选资格\n\n" +
            "【内推规则】\n" +
            "• 每位同学最多可投递2个岗位\n" +
            "• 建议通过牛客网、知乎、小红书等平台寻找在职员工获取内推码\n" +
            "• 也可以通过关注「得物招聘」公众号获取相关内推信息\n" +
            "• 校园大使内推可能会有更多指导和反馈\n\n" +
            "💡 内推不等于内定，最终录取仍需通过正常面试流程"
    },
    {
        id: 6,
        category: "笔试与测评",
        keywords: ["笔试", "测评", "在线", "考试", "题目", "准备", "测试", "行测", "coding", "算法题"],
        question_variants: [
            "得物校招笔试考什么？",
            "得物笔试怎么准备？",
            "得物笔试是什么形式？",
            "得物有测评吗？",
            "得物笔试用什么平台？",
            "笔试需要注意什么？",
            "错过了笔试怎么办？",
            "笔试通过后多久面试？"
        ],
        answer: "📝 得物校招笔试与测评：\n\n" +
            "【笔试形式】\n" +
            "• 技术岗位：通常需要参加在线编程笔试，考察算法和编程能力\n" +
            "• 非技术岗位：一般参加在线测评，考察逻辑、数理、语文等综合能力\n" +
            "• 设计/运营等岗位：可能有作品集审核或案例分析测试\n" +
            "• 具体形式和平台以邮件和短信通知为准\n\n" +
            "【考前准备】\n" +
            "• 准备好带有摄像头的电脑设备\n" +
            "• 下载谷歌最新版Chrome浏览器\n" +
            "• 提前测试好网络环境，避免断网\n" +
            "• 选择安静的环境参加考试\n" +
            "• 技术岗提前刷LeetCode、牛客网等平台的算法题\n" +
            "• 非技术岗可练习行测题和情景分析题\n\n" +
            "【笔试相关Q&A】\n" +
            "• 笔试通过后一般1-2周内会通知面试\n" +
            "• 部分岗位除了笔试还有测评环节，以邮件通知为准\n" +
            "• 注意查收邮件和短信，不要错过笔试通知\n" +
            "• 如有疑问可通过校招官网联系HR"
    },
    {
        id: 7,
        category: "面试",
        keywords: ["面试", "面经", "几轮", "流程", "HR", "技术面", "群面", "单面", "面试官", "线上"],
        question_variants: [
            "得物校招面试有几轮？",
            "得物面试流程是什么？",
            "得物面试怎么准备？",
            "面试时间可以改吗？",
            "得物面试注意事项？",
            "面试结果多久出来？",
            "面试反馈怎么查？"
        ],
        answer: "🎯 得物校招面试详情：\n\n" +
            "【面试形式】\n" +
            "得物校招以线上面试为主（部分岗位可能有线下终面），一般通过视频会议进行\n\n" +
            "【面试轮次】\n" +
            "• 技术岗位：一般为2-3轮技术面 + 1轮HR面\n" +
            "  技术面考察项目经验、算法基础、专业知识和系统设计能力\n" +
            "• 非技术岗位：一般为1-2轮业务面 + 1轮HR面\n" +
            "  业务面考察逻辑思维、行业认知、沟通表达等综合能力\n" +
            "• 部分岗位可能有群面（无领导小组讨论）环节\n\n" +
            "【面试时间调整】\n" +
            "接到面试邀请后，如需更改时间：\n" +
            "查看邮件中的面试邀请详情，联系HR进行时间调整\n\n" +
            "【面试注意事项】\n" +
            "• 提前5-10分钟上线测试设备和网络\n" +
            "• 保证安静良好的面试环境\n" +
            "• 技术岗如进行在线coding，注意对题目严格保密\n" +
            "• 提前了解得物的业务和产品（潮流电商+社区+鉴定）\n" +
            "• 准备2-3个向面试官提问的好问题\n\n" +
            "【投递进度查询】\n" +
            "同学可在校招官网中查看自己的投递进度。\n" +
            "面试反馈一般在1-2周内，各职位招聘流程有所不同，请耐心等待。"
    },
    {
        id: 8,
        category: "投递进度",
        keywords: ["进度", "查询", "投递进展", "状态", "结果", "流程终止", "流程中", "等待"],
        question_variants: [
            "怎么查询投递进度？",
            "我的投递进展怎么样？",
            "得物投递状态怎么看？",
            "流程终止了怎么办？",
            "投递后多久有消息？",
            "面试反馈多久出？"
        ],
        answer: "📋 得物校招投递进度查询：\n\n" +
            "【查询方式】\n" +
            "登录得物校招官网 campus.dewu.com，\n" +
            "进入个人中心即可查看投递进度\n\n" +
            "【进度状态说明】\n" +
            "• 简历筛选：简历正在被HR和业务部门查看\n" +
            "• 笔试/测评：已进入笔试或测评环节\n" +
            "• 面试中：已进入面试环节\n" +
            "• Offer沟通：已通过面试，进入Offer阶段\n" +
            "• 流程结束：该岗位的投递流程已结束\n\n" +
            "【常见问题】\n" +
            "• 投递后一般1-4周内有反馈，具体视岗位需求而定\n" +
            "• 面试反馈尽量控制在1-2周内\n" +
            "• 各职位招聘流程不同，无法给到统一的时间答复\n" +
            "• 请耐心等待后续邮件和短信通知\n\n" +
            "💡 建议保持手机畅通，及时查收邮件和短信"
    },
    {
        id: 9,
        category: "工作城市",
        keywords: ["城市", "地点", "工作地点", "上海", "北京", "杭州", "广州", "去哪里", "base", "总部"],
        question_variants: [
            "得物校招有哪些工作城市？",
            "得物在哪些城市有岗位？",
            "得物总部在哪里？",
            "得物工作地点可以选择吗？",
            "得物校招开放了几个城市？"
        ],
        answer: "📍 得物校招工作地点：\n\n" +
            "【主要办公城市】\n" +
            "• 上海（总部，杨浦区互联宝地）\n" +
            "• 北京\n" +
            "• 杭州\n" +
            "• 广州\n" +
            "• 武汉（部分岗位）\n" +
            "• 深圳（部分岗位）\n\n" +
            "【各城市业务侧重】\n" +
            "• 上海总部：全业务线，技术、产品、运营、设计核心团队\n" +
            "• 北京：部分技术和产品团队\n" +
            "• 杭州：技术研发、算法团队\n" +
            "• 广州：供应链、仓储物流相关岗位\n\n" +
            "💡 具体岗位的工作地点以校招官网发布的职位JD为准。\n" +
            "投递时可在系统中选择期望工作城市。"
    },
    {
        id: 10,
        category: "关于得物",
        keywords: ["得物", "公司", "介绍", "是什么", "做啥", "业务", "平台", "电商", "潮流", "鉴定", "社区"],
        question_variants: [
            "得物是什么公司？",
            "得物是做什么的？",
            "得物的业务模式是什么？",
            "得物公司怎么样？",
            "得物的公司规模？"
        ],
        answer: "🏢 关于得物App：\n\n" +
            "得物App（原名「毒」App）是新一代潮流网购社区，\n" +
            "开创了「先鉴别，后发货」的全新交易模式。\n\n" +
            "【核心业务】\n" +
            "👟 潮流电商：正品潮流商品交易平台\n" +
            "  覆盖球鞋、服饰、潮玩、美妆、数码等品类\n" +
            "🔍 鉴定服务：得物独有的专业商品鉴定体系\n" +
            "  每件商品均经过多重查验鉴别，确保正品\n" +
            "💬 潮流社区：年轻人分享潮流生活的社交平台\n" +
            "  达人穿搭、开箱评测、潮流资讯一应俱全\n\n" +
            "【公司实力】\n" +
            "• 2015年创立于上海，前身为「毒」App\n" +
            "• 2020年品牌升级为「得物App」\n" +
            "• 注册用户超过4亿\n" +
            "• 估值超百亿美元，中国电商独角兽企业\n" +
            "• 总部位于上海杨浦区互联宝地\n\n" +
            "【企业文化】\n" +
            "• 使命：帮助用户得到美好事物\n" +
            "• 价值观：正直、务实、高效、简单\n" +
            "• 技术驱动，工程师文化浓厚\n" +
            "• 年轻化的团队，扁平化管理\n" +
            "• 为年轻人提供快速成长的舞台"
    },
    {
        id: 11,
        category: "实习生招聘",
        keywords: ["实习", "intern", "暑期实习", "日常实习", "转正", "实习offer"],
        question_variants: [
            "得物有实习生招聘吗？",
            "得物暑期实习怎么投？",
            "得物实习可以转正吗？",
            "实习生校招流程？",
            "得物有实习岗位吗？"
        ],
        answer: "💼 得物实习生招聘：\n\n" +
            "得物每年都会开放暑期实习生招聘，面向下一届毕业生。\n\n" +
            "【暑期实习流程】\n" +
            "• 面向对象：下一届毕业生（如2027届）\n" +
            "• 投递时间：一般3月-5月\n" +
            "• 面试时间：滚动面试\n" +
            "• 实习入职：5月-7月\n" +
            "• 转正答辩：8月-9月\n" +
            "• 发放正式校招Offer：9月-10月\n\n" +
            "【日常实习】\n" +
            "得物也长期开放日常实习岗位，面向所有在校生，\n" +
            "全年可投递，具体岗位请关注官网。\n\n" +
            "【注意事项】\n" +
            "• 暑期实习仅面向对应毕业时间的同学\n" +
            "• 实习表现优异可获得转正机会（转正率较高）\n" +
            "• 通过得物校招官网 campus.dewu.com 投递\n" +
            "• 实习期间表现突出可免去部分校招流程\n\n" +
            "💡 建议大三/研二的同学重点关注暑期实习机会，这是进得物的最佳路径！"
    },
    {
        id: 12,
        category: "简历准备",
        keywords: ["简历", "模板", "格式", "写简历", "内容", "优化", "经历", "STAR"],
        question_variants: [
            "得物校招简历怎么写？",
            "投递得物简历要注意什么？",
            "得物校招简历有什么要求？",
            "简历需要哪些内容？",
            "得物简历筛选看重什么？"
        ],
        answer: "📄 得物校招简历建议：\n\n" +
            "【简历核心模块】\n" +
            "1. 基本信息：姓名、联系方式、邮箱、意向城市\n" +
            "2. 教育背景：学校、学历、专业、GPA（如优异可标注）\n" +
            "3. 实习/项目经历：最重要的模块，占简历篇幅的40%-50%\n" +
            "4. 专业技能：编程语言、开发工具、设计软件等\n" +
            "5. 获奖/证书：有含金量的竞赛获奖或证书\n" +
            "6. 作品集链接（设计/运营岗必备）\n\n" +
            "【写在得物简历的加分项】\n" +
            "• 对潮流文化和电商行业有热情和了解\n" +
            "• 有电商、社区、供应链相关项目经验\n" +
            "• 使用STAR法则描述经历（情境-任务-行动-结果）\n" +
            "• 用数据量化成果（如\u201cGMV增长20%\u201d）\n" +
            "• 展示与岗位直接相关的技能和作品\n" +
            "• 了解得物的鉴定体系和先鉴别后发货模式\n\n" +
            "💡 建议投递前去得物App体验产品，深入了解业务"
    },
    {
        id: 13,
        category: "培养与发展",
        keywords: ["培养", "发展", "晋升", "成长", "培训", "新人", "入职", "职业发展"],
        question_variants: [
            "得物校招生培养体系怎么样？",
            "入职后有什么培训？",
            "得物晋升机制是怎样的？",
            "校招生在得物的发展前景？",
            "得物新人培训？"
        ],
        answer: "🌱 得物校招生培养与发展：\n\n" +
            "得物为校招生提供了完善的成长体系：\n\n" +
            "【入职培训】\n" +
            "• 系统的新员工入职培训，了解公司业务和文化\n" +
            "• 配备专属导师（Mentor），一对一指导\n" +
            "• 业务培训、技术培训双线并行\n" +
            "• 新人破冰和团队融入活动\n\n" +
            "【成长路径】\n" +
            "• 新人期（0-6个月）：熟悉业务，在导师指导下完成任务\n" +
            "• 成长期（6-18个月）：独立负责模块，积累项目经验\n" +
            "• 进阶期（1.5年后）：向高级工程师/资深产品等方向发展\n\n" +
            "【职业发展双通道】\n" +
            "• 专业通道（P序列）：初级→高级→资深→专家→科学家\n" +
            "• 管理通道（M序列）：团队Leader→总监→VP\n\n" +
            "💡 得物注重年轻人的成长，提供丰富的学习资源和晋升机会，\n" +
            "业务快速发展期，校招生有机会接触核心项目和快速晋升。"
    },
    {
        id: 14,
        category: "联系方式",
        keywords: ["联系", "邮箱", "电话", "客服", "咨询", "hr", "校招邮箱", "公众号"],
        question_variants: [
            "得物校招怎么联系？",
            "得物招聘邮箱是什么？",
            "有问题找谁？",
            "得物HR联系方式？",
            "得物校招咨询电话？"
        ],
        answer: "📬 得物校招联系方式：\n\n" +
            "【校招官网】\n" +
            "campus.dewu.com\n\n" +
            "【公众号】\n" +
            "关注「得物招聘」公众号，获取最新招聘动态\n" +
            "关注「得物App」官方号，了解公司产品和活动\n\n" +
            "【其他渠道】\n" +
            "• 牛客网：搜索「得物校招」获取面经\n" +
            "• 小红书：关注「得物招聘」官方账号\n" +
            "• 知乎：搜索「得物校招」获取经验分享\n" +
            "• 各大高校BBS和就业信息网\n\n" +
            "💡 建议优先通过校招官网和公众号获取信息，\n" +
            "面试相关疑问可通过面试邀请邮件中的联系方式与HR沟通。"
    },
    {
        id: 15,
        category: "Offer与签约",
        keywords: ["offer", "签约", "三方", "薪资", "待遇", "工资", "薪酬", "福利"],
        question_variants: [
            "得物校招offer什么时候发？",
            "得物校招薪资待遇怎么样？",
            "得物offer怎么签？",
            "得物校招薪资水平？",
            "得物福利怎么样？"
        ],
        answer: "📋 得物校招Offer与签约：\n\n" +
            "【Offer发放时间】\n" +
            "• 秋招：预计2025年9月下旬开始发放Offer\n" +
            "• 春招：滚动发放\n" +
            "• 先通过先发Offer\n\n" +
            "【招聘全流程】\n" +
            "网申/内推 → 笔试/测评 → 线上面试 → Offer发放 → 签约入职\n\n" +
            "【薪酬福利（参考）】\n" +
            "• 提供具有竞争力的薪酬待遇（互联网行业中上水平）\n" +
            "• 五险一金 + 补充商业保险\n" +
            "• 弹性工作制，不打卡\n" +
            "• 免费下午茶、零食、团建活动\n" +
            "• 员工内购福利（潮流好物员工价）\n" +
            "• 健身补贴、节日礼盒等\n" +
            "• 年轻化的办公环境和文化氛围\n\n" +
            "💡 温馨提示：\n" +
            "• 具体薪资待遇以Offer通知为准\n" +
            "• 建议关注校招官网和邮件通知\n" +
            "• 有任何疑问可通过校招官网联系HR"
    },
    {
        id: 16,
        category: "面试准备",
        keywords: ["自我介绍", "面试技巧", "怎么准备面试", "面试经验", "面经", "反问", "准备"],
        question_variants: [
            "得物面试怎么准备？",
            "得物面试自我介绍怎么说？",
            "得物面试有什么技巧？",
            "得物面试要注意什么？",
            "面试最后可以问什么？"
        ],
        answer: "🎯 得物面试准备建议：\n\n" +
            "【面试前准备】\n" +
            "1. 深入了解得物的业务模式（先鉴别后发货、潮流电商+社区）\n" +
            "2. 下载得物App并体验核心功能，思考产品体验和可优化点\n" +
            "3. 了解潮流电商行业趋势、竞品分析（得物vs识货vs Nice等）\n" +
            "4. 仔细阅读投递岗位的JD，梳理匹配的经历\n" +
            "5. 准备1分钟/3分钟自我介绍（突出与岗位的匹配度）\n" +
            "6. 用STAR法则梳理简历上的每个项目经历\n" +
            "7. 技术岗：刷LeetCode热题100，复习基础知识\n" +
            "8. 提前5-10分钟上线测试设备和网络\n\n" +
            "【面试中注意】\n" +
            "• 保证安静良好的面试环境\n" +
            "• 技术岗如进行在线coding，注意对题目严格保密\n" +
            "• 真诚回答，展现对潮流文化和电商行业的热爱\n" +
            "• 展示逻辑思维和解决问题的能力\n" +
            "• 提前准备2-3个有深度的问题反问面试官\n\n" +
            "【时间调整】\n" +
            "如需更改面试时间，查看邮件中的HR联系方式联系即可。"
    },
    {
        id: 17,
        category: "投递规则",
        keywords: ["几个职位", "投递几个", "最多投递", "改志愿", "改简历", "改职位", "业务线", "志愿", "调剂"],
        question_variants: [
            "得物校招可以投几个岗位？",
            "最多能投几个职位？",
            "投递后能改简历吗？",
            "业务线志愿怎么选？",
            "投递后能改职位吗？",
            "秋招失败了还能投春招吗？"
        ],
        answer: "📋 得物校招投递规则：\n\n" +
            "【投递数量】\n" +
            "每位同学最多可投递2个岗位\n\n" +
            "【志愿顺序】\n" +
            "• 2个岗位志愿有先后顺序\n" +
            "• 优先处理第一志愿的岗位\n" +
            "• 第一志愿流程结束后才会处理第二志愿\n" +
            "• 建议把最想去的岗位放在第一志愿\n\n" +
            "【岗位修改】\n" +
            "• 如简历未在流程中，可以修改岗位\n" +
            "• 简历进入流程后不可修改职位\n" +
            "• 投递前请仔细确认岗位选择\n\n" +
            "【秋招与春招】\n" +
            "• 秋招和春招是独立的招聘批次\n" +
            "• 秋招失败不影响参加春招\n" +
            "• 但同一批次内不可重复投递已结束的岗位\n" +
            "• 建议主攻秋招，春招岗位数量较少\n\n" +
            "💡 投递前请仔细阅读职位描述，确认自己符合基本要求再投递。"
    }
];

    // ============================================
    // 中文分词（简易版，基于字符二元组和关键词匹配）
    // ============================================
    function tokenize(text) {
        // 简易分词：提取所有2-4字的中文词组和单字
        const tokens = [];
        const chinesePattern = /[\u4e00-\u9fff]+/g;
        let match;
        while ((match = chinesePattern.exec(text)) !== null) {
            const word = match[0];
            tokens.push(word);
            for (let i = 0; i < word.length; i++) {
                tokens.push(word.substring(i, i + 1));
                if (i + 2 <= word.length) tokens.push(word.substring(i, i + 2));
            }
        }
        // 也提取英文词
        const engPattern = /[a-zA-Z]+/g;
        while ((match = engPattern.exec(text)) !== null) {
            tokens.push(match[0].toLowerCase());
        }
        return [...new Set(tokens)];
    }

    // ============================================
    // TF-IDF 语义检索（简化版）
    // ============================================
    // 构建语料
    const allQuestions = [];
    const questionToFaqIndex = [];
    FAQ_KNOWLEDGE.forEach((faq, idx) => {
        faq.question_variants.forEach(q => {
            allQuestions.push(q);
            questionToFaqIndex.push(idx);
        });
    });

    // 构建 TF 矩阵
    const vocabulary = {};
    let vocabSize = 0;
    const docTokens = allQuestions.map(q => {
        const tokens = tokenize(q);
        tokens.forEach(t => {
            if (!(t in vocabulary)) {
                vocabulary[t] = vocabSize++;
            }
        });
        return tokens;
    });

    // 计算IDF
    const idf = new Float64Array(vocabSize);
    docTokens.forEach(tokens => {
        const seen = new Set(tokens);
        seen.forEach(t => {
            if (t in vocabulary) idf[vocabulary[t]]++;
        });
    });
    for (let i = 0; i < vocabSize; i++) {
        idf[i] = Math.log((allQuestions.length + 1) / (idf[i] + 1)) + 1;
    }

    // 计算 TF-IDF 向量
    const tfidfVectors = docTokens.map(tokens => {
        const tf = {};
        tokens.forEach(t => { tf[t] = (tf[t] || 0) + 1; });
        const vec = new Float64Array(vocabSize);
        Object.keys(tf).forEach(t => {
            if (t in vocabulary) {
                vec[vocabulary[t]] = (tf[t] / tokens.length) * idf[vocabulary[t]];
            }
        });
        return vec;
    });

    function cosineSim(a, b) {
        let dot = 0, normA = 0, normB = 0;
        for (let i = 0; i < a.length; i++) {
            dot += a[i] * b[i];
            normA += a[i] * a[i];
            normB += b[i] * b[i];
        }
        return normA && normB ? dot / (Math.sqrt(normA) * Math.sqrt(normB)) : 0;
    }

    function queryTfidfVector(query) {
        const tokens = tokenize(query);
        const tf = {};
        tokens.forEach(t => { tf[t] = (tf[t] || 0) + 1; });
        const vec = new Float64Array(vocabSize);
        Object.keys(tf).forEach(t => {
            if (t in vocabulary) {
                vec[vocabulary[t]] = (tf[t] / tokens.length) * idf[vocabulary[t]];
            }
        });
        return vec;
    }

    // ============================================
    // 关键词匹配
    // ============================================
    function keywordMatchScore(query, faq) {
        const queryLower = query.toLowerCase();
        let score = 0;
        const matchedKeywords = [];

        faq.keywords.forEach(kw => {
            if (queryLower.includes(kw.toLowerCase())) {
                score += 3;
                matchedKeywords.push(kw);
            }
        });

        // 检查问题变体相似度
        faq.question_variants.forEach(variant => {
            const queryTokens = new Set(tokenize(query));
            const variantTokens = new Set(tokenize(variant));
            let overlap = 0;
            queryTokens.forEach(t => { if (variantTokens.has(t)) overlap++; });
            const ratio = overlap / Math.max(variantTokens.size, 1);
            if (ratio > 0.3) score += 2 * ratio;
        });

        return { score, matchedKeywords };
    }

    // ============================================
    // 语义检索
    // ============================================
    function semanticSearch(query, topK = 5) {
        const queryVec = queryTfidfVector(query);
        const similarities = tfidfVectors.map((vec, i) => ({
            index: i,
            similarity: cosineSim(queryVec, vec)
        }));
        similarities.sort((a, b) => b.similarity - a.similarity);

        const results = [];
        const seenFaqIds = new Set();
        for (const item of similarities.slice(0, topK)) {
            const faqIdx = questionToFaqIndex[item.index];
            if (!seenFaqIds.has(faqIdx)) {
                seenFaqIds.add(faqIdx);
                results.push({
                    faq: FAQ_KNOWLEDGE[faqIdx],
                    similarity: item.similarity,
                    matchedQuestion: allQuestions[item.index]
                });
                if (results.length >= 3) break;
            }
        }
        return results;
    }

    // ============================================
    // 推荐问题
    // ============================================
    function getSuggestedQuestions() {
        return [
            "如何进行网申？", "校招面试一般有几轮？",
            "得物和腾讯可以同时投递吗？", "简历怎么写比较好？",
            "内推有用吗？", "得物有哪些岗位？"
        ];
    }

    // ============================================
    // 兜底回答
    // ============================================
    function getFallbackAnswer(query) {
        const campusKeywords = ["校招", "秋招", "春招", "应届", "招聘", "求职", "工作", "公司", "企业", "offer", "简历", "面试", "笔试"];
        const isCampusRelated = campusKeywords.some(kw => query.includes(kw));

        if (isCampusRelated) {
            return "🤔 您的问题我已经收到了，但目前我还在学习中，暂时无法给出特别精准的回答。\n\n💡 建议您：\n• 尝试换一种方式描述您的问题\n• 选择更具体的关键词提问\n• 参考下面为您推荐的热门问题\n\n您也可以关注「得物招聘」公众号获取最新信息~";
        }
        return "👋 您好！我是得物校招问答助手，专注于解答得物校园招聘相关问题。\n\n我可以帮您解答：\n📝 网申投递  📄 简历制作  ✍️ 笔试准备\n🎯 面试技巧  💰 Offer选择  💼 实习经验\n🔗 内推攻略  🏢 公司产品  📍 工作城市\n\n请向我提问校招相关问题，我会尽力为您解答！";
    }

    // ============================================
    // 综合匹配
    // ============================================
    function findBestAnswer(query) {
        query = query.trim();

        // 1. 关键词匹配
        let bestKeywordScore = 0, bestKeywordFaq = null, bestMatchedKw = [];
        FAQ_KNOWLEDGE.forEach(faq => {
            const { score, matchedKeywords } = keywordMatchScore(query, faq);
            if (score > bestKeywordScore) {
                bestKeywordScore = score;
                bestKeywordFaq = faq;
                bestMatchedKw = matchedKeywords;
            }
        });

        // 关键词高分直接返回
        if (bestKeywordScore >= 6 && bestKeywordFaq) {
            return {
                answer: bestKeywordFaq.answer,
                category: bestKeywordFaq.category,
                confidence: "high",
                related_questions: []
            };
        }

        // 2. 语义检索
        const semanticResults = semanticSearch(query);
        if (semanticResults.length && semanticResults[0].similarity > 0.2) {
            const top = semanticResults[0];
            const related = semanticResults.slice(1, 3).map(r => r.faq.question_variants[0]);
            return {
                answer: top.faq.answer,
                category: top.faq.category,
                confidence: top.similarity > 0.4 ? "high" : "medium",
                related_questions: related
            };
        }

        // 3. 弱关键词匹配
        if (bestKeywordScore >= 2 && bestKeywordFaq) {
            return {
                answer: bestKeywordFaq.answer,
                category: bestKeywordFaq.category,
                confidence: "medium",
                related_questions: []
            };
        }

        // 4. 兜底
        return {
            answer: getFallbackAnswer(query),
            category: "通用",
            confidence: "low",
            related_questions: getSuggestedQuestions(),
            suggested_questions: getSuggestedQuestions()
        };
    }

    // ============================================
    // DOM 交互逻辑
    // ============================================
    const $ = (sel) => document.querySelector(sel);
    const messageInput = $('#messageInput');
    const sendBtn = $('#sendBtn');
    const chatWindow = $('#chatWindow');
    const messagesContainer = $('#messagesContainer');
    const welcomeScreen = $('#welcomeScreen');
    const typingIndicator = $('#typingIndicator');
    const sidebar = $('#sidebar');
    const sidebarToggle = $('#sidebarToggle');
    const newChatBtn = $('#newChatBtn');
    const clearChatBtn = $('#clearChatBtn');
    const mobileMenuBtn = $('#mobileMenuBtn');
    const sidebarExpandBtn = document.getElementById('sidebarExpandBtn');
    const categoryList = $('#categoryList');
    const historyList = $('#historyList');
    const quickQuestions = $('#quickQuestions');

    if (sidebarExpandBtn) sidebarExpandBtn.style.display = 'none';

    let chatHistory = [];
    let isLoading = false;

    const categoryIcons = {
        '投递须知': 'fa-globe', '招聘对象': 'fa-users', '岗位类别': 'fa-compass',
        '内推': 'fa-link', '笔试与测评': 'fa-pen-fancy', '面试': 'fa-comments',
        '投递进度': 'fa-tasks', '工作城市': 'fa-map-marker-alt', '关于得物': 'fa-music',
        '实习生招聘': 'fa-briefcase', '简历准备': 'fa-file-alt', '培养与发展': 'fa-seedling',
        '联系方式': 'fa-envelope', 'Offer与签约': 'fa-hand-holding-usd',
        '面试准备': 'fa-chalkboard-teacher', '投递规则': 'fa-clipboard-list',
        '其他': 'fa-question-circle'
    };

    // ============================================
    // 初始化
    // ============================================
    function init() {
        loadCategories();
        loadSuggestions();
        bindEvents();
        messageInput.focus();
    }

    function bindEvents() {
        sendBtn.addEventListener('click', handleSend);
        messageInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); handleSend(); }
        });
        messageInput.addEventListener('input', () => {
            messageInput.style.height = 'auto';
            messageInput.style.height = Math.min(messageInput.scrollHeight, 100) + 'px';
        });
        sidebarToggle.addEventListener('click', toggleSidebar);
        newChatBtn.addEventListener('click', newChat);
        clearChatBtn.addEventListener('click', clearChat);
        mobileMenuBtn.addEventListener('click', () => {
            sidebar.classList.remove('collapsed');
            if (sidebarExpandBtn) sidebarExpandBtn.style.display = 'none';
        });
        if (sidebarExpandBtn) {
            sidebarExpandBtn.addEventListener('click', () => {
                sidebar.classList.remove('collapsed');
                sidebarExpandBtn.style.display = 'none';
            });
        }
    }

    function toggleSidebar() {
        const isCollapsed = sidebar.classList.toggle('collapsed');
        if (sidebarExpandBtn) sidebarExpandBtn.style.display = isCollapsed ? 'flex' : 'none';
    }

    function loadCategories() {
        const counts = {};
        FAQ_KNOWLEDGE.forEach(f => { counts[f.category] = (counts[f.category] || 0) + 1; });
        const categories = [...new Set(FAQ_KNOWLEDGE.map(f => f.category))];

        categoryList.innerHTML = '';
        categories.forEach(cat => {
            const btn = document.createElement('button');
            btn.className = 'category-item';
            btn.innerHTML = `<i class="fas ${categoryIcons[cat] || 'fa-folder'}"></i><span>${cat}</span><span class="badge">${counts[cat] || 0}</span>`;
            btn.addEventListener('click', () => {
                categoryList.querySelectorAll('.category-item').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                const faqs = FAQ_KNOWLEDGE.filter(f => f.category === cat);
                if (faqs.length) sendQuestion(faqs[0].question_variants[0]);
            });
            categoryList.appendChild(btn);
        });
    }

    function loadSuggestions() {
        const suggestions = getSuggestedQuestions();
        const icons = ['fa-file-alt', 'fa-comments', 'fa-globe', 'fa-file-contract', 'fa-link', 'fa-heart'];
        const grid = document.createElement('div');
        grid.className = 'quick-grid';
        suggestions.forEach((q, i) => {
            const btn = document.createElement('button');
            btn.className = 'quick-btn';
            btn.innerHTML = `<i class="fas ${icons[i % icons.length]}"></i> ${q}`;
            btn.addEventListener('click', () => sendQuestion(q));
            grid.appendChild(btn);
        });
        quickQuestions.appendChild(grid);
    }

    function handleSend() {
        const text = messageInput.value.trim();
        if (!text || isLoading) return;
        sendQuestion(text);
    }

    function sendQuestion(text) {
        if (welcomeScreen) welcomeScreen.style.display = 'none';
        appendUserMessage(text);
        chatHistory.push({ role: 'user', content: text });
        messageInput.value = '';
        messageInput.style.height = 'auto';
        addToHistory(text);
        requestAnswer(text);
    }

    async function requestAnswer(question) {
        isLoading = true;
        sendBtn.disabled = true;
        typingIndicator.style.display = 'flex';
        scrollToBottom();

        // 模拟思考延迟
        await new Promise(r => setTimeout(r, 300 + Math.random() * 500));

        try {
            const result = findBestAnswer(question);
            appendAssistantMessage(result.answer, result.related_questions || result.suggested_questions || []);
            chatHistory.push({ role: 'assistant', content: result.answer });
        } catch (e) {
            appendAssistantMessage('处理问题时出错，请重试。');
        } finally {
            isLoading = false;
            sendBtn.disabled = false;
            typingIndicator.style.display = 'none';
            scrollToBottom();
        }
    }

    function appendUserMessage(text) {
        const el = document.createElement('div');
        el.className = 'message user';
        el.innerHTML = `<div class="message-avatar"><i class="fas fa-user"></i></div><div class="message-body"><div class="message-bubble">${escapeHtml(text)}</div></div>`;
        messagesContainer.appendChild(el);
        scrollToBottom();
    }

    function appendAssistantMessage(answer, relatedQuestions) {
        const el = document.createElement('div');
        el.className = 'message assistant';

        let relatedHtml = '';
        if (relatedQuestions && relatedQuestions.length > 0) {
            relatedHtml = `<div class="related-questions"><div class="related-title">相关问题：</div>${relatedQuestions.map(q => `<button class="related-btn" data-q="${escapeHtml(q)}">${escapeHtml(q)}</button>`).join('')}</div>`;
        }

        el.innerHTML = `<div class="message-avatar"><img src="./img/favicon.ico" alt="得物"></div><div class="message-body"><div class="message-bubble"><div class="answer-text">${formatAnswer(answer)}</div>${relatedHtml}</div></div>`;
        el.querySelectorAll('.related-btn').forEach(btn => {
            btn.addEventListener('click', () => sendQuestion(btn.dataset.q));
        });
        messagesContainer.appendChild(el);
        scrollToBottom();
    }

    function formatAnswer(text) {
        return escapeHtml(text).replace(/\n/g, '<br>');
    }

    function addToHistory(question) {
        const short = question.length > 20 ? question.slice(0, 20) + '...' : question;
        if (chatHistory.length <= 1) historyList.innerHTML = '';
        const item = document.createElement('div');
        item.className = 'history-item';
        item.textContent = short;
        item.title = question;
        item.addEventListener('click', () => sendQuestion(question));
        historyList.prepend(item);
    }

    function newChat() {
        chatHistory = [];
        messagesContainer.innerHTML = '';
        if (welcomeScreen) welcomeScreen.style.display = '';
        messageInput.focus();
    }

    function clearChat() {
        messagesContainer.innerHTML = '';
        chatHistory = [];
        if (welcomeScreen) welcomeScreen.style.display = '';
        messageInput.focus();
    }

    function escapeHtml(str) {
        const div = document.createElement('div');
        div.textContent = str;
        return div.innerHTML;
    }

    function scrollToBottom() {
        requestAnimationFrame(() => { chatWindow.scrollTop = chatWindow.scrollHeight; });
    }

    document.addEventListener('DOMContentLoaded', init);
})();
