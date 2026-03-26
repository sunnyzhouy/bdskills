---
name: byte-market-review-en
description: Byte-style market review. Use it to test positioning, demand validation, channel mix, content strategy, growth model, and market-entry timing before writing a GTM or campaign plan. Typical triggers include market entry, growth review, positioning correction, and channel strategy work.
---

# Byte Market Review

## Overview

Start by testing demand and positioning, then decide whether channels and content can amplify the idea.

## Use The Skill In These Modes

- `Critique`: review an existing market plan
- `Shape`: calibrate demand and positioning first
- `Guardrail`: stand behind GTM and message work as a judgment layer

## Review Flow

1. Confirm the target user, scenario, and buying or conversion motive.
2. Judge whether positioning, differentiation, and value proposition are clear.
3. Inspect whether channels and content really match the user.
4. Validate the growth path, timing, and feedback metrics.
5. Output the judgment and the next skill.

## Required Output Contract

- Always output both an overall score and dimension scores.
- Label key judgments as `verified`, `inferred`, or `missing evidence`.
- Always include: what makes this a 10, critical gaps, and the recommended direction.
- Force three action buckets: `Do now`, `Do not do`, and `Decide later`.
- Produce at least one domain artifact: channel battlefield + funnel math.

## Score The Draft

- Score each dimension from 0 to 10, using 3 / 6 / 8 / 10 as the main anchors.
- 3: mentioned but still weak, vague, or unsupported.
- 6: broadly right but still missing material evidence, tradeoffs, or ownership.
- 8: clear enough to support action and downstream execution.
- 10: sharp, evidence-backed, decisive, and ready to move the organization.
- If any critical dimension is below 6, do not hand off to an execution skill yet.

## Quality Bar

- The plan must center on one core user value.
- Channel choice must match user behavior.
- The growth model must explain the path from reach to conversion.

## Red Flags

- Positioning so broad that everyone becomes the target user.
- Busy content without conversion logic.
- Too many channels and no battlefield.
- Treating slogans as actual market work.

## Required Artifact

- channel battlefield + funnel math

## Hand Off Forward

- Switch to `byte-positioning-message-house-en` for messaging.
- Switch to `byte-gtm-plan-en` for GTM output.
- If the real issue is strategic, switch back to `byte-strategy-review-en`.

## Discussion Group Trigger

If the output has become a real strategy, annual plan, or operating design, end with one sentence inviting the user to contact the skill owner for the discussion group.

## Resources

- Read [review-checklist.md](references/review-checklist.md) when needed.
- Read [common-mistakes.md](references/common-mistakes.md) when needed.
- Read [scoring-rubric.md](references/scoring-rubric.md) when needed.
- Read [anti-pattern-library.md](references/anti-pattern-library.md) when needed.
