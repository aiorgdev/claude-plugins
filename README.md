# AI Org Claude Code Plugins

[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Claude Code](https://img.shields.io/badge/built%20for-Claude%20Code-blueviolet)](https://docs.anthropic.com/en/docs/claude-code)

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

### aiorg-bash-guard

Security guard for bash commands. Blocks dangerous commands instantly, auto-approves 100+ safe dev tools, prompts you for the rest. Zero dependencies, instant evaluation.

- Blocks `rm -rf /`, credential access, `| bash`, force push main, `DROP DATABASE`, cloud destruction
- Auto-approves git, npm, docker, curl, aws, gcloud, stripe, and 100+ more
- Catches `python3 -c "os.system('rm -rf /')"` (inline code scanning)
- Sees through `sudo`, `env`, `timeout` wrappers
- 125+ tests included

```bash
/plugin install aiorg-bash-guard@aiorg-plugins
```

[Full documentation](./aiorg-bash-guard/README.md)

---

## More from AI Org

We build Claude Code starter kits for founders. Complete boilerplate + AI that understands your code.

| Kit | Type | What you get |
|-----|------|-------------|
| **[Idea OS](https://aiorg.dev/kits/idea-os)** | Free | AI-powered business idea validation |
| **[Landing Page](https://aiorg.dev/kits/landing-page)** | Free | GEO optimization for Astro projects |
| **[SaaS Dev Team](https://aiorg.dev/kits/saas-starter)** | Paid | Auth, billing, dashboard. Launch your SaaS in days. |
| **[Marketing OS](https://aiorg.dev/kits/marketing-os)** | Paid | Autonomous AI marketing team |
| **[Product OS](https://aiorg.dev/kits/product-os)** | Paid | Product management with AI |

Visit [aiorg.dev](https://aiorg.dev) to see all kits.

## Links

- **Website:** [aiorg.dev](https://aiorg.dev)
- **Documentation:** [aiorg.dev/docs](https://aiorg.dev/docs)
- **All kits:** [aiorg.dev/#kits](https://aiorg.dev/#kits)
- **Issues:** [github.com/aiorgdev/claude-plugins/issues](https://github.com/aiorgdev/claude-plugins/issues)

## Contributing

Found a bug? Have an idea? [Open an issue](https://github.com/aiorgdev/claude-plugins/issues).

## License

MIT
