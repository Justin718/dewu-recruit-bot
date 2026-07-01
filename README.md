# 得物校招 AI 问答机器人

一个基于 Flask 的校招常见问题智能问答系统，支持关键词匹配和 TF-IDF 语义检索。

## 🌟 功能特性

- 💬 智能问答：基于关键词匹配 + TF-IDF 语义检索
- 📚 9 大主题：网申投递、简历制作、笔试准备、面试技巧、Offer 选择、实习经验、内推攻略、公司产品、工作城市
- 🎨 现代化 UI：响应式设计，流畅的聊天交互体验
- 🚀 双模式部署：支持后端 Flask 服务 + 纯前端独立版

## 🏗 项目结构

```
.
├── app.py                      # Flask 后端主服务
├── requirements.txt            # Python 依赖
├── templates/                  # Flask 模板
│   └── index.html
├── static/                     # Flask 静态资源
│   ├── index.html
│   ├── css/style.css
│   ├── js/app.js
│   ├── js/app-standalone.js    # 纯前端独立版（无需后端）
│   └── img/
├── dewu_research/              # 学者研究方向管理子系统
└── .gitignore
```

## 🚀 本地运行

### 1. 后端服务版（Flask）

```bash
# 安装依赖
pip install -r requirements.txt

# 启动服务
python app.py

# 浏览器访问
http://localhost:5000
```

### 2. 纯前端独立版

直接用浏览器打开 `static/index.html` 即可使用，所有 FAQ 知识库内嵌在 JS 中，无需后端。

## 📦 部署到 GitHub Pages

`static/index.html` 是纯前端版本，可以直接部署到 GitHub Pages：

1. 在 GitHub 仓库 → **Settings** → **Pages**
2. Source 选择 `main` 分支根目录
3. 访问 `https://<用户名>.github.io/dewu-recruit-bot/static/`

## 🛠 技术栈

- **后端**：Flask + scikit-learn (TF-IDF)
- **前端**：原生 HTML/CSS/JavaScript（无框架依赖）
- **检索算法**：关键词匹配 + TF-IDF 余弦相似度

## 📄 License

MIT
