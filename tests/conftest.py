"""
Pytest configuration and shared fixtures.
"""
import sys
import pytest
from pathlib import Path

# Ensure scripts/ is on the path for all tests
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))


@pytest.fixture(autouse=True)
def reset_gemini_singleton():
    """Reset the module-level Gemini client singleton before every test."""
    import utils
    utils._client = None
    yield
    utils._client = None
