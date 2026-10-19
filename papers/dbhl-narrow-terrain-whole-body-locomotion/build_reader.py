from pathlib import Path
import json, re, html
import markdown

ROOT = Path(__file__).parent
source = (ROOT / 'translation' / '1-full-zh.md').read_text(encoding='utf-8-sig')
math_fragments = {}
def protect_math(match, display=False):
    token = f'MATHFRAGMENTTOKEN{len(math_fragments):04d}X'
    math_fragments[token] = (match.group(1), display)
    return token
source = re.sub(r'\$\$(.+?)\$\$', lambda m: protect_math(m, True), source, flags=re.S)
source = re.sub(r'(?<!\$)\$(?!\$)(.+?)(?<!\$)\$(?!\$)', lambda m: protect_math(m, False), source, flags=re.S)
source = re.sub(r'\\\[(.+?)\\\]', lambda m: protect_math(m, True), source, flags=re.S)
source = re.sub(r'\\\((.+?)\\\)', lambda m: protect_math(m, False), source, flags=re.S)
title = re.search(r'^# (.+)$', source, re.M).group(1)
rendered = markdown.markdown(source, extensions=['extra', 'tables', 'fenced_code', 'toc'])
for token, (formula, display) in math_fragments.items():
    left, right = ('\\[', '\\]') if display else ('\\(', '\\)')
    markup = f'<span class="math-fragment" style="display:{"block" if display else "inline"}">{left}{html.escape(formula, quote=False)}{right}</span>'
    rendered = rendered.replace(token, markup)
rendered = re.sub(r'\b(src|href)="\.\./assets/', r'\1="assets/', rendered)
term_links = {
    '零力矩点（zero moment point，ZMP）': 'zero-moment-point-zmp',
    'DBHL（Dynamic Balanced Humanoid Locomotion，动态平衡人形运动）': 'dynamic-balanced-humanoid-locomotion-dbhl',
    '零力矩线（ZML）': 'zero-moment-line-zml',
    '非对称 actor-critic 框架': 'asymmetric-actor-critic',
    '奖励向量化': 'reward-vectorization',
    '乘性动作噪声': 'multiplicative-action-noise',
}
for label, target in term_links.items():
    rendered = rendered.replace(label, f'<a class="term-link" href="#term-{target}">{label}</a>', 1)
headings = re.findall(r'<h([1-3]) id="([^"]+)">(.*?)</h\1>', rendered)
strip_tags = lambda value: re.sub(r'<.*?>', '', value)
toc = '<ul>' + ''.join(
    f'<li class="level-{level}"><a href="#{hid}">{strip_tags(label)}</a></li>'
    for level, hid, label in headings if level in ('2', '3')
) + '</ul>'

terms = []
for line in (ROOT / 'glossary.md').read_text(encoding='utf-8-sig').splitlines():
    if line.startswith('| ') and not line.startswith('| English') and '---' not in line:
        cells = [cell.strip() for cell in line.strip('|').split('|')]
        if len(cells) >= 4:
            terms.append(cells[:4])
terms_html = ''.join(
    '<details id="term-' + re.sub(r'[^a-z0-9]+', '-', en.lower()).strip('-') + '"><summary>' + html.escape(en) + '（' + html.escape(zh) + '）</summary>'
    '<p>' + html.escape(explanation) + '</p></details>'
    for en, zh, _policy, explanation, *_ in terms
)

pairs = []
for row in json.loads((ROOT / 'alignment.json').read_text(encoding='utf-8')):
    source_text = row['source']
    translations = row['translation']
    translation_html = ('\n'.join(translations) if row['type'] == 'equation'
                        else markdown.markdown('\n\n'.join(translations), extensions=['extra', 'tables']))
    pair_id = f'pair-eq-{html.escape(row["id"])}' if row['type'] == 'equation' else ''
    pairs.append(
        f'<section class="pair" id="{pair_id}"><div class="source-left">'
        f'<small>{html.escape(row["section"])} · {html.escape(row["type"])}</small>'
        f'<div class="pair-content">{source_text}</div></div><div class="translation-right">'
        f'<small>中文</small><div class="pair-content">{translation_html}</div></div></section>'
    )

