# -*- coding: utf-8 -*-
"""生成 TSG T7001-2023《电梯监督检验和定期检验规则》附件 B/C/D 报告格式模板 Word。"""
from docx import Document
from docx.shared import Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn

CN = '宋体'
doc = Document()

# 页面设置 A4
sec = doc.sections[0]
sec.page_width, sec.page_height = Cm(21), Cm(29.7)
sec.left_margin = sec.right_margin = Cm(2.2)
sec.top_margin = Cm(2.2)
sec.bottom_margin = Cm(2.0)

# 默认字体
st = doc.styles['Normal']
st.font.name = CN
st.font.size = Pt(10.5)
st._element.rPr.rFonts.set(qn('w:eastAsia'), CN)


def set_run(run, size=10.5, bold=False, name=CN):
    run.font.name = name
    run.font.size = Pt(size)
    run.font.bold = bold
    run._element.rPr.rFonts.set(qn('w:eastAsia'), name)


def para(text='', size=10.5, bold=False, align='left', space_after=4, indent_first=True):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.space_before = Pt(0)
    if indent_first:
        p.paragraph_format.first_line_indent = Pt(size * 2)
    if align == 'center':
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    elif align == 'right':
        p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r = p.add_run(text)
    set_run(r, size=size, bold=bold)
    return p


def title(text, size=16, bold=True, space_after=10):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.space_before = Pt(6)
    r = p.add_run(text)
    set_run(r, size=size, bold=bold)
    return p


def cell_text(cell, text, bold=False, size=10.5, align='left'):
    cell.text = ''
    p = cell.paragraphs[0]
    if align == 'center':
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    elif align == 'right':
        p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    for i, line in enumerate(str(text).split('\n')):
        if i > 0:
            p = cell.add_paragraph()
            if align == 'center':
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(line)
        set_run(r, size=size, bold=bold)


def mk_table(rows, cols, widths=None):
    t = doc.add_table(rows=rows, cols=cols)
    t.style = 'Table Grid'
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    if widths:
        for row in t.rows:
            for i, w in enumerate(widths):
                row.cells[i].width = Cm(w)
    return t


# ============================================================
# 附件 B  电梯检验意见通知书
# ============================================================
para('附件 B', size=12, bold=True, indent_first=False, space_after=2)
title('电梯检验意见通知书', size=16)
para('编号：', align='right', indent_first=False, space_after=2)

t = mk_table(12, 4, widths=[4.2, 4.0, 3.6, 4.8])
cell_text(t.cell(0, 0), '受检单位名称', bold=True, align='center')
cell_text(t.cell(0, 1), '', align='center')
t.cell(0, 1).merge(t.cell(0, 3))
cell_text(t.cell(1, 0), '安装地点', bold=True, align='center')
cell_text(t.cell(1, 1), '', align='center')
cell_text(t.cell(1, 2), '设备品种', bold=True, align='center')
cell_text(t.cell(1, 3), '', align='center')
cell_text(t.cell(2, 0), '唯一性编号', bold=True, align='center')
cell_text(t.cell(2, 1), '', align='center')
t.cell(2, 1).merge(t.cell(2, 3))
cell_text(t.cell(3, 0), '检验依据', bold=True, align='center')
cell_text(t.cell(3, 1), '《电梯监督检验和定期检验规则》(TSG T7001—2023)', align='center')
t.cell(3, 1).merge(t.cell(3, 3))
cell_text(t.cell(4, 0), '不符合情况：', bold=True)
t.cell(4, 0).merge(t.cell(4, 3))
t.rows[4].height = Cm(3.2)
cell_text(t.cell(5, 0), '检验意见：', bold=True)
t.cell(5, 0).merge(t.cell(5, 3))
t.rows[5].height = Cm(3.6)
cell_text(t.cell(6, 0), '检验人员：', bold=True)
cell_text(t.cell(6, 1), '')
cell_text(t.cell(6, 2), '检验日期：', bold=True)
cell_text(t.cell(6, 3), '    年    月    日')
cell_text(t.cell(7, 0), '检验机构名称：', bold=True)
cell_text(t.cell(7, 1), '')
cell_text(t.cell(7, 2), '核准证号：', bold=True)
cell_text(t.cell(7, 3), '')
cell_text(t.cell(8, 0), '受检单位代表：', bold=True)
cell_text(t.cell(8, 1), '')
cell_text(t.cell(8, 2), '签收日期：', bold=True)
cell_text(t.cell(8, 3), '    年    月    日')
cell_text(t.cell(9, 0), '处理结果：', bold=True)
t.cell(9, 0).merge(t.cell(9, 3))
t.rows[9].height = Cm(2.4)
cell_text(t.cell(10, 0), '施工/使用单位负责人：', bold=True)
cell_text(t.cell(10, 1), '')
cell_text(t.cell(10, 2), '日期：', bold=True)
cell_text(t.cell(10, 3), '    年    月    日')
cell_text(t.cell(11, 0), '（施工/使用单位公章）', align='right')
t.cell(11, 0).merge(t.cell(11, 3))

