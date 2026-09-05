# Unwrap website

Unwrap 的中英文产品页、支持页与隐私政策。纯 HTML/CSS，无 JavaScript、第三方字体、分析 SDK 或在线构建依赖。所有网站资源均在本仓库中，适配 GitHub Pages 的 `/unwrap-site/` 子路径。

## 开启 GitHub Pages

内容推送到 GitHub 后，在仓库中打开：

`Settings → Pages → Build and deployment → Deploy from a branch → main → /(root) → Save`

根目录已有 `.nojekyll`，直接发布静态页面。如果私有仓库的账户方案不支持 Pages，需要账户拥有者选择合适的方案，或将网站仓库改为公开；不要把 App 源码、密钥或 `.env` 复制到本仓库。

默认发布网址：

| 页面 | English | 简体中文 |
|---|---|---|
| 产品首页 / Marketing URL | https://bo-xing.github.io/unwrap-site/ | https://bo-xing.github.io/unwrap-site/zh/ |
| 支持 / Support URL | https://bo-xing.github.io/unwrap-site/support/ | https://bo-xing.github.io/unwrap-site/zh/support/ |
| 隐私政策 / Privacy Policy URL | https://bo-xing.github.io/unwrap-site/privacy/ | https://bo-xing.github.io/unwrap-site/zh/privacy/ |

先确认六个网址公开返回正常页面，再填写到 App Store Connect。网站发布后，可在 Unwrap 项目的 `docs/app-store/metadata.json` 更新网址并运行 `fastlane upload_metadata`。

## 修改与预览

中英文内容来源分别为 `content/en.json`、`content/zh.json`。样式在 `assets/site.css`，HTML 模板在 `scripts/build.py`。

```bash
python3 scripts/build.py
python3 -m http.server 8080
```

本地打开 `http://localhost:8080/` 或 `/zh/`。部署不运行 Python；生成的 HTML 已纳入 Git。修改内容或模板后重新生成，并提交生成文件。图标来自 Unwrap 正式 App 资源。

## 发布状态与内容约定

- App 当前尚未发布，首页明确标记“即将登陆”，主按钮跳转到功能介绍；没有无效的下载按钮。
- App 正式上线后，将首页状态改为已上线，并添加真实 App Store 地址 `https://apps.apple.com/app/id6808937701`。
- 公共支持邮箱沿用同开发者其他产品的 `boxing.support@gmail.com`。
- 主视觉是示例压缩包内容的网页插画，带明确的辅助文字说明，并非实际 App 截图。
- Pro 为一次性非消耗型内购；网页不硬编码不同地区售价。ZIP、7z、tar.gz 创建属 Pro，创建密码保护仅支持 ZIP。
- 不宣传尚未交付的远程归档流式访问、ZIP 就地编辑或 Mac 版。
- 隐私政策分别解释 App 本地处理、共享容器与临时文件、Apple/文件提供程序、主动邮件支持和 GitHub Pages 访问日志。
- 语言切换会进入相同类型的页面；支持 FAQ 使用原生 `<details>`，不依赖 JavaScript。

## 设计

基于 UI/UX 技能的简洁排版方向，配合实际 App 图标调整为暖白、深墨绿与浅薄荷色。系统字体减少外部请求；交互目标、焦点样式、跳转链接、移动端布局与减少动态效果均有相应处理。

## 参考

- [GitHub Pages 发布来源](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)
- [GitHub Pages 数据处理说明](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages)
