#!/usr/bin/env python3

"""
将Markdown文件放在本脚本目录即可。
"""

import markdown
import re
from pathlib import Path

# ============ 配置 ============
INPUT_FILE = "Praze.md"
OUTPUT_FILE = "Praze.html"
TITLE = "Praze 设定集"
SUBTITLE = "by ZpycuA,this work is licensed under CC BY-NC 4.0. "

# ============ CSS（内嵌） ============
CSS = r"""
:root {
    --bg: #f6f2ec;
    --sidebar-bg: #1a1a2e;
    --sidebar-text: #cdd1d9;
    --accent: #8b6f47;
    --accent-light: #c9a96e;
    --card-bg: #fffefb;
    --card-border: #e0d8cc;
    --text: #2c2c2c;
    --text-muted: #6b6560;
    --code-bg: #f0ebe3;
    --table-header: #2d2d44;
    --table-header-text: #f0e6d8;
    --link: #7a5c32;
    --details-bg: #faf7f2;
    --details-border: #d8cdbb;
    --tag-bg: #e8dfd0;
    --danger: #8b2f2f;
}

* { box-sizing: border-box; }
body {
    margin: 0;
    font-family: "Noto Serif SC", "Source Han Serif SC", "Georgia", "Times New Roman", serif;
    background: var(--bg);
    color: var(--text);
    line-height: 1.8;
    font-size: 15.5px;
}

.topbar {
    position: sticky;
    top: 0;
    z-index: 100;
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 12px 28px;
    background: var(--sidebar-bg);
    color: #eee;
    border-bottom: 3px solid var(--accent);
    flex-wrap: wrap;
}

.topbar h1 {
    font-size: 1.25rem;
    margin: 0;
    letter-spacing: 2px;
    font-weight: 700;
}

.topbar .subtitle {
    font-size: 0.8rem;
    color: #aaa;
    letter-spacing: 1px;
}

.topbar .hamburger {
    display: none;
    background: none;
    border: 1px solid #666;
    color: #ddd;
    font-size: 1.2rem;
    padding: 4px 10px;
    border-radius: 4px;
    cursor: pointer;
}

.layout {
    display: flex;
    max-width: 1400px;
    margin: 0 auto;
}

.sidebar {
    width: 280px;
    flex-shrink: 0;
    background: var(--sidebar-bg);
    color: var(--sidebar-text);
    min-height: calc(100vh - 60px);
    position: sticky;
    top: 60px;
    align-self: flex-start;
    overflow-y: auto;
    padding: 24px 0;
    font-size: 0.85rem;
}

.sidebar h2 {
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 3px;
    color: #777;
    padding: 0 22px;
    margin: 0 0 12px 0;
}

.sidebar ul {
    list-style: none;
    margin: 0;
    padding: 0;
}

.sidebar li a {
    display: block;
    padding: 6px 22px;
    color: var(--sidebar-text);
    text-decoration: none;
    border-left: 3px solid transparent;
    transition: all 0.2s;
    font-size: 0.83rem;
}

.sidebar li a:hover {
    background: rgba(255,255,255,0.06);
    border-left-color: var(--accent-light);
    color: #fff;
}

.sidebar li a.active {
    background: rgba(255,255,255,0.09);
    border-left-color: var(--accent-light);
    color: #fff;
}

.content {
    flex: 1;
    padding: 36px 48px 80px 48px;
    max-width: 860px;
    min-width: 0;
}

.content h1 {
    font-size: 1.9rem;
    border-bottom: 3px double var(--accent);
    padding-bottom: 12px;
    margin-top: 0;
    margin-bottom: 20px;
    letter-spacing: 1px;
    color: #1f1a15;
}

.content h2 {
    font-size: 1.45rem;
    border-left: 4px solid var(--accent);
    padding-left: 14px;
    margin-top: 48px;
    margin-bottom: 16px;
    color: #2a241e;
    letter-spacing: 1px;
}

.content h3 {
    font-size: 1.15rem;
    margin-top: 32px;
    margin-bottom: 10px;
    color: #4a3f31;
}

.content h4 {
    font-size: 1rem;
    margin-top: 24px;
    color: #5c5040;
}

.content p { margin: 12px 0; }

.content a {
    color: var(--link);
    text-decoration: underline dotted;
    text-underline-offset: 3px;
}

.content a:hover { color: #b8860b; }

.content blockquote {
    margin: 16px 0;
    padding: 14px 20px;
    background: var(--card-bg);
    border: 1px solid var(--card-border);
    border-left: 4px solid var(--accent-light);
    border-radius: 0 8px 8px 0;
    font-style: italic;
    color: #555;
}

.content code {
    background: var(--code-bg);
    padding: 2px 6px;
    border-radius: 4px;
    font-family: "JetBrains Mono", "Fira Code", "Consolas", monospace;
    font-size: 0.85em;
    color: #5a4632;
}

.content pre {
    background: #1e1e2e;
    color: #d0d0e0;
    padding: 18px 20px;
    border-radius: 8px;
    overflow-x: auto;
    font-size: 0.82rem;
    line-height: 1.6;
}

.content pre code {
    background: none;
    color: inherit;
    padding: 0;
}

.content table {
    width: 100%;
    border-collapse: collapse;
    margin: 20px 0;
    font-size: 0.88rem;
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
}

.content thead th {
    background: var(--table-header);
    color: var(--table-header-text);
    font-weight: 600;
    text-align: left;
    padding: 10px 14px;
    letter-spacing: 0.5px;
    font-size: 0.82rem;
}

.content tbody td {
    padding: 9px 14px;
    border-bottom: 1px solid var(--card-border);
    background: var(--card-bg);
}

.content tbody tr:nth-child(even) td {
    background: #f8f4ed;
}

.content tbody tr:hover td {
    background: #f0e8da;
}

.content details {
    margin: 18px 0;
    background: var(--details-bg);
    border: 1px solid var(--details-border);
    border-radius: 10px;
    overflow: hidden;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
}

.content details summary {
    cursor: pointer;
    padding: 14px 20px;
    font-weight: 700;
    font-size: 0.92rem;
    letter-spacing: 1px;
    color: #4a3d2b;
    background: linear-gradient(135deg, #f4ede2, #eae0cd);
    user-select: none;
    list-style: none;
    position: relative;
    transition: background 0.2s;
}

.content details summary::-webkit-details-marker { display: none; }

.content details summary::before {
    content: "▸";
    display: inline-block;
    margin-right: 10px;
    transition: transform 0.25s;
    color: var(--accent);
    font-weight: bold;
}

.content details[open] summary::before {
    transform: rotate(90deg);
}

.content details summary:hover {
    background: linear-gradient(135deg, #efe5d4, #e3d5bc);
}

.content details .details-inner {
    padding: 4px 22px 18px 22px;
    border-top: 1px solid var(--details-border);
}

.content hr {
    border: none;
    border-top: 2px dashed #c9bda8;
    margin: 40px 0;
}

@media (max-width: 900px) {
    .sidebar {
        position: fixed;
        left: -300px;
        top: 0;
        height: 100vh;
        z-index: 200;
        transition: left 0.3s;
        padding-top: 70px;
        box-shadow: 2px 0 12px rgba(0,0,0,0.3);
    }
    .sidebar.open { left: 0; }
    .topbar .hamburger { display: block; }
    .content { padding: 20px 16px 60px 16px; }
    .topbar h1 { font-size: 1rem; }
}
"""

