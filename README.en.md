# Justin Sun Agent · 孙宇晨 Agent

[简体中文](README.md) | **English**

A reusable **Agent Skill with a curated research library** for exploring Justin Sun's public decision-making ideas, comparing statements across periods, and turning relevant insights into practical questions and actions.

This is an independent, research-based simulation. It does not represent Justin Sun or claim his endorsement. The repository contains instructions, a source-linked knowledge base, and a local retrieval script. It is **not a fine-tuned model or a deployed chat backend**.

## What it does

| Mode | What you can ask it to do |
|---|---|
| Decision coaching | Examine a career, business, or product choice using relevant public material, then adapt the analysis to your resources and constraints. |
| Product and growth analysis | Explore user needs, distribution, attention, execution, feedback, and the cost of failure. |
| Statement verification | Locate a statement, identify its date and source, and distinguish a summary from a verified quotation. |
| Cross-period comparison | Compare earlier and later positions while preserving context, qualifications, and unresolved contradictions. |
| Critical review | Challenge a proposal's assumptions and specify what evidence would change the recommendation. |

The intended response style is direct and practical: a conditional judgment, relevant evidence, specific actions, and criteria for reassessment. The skill separates **what the public record says**, **the compiler's interpretation**, and **advice inferred for your situation**.

## Research coverage

The historical library covers accessible public material from **2011 through October 9, 2026, at 18:50 China Standard Time (UTC+08:00)**. It does not claim to include every historical post, deleted statement, paid course, or untranscribed recording.

| Material | Count | Meaning |
|---|---:|---|
| Main records | 94 | Summaries of substantive public statements and interviews, with source information and limitations. |
| Sources | 147 | Deduplicated source entries and links. |
| Thematic analyses | 14 | Interpretations across multiple records. |
| Working principles | 11 | Evidence-linked principles for the simulation, including qualifications and counterexamples. |
| Factual boundary notes | 12 | Guidance on dates, attribution, legal terminology, quotations, and other common misreadings. |
| Supplementary indices | 11 | Leads for material whose reliable full text was not obtained. |
| Course theme guides | 12 | Summaries of third-party course notes, separate from the 94 main records. |

These counts and the cutoff are recorded in [the corpus metadata](references/corpus.json). The knowledge base and skill instructions are primarily **Chinese**. A multilingual host model can answer in English, but that does not turn the underlying library into a separately verified English edition.

### Evidence labels

- **A:** An authored article or complete public statement.
- **B:** A readable published Q&A or edited transcript.
- **C:** Clearly attributable quotation reporting or an institutional release.
- **D/E:** Third-party notes, programme entries, or incomplete source leads.

The labels describe the form of the underlying material. They do not certify that every claim is true. Even an A- or B-grade record in this repository is a **compiler-written summary**, not the original full text. Open the linked source and check its wording and context before presenting an exact quotation or translation as such.

## Quick start: search the library locally

Clone the repository and enter its directory:

```bash
git clone https://github.com/weiyuhuan225-ai/sun-yuchen-agent.git
cd sun-yuchen-agent
```

The retrieval script uses Python 3's standard library. It needs no API key, package installation, or network connection once the repository is available locally.

Search by topic:

```bash
python3 scripts/retrieve.py --query '营销 产品 2019 2025' --limit 6
python3 scripts/retrieve.py --query 'AI 夸张 独立判断' --kind records --limit 4
```

Retrieve known record and source IDs:

```bash
python3 scripts/retrieve.py --ids R003 S115 S116
```

Pass structured input through standard input:

```bash
python3 scripts/retrieve.py --stdin <<'JSON'
{"query":"职业 选择 机会成本","kind":"all","limit":5}
JSON
```

`--kind` accepts `all`, `records`, `themes`, `boundaries`, `indices`, `courses`, or `sources`. Results are JSON containing the matching entries, linked supporting evidence, corpus metadata, and any missing IDs.

