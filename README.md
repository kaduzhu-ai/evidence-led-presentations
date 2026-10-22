# Evidence-Led Presentations｜循证决策汇报

把会议录音、研究材料和经营数据，转成结论清楚、证据可追溯、图表直观的管理层汇报 PPT。

An agent skill for turning source material into evidence-backed executive presentations, with traceable claims, clear decision logic, editable visuals, and final-slide quality checks.

## 简介

**循证决策汇报**是一套面向管理层汇报、战略研究和产品决策的 AI Skill。它从完整理解原始材料出发，结合第一性思考与适用的经典分析框架，把“用户价值—市场证据—商业判断—行动建议”组织成结论先行的故事线，再用恰当的图表、统一版式和逐页校验形成专业 PPT。它强调数据口径、评分依据与不确定性的透明表达，也支持对已有报告进行结构优化和视觉改版。

GitHub 仓库短简介：

> Evidence-backed executive PPTs: source review, strategic reasoning, clear storylines, editable charts, and slide-by-slide QA. 循证决策汇报 Skill。

## 适合什么任务

- 基于会议录音或转写，还原产品构想并制作汇报。
- 将 PDF、研究报告、表格转成管理层演示文稿。
- 对多个产品、市场或进入路径进行有依据的比较。
- 为已有 PPT 补强证据、精简结构，或仅优化排版。

## 工作方式

1. **定义决策**：明确受众、本次要决定的事和交付边界。
2. **还原意图**：处理完整材料，保留用户价值和关键限定条件。
3. **建立证据**：让结论对应来源，核对销量、收入、用户等指标口径。
4. **形成判断**：按问题选择第一性、JTBD、STP、市场规模或单位经济等框架。
5. **组织故事**：首页结论汇总，每页用一个主要结论推进论证。
6. **视觉表达**：按信息关系选图，优先原生可编辑元素。
7. **验证交付**：复核逻辑和数字，渲染最终文件并逐页检查。

## 安装与调用

本目录是独立的 Agent Skill，入口为 `SKILL.md`。保留目录结构，将整个目录交给支持该格式的宿主加载。

**Codex 本地使用**：把整个 `evidence-led-presentations` 目录放进项目的 `.agents/skills/`，或个人的 `~/.agents/skills/`。也可以请宿主的 Skill Installer 从发布后的 GitHub 仓库安装。发现与安装规则参见 [官方 Build skills 文档](https://learn.chatgpt.com/docs/build-skills)（核对日期：2026-10-22）。其他宿主按各自文档配置，不保证相同安装路径。

公开仓库：[kaduzhu-ai/evidence-led-presentations](https://github.com/kaduzhu-ai/evidence-led-presentations)。可以把下面的安装请求交给支持 GitHub Skill 安装的 Agent：

```text
请从 https://github.com/kaduzhu-ai/evidence-led-presentations 安装此 Skill。
Skill 位于仓库根目录，入口是 SKILL.md；请保留 references、assets、scripts 和 agents 目录。
```

在支持 `$` 调用的宿主中使用：

```text
请使用 $evidence-led-presentations，基于附件制作一份给管理层的汇报PPT。
本次要决定是否进入新市场。汇报时长15分钟。
请完整分析材料，第一张内容页给出建议与对比，关键数据可追溯，图表尽量可编辑。
```

仅改版：

```text
请使用 $evidence-led-presentations 优化附件PPT的视觉表达。
保留现有结论、数据、页数和顺序。发现内容疑点单独列出。
```

与战略技能配合：

```text
先用我的战略分析 Skill 形成市场进入建议，
再用 $evidence-led-presentations 将其组织成12页管理层汇报。
```

支持技能选择器的宿主也可直接选择“循证决策汇报”。

## 文件说明

| 文件 | 用途 |
|---|---|
| `SKILL.md` | Agent 的核心执行流程与质量要求 |
| `agents/openai.yaml` | 支持该元数据格式的宿主界面信息 |
| `references/evidence-and-analysis.md` | 录音覆盖、证据、市场模型与评分细则 |
| `references/storyline-and-design.md` | 故事线、选图、版式和交付检查 |
| `references/deck-spec.md` | 可选的数据规格及校验边界 |
| `assets/deck-spec.example.json` | 可复制的全虚构示例 |
| `scripts/check_deck_spec.py` | 来源、结论和图表结构检查工具 |

在此目录运行示例检查（Python 3.9+，仅标准库，无需 API Key）：

```bash
python3 scripts/check_deck_spec.py assets/deck-spec.example.json
```

## 能力与依赖

这是方法型 Skill，包含一个辅助校验器，不是独立的 PPT 软件。实际生成和渲染 PPT 需要宿主提供相应工具；音频分析、外部检索也依赖宿主能力与授权。缺少工具时，它应说明未完成的环节，不宣称已经听完录音、查验来源或检查成品。

可单独使用，也可与战略分析和演示文稿制作技能配合。示例不包含真实客户材料。咨询式表达指清晰的论证与图表原则；本项目不代表任何咨询机构或其官方模板。

## GitHub 发布范围

将本目录的内容作为独立仓库内容发布即可；不要一并上传宿主的完整 Skills 仓库、客户资料、生成报告或工作日志。当前包未指定开源许可证；如要授予复用、修改和再分发权限，由发布者选择并添加相应许可证。
