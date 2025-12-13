"""
Compatibility shim for Python 3.13 where imghdr was removed.
Implements a minimal subset of the stdlib imghdr module used by
python-telegram-bot 13.x to detect image types.
"""

import os
import struct


def what(file, h=None):
    """Guess the type of a file or bytes object."""
    if h is None:
        try:
            with open(file, "rb") as f:
                h = f.read(32)
        except OSError:
            return None
    for name, checker in tests:
        res = checker(h)
        if res:
            return res
    return None


def test_jpeg(h):
    if h[:3] == b"\xFF\xD8\xFF":
        return "jpeg"


def test_png(h):
    if h[:8] == b"\x89PNG\r\n\x1a\n":
        return "png"


def test_gif(h):
    if h[:6] in (b"GIF87a", b"GIF89a"):
        return "gif"


def test_tiff(h):
    if h[:4] in (b"MM\x00*", b"II*\x00"):
        return "tiff"


def test_bmp(h):
    if h[:2] == b"BM":
        return "bmp"


def test_webp(h):
    if h[:4] == b"RIFF" and h[8:12] == b"WEBP":
        return "webp"


tests = [
    ("jpeg", test_jpeg),
    ("png", test_png),
    ("gif", test_gif),
    ("tiff", test_tiff),
    ("bmp", test_bmp),
    ("webp", test_webp),
]

