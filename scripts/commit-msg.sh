#!/bin/bash

commit_msg_file="$1"
commit_msg=$(cat "$commit_msg_file")

# Allow merge commits
if [[ "$commit_msg" =~ ^Merge\  ]]; then
  exit 0
fi

# Allow revert commits
if [[ "$commit_msg" =~ ^Revert\  ]]; then
  exit 0
fi

# Conventional Commit regex
regex='^(feat|fix|docs|style|refactor|test|chore)(\(.+\))?: .+'

if [[ ! "$commit_msg" =~ $regex ]]; then
  echo "❌ Invalid commit message."
  echo ""
  echo "Expected format:"
  echo "  type(scope): description"
  echo ""
  echo "Allowed types:"
  echo "  feat, fix, docs, style, refactor, test, chore"
  echo ""
  echo "Merge and revert commits are allowed automatically."
  exit 1
fi