page = f'''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="theme-color" content="#f3f2ed"><title>{html.escape(title)}｜中译阅读版</title>
<script>window.MathJax={{tex:{{inlineMath:[['$', '$'],['\\\\(','\\\\)']],displayMath:[['$$','$$'],['\\\\[','\\\\]']],processEscapes:true,processEnvironments:true}}}};</script>
<script defer src="../../assets/mathjax/tex-svg-full.js" onload="MathJax.typesetPromise()"></script>
<style>
:root{{--ink:#252a31;--muted:#66717f;--accent:#246b73;--paper:#fff;--bg:#f1f3f4;--line:#dce1e4}}*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font:17px/1.82 system-ui,-apple-system,"Segoe UI",sans-serif}}header{{position:sticky;top:0;z-index:5;background:#ffffffed;border-bottom:1px solid var(--line);backdrop-filter:blur(8px);padding:10px 18px;display:flex;gap:10px;align-items:center;flex-wrap:wrap}}header strong{{margin-right:auto;font-size:15px}}button,.tool{{border:1px solid #b9c5ca;background:white;border-radius:5px;padding:7px 12px;color:var(--ink);cursor:pointer;text-decoration:none;font:inherit;font-size:14px}}button.active{{background:var(--accent);color:white;border-color:var(--accent)}}.layout{{display:grid;grid-template-columns:220px minmax(0,860px) 220px;gap:26px;max-width:1400px;margin:24px auto;padding:0 20px;align-items:start}}nav,.terms{{position:sticky;top:76px;max-height:calc(100vh - 100px);overflow:auto;font-size:14px;line-height:1.55}}nav a{{display:block;color:#39505b;text-decoration:none;padding:3px 0}}nav ul{{padding-left:18px}}main{{background:var(--paper);padding:46px 56px;min-width:0;box-shadow:0 2px 12px #15202a0b}}h1,h2,h3{{line-height:1.35;color:#1e3038}}h1{{font-size:30px;margin-top:0}}h2{{font-size:24px;margin-top:2.2em;border-bottom:1px solid var(--line);padding-bottom:8px}}h3{{font-size:20px;margin-top:1.7em}}p{{margin:1em 0}}a{{color:var(--accent)}}img{{max-width:100%;max-height:660px;object-fit:contain;display:block;margin:1.2em auto}}.math{{overflow-x:auto;padding:8px 0}}table{{border-collapse:collapse;width:100%;display:block;overflow-x:auto;font-size:14px}}th,td{{border:1px solid var(--line);padding:7px}}.terms{{background:white;padding:14px}}.terms h3{{margin-top:0}}details{{border-top:1px solid var(--line);padding:8px 0}}summary{{cursor:pointer;color:var(--accent)}}.parallel{{display:none}}body.mode-parallel .chinese{{display:none}}body.mode-parallel .parallel{{display:block}}.pair{{display:grid;grid-template-columns:1fr 1fr;gap:22px;padding:14px 0;border-bottom:1px solid var(--line)}}.pair>div{{min-width:0;overflow-wrap:anywhere}}.pair small{{color:var(--muted);display:block;margin-bottom:6px}}.pair-content{{overflow-x:auto}}.pair-content mjx-container{{max-width:100%;overflow-x:auto;overflow-y:hidden}}@media(max-width:1100px){{.layout{{grid-template-columns:180px minmax(0,1fr)}}.terms{{display:none}}}}@media(max-width:720px){{.layout{{display:block;margin:0;padding:0}}nav{{display:none}}main{{padding:24px 18px;box-shadow:none;font-size:16px}}header{{position:static}}.pair{{grid-template-columns:1fr;gap:8px}}}}@media print{{header,nav,.terms{{display:none!important}}body,.layout{{background:white;margin:0;padding:0;display:block}}main{{box-shadow:none;padding:0;max-width:none}}body.mode-parallel .chinese{{display:block}}body.mode-parallel .parallel{{display:none}}img{{max-height:220mm}}}}
</style></head><body><header><strong>{html.escape(title)}</strong>
<button id="zhBtn" class="active" onclick="setMode('zh')">中文阅读</button><button id="parallelBtn" onclick="setMode('parallel')">中英对照摘录</button>
<a class="tool" href="original.pdf" target="_blank" rel="noopener">查看原文 PDF ↗</a><button onclick="window.print()">打印 / 导出 PDF</button></header>
<div class="layout"><nav><b>章节导航</b><div id="toc">{toc}</div></nav><main>
<article class="chinese">{rendered}</article><article class="parallel"><h1>中英对照摘录</h1>
<p>关键定义、公式、实验结论及图注对照；完整译文请切换中文阅读。</p>{''.join(pairs)}</article>
</main><aside class="terms"><h3>术语注释</h3>{terms_html}</aside></div>
<script>function setMode(mode){{document.body.classList.toggle('mode-parallel',mode==='parallel');document.getElementById('zhBtn').classList.toggle('active',mode==='zh');document.getElementById('parallelBtn').classList.toggle('active',mode==='parallel');if(window.MathJax)MathJax.typesetPromise()}}</script></body></html>'''
(ROOT / 'translation-reading.html').write_text(page, encoding='utf-8')
