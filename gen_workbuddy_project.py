# -*- coding: utf-8 -*-
"""把公众号《我的 workbuddy 工作流架构》手册落成一个可直接使用的本地项目。"""
import os

ROOT = r"D:\Claw\workbuddy-project"

FILES = {}

# ---------------- 根 README ----------------
FILES["README.md"] = r"""# WorkBuddy 工作流架构项目

> 来源：公众号「明天的 AI」《我的 workbuddy 工作流架构，存下来吧》（原创，2026-09-23）
> 整理目标：把文章里"我的 WorkBuddy 工作流结构"从一张图，落成一个可以直接用的本地项目骨架。

## 一、四条核心理念

1. **工作流即资产**：复杂任务拆解为可复用的 Skill，一次搭建、反复调用，不再从零手写 Prompt。
2. **多智能体协作**：主 Agent 调度子代理并行执行，长任务不再断链。
3. **记忆分层**：项目记忆 + 跨项目偏好，越用越懂你。
4. **本地执行**：直接读写文件、跑命令，从"只会说"到"真会做"。

> 智能体的下一阶段，不是更会聊天，而是更会交付。

## 二、目录结构（10 个固定区域）

| 目录 | 职责 |
| --- | --- |
| `01_planner/` | 规划与任务管理：定义目标、拆解任务、排执行计划 |
| `02_memory/` | 记忆系统：短期 / 长期 / 实体记忆 + 知识图谱 |
| `03_tools/` | 工具系统：API 工具、代码工具、自定义工具 |
| `04_knowledge/` | 知识库与检索：文档、向量索引、RAG 流程 |
| `05_workbuddy_core/` | 核心配置：角色、能力边界、系统提示、工作流编排 |
| `06_evaluation/` | 评估与测试：指标、测试用例、基准、结果分析 |
| `07_observability/` | 观测与监控：日志、追踪、监控、告警规则 |
| `08_deployment/` | 部署与运维：容器化、环境配置、多种部署方式 |
| `09_examples/` | 示例与场景：典型用法、流程示例、Prompt 示例 |
| `10_docs/` | 文档与知识库：架构设计、最佳实践、FAQ、版本记录 |

## 三、怎么用

1. **先从 01_planner 开始**：把目标、计划、任务拆解写在对应文件里，再交给 WorkBuddy 执行。
2. **每完成一件事，回写 02_memory**：沉淀长期记忆与实体记忆，让后续任务越做越顺。
3. **把重复动作固化成 05_workbuddy_core/workflow.md 里的工作流 / Skill**，而不是每次重写 Prompt。
4. **所有可复用 Prompt 放进 prompt-template.md**，场景示例放进 `09_examples/`。
5. **完整手册**见 `10_docs/WorkBuddy从入门到精通手册.md`（含 17 个案例、个人工作台、自动化、AI 家教等）。

## 四、目录树

```
workbuddy-project/
├── README.md
├── 01_planner/        goal.md  plan.md  task-breakdown.md  roadmap.md
├── 02_memory/         long-term-memory.md  short-term-memory.md  entity-memory.md  knowledge-graph.md
├── 03_tools/
│   ├── api-tools/     search.md  weather.md  calculator.md  news.md
│   ├── code-tools/    code-executor.md  file-reader.md  terminal.md
│   └── custom-tools/  db-query.md  notion.md  slack.md
├── 04_knowledge/      documents.md  embeddings.md  vector-store.md  rag-pipeline.md  index-strategy.md
├── 05_workbuddy_core/ buddy.md  roles.md  persona.md  workflow.md  system-prompt.md  prompt-template.md
├── 06_evaluation/     eval-metrics.md  test-cases.md  benchmarks.md  result-analysis.md
├── 07_observability/  logs.md  traces.md  monitoring.md  alert-rules.md
├── 08_deployment/     deploy.md  env.example  docker/  k8s/
├── 09_examples/       17个案例清单.md  实操案例集.md  AI家教.md  胡楚靓AI工作台复刻.md  个人工作台7区域.md
└── 10_docs/           WorkBuddy从入门到精通手册.md
```
"""

# ---------------- 01_planner ----------------
FILES["01_planner/goal.md"] = r"""# goal.md — 目标定义

## 用途
动手前先把「要达成什么」写清楚。WorkBuddy 的规划能力依赖明确目标——目标越具体，拆解越准确。

## 模板
- **目标（一句话）**：
- **成功标准（可验证）**：
- **约束（时间 / 预算 / 范围）**：
- **交付物**：
- **验收人**：

## WorkBuddy 用法
> 读 `01_planner/goal.md`，帮我把目标拆成可执行任务，写入 `task-breakdown.md`。
"""

