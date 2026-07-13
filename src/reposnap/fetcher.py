"""Fetch repo data from the GitHub REST API."""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

import httpx

GITHUB_API = "https://api.github.com"


@dataclass
class Commit:
    sha: str
    message: str  # first line only, max 120 chars
    date: str
    url: str


@dataclass
class Release:
    tag: str
    name: str
    date: str
    url: str


@dataclass
class Issue:
    number: int
    title: str
    state: str  # "open" or "closed"
    date: str
    url: str


@dataclass
class RepoData:
    full_name: str  # owner/repo
    description: str
    stars: int
    forks: int
    language: Optional[str]
    commits: list[Commit] = field(default_factory=list)
    releases: list[Release] = field(default_factory=list)
    issues: list[Issue] = field(default_factory=list)


def _headers(token: Optional[str]) -> dict:
    h = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if token:
        h["Authorization"] = f"Bearer {token}"
    return h


def _parse_date(iso: Optional[str]) -> str:
    if not iso:
        return ""
    try:
        return datetime.fromisoformat(iso.replace("Z", "+00:00")).strftime("%Y-%m-%d")
    except ValueError:
        return iso[:10]


def _normalize_repo(name: str) -> str:
    """Accept owner/repo or https://github.com/owner/repo."""
    if name.startswith("https://github.com/"):
        name = name[len("https://github.com/"):]
    return name.strip("/")


def fetch_repo(repo: str, token: Optional[str] = None, limit: int = 8) -> RepoData:
    """Fetch repo data from the GitHub API and return a RepoData object.

    Uses unauthenticated access (60 req/hr) or token auth (5000 req/hr).
    Sections that fail are skipped gracefully — a missing releases endpoint
    won't break the whole call.
    """
    repo = _normalize_repo(repo)
    tok = token or os.environ.get("GITHUB_TOKEN")
    headers = _headers(tok)

    with httpx.Client(headers=headers, timeout=15.0) as client:
        # Repo metadata — this one is not optional
        r = client.get(f"{GITHUB_API}/repos/{repo}")
        r.raise_for_status()
        meta = r.json()

        data = RepoData(
            full_name=meta["full_name"],
            description=meta.get("description") or "",
            stars=meta.get("stargazers_count", 0),
            forks=meta.get("forks_count", 0),
            language=meta.get("language"),
        )

        # Commits — graceful degradation
        try:
            rc = client.get(
                f"{GITHUB_API}/repos/{repo}/commits",
                params={"per_page": limit},
            )
            rc.raise_for_status()
            for c in rc.json()[:limit]:
                msg_full = c.get("commit", {}).get("message", "")
                first_line = msg_full.split("\n")[0][:120]
                sha = (c.get("sha") or "")[:7]
                date = _parse_date(
                    c.get("commit", {}).get("committer", {}).get("date")
                )
                url = c.get(
                    "html_url",
                    f"https://github.com/{repo}/commit/{c.get('sha', '')}",
                )
                data.commits.append(
                    Commit(sha=sha, message=first_line, date=date, url=url)
                )
        except Exception:
            pass

        # Releases — graceful degradation
        try:
            rr = client.get(
                f"{GITHUB_API}/repos/{repo}/releases",
                params={"per_page": limit},
            )
            rr.raise_for_status()
            for rel in rr.json()[:limit]:
                tag = rel.get("tag_name", "")
                name = rel.get("name") or tag
                date = _parse_date(rel.get("published_at"))
                url = rel.get("html_url", "")
                data.releases.append(
                    Release(tag=tag, name=name, date=date, url=url)
                )
        except Exception:
            pass

        # Issues (excluding PRs) — graceful degradation
        try:
            ri = client.get(
                f"{GITHUB_API}/repos/{repo}/issues",
                params={"per_page": limit * 2, "state": "all"},
            )
            ri.raise_for_status()
            raw = [i for i in ri.json() if "pull_request" not in i][:limit]
            for issue in raw:
                data.issues.append(
                    Issue(
                        number=issue["number"],
                        title=issue.get("title", ""),
                        state=issue.get("state", ""),
                        date=_parse_date(issue.get("created_at")),
                        url=issue.get("html_url", ""),
                    )
                )
        except Exception:
            pass

    return data
