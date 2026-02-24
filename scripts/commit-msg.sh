#!/bin/bash

commit_msg_file="$1"
commit_msg=$(cat "$commit_msg_file")

regex='^(feat|fix|docs|style|refactor|test|chore)(\(.+\))?: .+'

if [[ ! "$commit_msg" =~ $regex ]]; then
  echo "❌ Invalid commit message."
  echo "Expected format:"
  echo "  type(scope): description"
  echo ""
  echo "Allowed types: feat, fix, docs, style, refactor, test, chore"
  exit 1
fi