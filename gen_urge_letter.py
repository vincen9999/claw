# -*- coding: utf-8 -*-
"""生成《关于催促提交绿化竣工资料及完成绿化移交查验工作的函》"""
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
CN = "宋体"
CN_B = "微软雅黑"
CN_H = "黑体"

def east(run, name=CN):
    run.font.name = name
    r = run._element
    rPr = r.get_or_add_rPr()
    rFonts = rPr.find(qn('w:rFonts'))
    if rFonts is None:
        rFonts = OxmlElement('w:rFonts'); rPr.append(rFonts)
    rFonts.set(qn('w:ascii'), name); rFonts.set(qn('w:hAnsi'), name); rFonts.set(qn('w:eastAsia'), name)

doc = Document()
for s in doc.sections:
    s.top_margin = Cm(2.5); s.bottom_margin = Cm(2.5)
    s.left_margin = Cm(3.0); s.right_margin = Cm(3.0)

def para(text, size=11, bold=False, align='left', font=CN, space_before=0, space_after=6, indent=None, line=1.5):
    p = doc.add_paragraph()
    p.alignment = {'left': WD_ALIGN_PARAGRAPH.LEFT, 'center': WD_ALIGN_PARAGRAPH.CENTER,
                   'right': WD_ALIGN_PARAGRAPH.RIGHT, 'justify': WD_ALIGN_PARAGRAPH.JUSTIFY}[align]
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = line
    if indent is not None:
        p.paragraph_format.first_line_indent = indent
    r = p.add_run(text)
    r.font.size = Pt(size); r.bold = bold; east(r, font)
    return p

# 文号（占位，可改）
para('聚悦蓝创函〔2026〕   号', size=11, align='right', font=CN, space_after=10)

# 标题
para('关于催促提交绿化竣工资料及完成\n绿化移交查验工作的函', size=16, bold=True,
     align='center', font=CN_B, space_after=16, line=1.3)

# 主送机关
para('上海颍林景观工程有限公司：', size=11, bold=True, font=CN_H, space_after=10)

# 正文
indent = Cm(0.74)  # 首行缩进2字符
para('蓝创中心绿化施工质保期将于2026年12月19日到期。根据2026年8月27日专题会要求，'
     '以及《蓝创中心（C10-05项目）景观绿化移交工作计划》确定的进度安排，贵司本应于2026年10月底前'
     '完成绿化竣工资料的提交，并配合实施绿化移交查验工作。',
     size=11, align='justify', indent=indent, space_after=8, line=1.6)

para('截至本函发出之日，贵司尚未按上述要求提供绿化竣工资料，导致原定于2026年10月底前完成的'
     '绿化移交查验工作拖延至今未能实施，已严重影响蓝创中心绿化移交的整体进度。',
     size=11, align='justify', indent=indent, space_after=8, line=1.6)

para('为确保蓝创中心绿化移交工作顺利推进，现正式函告并要求：请贵司务必于本周内'
     '（即2026年11月13日前）完成绿化竣工资料的整理、编制与移交，并积极配合我中心开展绿化移交查验工作。',
     size=11, align='justify', indent=indent, space_after=8, line=1.6)

para('如贵司未能在上述期限内完成绿化竣工资料移交，由此导致的绿化移交延误、质保期衔接及其他一切后果，'
     '均由贵司自行承担。',
     size=11, align='justify', indent=indent, space_after=10, line=1.6)

# 结语
para('特此函告。', size=11, align='left', indent=indent, space_after=18, line=1.6)

# 落款（右对齐）
para('上海聚悦资产管理有限公司', size=11, align='right', font=CN, space_after=0, line=1.4)
para('蓝创服务中心', size=11, align='right', font=CN, space_after=0, line=1.4)
para('2026年11月9日', size=11, align='right', font=CN, space_before=6, space_after=14, line=1.4)

# 抄送
para('抄送：上海临港奉贤经济发展有限公司', size=11, align='left', font=CN, space_after=0, line=1.4)

out = r'D:\Claw\关于催促提交绿化竣工资料及完成绿化移交查验工作的函.docx'
doc.save(out)
print('saved:', out)
