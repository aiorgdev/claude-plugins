# PRD Design Skill

Automatically recognize when users want to design or plan a new feature, and guide them through creating a Product Requirements Document.

## When to Activate

Activate this skill when the user says any of these (Polish & English):

### Start New PRD Triggers
- "let's design X" / "zaprojektujmy X"
- "create PRD for X" / "stwórz PRD dla X"
- "I want to build X" / "chcę zbudować X"
- "help me plan X" / "pomóż mi zaplanować X"
- "design X with me" / "zaprojektuj ze mną X"
- "let's plan X" / "zaplanujmy X"
- "I need a PRD for X" / "potrzebuję PRD dla X"
- "new feature: X" / "nowa funkcjonalność: X"
- "write PRD for X" / "napisz PRD dla X"

### View PRD Triggers
- "show me the X PRD" / "pokaż PRD X"
- "what's the plan for X" / "jaki jest plan na X"
- "view X requirements" / "zobacz wymagania X"

### Continue PRD Triggers
- "continue PRD for X" / "kontynuuj PRD X"
- "back to the X PRD" / "wróć do PRD X"
- "resume X requirements" / "wznów wymagania X"

### List PRDs Triggers
- "what PRDs do we have?" / "jakie mamy PRD?"
- "show all PRDs" / "pokaż wszystkie PRD"
- "list requirements" / "lista wymagań"

## Behavior

### On Start New PRD Trigger

1. **Extract feature name** from the user's message
   - "let's design a bookmarks feature" → "bookmarks"
   - "zaprojektujmy system folderów" → "system-folderow"

2. **Slugify the name**
   - Remove special characters
   - Replace spaces with hyphens
   - Lowercase

3. **Check if `.prd/[slug]/` exists**

4. **If exists:**
   ```
   I found an existing PRD for "[name]".

   [Use AskUserQuestion:]
   - "Continue where we left off"
   - "Start fresh (will archive old PRD)"
   - "Just show me the current PRD"
   ```

5. **If not exists:**
   - Create `.prd/[slug]/` folder
   - Create `metadata.json` with status: "drafting"
   - Start Phase 0 (Codebase Analysis)
   - Then start Phase 1 questions

### On View PRD Trigger

1. Extract feature name from message
2. Find matching folder in `.prd/`
3. Read and display `PRD.md`
4. Show status from `metadata.json`

### On Continue PRD Trigger

1. Extract feature name (or find most recent drafting PRD)
2. Read `metadata.json` for `currentPhase`
3. Resume from that phase

### On List PRDs Trigger

Run `/prd` dashboard mode.

## Feature Name Extraction

Parse the feature name from natural language:

| Input | Extracted |
|-------|-----------|
| "let's design a bookmarks feature" | "bookmarks" |
| "zaprojektujmy system autentykacji" | "system-autentykacji" |
| "I want to build user profiles" | "user-profiles" |
| "create PRD for payment flow" | "payment-flow" |
| "help me plan OAuth integration" | "oauth-integration" |

**Rules:**
- Remove articles: "a", "an", "the"
- Remove filler words: "feature", "system", "funkcjonalność"
- Keep descriptive adjectives: "user profiles" → "user-profiles"
- Polish → slugify with diacritics removed

## Progress Tracking

After each phase, update `metadata.json`:

```json
{
  "name": "feature-slug",
  "displayName": "Feature Name",
  "status": "drafting",
  "currentPhase": "scope",
  "phasesComplete": ["problem"],
  "questionsAnswered": 2,
  "questionsTotal": 7,
  "lastUpdated": "2025-12-19T10:30:00Z"
}
```

## Important

- **ALWAYS create files** when user triggers PRD creation - don't just acknowledge
- **Save progress frequently** - user can stop anytime
- **Resume gracefully** - pick up exactly where left off
- **Support both languages** - Polish and English work identically
- **Explore codebase first** - make suggestions based on existing patterns
- **One question at a time** - never batch questions
