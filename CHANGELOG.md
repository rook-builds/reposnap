# Changelog

## [0.2.0] - 2026-07-27

### Added
- `reposnap introspect` — prints ACLI-compliant JSON describing the tool
  (command tree, arguments, options, types) for agent pipeline integration
- `reposnap skill` — prints an agentskills.io-compliant SKILL.md for agent
  discovery and bootstrapping
- `SKILL.md` committed to repo root as a static discovery artifact
- `get_introspect_json()` and `get_skill_md()` exported from the public API
  (`from reposnap import get_introspect_json, get_skill_md`)
- 18 new tests in `tests/test_introspect.py`

## [0.1.2] - 2026-07-13

### Fixed
- PyPI packaging: corrected hatchling `packages` path to `src/reposnap`

## [0.1.1] - 2026-07-13

### Fixed
- Package renamed to `rook-reposnap` on PyPI (name `reposnap` was taken)

## [0.1.0] - 2026-07-13

### Added
- Initial release: GitHub repo → markdown or JSON digest
- Sections: Recent Commits, Releases, Issues (PRs excluded)
- `--limit`, `--format`, `--token` / `GITHUB_TOKEN` options
- Accepts `owner/repo` or full GitHub URL
- Graceful degradation: each section fails independently
