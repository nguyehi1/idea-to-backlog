"""
Unit tests for scripts/cli.py

Run with:  pytest tests/
"""
import os
import sys
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

# cli.py is already on sys.path via conftest.py
import cli


# ── Helpers ────────────────────────────────────────────────────────────────────

def run_cli(*argv: str):
    """Parse argv through the real parser and return the Namespace."""
    parser = cli._build_parser()
    return parser.parse_args(list(argv))


# ── Parser – happy paths ───────────────────────────────────────────────────────

class TestParser:
    def test_new_sets_project_name(self):
        args = run_cli("new", "my-app")
        assert args.project_name == "my-app"
        assert args.func == cli.cmd_new

    def test_prd_sets_project_path(self):
        args = run_cli("prd", "projects/my-app")
        assert args.project_path == "projects/my-app"
        assert args.func == cli.cmd_prd

    def test_stories_sets_project_path(self):
        args = run_cli("stories", "projects/my-app")
        assert args.func == cli.cmd_stories

    def test_backlog_sets_project_path(self):
        args = run_cli("backlog", "projects/my-app")
        assert args.func == cli.cmd_backlog

    def test_export_defaults(self):
        args = run_cli("export", "projects/my-app")
        assert args.project_path == "projects/my-app"
        assert args.sheet_id is None
        assert args.folder_id is None
        assert args.func == cli.cmd_export

    def test_export_with_sheet_id(self):
        args = run_cli("export", "projects/my-app", "--sheet-id", "abc123")
        assert args.sheet_id == "abc123"

    def test_export_with_folder_id(self):
        args = run_cli("export", "projects/my-app", "--folder-id", "folder42")
        assert args.folder_id == "folder42"

    def test_status_sets_project_path(self):
        args = run_cli("status", "projects/my-app")
        assert args.project_path == "projects/my-app"
        assert args.func == cli.cmd_status


# ── Parser – error paths ───────────────────────────────────────────────────────

class TestParserErrors:
    def test_no_command_exits_non_zero(self):
        with pytest.raises(SystemExit) as exc:
            cli._build_parser().parse_args([])
        assert exc.value.code != 0

    def test_unknown_command_exits_non_zero(self):
        with pytest.raises(SystemExit) as exc:
            cli._build_parser().parse_args(["fly"])
        assert exc.value.code != 0

    def test_export_missing_value_for_sheet_id_exits(self):
        """--sheet-id with no value should exit non-zero (argparse enforces this)."""
        with pytest.raises(SystemExit) as exc:
            cli._build_parser().parse_args(["export", "projects/my-app", "--sheet-id"])
        assert exc.value.code != 0

    def test_bare_dash_is_rejected(self):
        """Regression for the failing command: cli.py export <path> -"""
        with pytest.raises(SystemExit) as exc:
            cli._build_parser().parse_args(["export", "projects/my-app", "-"])
        assert exc.value.code != 0


# ── cmd_new ────────────────────────────────────────────────────────────────────

class TestCmdNew:
    def test_creates_project_dir_and_idea_md(self, tmp_path):
        old_cwd = os.getcwd()
        os.chdir(tmp_path)
        try:
            args = MagicMock()
            args.project_name = "cool-app"
            cli.cmd_new(args)
            assert (tmp_path / "projects" / "cool-app").is_dir()
            assert (tmp_path / "projects" / "cool-app" / "idea.md").exists()
        finally:
            os.chdir(old_cwd)

    def test_exits_if_project_already_exists(self, tmp_path):
        old_cwd = os.getcwd()
        os.chdir(tmp_path)
        try:
            (tmp_path / "projects" / "dup-app").mkdir(parents=True)
            args = MagicMock()
            args.project_name = "dup-app"
            with pytest.raises(SystemExit) as exc:
                cli.cmd_new(args)
            assert exc.value.code != 0
        finally:
            os.chdir(old_cwd)


# ── cmd_status ─────────────────────────────────────────────────────────────────

class TestCmdStatus:
    def test_exits_if_project_missing(self, tmp_path):
        args = MagicMock()
        args.project_path = str(tmp_path / "nonexistent")
        with pytest.raises(SystemExit) as exc:
            cli.cmd_status(args)
        assert exc.value.code != 0

    def test_shows_all_four_files(self, tmp_path, capsys):
        for f in ("idea.md", "prd.md", "user_stories.md", "backlog.md"):
            (tmp_path / f).write_text("content")
        args = MagicMock()
        args.project_path = str(tmp_path)
        cli.cmd_status(args)
        out = capsys.readouterr().out
        assert "idea.md" in out
        assert "prd.md" in out
        assert "user_stories.md" in out
        assert "backlog.md" in out
        assert "All stages complete" in out

    def test_incomplete_project_shows_next_step(self, tmp_path, capsys):
        (tmp_path / "idea.md").write_text("content")
        args = MagicMock()
        args.project_path = str(tmp_path)
        cli.cmd_status(args)
        out = capsys.readouterr().out
        assert "prd" in out.lower()


# ── cmd_* dispatch ─────────────────────────────────────────────────────────────

class TestCommandDispatch:
    def test_cmd_prd_calls_generate_prd(self):
        mock_mod = MagicMock()
        with patch.dict(sys.modules, {"generate_prd": mock_mod}):
            args = run_cli("prd", "projects/my-app")
            cli.cmd_prd(args)
        mock_mod.main.assert_called_once_with("projects/my-app", force=False)

    def test_cmd_stories_calls_generate_stories(self):
        mock_mod = MagicMock()
        with patch.dict(sys.modules, {"generate_stories": mock_mod}):
            args = run_cli("stories", "projects/my-app")
            cli.cmd_stories(args)
        mock_mod.main.assert_called_once_with("projects/my-app", force=False)

    def test_cmd_backlog_calls_generate_backlog(self):
        mock_mod = MagicMock()
        with patch.dict(sys.modules, {"generate_backlog": mock_mod}):
            args = run_cli("backlog", "projects/my-app")
            cli.cmd_backlog(args)
        mock_mod.main.assert_called_once_with("projects/my-app", force=False)

    def test_cmd_export_passes_all_args(self):
        mock_mod = MagicMock()
        with patch.dict(sys.modules, {"export_to_sheets": mock_mod}):
            args = run_cli("export", "projects/my-app", "--sheet-id", "s1", "--folder-id", "f1")
            cli.cmd_export(args)
        mock_mod.main.assert_called_once_with("projects/my-app", "s1", "f1")

    def test_cmd_export_passes_nones_when_flags_omitted(self):
        mock_mod = MagicMock()
        with patch.dict(sys.modules, {"export_to_sheets": mock_mod}):
            args = run_cli("export", "projects/my-app")
            cli.cmd_export(args)
        mock_mod.main.assert_called_once_with("projects/my-app", None, None)
