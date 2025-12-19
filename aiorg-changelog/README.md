# aiorg-changelog

Auto-generate changelog entries from git commits. Produces two formats:
- **Narrative JSON** - For landing pages, founder voice, marketing-friendly
- **Classic Markdown** - For developers, Keep a Changelog style

## Installation

```bash
# Add AI Org marketplace (one time)
/plugin marketplace add aiorgdev/claude-plugins

# Install to your project
/plugin install aiorg-changelog --scope project
```

## Quick Start

```bash
# Initialize changelog in your project
/changelog init

# Generate entry from recent commits
/changelog

# View recent entries
/changelog view
```

## What You Get

### `changelog.json` (for landing pages)

```json
{
  "entries": [
    {
      "date": "2024-12-19",
      "title": "Dashboard and bug fixes",
      "narrative": "This week we shipped the user dashboard you've been asking for...",
      "changes": [
        { "type": "added", "text": "User dashboard with analytics" },
        { "type": "fixed", "text": "Login redirect issue" }
      ]
    }
  ]
}
```

### `CHANGELOG.md` (for developers)

```markdown
## 2024-12-19 - Dashboard and bug fixes

### Added
- User dashboard with analytics

### Fixed
- Login redirect issue
```

## Commands

| Command | Description |
|---------|-------------|
| `/changelog` | Generate new entry from commits |
| `/changelog init` | First-time setup |
| `/changelog view` | Show recent entries |
| `/changelog edit` | Edit last entry |
| `/changelog sync` | Regenerate MD from JSON |

### Flags

- `--json-only` - Only update JSON, skip Markdown
- `--md-only` - Only update Markdown, skip JSON

## Display on Landing Page

Import `changelog.json` in your frontend:

```tsx
// Next.js example
import changelog from '@/changelog.json'

export default function ChangelogPage() {
  return (
    <div>
      <h1>Changelog</h1>
      {changelog.entries.map(entry => (
        <article key={entry.date}>
          <h2>{entry.title}</h2>
          <time>{entry.date}</time>
          <p>{entry.narrative}</p>
        </article>
      ))}
    </div>
  )
}
```

## Automation (Optional)

Want changelog generated automatically after push? Add this hook to your project:

1. Copy template: `cp ~/.claude/plugins/aiorg-changelog/templates/hook-post-push.sh .claude/hooks/`
2. Make executable: `chmod +x .claude/hooks/hook-post-push.sh`

Or manually run `/changelog` when you want to publish updates.

## Commit Message Tips

The plugin works best with conventional commits:

```bash
git commit -m "feat: add user dashboard"
git commit -m "fix: login redirect issue"
git commit -m "perf: improve page load speed"
```

But it also handles regular commit messages - AI will figure out the type.

## License

MIT
