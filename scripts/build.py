#!/usr/bin/env python3
"""Generate checked-in static pages. Python is only needed when editing content."""
from pathlib import Path
from html import escape as e
import json

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://bo-xing.github.io/unwrap-site/"
EMAIL = "boxing.support@gmail.com"


def icon(name="arrow"):
    paths = {
        "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
        "down": '<path d="M12 4v16M6 14l6 6 6-6"/>',
        "check": '<path d="m5 12 4 4L19 6"/>',
        "shield": '<path d="m12 3 8 3v6c0 4-5 8-8 9-3-1-8-5-8-9V6l8-3Z"/><path d="m8 12 3 3 5-6"/>',
        "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 6 9 7 9-7"/>',
    }
    return f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{paths[name]}</svg>'


def link(text, href, cls="text-link", glyph="arrow"):
    return f'<a class="{cls}" href="{e(href)}">{e(text)}{icon(glyph)}</a>'


def page_path(lang, kind):
    return ("zh/" if lang == "zh" else "") + (kind + "/" if kind != "home" else "")


def render(lang, kind, data, body):
    path = page_path(lang, kind)
    prefix = "../" * len(Path(path).parts) if path else "./"
    locale_home = prefix + ("zh/" if lang == "zh" else "")
    opposite = prefix + page_path("en" if lang == "zh" else "zh", kind)
    nav = data["nav"]
    meta = data[kind]
    current_support = ' aria-current="page"' if kind == "support" else ""
    current_privacy = ' aria-current="page"' if kind == "privacy" else ""
    brand = f'<a class="brand" href="{locale_home}" aria-label="Unwrap"><img src="{prefix}assets/app-icon.png" width="38" height="38" alt="">Unwrap</a>'
    canonical = BASE + path
    alternates = "\n".join(f'<link rel="alternate" hreflang="{code}" href="{BASE + page_path(l, kind)}">' for l, code in [("en", "en"), ("zh", "zh-Hans")])
    html = f'''<!doctype html>
<html lang="{data['lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(meta['title'])}</title>
<meta name="description" content="{e(meta['description'])}">
<meta name="theme-color" content="#f7f8f4">
<link rel="canonical" href="{canonical}">
{alternates}
<link rel="alternate" hreflang="x-default" href="{BASE + page_path('en', kind)}">
<meta property="og:type" content="website">
<meta property="og:title" content="{e(meta['title'])}">
<meta property="og:description" content="{e(meta['description'])}">
<meta property="og:url" content="{canonical}">
<meta property="og:locale" content="{data['locale']}">
<meta property="og:image" content="{BASE}assets/app-icon.png">
<meta name="twitter:card" content="summary">
<link rel="icon" type="image/png" href="{prefix}assets/app-icon.png">
<link rel="apple-touch-icon" href="{prefix}assets/app-icon.png">
<link rel="stylesheet" href="{prefix}assets/site.css">
</head>
<body>
<a class="skip" href="#main">{e(nav['skip'])}</a>
<header class="header container">
{brand}
<nav class="nav" aria-label="{'主导航' if lang == 'zh' else 'Main navigation'}">
<a class="desktop-link" href="{locale_home}#features">{e(nav['features'])}</a>
<a class="desktop-link" href="{locale_home}#pricing">{e(nav['pricing'])}</a>
<a href="{locale_home}support/"{current_support}>{e(nav['support'])}</a>
<a class="language" lang="{'en' if lang == 'zh' else 'zh-Hans'}" href="{opposite}">{e(nav['language'])}</a>
</nav>
</header>
<main id="main" class="container">
{body}
</main>
<footer class="footer container">
<div class="footer-top">{brand}<nav class="footer-links" aria-label="{'页脚导航' if lang == 'zh' else 'Footer navigation'}">
<a href="{locale_home}support/"{current_support}>{e(nav['support'])}</a>
<a href="{locale_home}privacy/"{current_privacy}>{e(nav['privacy'])}</a>
<a href="mailto:{EMAIL}">{EMAIL}</a>
</nav></div>
<div class="footer-bottom"><span>{e(data['footer']['copyright'])} · {e(data['footer']['line'])}</span><span>{e(data['footer']['note'])}</span></div>
</footer>
</body>
</html>
'''
    output = ROOT / path / "index.html"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(html)


