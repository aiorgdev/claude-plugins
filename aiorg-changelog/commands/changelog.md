---
description: Generate changelog entries from git commits - narrative JSON for landing pages, classic MD for developers
---

# /changelog Command

Smart changelog generator with multiple modes. Produces two outputs:
- `changelog.json` - Narrative format for landing pages (founder voice)
- `CHANGELOG.md` - Classic developer format (Keep a Changelog style)

Detect the mode from arguments or default to generate.

## Modes

### `/changelog` (no args) - Generate Entry

1. Read `changelog.json` from project root
   - If missing, run init mode first
2. Get last entry's date and commit hash
3. Run `git log --oneline` since last entry commit
4. Filter out noise commits:
   - Skip: "wip", "WIP", "work in progress"
   - Skip: "fix typo", "typo fix", "formatting"
   - Skip: merge commits ("Merge branch", "Merge pull request")
   - Skip: "chore: bump version", version-only commits
5. If no meaningful commits found, tell user "No new changes to log"
6. Group commits by type based on conventional commit prefixes:
   - `feat:` → "added"
   - `fix:` → "fixed"
   - `refactor:`, `perf:` → "changed"
   - `docs:` → "changed" (only if significant)
   - No prefix → infer from message content
7. AI generates:
   - `title` - Catchy, 5-8 words, describes the update theme
   - `narrative` - 2-3 sentences in founder voice, casual but informative
   - `changes` - Array of `{ "type": "added|fixed|changed|removed", "text": "..." }`
8. Show preview and ask for confirmation
9. On confirm:
   - Prepend new entry to `changelog.json` entries array
   - Regenerate `CHANGELOG.md` from all entries
   - Show success message with both file paths

Output preview format:
```
## Preview

**Title:** Dashboard and performance improvements

**Narrative:**
This week we shipped the user dashboard you've been asking for.
Also squeezed out some extra performance - pages load 40% faster now.

**Changes:**
- [added] User dashboard with analytics
- [added] Profile settings page
- [fixed] Login redirect issue
- [changed] Improved page load speed by 40%

---
Add this entry? (yes/no)
```

### `/changelog init` - First Time Setup

1. Check if `changelog.json` already exists
   - If yes, ask: "changelog.json already exists. Reinitialize? This won't delete existing entries."
2. Ask: "What's your main branch?" (use AskUserQuestion)
   - Options: main, master, Other
3. Create `changelog.json`:
```json
{
  "config": {
    "mainBranch": "main",
    "generateMarkdown": true,
    "markdownPath": "CHANGELOG.md"
  },
  "entries": []
}
```
4. Create `CHANGELOG.md`:
```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/).

---
```
5. Add both files to `.gitignore` suggestions if they want to keep changelog private (ask)
6. Confirm: "Changelog initialized! Run `/changelog` to generate your first entry."

### `/changelog view` - Show Recent Entries

1. Read `changelog.json`
2. If empty, suggest running `/changelog` first
3. Show last 5 entries in readable format:

```
## Recent Changelog Entries

### 2024-12-19 - Dashboard and bug fixes
This week we shipped the user dashboard...
- [added] User dashboard with analytics
- [fixed] Login redirect issue

### 2024-12-15 - Initial release
Launched the first version...
- [added] Landing page
- [added] User authentication

---
Showing 2 of 2 entries. View all in changelog.json
```

### `/changelog edit` - Edit Last Entry

1. Read `changelog.json` and get last entry
2. If no entries, tell user to generate one first
3. Show current entry and ask what to change (use AskUserQuestion):
   - Edit title
   - Edit narrative
   - Edit changes (add/remove/modify)
   - Cancel
4. Make requested changes
5. Update `changelog.json`
6. Regenerate `CHANGELOG.md`
7. Show updated entry

### `/changelog sync` - Regenerate Markdown

1. Read `changelog.json`
2. Regenerate `CHANGELOG.md` from all entries:

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/).

---

## 2024-12-19 - Dashboard and bug fixes

### Added
- User dashboard with analytics
- Profile settings page

### Fixed
- Login redirect issue

---

## 2024-12-15 - Initial release

### Added
- Landing page
- User authentication

---
```

3. Confirm: "CHANGELOG.md regenerated with X entries"

### `/changelog --json-only` - JSON Only Mode

Same as default `/changelog` but:
- Only updates `changelog.json`
- Does NOT touch `CHANGELOG.md`
- Useful for projects that only need marketing changelog

### `/changelog --md-only` - Markdown Only Mode

Same as default `/changelog` but:
- Only updates `CHANGELOG.md`
- Does NOT create/update `changelog.json`
- Useful for traditional open source projects

## Important Rules

- Always preserve existing entries - never delete without explicit user confirmation
- Keep entries sorted by date (newest first)
- Use ISO date format: YYYY-MM-DD
- Narrative should be casual, founder voice - not corporate
- Changes should be actionable, user-facing when possible
- Skip internal/technical changes unless significant
- If `changelog.json` doesn't exist, always run init first
- Commit hashes are stored for reference but not shown to users

## Example Narrative Styles

Good (founder voice):
- "This week we shipped dark mode - something you've been asking for since day one."
- "Squashed a nasty bug that was causing login issues for some users. Sorry about that!"
- "Big performance update - everything should feel snappier now."

Bad (corporate):
- "We are pleased to announce the release of dark mode functionality."
- "A bug affecting user authentication has been resolved."
- "Performance optimizations have been implemented."

## Change Type Guidelines

| Type | Use for |
|------|---------|
| added | New features, new pages, new capabilities |
| fixed | Bug fixes, error corrections |
| changed | Improvements, refactors, performance, UX tweaks |
| removed | Deprecated features, removed functionality |

## File Locations

- `changelog.json` - Project root (source of truth)
- `CHANGELOG.md` - Project root (generated from JSON)
- Config stored in `changelog.json` under `config` key
