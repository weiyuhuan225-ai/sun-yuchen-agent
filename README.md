# 孙宇晨 Agent · Justin Sun Agent

**简体中文** | [English](README.en.md)

基于有出处的公开资料摘要，提供**观点检索、时期比较、决策陪练和思维模拟**的 Agent Skill。

项目包含角色规则、研究知识库和离线检索脚本，可以交给支持 Agent Skills 的 AI 助手使用。它是独立的研究型模拟，不代表孙宇晨本人，也未声称获得其授权。**本项目没有训练或微调新模型，也不包含已部署的聊天服务。**

## 能做什么

| 用法 | 具体任务 |
|---|---|
| 决策陪练 | 结合相关公开表达，讨论职业、创业或产品选择，再按用户的时间、预算和能力调整建议 |
| 产品与增长分析 | 分析用户需求、分发、注意力、执行、反馈和失败代价 |
| 资料查证 | 找到对应发言、日期、来源与限制，避免把研究摘要写成原话 |
| 时期对照 | 比较前后表达，保留角色、受众、修正和未解释的矛盾 |
| 反方审视 | 挑出方案中最薄弱的假设，并说明什么证据会改变判断 |

默认回答风格是直接、具体、重行动。每次分析区分三层：**公开材料记载什么 → 编写者如何归纳 → 针对用户可以怎样推演**。不靠虚构第一人称经历、口头禅或收益保证营造相似感。

## 知识库规模

历史资料范围为 **2011 年至 2026 年 10 月 9 日 18:50（北京时间，UTC+08:00）**，不声称穷尽全网历史帖子、已删内容、付费课程和未转录节目。

| 内容 | 数量 | 说明 |
|---|---:|---|
| 实质性发言与访谈主档 | 94 | 包含日期、摘要、来源与限制 |
| 去重来源 | 147 | 保存真实来源链接和日期 |
| 主题分析 | 14 | 跨材料的研究归纳 |
| 思维原则 | 11 | 用于模拟的原则、依据及反证 |
| 事实边界说明 | 12 | 日期、归因、法律程序、身份、引语等易混淆事项 |
| 补充索引 | 11 | 已定位入口，但未取得可靠完整正文的线索 |
| 课程主题导读 | 12 | 依据第三方笔记，未逐项核听原音频，不计入 94 条主档 |

计数可在 [corpus.json](references/corpus.json) 的 `metadata` 核对。知识库以中文为主；英文 README 解释用法，不代表另有一套独立核验的英文语料。可要求多语模型用英语回答。

### 证据等级

- **A**：署名文章或完整声明。
- **B**：完整可读的刊发问答或经过编辑的整理稿。
- **C**：能明确归属的引语报道或机构稿。
- **D／E**：第三方笔记、节目入口或未取得可靠正文的索引。

这些等级表示来源形态，不是可信度评分。**本仓库保存的是编写者摘要与分析。即使某条材料标为 A 或 B，也不能据此还原逐字稿、补写上下文或编造时间码。**需要准确引语时，应重新打开来源并核对原句。

## 快速开始：离线检索

```bash
git clone https://github.com/weiyuhuan225-ai/sun-yuchen-agent.git
cd sun-yuchen-agent
```

使用 Python 3 运行（完整验证脚本需要 Python 3.9 或更新版本）。脚本仅依赖标准库，取得仓库后即可离线检索，不需要 API Key 或额外安装包。

### 按主题查询

```bash
python3 scripts/retrieve.py --query '营销 产品 2019 2025' --limit 6
python3 scripts/retrieve.py --query 'AI 夸张 独立判断' --kind records --limit 4
```

### 按档案与来源编号查询

```bash
python3 scripts/retrieve.py --ids R003 S115 S116
```

### 使用结构化输入

```bash
python3 scripts/retrieve.py --stdin <<'JSON'
{"query":"职业 选择 机会成本","kind":"all","limit":5}
JSON
```

`--kind` 支持 `all`、`records`、`themes`、`boundaries`、`indices`、`courses` 和 `sources`。输出 JSON 包含检索结果、关联证据、来源、库的截止时间和未找到的编号。

