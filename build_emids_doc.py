# -*- coding: utf-8 -*-
import json, re, subprocess, sys, os

SDK = r"C:\Program Files\WorkBuddy\resources\app.asar.unpacked\resources\plugins\workbuddy-builtin\skills\tencent-local-office-edit\edsdk.py"
PY = sys.executable

def raw(args):
    p = subprocess.run([PY, SDK] + args, capture_output=True, text=True, encoding="utf-8", errors="replace")
    return p.stdout, p.stderr

def call(tool, params):
    out, err = raw(["call", tool, "--json", json.dumps(params, ensure_ascii=False)])
    lines = [l for l in out.splitlines() if l.strip().startswith("{")]
    if lines:
        res = json.loads(lines[-1])
        if res.get("ok") is False:
            raise RuntimeError(f"{tool} failed: {res}")
        return res
    # 部分工具（如 save_file）只返回纯文本成功信息，无 JSON
    if "saved" in out or "ok" in out.lower():
        return {"ok": True, "message": out.strip()}
    raise RuntimeError(f"{tool} -> no json\nOUT:{out}\nERR:{err}")

# 1) create fresh doc
out, err = raw(["call", "create_doc", "--json", "{}"])
m = re.search(r"file_id=([^,\s]+)", out)
if not m:
    raise RuntimeError("create_doc parse failed: " + out + " | " + err)
FID = m.group(1)
print("FID =", FID)

MED = "D:/Claw/docx_media/"
FLOW = "D:/Claw/emids_flowchart.png"

# ---------- content ----------
S_TITLE = """# 电梯多媒体（EMIDS）调试要点 · 图文操作手册

**适用系统**：上海三菱电梯 多媒体信息显示系统 EMIDS（Elevator Multimedia Information Display System）

**软件版本**：系统 SYSTEM_JS616_v6.1.8　/　程序 SOFTWARE_JS616_v1.2.5

**编制说明**：本手册在原《多媒体调试要点》基础上，结合官方《新 EMIDS 上位机软件用户手册》（系统调试篇 + 上位机编辑篇）补充细化，并配全流程框图与界面截图，使操作步骤更清晰、更完整。
"""

S_SEC1 = """## 一、系统简介

EMIDS 是上海三菱电梯为电梯轿厢开发的多媒体信息显示系统，可在轿厢内发布文本信息、播放音视频、同步显示楼层等。

- **组网方式**：离线型——用笔记本电脑对单台显示系统写入信息；联网型——通过远程服务器 / 局域网 / 无线 AP / 轿顶多媒体控制器，实现文本实时发布、播放内容远程下载、参数远程设定与集中管理。
- **容量**：1 台远程服务器最多可管理 **255 台**多媒体显示系统。
- **链路**：监控室服务器 ↔ 电梯机房 走局域网；机房 ↔ 轿厢 走无线传输（抗干扰，不受提升高度限制）。
- **显示尺寸**：10.4″ / 12.1″ / 15″；安装方式：内嵌式、壁挂式。
- **主要功能**：文本信息发布、电梯信息显示、音视频文件播放、楼层同步显示、静态图片显示、日期时钟显示。
"""

S_SEC2 = """## 二、调试总流程

整个调试按"安装软件 → 配网 → 接通 → 屏端设服务器IP → 登录上位机 → 确认连接 → 上传素材 → 编辑内容 → 下发 → 验证备份"推进，见下图：
"""

S_SEC3 = """## 三、调试前准备

### 3.1 工具与材料

- 笔记本电脑（安装上位机软件）
- 网线（连接控制器 / 红点屏与电脑）
- 鼠标（USB 接入控制板 CN30，用于屏端设置）
- 可选：以太网转换器（机房 ↔ 轿顶链路测试）

### 3.2 账号与登录信息

- 上位机发布系统网址：本机 `http://127.0.0.1:8989/mps`；远程 `http://<多媒体IP>:8989/mps-t/`
- 管理员账号：**smec30**　密码：**200236**
- 超级管理员：**admin**　密码：**111111**
- 浏览器建议：火狐 / 谷歌；使用 IE 需 IE9 以上

### 3.3 网段规划（关键）

- 电脑 IP 与控制器 IP **必须在同一网段**；
- **服务器 IP = 安装上位机电脑的 IP**（务必一致，否则控制器显示"服务器连：离线"）。
"""

S_STEP12 = """## 四、分步操作流程

### 步骤 1　安装上位机软件

按安装程序提示，完成"电梯多媒体发布系统（上位机）"的安装。

### 步骤 2　设置电脑本地 IP（与控制器同网段）

打开「网络连接 → 本地连接 → Internet 协议版本 4（TCP/IPv4）→ 属性」，选择"使用下面的 IP 地址"，将电脑 IP 设为与控制器同一网段。
"""

