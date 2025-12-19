---
description: Interactive PRD (Product Requirements Document) designer - create detailed PRDs through guided conversation
---

# /prd Command

Design Product Requirements Documents through interactive dialogue. Claude acts as a product partner - asking smart questions, exploring the codebase, and generating implementation-ready documentation.

## Modes

### `/prd` (no args) - Dashboard

1. Check if `.prd/` directory exists
2. If not exists, show welcome message and suggest `/prd new`
3. If exists, read all PRD folders and show:

Output format:
```
## Product Requirements

| Name | Status | Last Updated |
|------|--------|--------------|
| oauth-integration | Ready | 2025-12-18 |
| bookmarks | Drafting (3/7) | 2025-12-19 |

---
2 PRDs | 1 ready | 1 in progress

Quick actions:
- `/prd new` - Create new PRD
- `/prd view [name]` - View PRD details
- `/prd continue` - Resume drafting
```

### `/prd new` - Start New PRD (Interactive)

1. Ask for feature name (use AskUserQuestion):
   ```
   What feature are you designing?
   [Text input]
   ```

2. Slugify the name (e.g., "OAuth Integration" → "oauth-integration")

3. Check if `.prd/[slug]/` exists:
   - If exists: Ask "PRD already exists. Continue editing or start fresh?"
   - If not: Create folder structure

4. Run **Phase 0: Codebase Analysis** (automatic, no questions)

5. Start **Interactive Flow** (see below)

### `/prd new "[feature name]"` - Start With Context

Same as `/prd new` but skip step 1, use provided name directly.

### `/prd view [name]` - View PRD

1. Read `.prd/[name]/PRD.md`
2. Read `.prd/[name]/metadata.json` for status
3. Display formatted PRD with status badge
4. Show available actions:
   - "Edit this PRD" → `/prd edit [name]`
   - "View tasks" → show TASKS.md

### `/prd continue` - Resume Drafting

1. Read all `.prd/*/metadata.json`
2. Find PRDs with `status: "drafting"`
3. If multiple, ask which to continue (use AskUserQuestion)
4. Resume from last completed phase

### `/prd edit [name]` - Edit Existing PRD

1. Load existing PRD
2. Show sections with numbers
3. Ask which section to edit
4. Re-ask relevant questions for that section
5. Update files

---

## Interactive Flow (Adaptive)

The questioning depth adapts based on feature complexity. Claude decides complexity after Phase 1.

### Phase 0: Codebase Analysis (Automatic)

Before asking any questions, explore the codebase:

1. **Read project context:**
   - Check for `CLAUDE.md` in project root
   - Read `package.json` for tech stack
   - Scan `src/` or `app/` for existing patterns

2. **Identify similar features:**
   - Look for CRUD patterns
   - Find components to reuse
   - Note database patterns (if Supabase, Prisma, etc.)

3. **Save to CONTEXT.md** (draft, will update later)

**Do not show this to user yet** - use insights to inform questions.

---

### Phase 1: Problem Definition (Always - 2 questions)

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PRD: [Feature Name]
Phase 1/6: Problem Definition
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Q1 (1/7): In one sentence - what does [feature] do?
Example: "Users can save bookmarks and organize them into folders"

[Wait for answer]
```

```
Q2 (2/7): What problem does this solve?
Not "what it does" - what PAIN does it eliminate?

Example: "Users lose track of interesting content and can't find it later"

[Wait for answer]
```

**After Phase 1:** Determine complexity:
- **Simple:** Feature is isolated, CRUD-like, 1-2 components → 5 questions total
- **Medium:** Has integrations, new models, user flows → 7 questions total
- **Complex:** New system, architecture decisions, security → 7+ questions with follow-ups

Show user:
```
Based on your description, this looks like a [simple/medium/complex] feature.
I'll ask [5/7/7+] questions to create a solid PRD.
```

---

### Phase 2: Scope Definition (Always - 1 question)

Based on Q1-Q2 answers AND codebase analysis, suggest scope:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Phase 2/6: Scope
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Q3 (3/7): Based on your description, here's what I think is IN SCOPE:

✓ Create/edit/delete bookmarks
✓ Organize into folders
✓ Quick add from any page
✓ Search bookmarks

And OUT OF SCOPE (for now):
✗ Sharing with other users
✗ Browser extension
✗ Import from other services

Is this right? What should I add or remove?

[Use AskUserQuestion with options:]
- "Looks good"
- "Add something" → ask what
- "Remove something" → ask what
- "Both add and remove" → ask what
```

