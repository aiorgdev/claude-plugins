#!/usr/bin/env python3
"""
Bash command security guard for Claude Code (PreToolUse hook).

Reads tool input from stdin, evaluates the bash command safety,
and outputs a permission decision JSON.

Layer 1: Deny patterns (instant) - always block dangerous commands
Layer 2: Allow patterns (instant) - always allow known dev tools
Layer 3: No decision - Claude Code prompts user (passthrough)

Best practices adopted from:
- Bash Guardian (wrapper unwrapping, pipe security)
- Safety Net (interpreter inline scanning)
- Damage Control (path protection tiers, cloud patterns)
- DCG (data context awareness)

https://github.com/aiorgdev/claude-plugins
"""

import json
import re
import sys

# --- Configuration ---

# Zero-access paths - ANY reference to these is blocked
ZERO_ACCESS_PATHS = [
    r'\.ssh/',
    r'\.aws/',
    r'\.gnupg/',
    r'\.docker/config\.json',
    r'\.kube/config',
    r'\.netrc',
    r'\.npmrc',                              # npm auth tokens
    r'\.pypirc',                             # PyPI auth
    r'\.git-credentials',
    r'serviceAccount.*\.json',               # GCP service accounts
    r'firebase-adminsdk.*\.json',            # Firebase admin SDK
]

# Patterns that are ALWAYS denied
DENY_PATTERNS = [
    # --- Filesystem destruction ---
    r'rm\s+-rf\s+/\s*($|[;&|"\')}\]])',       # rm -rf / (root, including in inline code)
    r'rm\s+-rf\s+/(etc|usr|var|bin|sbin|lib|boot|dev|proc|sys|opt|root|System|Library|Applications)\b',
    r'rm\s+-rf\s+~\s*($|[;&|/])',            # rm -rf ~ or rm -rf ~/
    r'mkfs\.',                               # Format disk
    r'dd\s+if=/dev/(zero|random|urandom)\s+of=/', # Overwrite disk
    r':\(\)\s*\{.*:\|:.*\}',                 # Fork bomb
    r'>\s*/dev/sd[a-z]',                     # Overwrite disk device
    r'chmod\s+-R\s+777\s+/',                 # Chmod 777 root

    # --- Credential access ---
    r'/etc/shadow',                          # System passwords
    r'/etc/passwd',                          # System users
    r'security\s+find.*password',            # macOS Keychain

    # --- Pipe to shell (any source, not just curl) ---
    r'\|\s*(bash|sh|zsh|dash|ksh|fish|eval)\b', # Pipe to any shell/eval

    # --- Git destructive ---
    r'push\s+--force\s+(origin\s+)?(main|master)\b', # Force push main
    r'git\s+push\s+-f\s+(origin\s+)?(main|master)\b', # Short flag force push

    # --- Database destruction ---
    r'DROP\s+(DATABASE|SCHEMA)\b',           # Drop database
    r'TRUNCATE\s+TABLE\b',                   # Truncate table
    r'DELETE\s+FROM\s+\S+\s*;',             # DELETE without WHERE

    # --- Cloud/infra destruction ---
    r'terraform\s+destroy\b',               # Terraform destroy
    r'pulumi\s+destroy\b',                  # Pulumi destroy
    r'aws\s+s3\s+rb\s+.*--force',           # AWS S3 delete bucket force
    r'gcloud\s+projects\s+delete\b',        # GCP delete project
    r'docker\s+system\s+prune\s+-a',        # Docker nuke everything
    r'kubectl\s+delete\s+(namespace|all\s+--all)', # K8s delete namespace/all
    r'gh\s+repo\s+delete\b',               # GitHub delete repo
    r'heroku\s+apps:destroy\b',             # Heroku destroy app
    r'supabase\s+db\s+reset\b',            # Supabase reset database
    r'redis-cli\s+FLUSHALL\b',             # Redis flush everything
]

# Wrapper commands that should be stripped before checking allow patterns
WRAPPER_COMMANDS = {
    'sudo', 'timeout', 'time', 'nice', 'nohup', 'strace', 'ltrace',
    'watch', 'caffeinate', 'unbuffer', 'command',
}

# Interpreter commands with their code flags
INTERPRETER_FLAGS = {
    'python': '-c', 'python3': '-c', 'python2': '-c',
    'bash': '-c', 'sh': '-c', 'zsh': '-c', 'dash': '-c', 'ksh': '-c',
    'node': '-e', 'ruby': '-e', 'perl': '-e', 'lua': '-e',
    'php': '-r',
}