para('（提示：根据《中华人民共和国特种设备安全法》的规定，未经监督检验或者监督检验不合格的电梯，不得交付使用；'
     '未经定期检验或者检验不合格的电梯，不得继续使用。）', size=9, indent_first=True, space_after=4)
para('注：(1) 本通知书一式三份。一份检验机构存档，两份送受检单位，其中一份受检单位应当按照相应要求返回检验机构；',
     size=9, indent_first=False, space_after=0)
para('　　(2) 受检单位代表拒绝签字时，本通知书仍有效；', size=9, indent_first=False, space_after=0)
para('　　(3) 最终检验结论以检验报告为准；', size=9, indent_first=False, space_after=0)
para('　　(4) 纸面不敷，可另增页。', size=9, indent_first=False, space_after=0)

# 附件 B 填写说明
doc.add_page_break()
title('填写说明', size=15)
para('1. “受检单位名称”栏，对于监督检验，填写施工单位名称；对于定期检验，填写使用单位名称。受检单位为个人的，填写与含个人身份号码的证明文件一致的姓名。')
para('2. “唯一性编号”栏，填写受检电梯的产品编号或者使用登记证编号等。')
para('3. “不符合情况”栏，填写经检验发现的不符合具体情况。')
para('4. “检验意见”栏，按照以下要求填写：')
para('(1) 经监督检验，该电梯存在不符合的，填写“该电梯存在不符合（见上栏），请将处理结果及时报送我机构”；', indent_first=False)
para('(2) 经定期检验，该电梯存在不符合，并且检验人员按照本规则 4.7 条初步判定为不合格的，填写“检验结论为不合格”；否则，填写“该电梯存在不符合（见上栏），请在　　年　　月　　日前将处理结果报送我机构”；', indent_first=False)
para('(3) 存在本规则 2.6 条所述情形，填写“因　　　　　　　　　　　　　　　　　　　　　，中止检验”；', indent_first=False)
para('(4) 填写其他需要说明的事项。', indent_first=False)

# ============================================================
# 附件 C  电梯监督检验报告
# ============================================================
doc.add_page_break()
para('附件 C', size=12, bold=True, indent_first=False, space_after=2)
para('报告编号：', align='right', indent_first=False, space_after=2)
for _ in range(3):
    para('', space_after=0, indent_first=False)
title('电梯监督检验报告', size=22, space_after=20)
for _ in range(2):
    para('', space_after=0, indent_first=False)
for label in ['使用单位名称：', '施工单位名称：', '设 备 代 码：', '设 备 类 别：', '施 工 类 别：', '检 验 日 期：']:
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(10)
    r = p.add_run(label + ' ' + '_' * 22)
    set_run(r, size=12)
para('', space_after=0, indent_first=False)
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run('（印制检验机构名称）')
set_run(r, size=11)

# 附件 C 注意事项
doc.add_page_break()
title('注意事项', size=15)
para('1. 有下列情况之一的，本检验报告无效：', indent_first=False)
para('(1) 无检验、审核、批准人员签字；', indent_first=False)
para('(2) 无检验机构的核准证号；', indent_first=False)
para('(3) 无检验机构的公章或者检验专用章。', indent_first=False)
para('2. 本检验报告一式三份，由检验机构、施工单位和使用单位分别保存。')
para('3. 对本检验报告结论如有异议，请在取得本报告后 15 日内，向检验机构提出书面意见。')
para('', space_after=0)
para('', space_after=0)
para('检验机构地址：', indent_first=False)
para('联系电话：', indent_first=False)

