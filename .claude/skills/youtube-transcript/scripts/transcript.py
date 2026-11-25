#!/usr/bin/env python3
"""Fetch a YouTube video's transcript (the "ears").

Usage:
  python3 transcript.py <url-or-id> [--lang zh-Hant zh-Hans en] [--out FILE] [--plain]

Output: one line per caption, prefixed with a [mm:ss] timestamp (unless --plain).
Needs: pip install youtube-transcript-api
"""
import argparse
import re
import sys

try:
    from youtube_transcript_api import YouTubeTranscriptApi
except ImportError:
    sys.exit("Missing dependency. Run: pip install youtube-transcript-api")

ID_RE = re.compile(r"(?:v=|youtu\.be/|shorts/|embed/|live/)([A-Za-z0-9_-]{11})")


def video_id(url_or_id: str) -> str:
    if re.fullmatch(r"[A-Za-z0-9_-]{11}", url_or_id):
        return url_or_id
    m = ID_RE.search(url_or_id)
    if not m:
        sys.exit(f"Could not find a video id in: {url_or_id}")
    return m.group(1)


def ts(seconds: float) -> str:
    s = int(seconds)
    h, rem = divmod(s, 3600)
    m, s = divmod(rem, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m:02d}:{s:02d}"


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("video")
    p.add_argument("--lang", nargs="+", default=["zh-Hant", "zh-TW", "zh-Hans", "zh", "en"])
    p.add_argument("--out")
    p.add_argument("--plain", action="store_true", help="no timestamps")
    a = p.parse_args()

    vid = video_id(a.video)
    api = YouTubeTranscriptApi()
    try:
        fetched = api.fetch(vid, languages=a.lang)
    except Exception:
        # Fall back to whatever transcript exists, translated if possible.
        tlist = api.list(vid)
        t = next(iter(tlist))
        fetched = t.fetch()

    lines = [s.text.replace("\n", " ") if a.plain else f"[{ts(s.start)}] {s.text.replace(chr(10), ' ')}"
             for s in fetched]
    text = f"# Transcript {vid} ({fetched.language_code})\n" + "\n".join(lines) + "\n"
    if a.out:
        with open(a.out, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"Saved {len(lines)} lines to {a.out}")
    else:
        sys.stdout.write(text)


if __name__ == "__main__":
    main()
