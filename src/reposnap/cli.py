"""Command-line interface for reposnap."""
from __future__ import annotations

import sys

import click

from .fetcher import fetch_repo
from .formatter import format_repo


@click.command()
@click.argument("repo")
@click.option(
    "--limit",
    "-n",
    default=8,
    show_default=True,
    help="Items per section.",
)
@click.option(
    "--format",
    "fmt",
    default="markdown",
    show_default=True,
    type=click.Choice(["markdown", "json"]),
    help="Output format.",
)
@click.option(
    "--token",
    envvar="GITHUB_TOKEN",
    default=None,
    help="GitHub API token. Raises rate limit from 60 to 5000 req/hr.",
)
def main(repo: str, limit: int, fmt: str, token: str | None) -> None:
    """Turn any GitHub repo into a clean markdown digest of recent activity.

    REPO is owner/repo or a full GitHub URL.

    \b
    Examples:
      reposnap simonw/llm
      reposnap --format json simonw/llm
      reposnap --limit 5 https://github.com/simonw/llm
    """
    try:
        data = fetch_repo(repo, token=token, limit=limit)
    except Exception as exc:
        click.echo(f"Error: {exc}", err=True)
        sys.exit(1)

    click.echo(format_repo(data, fmt=fmt))