# 附件 C 报告正文表
doc.add_page_break()
title('电梯监督检验报告', size=15)
para('报告编号：', align='right', indent_first=False, space_after=2)
t = mk_table(18, 4, widths=[3.6, 4.6, 3.6, 4.8])
cell_text(t.cell(0, 0), '使用单位名称', bold=True, align='center')
cell_text(t.cell(0, 2), '统一社会信用代码', bold=True, align='center')
cell_text(t.cell(1, 0), '安装地点', bold=True, align='center')
t.cell(1, 1).merge(t.cell(1, 3))
cell_text(t.cell(2, 0), '设备品种', bold=True, align='center')
cell_text(t.cell(2, 2), '产品型号', bold=True, align='center')
cell_text(t.cell(3, 0), '产品编号', bold=True, align='center')
cell_text(t.cell(3, 2), '制造日期', bold=True, align='center')
cell_text(t.cell(4, 0), '设备代码', bold=True, align='center')
cell_text(t.cell(4, 2), '施工类别', bold=True, align='center')
cell_text(t.cell(5, 0), '使用登记证编号', bold=True, align='center')
cell_text(t.cell(5, 2), '单位内编号', bold=True, align='center')
cell_text(t.cell(6, 0), '施工单位名称', bold=True, align='center')
t.cell(6, 1).merge(t.cell(6, 3))
cell_text(t.cell(7, 0), '制造单位名称', bold=True, align='center')
t.cell(7, 1).merge(t.cell(7, 3))
cell_text(t.cell(8, 0), '维护保养单位名称', bold=True, align='center')
t.cell(8, 1).merge(t.cell(8, 3))
cell_text(t.cell(9, 0), '设备技术\n参数', bold=True, align='center')
t.cell(9, 1).merge(t.cell(9, 3))
t.rows[9].height = Cm(3.0)
cell_text(t.cell(10, 0), '检验依据', bold=True, align='center')
cell_text(t.cell(10, 1), '《电梯监督检验和定期检验规则》(TSG T7001—2023)', align='center')
t.cell(10, 1).merge(t.cell(10, 3))
cell_text(t.cell(11, 0), '检验结论', bold=True, align='center')
t.cell(11, 1).merge(t.cell(11, 3))
cell_text(t.cell(12, 0), '备注', bold=True, align='center')
t.cell(12, 1).merge(t.cell(12, 3))
t.rows[12].height = Cm(1.6)
cell_text(t.cell(13, 0), '检验：                日期：', bold=True)
t.cell(13, 0).merge(t.cell(13, 2))
cell_text(t.cell(13, 3), '检验机构核准证号：')
cell_text(t.cell(14, 0), '审核：                日期：', bold=True)
t.cell(14, 0).merge(t.cell(14, 2))
cell_text(t.cell(14, 3), '')
cell_text(t.cell(15, 0), '批准：                日期：', bold=True)
t.cell(15, 0).merge(t.cell(15, 2))
cell_text(t.cell(15, 3), '（检验机构公章或者检验专用章）')
cell_text(t.cell(16, 0), '共    页    第    页', align='center')
t.cell(16, 0).merge(t.cell(16, 3))
t.cell(17, 0).merge(t.cell(17, 3))

# 附件 C 附页
doc.add_page_break()
title('电梯监督检验报告附页', size=15)
para('报告编号：', align='right', indent_first=False, space_after=2)
rows = 21
t = mk_table(rows, 8, widths=[1.2, 1.2, 2.6, 1.8, 1.2, 1.2, 2.6, 1.8])
t.cell(0, 0).merge(t.cell(1, 0))
cell_text(t.cell(0, 0), '序号', bold=True, align='center')
t.cell(0, 1).merge(t.cell(0, 2))
cell_text(t.cell(0, 1), '检验项目', bold=True, align='center')
cell_text(t.cell(1, 1), '编号', bold=True, align='center')
cell_text(t.cell(1, 2), '名称', bold=True, align='center')
t.cell(0, 3).merge(t.cell(1, 3))
cell_text(t.cell(0, 3), '检验结果', bold=True, align='center')
t.cell(0, 4).merge(t.cell(1, 4))
cell_text(t.cell(0, 4), '序号', bold=True, align='center')
t.cell(0, 5).merge(t.cell(0, 6))
cell_text(t.cell(0, 5), '检验项目', bold=True, align='center')
cell_text(t.cell(1, 5), '编号', bold=True, align='center')
cell_text(t.cell(1, 6), '名称', bold=True, align='center')
t.cell(0, 7).merge(t.cell(1, 7))
cell_text(t.cell(0, 7), '检验结果', bold=True, align='center')
para('共    页    第    页', align='center', indent_first=False, space_after=0)

