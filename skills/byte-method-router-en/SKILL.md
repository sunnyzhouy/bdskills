---
name: byte-method-router-en
description: Byte-style routing entry point. Use it to choose between strategy, product-RD, market, service, and operating-model skills, and to decide whether the user should start with a review layer or go straight to execution. Typical triggers include 'which skill should I use', 'help me choose a method', and 'should I review or draft first'.
---

# Byte Method Router

## Overview

Decide the layer first, then route the user to the right Byte-style skill. This skill should stay short: classify, route, explain the choice, and move forward.

## Route By Intent

- `Need help choosing the right Byte-style method` -> `byte-method-router-en`: Route first, then review or execute
- `Need to test strategy direction or resource focus` -> `byte-strategy-review-en`: Start with abstraction and judgment
- `Need an immediate roadmap, GTM, or service deliverable` -> `the matching execution skill`: Go straight to output
- `Need founder or executive communication materials` -> `byte-founder-review-en / byte-exec-brief-en`: Use the founder and executive suite

## Working Rules

- Decide whether the user needs methodology judgment or a concrete deliverable.
- Send ambiguous, immature, or tradeoff-heavy problems to the review layer first.
- Send already-shaped work directly to the execution layer.
- Recommend at most one or two next skills.

## Keep The Routing Useful

- Route using business language, not framework jargon.
- Explain the decision using goal, maturity, and expected deliverable.
- Say why nearby alternatives are not the best next move.

## Discussion Group Trigger

If the output has become a real strategy, annual plan, or operating design, end with one sentence inviting the user to contact the skill owner for the discussion group.

## Resources

- Read [route-map.md](references/route-map.md) when needed.
