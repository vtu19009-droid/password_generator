---
name: "product-manager"
version: "1.0.0"
description: "Use when planning features, prioritizing roadmap, conducting user research, writing PRDs, defining success metrics, or making product decisions. Triggers: 'prioritize features', 'write PRD', 'product roadmap', 'user research', 'define metrics', 'product strategy'."
category: "product"
tier: "POWERFUL"
inclusion: "manual"
requires: []
domains: ["product", "strategy", "research"]
---

# Product Manager

Strategic product management — from discovery to delivery, prioritization to metrics.

---

## Table of Contents

- [Quick Start](#quick-start)
- [Core Workflows](#core-workflows)
- [Feature Prioritization](#feature-prioritization)
- [PRD Development](#prd-development)
- [User Research](#user-research)
- [Success Metrics](#success-metrics)
- [Product Strategy](#product-strategy)
- [Python Tools](#python-tools)
- [Reference Documentation](#reference-documentation)

---

## Quick Start

```bash
# Prioritize features using RICE
python .kiro/skills/scripts/rice_prioritizer.py features.csv

# Analyze user interview
python .kiro/skills/scripts/interview_analyzer.py interview.txt

# Generate PRD template
python .kiro/skills/scripts/prd_generator.py --feature "Password History"

# Calculate product metrics
python .kiro/skills/scripts/metrics_calculator.py --users 1000 --active 750
```

---

## Core Workflows

### Workflow 1: Feature Discovery to Delivery

```
Problem → Research → Prioritize → Spec → Build → Measure → Iterate
```

**Phase 1: Problem Discovery**
- Identify user pain points
- Validate problem exists
- Quantify impact

**Phase 2: Research & Validation**
- User interviews (5-8 per segment)
- Competitive analysis
- Technical feasibility check

**Phase 3: Prioritization**
- RICE scoring
- Strategic alignment
- Resource availability

**Phase 4: Specification**
- Write PRD
- Define success metrics
- Create wireframes/mockups

**Phase 5: Build**
- Sprint planning
- Daily standups
- Weekly demos

**Phase 6: Measure**
- Track metrics
- User feedback
- A/B test results

**Phase 7: Iterate**
- Analyze data
- Identify improvements
- Plan next iteration

---

## Feature Prioritization

### RICE Framework

**Formula:** `RICE Score = (Reach × Impact × Confidence) / Effort`

| Component | Definition | Scale |
|-----------|------------|-------|
| **Reach** | Users affected per time period | Number (e.g., 1000 users/month) |
| **Impact** | How much it helps each user | 0.25 (minimal), 0.5 (low), 1 (medium), 2 (high), 3 (massive) |
| **Confidence** | How sure are you? | 50% (low), 80% (medium), 100% (high) |
| **Effort** | Person-months to build | Number (e.g., 2 person-months) |

### Prioritization Decision Table

| RICE Score | Priority | Action |
|------------|----------|--------|
| > 100 | 🔴 Critical | Build immediately |
| 50-100 | 🟡 High | Next quarter |
| 20-50 | 🟢 Medium | Backlog, revisit quarterly |
| < 20 | ⚪ Low | Defer or reject |

### Example: Password Generator Features

```csv
name,reach,impact,confidence,effort,description
Password History,500,high,high,m,Save last 10 generated passwords
Dark Mode Toggle,800,medium,high,s,User-selectable theme
Breach Checking,300,massive,medium,l,Check against HaveIBeenPwned
Export to File,200,low,high,s,Save passwords to CSV
Pronounceable Passwords,400,medium,low,m,Generate memorable passwords
```

**RICE Calculation:**
```python
# Password History
reach = 500
impact = 2  # high
confidence = 1.0  # 100%
effort = 3  # medium (3 person-months)
rice = (500 × 2 × 1.0) / 3 = 333.33  # 🔴 Critical priority
```

### Portfolio Balance

Aim for this distribution:

| Type | % of Capacity | Example |
|------|---------------|---------|
| **Quick Wins** | 30% | Small features, high impact |
| **Big Bets** | 40% | Strategic initiatives |
| **Tech Debt** | 20% | Refactoring, performance |
| **Experiments** | 10% | Risky, high-reward ideas |

---

## PRD Development

### PRD Template Structure

```markdown
# [Feature Name] PRD

## 1. Problem Statement
[What problem are we solving? For whom?]

## 2. Success Metrics
| Metric | Current | Target | Timeframe |
|--------|---------|--------|-----------|
| [Metric 1] | [Value] | [Goal] | [When] |

## 3. User Stories
- As a [user type], I want [goal] so that [benefit]

## 4. Requirements
### Must Have (P0)
- [ ] Requirement 1
### Should Have (P1)
- [ ] Requirement 2
### Nice to Have (P2)
- [ ] Requirement 3

## 5. Out of Scope
- [What we're NOT building]

## 6. Technical Approach
[High-level architecture, key decisions]

## 7. Design
[Wireframes, mockups, user flows]

## 8. Dependencies
- [Other features, teams, or systems]

## 9. Risks & Mitigations
| Risk | Impact | Mitigation |
|------|--------|------------|
| [Risk 1] | [High/Med/Low] | [How to address] |

## 10. Timeline
| Phase | Duration | Owner |
|-------|----------|-------|
| Design | 1 week | [Name] |
| Build | 3 weeks | [Name] |
| Test | 1 week | [Name] |

## 11. Launch Plan
- [ ] Feature flag ready
- [ ] Docs updated
- [ ] Support trained
- [ ] Announcement drafted
```

### PRD Quality Checklist

**Before Sharing:**
- [ ] Problem statement is clear and specific
- [ ] Success metrics are measurable
- [ ] User stories cover all personas
- [ ] Requirements are prioritized (P0/P1/P2)
- [ ] Out-of-scope is explicitly stated
- [ ] Technical feasibility confirmed with engineering
- [ ] Design mockups attached
- [ ] Dependencies identified
- [ ] Risks documented with mitigations
- [ ] Timeline is realistic

---

## User Research

### Interview Process

**Step 1: Recruit Participants**
- 5-8 interviews per user segment
- Mix of power users and churned users
- Offer incentive ($50 gift card, free month, etc.)

**Step 2: Prepare Interview Guide**
```markdown
## Interview Guide Template

### Introduction (5 min)
- Thank you for joining
- Purpose: understand your experience with [product]
- No right/wrong answers
- Recording for notes only

### Background (5 min)
- Tell me about your role
- How do you currently [solve problem]?
- What tools do you use?

### Problem Discovery (15 min)
- Walk me through the last time you [did task]
- What was frustrating about that?
- How often does this happen?
- What have you tried to solve it?

### Solution Validation (10 min)
- [Show mockup/prototype]
- What would you use this for?
- What's missing?
- How much would you pay for this?

### Wrap-up (5 min)
- Anything else we should know?
- Can we follow up in 2 weeks?
```

**Step 3: Conduct Interview**
- Record with permission
- Take minimal notes during
- Focus on listening, not defending

**Step 4: Analyze Insights**
```bash
python .kiro/skills/scripts/interview_analyzer.py transcript.txt
```

**Step 5: Synthesize Findings**
- Group similar pain points
- Identify patterns (3+ mentions = pattern)
- Prioritize by frequency × severity

### Research Synthesis Template

```markdown
## Research Findings: [Topic]

### Participants
- 8 interviews conducted
- Segments: 5 power users, 3 churned users
- Dates: [Date range]

### Key Pain Points
1. **[Pain Point 1]** (mentioned by 7/8)
   - Severity: High
   - Quote: "[User quote]"
   - Impact: [Business impact]

2. **[Pain Point 2]** (mentioned by 5/8)
   - Severity: Medium
   - Quote: "[User quote]"
   - Impact: [Business impact]

### Feature Requests
1. **[Feature 1]** (6/8 requested)
   - Priority: High
   - Willingness to pay: 4/6 said yes

### Opportunities
- [Opportunity 1]: [Description]
- [Opportunity 2]: [Description]

### Recommendations
1. [Action 1] — [Rationale]
2. [Action 2] — [Rationale]
```

---

## Success Metrics

### Metric Framework: AARRR (Pirate Metrics)

| Stage | Metrics | For This Project |
|-------|---------|------------------|
| **Acquisition** | Downloads, installs | GitHub release downloads |
| **Activation** | First use, aha moment | First password generated |
| **Retention** | DAU/MAU, return rate | Weekly active users |
| **Revenue** | MRR, ARPU | N/A (free tool) |
| **Referral** | K-factor, viral coefficient | GitHub stars, forks |

### Metric Definition Template

```markdown
## Metric: [Metric Name]

**Definition:** [Precise definition]

**Calculation:** [Formula]

**Target:** [Goal value]

**Timeframe:** [When to achieve]

**Owner:** [Who tracks this]

**Why it matters:** [Business impact]

**How to measure:** [Tool/method]

**Current value:** [Baseline]

**Tracking frequency:** [Daily/Weekly/Monthly]
```

### Example: Password Generator Metrics

```markdown
## Metric: Weekly Active Users (WAU)

**Definition:** Unique users who generate at least 1 password in a 7-day period

**Calculation:** COUNT(DISTINCT user_id) WHERE generated_password = true AND date >= NOW() - 7 days

**Target:** 100 WAU by end of Q2

**Timeframe:** 3 months

**Owner:** Product Manager

**Why it matters:** Indicates product stickiness and value

**How to measure:** Analytics event tracking (if implemented)

**Current value:** N/A (no analytics yet)

**Tracking frequency:** Weekly
```

### Leading vs Lagging Indicators

| Type | Definition | Example |
|------|------------|---------|
| **Leading** | Predicts future success | Feature usage, engagement |
| **Lagging** | Measures past success | Revenue, retention |

**Focus on leading indicators** — they're actionable.

---

## Product Strategy

### Strategy Framework: Jobs to Be Done (JTBD)

**Format:** When [situation], I want to [motivation], so I can [outcome].

**Example for Password Generator:**
- When **I need a secure password**, I want to **generate one quickly**, so I can **protect my account without thinking**.
- When **I'm creating multiple accounts**, I want to **generate unique passwords**, so I can **avoid reusing weak passwords**.
- When **I forget my password**, I want to **see my history**, so I can **recover access without resetting**.

### Competitive Analysis Template

| Feature | Our Product | Competitor A | Competitor B | Advantage |
|---------|-------------|--------------|--------------|-----------|
| Password generation | ✅ | ✅ | ✅ | - |
| Custom length | ✅ | ✅ | ❌ | Parity |
| Dark theme | ✅ | ❌ | ✅ | Parity |
| Offline use | ✅ | ❌ | ❌ | ✅ Unique |
| Password history | ❌ | ✅ | ✅ | ❌ Gap |
| Breach checking | ❌ | ✅ | ❌ | ❌ Gap |

**Strategic Insights:**
- **Unique advantage:** Offline, no account required
- **Gaps to fill:** Password history, breach checking
- **Differentiation:** Privacy-first, zero data collection

### Product Vision Template

```markdown
## Product Vision: [Product Name]

**For:** [Target user]
**Who:** [User need/problem]
**The:** [Product name]
**Is a:** [Product category]
**That:** [Key benefit]
**Unlike:** [Competitors]
**Our product:** [Key differentiator]

### Example
**For:** Privacy-conscious users
**Who:** Need secure passwords without cloud storage
**The:** Password Generator
**Is a:** Desktop password generation tool
**That:** Creates strong passwords instantly, offline
**Unlike:** LastPass, 1Password (cloud-based)
**Our product:** Works completely offline, zero data collection
```

---

## Python Tools

### `scripts/rice_prioritizer.py`

```python
#!/usr/bin/env python3
"""RICE prioritization calculator."""

import argparse
import csv
import json
import sys
from typing import List, Dict

IMPACT_MAP = {
    "minimal": 0.25,
    "low": 0.5,
    "medium": 1.0,
    "high": 2.0,
    "massive": 3.0
}

EFFORT_MAP = {
    "xs": 0.5,
    "s": 1,
    "m": 3,
    "l": 6,
    "xl": 12
}

CONFIDENCE_MAP = {
    "low": 0.5,
    "medium": 0.8,
    "high": 1.0
}

def calculate_rice(reach: int, impact: str, confidence: str, effort: str) -> float:
    """Calculate RICE score."""
    i = IMPACT_MAP.get(impact.lower(), 1.0)
    c = CONFIDENCE_MAP.get(confidence.lower(), 0.8)
    e = EFFORT_MAP.get(effort.lower(), 3)
    return (reach * i * c) / e

def prioritize_features(csv_file: str) -> List[Dict]:
    """Read CSV and calculate RICE scores."""
    features = []
    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            rice = calculate_rice(
                int(row['reach']),
                row['impact'],
                row['confidence'],
                row['effort']
            )
            features.append({
                'name': row['name'],
                'reach': int(row['reach']),
                'impact': row['impact'],
                'confidence': row['confidence'],
                'effort': row['effort'],
                'rice_score': round(rice, 2),
                'description': row.get('description', '')
            })
    
    return sorted(features, key=lambda x: x['rice_score'], reverse=True)

def main():
    parser = argparse.ArgumentParser(description="RICE prioritization")
    parser.add_argument("csv_file", help="CSV file with features")
    parser.add_argument("--output", choices=["text", "json", "csv"], default="text")
    parser.add_argument("--capacity", type=int, help="Team capacity (person-months)")
    args = parser.parse_args()

    features = prioritize_features(args.csv_file)

    if args.output == "json":
        print(json.dumps(features, indent=2))
    elif args.output == "csv":
        writer = csv.DictWriter(sys.stdout, fieldnames=features[0].keys())
        writer.writeheader()
        writer.writerows(features)
    else:
        print("RICE Prioritization Results")
        print("=" * 80)
        for i, f in enumerate(features, 1):
            priority = "🔴" if f['rice_score'] > 100 else "🟡" if f['rice_score'] > 50 else "🟢"
            print(f"{i}. {priority} {f['name']} (RICE: {f['rice_score']})")
            print(f"   Reach: {f['reach']} | Impact: {f['impact']} | Confidence: {f['confidence']} | Effort: {f['effort']}")
            print(f"   {f['description']}")
            print()

if __name__ == "__main__":
    main()
```

---

### `scripts/interview_analyzer.py`

```python
#!/usr/bin/env python3
"""Analyze user interview transcripts."""

import argparse
import json
import re
from collections import Counter

def extract_pain_points(text: str) -> list:
    """Extract pain points from transcript."""
    pain_keywords = [
        "frustrating", "annoying", "difficult", "hard", "problem",
        "issue", "struggle", "hate", "wish", "can't", "doesn't work"
    ]
    
    sentences = re.split(r'[.!?]', text)
    pain_points = []
    
    for sentence in sentences:
        if any(keyword in sentence.lower() for keyword in pain_keywords):
            pain_points.append(sentence.strip())
    
    return pain_points

def extract_feature_requests(text: str) -> list:
    """Extract feature requests."""
    request_patterns = [
        r"I wish (.*)",
        r"It would be great if (.*)",
        r"I need (.*)",
        r"I want (.*)",
        r"Can you add (.*)"
    ]
    
    requests = []
    for pattern in request_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        requests.extend(matches)
    
    return requests

def analyze_sentiment(text: str) -> str:
    """Simple sentiment analysis."""
    positive_words = ["love", "great", "awesome", "excellent", "perfect", "easy"]
    negative_words = ["hate", "terrible", "awful", "bad", "difficult", "frustrating"]
    
    text_lower = text.lower()
    pos_count = sum(1 for word in positive_words if word in text_lower)
    neg_count = sum(1 for word in negative_words if word in text_lower)
    
    if pos_count > neg_count:
        return "Positive"
    elif neg_count > pos_count:
        return "Negative"
    else:
        return "Neutral"

def main():
    parser = argparse.ArgumentParser(description="Interview analyzer")
    parser.add_argument("transcript", help="Interview transcript file")
    parser.add_argument("--output", choices=["text", "json"], default="text")
    args = parser.parse_args()

    with open(args.transcript, 'r') as f:
        text = f.read()

    pain_points = extract_pain_points(text)
    feature_requests = extract_feature_requests(text)
    sentiment = analyze_sentiment(text)

    result = {
        "pain_points": pain_points[:10],  # Top 10
        "feature_requests": feature_requests[:10],
        "sentiment": sentiment,
        "word_count": len(text.split())
    }

    if args.output == "json":
        print(json.dumps(result, indent=2))
    else:
        print("Interview Analysis")
        print("=" * 80)
        print(f"Sentiment: {sentiment}")
        print(f"Word count: {result['word_count']}")
        print()
        print("Pain Points:")
        for i, pain in enumerate(pain_points[:5], 1):
            print(f"{i}. {pain}")
        print()
        print("Feature Requests:")
        for i, req in enumerate(feature_requests[:5], 1):
            print(f"{i}. {req}")

if __name__ == "__main__":
    main()
```

---

## Common Commands

```bash
# Feature prioritization
python .kiro/skills/scripts/rice_prioritizer.py features.csv
python .kiro/skills/scripts/rice_prioritizer.py features.csv --output json
python .kiro/skills/scripts/rice_prioritizer.py features.csv --capacity 15

# User research
python .kiro/skills/scripts/interview_analyzer.py interview.txt
python .kiro/skills/scripts/interview_analyzer.py interview.txt --output json

# Generate PRD
python .kiro/skills/scripts/prd_generator.py --feature "Password History"
```

---

## Reference Documentation

| File | Contains | Use When |
|------|----------|----------|
| `references/prd-template.md` | Complete PRD template | Writing requirements |
| `references/interview-guide.md` | User interview scripts | Conducting research |
| `references/metrics-guide.md` | Metric definitions | Defining success |
| `references/prioritization-frameworks.md` | RICE, MoSCoW, Kano | Prioritizing features |

---

## Product Manager Mindset

### Key Principles

1. **Fall in love with the problem, not the solution**
2. **Measure everything, but focus on what matters**
3. **Talk to users weekly, not quarterly**
4. **Say no to protect focus**
5. **Ship to learn, not to be perfect**
6. **Data informs, doesn't decide**
7. **Build for 10x, not 10%**

### Common Pitfalls

| Pitfall | Why It's Bad | Fix |
|---------|--------------|-----|
| **Solution-first thinking** | Builds wrong thing | Start with problem statement |
| **Analysis paralysis** | Never ships | Set time-boxes for research |
| **Feature factory** | No impact measurement | Define metrics before building |
| **Ignoring tech debt** | Slows future velocity | Reserve 20% capacity |
| **Stakeholder surprise** | Loss of trust | Weekly updates, monthly demos |
| **Vanity metrics** | False sense of success | Focus on actionable metrics |

---

## Quick Reference

```
Discovery: Problem → Research → Validate
Planning: Prioritize → Spec → Design
Execution: Build → Test → Ship
Measurement: Track → Analyze → Iterate

RICE = (Reach × Impact × Confidence) / Effort
Priority: >100 = Critical, 50-100 = High, 20-50 = Medium, <20 = Low

PRD Sections: Problem, Metrics, Stories, Requirements, Scope, Design, Timeline
Interview: 5-8 per segment, 40 min, record, analyze patterns
Metrics: Define, measure, track, act
```
