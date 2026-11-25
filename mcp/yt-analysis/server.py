#!/usr/bin/env python3
"""YT Analysis MCP server (the "eyes").

Lets Claude Code ask Gemini about a YouTube video: Gemini watches the real
frames and audio and answers with timestamps.

Env:
  GEMINI_API_KEY   free key from https://aistudio.google.com/apikey  (starts with "AIza")
  GEMINI_MODEL     optional, default gemini-2.5-flash
Needs: pip install "mcp"   (works with mcp 1.x and 2.x)
"""
import json
import os
import urllib.error
import urllib.request

try:  # mcp 2.x
    from mcp.server.mcpserver import MCPServer as _Server
except ImportError:  # mcp 1.x
    from mcp.server.fastmcp import FastMCP as _Server

API = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
server = _Server("yt-analysis")


def _gemini(url: str, prompt: str, start: str | None = None, end: str | None = None) -> str:
    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        return "GEMINI_API_KEY is not set. Get a free key at https://aistudio.google.com/apikey"
    video_part: dict = {"file_data": {"file_uri": url}}
    meta = {k: v for k, v in (("start_offset", start), ("end_offset", end)) if v}
    if meta:
        video_part["video_metadata"] = meta
    body = {"contents": [{"parts": [video_part, {"text": prompt}]}]}
    req = urllib.request.Request(
        API.format(model=os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")),
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json", "x-goog-api-key": key},
    )
    try:
        with urllib.request.urlopen(req, timeout=600) as r:
            data = json.load(r)
    except urllib.error.HTTPError as e:
        return f"Gemini error {e.code}: {e.read().decode(errors='replace')[:800]}"
    parts = data.get("candidates", [{}])[0].get("content", {}).get("parts", [])
    return "".join(p.get("text", "") for p in parts) or json.dumps(data)[:800]


@server.tool()
def analyze_video(url: str, question: str, start: str = "", end: str = "") -> str:
    """Ask Gemini a question about a public YouTube video (it sees frames and hears audio).

    url: YouTube link. question: what you want to know.
    start/end: optional clip range like "90s" or "600s" to look at one part only.
    """
    return _gemini(url, question + "\nCite timestamps as [mm:ss].", start or None, end or None)


@server.tool()
def video_timeline(url: str, language: str = "繁體中文") -> str:
    """Build a scene-by-scene timeline: for each segment, what is said AND what is shown on screen."""
    prompt = (
        f"Watch this video and write, in {language}, a timeline table with columns: "
        "時間 [mm:ss] | 說了什麼 (spoken) | 畫面上有什麼 (on screen: UI, text, actions, edits). "
        "One row per meaningful change. End with a list of the key techniques taught."
    )
    return _gemini(url, prompt)


if __name__ == "__main__":
    server.run()
