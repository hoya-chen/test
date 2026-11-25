# test

## YouTube → Claude Code → expert agent

```
YouTube link
   │
   ├─ ears  : .claude/skills/youtube-transcript   → transcript (what is said)
   ├─ eyes  : mcp/yt-analysis (Gemini, .mcp.json) → timeline (what is shown)
   │
   └─ build : .claude/skills/build-video-agent    → knowledge/<role>/playbook.md
                                                  → .claude/agents/<role>-expert.md
```

### Setup (on your own computer)

1. `pip install youtube-transcript-api mcp`
2. Get a free Gemini key at https://aistudio.google.com/apikey and export it:
   `export GEMINI_API_KEY=AIza...`
3. Start Claude Code in this folder and approve the `yt-analysis` MCP server.
   `/mcp` should list it with tools `analyze_video` and `video_timeline`.

### Use

- 摘要一支影片: "总结这支影片 https://youtu.be/..."
- 看画面: "用 yt-analysis 看一下 https://youtu.be/... 第 3 分钟屏幕上做了什么"
- 造 agent: "用 build-video-agent，把这 10 支剪辑教学做成 editor agent: <links>"
  then: "use the editor-expert agent to write a cold email to a YouTuber"
