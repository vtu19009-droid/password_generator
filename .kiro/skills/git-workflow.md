---
name: "git-workflow"
description: Use this skill when the user asks to commit, push, pull, branch, or manage git repos. Covers GitHub auth, remotes, and common git operations.
inclusion: auto
---

# Git Workflow Skill

Git and GitHub operations for this workspace.

## This Repo

- Local path: `/Users/chaithanyavedagiri/nse-poller-worker`
- GitHub: `https://github.com/vtu19009-droid/password_generator`
- Branch: `main`
- Remote alias for password_generator repo: `password_origin`

---

## Common Commands

### Stage, commit, push
```bash
git add .
git commit -m "your message"
git push password_origin main
```

### Check status
```bash
git status
git log --oneline -5
```

### Add a new remote
```bash
git remote add <name> https://github.com/<user>/<repo>.git
```

### Fix auth (403 errors)
```bash
gh auth login   # easiest — uses browser
# or use a PAT token:
git remote set-url origin https://<token>@github.com/<user>/<repo>.git
```

---

## .gitignore Recommendations for Java

```
*.class
*.jar
*.war
.DS_Store
```

---

## Branching

```bash
git checkout -b feature/my-feature   # new branch
git push -u origin feature/my-feature
git checkout main                    # back to main
git merge feature/my-feature
```
