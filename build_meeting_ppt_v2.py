# -*- coding: utf-8 -*-
"""美化版会议PPT：商务蓝主题 + AI插图 + 表格/要点排版（可编辑）。"""
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn
from PIL import Image

A = "D:/Claw/meeting_assets/"
IMG = {
    "hero":        A + "Modern_outdoor_35kV_electrical_2026-11-06T02-29-35.png",
    "ppe":         A + "Flat_vector_illustration__whit_2026-11-06T02-30-43.png",
    "inspection":  A + "Flat_vector_illustration__whit_2026-11-06T02-37-14.png",
    "fire":        A + "Flat_vector_illustration__whit_2026-11-06T02-37-33.png",
    "hazard":      A + "Flat_vector_illustration__whit_2026-11-06T02-37-51.png",
    "management":  A + "Flat_vector_illustration__whit_2026-11-06T02-38-28.png",
}

PRIMARY  = RGBColor(0x1E, 0x3C, 0x72)   # 深蓝
SECOND   = RGBColor(0x34, 0x98, 0xDB)   # 亮蓝
ACCENT   = RGBColor(0xF1, 0xC4, 0x0F)   # 琥珀
LIGHT    = RGBColor(0xF2, 0xF6, 0xFB)   # 浅蓝灰
TEXTD    = RGBColor(0x2C, 0x3E, 0x50)   # 深字
TEXTS    = RGBColor(0x7F, 0x8C, 0x8D)   # 次字
WHITE    = RGBColor(0xFF, 0xFF, 0xFF)
LINEGRY  = RGBColor(0xD9, 0xE2, 0xEC)
GRIDALT  = RGBColor(0xEC, 0xF2, 0xFA)

EMU = 914400
def IN(x): return int(x * EMU)
def font(run, size, color=TEXTD, bold=False, name="微软雅黑"):
    run.font.size = Pt(size); run.font.color.rgb = color; run.font.bold = bold
    run.font.name = name
    rPr = run._r.get_or_add_rPr()
    rPr.set(qn('a:ea'), name); rPr.set(qn('a:cs'), name)

prs = Presentation()
prs.slide_width  = IN(13.333)
prs.slide_height = IN(7.5)
BLANK = prs.slide_layouts[6]
SW, SH = 13.333, 7.5
ML = 0.6; MR = 0.6
def add_slide(): return prs.slides.add_slide(BLANK)

def rect(slide, l, t, w, h, fill, line=None, line_w=None, shape=MSO_SHAPE.RECTANGLE):
    sp = slide.shapes.add_shape(shape, IN(l), IN(t), IN(w), IN(h))
    sp.fill.solid(); sp.fill.fore_color.rgb = fill
    if line is None:
        sp.line.fill.background()
    else:
        sp.line.color.rgb = line; sp.line.width = Pt(line_w or 1)
    sp.shadow.inherit = False
    return sp

def textbox(slide, l, t, w, h, anchor=MSO_ANCHOR.TOP, wrap=True):
    tb = slide.shapes.add_textbox(IN(l), IN(t), IN(w), IN(h))
    tf = tb.text_frame; tf.word_wrap = wrap
    tf.vertical_anchor = anchor
    tf.margin_left = IN(0.05); tf.margin_right = IN(0.05)
    tf.margin_top = IN(0.02); tf.margin_bottom = IN(0.02)
    return tb, tf

def set_para(p, text, size, color=TEXTD, bold=False, align=PP_ALIGN.LEFT, space_after=4, level=0):
    p.text = text; p.alignment = align; p.level = level
    p.space_after = Pt(space_after); p.space_before = Pt(0)
    for r in p.runs:
        font(r, size, color, bold)
    return p

def title_band(slide, title, kicker=None):
    rect(slide, 0, 0, SW, 1.12, PRIMARY)
    rect(slide, 0, 1.12, SW, 0.07, ACCENT)
    if kicker:
        tb, tf = textbox(slide, ML, 0.14, SW-ML-MR, 0.3)
        set_para(tf.paragraphs[0], kicker, 11, ACCENT, bold=True)
    tb, tf = textbox(slide, ML, 0.42 if kicker else 0.28, SW-ML-MR, 0.62, anchor=MSO_ANCHOR.MIDDLE)
    set_para(tf.paragraphs[0], title, 25, WHITE, bold=True)

