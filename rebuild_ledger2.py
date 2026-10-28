import os, shutil, copy
import openpyxl
from openpyxl.utils import get_column_letter
from PIL import Image as PILImage

base = 'E:/共享及知识库/环境管理/绿化施工期养护监管'
bak = os.path.join(base, '报告', '绿化问题整改台账-2026年9月_bak.xlsx')
ledger = os.path.join(base, '报告', '绿化问题整改台账-2026年9月.xlsx')
photo_dir = os.path.join(base, '现场图片')
thumb_dir = 'D:/Claw/_thumbs'
os.makedirs(thumb_dir, exist_ok=True)

RESP_COL = 8          # 责任单位
NEW_UNIT = '颍林景观'

src = openpyxl.load_workbook(bak)
sws = src.active
# 确认列标题
assert sws.cell(1, RESP_COL).value == '责任单位', sws.cell(1, RESP_COL).value

dst = openpyxl.Workbook()
dws = dst.active
dws.title = sws.title

for col, dim in sws.column_dimensions.items():
    dws.column_dimensions[col].width = dim.width
for r, dim in sws.row_dimensions.items():
    if dim.height:
        dws.row_dimensions[r].height = dim.height

changed = 0
for r in range(1, sws.max_row + 1):
    for c in range(1, sws.max_column + 1):
        sc = sws.cell(r, c)
        val = sc.value
        if r > 1 and c == RESP_COL:
            val = NEW_UNIT
            changed += 1
        dc = dws.cell(r, c, val)
        dc.font = copy.copy(sc.font)
        dc.fill = copy.copy(sc.fill)
        dc.border = copy.copy(sc.border)
        dc.alignment = copy.copy(sc.alignment)
        dc.number_format = sc.number_format

for dv in sws.data_validations.dataValidation:
    dws.add_data_validation(dv)

files = [f for f in os.listdir(photo_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
def find_file(no, loc):
    cands = [f for f in files if f[:-4].endswith(no)]
    if len(cands) == 1:
        return cands[0]
    for f in cands:
        if loc in f:
            return f
    return cands[0] if cands else None

PHOTO_COL = sws.max_column + 1
dws.cell(1, PHOTO_COL, '现场照片')
dws.column_dimensions[get_column_letter(PHOTO_COL)].width = 24

matched = 0
for r in range(2, sws.max_row + 1):
    no = str(sws.cell(r, 2).value).zfill(3)
    loc = str(sws.cell(r, 3).value)
    fn = find_file(no, loc)
    if not fn:
        continue
    im = PILImage.open(os.path.join(photo_dir, fn)).convert('RGB')
    w, h = im.size
    tw = 480
    th = int(h * tw / w)
    im = im.resize((tw, th), PILImage.LANCZOS)
    tpath = os.path.join(thumb_dir, f'{no}.jpg')
    im.save(tpath, 'JPEG', quality=82)
    img = openpyxl.drawing.image.Image(tpath)
    disp_w, disp_h = 160, int(th * 160 / tw)
    img.width, img.height = disp_w, disp_h
    dws.add_image(img, f'{get_column_letter(PHOTO_COL)}{r}')
    dws.row_dimensions[r].height = max(dws.row_dimensions[r].height or 110, disp_h + 14)
    matched += 1

print('责任单位已改:', changed, '张图嵌入:', matched)
dst.save(ledger)
shutil.rmtree(thumb_dir, ignore_errors=True)
print('saved ->', ledger)