FILES["01_planner/plan.md"] = r"""# plan.md — 执行计划

## 用途
把目标落成"先做什么、后做什么、谁来做、多久做完"的阶段计划。

## 模板
| 阶段 | 关键动作 | 产出 | 负责人 | 时间 |
| --- | --- | --- | --- | --- |
| P0 准备 |  |  |  |  |
| P1 执行 |  |  |  |  |
| P2 验收 |  |  |  |  |

## WorkBuddy 用法
> 按 `01_planner/plan.md` 的阶段推进，每完成一个阶段把结果写回本文件。
"""

FILES["01_planner/task-breakdown.md"] = r"""# task-breakdown.md — 任务拆解

## 用途
把每个阶段拆到"一个动作 = 一个可勾选任务"，方便 WorkBuddy 逐条执行与勾选。

## 模板
- [ ] 任务 1：______（产出：______）
- [ ] 任务 2：______（产出：______）
- [ ] 任务 3：______（产出：______）

## WorkBuddy 用法
> 逐条执行上面的任务，完成一条就把 `[ ]` 改成 `[x]`，并汇报产出文件路径。
"""

FILES["01_planner/roadmap.md"] = r"""# roadmap.md — 路线图

## 用途
跨周 / 跨月的长线规划，说明里程碑与依赖关系。

## 模板
- **里程碑 M1**（日期）：______
- **里程碑 M2**（日期）：______
- **依赖 / 风险**：______

## WorkBuddy 用法
> 每周一读 `roadmap.md`，结合当前进度生成本周待办。
"""

# ---------------- 02_memory ----------------
FILES["02_memory/long-term-memory.md"] = r"""# long-term-memory.md — 长期记忆

## 用途
沉淀稳定的偏好、约定、结论。跨会话复用，越用越懂你。

## 记录内容
- 个人偏好：______
- 项目约定：______
- 已确认结论：______

## WorkBuddy 用法
> 把这条结论写入长期记忆：______
"""

FILES["02_memory/short-term-memory.md"] = r"""# short-term-memory.md — 短期记忆

## 用途
当前会话 / 当前任务的临时上下文，任务结束后清理或归档。

## 记录内容
- 当前任务：______
- 临时结论：______
- 待确认事项：______
"""

FILES["02_memory/entity-memory.md"] = r"""# entity-memory.md — 实体记忆

## 用途
记录"人 / 组织 / 项目 / 产品"等实体及其关系，避免每次重复交代背景。

## 模板
| 实体 | 类型 | 关键信息 | 关系 |
| --- | --- | --- | --- |
|  | 人 / 组织 / 项目 |  |  |

## WorkBuddy 用法
> 从今天的对话里抽取实体与关系，更新 `entity-memory.md`。
"""

FILES["02_memory/knowledge-graph.md"] = r"""# knowledge-graph.md — 知识图谱

## 用途
把实体记忆连成"关系网络"，支持跨主题联想与推理。

## 模板
```
实体A --关系--> 实体B
示例：甲物业 --负责--> 生命蓝湾6期 --问题--> 消火栓被遮挡
```

## WorkBuddy 用法
> 基于 `entity-memory.md` 生成 / 更新知识图谱。
"""

# ---------------- 03_tools / api-tools ----------------
FILES["03_tools/README.md"] = r"""# 03_tools — 工具系统

提供 WorkBuddy 可调用的各类工具，扩展能力、与外部系统协同。

- `api-tools/`：搜索、天气、计算、新闻等在线能力
- `code-tools/`：代码执行、文件读取、终端命令
- `custom-tools/`：数据库查询、Notion、Slack 等自定义集成
"""

FILES["03_tools/api-tools/search.md"] = r"""# search.md — 搜索工具

## 用途
联网检索网页资料（相当于 WorkBuddy 的内置 WebSearch）。

## 适用
- 找资料、查最新信息、核对事实
- 找特定文章、公告、页面

## 示例
> 搜索"上海三菱 EMIDS 上位机手册"，汇总可用来源。
"""

FILES["03_tools/api-tools/weather.md"] = r"""# weather.md — 天气工具

## 用途
查询指定城市天气，用于出行 / 现场作业安排提示。

## 示例
> 查一下明天奉贤的天气，判断是否适合绿化养护作业。
"""