# Patterns that are ALWAYS allowed (fast path)
ALLOW_PATTERNS = [
    r'^(git|npm|pnpm|npx|yarn|bun|node|deno)\b',
    r'^(python3?|pip3?|uv|poetry|conda)\b',
    r'^(docker|docker-compose|podman)\b',
    r'^(stripe|vercel|supabase|fly|railway|heroku|netlify|firebase|wrangler|coolify)\b',
    r'^(aws|gcloud|az|terraform|kubectl|helm)\b',
    r'^(ls|cat|head|tail|find|grep|rg|ag|wc|sort|uniq|diff|comm)\b',
    r'^(echo|printf|test|\[|true|false|pwd|whoami|which|whereis|type|file)\b',
    r'^(mkdir|touch|cp|mv|ln|cd)\b',
    r'^(curl|wget|http)\b',
    r'^(jq|yq|sed|awk|cut|tr|tee|xargs)\b',
    r'^(tar|zip|unzip|gzip|gunzip|bzip2)\b',
    r'^(make|cmake|cargo|go|rustc|gcc|g\+\+|javac|java|mvn|gradle)\b',
    r'^(open|pbcopy|pbpaste|say|sips|sw_vers|uname|hostname|uptime|df|du|free|top|htop)\b',
    r'^(date|cal|time|timeout|sleep|wait)\b',
    r'^(lsof|ps|kill|killall|pgrep|pkill)\b',
    r'^(ssh|scp|rsync)\b',
    r'^(psql|mysql|sqlite3|mongosh|redis-cli)\b',
    r'^(gh|hub|lab)\b',
    r'^(chmod|chown)\b',
    r'^(source|\.)\s',
    r'^(export|unset|set)\b',
    r'^(if|for|while|case|do|done|then|else|fi)\b',
    r'^#',                                   # Comments
    r'^(env|printenv|read)\b',
    r'^(nvm|fnm|volta|asdf|mise|rtx)\b',
    r'^(brew|apt|yum|dnf|pacman|apk)\b',
    r'^(systemctl|launchctl|service)\s+(status|list|show)\b',
    r'^(claude)\b',
    r'^(readlink|realpath|basename|dirname|stat|md5|sha\d+sum|shasum)\b',
    r'rm\s+(-[rfv]+\s+)*(\S+/)*(node_modules|dist|build|lib|\.next|\.cache|\.turbo|coverage|\.parcel-cache|__pycache__|\.pytest_cache|\.mypy_cache|\.venv|venv|out|\.output|\.nuxt|\.svelte-kit|\.angular|target/debug|target/release)\b',
    r'rm\s+(-[fv]+\s+)*[^-\s]',             # rm without -r (single file deletion)
]


# --- Core functions ---

def read_input():
    """Read hook input JSON from stdin."""
    try:
        return json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        return {}


def extract_command(hook_input):
    """Extract the bash command from hook input."""
    tool_input = hook_input.get("tool_input", {})
    if isinstance(tool_input, str):
        try:
            tool_input = json.loads(tool_input)
        except json.JSONDecodeError:
            return tool_input
    return tool_input.get("command", "")


# --- Layer 1: Deny ---

def check_deny_patterns(command):
    """Check if command matches any deny pattern (including zero-access paths)."""
    # Check zero-access paths first
    for pattern in ZERO_ACCESS_PATHS:
        if re.search(pattern, command, re.IGNORECASE):
            return True, f"zero-access path ({pattern})"

    # Check deny patterns
    for pattern in DENY_PATTERNS:
        if re.search(pattern, command, re.IGNORECASE):
            return True, pattern

    # Check inline interpreter code for deny patterns
    inline_code = extract_inline_code(command)
    if inline_code:
        for pattern in DENY_PATTERNS:
            if re.search(pattern, inline_code, re.IGNORECASE):
                return True, f"inline code: {pattern}"

    return False, None


def extract_inline_code(command):
    """Extract code from interpreter -c/-e flags (e.g., python3 -c 'code')."""
    for interp, flag in INTERPRETER_FLAGS.items():
        # Match: interpreter [options] -c "code" or -c 'code'
        pattern = rf'\b{re.escape(interp)}[\d.]*\s+(?:-\S+\s+)*{re.escape(flag)}\s+'
        m = re.search(pattern, command)
        if m:
            rest = command[m.end():]
            # Extract quoted string
            if rest.startswith(("'", '"')):
                quote = rest[0]
                end = find_matching_quote(rest, 1, quote)
                if end > 0:
                    return rest[1:end]
            else:
                # Unquoted - take until next shell operator
                m2 = re.match(r'^(\S+)', rest)
                if m2:
                    return m2.group(1)
    return None


def find_matching_quote(s, start, quote):
    """Find matching closing quote, handling escapes."""
    i = start
    while i < len(s):
        if s[i] == '\\' and quote == '"':
            i += 2
            continue
        if s[i] == quote:
            return i
        i += 1
    return -1


# --- Layer 2: Allow ---

