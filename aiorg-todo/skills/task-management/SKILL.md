# Task Management Skill

Automatically recognize task-related phrases and manage the team task board in `TODO.md`.

## When to Activate

Activate this skill when the user says any of these (Polish & English):

### Add Task Triggers
- "I need to do X" / "muszę zrobić X"
- "task for me: X" / "zadanie dla mnie: X"
- "remind me to X" / "przypomnij mi o X"
- "to do: X" / "do zrobienia: X"
- "on Monday I need to X" / "w poniedziałek muszę X"
- "add task: X"
- "new task: X"

### Show Tasks Triggers
- "what do I have to do?" / "co mam do zrobienia?"
- "my tasks" / "moje taski"
- "show tasks" / "pokaż taski"
- "what's on my list?" / "co mam na liście?"

### Complete Task Triggers
- "done with X" / "zrobione X"
- "finished X" / "skończyłem X"
- "completed X" / "ukończyłem X"
- "mark X as done" / "oznacz X jako zrobione"

### Assign Task Triggers
- "task for @Name: X" / "zadanie dla @Name: X"
- "assign to @Name: X" / "przypisz do @Name: X"
- "@Name should do X" / "@Name powinien zrobić X"

## Behavior

### On Add Task Trigger

1. **Extract task description** from the user's message
2. **Detect due date** from context:
   - "today" / "dziś" / "dzisiaj" → Due: Today
   - "tomorrow" / "jutro" → Due: Tomorrow
   - "this week" / "w tym tygodniu" → Due: This Week
   - "Monday/Tuesday/etc." → Due: specific day
   - "next week" / "w przyszłym tygodniu" → Due: Next Week
   - No date mentioned → no due date
3. **Detect priority** if mentioned:
   - "urgent" / "pilne" / "ASAP" → Priority: High
   - "when you can" / "jak będziesz mógł" → Priority: Low
   - Otherwise → Priority: Medium
4. **Detect category** from context:
   - Code/bug/feature/deploy → [Dev]
   - Tweet/post/content/copy → [Marketing]
   - Plan/roadmap/design → [Product]
   - Review/check/audit → [Review]
   - Otherwise → [Admin]
5. **Check setup**: If `.claude-user` doesn't exist, ask user's name first
6. **Add to TODO.md**: Add task to current user's Active section
7. **Confirm**: Show what was added

### On Show Tasks Trigger

Run `/todo` command behavior - show current user's active tasks.

### On Complete Task Trigger

1. Find the mentioned task in user's Active section
2. If found, move to Done with completion date
3. If ambiguous, show options and ask

### On Assign Task Trigger

1. Parse @Name from message
2. Create/add task to that person's section
3. If person doesn't exist in TODO.md, create their section

## Formatting Rules

### Task Format
```
- [ ] [Category] Description | Priority: Level | Due: Date
```

### Sorting (Apply After Every Edit)

**Active section** - sort by:
1. Due date: Today → Tomorrow → This Week → Next Week → no date
2. Within same due: Priority: High → Medium → Low

**Backlog section** - sort by:
1. Priority: High → Medium → Low

### Categories
- `[Dev]` - Development tasks
- `[Marketing]` - Marketing and content
- `[Product]` - Product and planning
- `[Review]` - Reviews and audits
- `[Admin]` - Administrative tasks

### Priorities
- `High` - Do today/ASAP
- `Medium` - Normal priority
- `Low` - When time permits

### Due Dates
- `Today` - Must do today
- `Tomorrow` - Do tomorrow
- `This Week` - Complete this week
- `Next Week` - Plan for next week
- Specific date (e.g., `2025-12-20`)
- No due date - no deadline

## File Locations

- **User identity**: `.claude-user` (gitignored, contains just the name)
- **Task board**: `TODO.md` (committed, shared with team)

## Important

- **ALWAYS edit TODO.md** when user mentions a task - don't just acknowledge
- **Keep it sorted** - re-sort after every edit
- **Preserve formatting** - don't break existing structure
- **Support both languages** - Polish and English triggers work the same
