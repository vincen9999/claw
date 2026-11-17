# -*- coding: utf-8 -*-
"""生成《35kV、10kV 变电站 月度安全检查表》
依据：奉贤区域35KV、10KV电站安全管理专题会议纪要 + 《35kV、10kV 变电站日常安全管理检查标准》
（表格均不使用合并单元格，避免 python-docx 行列索引错位；同时采用固定列宽布局防止表头/表体错位）
"""
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'

C_TITLE = RGBColor(0x1F, 0x4E, 0x79)
C_HEAD  = RGBColor(0x1F, 0x4E, 0x79)
C_WHITE = RGBColor(0xFF, 0xFF, 0xFF)
C_RED   = RGBColor(0xC0, 0x00, 0x00)
C_GREY  = RGBColor(0x59, 0x59, 0x59)
SH_HEAD = "1F4E79"
SH_SUB  = "D9E2F3"
SH_PRI  = "FCE4D6"

CN = "宋体"
CN_B = "微软雅黑"

def east(run, name=CN):
    run.font.name = name
    r = run._element
    rPr = r.get_or_add_rPr()
    rFonts = rPr.find(qn('w:rFonts'))
    if rFonts is None:
        rFonts = OxmlElement('w:rFonts'); rPr.append(rFonts)
    rFonts.set(qn('w:ascii'), name)
    rFonts.set(qn('w:hAnsi'), name)
    rFonts.set(qn('w:eastAsia'), name)

def set_cell_text(cell, text, bold=False, size=9, color=None, align='left', font=CN):
    cell.text = ''
    p = cell.paragraphs[0]
    p.alignment = {'left': WD_ALIGN_PARAGRAPH.LEFT,
                   'center': WD_ALIGN_PARAGRAPH.CENTER,
                   'right': WD_ALIGN_PARAGRAPH.RIGHT}[align]
    p.paragraph_format.space_before = Pt(1)
    p.paragraph_format.space_after = Pt(1)
    p.paragraph_format.line_spacing = 1.0
    for i, line in enumerate(text.split('\n')):
        if i > 0:
            p.add_run().add_break()
        r = p.add_run(line)
        r.bold = bold; r.font.size = Pt(size)
        if color is not None:
            r.font.color.rgb = color
        east(r, font)

def shade(cell, hexcolor):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear'); shd.set(qn('w:color'), 'auto'); shd.set(qn('w:fill'), hexcolor)
    tcPr.append(shd)

def set_table_fixed(table, widths):
    tbl = table._tbl
    tblPr = tbl.tblPr
    layout = tblPr.find(qn('w:tblLayout'))
    if layout is None:
        layout = OxmlElement('w:tblLayout'); tblPr.append(layout)
    layout.set(qn('w:type'), 'fixed')
    grid = tbl.find(qn('w:tblGrid'))
    if grid is None:
        grid = OxmlElement('w:tblGrid'); tbl.insert(0, grid)
    for gc in list(grid.findall(qn('w:gridCol'))):
        grid.remove(gc)
    for w_ in widths:
        gc = OxmlElement('w:gridCol'); gc.set(qn('w:w'), str(int(w_))); grid.append(gc)
    for row in tbl.iter(qn('w:tr')):
        cells = row.findall(qn('w:tc'))
        for i, tc in enumerate(cells):
            if i >= len(widths):
                continue
            tcPr = tc.get_or_add_tcPr()
            tcW = tcPr.find(qn('w:tcW'))
            if tcW is None:
                tcW = OxmlElement('w:tcW'); tcPr.append(tcW)
            tcW.set(qn('w:w'), str(int(widths[i]))); tcW.set(qn('w:type'), 'dxa')