FILES["03_tools/api-tools/calculator.md"] = r"""# calculator.md — 计算工具

## 用途
精确数值计算，避免大模型口算出错（金额、面积、比例、日期差）。

## 示例
> 用计算器核对这张水电费结算表的合计数。
"""

FILES["03_tools/api-tools/news.md"] = r"""# news.md — 新闻 / 热点工具

## 用途
获取行业新闻、热点选题，用于内容生产与情报跟踪。

## 示例
> 收集今日 AI 领域热点，整理成 10 条选题推送到飞书。
"""

# ---------------- 03_tools / code-tools ----------------
FILES["03_tools/code-tools/code-executor.md"] = r"""# code-executor.md — 代码执行工具

## 用途
直接运行 Python / JS 等代码，处理数据、生成图表、批量转换文件。

## 示例
> 写一段 Python 读取这个 xlsx，清洗后导出汇总表。
"""

FILES["03_tools/code-tools/file-reader.md"] = r"""# file-reader.md — 文件读取工具

## 用途
读取本地文档（docx / xlsx / pdf / md / txt / 图片），是"本地执行"的基础。

## 示例
> 读取桌面《多媒体调试要点.docx》，总结结构。
"""

FILES["03_tools/code-tools/terminal.md"] = r"""# terminal.md — 终端工具

## 用途
执行命令行操作：文件管理、批处理、调用外部程序。

## 注意
系统级指令可能不在远程支持范围内，建议先验证再依赖。
"""

# ---------------- 03_tools / custom-tools ----------------
FILES["03_tools/custom-tools/db-query.md"] = r"""# db-query.md — 数据库查询工具

## 用途
连接业务数据库，做取数、统计、导出。

## 模板
- 连接（脱敏）：host / db / 只读账号
- 常用 SQL：______
"""

FILES["03_tools/custom-tools/notion.md"] = r"""# notion.md — Notion 集成

## 用途
读写 Notion 页面 / 数据库，作为团队知识库。

## 示例
> 把这份项目周报同步到 Notion 的"周报"数据库。
"""

FILES["03_tools/custom-tools/slack.md"] = r"""# slack.md — Slack 集成

## 用途
向 Slack 频道推送通知 / 日报 / 告警。

## 示例
> 任务完成后把结果摘要推送到 #project 频道。
"""

# ---------------- 04_knowledge ----------------
FILES["04_knowledge/documents.md"] = r"""# documents.md — 文档管理

## 用途
管理知识库原始文档：来源、分类、更新时间。

## 模板
| 文档 | 来源 | 归类 | 更新日期 |
| --- | --- | --- | --- |
"""

FILES["04_knowledge/embeddings.md"] = r"""# embeddings.md — 向量化

## 用途
说明文档如何切分 / 向量化，以便语义检索。

## 要点
- 切分粒度：按章节 / 段落
- 向量模型：______
- 重排策略：______
"""

FILES["04_knowledge/vector-store.md"] = r"""# vector-store.md — 向量库

## 用途
存放向量并支持相似度检索。

## 记录
- 向量库类型：______
- 索引规模：______
- 更新方式：______
"""

FILES["04_knowledge/rag-pipeline.md"] = r"""# rag-pipeline.md — RAG 流程

## 用途
定义"检索 → 组装上下文 → 生成回答"的完整链路，让 WorkBuddy 基于私有资料作答更准确。

## 流程
```
用户提问 → 改写查询 → 向量检索 → 重排 → 拼上下文 → 生成 → 引用出处
```
"""

FILES["04_knowledge/index-strategy.md"] = r"""# index-strategy.md — 索引策略

## 用途
决定如何建立 / 更新索引（全量 vs 增量），以及检索时的召回 / 排序策略。

## 要点
- 全量重建频率：______
- 增量更新触发：______
- 召回 Top-K：______
"""

# ---------------- 05_workbuddy_core ----------------
FILES["05_workbuddy_core/buddy.md"] = r"""# buddy.md — WorkBuddy 定位

## 用途
一句话说明"这个 WorkBuddy 是干什么的"，以及它的能力边界。

## 模板
- **定位**：______
- **能做什么**：______
- **不做什么**：______
"""

