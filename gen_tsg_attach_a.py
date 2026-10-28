# -*- coding: utf-8 -*-
"""将 TSG T7001-2023 附件A（规范第7~68页，PDF第10~71页）逐页整理为 Word（影印版，完整）。"""
from docx import Document
from docx.shared import Cm, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn

CN = '宋体'
doc = Document()
sec = doc.sections[0]
sec.page_width, sec.page_height = Cm(21), Cm(29.7)
sec.left_margin = sec.right_margin = Cm(1.6)
sec.top_margin = Cm(1.4)
sec.bottom_margin = Cm(1.2)

st = doc.styles['Normal']
st.font.name = CN
st.font.size = Pt(10.5)
st._element.rPr.rFonts.set(qn('w:eastAsia'), CN)


def add_title(text, size=16):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(4)
    r = p.add_run(text)
    r.font.name = CN
    r.font.size = Pt(size)
    r.font.bold = True
    r._element.rPr.rFonts.set(qn('w:eastAsia'), CN)


def add_note(text, size=9):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(2)
    r = p.add_run(text)
    r.font.name = CN
    r.font.size = Pt(size)
    r._element.rPr.rFonts.set(qn('w:eastAsia'), CN)


# 首页说明
add_title('附件 A', size=14)
add_title('电梯检验内容、要求和方法', size=18)
add_note('（TSG T7001—2023《电梯监督检验和定期检验规则》附件 A）')
add_note('说明：本节按国家市场监督管理总局发布原件逐页整理，共 62 页（规范第 7～68 页）。')
add_note('包含 A1 乘客与载货电梯、A2 自动扶梯与自动人行道、A3 杂物电梯 三部分。')

# 逐页插入（PDF 第10~71页），每页独立成页
for i in range(10, 72):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.page_break_before = True
    r = p.add_run()
    r.add_picture(f'D:/Claw/t7001_pages/p{i:03d}.png', width=Cm(17.6))

out = r'D:\Claw\TSG_T7001-2023_附件A_全文.docx'
doc.save(out)
print('SAVED', out)
