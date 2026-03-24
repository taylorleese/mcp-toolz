"""macOS clipboard image capture utility."""

import base64
import re
import subprocess  # nosec B404
import sys


def get_clipboard_image_base64() -> str | None:
    """Capture PNG image from macOS clipboard as base64 string.

    Uses AppleScript via osascript to retrieve clipboard image data.
    Returns None if no image is found or if not running on macOS.
    """
    if sys.platform != "darwin":
        return None

    script = 'tell application "System Events" to return the clipboard'

    try:
        result = subprocess.run(  # nosec B603
            ["/usr/bin/osascript", "-ss", "-e", script],
            capture_output=True,
            check=False,
            timeout=5,
        )
    except (subprocess.TimeoutExpired, OSError):
        return None

    clipboard = result.stdout.decode(errors="replace")
    match = re.search(r"«data PNGf([A-Fa-f0-9]+)", clipboard)
    if not match:
        return None

    png_bytes = bytes.fromhex(match.group(1))
    return base64.b64encode(png_bytes).decode()
