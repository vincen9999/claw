import docx

p = 'E:/共享及知识库/环境管理/绿化施工期养护监管/报告/蓝创中心绿化施工期养护监管报告（2026年9月）.docx'
d = docx.Document(p)

# (旧片段 -> 新片段)；顺序无关，均为唯一片段
repl = [
    ("现场管理：聚悦管理",
     "物业服务单位：上海聚悦资产管理有限公司　｜　绿化养护单位：上海颍林景观工程有限公司　｜　甲方：上海临港奉贤经济发展有限公司"),
    ("现场管理单位为聚悦管理",
     "物业服务单位为上海聚悦资产管理有限公司，绿化养护单位为上海颍林景观工程有限公司，甲方为上海临港奉贤经济发展有限公司"),
    ("现场管理单位（聚悦管理）",
     "物业服务单位（上海聚悦资产管理有限公司）"),
    ("现场管理/养护单位",
     "绿化养护单位（上海颍林景观工程有限公司）"),
    ("由管理单位组织复查验收",
     "由物业服务单位（上海聚悦资产管理有限公司）组织复查验收，甲方（上海临港奉贤经济发展有限公司）参与监督"),
]

def apply(obj):
    if obj.text:
        new = obj.text
        for old, nw in repl:
            if old in new:
                new = new.replace(old, nw)
        if new != obj.text:
            obj.text = new
            return True
    return False

n_para = sum(apply(par) for par in d.paragraphs)
n_cell = 0
for t in d.tables:
    for row in t.rows:
        for cell in row.cells:
            if apply(cell):
                n_cell += 1

d.save(p)
print('段落替换:', n_para, '表格单元格替换:', n_cell)
