/* ============================================ */
/* 校招AI问答机器人 - 前端逻辑                    */
/* ============================================ */

(function () {
    'use strict';

    // DOM 元素
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

    // 初始隐藏展开按钮
    if (sidebarExpandBtn) sidebarExpandBtn.style.display = 'none';

    // 状态
    let chatHistory = [];
    let isLoading = false;

    // 分类图标映射
    const categoryIcons = {
        '网申': 'fa-globe',
        '简历': 'fa-file-alt',
        '笔试': 'fa-pen-fancy',
        '面试': 'fa-comments',
        'Offer': 'fa-hand-holding-usd',
        '三方协议': 'fa-file-contract',
        '岗位选择': 'fa-compass',
        '实习': 'fa-briefcase',
        '内推': 'fa-link',
        '考公与校招': 'fa-landmark',
        '心态与准备': 'fa-heart',
        '学历与门槛': 'fa-university',
        '其他': 'fa-question-circle',
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

    // ============================================
    // 事件绑定
    // ============================================
    function bindEvents() {
        sendBtn.addEventListener('click', handleSend);
        messageInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                handleSend();
            }
        });

        // 自动调整输入框高度
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

    // ============================================
    // 侧边栏
    // ============================================
    function toggleSidebar() {
        const isCollapsed = sidebar.classList.toggle('collapsed');
        if (isCollapsed) {
            if (sidebarExpandBtn) sidebarExpandBtn.style.display = 'flex';
        } else {
            if (sidebarExpandBtn) sidebarExpandBtn.style.display = 'none';
        }
    }

    // ============================================
    // 加载分类
    // ============================================
    async function loadCategories() {
        try {
            const res = await fetch('/api/faq');
            const data = await res.json();

            const counts = {};
            data.faqs.forEach((q) => {
                counts[q.category] = (counts[q.category] || 0) + 1;
            });

            const categories = [...new Set(data.faqs.map((f) => f.category))];

            categoryList.innerHTML = '';
            categories.forEach((cat) => {
                const btn = document.createElement('button');
                btn.className = 'category-item';
                btn.innerHTML = `
                    <i class="fas ${categoryIcons[cat] || 'fa-folder'}"></i>
                    <span>${cat}</span>
                    <span class="badge">${counts[cat] || 0}</span>
                `;
                btn.addEventListener('click', () => {
                    categoryList.querySelectorAll('.category-item').forEach((b) => b.classList.remove('active'));
                    btn.classList.add('active');
                    const faqs = data.faqs.filter((f) => f.category === cat);
                    if (faqs.length > 0) {
                        sendQuestion(faqs[0].question);
                    }
                });
                categoryList.appendChild(btn);
            });
        } catch (e) {
            console.error('加载分类失败', e);
        }
    }

    // ============================================
    // 加载推荐问题
    // ============================================
    async function loadSuggestions() {
        try {
            const res = await fetch('/api/suggestions');
            const data = await res.json();
            const suggestions = data.suggestions || [];

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
        } catch (e) {
            console.error('加载推荐问题失败', e);
        }
    }

    // ============================================
    // 发送消息
    // ============================================
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

    // ============================================
    // 请求回答
    // ============================================
    async function requestAnswer(question) {
        isLoading = true;
        sendBtn.disabled = true;
        typingIndicator.style.display = 'flex';
        scrollToBottom();

        try {
            const res = await fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ question }),
            });
            const data = await res.json();

            if (data.error) {
                appendAssistantMessage('抱歉，出了点问题：' + data.error);
            } else {
                appendAssistantMessage(data.answer, data.related_questions || data.suggested_questions || []);
            }

            chatHistory.push({ role: 'assistant', content: data.answer });
        } catch (e) {
            appendAssistantMessage('网络错误，请稍后重试。');
        } finally {
            isLoading = false;
            sendBtn.disabled = false;
            typingIndicator.style.display = 'none';
            scrollToBottom();
        }
    }

    // ============================================
    // 消息渲染
    // ============================================
    function appendUserMessage(text) {
        const el = document.createElement('div');
        el.className = 'message user';
        el.innerHTML = `
            <div class="message-avatar"><i class="fas fa-user"></i></div>
            <div class="message-body">
                <div class="message-bubble">${escapeHtml(text)}</div>
            </div>
        `;
        messagesContainer.appendChild(el);
        scrollToBottom();
    }

    function appendAssistantMessage(answer, relatedQuestions) {
        const el = document.createElement('div');
        el.className = 'message assistant';

        let relatedHtml = '';
        if (relatedQuestions && relatedQuestions.length > 0) {
            relatedHtml = `
                <div class="related-questions">
                    <div class="related-title">相关问题：</div>
                    ${relatedQuestions.map((q) => `<button class="related-btn" data-q="${escapeHtml(q)}">${escapeHtml(q)}</button>`).join('')}
                </div>
            `;
        }

        el.innerHTML = `
            <div class="message-avatar"><img src="/static/img/favicon.ico" alt="得物"></div>
            <div class="message-body">
                <div class="message-bubble">
                    <div class="answer-text">${formatAnswer(answer)}</div>
                    ${relatedHtml}
                </div>
            </div>
        `;

        el.querySelectorAll('.related-btn').forEach((btn) => {
            btn.addEventListener('click', () => sendQuestion(btn.dataset.q));
        });

        messagesContainer.appendChild(el);
        scrollToBottom();
    }

    function formatAnswer(text) {
        return escapeHtml(text);
    }

    // ============================================
    // 历史记录
    // ============================================
    function addToHistory(question) {
        const short = question.length > 20 ? question.slice(0, 20) + '...' : question;

        if (chatHistory.length <= 1) {
            historyList.innerHTML = '';
        }

        const item = document.createElement('div');
        item.className = 'history-item';
        item.textContent = short;
        item.title = question;
        item.addEventListener('click', () => sendQuestion(question));
        historyList.prepend(item);
    }

    // ============================================
    // 新对话 / 清空
    // ============================================
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

    // ============================================
    // 工具函数
    // ============================================
    function escapeHtml(str) {
        const div = document.createElement('div');
        div.textContent = str;
        return div.innerHTML;
    }

    function scrollToBottom() {
        requestAnimationFrame(() => {
            chatWindow.scrollTop = chatWindow.scrollHeight;
        });
    }

    // 启动
    document.addEventListener('DOMContentLoaded', init);
})();
