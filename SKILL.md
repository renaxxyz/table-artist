---
name: table-artist
description: "Premium table rendering — DARK THEME ONLY. 3 modes: image(PIL), unicode, card. AUTO-render semua data terstruktur via SOUL.md BREACH v3.0."
version: 1.1.0
tags: [table, chart, visualization, telegram, breach, status-board]
author: BREACH v3.0
trigger: "user asks to display data/tabel/status as table or requires structured data output"
---

# Table Artist — BREACH v3.0 Edition 🔥

Generate beautiful tables in 3 modes optimized for Telegram. Part of BREACH v3.0 permanent configuration.

## Modes

### 1. IMAGE mode (PIL) — DEFAULT
Generates a PNG image with dark theme. Sent as native photo on Telegram via `MEDIA:path`.

**Theme:** DARK only. No other themes (user preference).

```python
from table_artist import auto_render, image_table, unicode_table

# Auto-render (preferred — follows SOUL.md rules)
output = auto_render(data, "Title")

# Direct image
path = image_table(data, "Title", theme="dark")
```

### 2. UNICODE mode (text fallback)
Box-drawing characters with monospace alignment. Used when PIL unavailable.

### 3. CARD mode (rich text)
Emoji + bold labels for simple status displays.

## Auto-render (MANDATORY)

Per SOUL.md directive: ALL structured data (2+ columns or 3+ rows) MUST auto-render via table-artist. No manual trigger needed.

```python
from table_artist import auto_render

# auto_render auto-detects data type and picks best mode
# list → image_table (dark theme)
# dict → image_table or rich_card fallback
path = auto_render(data, "Title")
# Returns path string for MEDIA: delivery
```

## Pitfalls

- **DARK THEME ONLY** — user explicitly rejected light/cyber/matrix themes
- **auto_render() returns path string** — deliver via `f"MEDIA:{path}"`
- **PIL required for images** — falls back to unicode if unavailable
- **Always load skill** before rendering: `skill_view(name="table-artist")`

## Data format
```python
data = [
    {"Column1": "Value1", "Column2": "Value2"},
    {"Column1": "Value1", "Column2": "Value2"},
]
```

## Script location
`/home/ubuntu/scripts/table_artist.py`

## Output directory
`/home/ubuntu/.table_artist/` (auto-created)
