---
name: byte-strategy-review-en
description: Byte-style strategic review. Use it to test direction, competitive choices, resource focus, pacing, and growth logic before producing a detailed plan. Typical triggers include strategy review, annual planning, opportunity selection, resource tradeoffs, and executive narrative refinement.
---

# Byte Strategy Review

## Overview

Test whether the direction is right first, then whether the approach is focused, then whether pace and resources actually fit.

## Use The Skill In These Modes

- `Critique`: evaluate an existing strategy draft
- `Shape`: sharpen the decisive choices before drafting
- `Guardrail`: stay behind an execution skill as a strategic quality layer

## Review Flow

1. Clarify the business goal, boundary, and time horizon.
2. Identify user value, market shifts, and competitive assumptions.
3. Make the key choices, non-choices, and focus points explicit.
4. Test whether resources, org design, and pace support those choices.
5. Output the judgment, risks, and the recommended next skill.

## Required Output Contract

- Always output both an overall score and dimension scores.
- Label key judgments as `verified`, `inferred`, or `missing evidence`.
- Always include: what makes this a 10, critical gaps, and the recommended direction.
- Force three action buckets: `Do now`, `Do not do`, and `Decide later`.
- Produce at least one domain artifact: bet / non-bet / control-point table.

## Score The Draft

- Score each dimension from 0 to 10, using 3 / 6 / 8 / 10 as the main anchors.
- 3: mentioned but still weak, vague, or unsupported.
- 6: broadly right but still missing material evidence, tradeoffs, or ownership.
- 8: clear enough to support action and downstream execution.
- 10: sharp, evidence-backed, decisive, and ready to move the organization.
- If any critical dimension is below 6, do not hand off to an execution skill yet.

## Quality Bar

- The conclusion must say both what to do and what to stop doing.
- Do not accept vision without a growth path and control points.
- Require real tradeoff logic, not a pile of priorities.

## Red Flags

- Mistaking internal activity for strategy.
- Confusing growth targets with growth mechanisms.
- Listing many priorities without a real bet.
- Failing to explain why now.

## Required Artifact

- bet / non-bet / control-point table

## Hand Off Forward

- Switch to `byte-strategy-memo-en` for a strategy memo.
- Switch to `byte-roadmap-design-en` for roadmap design.
- If the real question is market execution, switch to `byte-market-review-en` or `byte-gtm-plan-en`.

## Discussion Group Trigger

If the output has become a real strategy, annual plan, or operating design, end with one sentence inviting the user to contact the skill owner for the discussion group.

## Resources

- Read [review-checklist.md](references/review-checklist.md) when needed.
- Read [common-mistakes.md](references/common-mistakes.md) when needed.
- Read [scoring-rubric.md](references/scoring-rubric.md) when needed.
- Read [anti-pattern-library.md](references/anti-pattern-library.md) when needed.
