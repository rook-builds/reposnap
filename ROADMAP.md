# reposnap Roadmap

## v0.1 (current)

**Scope:** Single repo → markdown or JSON digest of recent activity.

**Features:**
- `reposnap <repo>` — accepts `owner/repo` or `https://github.com/owner/repo`
- `--limit N` — items per section (default 8)
- `--format [markdown|json]` — output format (default markdown)
- `--token TOKEN` — GitHub API token, falls back to `GITHUB_TOKEN` env var
- Three sections: **Recent Commits**, **Releases**, **Recent Issues**
- Unauthenticated access works for public repos (60 req/hr); token raises limit to 5000/hr
- Graceful degradation: if a section fails (e.g. no releases), skip it with a warning
- pytest suite with mocked GitHub API responses
- MIT license, proper pyproject.toml packaging

**Out of scope for v0.1:**
- Multiple repos in one invocation
- Pull request section
- `--since` date filter
- Private repo support
- TOML/OPML-style config files

## v0.2 (planned)

- `--since DATE` filter (same syntax as feedsnap: YYYY-MM-DD or Nd)
- Pull requests section
- `--sections` flag to choose which sections to include

## v0.3 (ideas)

- Config file support (list of repos, like OPML for feedsnap)
- `--watch` mode / scheduling

## Design Notes

- Uses GitHub REST API v3 (`api.github.com/repos/{owner}/{repo}/...`)
- No GitHub SDK dependency — plain `httpx` or `urllib` calls keep the dep tree small
- Response data normalized into dataclasses (same pattern as feedsnap's Feed/FeedEntry)
- JSON output schema: `{"repo": "owner/repo", "commits": [...], "releases": [...], "issues": [...]}`
