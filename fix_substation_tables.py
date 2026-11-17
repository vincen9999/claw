# -*- coding: utf-8 -*-
"""Fix table header/body misalignment: set fixed layout + correct gridCol widths."""
from docx import Document
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'

def set_table_fixed(t):
    tbl = t._tbl
    # ---- 1. fixed layout (child of tblPr) ----
    tblPr = tbl.find(W + 'tblPr')
    if tblPr is None:
        tblPr = OxmlElement('w:tblPr'); tbl.insert(0, tblPr)
    lay = tblPr.find(W + 'tblLayout')
    if lay is None:
        lay = OxmlElement('w:tblLayout'); tblPr.append(lay)
    lay.set(W + 'type', 'fixed')

    # ---- 2. per-column widths from first row tcW ----
    widths = []
    for c in t.rows[0].cells:
        tcw = c._tc.find(W + 'tcPr/' + W + 'tcW')
        w = tcw.get(W + 'w') if tcw is not None else None
        widths.append(int(w) if w else 0)
    if sum(widths) == 0:  # fallback: equal from existing gridCols
        grid0 = tbl.find(W + 'tblGrid')
        if grid0 is not None:
            widths = [int(g.get(W + 'w') or 0) for g in grid0.findall(W + 'gridCol')]

    # ---- 3. rebuild tblGrid gridCols ----
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

    # ---- 4. table width = sum of columns, and enforce each cell tcW ----
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
            tcW.set(W + 'type', 'dxa')
            tcW.set(W + 'w', str(widths[i]))

OUT = r'D:\Claw\35kV_10kV变电站日常安全管理检查标准_修正.docx'
doc = Document(r'D:\Claw\35kV_10kV变电站日常安全管理检查标准.docx')
for t in doc.tables:
    set_table_fixed(t)
doc.save(OUT)
print('patched', len(doc.tables), 'tables ->', OUT)
