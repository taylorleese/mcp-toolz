"""Tests for clipboard image capture utility."""

import base64
import subprocess
from unittest.mock import MagicMock, patch

import pytest

from context_manager.clipboard import get_clipboard_image_base64

# Minimal valid PNG: 1x1 pixel transparent
SAMPLE_PNG_BYTES = (
    b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01"
    b"\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89"
    b"\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01"
    b"\r\n\xb4\x00\x00\x00\x00IEND\xaeB`\x82"
)
SAMPLE_PNG_HEX = SAMPLE_PNG_BYTES.hex().upper()
SAMPLE_PNG_BASE64 = base64.b64encode(SAMPLE_PNG_BYTES).decode()


@pytest.mark.unit
class TestGetClipboardImageBase64:
    """Test clipboard image capture."""

    @patch("context_manager.clipboard.sys")
    def test_returns_none_on_non_macos(self, mock_sys: MagicMock) -> None:
        """Test returns None on non-macOS platforms."""
        mock_sys.platform = "linux"
        assert get_clipboard_image_base64() is None

    @patch("context_manager.clipboard.subprocess.run")
    def test_successful_capture(self, mock_run: MagicMock) -> None:
        """Test successful image capture from clipboard."""
        mock_run.return_value = subprocess.CompletedProcess(
            args=[],
            returncode=0,
            stdout=f"{{«class PNGf»:«data PNGf{SAMPLE_PNG_HEX}»}}".encode(),
            stderr=b"",
        )

        result = get_clipboard_image_base64()

        assert result == SAMPLE_PNG_BASE64
        mock_run.assert_called_once()

    @patch("context_manager.clipboard.subprocess.run")
    def test_no_image_in_clipboard(self, mock_run: MagicMock) -> None:
        """Test returns None when clipboard has no image."""
        mock_run.return_value = subprocess.CompletedProcess(
            args=[],
            returncode=0,
            stdout=b"some plain text",
            stderr=b"",
        )

        assert get_clipboard_image_base64() is None

    @patch("context_manager.clipboard.subprocess.run")
    def test_timeout_returns_none(self, mock_run: MagicMock) -> None:
        """Test returns None on subprocess timeout."""
        mock_run.side_effect = subprocess.TimeoutExpired(cmd="osascript", timeout=5)

        assert get_clipboard_image_base64() is None

    @patch("context_manager.clipboard.subprocess.run")
    def test_oserror_returns_none(self, mock_run: MagicMock) -> None:
        """Test returns None on OSError."""
        mock_run.side_effect = OSError("Command not found")

        assert get_clipboard_image_base64() is None
