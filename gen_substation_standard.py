# -*- coding: utf-8 -*-
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

EAST = '宋体'
HEI = '微软雅黑'

def set_east(run, font=EAST):
    run.font.name = font
    rPr = run._element.get_or_add_rPr()
    rFonts = rPr.get_or_add_rFonts()
    rFonts.set(qn('w:eastAsia'), font)
    rFonts.set(qn('w:ascii'), font)
    rFonts.set(qn('w:hAnsi'), font)

def shade(cell, hexcolor):
    tcPr = cell._tc.get_or_add_tcPr()
    sh = OxmlElement('w:shd')
    sh.set(qn('w:val'), 'clear'); sh.set(qn('w:color'), 'auto'); sh.set(qn('w:fill'), hexcolor)
    tcPr.append(sh)

def set_cell(cell, text, bold=False, size=9, color=None, fill=None, align='left'):
    cell.text = ''
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT if align=='left' else (WD_ALIGN_PARAGRAPH.CENTER if align=='center' else WD_ALIGN_PARAGRAPH.JUSTIFY)
    p.paragraph_format.space_after = Pt(1); p.paragraph_format.space_before = Pt(1)
    r = p.add_run(text)
    r.bold = bold; r.font.size = Pt(size)
    set_east(r)
    if color: r.font.color.rgb = RGBColor(*color)
    if fill: shade(cell, fill)
    return cell

def header_row(table, headers, widths, fill='1F4E79'):
    hdr = table.rows[0].cells
    for i, h in enumerate(headers):
        set_cell(hdr[i], h, bold=True, size=9, color=(0xFF,0xFF,0xFF), align='center', fill=fill)
        hdr[i].width = Cm(widths[i])
    # set col widths on all cells
    for row in table.rows:
        for i, w in enumerate(widths):
            row.cells[i].width = Cm(w)

def add_table(headers, widths, data_rows, fill='1F4E79', alt='F2F6FB'):
    t = doc.add_table(rows=1, cols=len(headers))
    t.style = 'Table Grid'
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    header_row(t, headers, widths, fill)
    for ri, row in enumerate(data_rows):
        cells = t.add_row().cells
        for ci, val in enumerate(row):
            set_cell(cells[ci], val, size=9, align='center' if ci==0 else 'left')
            if alt and ri % 2 == 1:
                shade(cells[ci], alt)
    return t

def H1(text):
    p = doc.add_heading(level=1)
    r = p.add_run(text); r.font.size = Pt(14); r.bold=True; set_east(r, HEI); r.font.color.rgb = RGBColor(0x1F,0x4E,0x79)
    return p

def H2(text):
    p = doc.add_heading(level=2)
    r = p.add_run(text); r.font.size = Pt(12); r.bold=True; set_east(r, HEI); r.font.color.rgb = RGBColor(0x2E,0x5C,0x8A)
    return p

def para(text, size=10, bold=False, color=None, justify=True):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY if justify else WD_ALIGN_PARAGRAPH.LEFT
    r = p.add_run(text); r.font.size = Pt(size); r.bold = bold; set_east(r)
    if color: r.font.color.rgb = RGBColor(*color)
    return p

def bullet(text, size=10):
    p = doc.add_paragraph(style='List Bullet')
    r = p.add_run(text); r.font.size = Pt(size); set_east(r)
    return p

doc = Document()

# default font
style = doc.styles['Normal']
style.font.name = EAST
style.font.size = Pt(10)
style.element.rPr.rFonts.set(qn('w:eastAsia'), EAST)

# ---- 页边距 ----
sec = doc.sections[0]
sec.top_margin = Cm(2.2); sec.bottom_margin = Cm(2.0)
sec.left_margin = Cm(2.2); sec.right_margin = Cm(2.2)

# ===== 封面标题 =====
t = doc.add_paragraph(); t.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = t.add_run('35kV、10kV 变电站\n日常安全管理检查标准'); r.bold=True; r.font.size=Pt(22); set_east(r, HEI); r.font.color.rgb = RGBColor(0x1F,0x4E,0x79)
sub = doc.add_paragraph(); sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = sub.add_run('（依据国家现行法律法规、消防与电力行业规程编制）'); r.font.size=Pt(11); set_east(r); r.font.color.rgb=RGBColor(0x66,0x66,0x66)
doc.add_paragraph()
info = doc.add_table(rows=4, cols=2); info.style='Table Grid'; info.alignment=WD_TABLE_ALIGNMENT.CENTER
for i,(k,v) in enumerate([('标准编号','Q/XXX·AQ—2026（企业自编）'),('版    本','A/0  首版'),('编 制 日 期','2026-11-06'),('适 用 范 围','35kV、10kV 变电站（含用户站、配电站）')]):
    set_cell(info.rows[i].cells[0], k, bold=True, size=10, fill='DCE6F1', align='center')
    set_cell(info.rows[i].cells[1], v, size=10)
    info.rows[i].cells[0].width=Cm(4); info.rows[i].cells[1].width=Cm(13)
