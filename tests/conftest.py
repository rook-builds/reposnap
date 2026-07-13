import pytest

from reposnap.fetcher import Commit, Issue, Release, RepoData


@pytest.fixture
def sample_repo() -> RepoData:
    return RepoData(
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
            ),
            Commit(
                sha="f8e9d2a",
                message="Fix streaming race condition",
                date="2026-07-10",
                url="https://github.com/simonw/llm/commit/f8e9d2a",
            ),
        ],
        releases=[
            Release(
                tag="v0.19",
                name="v0.19",
                date="2026-07-08",
                url="https://github.com/simonw/llm/releases/tag/v0.19",
            ),
        ],
        issues=[
            Issue(
                number=847,
                title="Support streaming in async context",
                state="open",
                date="2026-07-12",
                url="https://github.com/simonw/llm/issues/847",
            ),
            Issue(
                number=841,
                title="Add --no-stream flag",
                state="closed",
                date="2026-07-09",
                url="https://github.com/simonw/llm/issues/841",
            ),
        ],
    )