# 附件 C 填写说明
doc.add_page_break()
title('填写说明', size=15)
para('1. 使用单位为个人的，“统一社会信用代码”栏填写“—”。')
para('2. “设备技术参数”栏，至少填写以下内容：')
para('(1) 曳引驱动乘客与载货电梯、曳引驱动消防员电梯、强制驱动载货电梯、曳引与强制驱动杂物电梯：额定载重量、额定速度、层站门数、控制方式；斜行电梯还包括：倾斜角、轿门位置；', indent_first=False)
para('(2) 液压乘客与载货电梯、液压驱动消防员电梯、液压杂物电梯：额定载重量、额定速度（含上行速度和下行速度）、层站门数、控制方式、油缸数量、顶升方式；', indent_first=False)
para('(3) 防爆电梯（含防爆杂物电梯）：除 (1) 或者 (2) 所述外，还包括区域防爆等级和整机防爆标志；', indent_first=False)
para('(4) 自动扶梯、自动人行道：名义速度、名义宽度、倾斜角、输送能力、提升高度、使用区段长度。', indent_first=False)
para('3. “检验项目”栏，按照以下要求填写：')
para('(1) 安装监督检验：按照本规则附件 A 表 A1-6、表 A2-3、表 A3-1 填写适用于受检电梯的检验项目编号和名称，例如：编号栏分别填写“A1.1.1”“A2.2.3.1”“A3.2.2.4”，名称栏则分别填写“制造资料”“扶手装置”“防爆电气部件”；', indent_first=False)
para('(2) 改造、重大修理监督检验：按照本规则附件 A 表 A1-6、表 A2-3、表 A3-1 和表 A1-7、表 A2-4、表 A3-2 填写适用于受检电梯的检验项目编号和名称，其中表 A1-7、表 A2-4、表 A3-2 所列检验项目的编号前无需加“*”。', indent_first=False)
para('4. “检验结果”栏，按照以下要求填写：')
para('(1) 经检验符合要求的，填写“符合”；', indent_first=False)
para('(2) 对于不适用的检验项目，填写“无此项”。', indent_first=False)

# ============================================================
# 附件 D  电梯定期检验报告
# ============================================================
doc.add_page_break()
para('附件 D', size=12, bold=True, indent_first=False, space_after=2)
para('报告编号：', align='right', indent_first=False, space_after=2)
for _ in range(3):
    para('', space_after=0, indent_first=False)
title('电梯定期检验报告', size=22, space_after=20)
for _ in range(2):
    para('', space_after=0, indent_first=False)
for label in ['使用单位名称：', '设 备 代 码：', '设 备 类 别：', '检 验 日 期：']:
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(10)
    r = p.add_run(label + ' ' + '_' * 22)
    set_run(r, size=12)
para('', space_after=0, indent_first=False)
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run('（印制检验机构名称）')
set_run(r, size=11)

# 附件 D 注意事项
doc.add_page_break()
title('注意事项', size=15)
para('1. 有下列情况之一的，本检验报告无效：', indent_first=False)
para('(1) 无检验、审核、批准人员签字；', indent_first=False)
para('(2) 无检验机构的核准证号；', indent_first=False)
para('(3) 无检验机构的公章或者检验专用章。', indent_first=False)
para('2. 本检验报告一式两份，由检验机构和使用单位分别保存。')
para('3. 对本检验报告结论如有异议，请在取得本报告后 15 日内，向检验机构提出书面意见。')
para('', space_after=0)
para('检验机构地址：', indent_first=False)
para('联系电话：', indent_first=False)

