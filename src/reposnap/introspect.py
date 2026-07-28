"""ACLI introspection and agentskills.io skill description for reposnap."""
from __future__ import annotations

import json

# Hardcoded to avoid circular import (__init__ imports from here; this must
# not import back from __init__). Keep in sync with pyproject.toml.
_TOOL_VERSION = "0.2.0"

_ACLI_SPEC_VERSION = "0.1.0"


def get_introspect_json() -> str:
    """Return ACLI-compliant JSON describing the reposnap CLI."""
    data = {
        "acli_version": _ACLI_SPEC_VERSION,
        "tool": {
            "name": "reposnap",
            "version": _TOOL_VERSION,
            "description": (
                "Turn any GitHub repo into a clean markdown or JSON digest "
                "of recent activity (commits, releases, issues)."
            ),
            "commands": {
                "default": {
                    "description": "Fetch and format a GitHub repo digest.",
                    "arguments": [
                        {
                            "name": "repo",
                            "description": "owner/repo or full GitHub URL",
                        }
                    ],
                    "options": [
                        {
                            "flag": "--limit/-n",
                            "default": "8",
                            "description": "Items per section",
                        },
                        {
                            "flag": "--format",
                            "default": "markdown",
                            "choices": ["markdown", "json"],
                            "description": "Output format",
                        },
                        {
                            "flag": "--token",
                            "env": "GITHUB_TOKEN",
                            "description": (
                                "GitHub API token (raises rate limit from "
                                "60 to 5000 req/hr)"
                            ),
                        },
                    ],
                },
                "introspect": {
                    "description": (
                        "Print machine-readable ACLI JSON describing this tool."
                    ),
                },
                "skill": {
                    "description": (
                        "Print agentskills.io-compliant SKILL.md for "
                        "agent discovery."
                    ),
                },
            },
        },
    }
    return json.dumps(data, indent=2)


_SKILL_TEMPLATE = """\
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
  version: "{version}"
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
"""


def get_skill_md() -> str:
    """Return agentskills.io-compliant SKILL.md content."""
    return _SKILL_TEMPLATE.format(version=_TOOL_VERSION)