doc.add_paragraph()
para('说明：本标准所列各项规定的依据均为现行有效版本（截至 2026 年 11 月）。当上级法规、标准更新时，以最新版本为准。', size=9, color=(0x88,0x44,0x00))

# ===== 一、适用范围 =====
H1('一、适用范围')
para('本标准适用于 35kV、10kV 变电站（含用户变电站、配电站、开闭所）的日常安全管理工作，用于指导、检查、评价与考核。适用于变电站运行值班、设备巡视、倒闸操作、消防管理、工器具管理、隐患排查治理及应急管理等环节。')

# ===== 二、编制依据 =====
H1('二、编制依据（现行有效）')
H2('2.1 法律、法规、规章')
add_table(['类别','名  称','文号 / 版本','施行 / 修正'],
          [2.2, 8.3, 3.8, 2.7],
          [
           ['法律','中华人民共和国安全生产法','主席令第88号（2021年修正）','2021-09-01 施行'],
           ['法律','中华人民共和国消防法','主席令第81号（2021年修正）','2021-04-29 修正'],
           ['条例','生产安全事故应急条例','国务院令第708号','2019-04-01 施行'],
           ['条例','生产安全事故报告和调查处理条例','国务院令第493号','2007-06-01 施行'],
           ['规章','电力安全生产监督管理办法','国家发改委令2015年第21号','2015-03-01 施行'],
           ['规章','电力重大事故隐患判定标准及治理监督管理规定','国家发改委令第41号','2026-07-01 施行'],
          ])
doc.add_paragraph()
H2('2.2 国家、行业标准与反事故要求')
add_table(['类别','名  称','标准号 / 文号','状态'],
          [2.0, 9.2, 3.5, 2.3],
          [
           ['国标','电力安全工作规程 发电厂和变电站电气部分','GB 26860-2011','现行'],
           ['国标','火力发电厂与变电站设计防火标准','GB 50229-2019','现行'],
           ['行标','电力设备典型消防规程','DL 5027-2015','现行'],
           ['行标','电力设备预防性试验规程','DL/T 596-2021','现行'],
           ['国标','10kV及以上电力用户变电站运行管理规范','GB/T 32893-2016','现行'],
           ['行标','变电站运行导则','DL/T 969','现行'],
           ['国标','建筑灭火器配置设计规范','GB 50140','现行'],
           ['国标','建筑设计防火规范','GB 50016（2018年版）','现行'],
           ['国标','电气装置安装工程 电气设备交接试验标准','GB 50150-2016','现行'],
           ['文件','防止电力生产事故的二十五项重点要求（2023版）','国能发安全〔2023〕22号','现行'],
           ['国标','电能质量 公用电网谐波 / 电压波动和闪变 / 三相电压不平衡','GB/T 14549、12326、15543','现行'],
          ])

# ===== 三、检查分类与频次 =====
H1('三、检查分类与频次')
add_table(['检查类别','频次 / 时机','责任主体','主要依据'],
          [2.6, 7.0, 3.4, 4.0],
          [
           ['日常巡视','每班不少于 1 次；高峰负荷、恶劣天气增加频次','当班运行人员','GB/T 32893、DL/T 969、GB 26860'],
           ['交接班检查','每班交接时共同核查','交/接班人员','GB/T 32893 6.2'],
           ['定期专项检查','每周（消防、工器具）、每月（设备、隐患）','安全员 / 站长','企业运行规程'],
           ['操作后 / 异常后特巡','倒闸操作后、设备受短路冲击或过负荷后','当班人员','GB/T 32893 6.3.3、GB 26860'],
           ['季节性检查','雷雨前、高温、严寒、防汛、防小动物','站长 / 安全员','二十五项反措2023'],
           ['保电 / 节假日检查','重大活动、节假日前后','站长','GB/T 32893 6.3.3(g)'],
          ])

# ===== 四、日常安全管理检查标准 =====
H1('四、日常安全管理检查标准')

