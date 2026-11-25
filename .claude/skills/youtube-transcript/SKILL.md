---
name: youtube-transcript
description: Fetch the full transcript (逐字稿) of a YouTube video with timestamps. Use whenever the user gives a YouTube link and wants a summary, notes, quotes, key points, or anything that depends on what is said in the video.
---

# YouTube transcript (耳朵)

Claude Code cannot open a YouTube link by itself. This skill turns the spoken
content into text.

## Steps

1. Make sure the dependency exists (once):
   `pip install youtube-transcript-api`
2. Fetch the transcript:
   ```bash
   python3 .claude/skills/youtube-transcript/scripts/transcript.py "<youtube-url>" \
     --out knowledge/transcripts/<video-id>.md
   ```
   - `--lang zh-Hant en` sets preferred caption languages (first match wins).
   - `--plain` drops the `[mm:ss]` timestamps.
3. Read the saved file and answer the user's question from it. Quote timestamps
   like `[12:34]` so the user can jump to the moment.

## Limits

- Only works when the video has captions (manual or auto-generated).
- It hears words only. For what is shown on screen (slides, UI, editing moves),
  use the `yt-analysis` MCP tools (Gemini) instead.
- If YouTube blocks the request (cloud IPs often are), run it on your own computer.
