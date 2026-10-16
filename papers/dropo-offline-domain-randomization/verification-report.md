# 翻译项目核查报告

- 论文：DROPO: Sim-to-Real Transfer with Offline Domain Randomization，arXiv:2201.08434v2，16 页；已保留原始 PDF 和逐页文本提取。
- 译文文件：`translation/1-full-zh.md`，包含摘要、主文第 1–5 节、方法公式 (1)–(3)、关键实验数值，以及附录 A–D 译读。
- 阅读器：`translation-reading.html`，支持中文阅读与中英公式/图注摘录对照、章节导航、术语解释、MathJax 和原文 PDF 链接。
- 图表：图 1–12 从 PDF 页面裁切并核查；图注译文为独立正文。附录的完整结果图 D.16–D.21 仍在原 PDF 中。
- 元数据：已将论文加入站点 `papers.json` 及 `site.js` 离线目录回退数据；版本题名、作者、期刊卷页与 DOI 依据 arXiv 记录和期刊页面核对。

## 检查结果

- PDF 页数确认：16 页；页面文本提取：16 份。
- Article Translator 项目检查：通过（公式源与渲染、图像路径、MathJax 配置均通过）。
- `site.js` JavaScript 语法检查：通过。
- 目录 JSON 与项目文件路径：需随提交前再做一次站点级核查。

## 译读范围说明

正文按章节翻译并保留方法、实验设置、主要定量结论及关键表格数据；附录 A 的论证已译，附录 B–D 的补充噪声敏感性、数据量分析及 BayesSim 联合分布图以结构化摘要呈现。参考文献保持英文原文。完整表格和附录图可在原文 PDF 中核对。

## 公式显示问题修复（2026-10-16）

- 根因：Markdown 解析器会把 `\(`、`\)` 识别为转义字符，并将公式中的下划线/星号解释成 Markdown 标记；此外，页面在 MathJax 延迟脚本加载前调用了排版接口。
- 修复：阅读器生成脚本先将行内和块级数学内容替换为安全占位符，完成 Markdown 转换后再恢复 MathJax 分隔符；MathJax 加载完成后再执行初次排版，模式切换时也检查接口是否就绪。
- 复核：重新构建阅读页；Article Translator 项目检查通过，HTML 中公式片段保留为完整 LaTeX，不再被 Markdown 拆解。