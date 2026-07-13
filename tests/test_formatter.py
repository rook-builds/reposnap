import json

import pytest

from reposnap.fetcher import Commit, Issue, Release, RepoData
from reposnap.formatter import format_repo, format_repo_json, format_repo_markdown


def test_markdown_header(sample_repo):
    out = format_repo_markdown(sample_repo)
    assert "# simonw/llm" in out


def test_markdown_description(sample_repo):
    out = format_repo_markdown(sample_repo)
    assert "Access large language models" in out


def test_markdown_stars(sample_repo):
    out = format_repo_markdown(sample_repo)
    assert "4500" in out


def test_markdown_language(sample_repo):
    out = format_repo_markdown(sample_repo)
    assert "Python" in out


def test_markdown_commits_section(sample_repo):
    out = format_repo_markdown(sample_repo)
    assert "## Recent Commits" in out
    assert "Add support for attachments" in out
    assert "a1b2c3d" in out


def test_markdown_releases_section(sample_repo):
    out = format_repo_markdown(sample_repo)
    assert "## Releases" in out
    assert "v0.19" in out


def test_markdown_issues_section(sample_repo):
    out = format_repo_markdown(sample_repo)
    assert "## Recent Issues" in out
    assert "#847" in out
    assert "open" in out
    assert "closed" in out


def test_json_top_level_fields(sample_repo):
    parsed = json.loads(format_repo_json(sample_repo))
    assert parsed["repo"] == "simonw/llm"
    assert parsed["stars"] == 4500
    assert parsed["forks"] == 320
    assert parsed["language"] == "Python"


def test_json_commits(sample_repo):
    parsed = json.loads(format_repo_json(sample_repo))
    assert len(parsed["commits"]) == 2
    assert parsed["commits"][0]["sha"] == "a1b2c3d"


def test_json_releases(sample_repo):
    parsed = json.loads(format_repo_json(sample_repo))
    assert len(parsed["releases"]) == 1
    assert parsed["releases"][0]["tag"] == "v0.19"


def test_json_issues(sample_repo):
    parsed = json.loads(format_repo_json(sample_repo))
    assert len(parsed["issues"]) == 2
    assert parsed["issues"][0]["number"] == 847


def test_format_dispatch_markdown(sample_repo):
    out = format_repo(sample_repo, fmt="markdown")
    assert out.startswith("# simonw/llm")


def test_format_dispatch_json(sample_repo):
    out = format_repo(sample_repo, fmt="json")
    parsed = json.loads(out)
    assert "repo" in parsed


def test_empty_repo_no_sections():
    """Repo with no activity renders cleanly with no empty section headers."""
    empty = RepoData(
        full_name="foo/bar", description="", stars=0, forks=0, language=None
    )
    out = format_repo_markdown(empty)
    assert "# foo/bar" in out
    assert "## Recent Commits" not in out
    assert "## Releases" not in out
    assert "## Recent Issues" not in out


def test_no_language_omitted():
    """Repos with no primary language don't show 'None' in output."""
    repo = RepoData(
        full_name="foo/bar", description="", stars=1, forks=0, language=None
    )
    out = format_repo_markdown(repo)
    assert "None" not in out
