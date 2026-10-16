import fitz,json,re
from pathlib import Path
root=Path('papers/dropo-offline-domain-randomization')
doc=fitz.open(root/'original.pdf')
# page index, clip rect in PDF points; rectangles stop before caption blocks.
clips={1:(0,(306,450,558,570)),2:(2,(37,55,289,184)),3:(5,(37,35,289,201)),4:(5,(306,35,558,194)),5:(6,(306,35,558,205)),6:(6,(306,235,558,368)),7:(7,(37,35,289,205)),8:(7,(37,270,289,374)),9:(7,(37,610,289,742)),10:(7,(306,35,558,191)),11:(8,(37,180,289,290)),12:(9,(37,35,289,210))}
figures=[]
for n,(page,rect) in clips.items():
 out=f'assets/figures/fig-{n:02}.png'
 pix=doc[page].get_pixmap(matrix=fitz.Matrix(2.2,2.2),clip=fitz.Rect(*rect),alpha=False)
 pix.save(root/out)
 figures.append({'number':n,'page':page+1,'path':out,'caption_id':f'fig-{n:02}-caption','method':'PDF vector page crop; caption kept as text','status':'visually inspected contact sheet; crop geometry-based'})
(root/'figure-map.json').write_text(json.dumps(figures,ensure_ascii=False,indent=2),encoding='utf-8')
PY
@'
# 章节索引

| 原文页 | 内容 | 译文位置 |
|---:|---|---|
| 1–2 | 摘要、引言、相关工作 | 摘要、1–2 节 |
| 3–4 | MDP 定义、DROPO 算法、采集与分布拟合 | 3.1–3.4 节 |
| 4–5 | 策略训练与实验设计、Hopper 实验 | 3.5、4.1–4.2.3 节 |
| 6–8 | Hopper 的 epsilon 分析、机器人任务与冰球实验 | 4.2.3–4.3.1 节 |
| 9–11 | Panda 推箱、结论、致谢 | 4.3.2–5 节、致谢 |
| 11–12 | 参考文献 | 译文保留编号，书目见原文 |
| 12–16 | 附录 A–D | 附录译读；补充图表和完整后验见 PDF |

章节号与原文对应。图 1–12 已裁切为独立图像；图注以译文文本呈现。