H2('4.1 人员资质与培训')
add_table(['序号','检查项目','检查标准与要求','主要依据'],
          [1.2, 4.0, 9.0, 2.8],
          [
           ['1','持证上岗','运行、值班、倒闸操作人员须持有效特种作业（电工）操作证或相应资质，严禁无证上岗','安全生产法、GB/T 32893 5.4'],
           ['2','安规考试','在岗人员每年进行一次安全工作规程考试并合格；消防知识每年考试一次','GB 26860、DL 5027 1.0.6'],
           ['3','培训合格','新进、转岗、复岗人员须经安全培训并考试合格后方可上岗','安全生产法 第二十八条'],
           ['4','外来人员管理','外来施工 / 参观人员须登记、交待安全注意事项，并在监护下活动','GB 26860'],
          ])

H2('4.2 运行值班与交接班')
add_table(['序号','检查项目','检查标准与要求','主要依据'],
          [1.2, 4.0, 9.0, 2.8],
          [
           ['1','值守纪律','变电站应有人 24h 值守（或按规定巡维）；严格服从调度指令，不做与运行无关之事','GB/T 32893 6.1'],
           ['2','交接班','事故处理或电气操作中进行时不得交接班；交接须在交班人陪同下共同检查核对无误后签字','GB/T 32893 6.2'],
           ['3','运行记录','运行日志、设备缺陷记录、操作记录、巡视记录齐全、真实、规范','GB/T 32893'],
           ['4','录音要求','与电网有调度关系的操作、事故处理应启用录音设备并留存','GB/T 32893 6.1.3'],
          ])

H2('4.3 设备巡视与状态')
add_table(['序号','检查项目','检查标准与要求','主要依据'],
          [1.2, 4.0, 9.0, 2.8],
          [
           ['1','巡视制度','按规定的路线、定点定时巡视；发现缺陷及时记录、汇报、处理','DL/T 969、GB/T 32893 6.3'],
           ['2','变压器（室）','油位、油温正常；无异常声响、渗漏；呼吸器硅胶不过潮；冷却系统运行正常；有载分接开关位置正确','DL/T 596、GB 26860'],
           ['3','开关柜 / 断路器','SF6 气体压力正常（或真空断路器完好）；柜体无异响、过热；五防锁具完好','GB 26860、二十五项反措2023'],
           ['4','电力电缆','终端无放电、过热；电缆沟（隧道）无积水、封堵严密；电缆无破损','DL 5027 10.5、GB 50229'],
           ['5','互感器、避雷器','瓷套清洁、无裂纹放电；避雷器计数器、在线监测正常；接地可靠','DL/T 596'],
           ['6','红外测温','高峰负荷时对设备接头、刀闸、电缆终端测温，发现过热及时处理','GB 26860'],
           ['7','异常特巡','过电压 / 短路冲击后、过负荷、新投运、检修后、恶劣天气、保电等应增加巡视','GB/T 32893 6.3.3'],
          ])

H2('4.4 倒闸操作与"五防"')
add_table(['序号','检查项目','检查标准与要求','主要依据'],
          [1.2, 4.0, 9.0, 2.8],
          [
           ['1','操作票','倒闸操作必须填用操作票（一个任务一张票）；监护操作须两人进行','GB 26860 5.3'],
           ['2','操作顺序','停电拉闸：断路器→负荷侧隔离开关→电源侧隔离开关；送电相反；严禁带负荷拉合隔离开关','GB 26860'],
           ['3','"五防"装置','防误闭锁装置完好、投运；严禁擅自退出；停用须履行批准手续并限期修复','二十五项反措2023 第3部分'],
           ['4','技术措施','停电、验电、装设接地线、悬挂标示牌、装设遮栏（围栏）逐项落实','GB 26860'],
           ['5','解锁钥匙','解锁钥匙（应急钥匙）封存、编号、专用，使用须审批并登记','GB 26860、国家电网防误规定'],
          ])

H2('4.5 消防安全管理')
add_table(['序号','检查项目','检查标准与要求','主要依据'],
          [1.2, 4.0, 9.0, 2.8],
          [
           ['1','消防设施','灭火器（按 GB 50140 配置）、火灾自动报警、消防给水、应急照明完好有效，定期巡检、换药、检测','DL 5027、GB 50229、GB 50140'],
           ['2','防火封堵','电缆孔洞、盘柜、穿墙套管封堵严密，使用阻燃材料；电缆通道防火分隔到位','GB 50229、DL 5027 10.5'],
           ['3','动火管理','动火须办理动火票，落实监护、隔离、清理、灭火器材；禁止动火条件不得作业','DL 5027 第5章'],
           ['4','疏散与通道','安全出口、疏散通道、消防车通道畅通，严禁锁闭、堆物','消防法、GB 50016'],
           ['5','禁放物品','控制室、配电室、电缆夹层严禁存放易燃易爆物品','DL 5027 6'],
           ['6','蓄电池室','通风良好，防爆电气；氢（酸）气泄漏监测与报警正常','DL 5027 10.6'],
          ])