def home(lang, d):
    h = d["home"]
    prefix = "../" if lang == "zh" else "./"
    rows = "".join(f'<div class="sample-row"><span class="file-glyph">{e(kind)}</span><span class="file-copy"><strong>{e(name)}</strong><small>{e(note)}</small></span><span class="file-check {"selected" if i == 0 else ""}">{"✓" if i == 0 else ""}</span></div>' for i, (kind, name, note) in enumerate(h["art_files"]))
    features = "".join(f'<article class="feature"><span class="feature-number">{f["number"]}</span><h3>{e(f["title"])}</h3><p>{e(f["body"])}</p><span class="feature-tag">{e(f["tag"])}</span></article>' for f in h["features"])
    cards = ""
    for tier in ["free", "pro"]:
        items = "".join(f'<li>{icon("check")}<span>{e(text)}</span></li>' for text in h[tier + "_features"])
        cards += f'<article class="price-card {tier}"><p class="eyebrow">{e(h[tier+"_label"])}</p><h3>{e(h[tier+"_title"])}</h3><p class="price">{e(h[tier+"_price"])}</p><p class="price-note">{e(h[tier+"_note"])}</p><ul>{items}</ul></article>'
    trust = "".join(f'<span>{icon("check" if i < 2 else "shield")}{e(t)}</span>' for i, t in enumerate(h["strip"]))
    formats = "".join(f'<span>{f}</span>' for f in ["ZIP", "RAR", "7z", "TAR", "GZ", "BZ2", "XZ", "ZSTD"])
    return f'''
<section class="hero" aria-labelledby="hero-title">
<div class="hero-copy"><p class="eyebrow">{e(h['eyebrow'])}</p><h1 id="hero-title">{h['heading']}</h1><p class="intro">{e(h['intro'])}</p>
<div class="actions">{link(h['primary'], '#features', 'button', 'down')}{link(h['secondary'], 'support/')}</div><p class="availability">{e(h['availability'])}</p></div>
<div class="archive-art" role="img" aria-label="{e(h['art_label'])}">
<svg class="art-star" viewBox="0 0 100 100" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M50 5v90M5 50h90M18 18l64 64M18 82l64-64"/></svg>
<div class="archive-window" aria-hidden="true"><img class="art-logo" src="{prefix}assets/app-icon.png" width="85" height="85" alt="">
<div class="art-top"><span class="art-name">{'周末小记.zip' if lang == 'zh' else 'A little weekend.zip'}</span><span class="window-dots"><i></i><i></i><i></i></span></div>
<p class="art-count">{e(h['art_count'])}</p>{rows}<div class="art-bottom"><span>ZIP · 12.4 MB</span><span class="mini-pill">{'先看，再取出' if lang == 'zh' else 'Preview. Then pick.'}</span></div></div>
<p class="art-caption" aria-hidden="true">{e(h['art_note'])}</p></div>
</section>
<div class="trust-strip">{trust}</div>
<section class="section" id="features" aria-labelledby="features-title"><p class="eyebrow">{e(h['features_eyebrow'])}</p><div class="section-title"><h2 id="features-title">{h['features_title']}</h2><p>{e(h['features_intro'])}</p></div><div class="features-grid">{features}</div>
<div class="formats"><p class="formats-label">{e(h['formats_label'])}</p><div class="format-list">{formats}</div><small>{e(h['formats_note'])}</small></div></section>
<section class="section pricing-section" id="pricing" aria-labelledby="pricing-title"><p class="eyebrow">{e(h['pricing_eyebrow'])}</p><div class="section-title"><h2 id="pricing-title">{h['pricing_title']}</h2><p>{e(h['pricing_intro'])}</p></div><div class="pricing-grid">{cards}</div><p class="pricing-fine">{e(h['price_note'])}</p></section>
<section class="privacy-panel" aria-labelledby="privacy-title"><div><p class="eyebrow">{e(h['privacy_eyebrow'])}</p><h2 id="privacy-title">{h['privacy_title']}</h2></div><div><p>{e(h['privacy_body'])}</p>{link(h['privacy_link'], 'privacy/')}</div></section>
<section class="closing"><h2>{h['closing_title']}</h2><p>{e(h['closing_body'])}</p>{link(h['closing_link'], 'support/')}</section>
'''