def module_heading(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(4); p.paragraph_format.space_after = Pt(2)
    r = p.add_run(text); r.bold = True; r.font.size = Pt(10.5); r.font.color.rgb = C_HEAD; east(r, CN_B)

# ============ 文档 ============
doc = Document()
for s in doc.sections:
    s.top_margin = Cm(1.5); s.bottom_margin = Cm(1.5)
    s.left_margin = Cm(1.8); s.right_margin = Cm(1.8)

# ---- 标题 ----
p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run('35kV、10kV 变电站 月度安全检查表')
r.bold = True; r.font.size = Pt(18); r.font.color.rgb = C_TITLE; east(r, CN_B)
p2 = doc.add_paragraph(); p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
r2 = p2.add_run('（依据《奉贤区域35kV、10kV电站安全管理专题会议纪要》及《35kV、10kV 变电站日常安全管理检查标准》）')
r2.font.size = Pt(9); r2.font.color.rgb = C_GREY; east(r2, CN)

# ---- 一、基本信息 ----
module_heading('一、基本信息')
info_w = [1600, 2900, 1600, 2900]
t = doc.add_table(rows=4, cols=4); t.alignment = WD_TABLE_ALIGNMENT.CENTER
info = [
    ('电站名称 / 编号', '＿＿＿＿＿＿', '电压等级', '□35kV  □10kV'),
    ('检查月份', '＿＿年＿＿月', '检查日期', '＿＿年＿＿月＿＿日'),
    ('检查人', '＿＿＿＿＿＿', '受检单位（运维）', '＿＿＿＿＿＿'),
    ('天气 / 气温', '＿＿＿＿  ＿＿℃', '检查结论', '□合格  □限期整改  □不合格'),
]
for ri, (k1, v1, k2, v2) in enumerate(info):
    set_cell_text(t.cell(ri,0), k1, bold=True, size=9, color=C_HEAD, align='center', font=CN_B); shade(t.cell(ri,0), SH_SUB)
    set_cell_text(t.cell(ri,1), v1, size=9)
    set_cell_text(t.cell(ri,2), k2, bold=True, size=9, color=C_HEAD, align='center', font=CN_B); shade(t.cell(ri,2), SH_SUB)
    set_cell_text(t.cell(ri,3), v2, size=9)
set_table_fixed(t, info_w)

doc.add_paragraph().paragraph_format.space_after = Pt(2)

# ---- 二、会议纪要重点整改项（月度必查） ----
module_heading('二、会议纪要重点整改项（月度必查）')
note = doc.add_paragraph()
rn = note.add_run('※ 依据专题会议纪要（2026-11-05）集团质量检查发现问题，以下六项纳入每月必查，发现问题立即整改闭环。')
rn.font.size = Pt(8.5); rn.font.color.rgb = C_RED; east(rn, CN)

cols = ['序号', '重点整改项', '检查标准与要求', '检查结果\n(合格/不合格/不适用)', '问题描述', '整改要求 / 期限']
pri_w = [450, 1500, 3200, 1150, 1300, 1400]
tp = doc.add_table(rows=1+6, cols=6); tp.alignment = WD_TABLE_ALIGNMENT.CENTER
for ci, c in enumerate(cols):
    set_cell_text(tp.cell(0,ci), c, bold=True, size=9, color=C_WHITE, align='center', font=CN_B); shade(tp.cell(0,ci), SH_HEAD)
pri = [
    ('值班室严禁设置床铺', '35kV 值班室不得设置床铺；严禁在生活区外摆放床铺、被褥等生活用品，保持值班室整洁规范。'),
    ('配齐安全帽（绝缘帽）及二氧化碳灭火器', '每个站点按定员配备合格安全帽（绝缘帽）；控制室、关键设备室配置二氧化碳灭火器，数量、位置符合消防要求。'),
    ('绝缘手套符合 30kV 绝缘要求', '现场绝缘手套电压等级不低于 30kV、试验合格且在有效期内，外观无破损，定置存放可取用。'),
    ('设备巡检记录放置于现场', '每台/每回路设备的巡视检查记录册（卡）置于现场对应位置，记录真实、连续、可追溯。'),
    ('照明开关全部更换为漏电保护开关', '站内所有照明开关更换为带漏电保护功能的开关（漏保），动作可靠，无裸露、无破损。'),
    ('粘鼠板飞尘多的全部更换', '防小动物粘鼠板/设施保持有效，积灰、失效、污染的及时全部更换，并登记更换日期。'),
]
for i, (item, std) in enumerate(pri, 1):
    set_cell_text(tp.cell(i,0), str(i), size=9, align='center')
    set_cell_text(tp.cell(i,1), item, bold=True, size=9)
    set_cell_text(tp.cell(i,2), std, size=8.5)
    set_cell_text(tp.cell(i,3), '', size=9, align='center')
    set_cell_text(tp.cell(i,4), '', size=8.5)
    set_cell_text(tp.cell(i,5), '', size=8.5)
    for ci in range(6):
        shade(tp.cell(i,ci), SH_PRI)
set_table_fixed(tp, pri_w)

doc.add_paragraph().paragraph_format.space_after = Pt(2)

# ---- 三、月度安全检查项目（按十大模块） ----
module_heading('三、月度安全检查项目（参照《35kV、10kV 变电站日常安全管理检查标准》）')
item_w = [450, 1400, 3500, 1050, 1300, 1300]
modules = [
    ('4.1 人员资质与培训', [
        ('持证上岗', '运行、值班、倒闸操作人员须持有效特种作业（电工）操作证或相应资质，严禁无证上岗。', '安全生产法、GB/T 32893 5.4'),
        ('安规考试', '在岗人员每年一次安规考试合格；消防知识每年考试一次。', 'GB 26860、DL 5027 1.0.6'),
        ('培训合格', '新进、转岗、复岗人员须经安全培训并考试合格后方可上岗。', '安全生产法 第二十八条'),
        ('外来人员管理', '外来施工/参观人员须登记、交待安全事项，并在监护下活动。', 'GB 26860'),
    ]),
    ('4.2 运行值班与交接班', [
        ('值守纪律', '变电站应 24h 值守（或按规定巡维）；服从调度指令，不做与运行无关之事。', 'GB/T 32893 6.1'),
        ('交接班', '事故处理或操作中不得交接班；交班人陪同共同检查核对无误后签字。', 'GB/T 32893 6.2'),
        ('运行记录', '运行日志、缺陷、操作、巡视记录齐全、真实、规范。', 'GB/T 32893'),
        ('录音要求', '与电网有调度关系的操作、事故处理应启用录音设备并留存。', 'GB/T 32893 6.1.3'),
    ]),
    ('4.3 设备巡视与状态', [
        ('巡视制度', '按规定路线、定点定时巡视；发现缺陷及时记录、汇报、处理。', 'DL/T 969、GB/T 32893 6.3'),
        ('变压器（室）', '油位油温正常；无异常声响渗漏；呼吸器硅胶不过潮；冷却正常；分接开关位置正确。', 'DL/T 596、GB 26860'),
        ('开关柜/断路器', 'SF6 压力正常（或真空完好）；柜体无异响过热；五防锁具完好。', 'GB 26860、二十五项反措2023'),
        ('电力电缆', '终端无放电过热；电缆沟无积水、封堵严密；电缆无破损。', 'DL 5027、GB 50229'),
        ('互感器、避雷器', '瓷套清洁无裂纹放电；避雷器计数器/在线监测正常；接地可靠。', 'DL/T 596'),
        ('红外测温', '高峰负荷对设备接头、刀闸、电缆终端测温，发现过热及时处理。', 'GB 26860'),
        ('异常特巡', '过电压/短路冲击、过负荷、新投运、检修后、恶劣天气、保电等增加巡视。', 'GB/T 32893 6.3.3'),
    ]),
    ('4.4 倒闸操作与“五防”', [
        ('操作票', '倒闸操作必须填用操作票（一任务一票）；监护操作须两人进行。', 'GB 26860 5.3'),
        ('操作顺序', '停电：断路器→负荷侧隔离开关→电源侧；送电相反；严禁带负荷拉合隔离开关。', 'GB 26860'),
        ('“五防”装置', '防误闭锁完好投运；严禁擅自退出；停用须批准并限期修复。', '二十五项反措2023 第3部分'),
        ('技术措施', '停电、验电、装设接地线、悬挂标示牌、装设遮栏（围栏）逐项落实。', 'GB 26860'),
        ('解锁钥匙', '解锁钥匙封存、编号、专用，使用须审批并登记。', 'GB 26860、国家电网防误规定'),
    ]),
    ('4.5 消防安全管理', [
        ('消防设施', '灭火器（按 GB 50140 配置）、报警、消防给水、应急照明完好有效，定期巡检换药检测。', 'DL 5027、GB 50229、GB 50140'),
        ('防火封堵', '电缆孔洞、盘柜、穿墙套管封堵严密、用阻燃材料；电缆通道防火分隔到位。', 'GB 50229、DL 5027 10.5'),
        ('动火管理', '动火须办动火票，落实监护、隔离、清理、灭火器材；禁止动火条件不得作业。', 'DL 5027 第5章'),
        ('疏散与通道', '安全出口、疏散通道、消防车通道畅通，严禁锁闭、堆物。', '消防法、GB 50016'),
        ('禁放物品', '控制室、配电室、电缆夹层严禁存放易燃易爆物品。', 'DL 5027 6'),
        ('蓄电池室', '通风良好，防爆电气；氢（酸）气泄漏监测与报警正常。', 'DL 5027 10.6'),
    ]),
    ('4.6 安全工器具管理', [
        ('配置齐全', '绝缘手套、绝缘靴、验电器、接地线（编号）、绝缘杆、标示牌、遮栏/围栏齐全。', 'GB 26860、DL 5027'),
        ('定期试验', '工器具按周期试验合格并在有效期内；超期、不合格一律停用。', 'GB 26860、DL/T 596'),
        ('存放管理', '定置存放、干燥清洁，不与一般工器具混放；使用前检查外观。', 'GB 26860'),
    ]),
    ('4.7 环境与辅助设施', [
        ('防小动物', '挡鼠板、防鼠网、通风百叶、电缆沟封堵齐全有效；站内无鼠害痕迹。', '二十五项反措2023'),
        ('通风/温湿度', '开关室、电容器室、电缆室通风良好；温湿度在设备允许范围。', '运行规程'),
        ('防汛/排水', '排水沟畅通；防汛沙袋、抽水泵、挡水板齐备可用。', '二十五项反措2023'),
        ('照明/标识', '事故照明、正常照明完好；设备双重名称、安全警示牌、模拟图板清晰准确。', 'GB 26860'),
        ('接地与防雷', '接地网、设备接地可靠；避雷器、避雷带完好；接地电阻定期检测合格。', 'DL/T 596'),
    ]),
    ('4.8 二次系统与电力监控', [
        ('保护投运', '继电保护、安全自动装置投运状态与定值不得擅自更改；涉网保护按调度要求执行。', 'GB/T 32893 6.5'),
        ('告警处置', '保护、自动化、通信、监控告警或动作后，立即汇报调度并查明原因。', 'GB/T 32893 6.5.3'),
        ('监控安防', '电力监控系统落实安全防护，严禁违规外联、越权操作。', '国家发改委第41号、GB 26860'),
    ]),
    ('4.9 隐患治理与闭环', [
        ('排查建档', '建立隐患排查治理台账，日常排查发现的问题登记、分级。', '国家发改委第41号令'),
        ('一般隐患', '即查即改；不能立即整改的，落实责任人、措施、期限并跟踪。', '国家能源局隐患治理规定'),
        ('重大隐患', '立即管控并上报；挂牌督办、限期治理、验收销号，闭环管理。', '国家发改委第41号令'),
        ('判定标准', '重大隐患按第41号令判定情形（设备设施、监控、管理等领域）执行。', '国家发改委第41号令'),
    ]),
    ('4.10 应急管理与事故报告', [
        ('应急预案', '编制触电、火灾、全站失电、防汛等现场处置方案，并备案。', '安全生产法、应急条例'),
        ('演练与物资', '定期演练（每年≥1次）；应急物资、通讯工具齐备可用。', '应急条例、DL 5027'),
        ('事故报告', '发生事故（事件）按规定时限上报，保护现场、如实报告，不得瞒报谎报。', '安全生产法、493号令'),
    ]),
]
for title, items in modules:
    module_heading('● ' + title)
    n = len(items)
    t = doc.add_table(rows=1+n, cols=6); t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for ci, c in enumerate(cols):
        set_cell_text(t.cell(0,ci), c, bold=True, size=9, color=C_WHITE, align='center', font=CN_B); shade(t.cell(0,ci), SH_HEAD)
    for i, (item, std, basis) in enumerate(items, 1):
        set_cell_text(t.cell(i,0), str(i), size=9, align='center')
        set_cell_text(t.cell(i,1), item, bold=True, size=9)
        set_cell_text(t.cell(i,2), std + '（依据：' + basis + '）', size=8)
        set_cell_text(t.cell(i,3), '', size=9, align='center')
        set_cell_text(t.cell(i,4), '', size=8)
        set_cell_text(t.cell(i,5), '', size=8)
    set_table_fixed(t, item_w)
    doc.add_paragraph().paragraph_format.space_after = Pt(2)

# ---- 四、检查结论与签字 ----
module_heading('四、检查结论与签字确认')
info_w2 = [1700, 2900, 2000, 2400]
t = doc.add_table(rows=4, cols=4); t.alignment = WD_TABLE_ALIGNMENT.CENTER
concl = [
    ('检查结论', '□合格   □限期整改   □不合格', '发现隐患', '一般隐患＿＿项；重大隐患＿＿项'),
    ('整改闭环要求', '限期整改项应于＿＿年＿＿月＿＿日前完成整改并复查闭环；重大隐患按规定上报、挂牌督办、验收销号。', '', ''),
    ('检查人（签字）', '＿＿＿＿＿＿', '受检单位/运维（签收）', '＿＿＿＿＿＿'),
    ('站长/安全员（签字）', '＿＿＿＿＿＿', '日期', '＿＿年＿＿月＿＿日'),
]
# 第0行
set_cell_text(t.cell(0,0), '检查结论', bold=True, size=9, color=C_HEAD, align='center', font=CN_B); shade(t.cell(0,0), SH_SUB)
set_cell_text(t.cell(0,1), '□合格   □限期整改   □不合格', size=9)
set_cell_text(t.cell(0,2), '发现隐患', bold=True, size=9, color=C_HEAD, align='center', font=CN_B); shade(t.cell(0,2), SH_SUB)
set_cell_text(t.cell(0,3), '一般隐患＿＿项；重大隐患＿＿项', size=9)
# 第1行：整改闭环（跨列两格分别填，避免合并错位）
set_cell_text(t.cell(1,0), '整改闭环要求', bold=True, size=9, color=C_HEAD, align='center', font=CN_B); shade(t.cell(1,0), SH_SUB)
set_cell_text(t.cell(1,1), '限期整改项应于＿＿年＿＿月＿＿日前完成整改并复查闭环；重大隐患按规定上报、挂牌督办、验收销号。', size=8.5)
set_cell_text(t.cell(1,2), '', size=8.5); set_cell_text(t.cell(1,3), '', size=8.5)
# 第2行
set_cell_text(t.cell(2,0), '检查人（签字）', bold=True, size=9, color=C_HEAD, align='center', font=CN_B); shade(t.cell(2,0), SH_SUB)
set_cell_text(t.cell(2,1), '＿＿＿＿＿＿', size=9)
set_cell_text(t.cell(2,2), '受检单位/运维（签收）', bold=True, size=9, color=C_HEAD, align='center', font=CN_B); shade(t.cell(2,2), SH_SUB)
set_cell_text(t.cell(2,3), '＿＿＿＿＿＿', size=9)
# 第3行
set_cell_text(t.cell(3,0), '站长/安全员（签字）', bold=True, size=9, color=C_HEAD, align='center', font=CN_B); shade(t.cell(3,0), SH_SUB)
set_cell_text(t.cell(3,1), '＿＿＿＿＿＿', size=9)
set_cell_text(t.cell(3,2), '日期', bold=True, size=9, color=C_HEAD, align='center', font=CN_B); shade(t.cell(3,2), SH_SUB)
set_cell_text(t.cell(3,3), '＿＿年＿＿月＿＿日', size=9)
set_table_fixed(t, info_w2)

foot = doc.add_paragraph()
fr = foot.add_run('说明：本表由每月检查使用，检查人、受检单位签字确认后留档备查；发现重大隐患须单独填报并按国家发改委第41号令上报。')
fr.font.size = Pt(8); fr.font.color.rgb = C_GREY; east(fr, CN)

out = r'D:\Claw\35kV_10kV变电站月度安全检查表.docx'
doc.save(out)
print('saved:', out)
