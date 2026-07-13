"""Format a RepoData object as markdown or JSON."""
from __future__ import annotations

import json

from .fetcher import RepoData


def _section(title: str) -> str:
    return f"\n## {title}\n"


def format_repo_markdown(data: RepoData) -> str:
    lines = [f"# {data.full_name}"]

    if data.description:
        lines.append(f"\n{data.description}")

    meta_parts = [f"⭐ {data.stars}", f"🍴 {data.forks}"]
    if data.language:
        meta_parts.append(data.language)
    lines.append("\n" + " · ".join(meta_parts))

    if data.commits:
        lines.append(_section("Recent Commits"))
        for c in data.commits:
            lines.append(
                f"- **{c.message}** · [{c.sha}]({c.url}) · {c.date}"
            )

    if data.releases:
        lines.append(_section("Releases"))
        for r in data.releases:
            lines.append(f"- **{r.name}** · {r.date} · [notes]({r.url})")

    if data.issues:
        lines.append(_section("Recent Issues"))
        for i in data.issues:
            lines.append(
                f"- **[#{i.number}] {i.title}** · {i.state} · {i.date}"
            )

    return "\n".join(lines) + "\n"


def format_repo_json(data: RepoData) -> str:
    obj = {
        "repo": data.full_name,
        "description": data.description,
        "stars": data.stars,
        "forks": data.forks,
        "language": data.language,
        "commits": [
            {"sha": c.sha, "message": c.message, "date": c.date, "url": c.url}
            for c in data.commits
        ],
        "releases": [
            {"tag": r.tag, "name": r.name, "date": r.date, "url": r.url}
            for r in data.releases
        ],
        "issues": [
            {
                "number": i.number,
                "title": i.title,
                "state": i.state,
                "date": i.date,
                "url": i.url,
            }
            for i in data.issues
        ],
    }
    return json.dumps(obj, indent=2)


def format_repo(data: RepoData, fmt: str = "markdown") -> str:
    """Dispatch to markdown or JSON formatter."""
    if fmt == "json":
        return format_repo_json(data)
    return format_repo_markdown(data)
