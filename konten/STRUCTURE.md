# Project Structure

## Core Pipeline
main.py → core/orchestrator.py → workers/*

## Agents (logic per task)
- script_agent.py   → Generate script from headline
- visual_agent.py   → Generate visual prompts
- voice_agent.py    → Text-to-speech
- edit_agent.py     → Video editing + character overlay
- qc_agent.py       → Quality check

## Workers (executors)
- worker_script.py  → Calls script_agent, validates word count
- worker_visual.py  → Generates images from prompts
- worker_voice.py   → Generates audio
- worker_edit.py    → Renders final video
- worker_qc.py      → Validates output

## Assets
- assets/auditor/   → Character PNGs (focused, fullbody, halfbody, neutral, smirk, talk)

## Config
core/config.py → API keys, URLs, temperature settings

## Known Issues
- Groq API returns short scripts (23-54 words)
- Solution: Prioritize ClawRouter fallback
- Character overlay function: `add_character_overlay_blended()` in edit_agent.py
