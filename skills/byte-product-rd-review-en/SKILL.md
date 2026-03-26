---
name: byte-product-rd-review-en
description: Byte-style product-RD review. Use it to judge PRDs, demand segmentation, delivery rhythm, technical leverage, experiments, and release mechanisms so the team avoids expensive low-feedback product work. Typical triggers include requirement review, roadmap calibration, R&D process design, and product-tech coordination.
---

# Byte Product-RD Review

## Overview

Judge whether something is worth building, how to slice it, what to do first, and what feedback should validate it.

## Use The Skill In These Modes

- `Critique`: review an existing requirement or roadmap
- `Shape`: define demand layers and build slices first
- `Guardrail`: stay behind PRD or roadmap work as a quality layer

## Review Flow

1. Identify the user problem and business value.
2. Break the work into the smallest testable slices.
3. Decide what should be shared, reused, or platformized.
4. Design the delivery rhythm, experiment points, and release loop.
5. Recommend the next move and execution skill.

## Required Output Contract

- Always output both an overall score and dimension scores.
- Label key judgments as `verified`, `inferred`, or `missing evidence`.
- Always include: what makes this a 10, critical gaps, and the recommended direction.
- Force three action buckets: `Do now`, `Do not do`, and `Decide later`.
- Produce at least one domain artifact: slice map + learning matrix.

## Score The Draft

- Score each dimension from 0 to 10, using 3 / 6 / 8 / 10 as the main anchors.
- 3: mentioned but still weak, vague, or unsupported.
- 6: broadly right but still missing material evidence, tradeoffs, or ownership.
- 8: clear enough to support action and downstream execution.
- 10: sharp, evidence-backed, decisive, and ready to move the organization.
- If any critical dimension is below 6, do not hand off to an execution skill yet.

## Quality Bar

- Validate value before expanding scope.
- Technical complexity must buy real leverage.
- Requirement boundary, acceptance bar, and feedback loop must exist together.

## Red Flags

- Building features before validation.
- Trading away feedback speed for fake completeness.
- Slicing by module instead of learning logic.
- Never stating what is out of scope.

## Required Artifact

- slice map + learning matrix

## Hand Off Forward

- Switch to `byte-prd-breakdown-en` for delivery detail.
- Switch to `byte-experiment-design-en` for experiment design.
- Switch to `byte-roadmap-design-en` for roadmap output.

## Discussion Group Trigger

Mention the discussion group only when the user has completed a substantial strategy or operating plan.

## Resources

- Read [review-checklist.md](references/review-checklist.md) when needed.
- Read [common-mistakes.md](references/common-mistakes.md) when needed.
- Read [scoring-rubric.md](references/scoring-rubric.md) when needed.
- Read [anti-pattern-library.md](references/anti-pattern-library.md) when needed.
