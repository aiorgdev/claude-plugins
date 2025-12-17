---
description: Team task board - show, add, complete, and assign tasks
---

# /todo Command

Smart task management command with multiple modes. Detect the mode from arguments or ask if unclear.

## Modes

### `/todo` (no args) - Show My Tasks

1. Read `.claude-user` to get current user name
2. If `.claude-user` doesn't exist, run setup mode first
3. Read `TODO.md` and find user's section
4. Show tasks from **Active** section, sorted by:
   - Due date: Today > Tomorrow > This Week > Next Week > no date
   - Then by Priority: High > Medium > Low
5. Show summary: total tasks, high priority count, due today count

Output format:
```
## Your Tasks (Sarah)

### Due Today (2)
- [High] [Dev] Fix auth bug
- [Medium] [Marketing] Write tweet

### This Week (1)
- [Low] [Product] Review docs

---
3 active tasks | 1 high priority | 2 due today
```

### `/todo setup` - First Time Setup

1. Ask user: "What's your name?" (use AskUserQuestion with common names + Other)
2. Create `.claude-user` with the name
3. Add `.claude-user` to `.gitignore` if not already there
4. Create `TODO.md` with template if doesn't exist:

```markdown
# Tasks

> Team task board. Managed by Claude - just ask to add, update, or complete tasks.

---

## {UserName}

### Active


### Backlog


### Done

```

5. Confirm setup complete

### `/todo add` or `/todo add [description]` - Add Task

1. If description provided, parse it. Otherwise ask:
   - Task description (required)
   - Category: [Dev] | [Marketing] | [Product] | [Review] | [Admin]
   - Priority: High | Medium | Low
   - Due: Today | Tomorrow | This Week | Next Week | (none)

2. Read current user from `.claude-user`
3. Add task to user's **Active** section in `TODO.md`
4. Keep section sorted by due date, then priority
5. Confirm: "Added: [Category] Task description | Priority | Due"

Task format:
```
- [ ] [Category] Description | Priority: Level | Due: Date
```

### `/todo done` - Mark Task Complete

1. Read current user's Active tasks
2. Show numbered list of tasks
3. Ask which to mark done (use AskUserQuestion)
4. Move task to **Done** section with completion date
5. Confirm completion

Done format:
```
- [x] [Category] Description | Completed: 2025-12-17
```

### `/todo assign @Name [task]` - Assign Task to Teammate

1. Parse @Name from arguments
2. If task description provided, create new task for that person
3. If no task, show current user's tasks and ask which to reassign
4. Create user section in TODO.md if doesn't exist
5. Add task to that person's Active section
6. Confirm: "Assigned to @Name: [task]"

### `/todo all` - Show All Team Tasks

1. Read entire TODO.md
2. Show all users' Active tasks grouped by person
3. Show summary: total tasks, tasks per person

## Important Rules

- Always preserve existing formatting in TODO.md
- Never delete tasks without user confirmation
- Keep sections sorted after every edit
- If TODO.md doesn't exist, run setup first
- Support both English and Polish task keywords

## Example Natural Language Triggers

The skill handles these, but the command can also respond to:
- "what do I need to do?" -> show tasks
- "add task: X" -> add mode
- "I'm done with X" -> done mode
- "assign X to @Name" -> assign mode
