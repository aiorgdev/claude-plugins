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

### claude-todo

Team task board that lives in your repo. Track tasks, assign to teammates, and let Claude auto-recognize "I need to do X" phrases.

- Track tasks with priorities and due dates
- Assign tasks to teammates
- Auto-recognize natural language ("I need to do X")
- Git-friendly (TODO.md commits, .claude-user doesn't)
- Works in English and Polish

```bash
/plugin install claude-todo --scope project
/todo setup
```

[Full documentation](./claude-todo/README.md)

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
