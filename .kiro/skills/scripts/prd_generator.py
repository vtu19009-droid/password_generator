#!/usr/bin/env python3
"""Generate PRD template for a feature."""

import argparse
from datetime import datetime

PRD_TEMPLATE = """# {feature_name} PRD

**Author:** {author}  
**Date:** {date}  
**Status:** Draft

---

## 1. Problem Statement

**What problem are we solving?**
[Describe the user problem or pain point]

**For whom?**
[Target user segment]

**Why now?**
[Why is this important to solve now?]

---

## 2. Success Metrics

| Metric | Current | Target | Timeframe |
|--------|---------|--------|-----------|
| [Metric 1] | [Value] | [Goal] | [When] |
| [Metric 2] | [Value] | [Goal] | [When] |

---

## 3. User Stories

- As a [user type], I want [goal] so that [benefit]
- As a [user type], I want [goal] so that [benefit]

---

## 4. Requirements

### Must Have (P0)
- [ ] Requirement 1
- [ ] Requirement 2

### Should Have (P1)
- [ ] Requirement 3
- [ ] Requirement 4

### Nice to Have (P2)
- [ ] Requirement 5

---

## 5. Out of Scope

- [What we're NOT building in this version]
- [Features deferred to future iterations]

---

## 6. Technical Approach

**High-level architecture:**
[Brief technical overview]

**Key decisions:**
- Decision 1: [Rationale]
- Decision 2: [Rationale]

**Dependencies:**
- [External systems, APIs, libraries]

---

## 7. Design

**Wireframes:**
[Link to Figma/mockups]

**User flows:**
[Link to flow diagrams]

**Key interactions:**
- [Interaction 1]
- [Interaction 2]

---

## 8. Dependencies

| Dependency | Owner | Status | Blocker? |
|------------|-------|--------|----------|
| [Dependency 1] | [Team/Person] | [Status] | [Yes/No] |

---

## 9. Risks & Mitigations

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| [Risk 1] | High/Med/Low | High/Med/Low | [How to address] |

---

## 10. Timeline

| Phase | Duration | Owner | Deliverable |
|-------|----------|-------|-------------|
| Design | 1 week | [Name] | Mockups approved |
| Build | 3 weeks | [Name] | Feature complete |
| Test | 1 week | [Name] | QA signed off |
| Launch | 1 week | [Name] | Feature live |

**Total:** [X weeks]

---

## 11. Launch Plan

### Pre-Launch Checklist
- [ ] Feature flag configured
- [ ] Documentation updated
- [ ] Support team trained
- [ ] Announcement drafted
- [ ] Metrics dashboard ready

### Rollout Strategy
- [ ] Internal dogfooding (Week 1)
- [ ] Beta users (Week 2)
- [ ] 10% rollout (Week 3)
- [ ] 50% rollout (Week 4)
- [ ] 100% rollout (Week 5)

### Success Criteria
- [ ] [Metric 1] reaches [target]
- [ ] [Metric 2] reaches [target]
- [ ] No P0 bugs reported

---

## 12. Open Questions

1. [Question 1]
2. [Question 2]

---

## 13. Appendix

### Research
- [Link to user research]
- [Link to competitive analysis]

### References
- [Related PRDs]
- [Technical specs]
"""

def main():
    parser = argparse.ArgumentParser(description="Generate PRD template")
    parser.add_argument("--feature", required=True, help="Feature name")
    parser.add_argument("--author", default="Product Manager", help="Author name")
    args = parser.parse_args()

    prd = PRD_TEMPLATE.format(
        feature_name=args.feature,
        author=args.author,
        date=datetime.now().strftime("%Y-%m-%d")
    )

    filename = f"PRD_{args.feature.replace(' ', '_')}.md"
    with open(filename, 'w') as f:
        f.write(prd)
    
    print(f"✓ Generated {filename}")

if __name__ == "__main__":
    main()