H2('4.6 安全工器具管理')
add_table(['序号','检查项目','检查标准与要求','主要依据'],
          [1.2, 4.0, 9.0, 2.8],
          [
           ['1','配置齐全','绝缘手套、绝缘靴、验电器、接地线（编号）、绝缘杆、标示牌、遮栏 / 围栏齐全','GB 26860、DL 5027'],
           ['2','定期试验','工器具按周期试验合格并在有效期内；超期、不合格一律停用','GB 26860、DL/T 596'],
           ['3','存放管理','定置存放、干燥清洁，不与一般工器具混放；使用前检查外观','GB 26860'],
          ])

H2('4.7 环境与辅助设施')
add_table(['序号','检查项目','检查标准与要求','主要依据'],
          [1.2, 4.0, 9.0, 2.8],
          [
           ['1','防小动物','挡鼠板、防鼠网、通风百叶、电缆沟封堵齐全有效；站内无鼠害痕迹','二十五项反措2023'],
           ['2','通风 / 温湿度','开关室、电容器室、电缆室通风良好；温湿度在设备允许范围','运行规程'],
           ['3','防汛 / 排水','排水沟畅通，防汛沙袋、抽水泵、挡水板齐备并处于可用状态','二十五项反措2023'],
           ['4','照明 / 标识','事故照明、正常照明完好；设备双重名称、安全警示牌、模拟图板清晰准确','GB 26860'],
           ['5','接地与防雷','接地网、设备接地可靠；避雷器、避雷带完好；接地电阻定期检测合格','DL/T 596'],
          ])

H2('4.8 二次系统与电力监控')
add_table(['序号','检查项目','检查标准与要求','主要依据'],
          [1.2, 4.0, 9.0, 2.8],
          [
           ['1','保护投运','继电保护、安全自动装置投运状态与定值不得擅自更改；涉网保护须按调度要求执行','GB/T 32893 6.5'],
           ['2','告警处置','保护、自动化、通信、监控告警或动作后，立即汇报调度并查明原因','GB/T 32893 6.5.3'],
           ['3','监控安防','电力监控系统（二次系统）落实安全防护，严禁违规外联、越权操作','国家发改委第41号、GB 26860'],
          ])

H2('4.9 隐患治理与闭环')
add_table(['序号','检查项目','检查标准与要求','主要依据'],
          [1.2, 4.0, 9.0, 2.8],
          [
           ['1','排查建档','建立隐患排查治理台账，日常排查发现的问题登记、分级','国家发改委第41号令'],
           ['2','一般隐患','即查即改；不能立即整改的，落实责任人、措施、期限并跟踪','国家能源局隐患治理规定'],
           ['3','重大隐患','立即采取管控措施并上报；挂牌督办、限期治理、验收销号，闭环管理','国家发改委第41号令'],
           ['4','判定标准','重大事故隐患按第41号令明确的判定情形（设备设施、监控、管理等领域）执行','国家发改委第41号令'],
          ])

H2('4.10 应急管理与事故报告')
add_table(['序号','检查项目','检查标准与要求','主要依据'],
          [1.2, 4.0, 9.0, 2.8],
          [
           ['1','应急预案','编制触电、火灾、全站失电、防汛等现场处置方案，并备案','安全生产法、应急条例'],
           ['2','演练与物资','定期演练（每年不少于 1 次）；应急物资、通讯工具齐备可用','应急条例、DL 5027'],
           ['3','事故报告','发生事故（事件）按规定时限上报，保护现场、如实报告，不得瞒报谎报','安全生产法、493号令'],
          ])