FILES["05_workbuddy_core/roles.md"] = r"""# roles.md — 角色定义

## 用途
按场景定义不同角色（如：物业现场工程师 / 内容编辑 / 数据分析师），便于切换。

## 模板
| 角色 | 适用场景 | 语气 | 输出格式 |
| --- | --- | --- | --- |
|  |  |  |  |
"""

FILES["05_workbuddy_core/persona.md"] = r"""# persona.md — 人格设定

## 用途
设定 WorkBuddy 的性格与语气（对应 WorkBuddy 的 SOUL.md / IDENTITY.md）。

## 模板
- **性格**：______
- **语气**：______
- **禁忌**：______
"""

FILES["05_workbuddy_core/workflow.md"] = r"""# workflow.md — 工作流编排

## 用途
把多步骤任务固化成可复用的工作流 / Skill，一次搭建、反复调用。

## 示例：每日 AI 热点选题推送到飞书
- **触发**：每天 09:00
- **步骤**：多源抓取热点 → 合并去重排序 → 生成选题报告 → 推送飞书
- **提示词**（可复制到 WorkBuddy 的"自动化任务"）：

```
你是一个 AI 领域博主选题助手，请执行以下任务，全程不需要与用户确认，完全自主完成：
## 任务目标
收集今日 AI 领域热点，生成选题日报，并推送到飞书。
## 执行步骤
### 第1步：多源抓取 AI 热点（并行执行，提高效率）
使用以下工具抓取数据，尽量并行调用以提升效率：
1. "AIhot72" 接口：拉取过去 24h 的 AI HOT 精选动态
2. "Github 热门项目"：拉取今日 GitHub Trending
- 执行命令：`cd /path && python3 github_trending.py --period daily --limit 25 --json`
### 第2步：合并、去重、排序、生成 report
```

## 手动确认无误后，在同一对话里直接告诉 WorkBuddy
```
把这个任务设置为自动化，每天早上 9:00 运行，结果发送到 [指定飞书群 / 邮箱 / 企微通知]。
```

## 把自动化任务设计成状态机
为每个状态定义明确的成功条件与失败出口：

```
stateDiagram-v2
  [*] --> WaitingTrigger
  WaitingTrigger --> Fetching: 9:00 触发
  Fetching --> Deduping: 抓取成功
  Fetching --> Alert: 抓取失败
  Deduping --> Composing: 去重完成
  Composing --> Pushing: 报告生成
  Pushing --> [*]: 推送成功
  Pushing --> Alert: 推送失败
```

## 触发频率选项
周期（按周 / 按天 / 单次）、每天 / 09:00、生效日期区间。
"""

FILES["05_workbuddy_core/system-prompt.md"] = r"""# system-prompt.md — 系统提示

## 用途
定义 WorkBuddy 的角色、能力边界与系统级约束（对应 system prompt）。

## 模板
```
你是 ______，负责 ______。
规则：
1. ______
2. ______
输出要求：______
```
"""

FILES["05_workbuddy_core/prompt-template.md"] = r"""# prompt-template.md — Prompt 模板库

## 用途
存放可复用的 Prompt 模板，避免每次重写。

## 模板 A：任务执行型
```
你是 ______。任务：______。要求：______。输出：______。
```

## 模板 B：引导型（不直接给答案）
```
你是一位擅长 ______ 的导师。无论问什么，遵守以下规则：
1. 不直接给最终答案；
2. 先判断题目考查的知识点；
3. 用一个问题引导说出思路；
4. 若卡住，只给提示，不代替完成；
5. 最后总结方法，并出一道同类题巩固。
```

## 模板 C：整理归档型
```
把 ______ 目录下的文件按 ______ 规则整理归档，输出一份清单。
```
"""

# ---------------- 06_evaluation ----------------
FILES["06_evaluation/eval-metrics.md"] = r"""# eval-metrics.md — 评估指标

## 用途
定义"做得好不好"的量化标准。

## 常用指标
- 准确率 / 召回率
- 任务完成率、平均耗时
- 人工评分（1–5）
"""

FILES["06_evaluation/test-cases.md"] = r"""# test-cases.md — 测试用例

## 用途
沉淀典型输入 → 期望输出，用于回归验证。

## 模板
| 用例 | 输入 | 期望输出 | 结果 |
| --- | --- | --- | --- |
"""

FILES["06_evaluation/benchmarks.md"] = r"""# benchmarks.md — 基准

## 用途
记录基线表现，便于对比优化前后。

## 模板
- 基线版本：______
- 关键指标：______
"""

