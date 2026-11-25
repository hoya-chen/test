---
name: build-video-agent
description: Turn a list of the best YouTube videos on one topic into an expert subagent. Use when the user says things like "把这些影片做成 agent", "build an agent from these videos", or gives several YouTube links plus a role (e.g. video editor, marketer, outreach).
---

# Build an expert agent from videos (造 agent)

Input from the user: a **role name** (e.g. `editor`) and **5–10 YouTube links**
that teach that role well. One skill per video: the more videos, the more expert.

## Steps

For each video:

1. **Ears** – fetch the transcript with the `youtube-transcript` skill, saved to
   `knowledge/<role>/transcripts/<video-id>.md`.
2. **Eyes** – call the MCP tool `video_timeline` (server `yt-analysis`) on the
   same URL, saved to `knowledge/<role>/visual/<video-id>.md`. If the tool is
   not available or fails, continue with the transcript only and tell the user.
3. **Distil** – write `knowledge/<role>/lessons/<video-id>.md` with:
   - Title, URL, creator
   - 5–10 concrete techniques (each: what, when to use, how, timestamp)
   - Common mistakes the video warns about
   - Checklists or step sequences worth reusing

Then build the agent:

4. Write `knowledge/<role>/playbook.md`: merge all lessons, dedupe, group by
   task, and note where videos disagree.
5. Create `.claude/agents/<role>-expert.md` from
   `.claude/skills/build-video-agent/agent-template.md` (replace every `ROLE`). Fill in the role, the three
   kinds of work it does, and point it at `knowledge/<role>/playbook.md` and the
   `lessons/` folder.
6. Report to the user: which videos were processed, which failed and why, and
   how to call the agent (`@<role>-expert ...` or "use the <role>-expert agent").

Adding a video later: run steps 1–3 for it, then redo step 4.
