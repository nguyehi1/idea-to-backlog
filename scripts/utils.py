#!/usr/bin/env python3
"""
Shared utilities for PM Planner scripts
"""

import os
from pathlib import Path
from datetime import datetime
from google import genai
from google.genai import types, errors

# Module-level Gemini client singleton (avoids re-instantiation on every call)
_client = None


def load_prompt_template(prompt_file: str) -> str:
    """Load prompt template from prompts/ directory"""
    prompt_path = Path(__file__).parent.parent / "prompts" / prompt_file
    try:
        with open(prompt_path, 'r') as f:
            return f.read()
    except FileNotFoundError:
        raise FileNotFoundError(
            f"Prompt template '{prompt_file}' not found at {prompt_path}.\n"
            f"Ensure it exists in the prompts/ directory."
        )


def get_gemini_client():
    """Configure and return Gemini client (singleton — created once per process)."""
    global _client
    if _client is None:
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY environment variable not set.\n"
                "Please set it with: export GEMINI_API_KEY='your-api-key'"
            )
        _client = genai.Client(api_key=api_key)
    return _client


def generate_with_gemini(system_prompt: str, content: str, context: str) -> str:
    """
    Generate content using Gemini API with live streaming output.

    Args:
        system_prompt: The system prompt template
        content: The input content to process
        context: Description of what's being generated (e.g., "PRD", "user stories")

    Returns:
        Generated content from Gemini
    """
    client = get_gemini_client()

    user_prompt = (
        f"Here is the {context}:\n\n{content}\n\n"
        f"Today's date is {datetime.now().strftime('%Y-%m-%d')}."
    )

    try:
        chunks = []
        for chunk in client.models.generate_content_stream(
            model="gemini-2.5-flash",
            contents=user_prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                temperature=0.2,
                max_output_tokens=65536,
            ),
        ):
            if chunk.text:
                print(chunk.text, end="", flush=True)
                chunks.append(chunk.text)
        print()  # newline after streaming finishes
        return "".join(chunks)
    except errors.ClientError as e:
        msg = str(e)
        if "429" in msg or "RESOURCE_EXHAUSTED" in msg:
            raise RuntimeError(
                "Rate limit exceeded. Please wait a moment and retry.\n"
                f"Details: {e}"
            ) from e
        elif any(code in msg for code in ("401", "403", "API_KEY", "UNAUTHENTICATED")):
            raise RuntimeError(
                "Authentication failed. Check your GEMINI_API_KEY.\n"
                f"Details: {e}"
            ) from e
        else:
            raise RuntimeError(f"Gemini API error: {e}") from e
    except errors.ServerError as e:
        raise RuntimeError(
            "Gemini server error (5xx). This is likely transient — please retry.\n"
            f"Details: {e}"
        ) from e


def load_file(project_path: Path, filename: str, required_file: str = None) -> str:
    """
    Load a file from project directory with helpful error messages
    
    Args:
        project_path: Path to the project directory
        filename: Name of the file to load
        required_file: Optional name of prerequisite file for error message
    
    Returns:
        File content as string
    
    Raises:
        FileNotFoundError: If file doesn't exist
    """
    file_path = project_path / filename
    
    if not file_path.exists():
        error_msg = f"{filename} not found in {project_path}"
        if required_file:
            error_msg += f". Run generate_{Path(required_file).stem}.py first."
        raise FileNotFoundError(error_msg)

    with open(file_path, 'r') as f:
        content = f.read()

    if not content.strip():
        raise ValueError(
            f"{filename} in {project_path} is empty.\n"
            "Make sure the file is saved and contains content before generating."
        )

    return content


def save_file(project_path: Path, filename: str, content: str, force: bool = False):
    """Save content to file in project directory, prompting before overwrite.
    
    Pass force=True to skip the confirmation prompt.
    """
    file_path = project_path / filename
    if file_path.exists() and not force:
        try:
            confirm = input(f"⚠️  {filename} already exists. Overwrite? [y/N] ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            confirm = "n"
        if confirm != "y":
            print(f"⏭️  Skipped: {file_path}")
            return
    try:
        with open(file_path, "w") as f:
            f.write(content)
    except OSError as e:
        raise OSError(f"Failed to write {file_path}: {e}") from e
    print(f"✅ Generated: {file_path}")


def run_generation(
    project_path: Path,
    input_filename: str,
    output_filename: str,
    prompt_filename: str,
    context: str,
    required_file: str = None,
    success_msg: str = None,
    next_steps: str = None,
    force: bool = False,
):
    """
    Shared pipeline: load input → generate with Gemini → save output.
    Eliminates boilerplate duplicated across all generate_*.py scripts.
    Pass force=True to overwrite existing output without prompting.
    """
    # ── Guard: check for overwrite before burning API tokens ──────────────────
    output_path = project_path / output_filename
    if output_path.exists() and not force:
        try:
            confirm = input(f"⚠️  {output_filename} already exists. Overwrite? [y/N] ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            confirm = "n"
        if confirm != "y":
            print(f"⏭️  Skipped: {output_path}")
            return

    print(f"📖 Reading {input_filename} from {project_path}...")
    input_content = load_file(project_path, input_filename, required_file=required_file)

    print(f"🤖 Generating {context} with Gemini...")
    system_prompt = load_prompt_template(prompt_filename)
    output_content = generate_with_gemini(system_prompt, input_content, context)

    print(f"💾 Saving {output_filename}...")
    save_file(project_path, output_filename, output_content, force=True)  # pre-checked above

    if success_msg:
        print("\n" + "=" * 60)
        print(f"✅ {success_msg}")
        print("=" * 60)

    if next_steps:
        print(next_steps)
