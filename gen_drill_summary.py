# -*- coding: utf-8 -*-
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn

doc = Document()

def set_font(run, name='宋体', size=11, bold=False, color=None):
    run.font.name = name
    run.font.size = Pt(size)
    run.font.bold = bold
    if color:
        run.font.color.rgb = color
    rPr = run._element.get_or_add_rPr()
    rFonts = rPr.find(qn('w:rFonts'))
    if rFonts is None:
        rFonts = qn('w:rFonts') and __import__('docx.oxml').oxml.OxmlElement('w:rFonts')
        rPr.append(rFonts)
    rFonts.set(qn('w:eastAsia'), name)
    rFonts.set(qn('w:ascii'), name)
    rFonts.set(qn('w:hAnsi'), name)

for s in doc.sections:
    s.top_margin = Cm(2.2); s.bottom_margin = Cm(2.2)
    s.left_margin = Cm(2.5); s.right_margin = Cm(2.5)

def title(text, size=18, bold=True, color=None, align='CENTER'):
    p = doc.add_paragraph()
    p.alignment = getattr(WD_ALIGN_PARAGRAPH, align)
    r = p.add_run(text); set_font(r, '黑体', size, bold, color)
    return p

def h(text, size=13):
    p = doc.add_paragraph()
    r = p.add_run(text); set_font(r, '黑体', size, True)
    p.paragraph_format.space_before = Pt(8); p.paragraph_format.space_after = Pt(3)
    return p

def para(text, size=11, indent=True, line=1.25):
    p = doc.add_paragraph()
    r = p.add_run(text); set_font(r, '宋体', size)
    if indent:
        p.paragraph_format.first_line_indent = Pt(22)
    p.paragraph_format.line_spacing = line
    p.paragraph_format.space_after = Pt(3)
    return p

def item(text, size=11, lead=None, line=1.25, bold_lead=False):
    """带编号/要点的段落，lead 为行首加粗词（如 '存在不足：'）"""
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Pt(22)
    p.paragraph_format.line_spacing = line
    p.paragraph_format.space_after = Pt(3)
    if lead:
        r0 = p.add_run(lead); set_font(r0, '黑体', size, bold_lead or True)
        r = p.add_run(text); set_font(r, '宋体', size)
    else:
        r = p.add_run(text); set_font(r, '宋体', size)
    return p

# ===== 标题 =====
title('2026年蓝创中心“119”消防应急疏散演练总结')
title('上海聚悦资产管理有限公司（蓝创服务中心）', size=12, bold=False, color=RGBColor(0x55,0x55,0x55))

# ===== 一、演练概况 =====
h('一、演练概况')
para('2026年11月11日14时，上海聚悦资产管理有限公司（蓝创服务中心）在蓝创中心园区组织开展了年度综合消防应急疏散演练（专项演练）。演练以1#楼为核心区，覆盖10#楼、B1及园区重点部位，联动楼宇警铃、声光报警、消防广播及所有电梯迫降。本次实际参与演练80人，含各租户员工、物业人员、访客及与会人员，紧急集合点设在1#楼南门广场。演练设总指挥杨文胜（监控中心/消防控制室）、副总指挥曹自库，下设通信联络、灭火行动、疏散引导、设备保障、安全保卫、防护救护六个行动组，共52名行动组人员按当日签到到位、分工履职。')

# ===== 二、演练组织与实施 =====
h('二、演练组织与实施')
para('14:00模拟火情触发，楼宇警铃、声光报警与消防广播启动，所有电梯迫降；通信联络组（监控中心）确认火警并报告总指挥。总指挥下达指令启动《灭火和应急疏散预案》，各行动组按职责到位：灭火行动组利用灭火器、消火栓扑救初起火灾并引导专业消防队进场；疏散引导组按“就近、老弱病残及女士优先”原则组织各楼层人员沿安全通道撤离，接访人员负责引导访客至集合点；人员疏散至1#楼南门广场后按单位/部门纵队列队（每列10人）清点人数；防护救护、安全保卫、设备保障各组同步履职，警戒组封闭园区正博路门、1#楼南北门及地库出入口；最后组织现场讲评，宣布演练结束并恢复正常秩序。')

# ===== 三、演练结果与关键数据 =====
h('三、演练结果与关键数据')
para('本次演练关键数据如下：火情触发（演练开始）为14:00；首名人员疏散到达集合点为14:02；末名人员疏散到达集合点为14:05；自火情触发至全体到达约5分钟，首到至末到历时3分钟。实际参与演练80人，全部安全疏散至1#楼南门广场集合点，经清点人数无误，无人员遗漏、无人员受伤。楼宇警铃、声光报警、消防广播、电梯迫降等联动设备均正常运行，应急响应系统整体可靠。')

# ===== 四、演练成效 =====
h('四、演练成效')
para('本次演练严格落实 GB/T 38315-2019《社会单位灭火和应急疏散预案编制及实施导则》提出的“检验预案、锻炼队伍、宣传教育、完善准备”目的，达到预期效果：一是检验了蓝创中心报警、广播、联动、疏散全流程，设备联动可靠；二是使常驻办公及经营人员进一步熟悉了紧急状态下的安全撤离路线与集合点位置；三是提升了员工自防、自救能力，验证了各行动组协同与履职能力；四是80名参演人员在5分钟内全部安全疏散到位，疏散高效有序。')

