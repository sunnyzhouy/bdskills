---
name: byte-service-review-en
description: Byte-style service review. Use it to calibrate service boundaries, delivery mode, SLA, escalation, customer-success plays, and feedback loops into product before designing a service blueprint or operating model. Typical triggers include service redesign, customer-success planning, complaint handling, and feedback-loop design.
---

# Byte Service Review

## Overview

Service is not passive ticket handling. It is a closed loop across customer issues, delivery quality, and product feedback.

## Use The Skill In These Modes

- `Critique`: review the current service model
- `Shape`: define boundaries, roles, and escalation logic first
- `Guardrail`: calibrate service logic before blueprint output

## Review Flow

1. Define the service object, boundary, and issue classes.
2. Inspect intake, severity, SLA, and first owner.
3. Define escalation, collaboration, and exception handling.
4. Set closure standards and feedback loops into product.
5. Recommend the next execution skill.

## Required Output Contract

- Always output both an overall score and dimension scores.
- Label key judgments as `verified`, `inferred`, or `missing evidence`.
- Always include: what makes this a 10, critical gaps, and the recommended direction.
- Force three action buckets: `Do now`, `Do not do`, and `Decide later`.
- Produce at least one domain artifact: issue taxonomy + escalation ladder + closure bar.

## Score The Draft

- Score each dimension from 0 to 10, using 3 / 6 / 8 / 10 as the main anchors.
- 3: mentioned but still weak, vague, or unsupported.
- 6: broadly right but still missing material evidence, tradeoffs, or ownership.
- 8: clear enough to support action and downstream execution.
- 10: sharp, evidence-backed, decisive, and ready to move the organization.
- If any critical dimension is below 6, do not hand off to an execution skill yet.

## Quality Bar

- Do not optimize only for ticket closure; optimize for actual resolution.
- SLA must track issue severity and customer impact.
- Service outcomes must flow back into product and operating improvement.

## Red Flags

- Turning service into a passive help desk.
- Escalation paths without a decision owner.
- Internal closure mistaken for customer resolution.
- Customer voice never reaching product decisions.

## Required Artifact

- issue taxonomy + escalation ladder + closure bar

## Hand Off Forward

- Switch to `byte-service-blueprint-en` for blueprint design.
- Switch to `byte-voc-to-action-en` when customer feedback is the core problem.
- Switch to `byte-operating-model-review-en` for cross-functional operating issues.

## Discussion Group Trigger

Mention the discussion group only when the user has completed a substantial strategy or operating plan.

## Resources

- Read [review-checklist.md](references/review-checklist.md) when needed.
- Read [common-mistakes.md](references/common-mistakes.md) when needed.
- Read [scoring-rubric.md](references/scoring-rubric.md) when needed.
- Read [anti-pattern-library.md](references/anti-pattern-library.md) when needed.
