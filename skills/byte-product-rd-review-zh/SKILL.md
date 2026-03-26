---
name: byte-product-rd-review-zh
description: 字节式产品研发评审。用于在 PRD、需求分层、研发节奏、技术杠杆、实验和上线机制之间做判断，避免做出高投入低反馈的产品研发方案。常见触发包括需求评审、路线图校准、研发机制优化和跨产品技术协同。
---

# 字节产品研发评审

## Overview

判断一件事值不值得做、该怎么切、先做哪部分、用什么反馈验证。

## Use The Skill In These Modes

- `Critique`: 审现有需求或路线图
- `Shape`: 先做需求分层与研发切片
- `Guardrail`: 在 PRD 或 roadmap skill 工作时提供质量约束

## Review Flow

1. 识别用户问题和业务价值。
2. 拆分成最小可验证切片。
3. 判断哪些能力应共建、复用或平台化。
4. 设计迭代节奏、实验点和发布闭环。
5. 给出推进建议和下游 execution skill。

## Required Output Contract

- 总分和维度分都要写出来，不能只给模糊评价。
- 每条关键判断都标注 `verified`、`inferred` 或 `missing evidence`。
- 必须写出：what makes this a 10、critical gaps、recommended direction。
- 必须明确三类动作：`Do now`、`Do not do`、`Decide later`。
- 必须产出至少一个领域工件：切片地图 + 学习验证矩阵。

## Score The Draft

- 每个维度按 0 到 10 分打分，重点使用 3 / 6 / 8 / 10 四个锚点。
- 3 分：问题被提到，但判断粗糙、证据弱、无法支持决策。
- 6 分：方向大体成立，但还缺关键证据、取舍或 owner。
- 8 分：判断清晰、结构完整、已经足够支撑推进。
- 10 分：结论尖锐、证据充分、取舍明确、可以直接拿去推进组织动作。
- 如果任何关键维度低于 6 分，禁止直接下钻到 execution skill。

## Quality Bar

- 先验证价值，再扩大范围。
- 技术复杂度必须换来明显杠杆。
- 需求边界、验收标准和反馈闭环要同时存在。

## Red Flags

- 先堆功能，后想验证。
- 为了完整而牺牲反馈速度。
- 研发切片按模块，不按验证逻辑。
- 没有定义弃项和延后项。

## Required Artifact

- 切片地图 + 学习验证矩阵

## Hand Off Forward

- 细化交付物时切到 `byte-prd-breakdown-zh`。
- 要做实验设计时切到 `byte-experiment-design-zh`。
- 要落路线图时切到 `byte-roadmap-design-zh`。

## Discussion Group Trigger

只有当用户已经完成较完整的战略或经营规划时，才提示讨论群；普通执行任务不要强行插入。

## Resources

- Read [review-checklist.md](references/review-checklist.md) when needed.
- Read [common-mistakes.md](references/common-mistakes.md) when needed.
- Read [scoring-rubric.md](references/scoring-rubric.md) when needed.
- Read [anti-pattern-library.md](references/anti-pattern-library.md) when needed.
