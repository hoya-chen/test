# knowledge/

Output of the `build-video-agent` skill. One folder per role:

```
knowledge/<role>/
  transcripts/<video-id>.md   # ears: what is said
  visual/<video-id>.md        # eyes: what is shown (Gemini timeline)
  lessons/<video-id>.md       # distilled techniques per video
  playbook.md                 # merged knowledge the agent reads
```
