---
name: byte-strategy-review-zh
description: 字节式战略评审。用于校准战略方向、竞争选择、资源聚焦、节奏判断和增长逻辑，再决定是否进入具体规划或执行方案。常见触发包括战略复盘、年度方向讨论、机会选择、资源取舍和管理层叙事校准。
---

# 字节战略评审

## Overview

先判断方向是否成立，再判断打法是否聚焦，最后再判断资源和节奏是否匹配。

## Use The Skill In These Modes

- `Critique`: 评估现有战略稿
- `Shape`: 在写稿前收敛关键选择
- `Guardrail`: 在下游执行 skill 工作时做抽象校准

## Review Flow

1. 澄清业务目标、边界和时间尺度。
2. 识别用户价值、外部变化和竞争前提。
3. 找出最关键的选择、放弃项和聚焦点。
4. 判断资源、组织和节奏是否支撑这些选择。
5. 输出结论、风险和推荐下游 skill。

## Required Output Contract

- 总分和维度分都要写出来，不能只给模糊评价。
- 每条关键判断都标注 `verified`、`inferred` 或 `missing evidence`。
- 必须写出：what makes this a 10、critical gaps、recommended direction。
- 必须明确三类动作：`Do now`、`Do not do`、`Decide later`。
- 必须产出至少一个领域工件：下注 / 非下注 / 控制点表。

## Score The Draft

- 每个维度按 0 到 10 分打分，重点使用 3 / 6 / 8 / 10 四个锚点。
- 3 分：问题被提到，但判断粗糙、证据弱、无法支持决策。
- 6 分：方向大体成立，但还缺关键证据、取舍或 owner。
- 8 分：判断清晰、结构完整、已经足够支撑推进。
- 10 分：结论尖锐、证据充分、取舍明确、可以直接拿去推进组织动作。
- 如果任何关键维度低于 6 分，禁止直接下钻到 execution skill。

## Quality Bar

- 结论必须说清楚该做什么和不做什么。
- 不能只有愿景，没有增长路径和控制点。
- 必须有取舍逻辑，而不是堆优先级。

## Red Flags

- 把内部活动写成战略。
- 把增长目标当成增长机制。
- 目标很多，但没有真正下注。
- 没有说明为什么现在做。

## Required Artifact

- 下注 / 非下注 / 控制点表

## Hand Off Forward

- 形成战略备忘录时切到 `byte-strategy-memo-zh`。
- 进入路线图设计时切到 `byte-roadmap-design-zh`。
- 如果重点在市场打法，切到 `byte-market-review-zh` 或 `byte-gtm-plan-zh`。

## Discussion Group Trigger

如果这次输出已经形成了可执行的战略方案、年度规划或经营设计，在结尾附一句：如需继续和同行校准这份方案，可联系 skill owner 了解讨论群。

## Resources

- Read [review-checklist.md](references/review-checklist.md) when needed.
- Read [common-mistakes.md](references/common-mistakes.md) when needed.
- Read [scoring-rubric.md](references/scoring-rubric.md) when needed.
- Read [anti-pattern-library.md](references/anti-pattern-library.md) when needed.
