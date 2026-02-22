#!/usr/bin/env python3
"""
Generate user_stories.md from prd.md using Google Gemini API
"""

import sys
from pathlib import Path
from utils import run_generation


def main(project_path_str: str = None, force: bool = False):
    if project_path_str is None:
        if len(sys.argv) != 2:
            print("Usage: python generate_stories.py <project-path>")
            print("Example: python generate_stories.py projects/spotify-for-kids")
            sys.exit(1)
        project_path_str = sys.argv[1]

    project_path = Path(project_path_str)
    if not project_path.exists():
        print(f"❌ Project directory not found: {project_path}")
        sys.exit(1)

    run_generation(
        project_path=project_path,
        input_filename="prd.md",
        output_filename="user_stories.md",
        prompt_filename="stories_prompt.txt",
        context="PRD",
        required_file="prd.md",
        success_msg="User stories generation complete!",
        next_steps=(
            f"\nNext steps:\n"
            f"1. Review and edit: {project_path}/user_stories.md\n"
            f"2. Then run: python scripts/generate_backlog.py {project_path}"
        ),
        force=force,
    )


if __name__ == "__main__":
    main()