S_STEP2N_3 = """**要点**：取消"自动获得 IP 地址"改为手动填写；此时填的电脑 IP，就是第 4 步要在屏端填入的"服务器 IP"。

### 步骤 3　用网线连接控制器 / 红点屏

用网线把电脑与多媒体显示屏（红点屏）连接起来；观察电脑右下角的网络连接状态，或屏侧网口指示灯是否闪烁。必要时可 `ping` 控制器地址验证连通性。
"""

S_STEP4 = """### 步骤 4　控制器端设置（取消自动获取 IP + 填服务器 IP）

在多媒体显示屏上插入鼠标，点击屏幕左上角调出「控制器设置界面」：**取消"自动获取 IP 地址"的勾选**，填写**服务器 IP（= 步骤 2 中电脑的 IP）**，然后点击「应用设置」。
"""

S_STEP4N_5 = """**要点**：重点看两项状态——"网络连接：正常""服务器连：在线"（绿色）；若异常，回查网段与网线。同一界面还可设置静音时长、重启时间、屏幕亮度、音量，并查看 SD 卡剩余空间与系统 / 程序版本号。

### 步骤 5　浏览器访问上位机发布系统

在本机浏览器中输入 `127.0.0.1:8989/mps` 回车；或输入多媒体 IP 的 `http://<多媒体IP>:8989/mps-t/` 打开登录页。
"""

S_STEP6 = """**要点**：登录账号 **smec30 / 200236**；如需高级权限用超级管理员 **admin / 111111**。

### 步骤 6　确认控制器连接状态

进入「EMIDS 管理 → EMIDS 控制器管理」，核对每台控制器的连接状态：**绿色 = 已连接，红色 = 未连接**。可直接点击控制器名称重新命名，建议命名为便于识别对应电梯的名称。
"""

S_STEP7 = """### 步骤 7　上传媒体素材

进入「EMIDS 管理 → EMIDS 媒体素材管理」：在下来菜单中选择素材类型（图片 / 视频 / 音频）→ 点击「上传」→ 在弹窗中点「浏览」选择要上传的文件 → 点击「上传」。
"""

S_STEP7N_8 = """**注意**：这里的"上传"只是把素材上传到多媒体（控制器）内存。支持的素材格式——**图片**：jpg、png、gif；**视频**：mp4、3gp、avi、flv、mov、rmvb、wmv；**音频**：mp3、aac、ape、m4r、ogg、wav、wma。

### 步骤 8　编辑显示内容

进入「EMIDS 管理 → EMIDS 显示内容管理」，点击「添加 / 编辑」，逐项填写：

- **文件名**（内容名称）
- **多媒体种类**：播放图片 / 播放视频
- **图片组 / 视频组**：点右侧蓝色「+」或红色「−」增删素材；可设置循环（一直循环 / 10s / 30s / 自定义时长；视频可设"指定时间段循环"）
- **音频**：作为图片播放时的背景音乐
- **背景 / 紧急信息**：分别设置普通显示与播放紧急信息时的背景图
- **文字**：滚动字幕内容
- **流媒体地址**：选配流媒体时填入 RTSP 直播地址
"""

S_STEP8N_9 = """**要点**：滚动字幕速度——把鼠标接到控制板 USB 口（CN30），点击屏左上角菜单，选择"快 / 中 / 慢"三档调整滚动速率。

### 步骤 9　下载 / 下发到控制器

在显示内容列表中选中内容 → 点击「下载到控制器」；或进入「EMIDS 控制器管理」选中控制器 → 点击「下发显示内容」。
"""

S_STEP9N_10 = """**注意（顺序很关键）**：控制器 LCD 屏所需显示内容，必须先在"控制器管理 / 触屏屏管理"**下发到控制器**，再下发显示内容，才能正确显示。控制器重启后会显示编辑后的界面。

### 步骤 10　验证与备份

- 控制器重启后，确认新界面显示正常；
- 点击「导出媒体素材包」，以文件形式保存原有界面、视频、图片、音频，便于备份与迁移。

### 补充（选配）

- **楼层代码表**：非标楼层名（如 12A）与触屏密码在此设置，设置完成后「下载到控制器」。
- **音量设置**：在"控制器管理"选中控制器 → 点「设置音量」，调到适中。
- **流媒体**：将编码器网口连电脑 → 电脑 IP 设为 192.168.0.*（.31 除外）→ 浏览器访问 192.168.0.31（admin / admin）完成配置 → 复制 RTSP 地址填入"流媒体地址"。
"""

