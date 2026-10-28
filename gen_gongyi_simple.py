# -*- coding: utf-8 -*-
"""生成《上海市住宅小区公共收益监管账户·简洁易懂版》Word 文档"""
from docx import Document
from docx.shared import Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn

doc = Document()

# 默认字体
style = doc.styles["Normal"]
style.font.name = "微软雅黑"
style.font.size = Pt(10.5)
style._element.rPr.rFonts.set(qn("w:eastAsia"), "微软雅黑")

NAVY = RGBColor(0x1F, 0x3A, 0x5F)
GREEN = RGBColor(0x2E, 0x7D, 0x32)
ORANGE = RGBColor(0xC0, 0x52, 0x00)

def set_cn(run, name="微软雅黑"):
    run.font.name = name
    r = run._element
    r.rPr.rFonts.set(qn("w:eastAsia"), name)

def h1(text):
    p = doc.add_paragraph()
    p.space_before = Pt(10)
    r = p.add_run(text)
    r.bold = True
    r.font.size = Pt(14)
    r.font.color.rgb = NAVY
    set_cn(r)
    return p

def h2(text):
    p = doc.add_paragraph()
    r = p.add_run(text)
    r.bold = True
    r.font.size = Pt(11.5)
    r.font.color.rgb = GREEN
    set_cn(r)
    return p

def body(text, bold=False, color=None, size=10.5):
    p = doc.add_paragraph()
    r = p.add_run(text)
    r.bold = bold
    r.font.size = Pt(size)
    if color is not None:
        r.font.color.rgb = color
    set_cn(r)
    return p

def bullet(text, lead=None):
    p = doc.add_paragraph(style="List Bullet")
    if lead:
        r = p.add_run(lead)
        r.bold = True
        set_cn(r)
    r2 = p.add_run(text)
    set_cn(r2)
    return p

def table(headers, rows, widths=None):
    t = doc.add_table(rows=1, cols=len(headers))
    t.style = "Light Grid Accent 1"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr = t.rows[0].cells
    for i, htext in enumerate(headers):
        hdr[i].text = ""
        pr = hdr[i].paragraphs[0].add_run(htext)
        pr.bold = True
        pr.font.size = Pt(10)
        set_cn(pr)
    for row in rows:
        cells = t.add_row().cells
        for i, val in enumerate(row):
            cells[i].text = ""
            rr = cells[i].paragraphs[0].add_run(val)
            rr.font.size = Pt(9.5)
            set_cn(rr)
    if widths:
        for i, w in enumerate(widths):
            for r in t.rows:
                r.cells[i].width = Cm(w)
    return t

# ============ 标题 ============
title = doc.add_paragraph()
title.alignment = WD_ALIGN_PARAGRAPH.CENTER
tr = title.add_run("小区公共收益监管账户 · 一图读懂")
tr.bold = True
tr.font.size = Pt(18)
tr.font.color.rgb = NAVY
set_cn(tr)

sub = doc.add_paragraph()
sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
sr = sub.add_run("（依据：沪房规范〔2025〕8号，2026年4月1日起施行）")
sr.font.size = Pt(9.5)
sr.font.color.rgb = RGBColor(0x66, 0x66, 0x66)
set_cn(sr)

# ============ 一句话核心 ============
h1("先记住一句话")
body("小区公共收益（广告、停车、场地租金等）归全体业主共有，必须进专户、专款专用，花每一笔都要业主大会（或授权的业委会）点头。", bold=True, color=ORANGE)

# ============ 一、钱从哪来 ============
h1("一、公共收益都有啥")
body("凡是利用小区公共部位、共用设施赚的钱，都算公共收益：")
for x in ["电梯/楼道/门禁的广告费", "地面与地下车位停车费", "公共场地摆摊、快递柜、饮水机租金", "会所、泳池等经营收入", "通信基站、信号覆盖场地占用费", "利息收入（专户里的钱生钱）"]:
    bullet(x)

# ============ 二、账户怎么建 ============
h1("二、监管账户怎么建（3步）")
table(
    ["步骤", "干什么", "要点"],
    [
        ["1 开总户", "物业到指定银行（建行/上海银行）开对公监管总账户", "一家物业只能开一个监管账户"],
        ["2 分账", "在总户下按每个小区设分账户/虚拟账簿", "一个小区一本账，钱不混用"],
        ["3 接系统", "到维修资金开户行开'信息账'，接入监管系统", "当日办结；首季度入账前余额须为零"],
    ],
    widths=[2.2, 9.5, 4.5],
)

# ============ 三、钱怎么走 ============
h1("三、钱怎么进、怎么转（时间线）")
bullet("收入直接存进监管账户，专户专储，物业不能挪用。", "平时：")
bullet("每季度第1个月月底前，物业把上季度'扣掉管理成本后'的净收益划走：", "季度末：")
body("   · 业主大会还没成立  →  划到区房管局公共收益子账户（代管）")
body("   · 业主大会已成立  →  划到业主大会公共收益子账户")
bullet("扣除的'管理成本'部分，转回物业自己的其他账户。", "成本：")

# ============ 四、用钱要几步批 ============
h1("四、要花钱，走这 8 步")
for i, step in enumerate([
    "做年度使用计划",
    "业委会/物业动议，写使用方案",
    "报告居（村）'两委'",
    "业主大会表决（已一次性授权的，业委会可直接定）",
    "5万元以上工程：先审价 + 使用程序审核",
    "实施并验收",
    "银行审核后划付款项",
    "年度审计，结果公示不少于 30 日",
], 1):
    bullet(step, f"{i}. ")

body("铁规矩：公共收益优先补专项维修资金，补充比例须高于 50%；不是物业想花就能花。", bold=True, color=ORANGE)

# ============ 五、关键数字 ============
h1("五、记住这几个数")
table(
    ["数字", "含义"],
    [
        ["＞50%", "公共收益用于补充专项维修资金的最低比例"],
        ["5万元", "工程类使用超过此数，须先审价 + 程序审核"],
        ["30日", "年度审计结果最少公示天数"],
        ["每季度第1月月底", "上季度净收益划转截止时间"],
    ],
    widths=[3.5, 12.7],
)

# ============ 六、谁管啥 ============
h1("六、各方职责（一句话）")
bullet("业主大会/业委会：决定钱怎么花，监督公示。", "业主方：")
bullet("开户、归集、按批准划付，每季度公示收支。", "物业方：")
bullet("建专户体系、代管未成立业主大会前的收益、监管系统。", "房管方：")
bullet("接收报告、指导协调。", "居（村）委：")

# ============ 页脚说明 ============
doc.add_paragraph()
note = doc.add_paragraph()
nr = note.add_run("说明：本简版用于快速理解，具体操作以《上海市住宅小区公共收益管理办法》（沪房规范〔2025〕8号）原文为准。")
nr.font.size = Pt(8.5)
nr.font.color.rgb = RGBColor(0x88, 0x88, 0x88)
set_cn(nr)

out = r"D:\Claw\上海市住宅小区公共收益监管账户（简洁易懂版）.docx"
doc.save(out)
print("SAVED:", out)