def split_shell_commands(command):
    """Split compound command on &&, ||, ;, |, newline -- respecting quotes."""
    segments = []
    current = []
    i = 0
    in_single = False
    in_double = False
    in_escape = False

    while i < len(command):
        ch = command[i]

        if in_escape:
            current.append(ch)
            in_escape = False
            i += 1
            continue

        if ch == '\\' and not in_single:
            in_escape = True
            current.append(ch)
            i += 1
            continue

        if ch == "'" and not in_double:
            in_single = not in_single
            current.append(ch)
            i += 1
            continue

        if ch == '"' and not in_single:
            in_double = not in_double
            current.append(ch)
            i += 1
            continue

        if not in_single and not in_double:
            if i + 1 < len(command) and command[i:i+2] in ('&&', '||'):
                seg = ''.join(current).strip()
                if seg:
                    segments.append(seg)
                current = []
                i += 2
                continue
            if ch in (';', '|', '\n'):
                seg = ''.join(current).strip()
                if seg:
                    segments.append(seg)
                current = []
                i += 1
                continue

        current.append(ch)
        i += 1

    seg = ''.join(current).strip()
    if seg:
        segments.append(seg)
    return segments


def strip_wrappers(cmd):
    """Strip wrapper commands (sudo, timeout, env, etc.) to find the real command."""
    parts = cmd.split()
    if not parts:
        return cmd

    iterations = 0
    while iterations < 10 and parts:
        word = parts[0]
        # Get basename for path-qualified commands (/usr/bin/sudo -> sudo)
        basename = word.rsplit('/', 1)[-1] if '/' in word else word

        if basename not in WRAPPER_COMMANDS:
            break

        parts = parts[1:]
        iterations += 1

        # Skip flags of wrapper commands
        while parts and parts[0].startswith('-'):
            flag = parts.pop(0)
            # Flags that consume next arg: sudo -u root, timeout 5
            if basename == 'sudo' and flag in ('-u', '-g', '-C'):
                if parts:
                    parts.pop(0)
            elif basename == 'timeout' and not flag.startswith('--'):
                break  # Next arg after timeout flags is the duration, then command
            elif basename == 'env' and flag in ('-u', '-C', '--unset', '--chdir'):
                if parts:
                    parts.pop(0)

        # For env: also skip VAR=value assignments
        if basename == 'env':
            while parts and re.match(r'^[A-Z_][A-Z0-9_]*=', parts[0]):
                parts.pop(0)

    return ' '.join(parts) if parts else cmd


def extract_command_name(cmd):
    """Extract the first command word, skipping env var assignments."""
    cmd = cmd.strip()
    while True:
        m = re.match(r'^[A-Z_][A-Z0-9_]*=(?:\$\([^)]*\)|"[^"]*"|\'[^\']*\'|\S+)\s+', cmd)
        if not m:
            break
        cmd = cmd[m.end():]
    m = re.match(r'^(\S+)', cmd)
    return m.group(1) if m else cmd


def check_single_command(cmd):
    """Check if a single command matches any allow pattern."""
    cmd = cmd.strip()
    if not cmd:
        return True

    # Standalone variable assignment (e.g. TOKEN=$(gcloud auth ...))
    # Safe because deny patterns already caught dangerous content in Layer 1
    if re.match(r'^[A-Z_][A-Z0-9_]*=', cmd) and '&&' not in cmd:
        return True

    # Strip redirections for cleaner matching (2>/dev/null, >/tmp/out, etc.)
    clean = re.sub(r'\d*>\s*(?:/dev/null|/tmp/\S+|&\d+)', '', cmd).strip()

    # Try direct match
    for pattern in ALLOW_PATTERNS:
        if re.search(pattern, clean):
            return True

    # Try after stripping env var prefixes
    name = extract_command_name(clean)
    if name != clean:
        for pattern in ALLOW_PATTERNS:
            if re.search(pattern, name):
                return True

    # Try after stripping wrapper commands (sudo, timeout, env, etc.)
    unwrapped = strip_wrappers(clean)
    if unwrapped != clean:
        for pattern in ALLOW_PATTERNS:
            if re.search(pattern, unwrapped):
                return True

    return False


def check_allow_patterns(command):
    """Check if all commands in a compound command match allow patterns."""
    segments = split_shell_commands(command.strip())
    if not segments:
        return False
    return all(check_single_command(seg) for seg in segments)


# --- Output ---

def output_decision(decision, reason=""):
    """Output the permission decision JSON."""
    result = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": decision,
        }
    }
    if reason:
        result["hookSpecificOutput"]["permissionDecisionReason"] = reason
    print(json.dumps(result))


# --- Main ---

def main():
    hook_input = read_input()
    command = extract_command(hook_input)

    if not command:
        output_decision("allow", "Empty command")
        return

    # Layer 1: Check deny patterns (instant)
    is_denied, pattern = check_deny_patterns(command)
    if is_denied:
        output_decision("deny", f"Blocked: {pattern}")
        return

    # Layer 2: Check allow patterns (instant)
    if check_allow_patterns(command):
        output_decision("allow", "Matched safe pattern")
        return

    # Layer 3: No decision -- Claude Code falls back to its default permission prompt
    pass


if __name__ == "__main__":
    main()