FILES["06_evaluation/result-analysis.md"] = r"""# result-analysis.md — 结果分析

## 用途
分析失败案例，定位是 Prompt、工具还是数据问题，驱动迭代。

## 模板
- 现象：______
- 根因：______
- 改进：______
"""

# ---------------- 07_observability ----------------
FILES["07_observability/logs.md"] = r"""# logs.md — 日志

## 用途
记录每次任务的执行日志，便于回溯。
"""

FILES["07_observability/traces.md"] = r"""# traces.md — 追踪

## 用途
追踪多步 / 多 Agent 的执行链路，定位断点。
"""

FILES["07_observability/monitoring.md"] = r"""# monitoring.md — 监控

## 用途
监控关键指标与成本，保障稳定运行。
"""

FILES["07_observability/alert-rules.md"] = r"""# alert-rules.md — 告警规则

## 用途
定义异常告警：失败重试、超时、成本超阈。

## 模板
| 条件 | 级别 | 通知方式 |
| --- | --- | --- |
"""

# ---------------- 08_deployment ----------------
FILES["08_deployment/deploy.md"] = r"""# deploy.md — 部署说明

## 用途
描述部署方式：本地 / 云端 / 集群。

## 要点
- 运行环境：______
- 启动方式：______
- 回滚方案：______
"""

FILES["08_deployment/env.example"] = r"""# 环境变量示例（复制本文件为 .env 并填写真实值）
# 切勿把真实密钥提交到仓库 / 写进代码或文档

TENCENTCLOUD_SECRET_ID=
TENCENTCLOUD_SECRET_KEY=
API_BASE_URL=
"""

FILES["08_deployment/docker/README.md"] = r"""# docker/ — 容器化

放置 Dockerfile 与 docker-compose.yml。

## 示例 Dockerfile
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "main.py"]
```
"""

FILES["08_deployment/k8s/README.md"] = r"""# k8s/ — 集群部署

放置 Kubernetes 编排文件（deployment / service / configmap）。
"""

# ---------------- 09_examples ----------------
FILES["09_examples/17个案例清单.md"] = r"""# WorkBuddy 17 个案例清单（存一下吧 · 7月20日修改）

> 来源：公众号「明天的 AI」

## 一、Excel / 数据处理
## 二、文件批量处理 / 整理归档
## 三、文档 / 报告自动生成
## 四、定时自动化任务
## 五、Claw 远程控制进阶玩法

### 实战 13：出差在外急需文件
直接在微信里发给 ClawBot（一个微信联系人）：
```
打开电脑 E 盘"项目资料/XX项目"文件夹，找到最新版本的方案文件（文件名包含"方案"或"proposal"），用微信发送给我。
```
⚠️ 注意：Claw 会把文件发到它和你的微信聊天窗口里，不会发到"文件传输助手"。

### 实战 14：远程让电脑开始一项任务
> 前提：需要在电脑端提前设置好自动化任务。Claw 可以通过微信触发已配置的自动化，但不能凭空创建新任务。
```
开始执行之前设置好的"竞品分析"任务，搜集[竞品名]今天的最新动态，把结果保存到桌面"竞品追踪"文件夹，完成后微信通知我。
```

### 实战 15：远程检查电脑状态
```
帮我查看电脑当前 C 盘和 D 盘的剩余空间，把结果告诉我，如果某个盘剩余空间小于 10GB，提醒我及时清理。
```
⚠️ 注意：Claw 的远程能力以文件操作为主，系统级指令可能不在支持范围内，建议先验证再依赖。

## 六、内容创作 / 自媒体场景

### 实战 16：批量生成内容草稿
```
读取桌面"选题库.xlsx"（A 列是选题标题，B 列是关键词，C 列是目标平台），针对每一行选题，生成一篇 500 字左右的内容草稿，风格：口语化，适合小红书平台，多用短句。
```
"""

FILES["09_examples/实操案例集.md"] = r"""# WorkBuddy 实操案例集

## 短任务实战：Excel 可视化与数据清洗

### 提示词示例
```
帮我可视化这份流水账数据并分析一下。
重点关注：
1. 每月收支趋势；
2. 支出分类占比；
3. 异常大额支出标注；
4. 给出 3 条可操作的省钱建议。
```
> 执行过程可能较慢，但最终产出的可视化效果通常超出预期——包括图表、趋势分析和文字总结。数据清洗和 PPT 生成同理。

## 设计创意：用提示词生成完整网站

### 模板一：个人作品集 Hero Section
```
Build a full-screen hero section for a creative portfolio using React...
```
"""

