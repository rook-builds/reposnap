import json
from unittest.mock import patch

import pytest
from click.testing import CliRunner

from reposnap.cli import main
from reposnap.fetcher import Commit, Issue, Release, RepoData

SAMPLE = RepoData(
    full_name="simonw/llm",
    description="Access large language models from the command line.",
    stars=4500,
    forks=320,
    language="Python",
    commits=[
        Commit(
            sha="a1b2c3d",
            message="Add support for attachments",
            date="2026-07-11",
            url="https://github.com/simonw/llm/commit/a1b2c3d",
        )
    ],
    releases=[],
    issues=[],
)


def test_cli_basic():
    runner = CliRunner()
    with patch("reposnap.cli.fetch_repo", return_value=SAMPLE):
        result = runner.invoke(main, ["simonw/llm"])
    assert result.exit_code == 0
    assert "simonw/llm" in result.output


def test_cli_markdown_default():
    runner = CliRunner()
    with patch("reposnap.cli.fetch_repo", return_value=SAMPLE):
        result = runner.invoke(main, ["simonw/llm"])
    assert result.exit_code == 0
    assert result.output.startswith("# simonw/llm")


def test_cli_json_format():
    runner = CliRunner()
    with patch("reposnap.cli.fetch_repo", return_value=SAMPLE):
        result = runner.invoke(main, ["simonw/llm", "--format", "json"])
    assert result.exit_code == 0
    parsed = json.loads(result.output)
    assert parsed["repo"] == "simonw/llm"
    assert parsed["stars"] == 4500


def test_cli_limit_passed_through():
    runner = CliRunner()
    with patch("reposnap.cli.fetch_repo", return_value=SAMPLE) as mock_fetch:
        result = runner.invoke(main, ["simonw/llm", "--limit", "3"])
    mock_fetch.assert_called_once_with("simonw/llm", token=None, limit=3)
    assert result.exit_code == 0


def test_cli_error_exits_nonzero():
    runner = CliRunner()
    with patch(
        "reposnap.cli.fetch_repo", side_effect=Exception("404 Not Found")
    ):
        result = runner.invoke(main, ["nonexistent/repo"])
    assert result.exit_code == 1


def test_cli_accepts_full_url():
    """https://github.com/owner/repo is valid input."""
    runner = CliRunner()
    with patch("reposnap.cli.fetch_repo", return_value=SAMPLE) as mock_fetch:
        result = runner.invoke(main, ["https://github.com/simonw/llm"])
    assert result.exit_code == 0
    # The URL gets passed through to fetch_repo, which normalizes it
    assert mock_fetch.called
