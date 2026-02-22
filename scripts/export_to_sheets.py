#!/usr/bin/env python3
"""
Export backlog.md to Google Sheets as a structured table.

Prerequisites
-------------
1. Enable the Google Sheets API and Google Drive API in your Google Cloud project.
2. Create a Service Account, download its JSON key file, and share your target
   spreadsheet with the service account's email (Editor role).
3. Set the env var:
       export GOOGLE_SERVICE_ACCOUNT_FILE=/path/to/service-account.json
   Or place credentials.json in the project root (auto-detected).

Usage (via CLI)
---------------
    python scripts/cli.py export <project-path> [--sheet-id <spreadsheet-id>]

Direct usage
------------
    python scripts/export_to_sheets.py projects/spotify-for-kids \
        --sheet-id 1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgVE2upms
"""

import json
import re
import sys
import os
import argparse
from pathlib import Path

import gspread
from google.oauth2.service_account import Credentials

# ─── Google Sheets OAuth scopes ───────────────────────────────────────────────
SCOPES = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
]

# ─── Column definitions (order matters — matches the sheet header row) ────────
COLUMNS = [
    "Build Order",
    "Story ID",
    "Category",
    "Story Title",
    "Description",
    "Effort (SP)",
    "Complexity",
    "Breakdown",
    "Dependencies",
    "Acceptance Criteria",
    "Status",
]

# Header row background colour (light indigo)
HEADER_COLOR = {"red": 0.29, "green": 0.33, "blue": 0.75}
# Alternating row tint (very light blue)
ALT_ROW_COLOR = {"red": 0.93, "green": 0.95, "blue": 1.0}
# White
WHITE = {"red": 1.0, "green": 1.0, "blue": 1.0}


# ─── Parser ───────────────────────────────────────────────────────────────────

def _strip_emoji(text: str) -> str:
    """Remove leading emoji + whitespace from a section heading."""
    return re.sub(r"^[\U00010000-\U0010ffff\u2600-\u27BF\U0001F300-\U0001FAFF]+\s*", "", text).strip()


def _strip_markdown(text: str) -> str:
    """Remove common markdown formatting characters for clean spreadsheet output."""
    # Remove bold/italic markers (**text**, *text*, __text__, _text_)
    text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
    text = re.sub(r"__(.+?)__", r"\1", text)
    text = re.sub(r"\*(.+?)\*", r"\1", text)
    text = re.sub(r"_(.+?)_", r"\1", text)
    # Remove inline code backticks
    text = re.sub(r"`(.+?)`", r"\1", text)
    # Remove standalone asterisks/backticks that weren't part of a pair
    text = text.replace("`", "")
    return text


def parse_backlog(backlog_path: Path) -> list[dict]:
    """Parse backlog.md and return a list of story dicts."""
    text = backlog_path.read_text(encoding="utf-8")

    # Split into top-level sections (## headings)
    section_blocks = re.split(r"\n(?=## )", text)

    stories = []
    for block in section_blocks:
        lines = block.strip().splitlines()
        if not lines:
            continue

        # Determine current category from the ## heading
        first_line = lines[0].strip()
        if first_line.startswith("## "):
            raw_category = first_line[3:].strip()
            category = _strip_emoji(raw_category)
        else:
            category = "General"

        # Find individual stories (### Story …)
        story_blocks = re.split(r"\n(?=### Story )", block)
        for sb in story_blocks:
            if not sb.strip().startswith("### Story "):
                continue
            story = _parse_story_block(sb, category)
            if story:
                stories.append(story)

    return stories


def _parse_story_block(block: str, category: str) -> dict | None:
    """Extract all fields from a single story block."""
    # ── Story heading ──────────────────────────────────────────────
    id_title = re.search(r"^### Story\s+(\w+):\s+(.+)$", block, re.MULTILINE)
    if not id_title:
        return None
    story_id = id_title.group(1).strip()
    story_title = id_title.group(2).strip()

    # ── Description (combined user story + details) ────────────────
    desc_match = re.search(r"^(As\s+an?\s+.+)$", block, re.MULTILINE)
    description = desc_match.group(1).strip() if desc_match else ""
    # Capture the full (possibly multiline) Details block up to the next #### section
    details_match = re.search(r"\*\*Details\*\*:\s*(.*?)(?=\n####\s|\Z)", block, re.DOTALL)
    if details_match:
        details_text = _strip_markdown(details_match.group(1).strip())
        description = f"{description}\n\nDetails:\n{details_text}"

    # ── Effort ─────────────────────────────────────────────────────
    effort_match = re.search(r"Effort Estimate:\s+\*\*(\d+)\s+SP\*\*", block)
    effort_sp = int(effort_match.group(1)) if effort_match else ""

    # ── Complexity ─────────────────────────────────────────────────
    complexity_match = re.search(r"\*\*Complexity\*\*:\s*(⭐+)\s*(\w+)", block)
    if complexity_match:
        stars = len(complexity_match.group(1))
        level = complexity_match.group(2).strip()
        complexity = f"{level} ({stars}★)"
    else:
        complexity = ""

    # ── Breakdown ──────────────────────────────────────────────────
    breakdown_parts = re.findall(r"[-–]\s+(\w[\w\s/]+):\s+([\d.]+)%", block)
    breakdown = ", ".join(f"{role}: {pct}%" for role, pct in breakdown_parts) if breakdown_parts else ""

    # ── Dependencies ───────────────────────────────────────────────
    dep_match = re.search(r"\*\*Dependencies\*\*:\s*(.+)", block)
    dependencies = _strip_markdown(dep_match.group(1).strip()) if dep_match else "None"

    # ── Build Order ────────────────────────────────────────────────
    order_match = re.search(r"\*\*Build Order\*\*:\s*#?(\d+)", block)
    build_order = int(order_match.group(1)) if order_match else 9999

    # ── Acceptance Criteria (full text) ──────────────────────────────
    ac_items = re.findall(r"^\s*- \[[ xX]\]\s*(.+)$", block, re.MULTILINE)
    acceptance_criteria = "\n".join(f"• {_strip_markdown(item.strip())}" for item in ac_items)

    return {
        "Build Order": build_order,
        "Story ID": story_id,
        "Category": category,
        "Story Title": story_title,
        "Description": description,
        "Effort (SP)": effort_sp,
        "Complexity": complexity,
        "Breakdown": breakdown,
        "Dependencies": dependencies,
        "Acceptance Criteria": acceptance_criteria,
        "Status": "Not Started",
    }


