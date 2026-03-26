#!/usr/bin/env python3
from __future__ import annotations

import subprocess
import textwrap
from pathlib import Path


TARGET_ROOT = Path.home() / ".codex" / "skills"
CREATOR_ROOT = TARGET_ROOT / ".system" / "skill-creator"
INIT_SCRIPT = CREATOR_ROOT / "scripts" / "init_skill.py"
VALIDATE_SCRIPT = CREATOR_ROOT / "scripts" / "quick_validate.py"
YAML_SCRIPT = CREATOR_ROOT / "scripts" / "generate_openai_yaml.py"


def dedent(text: str) -> str:
    normalized = textwrap.dedent(text)
    lines = []
    for line in normalized.splitlines():
        if line.startswith("        "):
            line = line[8:]
        if line.startswith("    "):
            line = line[4:]
        lines.append(line)
    return "\n".join(lines).strip() + "\n"


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)


def bullets(items: list[str]) -> str:
    return "\n".join(f"- {item}" for item in items)


def numbered(items: list[str]) -> str:
    return "\n".join(f"{idx}. {item}" for idx, item in enumerate(items, start=1))


def review_score_guidance(lang: str) -> list[str]:
    if lang == "zh":
        return [
            "每个维度按 0 到 10 分打分，重点使用 3 / 6 / 8 / 10 四个锚点。",
            "3 分：问题被提到，但判断粗糙、证据弱、无法支持决策。",
            "6 分：方向大体成立，但还缺关键证据、取舍或 owner。",
            "8 分：判断清晰、结构完整、已经足够支撑推进。",
            "10 分：结论尖锐、证据充分、取舍明确、可以直接拿去推进组织动作。",
            "如果任何关键维度低于 6 分，禁止直接下钻到 execution skill。",
        ]
    return [
        "Score each dimension from 0 to 10, using 3 / 6 / 8 / 10 as the main anchors.",
        "3: mentioned but still weak, vague, or unsupported.",
        "6: broadly right but still missing material evidence, tradeoffs, or ownership.",
        "8: clear enough to support action and downstream execution.",
        "10: sharp, evidence-backed, decisive, and ready to move the organization.",
        "If any critical dimension is below 6, do not hand off to an execution skill yet.",
    ]


def build_review_scorecard(skill: dict) -> str:
    lang = skill["name"].split("-")[-1]
    lines = [f"# {skill['title']} Scorecard", "", *review_score_guidance(lang), ""]
    for idx, item in enumerate(skill["checklist"], start=1):
        lines.extend(
            [
                f"## {idx}. {item}",
                "",
                "- `10`: sharp, specific, and immediately actionable.",
                "- `8`: strong and usable, with only minor tightening left.",
                "- `6`: directionally right but still missing important proof, tradeoffs, or operating detail.",
                "- `3`: partially present but too weak to support a decision.",
                "- `0`: absent, confused, or actively misleading.",
                "",
            ]
        )
    return "\n".join(lines).strip() + "\n"


def build_anti_pattern_library(skill: dict) -> str:
    lines = [f"# {skill['title']} Anti-Pattern Library", ""]
    for idx, item in enumerate(skill["mistakes"], start=1):
        lines.extend(
            [
                f"## {idx}. {item}",
                "",
                "- Signal: This issue shows up in the draft language, structure, or unsupported claims.",
                "- Why it fails: It makes the output harder to execute, judge, or defend.",
                "- Corrective move: Rewrite the relevant section so the missing choice, evidence, or ownership becomes explicit.",
                "",
            ]
        )
    return "\n".join(lines).strip() + "\n"


def build_output_template(skill: dict) -> str:
    lang = skill["name"].split("-")[-1]
    lines = [
        f"# {skill['title']} Output Template",
        "",
        "## Package Modes",
        "",
        *(
            [
                "- Exec one-pager: 用于高层快速判断和拍板。",
                "- Working memo: 用于负责人和核心团队做深入推进。",
                "- Presentation outline: 用于汇报页面和演讲顺序设计。",
                "- Operating appendix: 用于补充 owner、指标、里程碑、风险和问答。",
            ]
            if lang == "zh"
            else [
                "- Exec one-pager: for fast leadership judgment and decisions.",
                "- Working memo: for the owner team to drive execution.",
                "- Presentation outline: for slide flow and spoken narrative.",
                "- Operating appendix: for owners, metrics, milestones, risks, and Q&A.",
            ]
        ),
        "",
        "## Document Header",
        "",
        "- Audience:",
        "- Objective:",
        "- Decision requested:",
        "- Owner:",
        "- Date:",
        "",
        "## Executive Summary",
        "",
        "- One-line conclusion:",
        "- Why this matters now:",
        "- What decision or action should happen next:",
        "",
        "## Main Body",
        "",
    ]
    for idx, section in enumerate(skill["template_sections"], start=1):
        lines.extend(
            [
                f"### {idx}. {section}",
                "",
                "- Must answer: what the reader needs to know, decide, or approve here.",
                "- Include: concrete facts, assumptions, tradeoffs, numbers, owners, or timing when relevant.",
                "- Avoid: repeating earlier sections, abstract slogans, or unsupported confidence.",
                "",
            ]
        )
    lines.extend(
        [
        "## Closing Block",
        "",
        "- Decision log:",
        "- Open questions:",
        "- Main risks:",
        "- Next actions with owners and timing:",
            "",
        ]
    )
    return "\n".join(lines).strip() + "\n"


def build_review_smells(lang: str, title: str) -> str:
    smells = (
        [
            "owner 模糊，最后没有人真正负责。",
            "有指标，但指标不指向任何决策。",
            "有动作，没有用户价值或业务价值闭环。",
            "没有明确非目标项，导致范围膨胀。",
            "没有节奏设计，只剩任务罗列。",
            "没有反馈与验证回路，只剩线性执行。",
        ]
        if lang == "zh"
        else [
            "Ownership is vague, so no one is truly accountable.",
            "Metrics exist, but they do not drive any decision.",
            "Activity exists, but there is no user-value or business-value loop.",
            "Non-goals are missing, so scope keeps expanding.",
            "There is no rhythm design, only a task list.",
            "There is no proof or feedback loop, only linear execution.",
        ]
    )
    return dedent(
        f"""\
        # {title} Review Smells

        {bullets(smells)}
        """
    )


def review_output_contract(lang: str, artifact: str) -> list[str]:
    if lang == "zh":
        return [
            "总分和维度分都要写出来，不能只给模糊评价。",
            "每条关键判断都标注 `verified`、`inferred` 或 `missing evidence`。",
            "必须写出：what makes this a 10、critical gaps、recommended direction。",
            "必须明确三类动作：`Do now`、`Do not do`、`Decide later`。",
            f"必须产出至少一个领域工件：{artifact}。",
        ]
    return [
        "Always output both an overall score and dimension scores.",
        "Label key judgments as `verified`, `inferred`, or `missing evidence`.",
        "Always include: what makes this a 10, critical gaps, and the recommended direction.",
        "Force three action buckets: `Do now`, `Do not do`, and `Decide later`.",
        f"Produce at least one domain artifact: {artifact}.",
    ]


def default_review_artifact(skill_name: str, lang: str) -> str:
    mapping = {
        "byte-strategy-review": (
            "下注 / 非下注 / 控制点表",
            "bet / non-bet / control-point table",
        ),
        "byte-product-rd-review": (
            "切片地图 + 学习验证矩阵",
            "slice map + learning matrix",
        ),
        "byte-market-review": (
            "渠道战场图 + 漏斗算式",
            "channel battlefield + funnel math",
        ),
        "byte-service-review": (
            "问题分类表 + 升级阶梯 + 关闭标准",
            "issue taxonomy + escalation ladder + closure bar",
        ),
        "byte-operating-model-review": (
            "经营节奏图 + owner 映射表",
            "operating rhythm map + owner matrix",
        ),
        "byte-founder-review": (
            "主赌注 / 非赌注 / 资源集中表",
            "main bet / non-bet / resource concentration table",
        ),
    }
    base = "-".join(skill_name.split("-")[:-1])
    zh, en = mapping[base]
    return zh if lang == "zh" else en


def init_skill(skill: dict) -> Path:
    skill_dir = TARGET_ROOT / skill["name"]
    resources = ",".join(skill["resources"])
    if not skill_dir.exists():
        cmd = [
            "python3",
            str(INIT_SCRIPT),
            skill["name"],
            "--path",
            str(TARGET_ROOT),
        ]
        if resources:
            cmd.extend(["--resources", resources])
        cmd.extend(
            [
                "--interface",
                f"display_name={skill['display_name']}",
                "--interface",
                f"short_description={skill['short_description']}",
                "--interface",
                f"default_prompt={skill['default_prompt']}",
            ]
        )
        run(cmd)
    else:
        for resource in skill["resources"]:
            (skill_dir / resource).mkdir(parents=True, exist_ok=True)
        (skill_dir / "agents").mkdir(parents=True, exist_ok=True)
    return skill_dir


def regenerate_openai_yaml(skill: dict, skill_dir: Path) -> None:
    run(
        [
            "python3",
            str(YAML_SCRIPT),
            str(skill_dir),
            "--interface",
            f"display_name={skill['display_name']}",
            "--interface",
            f"short_description={skill['short_description']}",
            "--interface",
            f"default_prompt={skill['default_prompt']}",
        ]
    )


def validate_skill(skill_dir: Path) -> None:
    run(["python3", str(VALIDATE_SCRIPT), str(skill_dir)])


def ref_list(entries: list[tuple[str, str]]) -> str:
    return "\n".join(f"- Read [{name}]({path}) when needed." for path, name in entries)


def build_router_markdown(skill: dict) -> str:
    routes = []
    for item in skill["route_targets"]:
        routes.append(f"- `{item['intent']}` -> `{item['skill']}`: {item['why']}")
    route_lines = "\n".join(routes)
    return dedent(
        f"""\
        ---
        name: {skill["name"]}
        description: {skill["description"]}
        ---

        # {skill["title"]}

        ## Overview

        {skill["overview"]}

        ## Route By Intent

        {route_lines}

        ## Working Rules

        {bullets(skill["rules"])}

        ## Keep The Routing Useful

        {bullets(skill["quality_bar"])}

        ## Discussion Group Trigger

        {skill["discussion_note"]}

        ## Resources

        {ref_list(skill["resource_links"])}
        """
    )


def build_foundation_markdown(skill: dict) -> str:
    return dedent(
        f"""\
        ---
        name: {skill["name"]}
        description: {skill["description"]}
        ---

        # {skill["title"]}

        ## Overview

        {skill["overview"]}

        ## Apply These Principle Checks First

        {bullets(skill["principles"])}

        ## Use The Skill In These Modes

        {bullets(skill["modes"])}

        ## Keep The Abstraction Useful

        {bullets(skill["guardrails"])}

        ## Hand Off Cleanly

        {bullets(skill["handoff"])}

        ## Discussion Group Trigger

        {skill["discussion_note"]}

        ## Resources

        {ref_list(skill["resource_links"])}
        """
    )