# 附件 D 报告正文表
doc.add_page_break()
title('电梯定期检验报告', size=15)
para('报告编号：', align='right', indent_first=False, space_after=2)
t = mk_table(18, 4, widths=[3.6, 4.6, 3.6, 4.8])
cell_text(t.cell(0, 0), '使用单位名称', bold=True, align='center')
cell_text(t.cell(0, 2), '统一社会信用代码', bold=True, align='center')
cell_text(t.cell(1, 0), '安装地点', bold=True, align='center')
t.cell(1, 1).merge(t.cell(1, 3))
cell_text(t.cell(2, 0), '设备品种', bold=True, align='center')
cell_text(t.cell(2, 2), '产品型号', bold=True, align='center')
cell_text(t.cell(3, 0), '产品编号', bold=True, align='center')
cell_text(t.cell(3, 2), '单位内编号', bold=True, align='center')
cell_text(t.cell(4, 0), '使用登记证编号', bold=True, align='center')
cell_text(t.cell(4, 2), '安全管理人员', bold=True, align='center')
cell_text(t.cell(5, 0), '制造单位名称', bold=True, align='center')
cell_text(t.cell(5, 2), '制造日期', bold=True, align='center')
cell_text(t.cell(6, 0), '改造单位名称', bold=True, align='center')
cell_text(t.cell(6, 2), '改造日期', bold=True, align='center')
cell_text(t.cell(7, 0), '维护保养单位名称', bold=True, align='center')
t.cell(7, 1).merge(t.cell(7, 3))
cell_text(t.cell(8, 0), '设备技术\n参数', bold=True, align='center')
t.cell(8, 1).merge(t.cell(8, 3))
t.rows[8].height = Cm(3.0)
cell_text(t.cell(9, 0), '检验依据', bold=True, align='center')
cell_text(t.cell(9, 1), '《电梯监督检验和定期检验规则》(TSG T7001—2023)', align='center')
t.cell(9, 1).merge(t.cell(9, 3))
cell_text(t.cell(10, 0), '检验结论', bold=True, align='center')
t.cell(10, 1).merge(t.cell(10, 3))
cell_text(t.cell(11, 0), '备注', bold=True, align='center')
t.cell(11, 1).merge(t.cell(11, 3))
t.rows[11].height = Cm(1.6)
cell_text(t.cell(12, 0), '检验：                日期：', bold=True)
t.cell(12, 0).merge(t.cell(12, 2))
cell_text(t.cell(12, 3), '检验机构核准证号：')
cell_text(t.cell(13, 0), '审核：                日期：', bold=True)
t.cell(13, 0).merge(t.cell(13, 2))
cell_text(t.cell(13, 3), '')
cell_text(t.cell(14, 0), '批准：                日期：', bold=True)
t.cell(14, 0).merge(t.cell(14, 2))
cell_text(t.cell(14, 3), '（检验机构公章或者检验专用章）')
cell_text(t.cell(15, 0), '共    页    第    页', align='center')
t.cell(15, 0).merge(t.cell(15, 3))
t.cell(16, 0).merge(t.cell(16, 3))
t.cell(17, 0).merge(t.cell(17, 3))

# 附件 D 附页
doc.add_page_break()
title('电梯定期检验报告附页', size=15)
para('报告编号：', align='right', indent_first=False, space_after=2)
t = mk_table(rows, 8, widths=[1.2, 1.2, 2.6, 1.8, 1.2, 1.2, 2.6, 1.8])
t.cell(0, 0).merge(t.cell(1, 0))
cell_text(t.cell(0, 0), '序号', bold=True, align='center')
t.cell(0, 1).merge(t.cell(0, 2))
cell_text(t.cell(0, 1), '检验项目', bold=True, align='center')
cell_text(t.cell(1, 1), '编号', bold=True, align='center')
cell_text(t.cell(1, 2), '名称', bold=True, align='center')
t.cell(0, 3).merge(t.cell(1, 3))
cell_text(t.cell(0, 3), '检验结果', bold=True, align='center')
t.cell(0, 4).merge(t.cell(1, 4))
cell_text(t.cell(0, 4), '序号', bold=True, align='center')
t.cell(0, 5).merge(t.cell(0, 6))
cell_text(t.cell(0, 5), '检验项目', bold=True, align='center')
cell_text(t.cell(1, 5), '编号', bold=True, align='center')
cell_text(t.cell(1, 6), '名称', bold=True, align='center')
t.cell(0, 7).merge(t.cell(1, 7))
cell_text(t.cell(0, 7), '检验结果', bold=True, align='center')
para('共    页    第    页', align='center', indent_first=False, space_after=0)

