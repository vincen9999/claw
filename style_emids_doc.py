# -*- coding: utf-8 -*-
"""Post-process: apply run-level heading/caption formatting (template has only Normal style)."""
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt, RGBColor
from docx.oxml.ns import qn
import re

CAP_RE = re.compile(r"^图\s*[\d一二三四五六七八九十]+\s*[-－]?\s*[\d一二三四五六七八九十]*")

P = r"C:\Users\User\Desktop\多媒体调试要点（图示增强版）.docx"
d = Document(P)

C_TITLE = RGBColor(0x1F, 0x38, 0x64)   # 深蓝
C_H1    = RGBColor(0x2E, 0x54, 0x96)   # 蓝
C_H2    = RGBColor(0x00, 0x00, 0x00)   # 黑
C_CAP   = RGBColor(0x59, 0x59, 0x59)   # 灰

def fmt(p, size, bold=False, italic=False, color=None, align=None, before=0, after=2):
    if align is not None:
        p.alignment = align
    pf = p.paragraph_format
    if before: pf.space_before = Pt(before)
    pf.space_after = Pt(after)
    # 中文 + 西文字体
    for r in p.runs:
        r.font.size = Pt(size)
        r.font.bold = bold
        r.font.italic = italic
        if color is not None:
            r.font.color.rgb = color
        r.font.name = "Microsoft YaHei"
        rPr = r._element.get_or_add_rPr()
        rFonts = rPr.find(qn('w:rFonts'))
        if rFonts is None:
            rFonts = rPr.makeelement(qn('w:rFonts'), {})
            rPr.append(rFonts)
        rFonts.set(qn('w:eastAsia'), "Microsoft YaHei")

for p in d.paragraphs:
    t = p.text.strip()
    if not t:
        continue
    if t.startswith("电梯多媒体（EMIDS）调试要点"):
        fmt(p, 18, bold=True, color=C_TITLE, align=WD_ALIGN_PARAGRAPH.CENTER, before=0, after=6)
        continue
    if any(t.startswith(x) for x in ["一、", "二、", "三、", "四、", "五、", "六、"]):
        fmt(p, 15, bold=True, color=C_H1, before=8, after=3)
        continue
    if t.startswith("步骤 ") or t.startswith(("3.1", "3.2", "3.3")) or t.startswith("补充"):
        fmt(p, 12.5, bold=True, color=C_H2, before=6, after=2)
        continue
    if CAP_RE.match(t):
        fmt(p, 9, italic=True, color=C_CAP, align=WD_ALIGN_PARAGRAPH.CENTER, before=1, after=6)
        continue
    if t.startswith("要点：") or t.startswith("**要点"):
        fmt(p, 10.5, italic=True, color=C_CAP, before=0, after=2)
        continue

d.save(P)
print("styled & saved:", P)

# 复核
d2 = Document(P)
from collections import Counter
sizes = Counter()
for p in d2.paragraphs:
    if p.runs:
        sizes[p.runs[0].font.size] += 1
print("run sizes distribution:", dict(sizes))
print("total paragraphs:", len(d2.paragraphs))
