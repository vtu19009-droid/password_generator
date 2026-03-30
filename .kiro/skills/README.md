# Kiro Skills for Password Generator Project

Production-grade skills following the claude-skills pattern library.

## Available Skills

| Skill | Inclusion | Category | Description |
|-------|-----------|----------|-------------|
| `java-developer` | auto | engineering | Java development, Swing UI, SecureRandom, OOP patterns |
| `git-workflow` | auto | engineering | Git operations, GitHub auth, branching, conflict resolution |
| `code-reviewer` | manual | engineering | Code quality, security audit, antipatterns, review checklists |
| `senior-architect` | manual | engineering | Architecture decisions, ADRs, tech stack evaluation |
| `ci-cd-pipeline` | manual | engineering | GitHub Actions, build automation, release pipelines |

## Usage

### Auto-Loaded Skills
These load automatically in every session:
- `java-developer` — always available for Java work
- `git-workflow` — always available for Git operations

### Manual Skills
Activate these when needed using `#skill-name` in chat:
- `#code-reviewer` — when reviewing code
- `#senior-architect` — when making architecture decisions
- `#ci-cd-pipeline` — when setting up automation

## Skill Structure

Each skill follows this pattern:

```markdown
---
name: "skill-identifier"
description: "When to use, triggers"
version: "1.0.0"
category: "engineering"
tier: "standard|POWERFUL"
inclusion: "auto|manual"
requires: []
---

# Skill Title

## Quick Start
[Immediate commands]

## Workflows
[Step-by-step processes]

## Decision Tables
[Structured choices]

## Reference Documentation
[Links to templates/guides]
```

## Directory Structure

```
.kiro/skills/
├── README.md (this file)
├── java-developer.md
├── git-workflow.md
├── code-reviewer.md
├── senior-architect.md
├── ci-cd-pipeline.md
├── references/ (detailed guides)
├── scripts/ (automation tools)
└── templates/ (copy-paste starting points)
```

## Patterns Used

Based on comprehensive analysis of claude-skills repository:

1. **Frontmatter metadata** — enables tool discovery
2. **Quick Start sections** — zero-to-running in <30 seconds
3. **Decision tables** — structured choices over prose
4. **Workflow diagrams** — step-by-step processes
5. **Severity levels** — categorized findings
6. **Reference externalization** — heavy docs in references/
7. **Executable scripts** — automation in scripts/
8. **Version tracking** — semantic versioning per skill

## Adding New Skills

1. Create `skill-name.md` in this directory
2. Follow the structure pattern above
3. Add frontmatter with metadata
4. Include Quick Start, Workflows, Decision Tables
5. Set `inclusion: auto` or `manual`
6. Update this README

## Version History

- v1.0.0 (2026-03-31) — Initial skill library created
