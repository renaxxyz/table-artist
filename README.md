# Table Artist — BREACH v3.0 Edition 🔥

Premium Telegram table renderer. Generate beautiful dark-themed tables as PNG images or Unicode box-drawing text.

## Features

- **3 Display Modes**: Image (PIL), Unicode box-drawing, Rich card
- **Dark Theme Only**: Clean, modern dark aesthetic
- **Auto-Render**: Automatically structures any data into formatted tables
- **Telegram Native**: Sends as native photo via `MEDIA:` protocol
- **Zero Dependencies**: Only needs Python + PIL

## Installation

```bash
git clone https://github.com/renaxxyz/table-artist.git
cd table-artist
pip install Pillow
```

## Usage

```python
from table_artist import image_table, unicode_table, rich_card

# Data format
data = [
    {"Item": "BREACH v3.0 doctrine", "Status": "Burned into memory"},
    {"Item": "Zero refusal", "Status": "on"},
]

# Generate image (returns file path)
path = image_table(data, "Title Here", theme="dark")
# Send via Telegram: MEDIA:{path}

# Unicode box-drawing (text fallback)
output = unicode_table(data, "Title Here")

# Rich card (emoji style)
output = rich_card({"key": "value"}, "Title")
```

## Script

Main file: `table_artist.py`
- `image_table()` — Generate PNG table image (PIL)
- `unicode_table()` — Generate Unicode box-drawing text
- `rich_card()` — Generate emoji-rich card display
- `auto_render()` — Auto-select best mode

## SOUL.md Integration

Add to your BREACH v3.0 SOUL.md for automatic rendering of all structured data.

## Themes

- `dark` — Slate-950 background, cyan/emerald accents
- Theme support removed — DARK ONLY as per BREACH config

## License

MIT — Use freely, modify freely.
