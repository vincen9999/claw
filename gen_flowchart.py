# -*- coding: utf-8 -*-
import os
from PIL import Image, ImageDraw, ImageFont

def font(size, bold=False):
    cands = [
        r"C:\Windows\Fonts\msyhbd.ttc" if bold else r"C:\Windows\Fonts\msyh.ttc",
        r"C:\Windows\Fonts\msyh.ttc",
        r"C:\Windows\Fonts\simhei.ttf",
        r"C:\Windows\Fonts\simsun.ttc",
    ]
    for c in cands:
        if os.path.exists(c):
            try:
                return ImageFont.truetype(c, size)
            except Exception:
                continue
    return ImageFont.load_default()

W = 1280
margin_x = 90
box_w = W - 2 * margin_x
box_h = 84
gap = 54
title_h = 150
footnote_h = 92

steps = [
    ("1", "安装上位机软件（电梯多媒体发布系统）"),
    ("2", "设置电脑本地 IP（与控制器同一网段）"),
    ("3", "用网线连接控制器 / 红点屏，确认链路指示灯闪烁"),
    ("4", "控制器端：取消“自动获取IP地址”，服务器IP = 电脑IP，点“应用设置”"),
    ("5", "浏览器访问上位机：127.0.0.1:8989/mps 或  <IP>:8989/mps-t/"),
    ("6", "确认控制器连接状态 = 绿色（已连接）"),
    ("7", "上传媒体素材：图片 / 视频 / 音频"),
    ("8", "编辑显示内容：图片组 / 视频组 / 音频 / 背景 / 滚动字幕"),
    ("9", "下载 / 下发到控制器"),
    ("10", "控制器重启 → 验证显示效果"),
    ("11", "导出媒体素材包（备份界面 / 素材）"),
]

n = len(steps)
H = title_h + n * box_h + (n - 1) * gap + footnote_h

img = Image.new("RGB", (W, H), "#FFFFFF")
d = ImageDraw.Draw(img)

f_title = font(44, bold=True)
f_sub = font(24)
f_node = font(27, bold=False)
f_num = font(28, bold=True)
f_note = font(23)

# Title band
d.rectangle([0, 0, W, title_h - 24], fill="#0B3D91")
d.text((W/2, 56), "电梯多媒体（EMIDS）调试总流程", font=f_title, fill="#FFFFFF", anchor="mm")
d.text((W/2, title_h - 52), "上海三菱电梯 · 多媒体信息显示系统（EMIDS）", font=f_sub, fill="#C9D8F0", anchor="mm")

y = title_h
for i, (num, text) in enumerate(steps):
    # connector arrow
    if i > 0:
        cx = W / 2
        d.line([(cx, y - gap + 6), (cx, y - 10)], fill="#7A93B8", width=4)
        d.polygon([(cx - 10, y - 12), (cx + 10, y - 12), (cx, y + 2)], fill="#7A93B8")
    # box
    box = [margin_x, y, margin_x + box_w, y + box_h]
    # highlight key nodes
    if num in ("4", "6", "9"):
        fill, border = "#FFF4D6", "#E8A33D"
    else:
        fill, border = "#EAF2FF", "#2F6FE0"
    d.rounded_rectangle(box, radius=16, fill=fill, outline=border, width=3)
    # number badge
    bcx, bcy, r = margin_x + 52, y + box_h/2, 27
    d.ellipse([bcx - r, bcy - r, bcx + r, bcy + r], fill=border)
    d.text((bcx, bcy), num, font=f_num, fill="#FFFFFF", anchor="mm")
    # text
    d.text((margin_x + 100, y + box_h/2), text, font=f_node, fill="#1A2B4A", anchor="lm")
    y += box_h + gap

# footnote
fy = H - footnote_h + 8
d.rounded_rectangle([margin_x, fy, margin_x + box_w, fy + footnote_h - 22], radius=12,
                    fill="#FDECEC", outline="#E06B6B", width=2)
d.text((margin_x + 24, fy + (footnote_h - 22)/2),
       "红色=未连接：回到步骤2/3 检查网段、IP、网线与 ping 连通性",
       font=f_note, fill="#B23B3B", anchor="lm")

out = r"D:\Claw\emids_flowchart.png"
img.save(out, "PNG")
print("SAVED", out, img.size)
