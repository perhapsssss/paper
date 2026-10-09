const grid=document.getElementById('paperGrid');
const search=document.getElementById('search');
const filters=document.getElementById('filters');
let papers=[];
let activeTag='全部';
const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
function card(p,i){return `<article class="card"><a href="${esc(p.reader)}" aria-label="阅读：${esc(p.title)}"><div class="card-visual"><span class="card-number">NO. ${String(i+1).padStart(2,'0')}</span><img src="${esc(p.cover)}" alt="论文图表预览" loading="lazy"></div></a><div class="card-body"><div class="card-meta"><span>${esc(p.venue)}</span><span>${esc(p.year)}</span></div><h3>${esc(p.title)}</h3><p class="original-title">${esc(p.title_original)}</p><p class="card-abstract">${esc(p.abstract)}</p><div class="tag-row">${(p.tags||[]).map(t=>`<span class="tag">${esc(t)}</span>`).join('')}</div></div><a class="card-foot" href="${esc(p.reader)}"><span>打开阅读页 · ${esc(p.status)}</span><span>↗</span></a></article>`}
function draw(){const q=search.value.trim().toLowerCase();const shown=papers.filter(p=>(activeTag==='全部'||p.tags.includes(activeTag))&&(!q||[p.title,p.title_original,p.authors.join(' '),p.abstract,...p.tags].join(' ').toLowerCase().includes(q)));grid.innerHTML=shown.map(p=>card(p,papers.indexOf(p))).join('');document.getElementById('empty').hidden=shown.length>0;document.getElementById('paperCount').textContent=String(papers.length).padStart(2,'0');document.getElementById('allCount').textContent=papers.length;}
function makeFilters(){const tags=[...new Set(papers.flatMap(p=>p.tags||[]))];filters.innerHTML=`<button class="filter active" data-tag="全部">全部 <span>${papers.length}</span></button>`+tags.map(t=>`<button class="filter" data-tag="${esc(t)}">${esc(t)} <span>${papers.filter(p=>p.tags.includes(t)).length}</span></button>`).join('');filters.addEventListener('click',e=>{const b=e.target.closest('button[data-tag]');if(!b)return;activeTag=b.dataset.tag;filters.querySelectorAll('.filter').forEach(x=>x.classList.toggle('active',x===b));draw();});}
search.addEventListener('input',draw);
// Keep the directory available when index.html is opened directly from disk.
// papers.json remains the canonical editable catalog for the local-server mode.
const embeddedPapers=[
  {id:'humanoid-nonlinear-state-estimation',title:'人形机器人非线性状态估计框架',title_original:'A nonlinear state estimation framework for humanoid robots',authors:['Jingchao Li','Zhaohui Yuan','Sheng Dong','Jingqin Zhang','Jianrui Zhang'],year:2022,venue:'Robotics and Autonomous Systems 153, 104100',doi:'10.1016/j.robot.2022.104100',tags:['人形机器人','状态估计','DLKF','IEKF'],abstract:'提出融合 IMU、关节编码器和足底 FSR 的非线性状态估计框架，使用 DLKF 补偿模型误差，并用 IEKF 估计浮动基座运动学。',project:'papers/humanoid-nonlinear-state-estimation',reader:'papers/humanoid-nonlinear-state-estimation/translation-reading.html',cover:'papers/humanoid-nonlinear-state-estimation/assets/figures/fig-14.png',status:'已完成'}
];
fetch('papers.json').then(r=>{if(!r.ok)throw Error('papers.json unavailable');return r.json()}).then(data=>{papers=data;makeFilters();draw()}).catch(()=>{papers=embeddedPapers;makeFilters();draw()});
