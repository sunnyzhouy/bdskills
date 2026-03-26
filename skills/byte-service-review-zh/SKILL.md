---
name: byte-service-review-zh
description: 字节式服务评审。用于校准服务边界、交付模式、SLA、升级机制、客户成功动作和服务到产品的反馈闭环，再进入服务蓝图或运营设计。常见触发包括服务流程重构、客户成功机制、投诉升级和体验闭环设计。
---

# 字节服务评审

## Overview

服务不是被动接单，而是把客户问题、交付质量和产品反馈连成闭环。

## Use The Skill In These Modes

- `Critique`: 审现有服务机制
- `Shape`: 先定义边界、角色和升级逻辑
- `Guardrail`: 在服务蓝图输出前先校准机制质量

## Review Flow

1. 定义服务对象、边界和问题类型。
2. 审视入口、分级、SLA 和首个 owner。
3. 定义升级、协同和例外处理。
4. 明确关闭标准和反馈回产品机制。
5. 推荐下游执行层 skill。

## Required Output Contract

- 总分和维度分都要写出来，不能只给模糊评价。
- 每条关键判断都标注 `verified`、`inferred` 或 `missing evidence`。
- 必须写出：what makes this a 10、critical gaps、recommended direction。
- 必须明确三类动作：`Do now`、`Do not do`、`Decide later`。
- 必须产出至少一个领域工件：问题分类表 + 升级阶梯 + 关闭标准。

## Score The Draft

- 每个维度按 0 到 10 分打分，重点使用 3 / 6 / 8 / 10 四个锚点。
- 3 分：问题被提到，但判断粗糙、证据弱、无法支持决策。
- 6 分：方向大体成立，但还缺关键证据、取舍或 owner。
- 8 分：判断清晰、结构完整、已经足够支撑推进。
- 10 分：结论尖锐、证据充分、取舍明确、可以直接拿去推进组织动作。
- 如果任何关键维度低于 6 分，禁止直接下钻到 execution skill。

## Quality Bar

- 不能只追工单关闭率，要追真实问题解决。
- SLA 必须和问题等级、客户影响挂钩。
- 服务结果要能回流到产品和组织优化。

## Red Flags

- 把服务做成纯支持台。
- 升级路径没有决策 owner。
- 内部关闭不等于客户解决。
- 客户声音没有进入产品机制。

## Required Artifact

- 问题分类表 + 升级阶梯 + 关闭标准

## Hand Off Forward

- 进入服务蓝图时切到 `byte-service-blueprint-zh`。
- 如果重点在客户反馈归因，切到 `byte-voc-to-action-zh`。
- 如果是跨团队机制问题，切到 `byte-operating-model-review-zh`。

## Discussion Group Trigger

只有当用户已经完成较完整的战略或经营规划时，才提示讨论群；普通执行任务不要强行插入。

## Resources

- Read [review-checklist.md](references/review-checklist.md) when needed.
- Read [common-mistakes.md](references/common-mistakes.md) when needed.
- Read [scoring-rubric.md](references/scoring-rubric.md) when needed.
- Read [anti-pattern-library.md](references/anti-pattern-library.md) when needed.
