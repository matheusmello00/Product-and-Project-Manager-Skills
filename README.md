<div align="center">

**🌐 English** · [Português](README.pt.md) · [Español](README.es.md)

<img src="assets/banner.svg" alt="Product and Project Manager Skills — Matheus Mello" width="100%">

*Skills for product and project managers, ready to use with your AI assistant.*

<a href="https://www.linkedin.com/in/matheusmello00/"><img src="https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn"></a>
<a href="mailto:m.mello00@outlook.com"><img src="https://img.shields.io/badge/Email-Say%20hello-6D1A36?style=for-the-badge&logo=microsoftoutlook&logoColor=white" alt="Email"></a>
<a href="https://wa.me/351920102358"><img src="https://img.shields.io/badge/WhatsApp-Chat-25D366?style=for-the-badge&logo=whatsapp&logoColor=white" alt="WhatsApp"></a>

<img src="https://img.shields.io/github/stars/matheusmello00/Product-and-Project-Manager-Skills?label=Stars&style=flat-square&color=6B7B3A" alt="Stars">

</div>

---

## 🧭 Start with the work in front of you

| Stage | Bring this | Use this skill | Ask for this |
|---|---|---|---|
| Discovery & Research | A pile of raw feedback (CSV, NPS export, pasted comments) | `feedback-analyzer` | Classify this feedback by theme, sentiment and urgency, with verbatim quotes and the top three patterns. |
| Discovery & Research | A research topic or a hypothesis | `user-interview-prep` | Prepare the research brief: hypotheses, a 30-minute interview guide with non-leading questions, and what to watch for. |
| Documentation | A product idea, notes or a workshop transcript | `create-prd` | Write a 1-2 page PRD with real exclusions, measurable metrics and a requirements table with stable IDs. |
| Backlog | The PRD (or any large document, notes, a spreadsheet) | `backlog-creator` | Build the backlog: epics and stories (As a / I want / So that), Given / When / Then criteria and Gherkin test scenarios, all traced to requirements. |
| Backlog | The backlog you just generated | `qa-check` | Validate the acceptance criteria and test scenarios, check that each story description has criteria, flag what is untestable or has no scenario, and propose the missing criteria and scenarios. |
| Development | Commits, tickets or raw notes of a release | `release-notes` | Write user-facing release notes in a B2B, B2C or internal tone. |

The skills hand work over to each other through files, not through your memory:

`feedback-analyzer` + `user-interview-prep` → `create-prd` → `backlog-creator` → `qa-check` → development → `release-notes`

`create-prd` writes `prd-<name>.md` with an `FR-xx / NFR-xx` requirements table. `backlog-creator` imports that table as its inventory and writes `<project>-backlog.md`. `qa-check` reads that backlog and returns a verdict per story, with findings and proposed criteria and scenarios that you apply and re-check.

The assistant reads what you provide, asks at most one batch of questions for what blocks the work, and states its assumptions. It never invents figures, users, criteria or changes that are not in your material, and it records gaps as open questions. Everything it proposes is marked as proposed. The skills only read your sources and produce a single Markdown deliverable. Publishing to a tracker only happens with explicit approval.

## 🧱 How each skill is built (Agent Skills standard)

Every skill follows the open [Agent Skills specification](https://agentskills.io/specification), so it works in any compatible assistant.

```
skill-name/
├── SKILL.md          # Required: frontmatter + instructions (under 500 lines)
├── references/       # Optional: detail loaded only when needed, one level deep
├── scripts/          # Optional: self-contained code with --help and clear errors
├── assets/           # Optional: templates and static resources
└── evals/            # Our addition: discovery queries and quality scenarios
```

| Standard | What it requires | How the skills apply it |
|---|---|---|
| `name` | 1-64 characters, lowercase letters, numbers and hyphens, no leading, trailing or double hyphen, equal to the folder name | Folder and `name` are identical, in `kebab-case` |
| `description` | 1-1024 characters, what the skill does **and when to use it**, with keywords | Capability, triggers and explicit limits ("does not…") toward neighbouring skills |
| `compatibility` | Up to 500 characters, real environment requirements only | Connector and Python needs, all well under the limit |
| `metadata` | String-to-string map for extra properties | `author` and `version` |
| `license`, `allowed-tools` | Optional; `allowed-tools` is experimental | `allowed-tools` limits each skill to the tools it needs |
| Progressive disclosure | Metadata (~100 tokens) at startup; instructions under about 5,000 tokens when activated; resources on demand | Short `SKILL.md`, depth in `references/`, each reference cited with *when* to read it |
| File references | Relative paths, one level deep | `references/<file>.md`, never chains |
| Scripts | Self-contained, helpful errors, edge cases handled | One optional standard-library script (`backlog-creator`), with `--help` and documented exit codes |
| Validation | `skills-ref validate ./skill` | Plus our evals: about 20 discovery queries and at least 3 outcome scenarios per skill |

Beyond the standard, each `SKILL.md` carries `when_to_use`, `argument-hint`, `maturity`, `audience` and `tags`, which help discovery and the catalogue.

## 📦 Install

### Claude Code plugin

Run these commands inside Claude Code:

```text
/plugin marketplace add matheusmello00/Product-and-Project-Manager-Skills
```

Then install the plugin listed by the marketplace and invoke its skills by plugin name.

### Codex or Cursor

Clone the repository, then copy the skills into your personal skills directory:

```bash
git clone https://github.com/matheusmello00/Product-and-Project-Manager-Skills.git
mkdir -p ~/.agents/skills
cp -R Product-and-Project-Manager-Skills/skills/* ~/.agents/skills/
```

Check for existing folders with the same names before copying; copying can overwrite files. For team use, copy into `.agents/skills/` in your project instead.

### Claude Code without the plugin

After cloning, use `~/.claude/skills/` for personal skills or `.claude/skills/` for project skills:

```bash
mkdir -p ~/.claude/skills
cp -R Product-and-Project-Manager-Skills/skills/* ~/.claude/skills/
```

Choose either the plugin or the copy method to avoid duplicate installations.

### Other assistants, including ChatGPT

Open the relevant `SKILL.md` and provide it with your work. Automatic discovery depends on the assistant; cloning this repository does not install the skills into every product.

## 👤 Author

Built by [Matheus Mello](https://github.com/matheusmello00) — Senior Product Manager & Agile Coach.