Retrieval uses lexical matching and a small set of bilingual topic synonyms. **Chinese topic keywords are the most reliable starting point**; arbitrary English questions are not automatically translated. A retrieval score measures text relevance, not factual reliability. By default, an `all` search focuses on main records and analyses; use an explicit kind when looking for sources, indices, or course notes.

## Use it with an AI assistant

Load [SKILL.md](SKILL.md) and the accompanying directories through a host that supports Agent Skills, following that host's installation procedure. Keep the package's relative paths intact so the assistant can read references and run the script when execution is available.

If the host cannot run Python, it can use the [topic map](references/topic-map.md), [catalogue](references/catalog.md), and linked Markdown records directly. Natural-language dialogue still requires a host language model. Browsing original sources and checking current events also require appropriate host tools; the local retrieval script does neither.

Example requests after loading the skill:

> Use sun-yuchen-agent and answer in English. I have one month to validate a small product idea. Help me choose the first experiment, cite the most relevant records, and explain what result would change your recommendation.

> Compare Justin Sun's earlier statements about marketing with his later statements about product usefulness. Include dates, counterevidence, and links. Do not treat summaries as direct quotations.

> 启用孙宇晨 Agent。帮我检查这个方案最薄弱的假设，并区分史料依据和针对我的推演。

Installing or cloning this repository does not automatically make it available in every ChatGPT conversation or add a Skills management page to the mobile app. Discovery, invocation syntax, and tool access depend on the host and the environment in which the skill is loaded.

## Repository guide

| Path | Contents |
|---|---|
| [SKILL.md](SKILL.md) | Role definition, mode selection, evidence workflow, response style, and boundaries. |
| [scripts/retrieve.py](scripts/retrieve.py) | Offline retrieval over the packaged corpus. |
| [references/principles.md](references/principles.md) | Eleven principles with evidence and limitations. |
| [references/topic-map.md](references/topic-map.md) | Fourteen thematic analyses. |
| [references/fact-boundaries.md](references/fact-boundaries.md) | Twelve factual and interpretation boundaries. |
| [references/catalog.md](references/catalog.md) | Main-record and supplementary-index navigation. |
| [references/records-2011-2020.md](references/records-2011-2020.md) | Early career, entrepreneurship, and early TRON material. |
| [references/records-2021-2024.md](references/records-2021-2024.md) | Material from 2021–2024. |
| [references/records-2025-2026.md](references/records-2025-2026.md) | Material from 2025 through the research cutoff. |
| [references/supplementary.md](references/supplementary.md) | Incomplete source leads and third-party course-note guides. |
| [references/sources.md](references/sources.md) | Source links, dates, and access limitations. |
| [references/corpus.json](references/corpus.json) | Structured data used by the retriever. |
| [agents/openai.yaml](agents/openai.yaml) | Host-facing display and invocation metadata. |

## Keeping answers grounded

For historical questions, preserve dates, attribution, conflicting accounts, and the difference between an allegation, a response, and an adjudicated finding. For current questions, verify fresh sources and identify which conclusions extend beyond the library cutoff.

The simulation should scale recommendations to the user's actual time, budget, skills, and tolerance for loss. It must not invent private intentions, personal relationships, transactions, first-person memories, or guaranteed outcomes. A public figure's past success does not establish that a similar strategy will work for another person.

When contributing a correction, include the affected record or source ID, a source link, the relevant publication or event date, and an explanation of the change. Preserve unresolved uncertainty rather than replacing it with a more confident story. Linked third-party material remains subject to its original rights and usage terms.

## Validation

Run `python3 scripts/validate.py` to check local counts, IDs, source references, relative links, and retrieval behavior. Python 3.9 or later is required for this validation helper. These checks do not re-verify external webpages or guarantee every future model answer.

## Publication and rights

No uniform open-source license has been selected for this version. External articles, interviews, quotations, and brands are not licensed by this repository. See [NOTICE.md](NOTICE.md) for the publication scope and source distinctions.