---

### Phase 3: User Flow (Always - 1 question)

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Phase 3/6: User Flow
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Q4 (4/7): Walk me through the HAPPY PATH.
Step by step, what does a user do?

Example:
1. User clicks "Add Bookmark" button
2. Modal appears with URL and title fields
3. User enters URL, title auto-fills
4. User picks a folder (optional)
5. Clicks Save
6. Bookmark appears in list

Your turn - describe the main flow:

[Wait for free-form answer]
```

---

### Phase 4: Edge Cases (Adaptive - for Medium/Complex)

Based on codebase patterns and user flow, suggest edge cases:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Phase 4/6: Edge Cases
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Q5 (5/7): Here are potential edge cases I identified:

[ ] Invalid URL format → show error
[ ] Duplicate bookmark → warn and offer to update
[ ] Folder doesn't exist → create it
[ ] User not logged in → redirect to login
[ ] Very long title → truncate with ellipsis

Which should we handle? (Select all that apply)

[Use AskUserQuestion with multiSelect: true]
```

---

### Phase 5: Technical Constraints (Adaptive - for Medium/Complex)

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Phase 5/6: Technical
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Q6 (6/7): Based on your codebase, I recommend:

Database: Supabase (you're already using it)
Pattern: Server Actions (like your notes feature)
Components: shadcn/ui Card, Dialog, Input

Any technical constraints I should know about?

[Use AskUserQuestion with options:]
- "Recommendations look good"
- "I have specific requirements" → ask what
- "Not sure, decide for me"
```

---

### Phase 6: Acceptance Criteria (Always - 1 question)

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Phase 6/6: Success Criteria
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Q7 (7/7): How do we know this is DONE?

I suggest these acceptance criteria:
[ ] User can create a bookmark with URL and title
[ ] User can organize bookmarks into folders
[ ] User can search bookmarks by title
[ ] User can delete bookmarks
[ ] Bookmarks persist across sessions

Anything to add or change?

[Use AskUserQuestion with options:]
- "Looks complete"
- "Add more criteria" → ask what
- "Some are not needed" → ask which
```

---

## File Generation

After all questions answered, generate files:

### 1. PRD.md

```markdown
# [Feature Name]

> [One-liner from Q1]

**Status:** Ready
**Complexity:** [Simple/Medium/Complex]
**Created:** [Date]

---

## Problem

[Answer from Q2]

---

## Scope

### In Scope
- [Items from Q3]

### Out of Scope
- [Items from Q3]

---

## User Flow

[Answer from Q4, formatted as numbered list]

---

## Edge Cases

[Items selected in Q5, with handling strategy]

| Case | Handling |
|------|----------|
| Invalid URL | Show error message |
| ... | ... |

---

## Technical Approach

[From Q6 + codebase analysis]

- **Database:** [recommendation]
- **Pattern:** [recommendation]
- **Components:** [recommendation]

---

## Acceptance Criteria

[Items from Q7 as checklist]

- [ ] User can...
- [ ] System shows...
```

### 2. CONTEXT.md (Auto-generated)

```markdown
# Codebase Context for [Feature Name]

> Auto-generated from codebase analysis. Do not edit manually.

---

## Tech Stack

- **Framework:** [from package.json]
- **Database:** [detected]
- **UI Library:** [detected]
- **Auth:** [detected]

---

## Similar Patterns to Follow

| Feature | Path | Pattern |
|---------|------|---------|
| Notes | `src/features/notes/` | CRUD with Server Actions |
| ... | ... | ... |

---

## Files to Create/Modify

### New Files
- `src/features/[name]/actions.ts` - Server actions
- `src/features/[name]/components/` - UI components
- `supabase/migrations/[timestamp]_[name].sql` - Database migration

### Files to Modify
- `src/components/sidebar.tsx` - Add navigation link
- `src/app/layout.tsx` - Add route if needed

---

## Database Schema (Suggested)

```sql
CREATE TABLE [name] (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  -- fields based on feature
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);

-- RLS policies
ALTER TABLE [name] ENABLE ROW LEVEL SECURITY;

CREATE POLICY "[name]_user_access" ON [name]
  FOR ALL USING (auth.uid() = user_id);
```

---

## TypeScript Interfaces (Suggested)

```typescript
interface [Name] {
  id: string
  userId: string
  // fields based on feature
  createdAt: Date
  updatedAt: Date
}

interface Create[Name]Input {
  // required fields
}

interface Update[Name]Input {
  // optional fields
}
```
```

### 3. TASKS.md

```markdown
# Implementation Tasks: [Feature Name]

> Ordered checklist for Claude Code implementation.

---

## Pre-Implementation

- [ ] Read this PRD completely
- [ ] Review similar pattern: `[path from CONTEXT.md]`
- [ ] Confirm understanding with user

---

## Phase 1: Database

- [ ] Create migration file: `supabase/migrations/[timestamp]_[name].sql`
- [ ] Add table with schema from CONTEXT.md
- [ ] Add RLS policies
- [ ] Run migration: `supabase db push`

---

## Phase 2: Types & Actions

- [ ] Create `src/features/[name]/types.ts` with interfaces
- [ ] Create `src/features/[name]/actions.ts` with server actions:
  - [ ] `create[Name](input: Create[Name]Input)`
  - [ ] `get[Name]s()`
  - [ ] `get[Name]ById(id: string)`
  - [ ] `update[Name](id: string, input: Update[Name]Input)`
  - [ ] `delete[Name](id: string)`

---

## Phase 3: UI Components

- [ ] Create `src/features/[name]/components/[name]-list.tsx`
- [ ] Create `src/features/[name]/components/[name]-card.tsx`
- [ ] Create `src/features/[name]/components/[name]-form.tsx`
- [ ] Create `src/features/[name]/components/[name]-dialog.tsx` (if needed)

---

## Phase 4: Pages

- [ ] Create `src/app/(dashboard)/[name]/page.tsx`
- [ ] Add route protection (if needed)
- [ ] Wire up components with actions

---

## Phase 5: Integration

- [ ] Add link to sidebar navigation
- [ ] Add any keyboard shortcuts (if applicable)
- [ ] Update any affected components

---

## Phase 6: Testing

- [ ] Verify all acceptance criteria:
  [Copy from PRD.md]
- [ ] Test edge cases:
  [Copy from PRD.md]

---

**Progress:** 0/[total] tasks
**Last Updated:** [date]
```

### 4. metadata.json

```json
{
  "name": "[feature-name]",
  "displayName": "[Feature Name]",
  "status": "ready",
  "complexity": "simple|medium|complex",
  "created": "2025-12-19",
  "lastUpdated": "2025-12-19",
  "questionsAnswered": 7,
  "questionsTotal": 7,
  "currentPhase": "complete"
}
```

---

## Important Rules

1. **One question at a time** - Never batch questions
2. **Use AskUserQuestion** for all user input - provides structured options
3. **Explore codebase first** - Make suggestions relevant to existing patterns
4. **Adapt complexity** - Don't over-question simple features
5. **Preserve formatting** - Keep consistent Markdown structure
6. **Save progress** - Update metadata.json after each phase
7. **Support resume** - User can stop anytime, `/prd continue` resumes
8. **Bilingual** - Accept Polish and English answers

---

## Complexity Detection Logic

After Q1-Q2, determine complexity:

**Simple (5 questions):**
- Single entity CRUD
- No external integrations
- Follows existing pattern exactly
- Examples: bookmarks, tags, notes

**Medium (7 questions):**
- Multiple related entities
- New database relationships
- Custom UI flows
- Examples: folders with items, comments system

**Complex (7+ questions):**
- New architectural patterns
- Security considerations
- External API integrations
- Multi-step workflows
- Examples: payments, auth system, real-time features
