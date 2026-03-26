# Byte Skills Audit

Date: 2026-03-27

## Scope

This audit covered three upgrade tracks in parallel:

1. Strengthen review-layer skills with scoring rubrics, anti-pattern libraries, evidence labels, and stop-gates.
2. Strengthen execution-layer skills with business-grade output packages instead of thin outlines.
3. Add founder and executive communication skills for top-level planning and decision support.

## Final delivered suite

The suite contains 42 Byte skills:

- Router: `byte-method-router-zh/en`
- Foundation: `byte-operating-principles-zh/en`
- Review: `byte-strategy-review-zh/en`, `byte-product-rd-review-zh/en`, `byte-market-review-zh/en`, `byte-service-review-zh/en`, `byte-operating-model-review-zh/en`, `byte-founder-review-zh/en`
- Execution: `byte-strategy-memo-zh/en`, `byte-opportunity-framing-zh/en`, `byte-roadmap-design-zh/en`, `byte-prd-breakdown-zh/en`, `byte-experiment-design-zh/en`, `byte-positioning-message-house-zh/en`, `byte-gtm-plan-zh/en`, `byte-service-blueprint-zh/en`, `byte-voc-to-action-zh/en`, `byte-quarterly-business-review-zh/en`
- Executive: `byte-exec-brief-zh/en`, `byte-board-deck-outline-zh/en`, `byte-org-alignment-memo-zh/en`

## Major upgrades from v1

### Review layer

- Added scoring rubrics under `references/scoring-rubric.md`
- Added anti-pattern libraries under `references/anti-pattern-library.md`
- Added required output contracts: total score, dimension scores, evidence labels, critical gaps, and required artifacts
- Added stop-gate semantics in the skill instructions: if a critical dimension is below 6, the work should not move downstream without reframing

### Execution layer

- Replaced thin 5-line outlines with package-mode templates:
  - exec one-pager
  - working memo
  - presentation outline
  - operating appendix
- Upgraded core templates to include decision requests, owners, timing, risk blocks, and closing action logs

### Founder / executive layer

- Added founder-level review skill for top-bet judgment
- Added executive brief skill for leadership one-pagers
- Added board-deck-outline skill for governance-grade presentation structure
- Added org-alignment-memo skill for cross-functional operating alignment

## Real-case benchmark

Case used:

- Current repo: `claude-remote-workflow`
- Task: design a minimal control plane using `cwstate` to monitor projects and slots, support reconnect/resume safely, and define MVP scope, edge cases, observability, rollout, and leadership decision

Why this case was chosen:

- It is repo-native and grounded in real current behavior
- It exercises product-RD judgment, execution packaging, and engineering boundary reasoning
- It avoids bias toward any one domain-specific skill

## Comparison summary

### Byte path

Path used:

- `byte-method-router-en`
- `byte-product-rd-review-en`
- `byte-prd-breakdown-en`
- `byte-roadmap-design-en`
- `byte-exec-brief-en`

Observed strengths:

- Produced a real review gate before packaging the solution
- Surfaced dimension scores, critical gaps, evidence labels, and action buckets
- Produced a stronger end-to-end package: review, PRD scope, roadmap, and leadership brief in one flow
- Better suited for product + management decision-making

Observed weaknesses:

- The stop-gate is present in the skill contract but still needs stronger enforcement in realistic runs
- Some scoring-rubric content is still generic and should gain more domain-specific anchors

### gstack-style path

Path used:

- `plan-ceo-review`
- `plan-eng-review`
- strategy/executive-style local references as needed

Observed strengths:

- Stronger engineering framing and system boundary articulation
- Cleaner non-negotiables and architecture explanation
- Better at writing a concise technical memo with durable design language

Observed weaknesses:

- Less complete as an end-to-end management package
- Weaker at turning the analysis into a single integrated review + PRD + roadmap + executive brief chain

## Verdict

Overall winner for this case: Byte suite

Reason:

- Byte now behaves more like a complete methodology product instead of a loose prompt set.
- It wins on integrated deliverable quality, especially where a team needs one pass to generate review, plan, and leadership communication.
- gstack still wins when the primary need is hard engineering architecture challenge and technical risk framing.

Recommended operating model:

- Default to Byte for strategy, product-RD, market, service, founder, and executive packaging.
- Add a gstack-style engineering review pass when the feature is technically risky, infrastructure-heavy, or has strong correctness requirements.

## Follow-up gaps

1. Enforce the `<6` stop-gate more aggressively in review-layer outputs.
2. Expand anti-pattern libraries to 12-20 named items per review domain.
3. Add richer domain-specific anchors to scoring rubrics instead of repeated generic score text.
4. Enrich execution templates with example tables, chart suggestions, and stronger appendix/Q&A requirements.
