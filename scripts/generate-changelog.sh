#!/bin/bash
set -e

# Last git tag
last_tag=$(git describe --tags --abbrev=0 2>/dev/null || echo "")

if [ -z "$last_tag" ]; then
    range=""
else
    range="$last_tag..HEAD"
fi

# Regex for Conventional Commits
regex='^(feat|fix|docs|style|refactor|test|chore)(\(.+\))?: (.+)'

echo "## Changelog ($(date +%Y-%m-%d))"
echo ""

git log $range --pretty=format:"%s" | while read -r line; do
  if [[ "$line" =~ $regex ]]; then
    type="${BASH_REMATCH[1]}"
    scope="${BASH_REMATCH[2]}"
    description="${BASH_REMATCH[3]}"

    echo "- **$type**${scope}: $description"
  fi
done