def _first_match(pattern: str, text: str) -> str | None:
    m = re.search(pattern, text)
    return m.group(1).strip() if m else None

# ─── Google Sheets helpers ────────────────────────────────────────────────────

def _get_credentials() -> tuple[Credentials, str]:
    """Load service-account credentials from env var or project root."""
    cred_path = os.environ.get("GOOGLE_SERVICE_ACCOUNT_FILE")
    if not cred_path:
        # fallback: look for credentials.json in project root
        fallback = Path(__file__).parent.parent / "credentials.json"
        if fallback.exists():
            cred_path = str(fallback)
    if not cred_path:
        raise FileNotFoundError(
            "Google credentials not found.\n"
            "Set GOOGLE_SERVICE_ACCOUNT_FILE=/path/to/service-account.json\n"
            "or place credentials.json in the project root."
        )
    return Credentials.from_service_account_file(cred_path, scopes=SCOPES), cred_path


def _service_account_email(cred_path: str | None) -> str | None:
    """Return the client_email from the service account JSON file, or None."""
    if not cred_path:
        return None
    try:
        with open(cred_path) as f:
            return json.load(f).get("client_email")
    except Exception:
        return None


def _open_or_create_spreadsheet(gc: gspread.Client, sheet_id: str | None, project_name: str, cred_path: str | None = None, folder_id: str | None = None):
    """Return the gspread Spreadsheet object (open existing or create new)."""
    if sheet_id:
        return gc.open_by_key(sheet_id)

    title = f"Backlog – {project_name}"
    try:
        spreadsheet = gc.create(title, folder_id=folder_id)
        print(f"✅ Created new spreadsheet: {spreadsheet.url}")
        return spreadsheet
    except gspread.exceptions.APIError as exc:
        msg = str(exc)
        sa_email = _service_account_email(cred_path)
        raise SystemExit(
            f"\n❌ Could not create spreadsheet.\n"
            f"   Google error: {msg}\n\n"
            "Make sure the service account has Editor/Content Manager access to the folder:\n"
            f"  {sa_email or '(see client_email in credentials.json)'}\n\n"
            "Alternative – use an existing spreadsheet:\n"
            "  1. Create a blank Google Sheet in your browser (https://sheets.new).\n"
            f"  2. Share it as Editor with the service account above.\n"
            "  3. Copy the spreadsheet ID from its URL and re-run:\n"
            f"       python scripts/cli.py export projects/{project_name} --sheet-id <ID>\n"
        ) from exc


def _get_or_create_worksheet(spreadsheet, title: str = "Backlog"):
    """Return the named worksheet, creating it if it doesn't exist."""
    try:
        ws = spreadsheet.worksheet(title)
        ws.clear()
        return ws
    except gspread.WorksheetNotFound:
        ws = spreadsheet.add_worksheet(title=title, rows=500, cols=len(COLUMNS) + 2)
        # Delete the default empty sheet if it exists
        try:
            default = spreadsheet.worksheet("Sheet1")
            spreadsheet.del_worksheet(default)
        except gspread.WorksheetNotFound:
            pass
        return ws


def _column_letter(n: int) -> str:
    """Convert 1-based column index to A, B, …, Z, AA, AB, …"""
    result = ""
    while n > 0:
        n, rem = divmod(n - 1, 26)
        result = chr(65 + rem) + result
    return result