S_SEC5 = """## 五、常见问题排查

| 现象 | 可能原因与处理 |
| --- | --- |
| 屏幕出现横向条纹 | LVDS 线接触不良，检查或更换 LVDS 线 |
| 控制器状态为红色（未连接） | 电脑与控制器不在同一网段、IP 冲突、网线或网口异常；`ping` 控制器验证 |
| 上位机页面打不开 | 端口 8989 是否可用、上位机服务是否已启动、浏览器是否兼容 |
| 机房 ↔ 轿顶 `ping` 不通 | 检查以太网转换器 |
| 显示内容不下发 / 不刷新 | 先在"控制器管理"下发到控制器，再下发显示内容；重启控制器 |
"""

S_SEC6 = """## 六、账号与参数速查

| 项目 | 值 |
| --- | --- |
| 上位机网址（本机） | 127.0.0.1:8989/mps |
| 上位机网址（远程） | <多媒体IP>:8989/mps-t/ |
| 管理员 | smec30 / 200236 |
| 超级管理员 | admin / 111111 |
| 控制器调试页（示例） | 192.168.80.1:8080/config/ |
| 流媒体编码器 | 192.168.0.31（admin / admin） |
| 支持图片格式 | jpg、png、gif |
| 支持视频格式 | mp4、3gp、avi、flv、mov、rmvb、wmv |
| 支持音频格式 | mp3、aac、ape、m4r、ogg、wav、wma |
"""

ops = [
    ("md", S_TITLE),
    ("md", S_SEC1),
    ("md", S_SEC2),
    ("img", FLOW, 560, "图 1　电梯多媒体（EMIDS）调试总流程"),
    ("md", S_SEC3),
    ("md", S_STEP12),
    ("img", MED + "image2.jpeg", 440, "图 2-1　设置电脑本地 IP（示例：192.168.0.237）"),
    ("img", MED + "image5.jpeg", 440, "图 2-2　另一现场示例：电脑 IP 192.168.2.11，网关 192.168.2.1"),
    ("md", S_STEP2N_3),
    ("md", S_STEP4),
    ("img", MED + "image1.jpeg", 440, "图 3-1　控制器设置界面（IP 192.168.0.156 / 服务器IP 192.168.0.237；连接正常、在线）"),
    ("img", MED + "image4.jpeg", 440, "图 3-2　另一现场示例（IP 192.168.30.7 / 服务器IP 192.168.2.11；控制器名「4」）"),
    ("md", S_STEP4N_5),
    ("img", MED + "image3.jpeg", 440, "图 4-1　电梯多媒体发布系统登录页（上海三菱电梯）"),
    ("md", S_STEP6),
    ("img", MED + "image6.jpeg", 440, "图 5-1　控制器列表（绿色=已连接，红色=未连接）"),
    ("img", MED + "image11.jpeg", 440, "图 5-2　控制器管理底部操作按钮（设置音量 / 重启时间 / 下发显示内容等）"),
    ("md", S_STEP7),
    ("img", MED + "image7.jpeg", 440, "图 6-1　上传媒体素材弹窗"),
    ("md", S_STEP7N_8),
    ("img", MED + "image8.jpeg", 440, "图 7-1　显示内容管理（图片组：default1.jpg / default2.jpg）"),
    ("img", MED + "image9.jpeg", 440, "图 7-2　显示内容管理（视频组：default.mp4）"),
    ("md", S_STEP8N_9),
    ("img", MED + "image10.jpeg", 440, "图 8-1　显示内容列表与「下载到控制器 / 导出媒体素材包」"),
    ("md", S_STEP9N_10),
    ("md", S_SEC5),
    ("md", S_SEC6),
]

def next_idx(resp, cur):
    # 不同工具返回的"下一个可插入位置"键名不一，统一兜底
    for k in ("last_edit_index", "next_index", "position"):
        if isinstance(resp.get(k), int) and resp[k] >= cur:
            return resp[k]
    return cur

idx = 0
for i, op in enumerate(ops):
    if op[0] == "md":
        r = call("doc_insert_markdown", {"file_id": FID, "idx": idx, "markdown": op[1]})
        idx = next_idx(r, idx)
        print(f"[{i}] md  -> idx {idx}")
    else:
        _, path, w, cap = op
        r = call("doc_insert_image", {"file_id": FID, "idx": idx, "image_path": path, "w": w})
        idx = next_idx(r, idx)
        r2 = call("doc_insert_paragraph_with_text", {"file_id": FID, "idx": idx, "text": cap})
        idx = next_idx(r2, idx)
        print(f"[{i}] img -> idx {idx} {os.path.basename(path)}")

# save to Desktop
DEST = r"C:\Users\User\Desktop\多媒体调试要点（图示增强版）.docx"
r = call("save_file", {"file_id": FID, "file_path": DEST})
print("SAVED:", DEST)
print("FINAL_FID:", FID)
