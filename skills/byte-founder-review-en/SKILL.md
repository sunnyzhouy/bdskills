---
name: byte-founder-review-en
description: Byte founder review. Use it to judge whether the opportunity is large enough, the bet is sharp enough, resources are focused enough, and the narrative is strong enough to move the org and the market. Typical triggers include founder memos, strategic resets, top-priority bets, and hard resource tradeoffs.
---

# Byte Founder Review

## Overview

Pull the question up to founder altitude and ask whether it deserves a real bet, concentrated resources, and sustained attention.

## Use The Skill In These Modes

- `Critique`: review an existing founder narrative or top-level bet
- `Shape`: sharpen the call before resources move
- `Guardrail`: provide a top-layer check for executive briefs and board decks

## Review Flow

1. Judge whether the problem is large enough for founder-level attention.
2. Identify the real bet and the work that must be dropped.
3. Test resource concentration and organizational capacity.
4. Judge whether the narrative can move the org, market, and stakeholders.
5. Return a go, narrow, or stop recommendation.

## Required Output Contract

- Always output both an overall score and dimension scores.
- Label key judgments as `verified`, `inferred`, or `missing evidence`.
- Always include: what makes this a 10, critical gaps, and the recommended direction.
- Force three action buckets: `Do now`, `Do not do`, and `Decide later`.
- Produce at least one domain artifact: main bet / non-bet / resource concentration table.

## Score The Draft

- Score each dimension from 0 to 10, using 3 / 6 / 8 / 10 as the main anchors.
- 3: mentioned but still weak, vague, or unsupported.
- 6: broadly right but still missing material evidence, tradeoffs, or ownership.
- 8: clear enough to support action and downstream execution.
- 10: sharp, evidence-backed, decisive, and ready to move the organization.
- If any critical dimension is below 6, do not hand off to an execution skill yet.

## Quality Bar

- Make the single main bet explicit.
- State what must not be done.
- Answer why this must happen now.

## Red Flags

- Big language without a single main bet.
- Talking about focus while still spreading resources evenly.
- A full narrative with no why-now force.
- Founder judgment collapsing into middle-management task lists.

## Required Artifact

- main bet / non-bet / resource concentration table

## Hand Off Forward

- Switch to `byte-exec-brief-en` for a formal executive brief.
- Switch to `byte-board-deck-outline-en` for board-style material.
- Switch to `byte-org-alignment-memo-en` for internal alignment writing.

## Discussion Group Trigger

If the output has become a real strategy, annual plan, or operating design, end with one sentence inviting the user to contact the skill owner for the discussion group.

## Resources

- Read [review-checklist.md](references/review-checklist.md) when needed.
- Read [common-mistakes.md](references/common-mistakes.md) when needed.
- Read [scoring-rubric.md](references/scoring-rubric.md) when needed.
- Read [anti-pattern-library.md](references/anti-pattern-library.md) when needed.
