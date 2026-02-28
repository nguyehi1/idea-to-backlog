"""
Unit tests for scripts/utils.py

Run with:  pytest tests/
"""
import os
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock


# ---------------------------------------------------------------------------
# get_gemini_client
# ---------------------------------------------------------------------------

class TestGetGeminiClient:
    def test_raises_when_api_key_missing(self):
        import utils
        with patch.dict(os.environ, {}, clear=True):
            os.environ.pop("GEMINI_API_KEY", None)
            with pytest.raises(ValueError, match="GEMINI_API_KEY"):
                utils.get_gemini_client()

    def test_returns_client_when_key_present(self):
        import utils
        with patch.dict(os.environ, {"GEMINI_API_KEY": "test-key"}):
            with patch("utils.genai.Client") as mock_cls:
                mock_cls.return_value = MagicMock()
                client = utils.get_gemini_client()
                assert client is not None
                mock_cls.assert_called_once_with(api_key="test-key")

    def test_singleton_created_only_once(self):
        import utils
        with patch.dict(os.environ, {"GEMINI_API_KEY": "test-key"}):
            with patch("utils.genai.Client") as mock_cls:
                mock_cls.return_value = MagicMock()
                c1 = utils.get_gemini_client()
                c2 = utils.get_gemini_client()
                assert c1 is c2
                mock_cls.assert_called_once()  # not twice


# ---------------------------------------------------------------------------
# load_prompt_template
# ---------------------------------------------------------------------------

class TestLoadPromptTemplate:
    def test_raises_with_helpful_message_when_missing(self):
        import utils
        with pytest.raises(FileNotFoundError, match="no_such_prompt.txt"):
            utils.load_prompt_template("no_such_prompt.txt")

    def test_loads_real_prompt(self):
        import utils
        # prd_prompt.txt must exist for the project to work at all
        content = utils.load_prompt_template("prd_prompt.txt")
        assert len(content) > 0


# ---------------------------------------------------------------------------
# load_file
# ---------------------------------------------------------------------------

class TestLoadFile:
    def test_raises_when_file_missing(self, tmp_path):
        import utils
        with pytest.raises(FileNotFoundError, match="missing.md not found"):
            utils.load_file(tmp_path, "missing.md")

    def test_error_includes_prerequisite_hint(self, tmp_path):
        import utils
        with pytest.raises(FileNotFoundError, match="generate_prd"):
            utils.load_file(tmp_path, "prd.md", required_file="prd.md")

    def test_loads_existing_file(self, tmp_path):
        import utils
        (tmp_path / "idea.md").write_text("My great idea")
        assert utils.load_file(tmp_path, "idea.md") == "My great idea"

    def test_raises_when_file_is_empty(self, tmp_path):
        """Regression: empty file (e.g. unsaved editor buffer) must fail loudly."""
        import utils
        (tmp_path / "idea.md").write_text("")
        with pytest.raises(ValueError, match="empty"):
            utils.load_file(tmp_path, "idea.md")

    def test_raises_when_file_is_whitespace_only(self, tmp_path):
        import utils
        (tmp_path / "idea.md").write_text("   \n\n\t  ")
        with pytest.raises(ValueError, match="empty"):
            utils.load_file(tmp_path, "idea.md")

    def test_path_stem_used_not_split(self, tmp_path):
        """Regression: required_file with dots like 'user_stories.md' should stem correctly."""
        import utils
        with pytest.raises(FileNotFoundError, match="generate_user_stories"):
            utils.load_file(tmp_path, "user_stories.md", required_file="user_stories.md")


# ---------------------------------------------------------------------------
# save_file
# ---------------------------------------------------------------------------