MATHJAX_CONFIG = r"""
window.MathJax = {
  tex: {
    inlineMath: [['$', '$'], ['\\(', '\\)']],
    displayMath: [['$$', '$$'], ['\\[', '\\]']],
    processEscapes: true,
    tags: 'ams'
  },
  options: {
    ignoreHtmlClass: 'no-mathjax',
    processHtmlClass: 'mathjax-process'
  }
};
"""

MATHJAX_SCRIPT = r"""
<script>
""" + MATHJAX_CONFIG + r"""
</script>
<script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
"""

# ============ Markdown 渲染函数 ============
def render_markdown(text, include_toc=True, use_md_in_html=False):
    """对给定文本做 Markdown → HTML 转换"""
    extensions = [
        "tables",
        "fenced_code",
        "attr_list",
        "def_list",
        "footnotes",
        "abbr",
        "sane_lists",
        "codehilite",
    ]
    if use_md_in_html:
        extensions.append("md_in_html")
    configs = {
        "codehilite": {
            "guess_lang": False,
            "css_class": "highlight"
        }
    }
    if include_toc:
        extensions.append("toc")
        configs["toc"] = {
            "permalink": False,
            "slugify": lambda value, separator: re.sub(r"[^\w\s-]", "", value.lower()).strip().replace(" ", separator)
        }
    return markdown.markdown(text, extensions=extensions, extension_configs=configs, output_format="html5")