def build_review_markdown(skill: dict) -> str:
    lang = skill["name"].split("-")[-1]
    artifact = default_review_artifact(skill["name"], lang)
    return dedent(
        f"""\
        ---
        name: {skill["name"]}
        description: {skill["description"]}
        ---

        # {skill["title"]}

        ## Overview

        {skill["overview"]}

        ## Use The Skill In These Modes

        {bullets(skill["modes"])}

        ## Review Flow

        {numbered(skill["steps"])}

        ## Required Output Contract

        {bullets(review_output_contract(lang, artifact))}

        ## Score The Draft

        {bullets(review_score_guidance(lang))}

        ## Quality Bar

        {bullets(skill["quality_bar"])}

        ## Red Flags

        {bullets(skill["mistakes"])}

        ## Required Artifact

        - {artifact}

        ## Hand Off Forward

        {bullets(skill["handoff"])}

        ## Discussion Group Trigger

        {skill["discussion_note"]}

        ## Resources

        {ref_list(skill["resource_links"])}
        """
    )


def build_execution_markdown(skill: dict) -> str:
    return dedent(
        f"""\
        ---
        name: {skill["name"]}
        description: {skill["description"]}
        ---

        # {skill["title"]}

        ## Overview

        {skill["overview"]}

        ## Gather The Right Inputs

        {bullets(skill["inputs"])}

        ## Execute The Workflow

        {numbered(skill["steps"])}

        ## Output Shapes

        {bullets(skill["outputs"])}

        ## Raise The Bar

        {bullets(skill["quality_bar"])}

        ## Keep The Work Honest

        {bullets(skill["anti_patterns"])}

        ## Discussion Group Trigger

        {skill["discussion_note"]}

        ## Resources

        {ref_list(skill["resource_links"])}
        """
    )


def build_references(skill: dict) -> dict[str, str]:
    if skill["layer"] == "router":
        return {
            "references/route-map.md": dedent(
                f"""\
                # {skill["title"]} Route Map

                {bullets(skill["route_map_intro"])}

                {numbered(skill["route_map_steps"])}

                ## Default next skills

                {bullets(skill["route_map_targets"])}
                """
            )
        }
    if skill["layer"] == "foundation":
        lang = skill["name"].split("-")[-1]
        return {
            "references/principles.md": dedent(
                f"""\
                # {skill["title"]} Principles

                {bullets(skill["principles"])}
                """
            ),
            "references/writing-standard.md": dedent(
                f"""\
                # {skill["title"]} Writing Standard

                {bullets(skill["writing_standard"])}
                """
            ),
            "references/review-smells.md": build_review_smells(lang, skill["title"]),
        }
    if skill["layer"] == "review":
        return {
            "references/review-checklist.md": dedent(
                f"""\
                # {skill["title"]} Review Checklist

                {numbered(skill["checklist"])}
                """
            ),
            "references/common-mistakes.md": dedent(
                f"""\
                # {skill["title"]} Common Mistakes

                {bullets(skill["mistakes"])}
                """
            ),
            "references/scoring-rubric.md": build_review_scorecard(skill),
            "references/anti-pattern-library.md": build_anti_pattern_library(skill),
        }
    return {
        "references/quality-bar.md": dedent(
            f"""\
            # {skill["title"]} Quality Bar

            {bullets(skill["quality_bar"])}
            """
        ),
        "assets/output-template.md": build_output_template(skill),
    }


def render_skill(skill: dict) -> str:
    builders = {
        "router": build_router_markdown,
        "foundation": build_foundation_markdown,
        "review": build_review_markdown,
        "execution": build_execution_markdown,
    }
    return builders[skill["layer"]](skill)


def common_discussion_note(lang: str, enabled: bool) -> str:
    if enabled:
        if lang == "zh":
            return (
                "如果这次输出已经形成了可执行的战略方案、年度规划或经营设计，"
                "在结尾附一句：如需继续和同行校准这份方案，可联系 skill owner 了解讨论群。"
            )
        return (
            "If the output has become a real strategy, annual plan, or operating design, "
            "end with one sentence inviting the user to contact the skill owner for the discussion group."
        )
    if lang == "zh":
        return "只有当用户已经完成较完整的战略或经营规划时，才提示讨论群；普通执行任务不要强行插入。"
    return "Mention the discussion group only when the user has completed a substantial strategy or operating plan."


