"""Command-line interface for reposnap."""
from __future__ import annotations

import sys

import click

from .fetcher import fetch_repo
from .formatter import format_repo
from .introspect import get_introspect_json, get_skill_md

# ---------------------------------------------------------------------------
# ACLI special sub-commands (handled before Click sees them)
# ---------------------------------------------------------------------------

#: When the first positional argument is one of these, we dispatch to the
#: corresponding ACLI function instead of treating it as a repo reference.
_ACLI_COMMANDS = {"introspect", "skill"}


def _handle_acli_command(name: str) -> None:
    """Dispatch to an ACLI built-in and exit."""
    if name == "introspect":
        click.echo(get_introspect_json())
    elif name == "skill":
        click.echo(get_skill_md(), nl=False)
    sys.exit(0)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


@click.command(context_settings={"help_option_names": ["-h", "--help"]})
@click.argument("repo", required=False, default=None)
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
def main(repo: str | None, limit: int, fmt: str, token: str | None) -> None:
    """Turn any GitHub repo into a clean markdown digest of recent activity.

    REPO is owner/repo or a full GitHub URL.

    \b
    ACLI built-in commands (agent discovery):
      reposnap introspect   Output the full command tree as JSON.
      reposnap skill        Output a SKILL.md for agent bootstrapping.

    \b
    Examples:
      reposnap simonw/llm
      reposnap --format json simonw/llm
      reposnap --limit 5 https://github.com/simonw/llm
    """
    # ── ACLI dispatch ────────────────────────────────────────────────────────
    if repo in _ACLI_COMMANDS:
        _handle_acli_command(repo)
        return  # unreachable (sys.exit inside), satisfies type checkers

    # Require a repo argument when not an ACLI command
    if repo is None:
        click.echo(
            "Error: Provide a repo (owner/repo or GitHub URL).\n\n"
            "Try 'reposnap --help' for usage.\n"
            "Try 'reposnap introspect' for machine-readable capability info.",
            err=True,
        )
        sys.exit(1)

    try:
        data = fetch_repo(repo, token=token, limit=limit)
    except Exception as exc:
        click.echo(f"Error: {exc}", err=True)
        sys.exit(1)

    click.echo(format_repo(data, fmt=fmt))
