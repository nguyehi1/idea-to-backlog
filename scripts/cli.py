#!/usr/bin/env python3
"""
PM Planner CLI - Main orchestrator
"""

import argparse
import sys
from pathlib import Path


# ─── Idea template ────────────────────────────────────────────────────────────

_IDEA_TEMPLATE = """\
# Project: [Project Name]

## Product Overview
[Describe your product idea in 2-3 sentences]

---

## Context

### Business Goal
[What business objective does this achieve?]

### Target Users
[Who will use this product?]

### Technical Constraints
[Any technical limitations or requirements?]

### Success Metrics
[How will you measure success?]

### Known Assumptions
[What assumptions are you making?]

### Out of Scope (for MVP)
[What are you explicitly NOT building?]
"""

# ─── Command handlers ─────────────────────────────────────────────────────────

def cmd_new(args: argparse.Namespace) -> None:
    """Create a new project with template."""
    projects_dir = Path("projects")
    projects_dir.mkdir(exist_ok=True)

    project_path = projects_dir / args.project_name
    if project_path.exists():
        print(f"❌ Project '{args.project_name}' already exists at {project_path}")
        sys.exit(1)

    project_path.mkdir()
    idea_path = project_path / "idea.md"
    idea_path.write_text(_IDEA_TEMPLATE)

    print(f"✅ Created new project: {project_path}")
    print(f"\nNext steps:")
    print(f"1. Edit {idea_path} with your product idea")
    print(f"2. Run: python scripts/cli.py prd {project_path}")


def cmd_prd(args: argparse.Namespace) -> None:
    import generate_prd
    generate_prd.main(args.project_path, force=args.force)


def cmd_stories(args: argparse.Namespace) -> None:
    import generate_stories
    generate_stories.main(args.project_path, force=args.force)


def cmd_backlog(args: argparse.Namespace) -> None:
    import generate_backlog
    generate_backlog.main(args.project_path, force=args.force)


def cmd_export(args: argparse.Namespace) -> None:
    import export_to_sheets
    export_to_sheets.main(args.project_path, args.sheet_id, args.folder_id)


def cmd_status(args: argparse.Namespace) -> None:
    """Show current project status."""
    project_path = Path(args.project_path)
    if not project_path.exists():
        print(f"❌ Project directory not found: {project_path}")
        sys.exit(1)

    print(f"📊 Project Status: {project_path.name}")
    print("=" * 60)

    files = {
        "idea.md": "Product idea and context",
        "prd.md": "Product Requirements Document",
        "user_stories.md": "Categorized user stories",
        "backlog.md": "Sprint backlog with estimates",
    }

    current_stage = 0
    for filename, description in files.items():
        filepath = project_path / filename
        if filepath.exists():
            size = filepath.stat().st_size
            print(f"✅ {filename:20s} ({size:,} bytes) - {description}")
            current_stage += 1
        else:
            print(f"⬜ {filename:20s} - {description}")

    print("=" * 60)

    next_steps = {
        0: (f"📝 Next step: Edit idea.md with your product concept\n"
            f"   Then run: python scripts/cli.py prd {project_path}"),
        1: (f"🤖 Next step: Generate PRD\n"
            f"   Run: python scripts/cli.py prd {project_path}"),
        2: (f"📝 Review prd.md, then generate user stories\n"
            f"   Run: python scripts/cli.py stories {project_path}"),
        3: (f"📝 Review user_stories.md, then generate backlog\n"
            f"   Run: python scripts/cli.py backlog {project_path}"),
        4: "✅ All stages complete!\n   Review backlog.md and start sprint planning 🚀",
    }
    print(f"\n{next_steps[current_stage]}")


# ─── Epilog shown at the bottom of --help ────────────────────────────────────

_EPILOG = """\
Workflow:
  1. cli.py new <name>               Create project
  2. Edit idea.md
  3. cli.py prd projects/<name>      Generate PRD
  4. Review / edit prd.md
  5. cli.py stories projects/<name>  Generate user stories
  6. Review / edit user_stories.md
  7. cli.py backlog projects/<name>  Generate backlog
  8. Review backlog.md
  9. cli.py export projects/<name>   Export to Google Sheets
"""

# ─── Argument parser ──────────────────────────────────────────────────────────

def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="cli.py",
        description="PM Planner – AI-powered user story generator",
        epilog=_EPILOG,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="command", metavar="<command>")
    sub.required = True

    # new
    p_new = sub.add_parser("new", help="Create a new project with template")
    p_new.add_argument("project_name", metavar="<project-name>")
    p_new.set_defaults(func=cmd_new)

    # prd
    p_prd = sub.add_parser("prd", help="Generate PRD from idea.md")
    p_prd.add_argument("project_path", metavar="<project-path>")
    p_prd.add_argument("-f", "--force", action="store_true", help="Overwrite existing file without prompting")
    p_prd.set_defaults(func=cmd_prd)

    # stories
    p_stories = sub.add_parser("stories", help="Generate user stories from prd.md")
    p_stories.add_argument("project_path", metavar="<project-path>")
    p_stories.add_argument("-f", "--force", action="store_true", help="Overwrite existing file without prompting")
    p_stories.set_defaults(func=cmd_stories)

    # backlog
    p_backlog = sub.add_parser("backlog", help="Generate backlog from user_stories.md")
    p_backlog.add_argument("project_path", metavar="<project-path>")
    p_backlog.add_argument("-f", "--force", action="store_true", help="Overwrite existing file without prompting")
    p_backlog.set_defaults(func=cmd_backlog)

    # export
    p_export = sub.add_parser("export", help="Export backlog.md to Google Sheets")
    p_export.add_argument("project_path", metavar="<project-path>")
    p_export.add_argument(
        "--sheet-id",
        default=None,
        help="Spreadsheet ID to update (omit to create a new sheet)",
    )
    p_export.add_argument(
        "--folder-id",
        default=None,
        help="Drive folder ID for new sheet creation (ignored when --sheet-id is set)",
    )
    p_export.set_defaults(func=cmd_export)

    # status
    p_status = sub.add_parser("status", help="Show current project status")
    p_status.add_argument("project_path", metavar="<project-path>")
    p_status.set_defaults(func=cmd_status)

    return parser


# ─── Entry point ──────────────────────────────────────────────────────────────

def main() -> None:
    parser = _build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