def _apply_formatting(spreadsheet, ws, num_data_rows: int):
    """Apply header styling and alternating row colours via batch update."""
    last_col = _column_letter(len(COLUMNS))
    sheet_id = ws.id

    requests = []

    # ── Freeze header row ──────────────────────────────────────────
    requests.append({
        "updateSheetProperties": {
            "properties": {
                "sheetId": sheet_id,
                "gridProperties": {"frozenRowCount": 1, "frozenColumnCount": 2},
            },
            "fields": "gridProperties.frozenRowCount,gridProperties.frozenColumnCount",
        }
    })

    # ── Bold + coloured header background ─────────────────────────
    requests.append({
        "repeatCell": {
            "range": {
                "sheetId": sheet_id,
                "startRowIndex": 0,
                "endRowIndex": 1,
                "startColumnIndex": 0,
                "endColumnIndex": len(COLUMNS),
            },
            "cell": {
                "userEnteredFormat": {
                    "backgroundColor": HEADER_COLOR,
                    "textFormat": {
                        "bold": True,
                        "foregroundColor": {"red": 1, "green": 1, "blue": 1},
                        "fontSize": 11,
                    },
                    "horizontalAlignment": "CENTER",
                    "wrapStrategy": "WRAP",
                }
            },
            "fields": "userEnteredFormat(backgroundColor,textFormat,horizontalAlignment,wrapStrategy)",
        }
    })

    # ── Alternating row colours ────────────────────────────────────
    for i in range(num_data_rows):
        row_idx = i + 1  # 0-based, skip header
        colour = ALT_ROW_COLOR if i % 2 == 1 else WHITE
        requests.append({
            "repeatCell": {
                "range": {
                    "sheetId": sheet_id,
                    "startRowIndex": row_idx,
                    "endRowIndex": row_idx + 1,
                    "startColumnIndex": 0,
                    "endColumnIndex": len(COLUMNS),
                },
                "cell": {"userEnteredFormat": {"backgroundColor": colour}},
                "fields": "userEnteredFormat.backgroundColor",
            }
        })

    # ── Auto-resize all columns ────────────────────────────────────
    requests.append({
        "autoResizeDimensions": {
            "dimensions": {
                "sheetId": sheet_id,
                "dimension": "COLUMNS",
                "startIndex": 0,
                "endIndex": len(COLUMNS),
            }
        }
    })

    # ── Wrap text for long columns (Want To, So That, Breakdown, etc.) ──
    long_col_indices = [
        COLUMNS.index(c) for c in ("Description", "Acceptance Criteria", "Breakdown", "Dependencies", "Complexity")
    ]
    for col_idx in long_col_indices:
        requests.append({
            "repeatCell": {
                "range": {
                    "sheetId": sheet_id,
                    "startRowIndex": 1,
                    "endRowIndex": num_data_rows + 1,
                    "startColumnIndex": col_idx,
                    "endColumnIndex": col_idx + 1,
                },
                "cell": {"userEnteredFormat": {"wrapStrategy": "WRAP"}},
                "fields": "userEnteredFormat.wrapStrategy",
            }
        })

    spreadsheet.batch_update({"requests": requests})


# ─── Main export function ─────────────────────────────────────────────────────

def main(project_path_str: str, sheet_id: str | None = None, folder_id: str | None = None):
    project_path = Path(project_path_str)
    backlog_path = project_path / "backlog.md"

    if not backlog_path.exists():
        print(f"❌ backlog.md not found at {backlog_path}")
        print(f"   Run: python scripts/cli.py backlog {project_path_str}")
        sys.exit(1)

    print(f"📖 Parsing {backlog_path} …")
    stories = parse_backlog(backlog_path)
    # Sort by Build Order so the sheet reads top-to-bottom in sequence
    stories.sort(key=lambda s: s["Build Order"])
    print(f"   Found {len(stories)} stories.")

    print("🔑 Loading Google credentials …")
    creds, cred_path = _get_credentials()
    gc = gspread.authorize(creds)

    project_name = project_path.name
    print(f"📊 Opening spreadsheet …")
    spreadsheet = _open_or_create_spreadsheet(gc, sheet_id, project_name, cred_path, folder_id)
    ws = _get_or_create_worksheet(spreadsheet, title="Backlog")

    # Build rows
    header = COLUMNS
    rows = [[story[col] for col in COLUMNS] for story in stories]

    print(f"⬆️  Writing {len(rows)} rows to sheet …")
    ws.update([header] + rows, value_input_option="USER_ENTERED")

    print("🎨 Applying formatting …")
    _apply_formatting(spreadsheet, ws, len(rows))

    print(f"\n✅ Done! Open your spreadsheet:")
    print(f"   {spreadsheet.url}\n")


# ─── CLI entry point ──────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Export backlog.md to Google Sheets."
    )
    parser.add_argument(
        "project_path",
        help="Path to the project folder (e.g. projects/spotify-for-kids)",
    )
    parser.add_argument(
        "--sheet-id",
        default=None,
        help=(
            "Google Spreadsheet ID to update. "
            "If omitted, a new spreadsheet is created automatically."
        ),
    )
    parser.add_argument(
        "--folder-id",
        default=None,
        help=(
            "Google Drive folder ID to create the new spreadsheet in. "
            "Paste the folder ID from the Drive URL. Ignored when --sheet-id is used."
        ),
    )
    args = parser.parse_args()
    main(args.project_path, args.sheet_id, args.folder_id)