# ===== 五、隐患分级与闭环 =====
H1('五、隐患分级与闭环管理')
para('依据《电力重大事故隐患判定标准及治理监督管理规定》（国家发改委令第41号，2026-07-01 施行），隐患实行分级闭环：')
bullet('一般隐患：由电站立即组织整改或落实防范措施，明确责任人、措施和期限，整改后确认销项。')
bullet('重大隐患：立即采取停产停业、停止运行、撤离人员等管控措施；按规定向监管（派出）机构和上级报告；挂牌督办、限期治理、评估验收、销号闭环，实行"排查—报告—治理—评估—销号"全链条管理。')
bullet('重大隐患判定严格按第41号令公布的判定情形执行（涵盖电力设备设施、电力监控系统、电力企业安全管理等）。')
bullet('隐患治理情况应如实记录并向从业人员通报；主要负责人对重大隐患排查治理负首要责任。')

# ===== 六、检查记录与考核 =====
H1('六、检查记录与考核')
bullet('每次检查应填写《变电站日常安全检查记录表》（见附录 A），检查人、受检人签字确认。')
bullet('检查结论分"合格 / 限期整改 / 不合格"；限期整改项应在规定期限内复查闭环。')
bullet('未按本标准执行、隐患逾期未改或瞒报事故的，按安全生产责任制考核问责；构成犯罪的，依法追究刑事责任。')

# ===== 附录 A =====
doc.add_page_break()
H1('附录 A　变电站日常安全检查记录表（模板）')
add_table(['检查日期','检查类别','检查人','受检人'],
          [4.2, 4.2, 4.2, 4.2],
          [['　年　月　日','','','']])
doc.add_paragraph()
add_table(['序号','检查项目','检查情况（符合 / 问题描述）','整改要求 / 期限','确认'],
          [1.4, 5.0, 5.4, 3.0, 2.2],
          [['1','人员资质与培训','','',''],
           ['2','运行值班与交接班','','',''],
           ['3','设备巡视与状态','','',''],
           ['4','倒闸操作与五防','','',''],
           ['5','消防安全管理','','',''],
           ['6','安全工器具','','',''],
           ['7','环境与辅助设施','','',''],
           ['8','二次系统与监控','','',''],
           ['9','隐患治理闭环','','',''],
           ['10','应急管理与报告','','','']])
doc.add_paragraph()
para('备注：本表与正文"四、日常安全管理检查标准"各章节对应使用；发现重大隐患须单独填报并按第41号令上报。', size=9, color=(0x88,0x44,0x00))

# ===== 表格固定列宽：避免表头与表体因自动(Autofit)布局错位 =====
W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
def _fix_table_layout():
    for t in doc.tables:
        tbl = t._tbl
        tblPr = tbl.find(W + 'tblPr')
        if tblPr is None:
            tblPr = OxmlElement('w:tblPr'); tbl.insert(0, tblPr)
        lay = tblPr.find(W + 'tblLayout')
        if lay is None:
            lay = OxmlElement('w:tblLayout'); tblPr.append(lay)
        lay.set(W + 'type', 'fixed')
        # 按首行 tcW 确定每列宽度
        widths = []
        for c in t.rows[0].cells:
            tcw = c._tc.find(W + 'tcPr/' + W + 'tcW')
            w = tcw.get(W + 'w') if tcw is not None else None
            widths.append(int(w) if w else 0)
        if sum(widths) == 0:
            grid0 = tbl.find(W + 'tblGrid')
            if grid0 is not None:
                widths = [int(g.get(W + 'w') or 0) for g in grid0.findall(W + 'gridCol')]
        grid = tbl.find(W + 'tblGrid')
        if grid is None:
            grid = OxmlElement('w:tblGrid'); tbl.append(grid)
        for gc in grid.findall(W + 'gridCol'):
            grid.remove(gc)
        for w in widths:
            gc = OxmlElement('w:gridCol')
            if w:
                gc.set(W + 'w', str(w))
            grid.append(gc)
        total = sum(w for w in widths if w)
        tw = tblPr.find(W + 'tblW')
        if tw is None:
            tw = OxmlElement('w:tblW'); tblPr.append(tw)
        tw.set(W + 'type', 'dxa'); tw.set(W + 'w', str(total))
        for row in t.rows:
            for i, c in enumerate(row.cells):
                if i >= len(widths):
                    continue
                tcPr = c._tc.get_or_add_tcPr()
                tcW = tcPr.find(W + 'tcW')
                if tcW is None:
                    tcW = OxmlElement('w:tcW'); tcPr.append(tcW)
                tcW.set(W + 'type', 'dxa'); tcW.set(W + 'w', str(widths[i]))
_fix_table_layout()

out = r'D:\Claw\35kV_10kV变电站日常安全管理检查标准.docx'
doc.save(out)
print('saved:', out)
