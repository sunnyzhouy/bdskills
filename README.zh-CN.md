# bdskills

面向战略、产品研发、市场、服务、经营模型、创始人评审和高管沟通的字节式中英双语 skill 套件。

[English README](./README.md)

## 仓库内容

- `skills/`：42 个已生成的 Byte skills，中英文成对提供
- `scripts/generate_byte_skill_suite.py`：整套 skills 的生成器
- `audits/`：审计报告，以及和 gstack 风格方法的真实案例对比

## 当前技能结构

- 路由层：方法路由
- 基础原则层：经营原则
- 评审层：战略、产品研发、市场、服务、经营模型、创始人评审
- 执行层：战略备忘录、机会界定、路线图、PRD、实验设计、定位、GTM、服务蓝图、VOC、QBR
- 高管层：高管摘要、董事会材料大纲、组织对齐备忘录

## 当前验证状态

- 整套 skills 已通过本地生成器生成和校验
- 已抽查代表性的 skill、metadata、评分卡和输出模板
- 已基于 `claude-remote-workflow` 做过一次真实项目案例测试，并与 gstack 风格方法做了对比审计

## 案例对比结论

- Byte 套件在端到端交付包和管理层可读性上更强
- gstack 风格方法在纯工程架构收敛和硬边界表达上更强
- 推荐用法：默认先用 Byte 做规划、评审和管理层打包；遇到高风险工程设计时，再补一遍 gstack 风格的 engineering pass

## 相关文档

- 审计总报告：`audits/2026-03-27-byte-vs-gstack-audit.md`
- Byte 案例输出：`audits/case-study-byte-output.md`
- gstack 案例输出：`audits/case-study-gstack-output.md`
