"""Tests for reposnap.introspect (ACLI JSON and agentskills.io SKILL.md)."""
import json

import pytest
from click.testing import CliRunner

from reposnap.cli import main
from reposnap.introspect import get_introspect_json, get_skill_md


# ---------------------------------------------------------------------------
# Unit tests — get_introspect_json()
# ---------------------------------------------------------------------------


def test_introspect_returns_valid_json():
    result = get_introspect_json()
    parsed = json.loads(result)  # raises if invalid
    assert isinstance(parsed, dict)


def test_introspect_has_acli_version():
    parsed = json.loads(get_introspect_json())
    assert "acli_version" in parsed


def test_introspect_tool_name():
    parsed = json.loads(get_introspect_json())
    assert parsed["tool"]["name"] == "reposnap"


def test_introspect_has_version_field():
    parsed = json.loads(get_introspect_json())
    assert "version" in parsed["tool"]


def test_introspect_has_commands():
    parsed = json.loads(get_introspect_json())
    commands = parsed["tool"]["commands"]
    assert "default" in commands
    assert "introspect" in commands
    assert "skill" in commands


def test_introspect_default_command_has_arguments():
    parsed = json.loads(get_introspect_json())
    args = parsed["tool"]["commands"]["default"]["arguments"]
    assert any(a["name"] == "repo" for a in args)


# ---------------------------------------------------------------------------
# Unit tests — get_skill_md()
# ---------------------------------------------------------------------------


def test_skill_returns_string():
    result = get_skill_md()
    assert isinstance(result, str)


def test_skill_has_yaml_frontmatter():
    result = get_skill_md()
    assert result.startswith("---")
    lines = result.split("\n")
    # There must be a closing --- somewhere after the first line
    assert any(line.strip() == "---" for line in lines[1:])


def test_skill_has_name():
    result = get_skill_md()
    assert "name: reposnap" in result


def test_skill_has_license():
    result = get_skill_md()
    assert "license: MIT" in result


def test_skill_has_author():
    result = get_skill_md()
    assert "author: rook-builds" in result


def test_skill_has_core_usage():
    result = get_skill_md()
    assert "## Core usage" in result


def test_skill_has_exit_codes():
    result = get_skill_md()
    assert "## Exit codes" in result


def test_skill_has_agent_discovery():
    result = get_skill_md()
    assert "## Agent discovery" in result


# ---------------------------------------------------------------------------
# CLI integration tests
# ---------------------------------------------------------------------------


def test_cli_introspect_exits_zero():
    runner = CliRunner()
    result = runner.invoke(main, ["introspect"])
    assert result.exit_code == 0


def test_cli_introspect_outputs_valid_json():
    runner = CliRunner()
    result = runner.invoke(main, ["introspect"])
    parsed = json.loads(result.output)
    assert parsed["tool"]["name"] == "reposnap"


def test_cli_skill_exits_zero():
    runner = CliRunner()
    result = runner.invoke(main, ["skill"])
    assert result.exit_code == 0


def test_cli_skill_contains_name():
    runner = CliRunner()
    result = runner.invoke(main, ["skill"])
    assert "name: reposnap" in result.output


def test_cli_no_args_exits_nonzero():
    """Invoking reposnap with no arguments should error (not an ACLI command)."""
    runner = CliRunner()
    result = runner.invoke(main, [])
    assert result.exit_code != 0
