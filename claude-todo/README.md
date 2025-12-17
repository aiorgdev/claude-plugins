# claude-todo

Team task board for Claude Code projects. Track tasks, assign to teammates, and let Claude auto-recognize when you mention something you need to do.

## Features

- **One smart command** - `/todo` does everything (show, add, complete, assign)
- **Team support** - Multiple people, each with their own section
- **Auto-recognition** - Say "I need to do X" and it's added automatically
- **Git-friendly** - `TODO.md` commits with your code, `.claude-user` is gitignored
- **Bilingual** - Works in English and Polish

## Installation

```bash
# Add AI Org marketplace (one time)
/plugin marketplace add aiorgdev/claude-plugins

# Install to your project (team sees it)
/plugin install claude-todo --scope project

# First time setup
/todo setup
```

## Usage

### Show your tasks
```
/todo
```

### Add a task
```
/todo add
/todo add Fix the login bug
```

Or just say it naturally:
```
"I need to fix the login bug today"
"muszę napisać dokumentację w tym tygodniu"
```

### Mark done
```
/todo done
```

### Assign to teammate
```
/todo assign @Alex Review the PR
```

### See all team tasks
```
/todo all
```

## How it works

Tasks live in `TODO.md` at your project root:

```markdown
# Tasks

> Team task board. Managed by Claude - just ask.

---

## Sarah

### Active
- [ ] [Dev] Fix login bug | Priority: High | Due: Today
- [ ] [Marketing] Write launch tweet | Priority: Medium | Due: This Week

### Done
- [x] [Dev] Setup CI/CD | Completed: 2025-12-16

---

## Mike

### Active
- [ ] [Review] Check PR #42 | Priority: High | Due: Today
```

Your identity is stored in `.claude-user` (gitignored):
```
Sarah
```

## Natural language triggers

The plugin recognizes these phrases (English & Polish):

| Trigger | Action |
|---------|--------|
| "I need to do X" / "muszę zrobić X" | Adds task |
| "remind me to X" / "przypomnij mi o X" | Adds task |
| "done with X" / "zrobione X" | Marks complete |
| "task for @Name: X" | Assigns to teammate |
| "my tasks" / "moje taski" | Shows tasks |

---

Made by [AI Org](https://aiorg.dev) - Claude Code starter kits for founders