# ============ 平衡提取 details 块 ============
def extract_balanced_details(text):
    """提取所有顶层 <details>...</details> 块（支持嵌套），返回 (替换后文本, 块列表)"""
    details_blocks = []
    replacements = []
    i = 0
    while i < len(text):
        start = text.find('<details>', i)
        if start == -1:
            break
        depth = 1
        pos = start + len('<details>')
        while depth > 0 and pos < len(text):
            next_open = text.find('<details>', pos)
            next_close = text.find('</details>', pos)
            if next_close == -1:
                raise ValueError("存在未闭合的 <details> 标签")
            if next_open != -1 and next_open < next_close:
                depth += 1
                pos = next_open + len('<details>')
            else:
                depth -= 1
                pos = next_close + len('</details>')
        if depth != 0:
            raise ValueError("存在未闭合的 <details> 标签")
        end = pos
        block = text[start:end]
        placeholder = f"@@DETAILS_{len(details_blocks)}@@"
        details_blocks.append(block)
        replacements.append((start, end, placeholder))
        i = end
    result = text
    for start, end, placeholder in reversed(replacements):
        result = result[:start] + placeholder + result[end:]
    return result, details_blocks

# ============ 渲染单个 details 块（递归处理嵌套） ============
def render_details_block(block):
    """渲染一个完整的 <details>...</details> 块，支持嵌套 details 的递归渲染"""
    summary_match = re.search(r'<summary>(.*?)</summary>', block, re.DOTALL)
    if not summary_match:
        return block  # 没有 summary，原样返回
    summary_text = summary_match.group(1).strip()
    inner_start = summary_match.end()
    inner_end = block.rfind('</details>')
    inner_content = block[inner_start:inner_end]
    # 去掉内部可能残留的 <div markdown="1"> 包装
    inner_content = re.sub(r'^\s*<div[^>]*markdown[^>]*>\s*', '', inner_content)
    inner_content = re.sub(r'\s*</div>\s*$', '', inner_content)

    # 提取内部嵌套的 details 块（第二层、第三层...）
    inner_with_placeholders, nested_blocks = extract_balanced_details(inner_content)

    # 对替换后的 inner_content 渲染 Markdown（不启用 md_in_html，因为嵌套 details 已被提取）
    inner_html = render_markdown(inner_with_placeholders, include_toc=False, use_md_in_html=False)

    # 递归渲染嵌套的 details 块
    rendered_nested = [render_details_block(nb) for nb in nested_blocks]

    # 将嵌套渲染结果替换回 inner_html
    for i, nested_html in enumerate(rendered_nested):
        placeholder = f"@@DETAILS_{i}@@"
        # 处理可能被 <p> 包裹的情况
        pattern = re.compile(r'<p>\s*' + re.escape(placeholder) + r'\s*</p>')
        if pattern.search(inner_html):
            inner_html = pattern.sub(lambda m: nested_html, inner_html)
        else:
            inner_html = inner_html.replace(placeholder, nested_html)

    return (
        f'<details>\n'
        f'<summary>{summary_text}</summary>\n'
        f'<div class="details-inner">\n'
        f'{inner_html}\n'
        f'</div>\n'
        f'</details>'
    )

