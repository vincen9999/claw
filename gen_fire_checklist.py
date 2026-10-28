# -*- coding: utf-8 -*-
import re, html, docx
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

raw = open('wx_article3.html', encoding='utf-8', errors='ignore').read()
i = raw.find('id="js_content"')
seg = raw[i:i+2000000]
for marker in ['id="js_sg_bar"','id="js_pc_qr_code"','wx_collapse_area']:
    e = seg.find(marker)
    if e != -1:
        seg = seg[:e]; break
seg = re.sub(r'<script[\s\S]*?</script>', ' ', seg)
seg = re.sub(r'<style[\s\S]*?</style>', ' ', seg)
seg = re.sub(r'<(p|div|br|h[1-6]|tr|li|section)[^>]*>', '\n', seg, flags=re.I)
seg = re.sub(r'</(p|div|tr|li|section)[^>]*>', '\n', seg, flags=re.I)
seg = re.sub(r'<[^>]+>', '', seg)
seg = html.unescape(seg)
lines = [l.strip() for l in seg.split('\n')]
lines = [l for l in lines if l and 'id="js_content"' not in l]

# 去掉尾部编辑/预览噪音
cut = len(lines)
for k, l in enumerate(lines):
    if l.startswith('来源：') or l.startswith('-END-'):
        pass
    if l in ('预览时标签不可点','不喜欢'):
        cut = k; break
lines = lines[:cut]

doc = docx.Document()
# 默认字体
style = doc.styles['Normal']
style.font.name = 'Microsoft YaHei'
style.element.rPr.rFonts.set(__import__('docx').oxml.ns.qn('w:eastAsia'), 'Microsoft YaHei')
style.font.size = Pt(11)

# 主标题
title = doc.add_heading('《重点场所消防安全检查要点清单》', level=0)
for r in title.runs:
    r.font.name = 'Microsoft YaHei'

def add_part_heading(t):
    h = doc.add_heading(t, level=1)
    for r in h.runs:
        r.font.name = 'Microsoft YaHei'

def add_section(t):
    h = doc.add_heading(t, level=2)
    for r in h.runs:
        r.font.name = 'Microsoft YaHei'

def add_item(t):
    p = doc.add_paragraph(t)
    for r in p.runs:
        r.font.name = 'Microsoft YaHei'
    return p

SECTION_TITLES = {'九小场所的检查要点','消防安全十一查','天然气安全二十一查',
                  '液化气安全九查','电力安全十一查','21类重点场所消防安全风险自查检查指南'}

# 拆分 PART.1 / PART.2
text = '\n'.join(lines)
part1 = part2 = ''
if 'PART.2' in text:
    p1, p2 = text.split('PART.2', 1)
    part1, part2 = p1, 'PART.2'+p2
else:
    part1 = text

# ---- PART.1 ----
add_part_heading('PART.1  九小场所的检查要点')
cur = None
for l in part1.replace('PART.1','').split('\n'):
    l = l.strip()
    if not l:
        continue
    if l in SECTION_TITLES:
        # 跳过“九小场所的检查要点”已是 PART 标题下的引导语，作为小标题
        if l == '九小场所的检查要点':
            add_section(l)
        else:
            add_section(l)
        cur = l
    elif l.startswith('◆'):
        add_item(l)
    else:
        # 兜底：非◆非标题行，当作普通段落
        add_item(l)

# ---- PART.2 ----
add_part_heading('PART.2  21类重点场所消防安全风险自查检查指南')
# 解析带编号的清单：单独数字行 + 后续名称行
p2lines = [l.strip() for l in part2.replace('PART.2','').split('\n') if l.strip()]
idx = 0
n = len(p2lines)
buf = []
while idx < n:
    l = p2lines[idx]
    if re.fullmatch(r'\d{1,2}', l) and idx+1 < n:
        num = int(l)
        name = p2lines[idx+1]
        add_item(f"{num}. {name}")
        idx += 2
    else:
        idx += 1

# 来源
src = [l for l in lines if l.startswith('来源：')]
if src:
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    run = p.add_run(src[0])
    run.font.size = Pt(9); run.font.color.rgb = RGBColor(0x80,0x80,0x80)

out = '重点场所消防安全检查要点清单.docx'
doc.save(out)
print('SAVED:', out)
print('lines used:', len(lines))