FILES["09_examples/AI家教.md"] = r"""# 用 WorkBuddy 定制 AI 家教

## 先设定"家教规则"（从"有问必答"切换到"引导为主"）
把下面这段提示词发给它：

```
你是一位擅长辅导三年级小学生的金牌家教。无论孩子问什么题，请遵守以下规则：
1. 不直接给最终答案；
2. 先判断题目考查的知识点；
3. 用一个问题引导孩子说出思路；
4. 如果孩子卡住，只给提示，不代替完成；
5. 最后总结方法，并出一道同类题巩固。
```

## 01 不知道从哪教？先诊断，再辅导

**WorkBuddy 用法：生成知识树和诊断题**

当你不知道从哪开始教，不要再凭感觉补课啦，直接让 WorkBuddy 帮你和孩子做个学习体检，找到薄弱环节，再决定怎么讲、练什么、练多少。

试着这样向 WorkBuddy 提需求：______（孩子的问题一目了然）。
"""

FILES["09_examples/胡楚靓AI工作台复刻.md"] = r"""# 用 WorkBuddy 复刻爆火的胡楚靓 AI 工作台

左边是每日计划、选题灵感、爆款内容、数据分析、备忘录，右边是每个功能对应的操作页面，整整齐齐，看着像一套专门定制的软件。

## 这不是一个网页

它为什么突然火了？大致三个原因：

1. **结果特别直观。** 让 AI 写一篇文章大家都习惯了；可当你跟 AI 聊几句，它直接甩出来一个有菜单、有按钮、有数据卡片的工作台，那个冲击完全不一样——你不是让 AI 回答了问题，是让 AI 给你做了一个工具。
2. **每个人都能做自己的版本。** 胡楚靓做的是内容创作者工作台，但看到那个页面，几乎每个人都会冒出一个念头：我能不能也来一个？考研的做学习台，打游戏的做客户端，健身的做打卡台，宝妈做育儿台。评论区那些交作业的，不是在复刻同一个网页，是在做自己的版本。
3. **它让普通人第一次觉得，自己也能做软件。** 以前一提到做软件，脑子里蹦出来的是学编程、写代码、配环境、买服务器、搭数据库。现在你只需要说，帮我做一个个人工作台，左边放每日计划、选题灵感和备忘录，整体简洁一点。AI 就开始动手了。它降的不只是编程门槛，是把想法变成工具的门槛。

## 我也试了一遍

用 WorkBuddy 的"代码开发模式 + Agent 应用开发"，描述需求即可生成个人工作台。
"""

FILES["09_examples/个人工作台7区域.md"] = r"""# WorkBuddy 搭建个人工作台（保姆级教程）

> 先把一套能用的工作台跑通，比安装一堆自己不会用的功能更重要。

## 一、搭完后，你的个人工作台长什么样

建议把工作台放在 D 盘，单独建一个文件夹：`D:\我的个人工作台`

里面分成 **7 个区域**：

```
D:\我的个人工作台
├── 00-收件箱
├── 01-我的资料
├── 02-进行中项目
├── 03-内容生产
├── 04-日常办公
├── 05-交付成果
└── 06-归档
```

> 每个文件夹只负责一件事。

### 00-收件箱
暂时不知道放哪里的文件，先丢进这里。

### 01-我的资料
身份、单位、常用信息等长期资料。

### 02-进行中项目
一个项目一个子文件夹。

### 03-内容生产
内容、选题、草稿、图文与发布记录。

### 04-日常办公
会议、周报、审批、日常汇报。

### 05-交付成果
已完成、可对外交付的成稿文件。

### 06-归档
结束项目的归档资料。

## 二、搭建步骤（原文）

### Step 1：准备工作
选择"代码开发模式"，并在输入提示词前引用"Agent 应用开发"功能。

### Step 2：先搭个框架
给一段较长的提示词说明目标与诉求，例如：

```
我想开发一个个人桌面工作台，可以直观呈现我每日的重要任务进展、待办清单，还能随时记录一些个人想法。我现在的每日重要任务就是 [3 个微信公众号的文章更新、1 个视频号和 1 个抖音号的更新]，当公众号文章更新完成后，我还需要把公众号文章归档到 ima 个人知识库。请先帮我规划这个个人工作台。
```

WorkBuddy 效率还挺高的，一会就直接给出了布局设计让我确认。
"""