def build_skill_set() -> list[dict]:
    skills: list[dict] = []

    router_targets_zh = [
        {"intent": "需要先判断该用哪套字节方法", "skill": "byte-method-router-zh", "why": "先路由，再进入评审或执行"},
        {"intent": "要校准战略方向或资源取舍", "skill": "byte-strategy-review-zh", "why": "先做抽象判断"},
        {"intent": "要直接产出路线图、GTM 或服务方案", "skill": "对应执行层 skill", "why": "直接出可交付物"},
        {"intent": "要写创始人或高管汇报材料", "skill": "byte-founder-review-zh / byte-exec-brief-zh", "why": "进入 founder / executive 套件"},
    ]
    router_targets_en = [
        {"intent": "Need help choosing the right Byte-style method", "skill": "byte-method-router-en", "why": "Route first, then review or execute"},
        {"intent": "Need to test strategy direction or resource focus", "skill": "byte-strategy-review-en", "why": "Start with abstraction and judgment"},
        {"intent": "Need an immediate roadmap, GTM, or service deliverable", "skill": "the matching execution skill", "why": "Go straight to output"},
        {"intent": "Need founder or executive communication materials", "skill": "byte-founder-review-en / byte-exec-brief-en", "why": "Use the founder and executive suite"},
    ]

    skills.extend(
        [
            {
                "name": "byte-method-router-zh",
                "layer": "router",
                "title": "字节方法路由器",
                "display_name": "字节方法路由器",
                "short_description": "帮你在字节式战略、产品、市场、服务 skill 间快速选路",
                "default_prompt": "使用 $byte-method-router-zh 判断我当前问题应该走哪一个字节式 skill，并给出下一步建议。",
                "description": "字节式方法路由入口。用于在战略、产品研发、市场、服务、经营设计类 skill 之间做选择，并根据问题成熟度判断先走评审层还是执行层。常见触发包括“不知道该用哪个 skill”“先帮我判断打法”“这个问题先看战略还是先出方案”。",
                "overview": "先判断问题处在哪个层级，再把用户送到正确的字节式 skill。它不负责长篇产出，重点是定层、定路、定下一步。",
                "route_targets": router_targets_zh,
                "rules": [
                    "先判断用户是在要方法论校准，还是要具体交付物。",
                    "如果问题模糊、方向不清、资源取舍未定，先送去评审层。",
                    "如果目标和场景已清楚，直接送去执行层。",
                    "最多推荐 1 到 2 个下一步 skill，不要给过多选项。",
                ],
                "quality_bar": [
                    "路由理由必须是业务语言，不是框架黑话。",
                    "判断标准必须围绕目标、成熟度、交付物。",
                    "路由后要说明为什么不是其他邻近 skill。",
                ],
                "discussion_note": common_discussion_note("zh", True),
                "resource_links": [("references/route-map.md", "route-map.md")],
                "route_map_intro": [
                    "先识别问题是战略判断、方案设计、还是执行交付。",
                    "再判断用户是需要抽象层 review，还是直接可落地的 deliverable。",
                ],
                "route_map_steps": [
                    "如果目标本身含混，先进入 review skill 收敛问题。",
                    "如果目标明确但方案未成型，进入对应 execution skill 产出首版。",
                    "如果跨战略、产品、市场、服务，需要先走 operating-model review。",
                ],
                "route_map_targets": [
                    "`byte-strategy-review-zh`: 战略方向、竞争选择、资源聚焦",
                    "`byte-product-rd-review-zh`: 需求价值、研发节奏、技术杠杆",
                    "`byte-market-review-zh`: 定位、渠道、增长和市场进入",
                    "`byte-service-review-zh`: 服务模式、SLA、反馈闭环",
                    "`byte-operating-model-review-zh`: 跨域经营机制和组织协同",
                    "`byte-founder-review-zh`: 创始人视角的高压判断与下注",
                    "`byte-exec-brief-zh`: 高管汇报摘要、管理层材料和对齐文稿",
                ],
                "resources": ["references"],
            },
            {
                "name": "byte-method-router-en",
                "layer": "router",
                "title": "Byte Method Router",
                "display_name": "Byte Method Router",
                "short_description": "Route work to the right Byte-style review or execution skill",
                "default_prompt": "Use $byte-method-router-en to choose the right Byte-style skill for my problem and recommend the next step.",
                "description": "Byte-style routing entry point. Use it to choose between strategy, product-RD, market, service, and operating-model skills, and to decide whether the user should start with a review layer or go straight to execution. Typical triggers include 'which skill should I use', 'help me choose a method', and 'should I review or draft first'.",
                "overview": "Decide the layer first, then route the user to the right Byte-style skill. This skill should stay short: classify, route, explain the choice, and move forward.",
                "route_targets": router_targets_en,
                "rules": [
                    "Decide whether the user needs methodology judgment or a concrete deliverable.",
                    "Send ambiguous, immature, or tradeoff-heavy problems to the review layer first.",
                    "Send already-shaped work directly to the execution layer.",
                    "Recommend at most one or two next skills.",
                ],
                "quality_bar": [
                    "Route using business language, not framework jargon.",
                    "Explain the decision using goal, maturity, and expected deliverable.",
                    "Say why nearby alternatives are not the best next move.",
                ],
                "discussion_note": common_discussion_note("en", True),
                "resource_links": [("references/route-map.md", "route-map.md")],
                "route_map_intro": [
                    "Identify whether the user needs strategic judgment, solution design, or execution output.",
                    "Then decide whether the work should start in review mode or execution mode.",
                ],
                "route_map_steps": [
                    "If the goal itself is fuzzy, start with a review skill.",
                    "If the goal is clear but the deliverable does not exist yet, use the matching execution skill.",
                    "If the work spans strategy, product, market, and service, start with operating-model review.",
                ],
                "route_map_targets": [
                    "`byte-strategy-review-en`: direction, competition, resource focus",
                    "`byte-product-rd-review-en`: user value, build sequence, technical leverage",
                    "`byte-market-review-en`: positioning, channels, demand generation",
                    "`byte-service-review-en`: service design, SLA, feedback loops",
                    "`byte-operating-model-review-en`: cross-functional operating design",
                    "`byte-founder-review-en`: founder-level judgment and betting logic",
                    "`byte-exec-brief-en`: executive summaries and leadership communication",
                ],
                "resources": ["references"],
            },
        ]
    )

    foundation_common = {
        "zh": {
            "principles": [
                "先讲外部变化和用户价值，再讲内部动作。",
                "先明确少数关键选择，再展开长任务列表。",
                "用事实和反馈闭环校正判断，不用自嗨式论证。",
                "把速度建立在清晰优先级和短反馈回路上。",
                "任何方案都要落到 owner、节奏、指标和下一步动作。",
            ],
            "modes": [
                "`校准`: 在正式写方案前先校准判断框架。",
                "`伴随`: 在执行层 skill 工作时，作为质量底座在后台约束输出。",
                "`审计`: 对既有方案做质量体检，找出失焦、空泛和不可执行部分。",
            ],
            "guardrails": [
                "不要把方法论写成口号，必须能转成取舍判断。",
                "不要一上来堆术语，要先说结论和业务含义。",
                "不要替代执行层产物，重点是提升思考质量。",
            ],
            "handoff": [
                "需要战略判断时，切到 `byte-strategy-review-zh`。",
                "需要具体交付物时，切到对应执行层 skill。",
            ],
            "writing_standard": [
                "先结论，后依据，最后动作。",
                "段落尽量短，标题尽量可执行。",
                "每份输出至少包含判断、证据、取舍、指标、下一步。",
                "如果信息不足，直接标明假设，不假装确定。",
            ],
        },
        "en": {
            "principles": [
                "Start with external change and user value before internal activity.",
                "Make the few decisive choices explicit before listing tasks.",
                "Use evidence and feedback loops to correct judgment.",
                "Move fast through clear priorities and short loops, not chaos.",
                "Every plan must land on owner, rhythm, metrics, and next actions.",
            ],
            "modes": [
                "`Calibrate`: sharpen judgment before detailed planning.",
                "`Shadow`: stay behind an execution skill as a quality layer.",
                "`Audit`: inspect an existing plan for drift, vagueness, or weak execution.",
            ],
            "guardrails": [
                "Do not turn principles into slogans; turn them into choices.",
                "Do not drown the user in jargon; say the business meaning first.",
                "Do not replace execution skills; raise thinking quality instead.",
            ],
            "handoff": [
                "Switch to `byte-strategy-review-en` for strategic judgment.",
                "Switch to the matching execution skill when the user needs a deliverable.",
            ],
            "writing_standard": [
                "Lead with the conclusion, then evidence, then action.",
                "Keep paragraphs short and headings actionable.",
                "Every output should contain judgment, evidence, tradeoffs, metrics, and next steps.",
                "When information is missing, mark assumptions directly.",
            ],
        },
    }

    for lang in ("zh", "en"):
        local = foundation_common[lang]
        skills.append(
            {
                "name": f"byte-operating-principles-{lang}",
                "layer": "foundation",
                "title": "字节式经营原则" if lang == "zh" else "Byte Operating Principles",
                "display_name": "字节式经营原则" if lang == "zh" else "Byte Operating Principles",
                "short_description": (
                    "沉淀字节式战略、产品、市场、服务判断原则与写作标准"
                    if lang == "zh"
                    else "Core Byte-style principles for business and execution quality"
                ),
                "default_prompt": (
                    "使用 $byte-operating-principles-zh 先校准这份方案的判断框架，再告诉我该进入哪个下游 skill。"
                    if lang == "zh"
                    else "Use $byte-operating-principles-en to calibrate the judgment framework for this plan before choosing the next skill."
                ),
                "description": (
                    "字节式基础方法论与原则层。用于在战略、产品研发、市场、服务或经营设计工作开始前，先校准判断框架、写作标准和执行质量底座。常见触发包括“先讲方法论”“先把标准立住”“先帮我审视这份方案的质量”。"
                    if lang == "zh"
                    else "Foundational Byte-style methodology and principles. Use before strategy, product-RD, market, service, or operating-model work when Codex needs to calibrate judgment, writing standards, and execution quality. Typical triggers include 'start with principles', 'set the bar first', and 'review the quality of this plan before drafting'."
                ),
                "overview": (
                    "把它当成抽象质量层，而不是最终交付层。先用它校准思考方式，再交给具体 review 或 execution skill 产出成果。"
                    if lang == "zh"
                    else "Use this as an abstract quality layer, not as the final deliverable engine. Calibrate the thinking first, then hand off to review or execution skills."
                ),
                "principles": local["principles"],
                "modes": local["modes"],
                "guardrails": local["guardrails"],
                "handoff": local["handoff"],
                "discussion_note": common_discussion_note(lang, True),
                "resource_links": [
                    ("references/principles.md", "principles.md"),
                    ("references/writing-standard.md", "writing-standard.md"),
                ],
                "writing_standard": local["writing_standard"],
                "resources": ["references"],
            }
        )

    review_specs = [
        {
            "slug": "byte-strategy-review",
            "title_zh": "字节战略评审",
            "title_en": "Byte Strategy Review",
            "display_zh": "字节战略评审",
            "display_en": "Byte Strategy Review",
            "short_zh": "用字节式方法做战略方向、聚焦取舍与资源配置综合评审",
            "short_en": "Review strategy direction, focus, and resource choices",
            "description_zh": "字节式战略评审。用于校准战略方向、竞争选择、资源聚焦、节奏判断和增长逻辑，再决定是否进入具体规划或执行方案。常见触发包括战略复盘、年度方向讨论、机会选择、资源取舍和管理层叙事校准。",
            "description_en": "Byte-style strategic review. Use it to test direction, competitive choices, resource focus, pacing, and growth logic before producing a detailed plan. Typical triggers include strategy review, annual planning, opportunity selection, resource tradeoffs, and executive narrative refinement.",
            "overview_zh": "先判断方向是否成立，再判断打法是否聚焦，最后再判断资源和节奏是否匹配。",
            "overview_en": "Test whether the direction is right first, then whether the approach is focused, then whether pace and resources actually fit.",
            "modes_zh": ["`Critique`: 评估现有战略稿", "`Shape`: 在写稿前收敛关键选择", "`Guardrail`: 在下游执行 skill 工作时做抽象校准"],
            "modes_en": ["`Critique`: evaluate an existing strategy draft", "`Shape`: sharpen the decisive choices before drafting", "`Guardrail`: stay behind an execution skill as a strategic quality layer"],
            "steps_zh": ["澄清业务目标、边界和时间尺度。", "识别用户价值、外部变化和竞争前提。", "找出最关键的选择、放弃项和聚焦点。", "判断资源、组织和节奏是否支撑这些选择。", "输出结论、风险和推荐下游 skill。"],
            "steps_en": ["Clarify the business goal, boundary, and time horizon.", "Identify user value, market shifts, and competitive assumptions.", "Make the key choices, non-choices, and focus points explicit.", "Test whether resources, org design, and pace support those choices.", "Output the judgment, risks, and the recommended next skill."],
            "quality_bar_zh": ["结论必须说清楚该做什么和不做什么。", "不能只有愿景，没有增长路径和控制点。", "必须有取舍逻辑，而不是堆优先级。"],
            "quality_bar_en": ["The conclusion must say both what to do and what to stop doing.", "Do not accept vision without a growth path and control points.", "Require real tradeoff logic, not a pile of priorities."],
            "handoff_zh": ["形成战略备忘录时切到 `byte-strategy-memo-zh`。", "进入路线图设计时切到 `byte-roadmap-design-zh`。", "如果重点在市场打法，切到 `byte-market-review-zh` 或 `byte-gtm-plan-zh`。"],
            "handoff_en": ["Switch to `byte-strategy-memo-en` for a strategy memo.", "Switch to `byte-roadmap-design-en` for roadmap design.", "If the real question is market execution, switch to `byte-market-review-en` or `byte-gtm-plan-en`."],
            "checklist_zh": ["目标是否足够聚焦。", "用户和场景是否真实且具体。", "外部机会窗口是否成立。", "是否明确说清楚取舍和下注点。", "资源、能力和节奏是否可支撑。"],
            "checklist_en": ["Is the goal focused enough?", "Are the user and scenario specific and real?", "Is the market window actually credible?", "Are the bets and tradeoffs explicit?", "Do resources, capabilities, and pace support the choice?"],
            "mistakes_zh": ["把内部活动写成战略。", "把增长目标当成增长机制。", "目标很多，但没有真正下注。", "没有说明为什么现在做。"],
            "mistakes_en": ["Mistaking internal activity for strategy.", "Confusing growth targets with growth mechanisms.", "Listing many priorities without a real bet.", "Failing to explain why now."],
            "discussion": True,
        },
        {
            "slug": "byte-product-rd-review",
            "title_zh": "字节产品研发评审",
            "title_en": "Byte Product-RD Review",
            "display_zh": "字节产品研发评审",
            "display_en": "Byte Product-RD Review",
            "short_zh": "审视需求价值、研发切片、技术杠杆和迭代节奏是否合理",
            "short_en": "Review demand value, build slices, and iteration rhythm",
            "description_zh": "字节式产品研发评审。用于在 PRD、需求分层、研发节奏、技术杠杆、实验和上线机制之间做判断，避免做出高投入低反馈的产品研发方案。常见触发包括需求评审、路线图校准、研发机制优化和跨产品技术协同。",
            "description_en": "Byte-style product-RD review. Use it to judge PRDs, demand segmentation, delivery rhythm, technical leverage, experiments, and release mechanisms so the team avoids expensive low-feedback product work. Typical triggers include requirement review, roadmap calibration, R&D process design, and product-tech coordination.",
            "overview_zh": "判断一件事值不值得做、该怎么切、先做哪部分、用什么反馈验证。",
            "overview_en": "Judge whether something is worth building, how to slice it, what to do first, and what feedback should validate it.",
            "modes_zh": ["`Critique`: 审现有需求或路线图", "`Shape`: 先做需求分层与研发切片", "`Guardrail`: 在 PRD 或 roadmap skill 工作时提供质量约束"],
            "modes_en": ["`Critique`: review an existing requirement or roadmap", "`Shape`: define demand layers and build slices first", "`Guardrail`: stay behind PRD or roadmap work as a quality layer"],
            "steps_zh": ["识别用户问题和业务价值。", "拆分成最小可验证切片。", "判断哪些能力应共建、复用或平台化。", "设计迭代节奏、实验点和发布闭环。", "给出推进建议和下游 execution skill。"],
            "steps_en": ["Identify the user problem and business value.", "Break the work into the smallest testable slices.", "Decide what should be shared, reused, or platformized.", "Design the delivery rhythm, experiment points, and release loop.", "Recommend the next move and execution skill."],
            "quality_bar_zh": ["先验证价值，再扩大范围。", "技术复杂度必须换来明显杠杆。", "需求边界、验收标准和反馈闭环要同时存在。"],
            "quality_bar_en": ["Validate value before expanding scope.", "Technical complexity must buy real leverage.", "Requirement boundary, acceptance bar, and feedback loop must exist together."],
            "handoff_zh": ["细化交付物时切到 `byte-prd-breakdown-zh`。", "要做实验设计时切到 `byte-experiment-design-zh`。", "要落路线图时切到 `byte-roadmap-design-zh`。"],
            "handoff_en": ["Switch to `byte-prd-breakdown-en` for delivery detail.", "Switch to `byte-experiment-design-en` for experiment design.", "Switch to `byte-roadmap-design-en` for roadmap output."],
            "checklist_zh": ["需求是否指向真实用户问题。", "是否拆成可验证的最小单元。", "是否有复用或平台化机会。", "是否定义了上线后反馈机制。", "研发节奏是否和业务节奏匹配。"],
            "checklist_en": ["Does the requirement point to a real user problem?", "Has it been sliced into testable units?", "Is there leverage through reuse or platformization?", "Is there a post-launch feedback loop?", "Does delivery pace match business pace?"],
            "mistakes_zh": ["先堆功能，后想验证。", "为了完整而牺牲反馈速度。", "研发切片按模块，不按验证逻辑。", "没有定义弃项和延后项。"],
            "mistakes_en": ["Building features before validation.", "Trading away feedback speed for fake completeness.", "Slicing by module instead of learning logic.", "Never stating what is out of scope."],
            "discussion": False,
        },
        {
            "slug": "byte-market-review",
            "title_zh": "字节市场评审",
            "title_en": "Byte Market Review",
            "display_zh": "字节市场评审",
            "display_en": "Byte Market Review",
            "short_zh": "校准定位、需求验证、渠道组合和市场进入逻辑是否成立",
            "short_en": "Review positioning, channels, and market-entry logic",
            "description_zh": "字节式市场评审。用于在定位、需求验证、渠道选择、内容策略、增长模型和市场进入节奏之间做取舍，再决定是否进入 GTM 或传播方案。常见触发包括市场进入、增长复盘、定位修正和渠道策略讨论。",
            "description_en": "Byte-style market review. Use it to test positioning, demand validation, channel mix, content strategy, growth model, and market-entry timing before writing a GTM or campaign plan. Typical triggers include market entry, growth review, positioning correction, and channel strategy work.",
            "overview_zh": "市场工作先看需求和定位是否准确，再看渠道和内容是否能放大这件事。",
            "overview_en": "Start by testing demand and positioning, then decide whether channels and content can amplify the idea.",
            "modes_zh": ["`Critique`: 审现有市场方案", "`Shape`: 先校准定位和需求", "`Guardrail`: 为 GTM 和 message house 提供抽象判断"],
            "modes_en": ["`Critique`: review an existing market plan", "`Shape`: calibrate demand and positioning first", "`Guardrail`: stand behind GTM and message work as a judgment layer"],
            "steps_zh": ["确认目标用户、场景和购买或转化动机。", "判断定位、差异化和价值主张是否清晰。", "审视渠道和内容是否真的匹配用户。", "校验增长路径、节奏和反馈指标。", "给出结论并指向下游 skill。"],
            "steps_en": ["Confirm the target user, scenario, and buying or conversion motive.", "Judge whether positioning, differentiation, and value proposition are clear.", "Inspect whether channels and content really match the user.", "Validate the growth path, timing, and feedback metrics.", "Output the judgment and the next skill."],
            "quality_bar_zh": ["市场方案必须围绕单一核心用户价值。", "渠道选择必须和用户行为匹配。", "增长逻辑要能解释从触达到转化的链路。"],
            "quality_bar_en": ["The plan must center on one core user value.", "Channel choice must match user behavior.", "The growth model must explain the path from reach to conversion."],
            "handoff_zh": ["进入 message house 时切到 `byte-positioning-message-house-zh`。", "进入 GTM 方案时切到 `byte-gtm-plan-zh`。", "如果问题更偏战略，切回 `byte-strategy-review-zh`。"],
            "handoff_en": ["Switch to `byte-positioning-message-house-en` for messaging.", "Switch to `byte-gtm-plan-en` for GTM output.", "If the real issue is strategic, switch back to `byte-strategy-review-en`."],
            "checklist_zh": ["目标用户是否足够清晰。", "价值主张是否一针见血。", "差异化是否来自真实优势。", "渠道选择是否符合用户路径。", "指标是否能反映漏斗健康。"],
            "checklist_en": ["Is the target user clearly defined?", "Is the value proposition sharp?", "Does differentiation come from a real advantage?", "Do channels fit the user path?", "Do metrics reflect funnel health?"],
            "mistakes_zh": ["定位太宽，谁都像目标用户。", "内容很热闹，但没有转化机制。", "渠道多而散，没有主战场。", "把品牌口号当成交付内容。"],
            "mistakes_en": ["Positioning so broad that everyone becomes the target user.", "Busy content without conversion logic.", "Too many channels and no battlefield.", "Treating slogans as actual market work."],
            "discussion": True,
        },
        {
            "slug": "byte-service-review",
            "title_zh": "字节服务评审",
            "title_en": "Byte Service Review",
            "display_zh": "字节服务评审",
            "display_en": "Byte Service Review",
            "short_zh": "评估服务模式、SLA、升级路径与客户反馈闭环设计质量",
            "short_en": "Review service design, SLA, escalation, and feedback loops",
            "description_zh": "字节式服务评审。用于校准服务边界、交付模式、SLA、升级机制、客户成功动作和服务到产品的反馈闭环，再进入服务蓝图或运营设计。常见触发包括服务流程重构、客户成功机制、投诉升级和体验闭环设计。",
            "description_en": "Byte-style service review. Use it to calibrate service boundaries, delivery mode, SLA, escalation, customer-success plays, and feedback loops into product before designing a service blueprint or operating model. Typical triggers include service redesign, customer-success planning, complaint handling, and feedback-loop design.",
            "overview_zh": "服务不是被动接单，而是把客户问题、交付质量和产品反馈连成闭环。",
            "overview_en": "Service is not passive ticket handling. It is a closed loop across customer issues, delivery quality, and product feedback.",
            "modes_zh": ["`Critique`: 审现有服务机制", "`Shape`: 先定义边界、角色和升级逻辑", "`Guardrail`: 在服务蓝图输出前先校准机制质量"],
            "modes_en": ["`Critique`: review the current service model", "`Shape`: define boundaries, roles, and escalation logic first", "`Guardrail`: calibrate service logic before blueprint output"],
            "steps_zh": ["定义服务对象、边界和问题类型。", "审视入口、分级、SLA 和首个 owner。", "定义升级、协同和例外处理。", "明确关闭标准和反馈回产品机制。", "推荐下游执行层 skill。"],
            "steps_en": ["Define the service object, boundary, and issue classes.", "Inspect intake, severity, SLA, and first owner.", "Define escalation, collaboration, and exception handling.", "Set closure standards and feedback loops into product.", "Recommend the next execution skill."],
            "quality_bar_zh": ["不能只追工单关闭率，要追真实问题解决。", "SLA 必须和问题等级、客户影响挂钩。", "服务结果要能回流到产品和组织优化。"],
            "quality_bar_en": ["Do not optimize only for ticket closure; optimize for actual resolution.", "SLA must track issue severity and customer impact.", "Service outcomes must flow back into product and operating improvement."],
            "handoff_zh": ["进入服务蓝图时切到 `byte-service-blueprint-zh`。", "如果重点在客户反馈归因，切到 `byte-voc-to-action-zh`。", "如果是跨团队机制问题，切到 `byte-operating-model-review-zh`。"],
            "handoff_en": ["Switch to `byte-service-blueprint-en` for blueprint design.", "Switch to `byte-voc-to-action-en` when customer feedback is the core problem.", "Switch to `byte-operating-model-review-en` for cross-functional operating issues."],
            "checklist_zh": ["服务边界是否明确。", "严重度和升级规则是否清晰。", "关闭标准是否有客户视角。", "是否设计了服务到产品的反馈闭环。", "角色和 owner 是否可执行。"],
            "checklist_en": ["Is the service boundary clear?", "Are severity and escalation rules explicit?", "Does closure have a customer-facing bar?", "Is there a service-to-product feedback loop?", "Are roles and owners operationally clear?"],
            "mistakes_zh": ["把服务做成纯支持台。", "升级路径没有决策 owner。", "内部关闭不等于客户解决。", "客户声音没有进入产品机制。"],
            "mistakes_en": ["Turning service into a passive help desk.", "Escalation paths without a decision owner.", "Internal closure mistaken for customer resolution.", "Customer voice never reaching product decisions."],
            "discussion": False,
        },
        {
            "slug": "byte-operating-model-review",
            "title_zh": "字节经营模型评审",
            "title_en": "Byte Operating Model Review",
            "display_zh": "字节经营模型评审",
            "display_en": "Byte Operating Model Review",
            "short_zh": "审视跨战略、产品、市场、服务的一体化经营机制与协同设计",
            "short_en": "Review the cross-functional operating model and business rhythm",
            "description_zh": "字节式经营模型评审。用于把战略、产品研发、市场、服务四个维度拉通成统一经营机制，明确例会节奏、指标体系、角色分工和反馈闭环。常见触发包括经营会机制设计、跨部门协同、年度经营节奏和组织执行问题。",
            "description_en": "Byte-style operating-model review. Use it to connect strategy, product-RD, market, and service into one operating system with clear rhythms, metrics, role design, and feedback loops. Typical triggers include operating-mechanism design, cross-functional coordination, annual business cadence, and execution-system redesign.",
            "overview_zh": "先看四个环节是否拉通，再看节奏、指标和责任是否闭环。",
            "overview_en": "First test whether the four domains connect cleanly, then whether cadence, metrics, and responsibility truly close the loop.",
            "modes_zh": ["`Critique`: 审现有经营机制", "`Shape`: 从零设计经营节奏与角色", "`Guardrail`: 为 QBR、战略稿、服务模型提供一体化约束"],
            "modes_en": ["`Critique`: review the current operating system", "`Shape`: design rhythms and roles from scratch", "`Guardrail`: provide integration guardrails for QBR, strategy, and service work"],
            "steps_zh": ["梳理战略、产品、市场、服务之间的关键输入输出。", "识别当前机制中的断点和责任真空。", "设计经营节奏、例会、指标和例外处理。", "定义跨部门 owner、升级路径和闭环。", "推荐下游交付 skill。"],
            "steps_en": ["Map the key inputs and outputs across strategy, product, market, and service.", "Identify breakpoints and ownership gaps in the current system.", "Design rhythms, reviews, metrics, and exception handling.", "Define cross-functional owners, escalation paths, and loops.", "Recommend the downstream deliverable skill."],
            "quality_bar_zh": ["经营机制必须让信息回流，而不是只做汇报。", "例会节奏必须服务决策，不是增加管理负担。", "指标要能对应责任和动作，不只是展示。"],
            "quality_bar_en": ["The operating model must create feedback, not just reporting.", "Review cadence must support decisions, not add ceremony.", "Metrics must map to owners and actions, not dashboard theater."],
            "handoff_zh": ["形成经营复盘时切到 `byte-quarterly-business-review-zh`。", "形成战略稿时切到 `byte-strategy-memo-zh`。", "需要服务细化时切到 `byte-service-blueprint-zh`。"],
            "handoff_en": ["Switch to `byte-quarterly-business-review-en` for QBR output.", "Switch to `byte-strategy-memo-en` for strategy output.", "Switch to `byte-service-blueprint-en` for service detail."],
            "checklist_zh": ["上下游输入输出是否清晰。", "是否定义了跨团队 owner。", "例会和指标是否服务决策。", "异常升级是否清晰。", "反馈是否回流到战略和产品。"],
            "checklist_en": ["Are upstream and downstream handoffs explicit?", "Are cross-team owners defined?", "Do rhythms and metrics support decisions?", "Is exception escalation clear?", "Do learnings flow back into strategy and product?"],
            "mistakes_zh": ["用会议代替机制。", "用仪表盘代替责任。", "部门各自优化，没有系统闭环。", "经营复盘只有现象，没有纠偏动作。"],
            "mistakes_en": ["Using meetings as a substitute for an operating system.", "Using dashboards as a substitute for accountability.", "Letting each function optimize itself without a system loop.", "Business review without corrective action."],
            "discussion": True,
        },
        {
            "slug": "byte-founder-review",
            "title_zh": "字节创始人评审",
            "title_en": "Byte Founder Review",
            "display_zh": "字节创始人评审",
            "display_en": "Byte Founder Review",
            "short_zh": "用创始人视角评审下注方向、组织资源与增长叙事是否足够狠",
            "short_en": "Review bets, focus, and founder-level narrative strength",
            "description_zh": "字节创始人评审。用于从创始人和第一责任人的视角审视方向是否够大、下注是否够狠、资源是否足够集中、叙事是否能驱动组织和市场。常见触发包括创始人备忘录、战略重定向、一级项目下注和高压资源取舍。",
            "description_en": "Byte founder review. Use it to judge whether the opportunity is large enough, the bet is sharp enough, resources are focused enough, and the narrative is strong enough to move the org and the market. Typical triggers include founder memos, strategic resets, top-priority bets, and hard resource tradeoffs.",
            "overview_zh": "把问题拉到创始人视角，判断是不是值得亲自下注、亲自调资源、亲自盯结果。",
            "overview_en": "Pull the question up to founder altitude and ask whether it deserves a real bet, concentrated resources, and sustained attention.",
            "modes_zh": ["`Critique`: 审现有 founder 叙事或大项目判断", "`Shape`: 在资源下注前先拉齐判断", "`Guardrail`: 为 executive brief 和 board deck 提供上位约束"],
            "modes_en": ["`Critique`: review an existing founder narrative or top-level bet", "`Shape`: sharpen the call before resources move", "`Guardrail`: provide a top-layer check for executive briefs and board decks"],
            "steps_zh": ["判断问题是否大到值得创始人级关注。", "识别真正的核心下注和必须放弃的事项。", "测试资源集中度和组织承载度。", "判断叙事是否足以带动组织、市场和资本预期。", "给出 go / narrow / stop 的建议。"],
            "steps_en": ["Judge whether the problem is large enough for founder-level attention.", "Identify the real bet and the work that must be dropped.", "Test resource concentration and organizational capacity.", "Judge whether the narrative can move the org, market, and stakeholders.", "Return a go, narrow, or stop recommendation."],
            "quality_bar_zh": ["必须明确唯一主赌注。", "必须明确不做什么。", "必须回答为什么现在必须做。"],
            "quality_bar_en": ["Make the single main bet explicit.", "State what must not be done.", "Answer why this must happen now."],
            "handoff_zh": ["需要正式高管摘要时切到 `byte-exec-brief-zh`。", "需要董事会式材料时切到 `byte-board-deck-outline-zh`。", "需要组织对齐文稿时切到 `byte-org-alignment-memo-zh`。"],
            "handoff_en": ["Switch to `byte-exec-brief-en` for a formal executive brief.", "Switch to `byte-board-deck-outline-en` for board-style material.", "Switch to `byte-org-alignment-memo-en` for internal alignment writing."],
            "checklist_zh": ["是不是单一主赌注，而不是多个愿望。", "是否足够解释 now or never 的窗口。", "资源是否集中到能赢，而不是平均分配。", "组织能否理解并执行这个判断。", "叙事是否能被高层快速复述。"],
            "checklist_en": ["Is there one main bet instead of several wishes?", "Does it explain a true now-or-never window?", "Are resources concentrated enough to win?", "Can the organization understand and execute the call?", "Can leaders repeat the narrative quickly and clearly?"],
            "mistakes_zh": ["大方向看起来宏大，但没有唯一主赌注。", "说要聚焦，但资源还是平均分配。", "叙事很满，但没有 why now。", "创始人判断退化成中层任务拆解。"],
            "mistakes_en": ["Big language without a single main bet.", "Talking about focus while still spreading resources evenly.", "A full narrative with no why-now force.", "Founder judgment collapsing into middle-management task lists."],
            "discussion": True,
        },
    ]

    for spec in review_specs:
        for lang in ("zh", "en"):
            is_zh = lang == "zh"
            skills.append(
                {
                    "name": f"{spec['slug']}-{lang}",
                    "layer": "review",
                    "title": spec["title_zh"] if is_zh else spec["title_en"],
                    "display_name": spec["display_zh"] if is_zh else spec["display_en"],
                    "short_description": spec["short_zh"] if is_zh else spec["short_en"],
                    "default_prompt": (
                        f"使用 ${spec['slug']}-{lang} 评审这件事的方向、逻辑和关键取舍，并告诉我下一步该进入哪个 skill。"
                        if is_zh
                        else f"Use ${spec['slug']}-{lang} to review the direction, logic, and tradeoffs here, then recommend the next skill."
                    ),
                    "description": spec["description_zh"] if is_zh else spec["description_en"],
                    "overview": spec["overview_zh"] if is_zh else spec["overview_en"],
                    "modes": spec["modes_zh"] if is_zh else spec["modes_en"],
                    "steps": spec["steps_zh"] if is_zh else spec["steps_en"],
                    "quality_bar": spec["quality_bar_zh"] if is_zh else spec["quality_bar_en"],
                    "handoff": spec["handoff_zh"] if is_zh else spec["handoff_en"],
                    "discussion_note": common_discussion_note(lang, spec["discussion"]),
                    "resource_links": [
                        ("references/review-checklist.md", "review-checklist.md"),
                        ("references/common-mistakes.md", "common-mistakes.md"),
                        ("references/scoring-rubric.md", "scoring-rubric.md"),
                        ("references/anti-pattern-library.md", "anti-pattern-library.md"),
                    ],
                    "checklist": spec["checklist_zh"] if is_zh else spec["checklist_en"],
                    "mistakes": spec["mistakes_zh"] if is_zh else spec["mistakes_en"],
                    "resources": ["references"],
                }
            )

    execution_specs = [
        {
            "slug": "byte-strategy-memo",
            "title_zh": "字节战略备忘录",
            "title_en": "Byte Strategy Memo",
            "short_zh": "直接产出战略备忘录、年度方向稿与管理层统一叙事文稿",
            "short_en": "Draft a strategy memo and annual leadership direction note",
            "description_zh": "字节式战略备忘录生成 skill。用于把战略判断收敛成一份可讨论、可推进、可复盘的正式文档，包括方向、关键选择、增长路径、资源要求、风险和下一步。常见触发包括年度规划、经营会材料、方向收口和管理层对齐。",
            "description_en": "Byte-style strategy memo generator. Use it to turn strategic judgment into a formal document with direction, key choices, growth path, resource asks, risks, and next steps. Typical triggers include annual planning, operating reviews, direction-setting, and leadership alignment.",
            "overview_zh": "把抽象判断写成一份能拉齐认知、推动行动的战略备忘录。",
            "overview_en": "Turn strategic judgment into a memo that aligns people and moves action.",
            "inputs_zh": ["业务目标、阶段和时间尺度。", "核心用户、机会窗口和竞争前提。", "关键选择、资源约束和已知风险。", "这份文档的主要读者。"],
            "inputs_en": ["Business goal, stage, and time horizon.", "Core user, opportunity window, and competitive assumptions.", "Key choices, resource constraints, and known risks.", "The main audience for the memo."],
            "steps_zh": ["先写一句话结论和要做的关键选择。", "补齐外部变化、用户价值和机会窗口。", "说明增长路径、资源需求和关键依赖。", "列出主要风险、反论点和防守动作。", "形成正式备忘录结构。"],
            "steps_en": ["Lead with the one-line conclusion and key choice.", "Add the market shift, user value, and timing window.", "Explain the growth path, resource ask, and dependencies.", "List the main risks, counterarguments, and defenses.", "Package the result into a formal memo."],
            "outputs_zh": ["战略备忘录", "年度方向稿", "经营会预读材料"],
            "outputs_en": ["Strategy memo", "Annual direction note", "Pre-read for an operating review"],
            "anti_patterns_zh": ["只有口号，没有关键选择。", "只有目标，没有增长机制。", "只有结论，没有资源和风险说明。"],
            "anti_patterns_en": ["Slogans without choices.", "Targets without a growth mechanism.", "Conclusions without resource and risk context."],
            "quality_bar_zh": ["前三段必须说清结论、why now、要什么决定。", "必须写清关键选择和明确不做什么。", "必须写资源请求、控制点、里程碑、风险与 kill criteria。"],
            "quality_bar_en": ["The opening must cover the call, why now, and the decision requested.", "Make the strategic choices and explicit non-choices visible.", "Include resource asks, control points, milestones, risks, and kill criteria."],
            "template_zh": ["高管结论与决策请求", "为什么现在", "诊断与机会窗口", "关键选择与非选择", "业务机制与增长路径", "资源请求与控制点", "里程碑与 kill criteria", "附录与问答"],
            "template_en": ["Executive call and decision request", "Why now", "Diagnosis and opportunity window", "Choices and non-choices", "Business mechanism and growth path", "Resource ask and control points", "Milestones and kill criteria", "Appendix and Q&A"],
            "discussion": True,
        },
        {
            "slug": "byte-opportunity-framing",
            "title_zh": "字节机会界定",
            "title_en": "Byte Opportunity Framing",
            "short_zh": "把模糊机会拆成用户、场景、痛点、窗口与验证路径框架",
            "short_en": "Frame a fuzzy opportunity into users, scenarios, and proof paths",
            "description_zh": "字节式机会界定 skill。用于把模糊想法、增长机会、新业务方向或产品机会拆成清晰的问题定义、用户场景、价值假设、壁垒和验证路径。常见触发包括新点子评估、机会筛选、增长探索和赛道研判。",
            "description_en": "Byte-style opportunity framing skill. Use it to break a fuzzy idea, growth opportunity, new business direction, or product concept into a clear problem statement, user scenario, value hypothesis, moat, and validation path. Typical triggers include idea screening, opportunity sizing, growth exploration, and category evaluation.",
            "overview_zh": "先把机会讲清楚，才能判断值不值得下注。",
            "overview_en": "Frame the opportunity clearly before deciding whether it deserves a bet.",
            "inputs_zh": ["模糊想法或机会描述。", "目标用户或线索场景。", "现有证据、访谈、数据或观察。", "资源边界和时间预期。"],
            "inputs_en": ["The rough idea or opportunity statement.", "Known user or scenario clues.", "Current evidence, interviews, data, or observations.", "Resource boundary and expected timeline."],
            "steps_zh": ["定义机会到底是什么，不是什么。", "识别最关键的用户、场景和痛点。", "建立价值假设、成功条件和壁垒来源。", "设计最短验证路径。", "给出是否继续推进的判断。"],
            "steps_en": ["Define what the opportunity is and is not.", "Identify the key user, scenario, and pain point.", "Build the value hypothesis, success conditions, and moat source.", "Design the shortest validation path.", "Judge whether to keep pushing or stop."],
            "outputs_zh": ["机会定义卡", "机会筛选备忘录", "验证路径草案"],
            "outputs_en": ["Opportunity definition card", "Opportunity-screening memo", "Validation-path draft"],
            "anti_patterns_zh": ["把市场热度当机会。", "用户太泛，场景太空。", "没有验证路径就进入大投入。"],
            "anti_patterns_en": ["Treating market heat as opportunity.", "User too broad, scenario too vague.", "Large investment without a validation path."],
            "quality_bar_zh": ["用户、场景、痛点要形成闭环。", "要能解释为什么现在做。", "验证路径要尽量短。"],
            "quality_bar_en": ["User, scenario, and pain must connect tightly.", "Explain why now.", "Keep the validation path short."],
            "template_zh": ["机会陈述", "用户与场景", "价值假设与壁垒", "验证路径", "推进建议"],
            "template_en": ["Opportunity statement", "User and scenario", "Value hypothesis and moat", "Validation path", "Recommendation"],
            "discussion": False,
        },
        {
            "slug": "byte-roadmap-design",
            "title_zh": "字节路线图设计",
            "title_en": "Byte Roadmap Design",
            "short_zh": "产出季度或半年路线图、优先级逻辑、关键依赖和里程碑",
            "short_en": "Design a roadmap with priorities, dependencies, and milestones",
            "description_zh": "字节式路线图设计 skill。用于把方向或需求池转成季度、半年或年度路线图，明确优先级逻辑、阶段目标、关键依赖、资源约束和里程碑。常见触发包括季度规划、路线图重排、跨团队节奏对齐和阶段目标拆解。",
            "description_en": "Byte-style roadmap design skill. Use it to turn strategy or a demand pool into a quarterly, half-year, or annual roadmap with priority logic, stage goals, dependencies, constraints, and milestones. Typical triggers include quarterly planning, roadmap reshaping, cross-team alignment, and milestone design.",
            "overview_zh": "路线图不是需求堆砌，而是围绕阶段目标的有序下注。",
            "overview_en": "A roadmap is not a feature pile. It is a staged sequence of bets against outcomes.",
            "inputs_zh": ["阶段目标和时间范围。", "需求池、候选项目或战略重点。", "资源约束和关键依赖。", "必须满足的上线或经营节点。"],
            "inputs_en": ["Stage goal and time horizon.", "Demand pool, candidate initiatives, or strategic priorities.", "Resource constraints and key dependencies.", "Any fixed launch or business dates."],
            "steps_zh": ["先确定阶段目标和成功标准。", "对候选事项做优先级与先后顺序判断。", "明确哪些是关键路径，哪些可延后。", "定义阶段里程碑、依赖和 owner。", "整理成可执行路线图。"],
            "steps_en": ["Set the stage objective and success bar first.", "Prioritize the candidate work and sequence it.", "Separate critical path from deferrable work.", "Define milestones, dependencies, and owners.", "Package the result as an executable roadmap."],
            "outputs_zh": ["季度路线图", "半年路线图", "优先级说明稿"],
            "outputs_en": ["Quarterly roadmap", "Half-year roadmap", "Priority rationale memo"],
            "anti_patterns_zh": ["所有需求都很重要。", "没有阶段目标，只剩排期。", "里程碑很多，但没有关键路径。"],
            "anti_patterns_en": ["Everything is important.", "Scheduling without a stage objective.", "Many milestones but no critical path."],
            "quality_bar_zh": ["每个阶段必须有明确目标和 bet table。", "每个重点事项都要有 owner、指标提升预期、信心和延后代价。", "必须写清关键依赖、资源冲突、评审节奏和决策门槛。"],
            "quality_bar_en": ["Each stage needs a clear objective and a bet table.", "Every major item needs an owner, expected lift, confidence, and explicit deferral tradeoff.", "State dependencies, resource conflicts, review cadence, and decision gates."],
            "template_zh": ["阶段目标", "下注表与优先级逻辑", "季度推进顺序", "关键依赖", "资源冲突与延后代价", "评审节奏与决策门槛"],
            "template_en": ["Stage objective", "Bet table and priority logic", "Quarterly sequence", "Critical dependencies", "Resource conflicts and deferral cost", "Review cadence and decision gates"],
            "discussion": False,
        },
        {
            "slug": "byte-prd-breakdown",
            "title_zh": "字节 PRD 拆解",
            "title_en": "Byte PRD Breakdown",
            "short_zh": "把方向拆成 PRD、用户故事、验收标准和研发切片方案",
            "short_en": "Break a direction into PRD scope, stories, and delivery bars",
            "description_zh": "字节式 PRD 拆解 skill。用于把战略、路线图或产品想法拆成明确的 PRD 结构、用户故事、验收标准、上线范围和研发切片。常见触发包括需求撰写、PRD 拆解、研发对齐和验收标准设计。",
            "description_en": "Byte-style PRD breakdown skill. Use it to turn a strategy, roadmap item, or product idea into clear PRD structure, user stories, acceptance criteria, launch scope, and implementation slices. Typical triggers include PRD writing, demand breakdown, build alignment, and acceptance design.",
            "overview_zh": "把方向拆成研发可执行、上线可验证的产品文档。",
            "overview_en": "Translate direction into a product document engineering can build and the business can verify.",
            "inputs_zh": ["目标和用户问题。", "希望达成的业务结果。", "已有假设、限制和依赖。", "需要对齐的研发或设计上下文。"],
            "inputs_en": ["Goal and user problem.", "Expected business outcome.", "Known assumptions, constraints, and dependencies.", "Any engineering or design context to align."],
            "steps_zh": ["定义范围、目标用户和核心场景。", "拆出主要流程、能力点和非目标项。", "为每块能力写用户故事和验收标准。", "给出研发切片和上线边界。", "形成 PRD 草案。"],
            "steps_en": ["Define scope, target user, and core scenarios.", "Break out main flows, capability blocks, and non-goals.", "Write user stories and acceptance bars for each block.", "Suggest engineering slices and launch boundaries.", "Package the result as a PRD draft."],
            "outputs_zh": ["PRD 草案", "用户故事清单", "验收标准清单"],
            "outputs_en": ["PRD draft", "User-story list", "Acceptance-criteria set"],
            "anti_patterns_zh": ["只有功能点，没有用户流程。", "验收标准模糊。", "没有说明本期不做什么。"],
            "anti_patterns_en": ["Feature bullets without user flow.", "Fuzzy acceptance criteria.", "Never stating what is not in this release."],
            "quality_bar_zh": ["先给决策摘要，再展开问题与证据。", "范围、非目标、端到端流程、验收和埋点必须成套出现。", "必须写 rollout / rollback 与开放问题。"],
            "quality_bar_en": ["Lead with the decision summary before the detail.", "Scope, non-goals, end-to-end flows, acceptance, and instrumentation must appear together.", "Include rollout, rollback, and open questions."],
            "template_zh": ["决策摘要", "问题与证据", "目标用户与场景", "范围与非目标", "端到端流程", "需求表", "验收与埋点", "上线回滚与开放问题"],
            "template_en": ["Decision summary", "Problem and evidence", "Target user and scenario", "Scope and non-goals", "End-to-end flows", "Requirement table", "Acceptance and instrumentation", "Rollout, rollback, and open questions"],
            "discussion": False,
        },
        {
            "slug": "byte-experiment-design",
            "title_zh": "字节实验设计",
            "title_en": "Byte Experiment Design",
            "short_zh": "输出实验假设、指标、样本、判定条件与完整复盘结构设计",
            "short_en": "Design experiments with hypotheses, metrics, and decision rules",
            "description_zh": "字节式实验设计 skill。用于把增长、产品、营销或服务问题转成清晰实验，包括假设、实验单元、指标、样本、节奏、判定条件和复盘机制。常见触发包括 A/B 实验、功能试点、内容验证和流程验证。",
            "description_en": "Byte-style experiment design skill. Use it to turn a product, growth, market, or service question into a clear experiment with hypothesis, unit, metrics, sample, timing, decision rules, and review structure. Typical triggers include A/B tests, pilots, content validation, and process experiments.",
            "overview_zh": "实验不是为了跑动作，而是为了用最短路径得到可行动的结论。",
            "overview_en": "An experiment exists to produce actionable learning with the shortest possible loop.",
            "inputs_zh": ["待验证的问题或假设。", "可操作的实验对象或流量单元。", "业务约束、样本限制和时间限制。", "结果要影响的决策。"],
            "inputs_en": ["The question or hypothesis to validate.", "The operable unit, audience, or traffic segment.", "Business, sample, and time constraints.", "The decision this experiment should influence."],
            "steps_zh": ["把问题改写成可证伪假设。", "定义实验对象、对照和主要指标。", "给出样本、周期和停表条件。", "明确结果解释和后续动作。", "形成实验卡或复盘模板。"],
            "steps_en": ["Rewrite the question into a falsifiable hypothesis.", "Define the unit, control, and primary metrics.", "Set sample, timing, and stop rules.", "Specify how results will be interpreted and acted on.", "Package the result as an experiment card or review template."],
            "outputs_zh": ["实验卡", "A/B 方案", "实验复盘模板"],
            "outputs_en": ["Experiment card", "A/B plan", "Experiment review template"],
            "anti_patterns_zh": ["指标太多，不知道看哪个。", "实验结果无法影响真实决策。", "没有停表条件或失败处理。"],
            "anti_patterns_en": ["Too many metrics and no primary one.", "Results that do not affect a real decision.", "No stop rule or failure handling."],
            "quality_bar_zh": ["假设必须可证伪。", "指标必须和决策直接相关。", "结果解释要提前写清。"],
            "quality_bar_en": ["The hypothesis must be falsifiable.", "Metrics must connect directly to a decision.", "Write the interpretation logic up front."],
            "template_zh": ["实验目标与假设", "实验设计", "指标与判定条件", "样本与周期", "复盘与后续动作"],
            "template_en": ["Experiment goal and hypothesis", "Experiment design", "Metrics and decision rules", "Sample and timing", "Review and next actions"],
            "discussion": False,
        },
        {
            "slug": "byte-positioning-message-house",
            "title_zh": "字节定位与信息屋",
            "title_en": "Byte Positioning and Message House",
            "short_zh": "输出定位、价值主张、关键信息架构与差异化表达完整方案",
            "short_en": "Build positioning, value proposition, and a message house",
            "description_zh": "字节式定位与信息屋 skill。用于把产品、业务或方案的价值主张、目标用户、差异化与证明材料组织成清晰的定位和 message house。常见触发包括新产品定位、传播口径对齐、销售话术统一和发布信息设计。",
            "description_en": "Byte-style positioning and message-house skill. Use it to turn a product, business, or initiative into clear positioning, value proposition, differentiation, and supporting proof. Typical triggers include new-product positioning, launch messaging, sales narrative alignment, and communication design.",
            "overview_zh": "先把一句话价值讲准，再展开支撑它的核心信息架构。",
            "overview_en": "Nail the one-line value first, then build the message architecture around it.",
            "inputs_zh": ["目标用户和典型场景。", "核心价值和替代方案。", "差异化能力和证据素材。", "使用场景是品牌、增长还是销售。"],
            "inputs_en": ["Target user and core scenario.", "Core value and the alternative being replaced.", "Differentiating capability and proof points.", "Whether the usage is brand, growth, or sales."],
            "steps_zh": ["定义一句话定位和价值主张。", "拆出 3 到 4 个一级支柱信息。", "补齐证据、案例和反质疑。", "按渠道或对象微调表达。", "输出 message house。"],
            "steps_en": ["Define the one-line positioning and value proposition.", "Break the story into three or four pillar messages.", "Add proof points, cases, and objection handling.", "Adjust the wording by audience or channel.", "Package the result as a message house."],
            "outputs_zh": ["定位稿", "message house", "对外口径草案"],
            "outputs_en": ["Positioning draft", "Message house", "External narrative draft"],
            "anti_patterns_zh": ["定位像功能列表。", "差异化没有证据。", "每个渠道都讲一套不同逻辑。"],
            "anti_patterns_en": ["Positioning that reads like a feature list.", "Differentiation without proof.", "A different logic for every channel."],
            "quality_bar_zh": ["一句话定位要可复述。", "一级信息支柱不能互相重叠。", "每个核心信息都最好有证明材料。"],
            "quality_bar_en": ["The one-line positioning must be repeatable.", "Pillar messages should not overlap.", "Each core message should ideally carry proof."],
            "template_zh": ["一句话定位", "目标用户与场景", "核心信息支柱", "证据与案例", "渠道改写建议"],
            "template_en": ["One-line positioning", "Target user and scenario", "Core message pillars", "Proof and examples", "Channel adaptation notes"],
            "discussion": False,
        },
        {
            "slug": "byte-gtm-plan",
            "title_zh": "字节 GTM 计划",
            "title_en": "Byte GTM Plan",
            "short_zh": "制定市场进入、渠道组合、节奏、指标与 90 天推进计划",
            "short_en": "Build a GTM plan with channels, timing, metrics, and actions",
            "description_zh": "字节式 GTM 计划 skill。用于把定位、增长目标和资源约束转成市场进入与推广计划，包括目标人群、渠道组合、节奏安排、核心内容、关键指标和前 90 天动作。常见触发包括新产品发布、新市场进入和增长计划制定。",
            "description_en": "Byte-style GTM planning skill. Use it to turn positioning, growth goals, and resource constraints into a market-entry and launch plan with audience, channel mix, timing, core content, metrics, and a 90-day action path. Typical triggers include launches, new market entry, and growth planning.",
            "overview_zh": "把定位和增长目标落到渠道、节奏、内容和指标上。",
            "overview_en": "Translate positioning and growth goals into channels, timing, content, and metrics.",
            "inputs_zh": ["产品或方案定位。", "目标用户和市场阶段。", "可用渠道、预算和资源。", "发布窗口和目标指标。"],
            "inputs_en": ["Product or initiative positioning.", "Target audience and market stage.", "Available channels, budget, and resources.", "Launch window and target metrics."],
            "steps_zh": ["明确目标受众和阶段目标。", "选择主渠道、辅助渠道和放弃渠道。", "设计核心内容、节奏和关键节点。", "定义指标、归因和优化节奏。", "形成 90 天 GTM 计划。"],
            "steps_en": ["Set the target audience and stage objective.", "Choose primary, secondary, and dropped channels.", "Design the core content, pacing, and key moments.", "Define metrics, attribution, and optimization rhythm.", "Package the result as a 90-day GTM plan."],
            "outputs_zh": ["GTM 计划", "市场进入方案", "90 天推进表"],
            "outputs_en": ["GTM plan", "Market-entry plan", "90-day execution sheet"],
            "anti_patterns_zh": ["渠道很多，没有主战场。", "发布动作和目标用户脱节。", "指标只看曝光，不看转化。"],
            "anti_patterns_en": ["Too many channels and no main battlefield.", "Launch actions disconnected from the target user.", "Metrics that stop at reach and ignore conversion."],
            "quality_bar_zh": ["必须写清市场假设、ICP 与 buying journey。", "必须明确主战场渠道和放弃渠道。", "必须写 launch calendar、漏斗目标、周节奏、销售使能和风险触发点。"],
            "quality_bar_en": ["State the market thesis, ICP, and buying journey clearly.", "Make the primary battlefield channel and the dropped channels explicit.", "Include the launch calendar, funnel targets, weekly rhythm, sales enablement, and risk triggers."],
            "template_zh": ["市场假设", "ICP 与购买旅程", "offer 与 message", "主战场渠道与放弃渠道", "launch calendar", "漏斗目标", "周运营节奏", "销售使能", "风险与触发点"],
            "template_en": ["Market thesis", "ICP and buying journey", "Offer and message", "Primary battlefield and dropped channels", "Launch calendar", "Funnel targets", "Weekly operating rhythm", "Sales enablement", "Risks and trigger points"],
            "discussion": True,
        },
        {
            "slug": "byte-service-blueprint",
            "title_zh": "字节服务蓝图",
            "title_en": "Byte Service Blueprint",
            "short_zh": "输出服务触点、角色、流程、SLA、升级和反馈闭环蓝图",
            "short_en": "Create a service blueprint with touchpoints, roles, and flows",
            "description_zh": "字节式服务蓝图 skill。用于把服务边界、客户旅程、触点、角色、流程、SLA、升级机制和反馈闭环组织成一份服务蓝图。常见触发包括服务流程设计、客户成功模型、交付重构和体验优化。",
            "description_en": "Byte-style service blueprint skill. Use it to turn service boundaries, customer journey, touchpoints, roles, process, SLA, escalation, and feedback loops into a concrete service blueprint. Typical triggers include service-process design, customer-success setup, delivery redesign, and experience improvement.",
            "overview_zh": "用一张能执行的蓝图，把客户旅程、内部流程和责任机制连起来。",
            "overview_en": "Build one executable blueprint that links customer journey, internal flow, and accountability.",
            "inputs_zh": ["服务对象和典型问题。", "客户旅程或触点。", "现有角色、系统和 SLA 约束。", "主要痛点和升级场景。"],
            "inputs_en": ["Service audience and common issue types.", "Customer journey or touchpoints.", "Current roles, systems, and SLA constraints.", "Main pain points and escalation scenarios."],
            "steps_zh": ["画出客户关键旅程和触点。", "定义前台动作、后台动作和 owner。", "补齐 SLA、升级和异常处理。", "设计反馈到产品和经营的机制。", "输出服务蓝图文档。"],
            "steps_en": ["Map the key customer journey and touchpoints.", "Define frontstage actions, backstage actions, and owners.", "Add SLA, escalation, and exception handling.", "Design the loop back into product and operations.", "Package the result as a service blueprint."],
            "outputs_zh": ["服务蓝图", "服务流程图", "角色与升级说明"],
            "outputs_en": ["Service blueprint", "Service process map", "Role and escalation design"],
            "anti_patterns_zh": ["只有流程，没有责任。", "只有 SLA，没有升级机制。", "没有反馈回产品与经营。"],
            "anti_patterns_en": ["Flow without ownership.", "SLA without escalation logic.", "No loop back into product and operations."],
            "quality_bar_zh": ["先写服务承诺，再写问题分类和严重度。", "必须有前台 / 后台泳道、SLA 矩阵、升级触发和关闭标准。", "必须写 VOC / 产品反馈闭环、例外政策与 dashboard 节奏。"],
            "quality_bar_en": ["Lead with the service promise before issue taxonomy.", "Include frontstage/backstage swimlanes, an SLA matrix, escalation triggers, and closure standards.", "Include the VOC/product loop, exception policies, and dashboard cadence."],
            "template_zh": ["服务承诺", "问题分类与严重度", "前台 / 后台泳道", "SLA 矩阵", "升级触发", "关闭标准", "VOC 与产品闭环", "例外政策", "dashboard 与节奏"],
            "template_en": ["Service promise", "Issue taxonomy and severity", "Frontstage and backstage swimlane", "SLA matrix", "Escalation triggers", "Closure standard", "VOC and product loop", "Exception policies", "Dashboard and cadence"],
            "discussion": False,
        },
        {
            "slug": "byte-voc-to-action",
            "title_zh": "字节 VOC 到行动",
            "title_en": "Byte VOC to Action",
            "short_zh": "把客户声音、投诉与访谈整理成行动项、机制改进与 owner",
            "short_en": "Turn customer feedback into actions, fixes, and clear owners",
            "description_zh": "字节式 VOC 到行动 skill。用于把投诉、工单、访谈、客服记录和满意度反馈转成问题归类、优先级、机制缺口、产品改进和 owner 动作。常见触发包括 VOC 分析、投诉复盘、客户体验改进和问题闭环设计。",
            "description_en": "Byte-style VOC-to-action skill. Use it to turn complaints, tickets, interviews, support logs, and satisfaction feedback into issue themes, priorities, mechanism gaps, product fixes, and named owners. Typical triggers include VOC analysis, complaint review, customer-experience improvement, and feedback-loop design.",
            "overview_zh": "把客户声音从素材，变成行动和机制改善。",
            "overview_en": "Convert customer voice from raw input into action and system change.",
            "inputs_zh": ["客户反馈、访谈、投诉或工单材料。", "问题频次、严重度或影响信息。", "已有责任团队和处理状态。", "希望影响的产品、服务或经营决策。"],
            "inputs_en": ["Customer feedback, interviews, complaints, or ticket data.", "Frequency, severity, or impact signal.", "Current owner teams and status.", "The product, service, or business decision this should influence."],
            "steps_zh": ["先做问题归类和主题聚合。", "判断频次、严重度和业务影响。", "找出机制缺口和责任归属。", "形成行动项、owner 和跟踪节奏。", "输出 VOC 到行动清单。"],
            "steps_en": ["Cluster the issues into themes first.", "Judge frequency, severity, and business impact.", "Identify system gaps and ownership.", "Turn them into actions, owners, and follow-up rhythm.", "Package the result as a VOC action sheet."],
            "outputs_zh": ["VOC 行动清单", "客户体验问题地图", "反馈闭环表"],
            "outputs_en": ["VOC action sheet", "Customer-experience issue map", "Feedback loop tracker"],
            "anti_patterns_zh": ["只统计反馈，不形成动作。", "所有问题都放在一个优先级。", "没有明确 owner 和跟踪节点。"],
            "anti_patterns_en": ["Counting feedback without action.", "Putting every issue in the same priority bucket.", "No named owner or follow-up point."],
            "quality_bar_zh": ["问题分类要能指导动作。", "优先级要结合影响和频次。", "最终结果必须落到 owner 和节奏。"],
            "quality_bar_en": ["Issue categories should guide action.", "Priority should combine impact and frequency.", "The final output must land on owners and cadence."],
            "template_zh": ["问题主题", "影响判断", "根因与机制缺口", "行动项与 owner", "跟踪节奏"],
            "template_en": ["Issue themes", "Impact assessment", "Root cause and mechanism gap", "Actions and owners", "Follow-up cadence"],
            "discussion": False,
        },
        {
            "slug": "byte-quarterly-business-review",
            "title_zh": "字节季度业务复盘",
            "title_en": "Byte Quarterly Business Review",
            "short_zh": "产出季度复盘、问题归因、策略修正和下阶段重点动作方案",
            "short_en": "Create a quarterly business review with correction actions",
            "description_zh": "字节式季度业务复盘 skill。用于把季度经营结果、指标变化、策略执行、问题归因和下阶段修正动作组织成一份高层可读、团队可执行的业务复盘。常见触发包括季度复盘、经营会材料、问题归因和节奏校正。",
            "description_en": "Byte-style quarterly business review skill. Use it to turn quarterly business results, metric shifts, strategy execution, issue diagnosis, and next-stage correction actions into a leadership-readable and team-executable review. Typical triggers include QBR preparation, operating-review materials, issue diagnosis, and execution-course correction.",
            "overview_zh": "复盘不只是讲发生了什么，而是讲为什么、怎么纠偏、下一阶段抓什么。",
            "overview_en": "A real review explains not only what happened, but why, what changes, and what matters next.",
            "inputs_zh": ["季度目标、核心指标和实际结果。", "关键动作、项目进展和市场变化。", "主要问题、风险和已知原因。", "下季度资源和组织约束。"],
            "inputs_en": ["Quarter goals, core metrics, and actual results.", "Key actions, initiative progress, and market changes.", "Main issues, risks, and known causes.", "Next-quarter resource and org constraints."],
            "steps_zh": ["总结目标与结果之间的差异。", "解释核心指标变化和关键原因。", "复盘策略、产品、市场、服务中的主要问题。", "提出纠偏动作、owner 和下一阶段重点。", "形成季度复盘文档。"],
            "steps_en": ["Summarize the gap between goal and result.", "Explain key metric changes and their main causes.", "Review the main issues across strategy, product, market, and service.", "Propose correction actions, owners, and next-quarter focus.", "Package the result as a QBR document."],
            "outputs_zh": ["季度业务复盘", "经营会材料", "纠偏动作清单"],
            "outputs_en": ["Quarterly business review", "Operating-review material", "Correction-action list"],
            "anti_patterns_zh": ["只报结果，不讲归因。", "只有问题，没有纠偏动作。", "复盘很全，但没有下一阶段聚焦。"],
            "anti_patterns_en": ["Reporting results without diagnosis.", "Naming problems without corrective action.", "A full review with no real focus for the next quarter."],
            "quality_bar_zh": ["必须有高管摘要和 scorecard vs target。", "根因要写成叙事，不是指标流水账。", "必须明确 cross-functional blockers、decisions needed、下季度 top bets、owner、节奏和 risk watchlist。"],
            "quality_bar_en": ["Include an executive summary and a scorecard versus target.", "Root cause must read as a narrative, not a metric dump.", "State cross-functional blockers, decisions needed, next-quarter top bets, owners, cadence, and a risk watchlist."],
            "template_zh": ["高管摘要", "目标对比分数卡", "核心归因叙事", "做对了什么 / 失败了什么", "跨团队阻塞", "需要决策", "下季度 top bets", "owner、节奏与风险 watchlist"],
            "template_en": ["Executive summary", "Scorecard versus target", "Root-cause narratives", "What worked and what failed", "Cross-functional blockers", "Decisions needed", "Next-quarter top bets", "Owners, cadence, and risk watchlist"],
            "discussion": True,
        },
        {
            "slug": "byte-exec-brief",
            "title_zh": "字节高管摘要",
            "title_en": "Byte Executive Brief",
            "short_zh": "输出高管摘要、管理层一页纸与关键决策请求完整文稿包",
            "short_en": "Draft an executive brief, one-pager, and decision request",
            "description_zh": "字节式高管摘要 skill。用于把复杂项目、业务问题或战略判断压缩成高管可快速理解和决策的一页纸或短摘要。常见触发包括管理层过会、一页纸汇报、预读材料和重大事项请示。",
            "description_en": "Byte executive brief skill. Use it to compress a complex initiative, business issue, or strategic decision into a leadership-ready one-pager or short brief. Typical triggers include executive reviews, decision memos, pre-reads, and major escalation material.",
            "overview_zh": "把复杂问题压成高层能在几分钟内看懂、判断和拍板的摘要。",
            "overview_en": "Compress a complex problem into something leadership can read, judge, and decide within minutes.",
            "inputs_zh": ["问题背景和当前状态。", "核心结论或建议。", "关键数据、风险和依赖。", "需要高管做的决定。"],
            "inputs_en": ["Background and current state.", "Core recommendation or conclusion.", "Key numbers, risks, and dependencies.", "The decision leadership needs to make."],
            "steps_zh": ["先写一句话结论和决策请求。", "只保留支撑决策的背景与数据。", "说明主要风险、取舍和选项。", "明确推荐动作和 owner。", "形成一页纸或短摘要。"],
            "steps_en": ["Lead with the call and the decision requested.", "Keep only the background and data needed for the decision.", "State the main risks, tradeoffs, and options.", "Make the recommended action and owner explicit.", "Package the result as a one-pager or short brief."],
            "outputs_zh": ["高管摘要", "管理层一页纸", "决策请求文稿"],
            "outputs_en": ["Executive brief", "Leadership one-pager", "Decision request memo"],
            "anti_patterns_zh": ["背景太多，结论太晚。", "没有明确要高管决定什么。", "风险和依赖被藏起来。"],
            "anti_patterns_en": ["Too much background and the call comes too late.", "Never stating what leadership must decide.", "Hiding the main risks and dependencies."],
            "quality_bar_zh": ["前三行必须能说清结论、 why now、要什么决定。", "只保留支撑决策的信息。", "最后要落到 owner 和下一步。"],
            "quality_bar_en": ["The first lines must cover the call, why now, and the decision requested.", "Keep only information that helps the decision.", "End with owners and next steps."],
            "template_zh": ["一句话结论", "为什么现在", "核心事实与数据", "风险与选项", "决策请求与下一步"],
            "template_en": ["One-line call", "Why now", "Core facts and metrics", "Risks and options", "Decision request and next steps"],
            "discussion": True,
        },
        {
            "slug": "byte-board-deck-outline",
            "title_zh": "字节董事会材料大纲",
            "title_en": "Byte Board Deck Outline",
            "short_zh": "产出董事会或经营委材料大纲、逻辑顺序与关键页面设计",
            "short_en": "Outline a board-style deck with logic flow and key slides",
            "description_zh": "字节式董事会材料大纲 skill。用于为董事会、经营委或高层评审设计一套高密度材料大纲，明确叙事顺序、关键页面、证据、风险和决策点。常见触发包括董事会汇报、经营委评审、年度重大议题和融资级叙事准备。",
            "description_en": "Byte board-deck outline skill. Use it to design a dense, leadership-level deck outline for a board, operating committee, or top-level review, including narrative order, key slides, proof, risks, and decision moments. Typical triggers include board reviews, operating committees, annual strategic topics, and financing-style narratives.",
            "overview_zh": "不是做美化 PPT，而是先设计一套能推动决策的大纲和页面逻辑。",
            "overview_en": "This is not slide decoration. It is the logic architecture for a deck that drives decisions.",
            "inputs_zh": ["汇报对象和会议目标。", "核心结论、关键数据和主要争议。", "希望会后达成的决策或动作。", "时间限制和页面预期。"],
            "inputs_en": ["Audience and meeting objective.", "Core conclusion, key numbers, and main tensions.", "The decision or action expected after the meeting.", "Time and page constraints."],
            "steps_zh": ["定义整场汇报的核心主线。", "设计页面顺序、关键图表和论证节奏。", "安排风险、反论点和决策页面。", "标注每页要回答的关键问题。", "形成材料大纲。"],
            "steps_en": ["Define the core storyline of the meeting.", "Design slide order, key evidence, and narrative pacing.", "Place risks, counterpoints, and decision slides deliberately.", "Mark the key question each slide must answer.", "Package the result as a deck outline."],
            "outputs_zh": ["董事会材料大纲", "经营委材料结构", "关键页面说明"],
            "outputs_en": ["Board-deck outline", "Operating-committee deck structure", "Key-slide notes"],
            "anti_patterns_zh": ["页面很多，但主线不清。", "重要风险没有单独页面。", "图表存在，但不服务结论。"],
            "anti_patterns_en": ["Many slides with no clear spine.", "Major risks hidden without a dedicated slide.", "Charts that exist but do not support the call."],
            "quality_bar_zh": ["首页必须明确会议要解决什么。", "页面顺序要服务决策推进。", "必须有关键风险和决策页面。"],
            "quality_bar_en": ["The first slide must say what the meeting is meant to decide.", "Slide order should move the decision forward.", "There must be dedicated risk and decision slides."],
            "template_zh": ["会议目标与结论", "业务现状与窗口", "关键论证页面", "风险与反论点页面", "决策请求页面"],
            "template_en": ["Meeting objective and call", "Business state and window", "Core argument slides", "Risk and counterpoint slides", "Decision-request slide"],
            "discussion": True,
        },
        {
            "slug": "byte-org-alignment-memo",
            "title_zh": "字节组织对齐备忘录",
            "title_en": "Byte Org Alignment Memo",
            "short_zh": "输出跨团队组织对齐文稿、边界说明、owner 与协同节奏",
            "short_en": "Draft an org-alignment memo with roles, boundaries, and rhythm",
            "description_zh": "字节式组织对齐备忘录 skill。用于把跨团队的目标、边界、角色分工、协同节奏、依赖关系和升级机制写成一份组织可执行的对齐文稿。常见触发包括跨部门项目、专项推进、组织调整和机制落地。",
            "description_en": "Byte org-alignment memo skill. Use it to turn a cross-functional objective, scope, role split, cadence, dependencies, and escalation path into an internal memo the organization can actually execute. Typical triggers include cross-team programs, transformation initiatives, org adjustments, and new operating mechanisms.",
            "overview_zh": "把模糊协同写成清晰边界、清晰责任、清晰节奏。",
            "overview_en": "Turn vague coordination into crisp boundaries, responsibilities, and operating rhythm.",
            "inputs_zh": ["跨团队目标和范围。", "涉及团队、角色和依赖。", "现有矛盾、风险和协同痛点。", "需要确定的节奏和升级机制。"],
            "inputs_en": ["Cross-functional goal and scope.", "Teams, roles, and dependencies involved.", "Current conflicts, risks, and coordination pain points.", "Required cadence and escalation design."],
            "steps_zh": ["先写清共同目标和非目标。", "定义角色、边界和关键 handoff。", "明确节奏、例会、升级和例外处理。", "列出关键依赖、风险和 owner。", "形成组织对齐备忘录。"],
            "steps_en": ["State the shared goal and non-goals first.", "Define roles, boundaries, and key handoffs.", "Make cadence, reviews, escalation, and exceptions explicit.", "List dependencies, risks, and owners.", "Package the result as an org-alignment memo."],
            "outputs_zh": ["组织对齐备忘录", "协同边界说明", "升级机制文稿"],
            "outputs_en": ["Org-alignment memo", "Boundary and handoff note", "Escalation mechanism memo"],
            "anti_patterns_zh": ["大家都负责，等于没人负责。", "边界不清，问题只能升级不能解决。", "节奏存在，但没有决策 owner。"],
            "anti_patterns_en": ["Everyone is responsible, which means nobody is.", "Blurred boundaries that force every issue into escalation.", "Cadence exists, but no one owns decisions."],
            "quality_bar_zh": ["共同目标和非目标必须同时存在。", "边界和 handoff 要具体。", "升级机制要写清触发条件和决策 owner。"],
            "quality_bar_en": ["Shared goals and non-goals must both be explicit.", "Boundaries and handoffs must be concrete.", "Escalation rules need triggers and decision owners."],
            "template_zh": ["共同目标与非目标", "角色与边界", "关键协同节点", "升级与例外", "owner 与下一步"],
            "template_en": ["Shared goal and non-goals", "Roles and boundaries", "Key coordination moments", "Escalation and exceptions", "Owners and next steps"],
            "discussion": False,
        },
    ]

    for spec in execution_specs:
        for lang in ("zh", "en"):
            is_zh = lang == "zh"
            skills.append(
                {
                    "name": f"{spec['slug']}-{lang}",
                    "layer": "execution",
                    "title": spec["title_zh"] if is_zh else spec["title_en"],
                    "display_name": spec["title_zh"] if is_zh else spec["title_en"],
                    "short_description": spec["short_zh"] if is_zh else spec["short_en"],
                    "default_prompt": (
                        f"使用 ${spec['slug']}-{lang} 直接为我产出这份文档或方案，并保持字节式判断和结构。"
                        if is_zh
                        else f"Use ${spec['slug']}-{lang} to draft the actual deliverable and keep the Byte-style structure and judgment."
                    ),
                    "description": spec["description_zh"] if is_zh else spec["description_en"],
                    "overview": spec["overview_zh"] if is_zh else spec["overview_en"],
                    "inputs": spec["inputs_zh"] if is_zh else spec["inputs_en"],
                    "steps": spec["steps_zh"] if is_zh else spec["steps_en"],
                    "outputs": spec["outputs_zh"] if is_zh else spec["outputs_en"],
                    "anti_patterns": spec["anti_patterns_zh"] if is_zh else spec["anti_patterns_en"],
                    "quality_bar": spec["quality_bar_zh"] if is_zh else spec["quality_bar_en"],
                    "template_sections": spec["template_zh"] if is_zh else spec["template_en"],
                    "discussion_note": common_discussion_note(lang, spec["discussion"]),
                    "resource_links": [
                        ("references/quality-bar.md", "quality-bar.md"),
                        ("assets/output-template.md", "output-template.md"),
                    ],
                    "resources": ["references", "assets"],
                }
            )

    return skills


def main() -> None:
    if not TARGET_ROOT.exists():
        raise SystemExit(f"Target root does not exist: {TARGET_ROOT}")
    if not INIT_SCRIPT.exists():
        raise SystemExit(f"Missing init script: {INIT_SCRIPT}")

    skills = build_skill_set()
    created = []
    for skill in skills:
        skill_dir = init_skill(skill)
        write(skill_dir / "SKILL.md", render_skill(skill))
        for rel_path, content in build_references(skill).items():
            write(skill_dir / rel_path, content)
        regenerate_openai_yaml(skill, skill_dir)
        validate_skill(skill_dir)
        created.append(skill["name"])

    print(f"Generated {len(created)} skills under {TARGET_ROOT}")
    for name in created:
        print(name)


if __name__ == "__main__":
    main()