# 附件 D 填写说明
doc.add_page_break()
title('填写说明', size=15)
para('1. “统一社会信用代码”“设备技术参数”栏的填写说明见本规则附件 C。')
para('2. 对于本规则 4.7 条第 (2) 项所述的使用单位签署了监护使用意见并且判定为“整改后合格”的情形，应当在“备注”栏填写：“本报告第 XX、XX、XX 项的检验结果为不符合，使用单位已经承诺采取安全措施，对电梯实行监护使用（见编号为 XXXXXX 的《电梯检验意见通知书》）。”；按照本规则 4.8 条规定进行复检的，应当在“备注”栏填写：“本检验机构于 XXXX 年 XX 月 XX 日出具了编号为 XXXXXX 的《电梯定期检验报告》。按照 TSG T7001—2023 的规定，本检验机构对该报告所对应的电梯进行了复检，出具本检验报告。”')
para('3. “检验项目”栏，按照本规则附件 A 表 A1-7、表 A2-4、表 A3-2 填写适用于受检电梯的检验项目编号和名称，例如：编号栏分别填写“A1.2.6.3(3)”“*A2.2.2.5”“A3.1.4”，名称栏则分别填写“轿厢安全窗电气安全装置”“防护挡板”“使用资料”。')
para('4. “检验结果”栏，按照以下要求填写：')
para('(1) 经检验符合要求的，填写“符合”；', indent_first=False)
para('(2) 经检验不符合要求的，填写“不符合”；', indent_first=False)
para('(3) 对于不适用的检验项目，填写“无此项”。', indent_first=False)

