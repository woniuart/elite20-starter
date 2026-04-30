#!/usr/bin/env python3
"""Markdown 转 HTML 转换器"""

import markdown
from pathlib import Path

def md_to_html(md_file):
    """将 Markdown 文件转换为 HTML"""
    md_path = Path(md_file)
    html_path = md_path.with_suffix('.html')

    with open(md_path, 'r', encoding='utf-8') as f:
        md_content = f.read()

    html_body = markdown.markdown(
        md_content,
        extensions=['tables', 'fenced_code', 'codehilite', 'toc']
    )

    html_doc = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{md_path.stem}</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;700&display=swap');

        body {{
            font-family: 'Noto Sans SC', 'Microsoft YaHei', 'SimHei', Arial, sans-serif;
            font-size: 14px;
            line-height: 1.8;
            max-width: 800px;
            margin: 0 auto;
            padding: 40px 20px;
            color: #333;
            background: #fff;
        }}

        h1 {{
            font-size: 24px;
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 15px;
            margin-top: 30px;
        }}

        h2 {{
            font-size: 18px;
            color: #34495e;
            margin-top: 25px;
            padding-left: 10px;
            border-left: 4px solid #3498db;
        }}

        h3 {{
            font-size: 15px;
            color: #555;
            margin-top: 20px;
        }}

        code {{
            background-color: #f5f5f5;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: Consolas, Monaco, 'Courier New', monospace;
            font-size: 13px;
            color: #e74c3c;
        }}

        pre {{
            background-color: #f8f8f8;
            padding: 15px;
            border-radius: 5px;
            border-left: 4px solid #3498db;
            overflow-x: auto;
        }}

        pre code {{
            background: none;
            padding: 0;
            color: #333;
        }}

        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 15px 0;
        }}

        th, td {{
            border: 1px solid #ddd;
            padding: 10px 12px;
            text-align: left;
        }}

        th {{
            background-color: #3498db;
            color: white;
            font-weight: bold;
        }}

        tr:nth-child(even) {{
            background-color: #f9f9f9;
        }}

        blockquote {{
            border-left: 4px solid #3498db;
            margin: 15px 0;
            padding: 10px 20px;
            background-color: #f9f9f9;
            font-style: italic;
            color: #555;
        }}

        ul, ol {{
            margin: 10px 0;
            padding-left: 25px;
        }}

        li {{
            margin: 5px 0;
        }}

        hr {{
            border: none;
            border-top: 1px solid #ddd;
            margin: 25px 0;
        }}

        strong {{
            color: #2c3e50;
        }}

        /* 打印样式 */
        @media print {{
            body {{
                padding: 0;
                font-size: 12px;
            }}

            h1 {{
                font-size: 20px;
                page-break-after: avoid;
            }}

            h2 {{
                font-size: 16px;
                page-break-after: avoid;
            }}

            pre, blockquote {{
                page-break-inside: avoid;
            }}

            table {{
                page-break-inside: avoid;
            }}

            @page {{
                margin: 2cm;
            }}
        }}
    </style>
</head>
<body>
{html_body}
</body>
</html>"""

    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_doc)

    print(f"HTML: {html_path}")
    return html_path

if __name__ == "__main__":
    import sys
    md_file = sys.argv[1] if len(sys.argv) > 1 else "AI-X-Study/Daily/D02/今日学习.md"
    md_to_html(md_file)