# ============ 主逻辑 ============
def main():
    md_text = Path(INPUT_FILE).read_text(encoding="utf-8")
    md_text = md_text.replace('\r\n', '\n').replace('\r', '\n')

    # ---- 1. 提取所有顶层 <details> 块 ----
    md_text_with_placeholders, details_blocks = extract_balanced_details(md_text)

    # ---- 2. 渲染主文档（不含顶层 details） ----
    html_body = render_markdown(md_text_with_placeholders, include_toc=True)

    # ---- 3. 提取 TOC ----
    toc_pattern = re.compile(r'<div class="toc">.*?</div>', re.DOTALL)
    toc_match = toc_pattern.search(html_body)
    toc_html = toc_match.group(0) if toc_match else "<div class='toc'><ul></ul></div>"
    html_body = toc_pattern.sub("", html_body, count=1)

    # ---- 4. 渲染每个顶层 details 块（递归处理内部嵌套） ----
    rendered_details_list = [render_details_block(block) for block in details_blocks]

    # ---- 5. 替换占位符（同时去除可能包裹的 <p> 标签） ----
    for idx, rendered_details in enumerate(rendered_details_list):
        placeholder = f"@@DETAILS_{idx}@@"
        # 匹配 <p>@@DETAILS_X@@</p>，允许内部空白
        pattern = re.compile(r'<p>\s*' + re.escape(placeholder) + r'\s*</p>')
        if pattern.search(html_body):
            # 使用 lambda 避免替换字符串中的反斜杠被解析
            html_body = pattern.sub(lambda m: rendered_details, html_body)
        else:
            # 如果占位符未被段落包裹，直接替换
            html_body = html_body.replace(placeholder, rendered_details)

    # ---- 6. 组装完整 HTML ----
    full_html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{TITLE} — {SUBTITLE}</title>
<style>
{CSS}
</style>
{MATHJAX_SCRIPT}
</head>
<body>
<header class="topbar">
    <button class="hamburger" onclick="document.querySelector('.sidebar').classList.toggle('open')">☰</button>
    <h1>{TITLE}</h1>
    <span class="subtitle">{SUBTITLE}</span>
</header>
<div class="layout">
    <nav class="sidebar" id="sidebar">
        <h2>目录 Contents</h2>
        {toc_html}
    </nav>
    <main class="content mathjax-process">
        {html_body}
    </main>
</div>
<script>
document.addEventListener('scroll', () => {{
    const headings = document.querySelectorAll('.content h1[id], .content h2[id], .content h3[id]');
    const links = document.querySelectorAll('.sidebar a');
    let current = '';
    headings.forEach(h => {{
        if (window.scrollY >= h.offsetTop - 80) current = h.id;
    }});
    links.forEach(a => {{
        a.classList.toggle('active', a.getAttribute('href') === '#' + current);
    }});
}});
document.querySelectorAll('.sidebar a').forEach(a => {{
    a.addEventListener('click', () => {{
        document.querySelector('.sidebar').classList.remove('open');
    }});
}});
</script>
</body>
</html>"""

    Path(OUTPUT_FILE).write_text(full_html, encoding="utf-8")
    print(f"已生成 {OUTPUT_FILE}")
    print(f"   提取到 {len(details_blocks)} 个折叠栏")
    print(f"   源文件大小: {len(md_text)} 字符")
    print(f"   输出文件大小: {len(full_html)} 字符")

if __name__ == "__main__":
    main()
