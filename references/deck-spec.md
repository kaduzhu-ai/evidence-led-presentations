# 可选的汇报数据规格

用 JSON 把来源、结论、页面和数值连接起来，适合多页研究报告。它是制作前的中间记录，不是 PPT 文件或渲染模板。普通改字、排版不必使用。

复制 `assets/deck-spec.example.json` 后替换全部虚构内容；真实项目设 `synthetic: false`。示例中的 `fact` 和 `observed` 仅表示虚构案例内部的已给定数据，不代表真实世界证据。

## 必需字段

| 对象 | 字段与规则 |
|---|---|
| 根对象 | `schema_version: "1.0"`；`synthetic` 布尔值；`decision`、`audience`、`as_of` 非空文本；`sources`、`claims`、`slides` 数组 |
| 来源 | `id` 唯一；`title`、`publisher`、`locator`、`published_on`、`period`、`scope`、`limitations` 非空文本；`provenance` 为 `public`、`user_provided` 或 `synthetic` |
| 结论 | `id` 唯一；`text`；`kind`；`source_ids`；推断、假设、建议另填 `reasoning` |
| 页面 | `id` 唯一；`title`、`question`、`implication`、`visual`；非空 `claim_ids`；`charts` 数组，无图表填 `[]` |
| 图表 | `type`、`unit`、`period`、`scope`；`basis` 为 `observed`、`scenario` 或 `mixed`；`source_ids`；`labels`；`series` |
| 数据系列 | `name`；`values` 为有限数值列表，长度与 `labels` 一致，不用 `null`、NaN 或布尔值代替缺失值 |

`kind` 可选：`fact`（事实）、`party_claim`（主体声称）、`inference`（推断）、`assumption`（假设）、`recommendation`（建议）。前三类必须有来源。推断写明从证据到结论的逻辑；假设写明设定理由；建议写明权衡与前提。

`locator` 写原始 URL 加页码、章节、表名，或私有源文件定位和时间戳；不把真实项目中的私有定位随公开示例发布。来源日期或范围确实未知可填 `unknown`，并在限制中解释。`scope` 记录地区、对象、单位、分母、样本和统计定义；不适用项明确写不适用。

`basis` 区分观察、情景和混合数据。混合图表必须在最终图中另用分界线、虚实线或标签区分。校验器不判断这项视觉要求。

情景图也需要来源记录：可将模型假设作为 `user_provided` 来源，写明来源为分析者设定与公式位置，不能伪装为外部实测。JSON 允许额外字段，可增加计算公式、证据评级、录音覆盖记录和备注；校验器不验证额外字段。

## 运行与边界

从 Skill 根目录运行：

```bash
python3 scripts/check_deck_spec.py path/to/deck-spec.json
```

需要 Python 3.9 或更新版本，仅使用标准库。不联网、不读取凭证、不修改输入文件。

- 退出码 `0`：结构和引用检查通过。警告可能仍需处理。
- 退出码 `1`：字段、引用、ID、图表长度或数值类型有误。
- 退出码 `2`：输入无法读取或不是有效 JSON。

该脚本检查的是记录完整性与基本一致性，**不验证**来源真实性、URL 可访问性、日期正确性、数据口径的实质可比性、数学公式、推理成立与否、评分合理性、隐私、排版和最终 PPTX 文件。对这些项目仍须人工或 Agent 复核。