def support(lang, d):
    s = d["support"]
    faqs = "".join(f'<details><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in s["faqs"])
    return f'''
<section class="page-hero"><p class="eyebrow">{e(s['eyebrow'])}</p><h1>{s['heading']}</h1><p class="intro">{e(s['intro'])}</p><div class="contact-line">{link(s['contact'], f'mailto:{EMAIL}?subject=Unwrap%20Support', 'button', 'mail')}<span class="contact-address">{EMAIL}</span></div><p class="contact-note">{e(s['contact_note'])}</p></section>
<div class="support-grid"><section><h2>{e(s['faq_title'])}</h2><div class="faq-list">{faqs}</div></section><aside class="support-aside"><h2>{e(s['details_title'])}</h2><p>{e(s['details_body'])}</p><div class="refund"><h3>{e(s['refund_title'])}</h3><p>{e(s['refund_body'])}</p><a href="https://reportaproblem.apple.com/">{e(s['refund_link'])} ↗</a></div></aside></div>
'''


def privacy(lang, d):
    p = d["privacy"]
    toc = "".join(f'<a href="#section-{i}">{e(title)}</a>' for i, (title, _) in enumerate(p["sections"], 1))
    sections = "".join(f'<section id="section-{i}"><h2>{e(title)}</h2><p>{e(text).replace(EMAIL, f"<a href=\"mailto:{EMAIL}\">{EMAIL}</a>")}</p></section>' for i, (title, text) in enumerate(p["sections"], 1))
    return f'''
<section class="page-hero"><p class="eyebrow">{e(p['eyebrow'])}</p><h1>{p['heading']}</h1><p class="intro">{e(p['intro'])}</p><p class="updated">{e(p['date'])}</p></section>
<div class="legal-layout"><nav class="toc" aria-label="{'政策目录' if lang == 'zh' else 'Policy sections'}">{toc}</nav><article class="legal-copy">{sections}<div class="legal-links"><a href="https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement">{e(p['github_link'])} ↗</a><a href="https://www.apple.com/legal/privacy/">{e(p['apple_link'])} ↗</a></div><div class="legal-contact">{e(p['question'])}<br><a href="mailto:{EMAIL}">{EMAIL}</a></div></article></div>
'''


def main():
    urls = []
    for lang in ["en", "zh"]:
        data = json.loads((ROOT / "content" / f"{lang}.json").read_text())
        for kind, renderer in [("home", home), ("support", support), ("privacy", privacy)]:
            render(lang, kind, data, renderer(lang, data))
            urls.append(BASE + page_path(lang, kind))
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    sitemap += "\n".join(f'  <url><loc>{u}</loc></url>' for u in urls) + '\n</urlset>\n'
    (ROOT / "sitemap.xml").write_text(sitemap)
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {BASE}sitemap.xml\n")
    (ROOT / "404.html").write_text('''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><title>Page not found — Unwrap</title><link rel="stylesheet" href="/unwrap-site/assets/site.css"></head><body><main class="container not-found"><p class="eyebrow">UNWRAP / 404</p><h1>This one's<br>not in the archive.</h1><p>The page may have moved. Let's go back to somewhere familiar.</p><a class="button" href="/unwrap-site/">Back to Unwrap</a> <a class="text-link" lang="zh-Hans" href="/unwrap-site/zh/">返回中文首页</a></main></body></html>''')
    print("Generated 6 localized pages, 404.html, sitemap.xml and robots.txt.")


if __name__ == "__main__":
    main()