# ---------------- 10_docs ----------------
FILES["10_docs/WorkBuddy从入门到精通手册.md"] = r"""# WorkBuddy 从入门到精通手册

> 整理自公众号「明天的 AI」的 WorkBuddy 系列内容。

## 一、WorkBuddy 是什么

WorkBuddy 是 AI 原生的桌面智能体工作台，可在手机主流 IM 下指令，AI 自动干活交付。

**核心能力**
- 理解自然语言：用一句话下达任务，无需复杂的操作步骤
- 自主规划执行：自动拆解任务、规划步骤、执行操作
- 多模态任务处理：支持文档、表格、PPT、数据分析等多种任务类型
- 本地文件操作：可读取授权的电脑文件夹，进行批量处理

> 不叫 AI 帮你干活，这叫 AI 给你布置作业。今天要说的这个工具，干的是另一件事：你说一句话，它直接在你的电脑上执行，文件整理好了，报告生成了，表格分析完了，结果放在桌面上等你。
>
> 这是 WorkBuddy，腾讯出的全场景 AI 智能体桌面工作台，2026 年 3 月 9 日正式上线，下载即用，零部署，0 代码基础。

## 二、工作流结构（10 目录）

见项目根目录 `README.md` 与各子目录。

| 目录 | 职责 |
| --- | --- |
| 01_planner | 规划与任务管理｜定义目标、拆解任务和执行计划 |
| 02_memory | 记忆系统｜管理短期/长期/实体记忆，支持上下文延续、知识沉淀 |
| 03_tools | 工具系统｜搜索、文档、日历、表格和自定义工具，与外部系统协同 |
| 04_knowledge | 知识库与检索｜知识库、向量索引和检索流程，基于私有资料作答 |
| 05_workbuddy_core | 核心配置｜角色、能力边界、系统提示、工作流编排与 Prompt 模板 |
| 06_evaluation | 评估与测试｜评估指标、测试用例和效果分析，驱动优化迭代 |
| 07_observability | 观测与监控｜日志、追踪、性能监控、成本追踪与异常告警 |
| 08_deployment | 部署与运维｜部署、容器化和运行环境配置，支持本地/云端/集群 |
| 09_examples | 示例与场景｜典型使用场景、流程示例和 Prompt 示例 |
| 10_docs | 文档与知识库｜架构设计、最佳实践、FAQ 和版本更新记录 |

## 三、核心理念（四条）

1. 工作流即资产：复杂任务拆解为可复用的 Skill，一次搭建，反复调用。
2. 多智能体协作：主 Agent 调度子代理并行执行，长任务不再断链。
3. 记忆分层：项目记忆 + 跨项目偏好，越用越懂你。
4. 本地执行：直接读写文件、跑命令，从"只会说"到"真会做"。

## 四、案例与场景

- 17 个案例清单 → `09_examples/17个案例清单.md`
- Excel 可视化 / 网站生成 → `09_examples/实操案例集.md`
- AI 家教 → `09_examples/AI家教.md`
- 胡楚靓 AI 工作台复刻 → `09_examples/胡楚靓AI工作台复刻.md`
- 个人工作台 7 区域 → `09_examples/个人工作台7区域.md`
- 自动化工作流与状态机 → `05_workbuddy_core/workflow.md`

## 五、最佳实践

1. 先跑通一套最小可用工作流，再逐步加功能。
2. 把重复动作固化成 Skill / 工作流，而不是每次重写 Prompt。
3. 目标写清、任务拆细、成果回写记忆。
4. 自动化任务用状态机定义成功条件与失败出口。
5. 密钥放 `.env`，不进仓库。
"""

# ---------------- 写入 ----------------
def main():
    count = 0
    for rel, content in FILES.items():
        p = os.path.join(ROOT, rel.replace("/", os.sep))
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8") as f:
            f.write(content)
        count += 1
    # 补充空目录（09_examples 已有文件，docker/k8s 已有 README）
    print("created files:", count)
    # 打印目录树
    from collections import defaultdict
    for dirpath, dirnames, filenames in os.walk(ROOT):
        level = dirpath.replace(ROOT, "").count(os.sep)
        indent = "  " * level
        print(f"{indent}{os.path.basename(dirpath)}/")
        for fn in sorted(filenames):
            print(f"{indent}  {fn}")

if __name__ == "__main__":
    main()
