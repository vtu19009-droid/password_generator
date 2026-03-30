---
name: "git-workflow"
description: Use this skill when the user asks to commit, push, pull, branch, merge, resolve conflicts, or manage GitHub remotes and authentication.
inclusion: auto
---

# Git Workflow

Git and GitHub operations — commits, remotes, auth, branching, and conflict resolution.

---

## This Repo

| Key | Value |
|-----|-------|
| Local path | `/Users/chaithanyavedagiri/nse-poller-worker` |
| GitHub repo | `https://github.com/vtu19009-droid/password_generator` |
| Remote alias | `password_origin` |
| Branch | `main` |

---

## Daily Workflows

### Stage, commit, push
```bash
git add .
git commit -m "your message"
git push password_origin main
```

### Check what changed
```bash
git status
git diff
git log --oneline -10
```

### Pull latest
```bash
git pull password_origin main
```

---

## Authentication

### Fix 403 / permission denied (easiest)
```bash
gh auth login   # browser-based, handles token automatically
```

### Use a Personal Access Token (PAT)
1. Go to github.com/settings/tokens → Generate new token (classic) → check `repo`
2. Update remote:
```bash
git remote set-url password_origin https://<YOUR_TOKEN>@github.com/vtu19009-droid/password_generator.git
```

### Check current remotes
```bash
git remote -v
```

---

## Branching

```bash
git checkout -b feature/my-feature     # create + switch
git push -u password_origin feature/my-feature
git checkout main                      # back to main
git merge feature/my-feature           # merge in
git branch -d feature/my-feature       # delete local branch
```

---

## Conflict Resolution

```bash
git pull password_origin main          # triggers conflict
# Edit conflicted files — remove <<<< ==== >>>> markers
git add .
git commit -m "resolve merge conflict"
git push password_origin main
```

---

## Undo Operations

| Need | Command |
|------|---------|
| Undo last commit (keep changes) | `git reset --soft HEAD~1` |
| Discard all local changes | `git checkout -- .` |
| Remove untracked files | `git clean -fd` |
| Amend last commit message | `git commit --amend -m "new message"` |

---

## .gitignore for Java

```
*.class
*.jar
*.war
.DS_Store
.env
```

---

## Commit Message Convention

```
feat: add copy to clipboard button
fix: correct strength label color for weak passwords
refactor: extract password logic into PasswordService
docs: update README with JAR packaging steps
chore: add *.class to .gitignore
```
