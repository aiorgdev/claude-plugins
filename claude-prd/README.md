# claude-prd

Interactive PRD (Product Requirements Document) designer for Claude Code. Design features through guided conversation - Claude acts as your product partner, asking smart questions and generating implementation-ready documentation.

## Features

- **Interactive questioning** - Claude asks one question at a time, suggests options, explores your codebase
- **Adaptive depth** - Simple features get 5 questions, complex ones get 7+
- **Codebase-aware** - Analyzes your project to make relevant suggestions
- **Implementation-ready** - Generates PRD.md, CONTEXT.md, and TASKS.md
- **Resume anytime** - Stop mid-PRD, continue later with `/prd continue`
- **Bilingual** - Works in English and Polish

## Installation

```bash
# Add AI Org marketplace (one time)
/plugin marketplace add aiorgdev/claude-plugins

# Install to your project
/plugin install claude-prd --scope project
```

## Usage

### Start a new PRD
```
/prd new
/prd new "bookmarks feature"
```

Or just say it naturally:
```
"Let's design a bookmarks feature"
"Zaprojektujmy system folderów"
"Help me plan the payment flow"
"Create PRD for user authentication"
```

### View PRDs
```
/prd                    # Dashboard - list all PRDs
/prd view bookmarks     # View specific PRD
```

### Continue drafting
```
/prd continue           # Resume last incomplete PRD
```

## How It Works

### 1. Codebase Analysis (Automatic)
Claude explores your project first - reading CLAUDE.md, checking package.json, scanning for patterns. This makes all suggestions relevant to YOUR codebase.

### 2. Interactive Questions (5-7 questions)

**Always asked:**
- Q1: What does [feature] do? (one sentence)
- Q2: What problem does it solve? (the pain point)
- Q3: Scope check (Claude suggests, you confirm)
- Q4: Happy path (step-by-step user flow)
- Q7: Acceptance criteria (how we know it's done)

**For complex features:**
- Q5: Edge cases (what can go wrong)
- Q6: Technical constraints (any requirements)

### 3. Generated Files

```
.prd/
└── bookmarks/
    ├── PRD.md            # Main requirements document
    ├── CONTEXT.md        # Codebase analysis
    ├── TASKS.md          # Implementation checklist
    └── metadata.json     # Status tracking
```

## Example Session

```
You: Let's design a bookmarks feature

Claude:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PRD: bookmarks
Phase 1/6: Problem Definition
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Let me explore your codebase first...

CODEBASE ANALYSIS:
├── Tech: Next.js 15 + Supabase + shadcn/ui
├── Pattern: Server Actions (like notes feature)
└── Similar: src/features/notes/ (CRUD)

Q1 (1/7): In one sentence - what do bookmarks do?

You: Users can save URLs and organize them into folders

Claude: Got it. This looks like a medium-complexity feature.
I'll ask 7 questions to create a solid PRD.

Q2 (2/7): What problem does this solve?
Not "what it does" - what PAIN does it eliminate?

[... continues through all questions ...]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PRD COMPLETE!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Created:
├── .prd/bookmarks/PRD.md
├── .prd/bookmarks/CONTEXT.md
├── .prd/bookmarks/TASKS.md
└── .prd/bookmarks/metadata.json

To implement: "Implement the bookmarks PRD"
```

## Generated File Formats

### PRD.md
Human-readable requirements document with:
- Problem statement
- Scope (in/out)
- User flow
- Edge cases
- Acceptance criteria

### CONTEXT.md
Auto-generated codebase analysis:
- Tech stack detected
- Similar patterns to follow
- Files to create/modify
- Suggested database schema
- TypeScript interfaces

### TASKS.md
Implementation checklist ordered by phase:
1. Database (migrations, RLS)
2. Types & Actions (interfaces, server actions)
3. UI Components (list, card, form)
4. Pages (routes, protection)
5. Integration (sidebar, shortcuts)
6. Testing (acceptance criteria)

## Natural Language Triggers

| Trigger | Action |
|---------|--------|
| "let's design X" / "zaprojektujmy X" | Start new PRD |
| "create PRD for X" / "stwórz PRD dla X" | Start new PRD |
| "show me the X PRD" / "pokaż PRD X" | View PRD |
| "continue PRD" / "kontynuuj PRD" | Resume drafting |
| "what PRDs do we have?" | List all PRDs |

---

Made by [AI Org](https://aiorg.dev) - Claude Code starter kits for founders