def footer(slide, idx):
    tb, tf = textbox(slide, ML, 7.08, 9.5, 0.32)
    set_para(tf.paragraphs[0], "奉贤区域 35kV/10kV 电站安全管理专题会议", 9, TEXTS)
    tb, tf = textbox(slide, SW-1.3, 7.08, 0.9, 0.32)
    set_para(tf.paragraphs[0], str(idx), 9, TEXTS, align=PP_ALIGN.RIGHT)

def side_image(slide, path, l, t, w, h, frame=True):
    # fit preserving aspect, center in box
    iw, ih = Image.open(path).size
    ar = iw/ih; bar = w/h
    if ar > bar:
        dw = w; dh = w/ar
    else:
        dh = h; dw = h*ar
    il = l + (w-dw)/2; it = t + (h-dh)/2
    if frame:
        rect(slide, l-0.06, t-0.06, w+0.12, h+0.12, LIGHT, line=LINEGRY, line_w=1, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    slide.shapes.add_picture(path, IN(il), IN(it), IN(dw), IN(dh))

def bullets(slide, items, l, t, w, h, size=14, gap=8, accent=ACCENT):
    tb, tf = textbox(slide, l, t, w, h)
    first = True
    for it in items:
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        p.space_after = Pt(gap); p.space_before = Pt(0)
        # accent marker
        r0 = p.add_run(); r0.text = "▎ "; font(r0, size, accent, bold=True)
        r1 = p.add_run(); r1.text = it; font(r1, size, TEXTD)
    return tb

def add_table(slide, headers, rows, l, t, w, col_w, fsize=11, hsize=11):
    nrows = len(rows)+1; ncols = len(headers)
    gf = slide.shapes.add_table(nrows, ncols, IN(l), IN(t), IN(w), IN(0.4*nrows))
    tbl = gf.table
    tbl.first_row = False; tbl.horz_banding = False
    # column widths
    for i, cw in enumerate(col_w):
        tbl.columns[i].width = IN(cw)
    # header
    for j, htext in enumerate(headers):
        c = tbl.cell(0, j); c.fill.solid(); c.fill.fore_color.rgb = PRIMARY
        c.vertical_anchor = MSO_ANCHOR.MIDDLE
        c.margin_left = IN(0.06); c.margin_right = IN(0.06); c.margin_top = IN(0.03); c.margin_bottom = IN(0.03)
        tf = c.text_frame; tf.word_wrap = True; p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER if j==0 else PP_ALIGN.LEFT
        set_para(p, htext, hsize, WHITE, bold=True)
    # body
    for i, row in enumerate(rows):
        for j, val in enumerate(row):
            c = tbl.cell(i+1, j)
            c.fill.solid(); c.fill.fore_color.rgb = GRIDALT if i % 2 == 1 else WHITE
            c.vertical_anchor = MSO_ANCHOR.MIDDLE
            c.margin_left = IN(0.06); c.margin_right = IN(0.06); c.margin_top = IN(0.03); c.margin_bottom = IN(0.03)
            tf = c.text_frame; tf.word_wrap = True; p = tf.paragraphs[0]
            p.alignment = PP_ALIGN.CENTER if j==0 else PP_ALIGN.LEFT
            set_para(p, val, fsize, TEXTD)
    return gf

def section_divider(slide, num, title):
    rect(slide, 0, 0, SW, SH, PRIMARY)
    rect(slide, 0, 0, 0.22, SH, ACCENT)
    # big number
    tb, tf = textbox(slide, 0.9, 1.7, 4, 2.4, anchor=MSO_ANCHOR.MIDDLE)
    set_para(tf.paragraphs[0], num, 90, SECOND, bold=True)
    tb, tf = textbox(slide, 0.95, 3.9, 11.4, 2.2)
    set_para(tf.paragraphs[0], title, 30, WHITE, bold=True)
    rect(slide, 1.0, 5.5, 2.2, 0.09, ACCENT)

# ============ 内容定义 ============
SLIDES = [
 ("cover",),
 ("info",),
 ("agenda",),
 ("section", "一", "集团对电站质量检查情况"),
 ("content", "质量检查发现的六项问题",
   ["35kV 值班室设置床铺，不符合值班管理要求",
    "站点未配备安全帽（绝缘帽）及二氧化碳灭火器",
    "现场绝缘手套不符合 30kV 绝缘要求",
    "各设备巡检记录未放置在现场",
    "站内照明开关需全部更换为漏电保护开关",
    "站内粘鼠板飞尘较多，需全部更换"], "hazard"),
 ("section", "二", "电站安全管理措施与要求"),
 ("timeline", "安全管理三项措施",
   [("立即全面排查","2026年11月7日前，各项目对所辖 35kV、10kV 电站组织一次全面安全检查，逐站排查隐患，形成书面记录"),
    ("限期整改约谈","约谈运维单位限期整改，明确整改内容、责任人与时限，书面签收确认；逾期未改书面抄报甲方"),
    ("常态化机制","每月至少组织一次检查，形成常态化检查机制，结果留档备查，保障电站安全运行")], "inspection"),
 ("section", "三", "检查标准与要求"),
 ("content", "日常检查标准依据",
   ["日常检查参照附件《35kV、10kV 变电站日常安全管理检查参照标准》",
    "同时执行临港集团关于电站管理相关的标准要求",
    "标准涵盖人员资质、运行值班、设备巡视、倒闸操作、消防、工器具、环境、二次系统、隐患治理与应急管理"], "ppe"),
 ("section", "附", "日常安全管理检查标准"),
 ("content", "检查标准结构",
   ["一、适用范围",
    "二、编制依据（现行法律法规、消防与电力行业规程）",
    "三、检查分类与频次",
    "四、日常安全管理检查标准（十大模块）",
    "五、隐患分级与闭环管理"], "management"),
 ("content2", "日常安全管理十大检查模块",
   ["4.1 人员资质与培训","4.2 运行值班与交接班","4.3 设备巡视与状态","4.4 倒闸操作与“五防”",
    "4.5 消防安全管理","4.6 安全工器具管理","4.7 环境与辅助设施","4.8 二次系统与电力监控",
    "4.9 隐患治理与闭环","4.10 应急管理与事故报告"], "management"),
 ("table", "检查分类与频次", ["检查类别","频次 / 时机","责任主体"],
   [["日常巡视","每班不少于1次；高峰负荷、恶劣天气增加频次","当班运行人员"],
    ["交接班检查","每班交接时共同核查","交/接班人员"],
    ["定期专项检查","每周（消防、工器具）、每月（设备、隐患）","安全员 / 站长"],
    ["操作后/异常后特巡","倒闸操作后、设备受短路冲击或过负荷后","当班人员"],
    ["季节性检查","雷雨前、高温、严寒、防汛、防小动物","站长 / 安全员"],
    ["保电/节假日检查","重大活动、节假日前后","站长"]], [2.6, 6.0, 2.4], "management"),
 ("table", "示例：4.5 消防安全管理检查要点", ["检查项目","检查标准与要求"],
   [["消防设施","灭火器（按 GB 50140 配置）、火灾报警、消防给水、应急照明完好有效，定期巡检、换药、检测"],
    ["防火封堵","电缆孔洞、盘柜、穿墙套管封堵严密，使用阻燃材料；电缆通道防火分隔到位"],
    ["动火管理","动火须办理动火票，落实监护、隔离、清理、灭火器材"],
    ["疏散与通道","安全出口、疏散通道、消防车通道畅通，严禁锁闭、堆物"],
    ["禁放物品","控制室、配电室、电缆夹层严禁存放易燃易爆物品"],
    ["蓄电池室","通风良好，防爆电气；氢（酸）气泄漏监测与报警正常"]], [2.3, 9.7], "fire"),
 ("content", "隐患分级与闭环管理",
   ["依据《电力重大事故隐患判定标准及治理监督管理规定》（国家发改委令第41号，2026-07-01 施行）",
    "一般隐患：立即整改或落实防范措施，明确责任人、措施和期限，整改后确认销项",
    "重大隐患：立即采取停产停运、撤离人员等管控措施并上报；挂牌督办、限期治理、评估验收、销号闭环",
    "主要负责人对重大隐患排查治理负首要责任；治理情况如实记录并向从业人员通报"], "hazard"),
 ("summary", "会议要求",
   ["立即全面排查：2026年11月7日前完成所辖电站安全检查",
    "限期整改：约谈运维单位，明确责任人与时限，书面签收",
    "常态机制：每月至少一次检查，结果留档备查",
    "标准落地：严格按附件检查标准与临港集团要求执行"],
   "保障 35kV、10kV 电站安全稳定运行", "management"),
 ("contact", "会议落款", "主持：杨文胜　|　奉贤区域 35kV、10kV 电站安全管理专题会议纪要　|　2026年11月5日"),
]

idx = 0
for s in SLIDES:
    kind = s[0]
    idx += 1
    if kind == "cover":
        slide = add_slide()
        rect(slide, 0, 0, 7.0, SH, PRIMARY)
        rect(slide, 7.0, 0, 0.12, SH, ACCENT)
        tb, tf = textbox(slide, 0.7, 2.5, 5.9, 2.4, anchor=MSO_ANCHOR.TOP)
        set_para(tf.paragraphs[0], "奉贤区域 35kV、10kV", 30, WHITE, bold=True)
        p = tf.add_paragraph(); set_para(p, "电站安全管理专题会议", 30, WHITE, bold=True)
        rect(slide, 0.75, 4.55, 1.6, 0.06, ACCENT)
        tb, tf = textbox(slide, 0.7, 4.8, 5.9, 1.6)
        set_para(tf.paragraphs[0], "会议纪要 · 2026年11月5日", 15, SECOND, bold=True)
        p = tf.add_paragraph(); set_para(p, "蓝创中心 12#楼 2F 会议室", 13, RGBColor(0xCF,0xDD,0xEE))
        slide.shapes.add_picture(IMG["hero"], IN(7.12), IN(0), IN(6.21), IN(SH))
        continue

    if kind == "info":
        slide = add_slide()
        title_band(slide, "会议概况", "MEETING OVERVIEW")
        rows = [["会议时间","2026年11月5日 16:00"],
                ["会议地点","蓝创中心 12#楼 2F 会议室"],
                ["会议主题","35kV、10kV 电站安全管理"],
                ["主　持","杨文胜"],
                ["参加项目","蓝创中心、香樟园、青桐园、玉兰园、6期、7期8期、10期、夏栎园"]]
        add_table(slide, ["项目","内容"], rows, ML, 1.5, 7.4, [1.7, 5.7], fsize=12, hsize=12)
        side_image(slide, IMG["management"], 8.2, 1.7, 4.55, 4.4)
        footer(slide, idx); continue

    if kind == "agenda":
        slide = add_slide()
        title_band(slide, "会议议程", "AGENDA")
        items = ["一、集团对电站质量检查情况","二、电站安全管理措施与要求",
                 "三、检查标准与要求","附件：日常安全管理检查标准"]
        bullets(slide, items, ML, 1.7, 7.2, 4.6, size=17, gap=16)
        side_image(slide, IMG["management"], 8.2, 1.7, 4.55, 4.4)
        footer(slide, idx); continue

    if kind == "section":
        slide = add_slide()
        section_divider(slide, s[1], s[2])
        footer(slide, idx); continue

    if kind == "content":
        slide = add_slide()
        title_band(slide, s[1], "KEY POINTS")
        bullets(slide, s[2], ML, 1.55, 7.2, 5.2, size=14, gap=10)
        if s[3]:
            side_image(slide, IMG[s[3]], 8.2, 1.6, 4.55, 4.6)
        footer(slide, idx); continue

    if kind == "content2":
        slide = add_slide()
        title_band(slide, s[1], "10 MODULES")
        # two columns
        left = s[2][:5]; right = s[2][5:]
        bullets(slide, left, ML, 1.6, 5.9, 5.0, size=14, gap=10)
        bullets(slide, right, 6.7, 1.6, 5.9, 5.0, size=14, gap=10)
        footer(slide, idx); continue

    if kind == "timeline":
        slide = add_slide()
        title_band(slide, s[1], "ACTION PLAN")
        ms = s[2]
        # vertical timeline with three nodes on left, text right
        top = 1.7; gap = 1.55; x = 1.1
        rect(slide, x, top, 0.05, gap*(len(ms)-1)+0.4, SECOND)
        for i,(lab,desc) in enumerate(ms):
            cy = top + gap*i
            c = slide.shapes.add_shape(MSO_SHAPE.OVAL, IN(x-0.28), IN(cy-0.28), IN(0.56), IN(0.56))
            c.fill.solid(); c.fill.fore_color.rgb = PRIMARY; c.line.color.rgb = ACCENT; c.line.width=Pt(2); c.shadow.inherit=False
            tb, tf = textbox(slide, x-0.28, cy-0.34, 0.56, 0.62, anchor=MSO_ANCHOR.MIDDLE)
            set_para(tf.paragraphs[0], str(i+1), 16, WHITE, bold=True, align=PP_ALIGN.CENTER)
            tb, tf = textbox(slide, 1.9, cy-0.42, 6.0, 1.2, anchor=MSO_ANCHOR.MIDDLE)
            set_para(tf.paragraphs[0], lab, 15, PRIMARY, bold=True)
            p = tf.add_paragraph(); set_para(p, desc, 11.5, TEXTD)
        side_image(slide, IMG[s[3]], 8.2, 1.7, 4.55, 4.4)
        footer(slide, idx); continue

    if kind == "table":
        slide = add_slide()
        title_band(slide, s[1], "STANDARD")
        add_table(slide, s[2], s[3], ML, 1.55, sum(s[4]), s[4], fsize=11.5, hsize=12)
        if s[5]:
            side_image(slide, IMG[s[5]], 8.4, 1.7, 4.3, 4.3)
        footer(slide, idx); continue

    if kind == "summary":
        slide = add_slide()
        title_band(slide, s[1], "SUMMARY")
        bullets(slide, s[2], ML, 1.6, 7.2, 4.0, size=15, gap=12)
        rect(slide, ML, 5.95, 7.2, 0.85, ACCENT)
        tb, tf = textbox(slide, ML+0.2, 5.95, 6.8, 0.85, anchor=MSO_ANCHOR.MIDDLE)
        set_para(tf.paragraphs[0], "结论：" + s[3], 15, TEXTD, bold=True)
        side_image(slide, IMG[s[4]], 8.2, 1.7, 4.55, 4.4)
        footer(slide, idx); continue

    if kind == "contact":
        slide = add_slide()
        rect(slide, 0, 0, SW, SH, PRIMARY)
        rect(slide, 0, 0, 0.22, SH, ACCENT)
        tb, tf = textbox(slide, 1.0, 2.7, 11.3, 1.4, anchor=MSO_ANCHOR.MIDDLE)
        set_para(tf.paragraphs[0], s[1], 30, WHITE, bold=True)
        rect(slide, 1.0, 4.0, 2.2, 0.08, ACCENT)
        tb, tf = textbox(slide, 1.0, 4.3, 11.3, 1.4)
        set_para(tf.paragraphs[0], s[2], 14, RGBColor(0xCF,0xDD,0xEE))
        footer(slide, idx); continue

OUT = "D:/Claw/35KV10KV电站管理专题会议_美化.pptx"
prs.save(OUT)
print("saved:", OUT, "slides:", len(prs.slides._sldIdLst))
