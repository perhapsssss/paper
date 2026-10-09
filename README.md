# 论文译读室

静态论文库。首页支持论文检索和标签筛选；每篇论文保留独立的中文/原文对照阅读页、公式、图表和术语。

## 本地预览

```powershell
python -m http.server 8000
```

访问 `http://localhost:8000`。

## 添加论文

1. 用 `article_translator` 生成完整阅读项目。
2. 将项目放入 `papers/<short-id>/`，其中 `<short-id>` 使用小写英文和连字符。
3. 确认目录包含 `translation-reading.html`、`original.pdf` 和 `assets/figures/` 中的封面图。
4. 在 `papers.json` 添加元数据对象，路径使用相对站点根目录的路径。
5. 预览目录卡片、检索、筛选和阅读页链接。

## GitHub Pages 发布

仓库已包含 `.github/workflows/pages.yml`。把站点推送到 GitHub 仓库 `main` 分支后，工作流会自动发布。首次发布前，在仓库 **Settings → Pages → Build and deployment** 中把来源设为 **GitHub Actions**。部署完成后，Actions 页面会显示网站网址。

当前首篇论文及原文 PDF 已复制为普通文件放在 `papers/humanoid-nonlinear-state-estimation/`，可与网站一起发布。

公开发布前，请确认你有权公开论文原文 PDF、图表和译文。
