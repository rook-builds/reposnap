---
name: reposnap
description: >-
  Turn any GitHub repo into a clean markdown or JSON digest of recent activity
  (commits, releases, issues). Use when an agent needs a structured summary of
  a GitHub repository -- recent changes, release history, or open issues --
  without reading raw API responses. Accepts owner/repo or full GitHub URL.
license: MIT
metadata:
  author: rook-builds
  version: "0.2.0"
---

## Core usage

```
reposnap simonw/llm
reposnap --limit 5 simonw/llm
reposnap --format json simonw/llm
reposnap --token $GITHUB_TOKEN simonw/llm
reposnap https://github.com/simonw/llm
```

## Output modes

- **markdown** (default): three sections -- Recent Commits, Releases, Issues;
  each item is a markdown list entry with date and URL
- **json**: structured dict with keys `repo`, `stars`, `forks`, `language`,
  `commits`, `releases`, `issues`

## Exit codes

- `0` -- success
- `1` -- error (invalid repo name, network failure, GitHub API error)

## Agent discovery

```
reposnap introspect   # ACLI JSON: full command tree, options, types
reposnap skill        # this file
```
