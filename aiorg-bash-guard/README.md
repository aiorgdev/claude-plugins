# aiorg-bash-guard

Security guard for bash commands in Claude Code. Blocks dangerous commands instantly, auto-approves safe dev tools, and prompts you for everything else.

## Install

```bash
# Add the marketplace (one-time)
/plugin marketplace add aiorgdev/claude-plugins

# Install the plugin
/plugin install aiorg-bash-guard@aiorg-plugins
```

Or manually -- copy `scripts/bash-guard.py` and add to your `.claude/settings.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "python3 /path/to/bash-guard.py"
          }
        ]
      }
    ]
  }
}
```

## How it works

Three layers, evaluated in order:

### Layer 1: Deny (instant block)

Always blocked, no override. Protects against:

- **Filesystem destruction** -- `rm -rf /`, `rm -rf ~`, `mkfs`, `dd of=/dev/`, fork bombs
- **Credential access** -- `.ssh/`, `.aws/`, `.gnupg/`, `.npmrc`, `.git-credentials`, service account keys
- **Pipe to shell** -- `curl ... | bash`, `cat file | sh`, `anything | eval`
- **Git destructive** -- `git push --force origin main/master`
- **Database destruction** -- `DROP DATABASE`, `TRUNCATE TABLE`, `DELETE FROM table;` (no WHERE)
- **Cloud/infra destruction** -- `terraform destroy`, `kubectl delete namespace`, `gh repo delete`, `docker system prune -a`, and more

### Layer 2: Allow (instant approve)

Auto-approved without prompting. Covers 100+ common dev tools:

- **Package managers** -- git, npm, pnpm, yarn, bun, pip, cargo, go, brew
- **Cloud CLIs** -- aws, gcloud, az, terraform, kubectl, stripe, vercel, firebase
- **Unix tools** -- ls, cat, grep, find, curl, jq, sed, awk, tar, ssh
- **Build cleanup** -- `rm -rf node_modules`, `rm -rf dist`, `rm -rf .next`, `rm -rf __pycache__`
- **Single file deletion** -- `rm -f file.txt` (non-recursive rm is safe)
- **Compound commands** -- `git add . && git commit -m "fix" && git push`
- **Wrapper commands** -- `sudo git status`, `timeout 5 curl`, `env VAR=x node`

### Layer 3: Passthrough (prompt user)

Unknown commands fall through to Claude Code's default permission prompt. You decide.

Examples: `nc`, `nmap`, `socat`, custom binaries.

## Features

- **Zero dependencies** -- Python 3 standard library only
- **Instant** -- regex-based, no API calls, no cold start
- **Quote-aware** -- correctly handles `&&`, `||`, `;`, `|` inside quoted strings
- **Inline code scanning** -- catches `python3 -c "os.system('rm -rf /')"` and similar
- **Wrapper unwrapping** -- sees through `sudo`, `env`, `timeout`, `caffeinate`, etc.
- **125+ tests** -- comprehensive test suite included

## Running tests

```bash
python3 tests/test_bash_guard.py
```

## Customizing

The script is a single Python file with clear sections. To customize:

1. **Add deny patterns** -- add regex to `DENY_PATTERNS` list
2. **Add allow patterns** -- add regex to `ALLOW_PATTERNS` list
3. **Add zero-access paths** -- add regex to `ZERO_ACCESS_PATHS` list
4. **Add build artifacts** -- extend the `rm -rf` allow pattern with your directories

## Credits

Best practices adopted from:
- [Bash Guardian](https://github.com/search?q=bash+guardian+claude) -- wrapper unwrapping, pipe security
- [Safety Net](https://github.com/kenryu42/claude-code-safety-net) -- interpreter inline scanning
- [Damage Control](https://github.com/disler/claude-code-damage-control) -- path protection tiers, cloud patterns
- [DCG](https://github.com/Dicklesworthstone/destructive_command_guard) -- data context awareness

## License

MIT
