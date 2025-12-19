# AI Org Claude Code Plugins

Free, open-source plugins for Claude Code. Built by the team behind [aiorg.dev](https://aiorg.dev).

## Quick Start

```bash
# Add this marketplace to Claude Code
/plugin marketplace add aiorgdev/claude-plugins

# Browse and install plugins
/plugin
```

---

## Available Plugins

### aiorg-todo

Team task board that lives in your repo. Track tasks, assign to teammates, and let Claude auto-recognize "I need to do X" phrases.

- Track tasks with priorities and due dates
- Assign tasks to teammates
- Auto-recognize natural language ("I need to do X")
- Git-friendly (TODO.md commits, .claude-user doesn't)
- Works in English and Polish

```bash
/plugin install aiorg-todo --scope project
/todo setup
```

[Full documentation](./aiorg-todo/README.md)

---

### aiorg-prd

Interactive PRD (Product Requirements Document) designer. Design features through guided conversation - Claude acts as your product partner, asking smart questions and generating implementation-ready documentation.

- Interactive questioning (one question at a time)
- Codebase-aware suggestions
- Generates PRD.md, CONTEXT.md, and TASKS.md
- Resume anytime with `/prd continue`
- Works in English and Polish

```bash
/plugin install aiorg-prd --scope project
/prd new "my feature"
```

[Full documentation](./aiorg-prd/README.md)

---

### aiorg-changelog

Auto-generate changelog entries from git commits. Produces two formats - narrative JSON for landing pages (founder voice), and classic Markdown for developers.

- Dual output: JSON + Markdown
- Marketing-friendly narratives
- Works with conventional commits
- Optional automation hooks

```bash
/plugin install aiorg-changelog --scope project
/changelog init
```

[Full documentation](./aiorg-changelog/README.md)

---

## More from AI Org

We build Claude Code starter kits for founders. Complete boilerplate + AI that understands your code.

| Product | What you get |
|---------|--------------|
| **[SaaS Starter Kit](https://aiorg.dev)** | Auth, billing, dashboard. Launch your SaaS in days. |
| **[Landing Page Kit](https://aiorg.dev)** | High-converting pages with AI copy assistance. |

Visit [aiorg.dev](https://aiorg.dev) to learn more.

## Contributing

Found a bug? Have an idea? [Open an issue](https://github.com/aiorgdev/claude-plugins/issues).

## License

MIT
