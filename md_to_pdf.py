#!/usr/bin/env python3
"""Markdown 转 PDF 转换器 (使用 fpdf2)"""

import re
from pathlib import Path
from fpdf import FPDF

def parse_markdown_to_lines(md_content):
    """解析 Markdown 内容为结构化行"""
    lines = []
    in_code_block = False
    in_table = False
    table_data = []

    for line in md_content.split('\n'):
        # 代码块
        if line.strip().startswith('```'):
            in_code_block = not in_code_block
            lines.append(('code_block_end' if not in_code_block else 'code_block_start', ''))
            continue

        if in_code_block:
            lines.append(('code', line))
            continue

        # 标题
        if line.startswith('# '):
            lines.append(('h1', line[2:].strip()))
        elif line.startswith('## '):
            lines.append(('h2', line[3:].strip()))
        elif line.startswith('### '):
            lines.append(('h3', line[4:].strip()))

        # 水平线
        elif line.strip() in ['---', '***', '___']:
            lines.append(('hr', ''))

        # 表格
        elif '|' in line and line.strip().startswith('|'):
            if line.strip().replace('|', '').replace('-', '').replace(':', '').strip() == '':
                # 分隔行
                in_table = True
                continue
            else:
                # 表格数据行
                cells = [c.strip() for c in line.strip().strip('|').split('|')]
                table_data.append(cells)
                continue
        elif in_table and (not line.strip() or '|' not in line):
            # 表格结束
            in_table = False
            lines.append(('table', table_data))
            table_data = []

        # 无序列表
        elif line.strip().startswith('- '):
            lines.append(('ul', line.strip()[2:]))

        # 有序列表
        elif re.match(r'^\d+\. ', line.strip()):
            lines.append(('ol', re.sub(r'^\d+\. ', '', line.strip())))

        # 引用
        elif line.strip().startswith('>'):
            lines.append(('quote', line.strip()[1:].strip()))

        # 普通文本
        elif line.strip():
            lines.append(('text', line.strip()))
        else:
            lines.append(('empty', ''))

    # 处理最后一个表格
    if table_data:
        lines.append(('table', table_data))

    return lines

def md_to_pdf(md_file, output_pdf=None):
    """将 Markdown 文件转换为 PDF"""
    md_path = Path(md_file)
    pdf_path = Path(output_pdf) if output_pdf else md_path.with_suffix('.pdf')

    # 读取 Markdown 内容
    with open(md_path, 'r', encoding='utf-8') as f:
        md_content = f.read()

    # 创建 PDF
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # 添加中文字体 (微软雅黑)
    font_path = "C:/Windows/Fonts/msyh.ttc"
    pdf.add_font('YaHei', '', font_path, uni=True)
    pdf.add_font('YaHei', 'B', font_path, uni=True)

    # 解析并添加内容
    lines = parse_markdown_to_lines(md_content)

    for item_type, content in lines:
        if item_type == 'h1':
            pdf.set_font('YaHei', 'B', 18)
            pdf.set_text_color(44, 62, 80)
            pdf.ln(8)
            pdf.multi_cell(0, 10, content)
            pdf.ln(5)

        elif item_type == 'h2':
            pdf.set_font('YaHei', 'B', 14)
            pdf.set_text_color(52, 73, 94)
            pdf.ln(5)
            pdf.multi_cell(0, 8, content)
            pdf.ln(3)

        elif item_type == 'h3':
            pdf.set_font('YaHei', 'B', 12)
            pdf.set_text_color(85, 85, 85)
            pdf.multi_cell(0, 7, content)
            pdf.ln(2)

        elif item_type == 'hr':
            pdf.ln(3)
            pdf.line(10, pdf.get_y(), 200, pdf.get_y())
            pdf.ln(3)

        elif item_type == 'text':
            pdf.set_font('YaHei', '', 11)
            pdf.set_text_color(51, 51, 51)
            # 处理行内代码
            if '`' in content:
                parts = re.split(r'`([^`]+)`', content)
                for i, part in enumerate(parts):
                    if i % 2 == 1:  # 代码部分
                        pdf.set_font('Courier', '', 10)
                        pdf.set_fill_color(245, 245, 245)
                        pdf.cell(pdf.get_string_width(part) + 4, 6, part, fill=True)
                    else:
                        pdf.set_font('YaHei', '', 11)
                        pdf.write(6, part)
                pdf.ln()
            else:
                pdf.multi_cell(0, 6, content)
            pdf.ln(2)

        elif item_type == 'code':
            pdf.set_font('Courier', '', 9)
            pdf.set_fill_color(248, 248, 248)
            pdf.set_text_color(40, 40, 40)
            pdf.set_x(15)
            pdf.multi_cell(0, 5, content, fill=True)
            pdf.ln(2)

        elif item_type == 'quote':
            pdf.set_font('YaHei', 'I', 11)
            pdf.set_text_color(100, 100, 100)
            pdf.set_x(15)
            pdf.multi_cell(0, 6, content)
            pdf.ln(2)

        elif item_type == 'ul':
            pdf.set_font('YaHei', '', 11)
            pdf.set_text_color(51, 51, 51)
            pdf.set_x(15)
            pdf.write(6, '- ')
            pdf.multi_cell(0, 6, content)
            pdf.ln(1)

        elif item_type == 'ol':
            pdf.set_font('YaHei', '', 11)
            pdf.set_text_color(51, 51, 51)
            pdf.set_x(15)
            pdf.multi_cell(0, 6, content)
            pdf.ln(1)

        elif item_type == 'table':
            if content:
                col_widths = []
                for row in content:
                    col_widths.append(190 / len(row))

                pdf.set_font('YaHei', 'B', 10)
                pdf.set_fill_color(52, 152, 219)
                pdf.set_text_color(255, 255, 255)
                for i, cell in enumerate(content[0]):
                    x = pdf.get_x()
                    pdf.cell(col_widths[i], 8, str(cell)[:30], border=1, fill=True)
                pdf.ln()

                pdf.set_font('YaHei', '', 10)
                fill = False
                for row in content[1:]:
                    pdf.set_fill_color(249, 249, 249 if fill else 255)
                    pdf.set_text_color(51, 51, 51)
                    for i, cell in enumerate(row):
                        pdf.cell(col_widths[i], 7, str(cell)[:30], border=1, fill=True)
                    pdf.ln()
                    fill = not fill
                pdf.ln(5)

        elif item_type == 'empty':
            pdf.ln(2)

    # 保存 PDF
    pdf.output(str(pdf_path))
    print(f"PDF: {pdf_path}")
    return pdf_path

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        md_file = sys.argv[1]
    else:
        md_file = "AI-X-Study/Daily/D02/今日学习.md"

    md_to_pdf(md_file)
