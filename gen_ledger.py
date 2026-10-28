# -*- coding: utf-8 -*-
"""生成绿化问题整改台账模板（含数据验证下拉）"""
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation

wb = Workbook()
ws = wb.active
ws.title = "绿化问题整改台账"

headers = ["序号", "图片编号", "拍摄位置/区域", "问题类别", "问题描述",
           "严重程度", "整改要求", "责任单位", "整改期限", "复核结果", "备注"]
widths = [6, 16, 18, 16, 34, 9, 36, 14, 14, 11, 16]

head_fill = PatternFill("solid", fgColor="3B6D11")
head_font = Font(name="微软雅黑", bold=True, color="FFFFFF", size=10.5)
thin = Side(style="thin", color="CCCCCC")
border = Border(left=thin, right=thin, top=thin, bottom=thin)

for c, (h, w) in enumerate(zip(headers, widths), 1):
    cell = ws.cell(row=1, column=c, value=h)
    cell.fill = head_fill
    cell.font = head_font
    cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    cell.border = border
    ws.column_dimensions[cell.column_letter].width = w

# 预填 20 行空行（含边框）
body_font = Font(name="微软雅黑", size=10)
for r in range(2, 22):
    for c in range(1, len(headers) + 1):
        cell = ws.cell(row=r, column=c)
        cell.border = border
        cell.font = body_font
        cell.alignment = Alignment(vertical="center", wrap_text=True)
    ws.cell(row=r, column=1, value=r - 1)

# 数据验证
cat = ",".join(["苗木枯死/缺株", "斑秃露土", "杂草丛生", "病虫害",
               "修剪不当", "旱涝(浇水不足/积水)", "支撑设施破损",
               "垃圾杂物", "长势衰弱", "其他"])
dv_cat = DataValidation(type="list", formula1='"%s"' % cat, allow_blank=True)
dv_sev = DataValidation(type="list", formula1='"轻,中,重"', allow_blank=True)
dv_review = DataValidation(type="list", formula1='"未复核,整改中,已整改,未通过"', allow_blank=True)
for dv in (dv_cat, dv_sev, dv_review):
    ws.add_data_validation(dv)
dv_cat.add("D2:D21")
dv_sev.add("F2:F21")
dv_review.add("J2:J21")

ws.freeze_panes = "A2"

out = r"E:\共享及知识库\环境管理\绿化施工期养护监管\绿化问题整改台账.xlsx"
wb.save(out)
print("SAVED:", out)
