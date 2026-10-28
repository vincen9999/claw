# -*- coding: utf-8 -*-
"""生成《TSG T7001-2023 附件A 检验项目表（抽取）》Word（高清影印，聚焦 6 张检验项目表）。"""
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


def h(text, size=15, center=True):
    p = doc.add_paragraph()
    if center:
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(6)
    r = p.add_run(text)
    r.font.name = CN
    r.font.size = Pt(size)
    r.font.bold = True
    r._element.rPr.rFonts.set(qn('w:eastAsia'), CN)


def note(text, size=9):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(3)
    r = p.add_run(text)
    r.font.name = CN
    r.font.size = Pt(size)
    r._element.rPr.rFonts.set(qn('w:eastAsia'), CN)


def img(path, first=False, width=17.6):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    if not first:
        p.paragraph_format.page_break_before = True
    r = p.add_run()
    r.add_picture(path, width=Cm(width))


# 封面/说明
h('附件 A 检验项目表（抽取）', size=18)
note('TSG T7001—2023《电梯监督检验和定期检验规则》')
note('本册抽取附件 A 中的 6 张检验项目表（按官方原件高清整理）：')
note('表A1-6、表A1-7（乘客与载货电梯）；表A2-3、表A2-4（自动扶梯与自动人行道）；表A3-1、表A3-2（杂物电梯）。')
note('说明：“√”表示适用该项目，“—”表示不适用；带“*”的项目为定期检验关键检验项目。')
note('机型代号：TD 曳引驱动乘客与载货电梯、PD 强制驱动载货电梯、HD 液压乘客与载货电梯、TF 曳引驱动消防员电梯、')
note('HF 液压消防员电梯、TE 曳引驱动防爆电梯、HE 液压防爆电梯、TI 曳引驱动斜行乘客与载货电梯、PI 强制驱动斜行载货电梯。')

# 一、A1
h('一、A1 乘客与载货电梯的检验项目表', size=15)
h('表 A1-6 各类乘客与载货电梯的监督检验项目（注 A1-26）', size=12)
img('D:/Claw/t7001_hd/h040.png', first=False)
for pno in (41, 42, 43, 44):
    img(f'D:/Claw/t7001_hd/h{pno:03d}.png')
h('表 A1-7 各类乘客与载货电梯的定期检验项目（注 A1-27）', size=12)
for pno in (44, 45, 46):
    img(f'D:/Claw/t7001_hd/h{pno:03d}.png')

# 二、A2
h('二、A2 自动扶梯与自动人行道的检验项目表', size=15)
h('表 A2-3 自动扶梯与自动人行道的监督检验项目；表 A2-4 定期检验项目（注 A2-6）', size=12)
for pno in (56, 57, 58):
    img(f'D:/Claw/t7001_hd/h{pno:03d}.png')

# 三、A3
h('三、A3 杂物电梯的检验项目表', size=15)
h('表 A3-1 各类杂物电梯的监督检验项目；表 A3-2 定期检验项目（注 A3-5）', size=12)
for pno in (69, 70):
    img(f'D:/Claw/t7001_hd/h{pno:03d}.png')

out = r'D:\Claw\TSG_T7001-2023_附件A_检验项目表.docx'
doc.save(out)
print('SAVED', out)
