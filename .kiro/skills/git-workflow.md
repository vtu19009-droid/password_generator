---
name: "git-workflow"
description: "Use when committing, pushing, pulling, branching, merging, resolving conflicts, or managing GitHub remotes and authentication. Triggers: 'git commit', 'push to GitHub', 'create branch', 'merge conflict', 'git authentication', 'revert commit'."
version: "1.0.0"
category: "engineering"
tier: "standard"
inclusion: "auto"
requires: []
---

# Git Workflow

Git and GitHub operations — commits, remotes, auth, branching, conflict resolution, and undo operations.

---

## Table of Contents

- [Quick Start](#quick-start)
- [This Repository](#this-repository)
- [Daily Workflows](#daily-workflows)
- [Authentication](#authentication)
- [Branching Strategy](#branching-strategy)
- [Conflict Resolution](#conflict-resolution)
- [Undo Operations](#undo-operations)
- [Commit Message Convention](#commit-message-convention)
- [Advanced Workflows](#advanced-workflows)
- [Reference Documentation](#reference-documentation)

---

## Quick Start

```bash
# Stage, commit, push
git add .
git commit -m "feat: add password strength indicator"
git push password_origin main

# Check status
git status
git log --oneline -10

# Pull latest
git pull password_origin main
```

---

## This Repository

| Property | Value |
|----------|-------|
| **Local path** | `/Users/chaithanyavedagiri/nse-poller-worker` |
| **GitHub repo** | `https://github.com/vtu19009-droid/password_generator` |
| **Remote alias** | `password_origin` |
| **Default branch** | `main` |
| **Current files** | `PasswordGenerator.java`, `README.md`, `.kiro/skills/` |

---

## Daily Workflows

### Workflow 1: Make Changes and Push

```
Edit → Stage → Commit → Push
```

**Step 1: Edit files**
```bash
# Make your changes in the editor
```

**Step 2: Check what changed**
```bash
git status
git diff
```

**Step 3: Stage changes**
```bash
# Stage all changes
git add .

# Stage specific files
git add PasswordGenerator.java README.md

# Stage interactively
git add -p
```

**Step 4: Commit with message**
```bash
git commit -m "feat: add copy to clipboard button"
```

**Step 5: Push to remote**
```bash
git push password_origin main
```

### Workflow 2: Pull Latest Changes

```
Fetch → Review → Merge
```

**Step 1: Fetch changes**
```bash
git fetch password_origin
```

**Step 2: Review what changed**
```bash
git log HEAD..password_origin/main --oneline
```

**Step 3: Pull and merge**
```bash
git pull password_origin main
```

### Workflow 3: Sync Fork with Upstream

```
Add upstream → Fetch → Merge → Push
```

**Step 1: Add upstream remote (once)**
```bash
git remote add upstream https://github.com/original-owner/repo.git
```

**Step 2: Fetch upstream**
```bash
git fetch upstream
```

**Step 3: Merge upstream changes**
```bash
git checkout main
git merge upstream/main
```

**Step 4: Push to your fork**
```bash
git push password_origin main
```

---

## Authentication

### Method 1: GitHub CLI (Recommended)

```bash
# Install GitHub CLI
brew install gh

# Authenticate
gh auth login
# Choose: GitHub.com → HTTPS → Login with browser

# Verify
gh auth status
```

**Why:** Handles tokens automatically, works with 2FA.

### Method 2: Personal Access Token (PAT)

**Step 1: Generate token**
1. Go to https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Select scopes: `repo`, `workflow`
4. Copy the token (shown once)

**Step 2: Update remote URL**
```bash
git remote set-url password_origin https://<YOUR_TOKEN>@github.com/vtu19009-droid/password_generator.git
```

**Step 3: Test**
```bash
git push password_origin main
```

### Method 3: SSH Keys

**Step 1: Generate SSH key**
```bash
ssh-keygen -t ed25519 -C "your@email.com"
# Press Enter to accept default location
# Enter passphrase (optional)
```

**Step 2: Add to ssh-agent**
```bash
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
```

**Step 3: Add to GitHub**
```bash
# Copy public key
cat ~/.ssh/id_ed25519.pub | pbcopy

# Go to https://github.com/settings/keys
# Click "New SSH key", paste, save
```

**Step 4: Update remote to SSH**
```bash
git remote set-url password_origin git@github.com:vtu19009-droid/password_generator.git
```

### Troubleshooting Auth

| Error | Cause | Fix |
|-------|-------|-----|
| `403 Permission denied` | Wrong credentials | Re-authenticate with `gh auth login` |
| `fatal: could not read Username` | No credentials stored | Use PAT or SSH |
| `Host key verification failed` | SSH key not added | Add key to GitHub settings |

---

## Branching Strategy

### Strategy 1: Feature Branches

```
main → feature/my-feature → PR → main
```

**Step 1: Create feature branch**
```bash
git checkout -b feature/dark-mode
```

**Step 2: Make changes and commit**
```bash
git add .
git commit -m "feat: implement dark mode toggle"
```

**Step 3: Push feature branch**
```bash
git push -u password_origin feature/dark-mode
```

**Step 4: Create pull request**
```bash
gh pr create --title "Add dark mode" --body "Implements user-requested dark mode"
```

**Step 5: Merge and cleanup**
```bash
# After PR is merged on GitHub
git checkout main
git pull password_origin main
git branch -d feature/dark-mode
```

### Strategy 2: Hotfix Branches

```
main → hotfix/critical-bug → main (fast)
```

**Step 1: Create hotfix from main**
```bash
git checkout main
git pull password_origin main
git checkout -b hotfix/password-generation-bug
```

**Step 2: Fix and commit**
```bash
git add .
git commit -m "fix: correct SecureRandom initialization"
```

**Step 3: Push and merge immediately**
```bash
git push -u password_origin hotfix/password-generation-bug
gh pr create --title "HOTFIX: Password generation bug" --body "Critical fix"
# Merge immediately without waiting for review
```

### Branch Naming Convention

| Type | Pattern | Example |
|------|---------|---------|
| Feature | `feature/<description>` | `feature/password-history` |
| Bugfix | `fix/<description>` | `fix/clipboard-error` |
| Hotfix | `hotfix/<description>` | `hotfix/security-vulnerability` |
| Refactor | `refactor/<description>` | `refactor/extract-service` |
| Docs | `docs/<description>` | `docs/update-readme` |

---

## Conflict Resolution

### Workflow: Resolve Merge Conflict

```
Pull → Conflict → Edit → Stage → Commit
```

**Step 1: Pull triggers conflict**
```bash
git pull password_origin main
# Auto-merging PasswordGenerator.java
# CONFLICT (content): Merge conflict in PasswordGenerator.java
```

**Step 2: Identify conflicted files**
```bash
git status
# Unmerged paths:
#   both modified:   PasswordGenerator.java
```

**Step 3: Open and edit conflicted file**
```java
<<<<<<< HEAD
private static final Color ACCENT = new Color(99, 102, 241);
=======
private static final Color ACCENT = new Color(67, 97, 238);
>>>>>>> password_origin/main
```

**Choose one or combine:**
```java
private static final Color ACCENT = new Color(99, 102, 241);
```

**Step 4: Remove conflict markers**
```bash
# Remove all <<<<<<, ======, >>>>>> lines
```

**Step 5: Stage resolved file**
```bash
git add PasswordGenerator.java
```

**Step 6: Complete merge**
```bash
git commit -m "merge: resolve color constant conflict"
```

**Step 7: Push**
```bash
git push password_origin main
```

### Conflict Prevention

- Pull before starting work
- Communicate with team about file ownership
- Keep commits small and focused
- Push frequently

---

## Undo Operations

### Undo Table

| Need | Command | Safety |
|------|---------|--------|
| Undo last commit (keep changes) | `git reset --soft HEAD~1` | ✅ Safe |
| Undo last commit (discard changes) | `git reset --hard HEAD~1` | ⚠️ Destructive |
| Discard all local changes | `git checkout -- .` | ⚠️ Destructive |
| Discard changes in one file | `git checkout -- file.java` | ⚠️ Destructive |
| Remove untracked files | `git clean -fd` | ⚠️ Destructive |
| Amend last commit message | `git commit --amend -m "new message"` | ✅ Safe (if not pushed) |
| Revert a pushed commit | `git revert <commit-hash>` | ✅ Safe |
| Unstage file | `git reset HEAD file.java` | ✅ Safe |

### Workflow: Undo Last Commit (Keep Changes)

```bash
# Undo commit but keep changes staged
git reset --soft HEAD~1

# Edit files
# ...

# Commit again with new message
git commit -m "corrected commit message"
```

### Workflow: Revert a Pushed Commit

```bash
# Find commit hash
git log --oneline

# Revert (creates new commit)
git revert abc1234

# Push
git push password_origin main
```

**Why revert instead of reset:** Preserves history, safe for shared branches.

---

## Commit Message Convention

### Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

| Type | Use When | Example |
|------|----------|---------|
| `feat` | New feature | `feat: add password strength indicator` |
| `fix` | Bug fix | `fix: correct clipboard copy on Windows` |
| `refactor` | Code restructure | `refactor: extract PasswordService class` |
| `docs` | Documentation | `docs: update README with JAR packaging` |
| `style` | Formatting | `style: apply consistent indentation` |
| `test` | Tests | `test: add unit tests for password generation` |
| `chore` | Maintenance | `chore: add *.class to .gitignore` |
| `perf` | Performance | `perf: optimize password generation loop` |

### Examples

```bash
# Simple
git commit -m "feat: add copy to clipboard button"

# With scope
git commit -m "fix(ui): correct button alignment on macOS"

# With body
git commit -m "refactor: extract password logic

- Create PasswordService class
- Move generation logic from UI
- Add unit tests for service"

# Breaking change
git commit -m "feat!: change password generation algorithm

BREAKING CHANGE: Passwords now use SecureRandom instead of Random"
```

---

## Advanced Workflows

### Workflow: Interactive Rebase

```bash
# Rebase last 3 commits
git rebase -i HEAD~3

# Editor opens with:
# pick abc1234 feat: add feature A
# pick def5678 fix: typo
# pick ghi9012 feat: add feature B

# Change to:
# pick abc1234 feat: add feature A
# squash def5678 fix: typo
# pick ghi9012 feat: add feature B

# Save and close — commits are combined
```

### Workflow: Cherry-Pick Commit

```bash
# Copy commit from another branch
git checkout main
git cherry-pick abc1234
git push password_origin main
```

### Workflow: Stash Changes

```bash
# Save work in progress
git stash save "WIP: password history feature"

# Switch branches
git checkout other-branch

# Return and restore
git checkout main
git stash pop
```

---

## Reference Documentation

| File | Contains | Use When |
|------|----------|----------|
| `references/git-commands.md` | Complete command reference | Looking up syntax |
| `references/gitignore-templates.md` | Language-specific .gitignore | Setting up new project |
| `references/git-workflows.md` | Team collaboration patterns | Multi-developer projects |

---

## Common Commands

```bash
# Status and history
git status
git log --oneline -10
git log --graph --all --oneline
git diff
git diff --staged

# Branching
git branch
git branch -a
git checkout -b feature/new-feature
git branch -d feature/old-feature

# Remotes
git remote -v
git remote add <name> <url>
git remote set-url <name> <url>

# Syncing
git fetch password_origin
git pull password_origin main
git push password_origin main
git push -u password_origin feature-branch

# Undo
git reset --soft HEAD~1
git checkout -- file.java
git clean -fd
git revert <commit-hash>

# Stash
git stash
git stash list
git stash pop
git stash drop
```
