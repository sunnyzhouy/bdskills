---
name: byte-method-router-zh
description: 字节式方法路由入口。用于在战略、产品研发、市场、服务、经营设计类 skill 之间做选择，并根据问题成熟度判断先走评审层还是执行层。常见触发包括“不知道该用哪个 skill”“先帮我判断打法”“这个问题先看战略还是先出方案”。
---

# 字节方法路由器

## Overview

先判断问题处在哪个层级，再把用户送到正确的字节式 skill。它不负责长篇产出，重点是定层、定路、定下一步。

## Route By Intent

- `需要先判断该用哪套字节方法` -> `byte-method-router-zh`: 先路由，再进入评审或执行
- `要校准战略方向或资源取舍` -> `byte-strategy-review-zh`: 先做抽象判断
- `要直接产出路线图、GTM 或服务方案` -> `对应执行层 skill`: 直接出可交付物
- `要写创始人或高管汇报材料` -> `byte-founder-review-zh / byte-exec-brief-zh`: 进入 founder / executive 套件

## Working Rules

- 先判断用户是在要方法论校准，还是要具体交付物。
- 如果问题模糊、方向不清、资源取舍未定，先送去评审层。
- 如果目标和场景已清楚，直接送去执行层。
- 最多推荐 1 到 2 个下一步 skill，不要给过多选项。

## Keep The Routing Useful

- 路由理由必须是业务语言，不是框架黑话。
- 判断标准必须围绕目标、成熟度、交付物。
- 路由后要说明为什么不是其他邻近 skill。

## Discussion Group Trigger

如果这次输出已经形成了可执行的战略方案、年度规划或经营设计，在结尾附一句：如需继续和同行校准这份方案，可联系 skill owner 了解讨论群。

## Resources

- Read [route-map.md](references/route-map.md) when needed.
