"""
Unit tests for scripts/export_to_sheets.py – parser layer

Run with:  pytest tests/
"""
import pytest
from pathlib import Path

import export_to_sheets as ex


# ── Shared fixtures ────────────────────────────────────────────────────────────

MINIMAL_STORY_BLOCK = """\
### Story US001: Play a Song
As a child, I want to tap a song tile, so that I can hear music immediately.
**Details**: Audio player component, tap interaction, loading state

Effort Estimate: **5 SP**

**Complexity**: ⭐⭐⭐ High

- Child: 60%
- Backend: 40%

**Dependencies**: US002
**Build Order**: #1

#### Acceptance Criteria
- [ ] Song starts playing within 2 seconds
- [ ] Play button shows a pause icon
"""

MINIMAL_BACKLOG = f"## 🔧 Core Playback\n\n{MINIMAL_STORY_BLOCK}"


# ── _strip_emoji ───────────────────────────────────────────────────────────────

class TestStripEmoji:
    def test_strips_leading_emoji(self):
        assert ex._strip_emoji("🎵 Playback") == "Playback"

    def test_strips_multiple_leading_emoji(self):
        assert ex._strip_emoji("🎵🔧 Mixed") == "Mixed"

    def test_no_emoji_unchanged(self):
        assert ex._strip_emoji("Core Playback") == "Core Playback"

    def test_empty_string(self):
        assert ex._strip_emoji("") == ""


# ── _column_letter ─────────────────────────────────────────────────────────────

class TestColumnLetter:
    def test_first_column(self):
        assert ex._column_letter(1) == "A"

    def test_last_single_letter(self):
        assert ex._column_letter(26) == "Z"

    def test_first_double_letter(self):
        assert ex._column_letter(27) == "AA"

    def test_double_letter_sequence(self):
        assert ex._column_letter(28) == "AB"
        assert ex._column_letter(52) == "AZ"
        assert ex._column_letter(53) == "BA"


# ── _parse_story_block ─────────────────────────────────────────────────────────

class TestParseStoryBlock:
    def test_extracts_all_fields(self):
        story = ex._parse_story_block(MINIMAL_STORY_BLOCK, "Core Playback")
        assert story["Story ID"] == "US001"
        assert story["Story Title"] == "Play a Song"
        assert story["Category"] == "Core Playback"
        assert "child" in story["Description"]
        assert "tap a song tile" in story["Description"]
        assert "hear music immediately" in story["Description"]
        assert story["Effort (SP)"] == 5
        assert "High" in story["Complexity"]
        assert "3★" in story["Complexity"]
        assert story["Breakdown"] == "Child: 60%, Backend: 40%"
        assert story["Dependencies"] == "US002"
        assert story["Build Order"] == 1
        assert "Song starts playing within 2 seconds" in story["Acceptance Criteria"]
        assert "Play button shows a pause icon" in story["Acceptance Criteria"]
        assert story["Status"] == "Not Started"

    def test_returns_none_when_no_story_heading(self):
        assert ex._parse_story_block("## Just a section heading\n", "General") is None

    def test_missing_optional_fields_use_safe_defaults(self):
        story = ex._parse_story_block("### Story US099: Bare Minimum\n", "General")
        assert story is not None
        assert story["Effort (SP)"] == ""
        assert story["Complexity"] == ""
        assert story["Breakdown"] == ""
        assert story["Dependencies"] == "None"
        assert story["Build Order"] == 9999
        assert story["Acceptance Criteria"] == ""
        assert story["Description"] == ""

    def test_status_is_always_not_started(self):
        story = ex._parse_story_block(MINIMAL_STORY_BLOCK, "Any")
        assert story["Status"] == "Not Started"

    def test_ac_ignores_checked_boxes(self):
        block = (
            "### Story US010: ACs\n"
            "- [ ] unchecked one\n"
            "- [x] already done\n"
            "- [ ] unchecked two\n"
        )
        story = ex._parse_story_block(block, "Cat")
        ac = story["Acceptance Criteria"]
        assert "unchecked one" in ac
        assert "unchecked two" in ac
        assert "already done" not in ac  # - [x] excluded

    def test_build_order_without_hash_prefix(self):
        block = "### Story US011: No Hash\n**Build Order**: 5\n"
        story = ex._parse_story_block(block, "Cat")
        assert story["Build Order"] == 5

    def test_role_matches_as_a_variant(self):
        block = "### Story US012: Parent role\nAs a parent, I want to manage settings.\n"
        story = ex._parse_story_block(block, "Cat")
        assert "parent" in story["Description"]


# ── parse_backlog ──────────────────────────────────────────────────────────────

class TestParseBacklog:
    def test_parses_single_story(self, tmp_path):
        f = tmp_path / "backlog.md"
        f.write_text(MINIMAL_BACKLOG, encoding="utf-8")
        stories = ex.parse_backlog(f)
        assert len(stories) == 1
        assert stories[0]["Story ID"] == "US001"

    def test_category_has_emoji_stripped(self, tmp_path):
        f = tmp_path / "backlog.md"
        f.write_text(MINIMAL_BACKLOG, encoding="utf-8")
        stories = ex.parse_backlog(f)
        assert stories[0]["Category"] == "Core Playback"

    def test_parses_stories_across_multiple_sections(self, tmp_path):
        content = (
            "## 🎵 Playback\n\n"
            + MINIMAL_STORY_BLOCK
            + "\n## 📚 Library\n\n"
            + MINIMAL_STORY_BLOCK.replace("US001", "US002").replace("Play a Song", "Browse Albums")
        )
        f = tmp_path / "backlog.md"
        f.write_text(content, encoding="utf-8")
        stories = ex.parse_backlog(f)
        assert len(stories) == 2
        assert {s["Category"] for s in stories} == {"Playback", "Library"}

    def test_returns_empty_list_when_no_stories(self, tmp_path):
        f = tmp_path / "backlog.md"
        f.write_text("## Headings only, no stories\n", encoding="utf-8")
        assert ex.parse_backlog(f) == []

    def test_build_order_field_is_populated(self, tmp_path):
        f = tmp_path / "backlog.md"
        f.write_text(MINIMAL_BACKLOG, encoding="utf-8")
        stories = ex.parse_backlog(f)
        assert stories[0]["Build Order"] == 1

    def test_all_columns_present_in_every_story(self, tmp_path):
        f = tmp_path / "backlog.md"
        f.write_text(MINIMAL_BACKLOG, encoding="utf-8")
        story = ex.parse_backlog(f)[0]
        assert set(story.keys()) == set(ex.COLUMNS)
