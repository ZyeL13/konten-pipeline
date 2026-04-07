# Assets Structure

## Character: Auditor
Path: `assets/auditor/`

| File | Usage |
|------|-------|
| focused.png | Serious, concentrated expression |
| fullbody.png | Full body shot for wide scenes |
| halfbody.png | Medium shot, waist up |
| neutral.png | Default expression, no emotion |
| smirk.png | Sarcastic/wry smile |
| talk.png | Mouth open for speech animation |

## Format
- All PNG files, transparent background
- Recommended for overlay on video scenes
- Position: bottom-right or bottom-left corner
- Scale: 15-20% of video height

## Usage in code
`agents/edit_agent.py` → `add_character_overlay_blended()`