class TestSaveFile:
    def test_saves_new_file(self, tmp_path):
        import utils
        utils.save_file(tmp_path, "output.md", "# Hello")
        assert (tmp_path / "output.md").read_text() == "# Hello"

    def test_skips_when_overwrite_declined(self, tmp_path):
        import utils
        (tmp_path / "output.md").write_text("original")
        with patch("builtins.input", return_value="n"):
            utils.save_file(tmp_path, "output.md", "new content")
        assert (tmp_path / "output.md").read_text() == "original"

    def test_overwrites_when_confirmed(self, tmp_path):
        import utils
        (tmp_path / "output.md").write_text("original")
        with patch("builtins.input", return_value="y"):
            utils.save_file(tmp_path, "output.md", "new content")
        assert (tmp_path / "output.md").read_text() == "new content"

    def test_skips_on_eof_input(self, tmp_path):
        """Non-interactive environments (CI, pipes) should default to skip."""
        import utils
        (tmp_path / "output.md").write_text("original")
        with patch("builtins.input", side_effect=EOFError):
            utils.save_file(tmp_path, "output.md", "new content")
        assert (tmp_path / "output.md").read_text() == "original"

    def test_force_overwrites_without_prompt(self, tmp_path):
        """force=True must overwrite existing files without asking."""
        import utils
        (tmp_path / "output.md").write_text("original")
        utils.save_file(tmp_path, "output.md", "new content", force=True)
        assert (tmp_path / "output.md").read_text() == "new content"


# ---------------------------------------------------------------------------
# run_generation — overwrite guard
# ---------------------------------------------------------------------------

class TestRunGenerationOverwriteGuard:
    def test_skips_gemini_when_output_exists_and_declined(self, tmp_path):
        """Gemini must NOT be called if the user declines the overwrite prompt."""
        import utils
        (tmp_path / "idea.md").write_text("# My Idea\nSome content")
        (tmp_path / "prd.md").write_text("existing prd")

        with patch("builtins.input", return_value="n"), \
             patch("utils.generate_with_gemini") as mock_gen:
            utils.run_generation(
                project_path=tmp_path,
                input_filename="idea.md",
                output_filename="prd.md",
                prompt_filename="prd_prompt.txt",
                context="product idea and context",
            )
            mock_gen.assert_not_called()

        assert (tmp_path / "prd.md").read_text() == "existing prd"


# ---------------------------------------------------------------------------
# generate_with_gemini
# ---------------------------------------------------------------------------

class TestGenerateWithGemini:
    def _make_chunk(self, text):
        chunk = MagicMock()
        chunk.text = text
        return chunk

    def test_returns_joined_stream_chunks(self):
        import utils
        mock_client = MagicMock()
        mock_client.models.generate_content_stream.return_value = [
            self._make_chunk("Hello "),
            self._make_chunk("world"),
        ]
        utils._client = mock_client

        result = utils.generate_with_gemini("system", "content", "PRD")
        assert result == "Hello world"

    def test_skips_none_chunks(self):
        import utils
        none_chunk = MagicMock()
        none_chunk.text = None
        mock_client = MagicMock()
        mock_client.models.generate_content_stream.return_value = [
            none_chunk,
            self._make_chunk("valid"),
        ]
        utils._client = mock_client

        result = utils.generate_with_gemini("system", "content", "PRD")
        assert result == "valid"

    def test_raises_runtime_error_on_rate_limit(self):
        import utils
        from google.genai import errors as genai_errors

        # Build a minimal response mock that satisfies ClientError(status_code, response_json, response)
        mock_response = MagicMock()
        mock_response.status_code = 429
        rate_limit_err = genai_errors.ClientError(
            429,
            {"error": {"code": 429, "message": "RESOURCE_EXHAUSTED", "status": "RESOURCE_EXHAUSTED"}},
            mock_response,
        )

        mock_client = MagicMock()
        mock_client.models.generate_content_stream.side_effect = rate_limit_err
        utils._client = mock_client

        with pytest.raises(RuntimeError, match="Rate limit"):
            utils.generate_with_gemini("system", "content", "PRD")
