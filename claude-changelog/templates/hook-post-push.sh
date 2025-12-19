#!/bin/bash
# Claude Code Hook: Post-Push Changelog Reminder
#
# This hook runs after pushing to your main branch and reminds you
# to update the changelog if there are new commits.
#
# Installation:
# 1. Copy to your project: cp hook-post-push.sh .claude/hooks/
# 2. Make executable: chmod +x .claude/hooks/hook-post-push.sh
#
# Note: This is a reminder hook, not automatic generation.
# Run /changelog manually when you're ready to publish updates.

# Get the current branch
CURRENT_BRANCH=$(git branch --show-current)

# Get main branch from changelog config or default to main
if [ -f "changelog.json" ]; then
  MAIN_BRANCH=$(grep -o '"mainBranch"[[:space:]]*:[[:space:]]*"[^"]*"' changelog.json | cut -d'"' -f4)
fi
MAIN_BRANCH=${MAIN_BRANCH:-main}

# Only run on main branch
if [ "$CURRENT_BRANCH" != "$MAIN_BRANCH" ]; then
  exit 0
fi

# Check if changelog.json exists
if [ ! -f "changelog.json" ]; then
  cat << 'REMINDER'
<additionalContext>
## Changelog Not Initialized

You pushed to main but don't have a changelog yet.
Run `/changelog init` to set up changelog tracking.
</additionalContext>
REMINDER
  exit 0
fi

# Get last changelog entry date
LAST_ENTRY_DATE=$(grep -o '"date"[[:space:]]*:[[:space:]]*"[^"]*"' changelog.json | head -1 | cut -d'"' -f4)

if [ -z "$LAST_ENTRY_DATE" ]; then
  # No entries yet
  COMMITS_SINCE="all commits"
else
  # Count commits since last entry
  COMMIT_COUNT=$(git log --oneline --since="$LAST_ENTRY_DATE" | wc -l | tr -d ' ')
  COMMITS_SINCE="$COMMIT_COUNT commits since $LAST_ENTRY_DATE"
fi

# Only show reminder if there are commits
if [ "$COMMITS_SINCE" != "0 commits since $LAST_ENTRY_DATE" ]; then
  cat << REMINDER
<additionalContext>
## Changelog Reminder

Pushed to $MAIN_BRANCH with $COMMITS_SINCE.

Ready to publish an update? Run:
\`\`\`
/changelog
\`\`\`
</additionalContext>
REMINDER
fi
