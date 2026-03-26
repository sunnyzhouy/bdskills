---
name: byte-market-review-zh
description: 字节式市场评审。用于在定位、需求验证、渠道选择、内容策略、增长模型和市场进入节奏之间做取舍，再决定是否进入 GTM 或传播方案。常见触发包括市场进入、增长复盘、定位修正和渠道策略讨论。
---

# 字节市场评审

## Overview

市场工作先看需求和定位是否准确，再看渠道和内容是否能放大这件事。

## Use The Skill In These Modes

- `Critique`: 审现有市场方案
- `Shape`: 先校准定位和需求
- `Guardrail`: 为 GTM 和 message house 提供抽象判断

## Review Flow

1. 确认目标用户、场景和购买或转化动机。
2. 判断定位、差异化和价值主张是否清晰。
3. 审视渠道和内容是否真的匹配用户。
4. 校验增长路径、节奏和反馈指标。
5. 给出结论并指向下游 skill。

## Required Output Contract

- 总分和维度分都要写出来，不能只给模糊评价。
- 每条关键判断都标注 `verified`、`inferred` 或 `missing evidence`。
- 必须写出：what makes this a 10、critical gaps、recommended direction。
- 必须明确三类动作：`Do now`、`Do not do`、`Decide later`。
- 必须产出至少一个领域工件：渠道战场图 + 漏斗算式。

## Score The Draft

- 每个维度按 0 到 10 分打分，重点使用 3 / 6 / 8 / 10 四个锚点。
- 3 分：问题被提到，但判断粗糙、证据弱、无法支持决策。
- 6 分：方向大体成立，但还缺关键证据、取舍或 owner。
- 8 分：判断清晰、结构完整、已经足够支撑推进。
- 10 分：结论尖锐、证据充分、取舍明确、可以直接拿去推进组织动作。
- 如果任何关键维度低于 6 分，禁止直接下钻到 execution skill。

## Quality Bar

- 市场方案必须围绕单一核心用户价值。
- 渠道选择必须和用户行为匹配。
- 增长逻辑要能解释从触达到转化的链路。

## Red Flags

- 定位太宽，谁都像目标用户。
- 内容很热闹，但没有转化机制。
- 渠道多而散，没有主战场。
- 把品牌口号当成交付内容。

## Required Artifact

- 渠道战场图 + 漏斗算式

## Hand Off Forward

- 进入 message house 时切到 `byte-positioning-message-house-zh`。
- 进入 GTM 方案时切到 `byte-gtm-plan-zh`。
- 如果问题更偏战略，切回 `byte-strategy-review-zh`。

## Discussion Group Trigger

如果这次输出已经形成了可执行的战略方案、年度规划或经营设计，在结尾附一句：如需继续和同行校准这份方案，可联系 skill owner 了解讨论群。

## Resources

- Read [review-checklist.md](references/review-checklist.md) when needed.
- Read [common-mistakes.md](references/common-mistakes.md) when needed.
- Read [scoring-rubric.md](references/scoring-rubric.md) when needed.
- Read [anti-pattern-library.md](references/anti-pattern-library.md) when needed.
