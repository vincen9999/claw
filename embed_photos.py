import os, io, shutil
import openpyxl
from openpyxl.utils import get_column_letter
from PIL import Image as PILImage

base = 'E:/共享及知识库/环境管理/绿化施工期养护监管'
ledger = os.path.join(base, '报告', '绿化问题整改台账-2026年9月.xlsx')
photo_dir = os.path.join(base, '现场图片')
thumb_dir = 'D:/Claw/_thumbs'
os.makedirs(thumb_dir, exist_ok=True)

wb = openpyxl.load_workbook(ledger)
ws = wb.active
print('SHEET:', ws.title, 'ROWS:', ws.max_row)

# 备份原文件
backup = ledger.replace('.xlsx', '_bak.xlsx')
if not os.path.exists(backup):
    shutil.copyfile(ledger, backup)
    print('已备份原台账 ->', os.path.basename(backup))

files = [f for f in os.listdir(photo_dir)
         if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

def find_file(no, loc):
    cands = [f for f in files if f[:-4].endswith(no)]
    if not cands:
        return None
    if len(cands) == 1:
        return cands[0]
    for f in cands:               # 同号多文件时按位置精确匹配
        if loc in f:
            return f
    return cands[0]

# 新增“现场照片”列
PHOTO_COL = 12
ws.cell(1, PHOTO_COL, '现场照片')
ws.column_dimensions[get_column_letter(PHOTO_COL)].width = 24

matched = 0
unmatched = []
for r in range(2, ws.max_row + 1):
    no = str(ws.cell(r, 2).value).zfill(3)
    loc = str(ws.cell(r, 3).value)
    fn = find_file(no, loc)
    if not fn:
        unmatched.append((r, no, loc))
        continue
    src = os.path.join(photo_dir, fn)
    # 缩略图：宽 480，保持比例
    im = PILImage.open(src)
    im = im.convert('RGB')
    w, h = im.size
    tw = 480
    th = int(h * tw / w)
    im = im.resize((tw, th), PILImage.LANCZOS)
    tpath = os.path.join(thumb_dir, f'{no}.jpg')
    im.save(tpath, 'JPEG', quality=82)
    # 嵌入
    img = openpyxl.drawing.image.Image(tpath)
    disp_w = 160
    disp_h = int(th * disp_w / tw)
    img.width = disp_w
    img.height = disp_h
    ws.add_image(img, f'{get_column_letter(PHOTO_COL)}{r}')
    ws.row_dimensions[r].height = max(110, disp_h + 14)
    matched += 1

print(f'已匹配并嵌入: {matched} / {ws.max_row - 1}')
print('未匹配:', unmatched if unmatched else '无')

try:
    wb.save(ledger)
    print('已保存到原台账文件:', ledger)
except PermissionError:
    newp = ledger.replace('.xlsx', '_含照片.xlsx')
    wb.save(newp)
    print('原文件被占用，已另存为新文件:', newp)

shutil.rmtree(thumb_dir, ignore_errors=True)
print('DONE')
