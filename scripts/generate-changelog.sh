#!/bin/bash
set -e

last_tag=$(git describe --tags --abbrev=0 2>/dev/null || echo "")
if [ -z "$last_tag" ]; then
    range=""
else
    range="$last_tag..HEAD"
fi

regex='^(feat|fix|docs|style|refactor|test|chore)(\(([^)]+)\))?: (.+)'

features=()
fixes=()
docs=()
style=()
refactor=()
test=()
chore=()

while read -r line; do

  # 🔹 Skip automatic changelog update commits and any ci commit
if [[ "$line" =~ \[ci\ skip\] ]]; then
    continue
fi

  if [[ "$line" =~ $regex ]]; then
    type="${BASH_REMATCH[1]}"
    scope="${BASH_REMATCH[3]}"
    description="${BASH_REMATCH[4]}"

    entry="- ${description}"
    [[ -n "$scope" ]] && entry="- **$scope**: ${description}"

    case "$type" in
      feat) features+=("$entry") ;;
      fix) fixes+=("$entry") ;;
      docs) docs+=("$entry") ;;
      style) style+=("$entry") ;;
      refactor) refactor+=("$entry") ;;
      test) test+=("$entry") ;;
      chore) chore+=("$entry") ;;
    esac
  fi

done < <(git log $range --pretty=format:"%s")

echo "## Changelog ($(date +%Y-%m-%d))"
echo ""

[[ ${#features[@]} -gt 0 ]] && { echo "### Features"; printf '%s\n' "${features[@]}"; echo ""; }
[[ ${#fixes[@]} -gt 0 ]] && { echo "### Bug Fixes"; printf '%s\n' "${fixes[@]}"; echo ""; }
[[ ${#docs[@]} -gt 0 ]] && { echo "### Documentation"; printf '%s\n' "${docs[@]}"; echo ""; }
[[ ${#style[@]} -gt 0 ]] && { echo "### Style"; printf '%s\n' "${style[@]}"; echo ""; }
[[ ${#refactor[@]} -gt 0 ]] && { echo "### Refactor"; printf '%s\n' "${refactor[@]}"; echo ""; }
[[ ${#test[@]} -gt 0 ]] && { echo "### Tests"; printf '%s\n' "${test[@]}"; echo ""; }
[[ ${#chore[@]} -gt 0 ]] && { echo "### Chores"; printf '%s\n' "${chore[@]}"; echo ""; }