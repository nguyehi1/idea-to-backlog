#!/usr/bin/env python3
"""
Generate backlog.md from user_stories.md using Google Gemini API
"""

import sys
from pathlib import Path
from utils import run_generation


def main(project_path_str: str = None, force: bool = False):
    if project_path_str is None:
        if len(sys.argv) != 2:
            print("Usage: python generate_backlog.py <project-path>")
            print("Example: python generate_backlog.py projects/spotify-for-kids")
            sys.exit(1)
        project_path_str = sys.argv[1]

    project_path = Path(project_path_str)
    if not project_path.exists():
        print(f"❌ Project directory not found: {project_path}")
        sys.exit(1)

    run_generation(
        project_path=project_path,
        input_filename="user_stories.md",
        output_filename="backlog.md",
        prompt_filename="backlog_prompt.txt",
        context="user stories",
        required_file="user_stories.md",
        success_msg="Backlog generation complete!",
        next_steps=(
            f"\nYour sprint backlog is ready at: {project_path}/backlog.md\n"
            "\nNext steps:\n"
            "1. Review estimates and adjust based on your team's velocity\n"
            "2. Start sprint planning!\n"
            "3. After completing stories, update with actual effort for calibration"
        ),
        force=force,
    )


if __name__ == "__main__":
    main()
