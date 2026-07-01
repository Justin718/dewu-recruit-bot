/**
 * 得物研究型实习生 - 一体化AI学者信息平台
 * 前端交互逻辑：SPA导航 / Canvas图表 / SVG知识图谱 / 数据渲染
 *
 * 技术栈：原生 JavaScript (无框架依赖)
 * 图表引擎：原生 Canvas 2D API (手绘折线图、饼图)
 * 知识图谱：原生 SVG (手绘力导向布局)
 */
(function () {
  'use strict';

  // ==================== 工具函数 ====================
  const $ = (sel, ctx) => (ctx || document).querySelector(sel);
  const $$ = (sel, ctx) => Array.from((ctx || document).querySelectorAll(sel));

  function fmt(n) { return Number(n).toLocaleString(); }

  // 页面标题映射
  const PAGE_META = {
    dashboard: ['数据看板', '实时监控 · 项目进展 · 核心指标一览'],
    projects:  ['研究项目', '5大核心研究方向与成果'],
    architecture: ['技术架构', '5层推荐系统技术栈全景'],
    knowledge:  ['知识图谱', '推荐系统领域知识关联网络'],
    feishu:   ['飞书集成', '智能助手 · 告警推送 · 消息流'],
  };

  // 颜色表
  const COLORS = {
    chartLine: '#3b82f6',
    chartFill: 'rgba(59,130,246,.12)',
    gridLine: 'rgba(255,255,255,.05)',
    textMuted: '#6b7090',
    pieColors: ['#3b82f6','#10b981','#8b5cf6','#f59e0b','#06b6d4','#ec4899'],
    barColors: ['#3b82f6','#10b981','#8b5cf6','#f59e0b'],
    categoryColors: {
      '用户建模': '#3b82f6',
      '召回优化': '#10b981',
      '知识图谱': '#8b5cf6',
      '冷启动': '#f59e0b',
      '评估体系': '#ec4899',
    },
  };

  // ==================== SPA 导航 ====================
  function initNav() {
    $$('.nav-item').forEach(el => {
      el.addEventListener('click', () => {
        const page = el.dataset.page;
        if (!page) return;

        // 更新导航激活态
        $$('.nav-item').forEach(i => i.classList.remove('active'));
        el.classList.add('active');

        // 切换页面
        $$('.page').forEach(p => p.classList.remove('active'));
        const target = $('#page-' + page);
        if (target) target.classList.add('active');

        // 更新标题
        if (PAGE_META[page]) {
          $('#pageTitle').textContent = PAGE_META[page][0];
          $('#pageDesc').textContent = PAGE_META[page][1];
        }

        // 移动端关闭侧栏
        $('.sidebar').classList.remove('open');

        // 加载页面数据
        loadPageData(page);
      });
    });

    // 移动端汉堡菜单
    $('#mobileToggle').addEventListener('click', () => {
      $('.sidebar').classList.toggle('open');
    });
  }

  // ==================== 时钟 ====================
  function initClock() {
    function tick() {
      const now = new Date();
      $('#topbarTime').textContent = now.toLocaleTimeString('zh-CN', { hour12: false });
    }
    tick();
    setInterval(tick, 1000);
  }

  // ==================== 页面数据加载路由 ====================
  function loadPageData(page) {
    switch (page) {
      case 'dashboard': loadDashboard(); break;
      case 'projects':  loadProjects(); break;
      case 'architecture': loadArchitecture(); break;
      case 'knowledge':  loadKnowledgeGraph(); break;
      case 'feishu':    loadFeishu(); break;
    }
  }

  // ==================== 1. 数据看板 ====================
  async function loadDashboard() {
    try {
      const res = await fetch('/api/dashboard');
      const data = await res.json();
      renderSummaryCards(data.summary_cards);
      renderCTRTrend(data.ctr_trend);
      renderRecallPie(data.recall_routes);
      renderCategoryCTR(data.category_ctr);
      renderExperimentTable(data.experiments);
      renderTimeline(data.timeline);
    } catch (e) { console.error('Dashboard加载失败:', e); }
  }

  // KPI 卡片
  function renderSummaryCards(cards) {
    const el = $('#summaryCards');
    if (!el || !cards) return;
    el.innerHTML = cards.map(c => `
      <div class="stat-card">
        <div class="stat-icon" style="background:${c.color}18;color:${c.color}">
          <i class="fas ${c.icon}"></i>
        </div>
        <div class="stat-value">${c.value}</div>
        <div class="stat-label">${c.title}</div>
        <div class="stat-desc">${c.desc}</div>
      </div>`).join('');
  }

  // CTR 趋势折线图 (Canvas)
  function renderCTRTrend(trend) {
    const canvas = $('#ctrTrendChart');
    if (!canvas || !trend || !trend.length) return;

    const ctx = canvas.getContext('2d');
    const dpr = window.devicePixelRatio || 1;
    const rect = canvas.parentElement.getBoundingClientRect();
    const W = rect.width - 40, H = 260;
    canvas.width = W * dpr; canvas.height = H * dpr;
    canvas.style.width = W + 'px'; canvas.style.height = H + 'px';
    ctx.scale(dpr, dpr);

    const pad = { t: 20, r: 20, b: 36, l: 48 };
    const cw = W - pad.l - pad.r, ch = H - pad.t - pad.b;

    const vals = trend.map(d => d.ctr);
    const minV = Math.min(...vals) - .15, maxV = Math.max(...vals) + .1;

    function pxX(i) { return pad.l + (i / (trend.length - 1)) * cw; }
    function pxY(v) { return pad.t + ch - ((v - minV) / (maxV - minV)) * ch; }

    // 清空 & 网格线
    ctx.clearRect(0, 0, W, H);
    ctx.strokeStyle = COLORS.gridLine;
    ctx.lineWidth = 1;
    for (let i = 0; i <= 5; i++) {
      const y = pad.t + (ch / 5) * i;
      ctx.beginPath(); ctx.moveTo(pad.l, y); ctx.lineTo(W - pad.r, y); ctx.stroke();
      // Y轴标签
      const val = maxV - ((maxV - minV) / 5) * i;
      ctx.fillStyle = COLORS.textMuted;
      ctx.font = '11px Inter';
      ctx.textAlign = 'right';
      ctx.fillText(val.toFixed(2), pad.l - 8, y + 4);
    }

    // X轴标签(每隔5天)
    ctx.textAlign = 'center';
    trend.forEach((d, i) => {
      if (i % 5 === 0 || i === trend.length - 1) {
        ctx.fillText(d.date, pxX(i), H - 10);
      }
    });

    // 填充区域渐变
    const grad = ctx.createLinearGradient(0, pad.t, 0, H - pad.b);
    grad.addColorStop(0, 'rgba(59,130,246,.25)');
    grad.addColorStop(1, 'rgba(59,130,246,0)');
    ctx.beginPath();
    ctx.moveTo(pxX(0), pxY(vals[0]));
    trend.forEach((d, i) => { ctx.lineTo(pxX(i), pxY(vals[i])); });
    ctx.lineTo(pxX(trend.length - 1), H - pad.b);
    ctx.lineTo(pxX(0), H - pad.b);
    ctx.closePath();
    ctx.fillStyle = grad; ctx.fill();

    // 线条
    ctx.beginPath();
    trend.forEach((d, i) => {
      i === 0 ? ctx.moveTo(pxX(i), pxY(vals[i])) : ctx.lineTo(pxX(i), pxY(vals[i]));
    });
    ctx.strokeStyle = COLORS.chartLine;
    ctx.lineWidth = 2.5;
    ctx.lineCap = 'round';
    ctx.lineJoin = 'round';
    ctx.stroke();

    // 数据点
    trend.forEach((d, i) => {
      if (i % 3 === 0 || i === trend.length - 1) {
        ctx.beginPath();
        ctx.arc(pxX(i), pxY(vals[i]), 4, 0, Math.PI * 2);
        ctx.fillStyle = '#fff';
        ctx.fill();
        ctx.strokeStyle = COLORS.chartLine;
        ctx.lineWidth = 2;
        ctx.stroke();
      }
    });
  }

  // 召回路由饼图 (Canvas)
  function renderRecallPie(routes) {
    const canvas = $('#recallChart');
    if (!canvas || !routes) return;

    const ctx = canvas.getContext('2d');
    const dpr = window.devicePixelRatio || 1;
    const W = canvas.parentElement.getBoundingClientRect().width - 40;
    const H = 260;
    canvas.width = W * dpr; canvas.height = H * dpr;
    canvas.style.width = W + 'px'; canvas.style.height = H + 'px';
    ctx.scale(dpr, dpr);

    const cx = W / 2, cy = H / 2 - 10, R = Math.min(cx, cy) - 30;
    const total = routes.reduce((s, r) => s + r.value, 0);

    let startAngle = -Math.PI / 2;

    routes.forEach((r, i) => {
      const slice = (r.value / total) * Math.PI * 2;
      ctx.beginPath();
      ctx.moveTo(cx, cy);
      ctx.arc(cx, cy, R, startAngle, startAngle + slice);
      ctx.closePath();
      ctx.fillStyle = COLORS.pieColors[i % COLORS.pieColors.length];
      ctx.fill();
      // 分割白线
      ctx.strokeStyle = '#0f1117';
      ctx.lineWidth = 2;
      ctx.stroke();

      // 标签
      const midA = startAngle + slice / 2;
      const labelR = R * 0.68;
      const lx = cx + Math.cos(midA) * labelR;
      const ly = cy + Math.sin(midA) * labelR;
      ctx.fillStyle = '#e4e6f0';
      ctx.font = 'bold 12px Inter';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText(r.value + '%', lx, ly);

      // 外部名称
      const nameR = R + 20;
      const nx = cx + Math.cos(midA) * nameR;
      const ny = cy + Math.sin(midA) * nameR;
      ctx.fillStyle = COLORS.textMuted;
      ctx.font = '11px Inter';
      ctx.fillText(r.name.length > 7 ? r.name.slice(0, 7) + '..' : r.name, nx, ny);

      startAngle += slice;
    });

    // 中心圆（环形效果）
    ctx.beginPath();
    ctx.arc(cx, cy, R * .42, 0, Math.PI * 2);
    ctx.fillStyle = '#1c1e2a';
    ctx.fill();
    ctx.fillStyle = '#e4e6f0';
    ctx.font = 'bold 14px Inter';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText('召回源', cx, cy - 6);
    ctx.font = '11px Inter';
    ctx.fillStyle = COLORS.textMuted;
    ctx.fillText('分布', cx, cy + 10);
  }

  // 品类 CTR 对比柱状图 (HTML/CSS)
  function renderCategoryCTR(categories) {
    const el = $('#categoryCtrChart');
    if (!el || !categories) return;
    const maxCt = Math.max(...categories.map(c => c.ctr));
    el.innerHTML = categories.map((c, i) => `
      <div class="cat-bar-row">
        <span class="cat-bar-label">${c.category}</span>
        <div class="cat-bar-track">
          <div class="cat-bar-fill" style="width:${(c.ctr / maxCt) * 100}%;background:${COLORS.barColors[i]}">${c.ctr}%</div>
        </div>
        <span class="cat-bar-value">${fmt(c.count)}</span>
      </div>`).join('');
    // 动画延迟触发
    requestAnimationFrame(() =>
      $$('.cat-bar-fill', el).forEach(bar => bar.style.transitionDelay = '.3s')
    );
  }

  // 实验监控表格
  function renderExperimentTable(exps) {
    const el = $('#experimentTable');
    if (!el || !exps) return;
    el.innerHTML = `
      <table class="exp-table">
        <thead><tr>
          <th>实验名称</th><th>状态</th><th>核心指标</th><th>Baseline</th>
          <th>Treatment</th><th>Lift</th><th>置信度</th><th>样本量</th>
        </tr></thead>
        <tbody>${exps.map(e => {
          const statusCls = e.status === '运行中' ? 'run' : e.status === '已通过' ? 'pass' : 'plan';
          const liftCls = e.lift && e.lift.startsWith('+') ? 'positive' : 'neutral';
          return `<tr>
            <td class="exp-name">${e.name}</td>
            <td><span class="exp-status ${statusCls}">${e.status}</span></td>
            <td>${e.metric}</td><td>${e.baseline}</td><td>${e.treatment}</td>
            <td class="exp-lift ${liftCls}">${e.lift}</td>
            <td>${e.confidence}</td><td>${e.samples}</td>
          </tr>`;
        }).join('')}</tbody>
      </table>`;
  }

  // 时间线
  function renderTimeline(events) {
    const el = $('#projectTimeline');
    if (!el || !events) return;
    el.innerHTML = `<div class="timeline">${events.map(e =>
      `<div class="tl-item">
         <div class="tl-dot ${e.type}"></div>
         <div class="tl-date">${e.date}</div>
         <div class="tl-event">${e.event}</div>
       </div>`
    ).join('')}</div>`;
  }

  // ==================== 2. 研究项目 ====================
  async function loadProjects() {
    try {
      const res = await fetch('/api/projects');
      const data = await res.json();
      renderProjectGrid(data.projects);
    } catch (e) { console.error('Projects加载失败:', e); }
  }

  function renderProjectGrid(projects) {
    const el = $('#projectGrid');
    if (!el) return;
    el.innerHTML = projects.map(p => {
      const catColor = COLORS.categoryColors[p.category] || '#3b82f6';
      const statusCls = p.status === '已完成' ? 'proj-status-done' :
                         p.status === '进行中' ? 'proj-status-active' : 'proj-status-plan';
      const metricsHtml = p.metrics ?
        Object.entries(p.metrics).map(([k,v]) =>
          `<div class="proj-metric"><span class="pm-val">${v}</span><span class="pm-key">${k}</span></div>`
        ).join('') : '';

      const descLines = p.description.split('\n');
      const shortDesc = descLines.filter(l => l.trim()).slice(0, 4).join('\n');

      return `<div class="proj-card">
        <div class="proj-card-header">
          <div class="proj-icon-wrap" style="background:${catColor}18;color:${catColor}">
            <i class="fas ${p.icon}"></i>
          </div>
          <div class="proj-title-area">
            <span class="proj-category" style="background:${catColor}18;color:${catColor}">${p.category}</span>
            <h3>${p.title}</h3>
          </div>
        </div>
        <div class="proj-card-body">
          <p class="proj-desc">${shortDesc}</p>
          <div class="proj-tech-tags">${(p.tech_stack||[]).map(t =>
            `<span class="tech-tag">${t}</span>`).join('')}</div>
        </div>
        <div class="proj-card-footer">
          <div class="proj-metrics">${metricsHtml}</div>
          <div style="display:flex;align-items:center;gap:14px;">
            <div class="progress-bar-track"><div class="progress-bar-fill" style="width:${p.progress}%;background:${catColor}"></div></div>
            <span class="proj-status-tag ${statusCls}">${p.status}</span>
          </div>
        </div>
      </div>`;
    }).join('');
  }

  // ==================== 3. 技术架构 ====================
  async function loadArchitecture() {
    try {
      const res = await fetch('/api/architecture');
      const data = await res.json();
      renderArchLayers(data.layers);
    } catch (e) { console.error('Architecture加载失败:', e); }
  }

  function renderArchLayers(layers) {
    const el = $('#archContainer');
    if (!el) return;
    el.innerHTML = layers.map(layer => `
      <div class="arch-layer">
        <div class="arch-layer-header">
          <div class="arch-icon"><i class="fas ${layer.layer_icon}"></i></div>
          <h3>${layer.layer_name}</h3>
          <p>${layer.layer_desc}</p>
        </div>
        <div class="arch-components">
          ${(layer.components||[]).map(c => `
            <div class="arch-comp">
              <h4>${c.comp_name}</h4>
              <p>${c.comp_desc}</p>
              <div class="arch-comp-tags">${(c.comp_tags||[]).map(t =>
                `<span class="arch-tag">${t}</span>`).join('')}</div>
            </div>`).join('')}
        </div>
      </div>`).join('');
  }

  // ==================== 4. 知识图谱 (SVG) ====================
  let _kgData = null;

  async function loadKnowledgeGraph() {
    try {
      const res = await fetch('/api/knowledge-graph');
      _kgData = await res.json();
      renderKnowledgeGraph(_kgData);
    } catch (e) { console.error('KG加载失败:', e); }
  }

  function renderKnowledgeGraph(data) {
    const svg = $('#kgSvg');
    const detailPanel = $('#nodeDetail');
    if (!svg || !data || !data.nodes) return;

    const W = svg.clientWidth || 900, H = svg.clientHeight || 550;
    svg.setAttribute('viewBox', `0 0 ${W} ${H}`);

    let nodes = data.nodes.map(n => ({
      ...n,
      x: n.x || W/2 + (Math.random()-.5)*300,
      y: n.y || H/2 + (Math.random()-.5)*250,
      vx: 0, vy: 0,
    }));
    const edges = data.edges || [];

    // 简单力导向迭代
    for (let iter = 0; iter < 60; iter++) {
      // 斥力
      for (let i = 0; i < nodes.length; i++) {
        for (let j = i+1; j < nodes.length; j++) {
          const dx = nodes[j].x - nodes[i].x, dy = nodes[j].y - nodes[i].y;
          const dist = Math.sqrt(dx*dx + dy*dy) || 1;
          const force = 3000 / (dist * dist);
          const fx = dx / dist * force, fy = dy / dist * force;
          nodes[i].vx -= fx; nodes[i].vy -= fy;
          nodes[j].vx += fx; nodes[j].vy += fy;
        }
      }
      // 引力（边）
      edges.forEach(e => {
        const src = nodes.find(n => n.id === e.source);
        const tgt = nodes.find(n => n.id === e.target);
        if (!src || !tgt) return;
        const dx = tgt.x - src.x, dy = tgt.y - src.y;
        const dist = Math.sqrt(dx*dx + dy*dy) || 1;
        const force = (dist - 140) * .03;
        const fx = dx / dist * force, fy = dy / dist * force;
        src.vx += fx; src.vy += fy;
        tgt.vx -= fx; tgt.vy -= fy;
      });
      // 中心引力 + 应用速度
      nodes.forEach(n => {
        n.vx += (W/2 - n.x) * .001; n.vy += (H/2 - n.y) * .001;
        n.vx *= .85; n.vy *= .85;
        n.x += n.vx; n.y += n.vy;
        // 边界约束
        n.x = Math.max(40, Math.min(W-40, n.x));
        n.y = Math.max(40, Math.min(H-40, n.y));
      });
    }

    // 渲染边
    let edgeHtml = '';
    edges.forEach(e => {
      const s = nodes.find(n => n.id === e.source);
      const t = nodes.find(n => n.id === e.target);
      if (!s || !t) return;
      const mx = (s.x + t.x) / 2, my = (s.y + t.y) / 2;
      edgeHtml += `<line class="kg-edge-line" x1="${s.x}" y1="${s.y}" x2="${t.x}" y2="${t.y}" />`;
      edgeHtml += `<text class="kg-edge-label" x="${mx}" y="${my-4}">${e.relation}</text>`;
    });

    // 渲染节点
    let nodeHtml = '';
    nodes.forEach(n => {
      nodeHtml += `
        <g class="kg-node-group" data-id="${n.id}" data-label="${n.label}" data-type="${n.node_type}"
           data-detail="${(n.detail||'').replace(/"/g,'&quot;')}" style="cursor:pointer">
          <circle class="kg-node-circle" cx="${n.x}" cy="${n.y}" r="${n.size}"
                  fill="${n.color}" fill-opacity=".75"
                  stroke="${n.color}" stroke-width="1.5" />
          <text class="kg-node-label" x="${n.x}" y="${n.y + n.size + 14}">${n.label}</text>
        </g>`;
    });

    svg.innerHTML = edgeHtml + nodeHtml;

    // 点击事件
    $$('.kg-node-group', svg).forEach(group => {
      group.addEventListener('click', () => {
        const id = group.dataset.id;
        const label = group.dataset.label;
        const type = group.dataset.type;
        const detail = group.dataset.detail;

        // 高亮当前节点
        $$('.kg-node-circle', svg).forEach(c => c.setAttribute('stroke-width', '1.5'));
        $('circle', group).setAttribute('stroke-width', '3.5');

        // 找出相关边
        const relEdges = edges.filter(e => e.source === id || e.target === id);
        const relNames = new Set();
        relEdges.forEach(e => {
          const otherId = e.source === id ? e.target : e.source;
          const otherNode = nodes.find(n => n.id === otherId);
          if (otherNode) relNames.add(otherNode.label);
        });

        const typeLabel = type === 'domain' ? '核心领域' : type === 'tech' ? '算法技术' : '工具平台';
        detailPanel.innerHTML = `
          <div class="node-detail-type" style="color:${type==='domain'?COLORS.chartLine:type==='tech'?COLORS.pieColors[1]:COLORS.pieColors[2]}">${typeLabel}</div>
          <div class="node-detail-title">${label}</div>
          <div class="node-detail-text">${detail || '暂无详细描述'}</div>
          ${relNames.size > 0 ? `
          <div class="node-detail-relations">
            <h5>关联节点 (${relNames.size})</h5>
            ${Array.from(relNames).map(n => `<div class="relation-item"><strong>${n}</strong> — ${edges.find(e=>
              (e.source===id&&nodes.find(nn=>nn.id===e.target)?.label===n)||
              (e.target===id&&nodes.find(nn=>nn.id===e.source)?.label===n)
            )?.relation||'related_to'}</div>`).join('')}
          </div>` : ''}`;
      });
    });
  }

  // ==================== 5. 飞书集成 ====================
  async function loadFeishu() {
    try {
      const res = await fetch('/api/feishu');
      const data = await res.json();
      renderFsFeatures(data.features);
      renderFsMessages(data.messages);
    } catch (e) { console.error('飞书加载失败:', e); }
  }

  function renderFsFeatures(features) {
    const el = $('#feishuFeatures');
    if (!el) return;
    el.innerHTML = (features||[]).map(f => {
      const sc = f.status === 'active' ? 'fs-status-active' :
               f.status === 'planned' ? 'fs-status-planned' : 'fs-disabled';
      return `<div class="fs-feature-card">
        <div class="fs-fc-header">
          <div class="fs-fc-icon"><i class="fas ${f.icon}"></i></div>
          <span class="fs-fc-name">${f.name}</span>
        </div>
        <p class="fs-fc-desc">${f.description}</p>
        <div class="fs-fc-status"><span class="fs-status-pill ${sc}">${
          f.status === 'active'?'已启用': f.status === 'planned'?'规划中':'未启用'
        }</span></div>
      </div>`}).join('');
  }

  function renderFsMessages(messages) {
    const el = $('#feishuMessages');
    if (!el) return;
    el.innerHTML = `<div class="msg-list">${(messages||[]).map(m => {
      const cls = m.type === 'alert' ? 'msg-alert' :
                 m.type === 'report' ? 'msg-report' :
                 m.type === 'paper' ? 'msg-paper' : 'msg-info';
      return `<div class="msg-item ${cls}">
        <span class="msg-time">${m.time}</span>
        <div class="msg-bubble">
          <span class="msg-type-icon">[${m.type.toUpperCase()}]</span>
          <span class="msg-text">${m.content}</span>
        </div>
      </div>`}).join('')}</div>`;
  }

  // ==================== 初始化 ====================
  function init() {
    initNav();
    initClock();
    // 默认加载首页
    loadPageData('dashboard');
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
