# 翻译项目核查报告

## 输出范围

- 模式：完整阅读输出（full-reading-output）。
- 译文文件：`translation/1-full-zh.md`。
- 阅读器：`translation-reading.html`，支持中文阅读、段落对照、目录导航、术语栏、MathJax 公式和打印样式。
- 段落对照：`alignment.json`，共 20 条记录，含标题、摘要、引言、方法、仿真、结论、附录和公式组。
- 图表地图：`figure-map.json`，共 15 项（正文 14 幅图、附录伪代码图）。

## 已执行检查

1. 运行 `article_translator/scripts/verify_translation_project.py`：**通过**。
2. 检查图表地图引用的素材：15 项均有文件。
3. 检查 HTML 图片引用：15 处，缺失引用 0。
4. 检查 alignment JSON：有效 JSON，20 条记录，4 条公式组记录包含可渲染数学源。
5. 对照原 PDF 页面图像抽查式 (1)–(8)、式 (12)–(27) 的编号、符号和主要项；核查图 4、图 5、图 7–14 和附录伪代码图。

## 保留事项与限制

- 原 PDF 中式 (16)–(19) 的部分矩阵排版与邻栏交叠；译文保留了可以可靠识别的公式内容，并标出了无法确认的矩阵细节。式 (27)、(30) 中若干导数矩阵也按原文可读内容概述，完整矩阵应以 PDF 页面为准。
- 图 1 的 LIPM/CIP 矢量线稿无法作为独立位图提取；图题和模型顺序已译出，图表地图说明了图像资产限制。图 3 的右侧简化结构来自复合矢量图，译文用图注与正文文字补足含义。
- 参考文献 [1]–[38] 保留英文条目并由原 PDF 定位，未逐条重排进译文。作者简介版面为多栏交错，译文未将简介强行对应到个人。
- PDF 的参考文献和作者照片仍可在项目中的 `source-pages/` 与原始 PDF 查阅；`source.md` 保存 PDF 文本层提取结果。

## 项目文件

- `translation/1-full-zh.md`
- `translation-reading.html`
- `source.md`
- `source-pages/`
- `glossary.md`
- `style-guide.md`
- `chapter-index.md`
- `alignment.json`
- `figure-map.json`
- `assets/figures/`
- `build_reader.py`
- `check_assets.py`