# ===== 五、存在的问题 =====
h('五、存在的问题')
para('对照方案要求及现场观察，本次演练仍暴露出以下不足，需在后续工作中重点改进：')
item('部分人员对最近安全出口不够熟悉，疏散时存在走习惯路线、未严格就近撤离的情况；个别人员疏散过程中紧张感不足，有说笑现象，未始终保持低姿前行。', lead='1. 疏散路线掌握不牢、纪律性有待加强：')
item('外来访客及与会人员对园区疏散路径不熟，依赖接访人员引导、独立性差；个别访客初期未察觉演练、反应迟缓，与方案预判的“最不利情形”相符，需纳入常态化管理。', lead='2. 访客及与会人员疏散薄弱：')
item('1#楼南门广场集合点按单位纵队列队（每列10人）清点，在人员集中到达时效率不高，列队与报到耗时偏长，影响末到人员统计时效。', lead='3. 集合点清点耗时偏长：')
item('通信联络组与部分楼层义务消防员的联络在初期存在短暂不畅，个别楼层上报人数滞后，火情信息传递的时效性和稳定性有待提升。', lead='4. 初期通信联络不够顺畅：')
item('电梯迫降后，仍有个别人员习惯性欲乘电梯；部分安全出口指示标识在强光环境下辨识度一般，现场引导与标识可视性需加强。', lead='5. 电梯禁乘与标识可视性不足：')
item('行动不便人员（孕妇、腿脚不便者）的专门协助预案在现场落实不够具体，个别单位未提前登记不能参加人员，特殊人群帮扶机制有待细化。', lead='6. 特殊人群协助机制不实：')

# ===== 六、下步改进措施 =====
h('六、下步改进措施')
para('针对上述问题，制定以下整改措施，明确责任、限期闭环：')
item('开展楼层疏散路线专项培训与现场走线，在各楼层张贴“最近安全出口”示意图，定期组织“盲走”演练提升就近撤离意识；重申疏散纪律（严禁奔跑推挤、保持低姿、火警禁乘电梯），将纪律要求纳入入职与日常安全教育。', lead='1. 强化路线培训与疏散纪律：')
item('将访客疏散纳入常态化管理：接访人员须在访客到达时即告知疏散路线与集合点；园区入口、电梯厅增设临时疏散指引；重要会议前向与会人员做简短安全告知，消除“最不利情形”隐患。', lead='2. 固化访客疏散管理：')
item('优化集合点清点流程，采用“单位—楼层—人数”三级快速报到加对讲机即时上报，配置防噪扩音与分组标识牌，缩短列队清点时间，确保末到人员统计及时准确。', lead='3. 优化集合点清点流程：')
item('梳理通信联络链路，明确各楼层义务消防员为第一报告人，配齐对讲设备并开展呼点演练，确保火情信息在30秒内上报指挥部，杜绝上报滞后。', lead='4. 畅通通信联络链路：')
item('加固电梯迫降后的现场值守与警示，在电梯厅增设“火警禁用电梯”明显标识；对辨识度低的安全出口标识全面排查更换，提升可视性。', lead='5. 加强电梯值守与标识整治：')
item('完善特殊人群协助机制，各单位提前报送行动不便人员清单并指定协助人，预案中明确“一对一”帮扶与自愿参加原则，做到底数清、有人管。', lead='6. 细化特殊人群帮扶：')
item('依据 GB/T 38315-2019 及本次评估，及时修订蓝创中心《灭火和应急疏散预案》，将问题清单纳入闭环整改台账，逐项明确责任人、整改措施与完成期限；下半年再组织一次演练验证改进成效。', lead='7. 修订预案并闭环整改：')

# ===== 七、演练结论 =====
h('七、演练结论')
para('本次“119”消防应急疏散演练组织周密、指挥顺畅、行动组履职到位，80名参演人员在火情触发后5分钟内全部安全疏散至指定集合点，无人员遗漏、无人员受伤，设备联动正常，达到了检验预案、锻炼队伍、宣传教育、完善准备的预期目的。演练符合《消防法》及公安部61号令要求，满足消防安全重点单位至少每半年组织一次灭火和应急疏散演练的规定。建议严格落实上述改进措施，并依据评估结果与整改台账及时修订预案，持续提升园区应急处置能力。')

# ===== 落款 =====
sign = doc.add_paragraph(); sign.alignment = WD_ALIGN_PARAGRAPH.RIGHT
r = sign.add_run('\n上海聚悦资产管理有限公司（蓝创服务中心）\n2026年11月11日')
set_font(r, '宋体', 11)

att = doc.add_paragraph(); att.paragraph_format.space_before = Pt(6)
r = att.add_run('附件：签到与疏散统计表、计时记录、评估报告、问题整改台账、照片影像等一并归档备查。')
set_font(r, '宋体', 9.5, color=RGBColor(0x66,0x66,0x66))

out = r'D:\Claw\2026年蓝创中心119消防应急疏散演练总结_无表版.docx'
doc.save(out)
print('saved:', out)
