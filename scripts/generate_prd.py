#!/usr/bin/env python3
"""
Generate PRD from idea.md using Google Gemini API
"""

import sys
from pathlib import Path
from utils import run_generation


def main(project_path_str: str = None, force: bool = False):
    if project_path_str is None:
        if len(sys.argv) != 2:
            print("Usage: python generate_prd.py <project-path>")
            print("Example: python generate_prd.py projects/spotify-for-kids")
            sys.exit(1)
        project_path_str = sys.argv[1]

    project_path = Path(project_path_str)
    if not project_path.exists():
        print(f"❌ Project directory not found: {project_path}")
        sys.exit(1)

    run_generation(
        project_path=project_path,
        input_filename="idea.md",
        output_filename="prd.md",
        prompt_filename="prd_prompt.txt",
        context="product idea and context",
        success_msg="PRD generation complete!",
        next_steps=(
            f"\nNext steps:\n"
            f"1. Review and edit: {project_path}/prd.md\n"
            f"2. Then run: python scripts/generate_stories.py {project_path}"
        ),
        force=force,
    )


if __name__ == "__main__":
    main()