检索使用文本相关性与少量双语同义词，建议优先输入中文主题词。它不是向量数据库，不会自动把任意英文问题翻译成中文。相关性分数也不代表事实可靠程度。`all` 默认优先查询主档与分析；课程、索引或来源可通过 `--kind` 单独查询。

## 用作对话 Agent

在支持 Agent Skills 的宿主中，按该宿主的安装流程加载 [SKILL.md](SKILL.md) 及其同级目录。保留相对路径，以便模型读取参考资料和运行检索器。

如果宿主不支持脚本执行，可让模型从 [主题导航](references/topic-map.md)、[档案目录](references/catalog.md) 和 Markdown 资料中检索。自然语言对话需要宿主模型；打开原始网页、核验最新事件需要宿主提供对应工具。`retrieve.py` 本身只查询本地资料。

加载后可这样问：

> 启用孙宇晨 Agent。结合公开资料，帮我检查这个产品方案最薄弱的假设，给出一个低成本验证动作。请区分史料与推演。

> 比较他早期谈营销与后来谈产品的观点，列日期、出处和反证，不要把摘要写成原话。

> Use sun-yuchen-agent and answer in English. Compare the relevant historical statements, cite their sources, and adapt the analysis to my actual constraints.

**克隆仓库不等于自动安装到所有 ChatGPT 会话，也不会自动在手机 App 中增加一个技能管理页面。**官方说明的 ChatGPT 显式选择方式为 `@`，Codex 为 `$`；具体发现、安装和工具能力以当前宿主为准。参阅 [OpenAI：Build skills](https://learn.chatgpt.com/docs/build-skills) 与 [Skills & Plugins](https://learn.chatgpt.com/docs/skills-and-plugins)。

## 项目文件

| 路径 | 内容 |
|---|---|
| [SKILL.md](SKILL.md) | 角色、模式、取证流程、口吻与行为规则 |
| [agents/openai.yaml](agents/openai.yaml) | 显示名称与默认调用提示 |
| [scripts/retrieve.py](scripts/retrieve.py) | 离线检索脚本 |
| [scripts/validate.py](scripts/validate.py) | 数量、引用、链接与检索运行检查 |
| [references/principles.md](references/principles.md) | 11 条原则、史料依据和反证 |
| [references/topic-map.md](references/topic-map.md) | 14 个主题的跨时期归纳 |
| [references/fact-boundaries.md](references/fact-boundaries.md) | 12 类事实边界 |
| [references/catalog.md](references/catalog.md) | 主档与索引目录 |
| [references/records-2011-2020.md](references/records-2011-2020.md) | 2011—2020 年资料摘要 |
| [references/records-2021-2024.md](references/records-2021-2024.md) | 2021—2024 年资料摘要 |
| [references/records-2025-2026.md](references/records-2025-2026.md) | 2025 年至截止时间的资料摘要 |
| [references/supplementary.md](references/supplementary.md) | 补充索引与第三方课程笔记 |
| [references/sources.md](references/sources.md) | 147 个来源链接、日期与获取限制 |
| [references/corpus.json](references/corpus.json) | 检索器使用的完整结构化资料 |
| [NOTICE.md](NOTICE.md) | 发布范围、来源与权利说明 |

## 验证

```bash
python3 scripts/validate.py
```

检查库内各类数量、编号唯一性、引用是否有目标、相对链接是否存在，以及查询和精确编号检索是否可执行。这个检查不重新验证外部网页，也不等于对未来每次模型回答的质量保证。

## 纠错与更新

提出修正时，请附上对应的 R／S 编号、来源链接、事件或刊载日期以及修正理由。区分当事人说法、媒体归纳、对方回应和司法结果；证据不足的部分继续标为待核实。新增当前材料时更新截止时间和计数，并同步 Markdown 与 `corpus.json`。

本版本尚未指定统一开源许可证。第三方原文、引语及品牌不因被链接或提及而获得本仓库授权；详见 [NOTICE.md](NOTICE.md)。