# ============================================================
# 相关规章和规范历次制（修）订情况
# ============================================================
doc.add_page_break()
title('相关规章和规范历次制（修）订情况', size=14)
items = [
    '《起重机械安全监察规定》（劳安字〔1991〕8 号），原劳动部，1991 年 3 月 21 日发布，1991 年 10 月 1 日起实施。',
    '《关于进一步加强电梯安全管理工作的通知》（劳部发〔1995〕21 号），原劳动部，1995 年 1 月 11 日发布并实施。',
    '《电梯安全技术检验大纲》（劳部发〔1995〕44 号），原劳动部，1995 年 2 月 17 日发布并实施。',
    '《自动扶梯及自动人行道安全技术检验大纲》（劳部发〔1996〕207 号），原劳动部，1996 年 6 月 17 日发布并实施。',
    '《特种设备质量监督与安全监察规定》（国家质量技术监督局令第 13 号），原国家质量技术监督局，2000 年 6 月 29 日发布，自 2000 年 10 月 1 日起实施。',
    '《电梯监督检验规程》（国质检锅〔2002〕1 号），原国家质量监督检验检疫总局，2002 年 1 月 9 日发布，2002 年 3 月 1 日起施行。',
    '《液压电梯监督检验规程（试行）》（国质检锅〔2002〕358 号），原国家质量监督检验检疫总局，2002 年 12 月 13 日发布，自 2003 年 4 月 1 日起施行。',
    '《自动扶梯和自动人行道监督检验规程》（国质检锅〔2002〕360 号），原国家质量监督检验检疫总局，2002 年 12 月 13 日发布，自 2003 年 2 月 1 日起施行。',
    '《杂物电梯监督检验规程》（国质检锅〔2003〕33 号），原国家质量监督检验检疫总局，2003 年 2 月 9 日发布，自 2003 年 9 月 1 日起施行。',
    '《电梯监督检验和定期检验规则——曳引与强制驱动电梯》（TSG T7001—2009），原国家质量监督检验检疫总局公告（2009 年第 114 号），2009 年 12 月 4 日发布，2010 年 4 月 1 日起实施；第 1 号修改单，原国家质量监督检验检疫总局公告（2013 年第 191 号），2013 年 12 月 31 日发布，2014 年 3 月 1 日起施行；第 2 号修改单，原国家质量监督检验检疫总局公告（2017 年第 44 号），2017 年 6 月 12 日发布，2017 年 10 月 1 日起施行；第 3 号修改单，国家市场监督管理总局公告（2019 年第 51 号），2019 年 10 月 31 日发布，2020 年 1 月 1 日起施行。',
    '《电梯监督检验和定期检验规则——消防员电梯》（TSG T7002—2011），原国家质量监督检验检疫总局公告（2011 年第 117 号），2011 年 8 月 8 日发布，2012 年 2 月 1 日起施行；第 1 号修改单，原国家质量监督检验检疫总局公告（2013 年第 191 号），2013 年 12 月 31 日发布，2014 年 3 月 1 日起施行；第 2 号修改单，原国家质量监督检验检疫总局公告（2017 年第 44 号），2017 年 6 月 12 日发布，2017 年 10 月 1 日起施行；第 3 号修改单，国家市场监督管理总局公告（2019 年第 51 号），2019 年 10 月 31 日发布，2020 年 1 月 1 日起施行。',
    '《电梯监督检验和定期检验规则——防爆电梯》（TSG T7003—2011），原国家质量监督检验检疫总局公告（2011 年第 117 号），2011 年 8 月 8 日发布，2012 年 2 月 1 日起施行；第 1 号修改单，原国家质量监督检验检疫总局公告（2013 年第 191 号），2013 年 12 月 31 日发布，2014 年 3 月 1 日起施行；第 2 号修改单，原国家质量监督检验检疫总局公告（2017 年第 44 号），2017 年 6 月 12 日发布，2017 年 10 月 1 日起施行；第 3 号修改单，国家市场监督管理总局公告（2019 年第 51 号），2019 年 10 月 31 日发布，2020 年 1 月 1 日起施行。',
    '《电梯监督检验和定期检验规则——液压电梯》（TSG T7004—2012），原国家质量监督检验检疫总局公告（2012 年第 47 号），2012 年 3 月 23 日发布，2012 年 7 月 1 日起施行；第 1 号修改单，原国家质量监督检验检疫总局公告（2013 年第 191 号），2013 年 12 月 31 日发布，2014 年 3 月 1 日起施行；第 2 号修改单，原国家质量监督检验检疫总局公告（2017 年第 44 号），2017 年 6 月 12 日发布，2017 年 10 月 1 日起施行；第 3 号修改单，国家市场监督管理总局公告（2019 年第 51 号），2019 年 10 月 31 日发布，2020 年 1 月 1 日起施行。',
    '《电梯监督检验和定期检验规则——自动扶梯与自动人行道》（TSG T7005—2012），原国家质量监督检验检疫总局公告（2012 年第 47 号），2012 年 3 月 23 日发布，2012 年 7 月 1 日起施行；第 1 号修改单，原国家质量监督检验检疫总局公告（2013 年第 191 号），2013 年 12 月 31 日发布，2014 年 3 月 1 日起施行；第 2 号修改单，原国家质量监督检验检疫总局公告（2017 年第 44 号），2017 年 6 月 12 日发布，2017 年 10 月 1 日起施行；第 3 号修改单，国家市场监督管理总局公告（2019 年第 51 号），2019 年 10 月 31 日发布，2020 年 1 月 1 日起施行。',
    '《电梯监督检验和定期检验规则——杂物电梯》（TSG T7006—2012），原国家质量监督检验检疫总局公告（2012 年第 47 号），2012 年 3 月 23 日发布，2012 年 7 月 1 日起施行；第 1 号修改单，原国家质量监督检验检疫总局公告（2013 年第 191 号），2013 年 12 月 31 日发布，2014 年 3 月 1 日起施行；第 2 号修改单，原国家质量监督检验检疫总局公告（2017 年第 44 号），2017 年 6 月 12 日发布，2017 年 10 月 1 日起施行；第 3 号修改单，国家市场监督管理总局公告（2019 年第 51 号），2019 年 10 月 31 日发布，2020 年 1 月 1 日起施行。',
    '《市场监管总局关于进一步做好改进电梯维护保养模式和调整电梯检验检测方式试点工作的意见》（国市监特设〔2020〕56 号），国家市场监督管理总局，2020 年 4 月 6 日发布。',
]
for i, it in enumerate(items, 1):
    para(f'{i}. {it}', size=9.5, indent_first=False, space_after=2)

out = r'D:\Claw\TSG_T7001-2023_附件BCD_报告格式模板.docx'
doc.save(out)
print('SAVED', out)
