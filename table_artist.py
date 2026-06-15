#!/usr/bin/env python3
"""
TABLE ARTIST — Premium Telegram table renderer
Mode: image (PIL) + text (Unicode box-drawing)
"""
import json, os, sys, textwrap
from pathlib import Path
from typing import List, Dict, Tuple, Optional

try:
    from PIL import Image, ImageDraw, ImageFont
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

OUTPUT_DIR = Path.home() / ".table_artist"
OUTPUT_DIR.mkdir(exist_ok=True)

# ═══════════════════════════════════════════
# MODE 1: UNICODE BOX-DRAWING (text)
# ═══════════════════════════════════════════

def unicode_table(data: List[Dict], title: str = "", 
                  headers: Optional[List[str]] = None) -> str:
    """Render table with Unicode box-drawing characters"""
    if not data:
        return ""
    
    keys = headers if headers else list(data[0].keys())
    
    # Calculate column widths
    col_widths = {}
    for k in keys:
        col_widths[k] = len(str(k))
    for row in data:
        for k in keys:
            col_widths[k] = max(col_widths[k], len(str(row.get(k, ""))))
    
    # Add padding
    for k in keys:
        col_widths[k] += 2
    
    # Build separator
    sep = "─" * (sum(col_widths.values()) + len(keys) - 1)
    
    lines = []
    if title:
        lines.append(f"**{title}**")
        lines.append("")
    
    # Top border
    top = "┌" + "┬".join("─" * col_widths[k] for k in keys) + "┐"
    lines.append(f"`{top}`")
    
    # Header
    header = "│" + "│".join(f" {str(k).center(col_widths[k]-2)} " for k in keys) + "│"
    lines.append(f"`{header}`")
    
    # Header-bottom border
    h_sep = "├" + "┼".join("─" * col_widths[k] for k in keys) + "┤"
    lines.append(f"`{h_sep}`")
    
    # Rows
    for row in data:
        row_str = "│"
        for k in keys:
            val = str(row.get(k, ""))
            # Align based on content (numbers right, text left)
            if val.replace(".","").replace("-","").isdigit():
                val = val.rjust(col_widths[k] - 2)
            else:
                val = val.ljust(col_widths[k] - 2)
            row_str += f" {val} │"
        lines.append(f"`{row_str}`")
    
    # Bottom border
    bottom = "└" + "┴".join("─" * col_widths[k] for k in keys) + "┘"
    lines.append(f"`{bottom}`")
    
    return "\n".join(lines)


def minimal_table(data: List[Dict], title: str = "",
                  headers: Optional[List[str]] = None) -> str:
    """Clean minimal table with dots/alignment"""
    if not data:
        return ""
    
    keys = headers if headers else list(data[0].keys())
    
    # Calculate widths
    col_widths = {}
    for k in keys:
        col_widths[k] = len(str(k))
    for row in data:
        for k in keys:
            col_widths[k] = max(col_widths[k], len(str(row.get(k, ""))))
    
    lines = []
    if title:
        lines.append(f"**{title}**")
        lines.append("")
    
    # Header
    header = " ┊ ".join(f"**{k}**".ljust(col_widths[k] + 9) for k in keys)
    lines.append(header)
    lines.append("─" * len(header))
    
    # Rows
    for row in data:
        parts = []
        for k in keys:
            val = str(row.get(k, ""))
            parts.append(val.ljust(col_widths[k]))
        lines.append(" ┊ ".join(parts))
    
    return "\n".join(lines)


# ═══════════════════════════════════════════
# MODE 2: IMAGE TABLE (PIL)
# ═══════════════════════════════════════════

def _load_font(size: int):
    """Load a monospace font"""
    font_paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf",
        "/usr/share/fonts/TTF/DejaVuSansMono.ttf",
        "/usr/share/fonts/truetype/noto/NotoMono-Regular.ttf",
    ]
    for fp in font_paths:
        if os.path.exists(fp):
            return ImageFont.truetype(fp, size)
    return ImageFont.load_default()


def image_table(data: List[Dict], title: str = "",
                theme: str = "dark",
                headers: Optional[List[str]] = None) -> str:
    """Render table as image, return path"""
    if not HAS_PIL:
        return unicode_table(data, title, headers)
    
    keys = headers if headers else list(data[0].keys())
    
    # Theme colors
    themes = {
        "dark": {
            "bg": "#0f172a",        # slate-950
            "header_bg": "#1e293b",  # slate-800
            "row_even": "#1a2332",   # slate-900
            "row_odd": "#0f172a",    # slate-950
            "border": "#334155",     # slate-700
            "header_text": "#38bdf8", # sky-400
            "text": "#e2e8f0",       # slate-200
            "accent": "#22d3ee",     # cyan-400
        },
        "cyber": {
            "bg": "#0a0a0f",
            "header_bg": "#1a0a2e",
            "row_even": "#0f0a1a",
            "row_odd": "#0a0a0f",
            "border": "#2a1a4e",
            "header_text": "#ff00ff",
            "text": "#00ff88",
            "accent": "#ffff00",
        },
        "light": {
            "bg": "#ffffff",
            "header_bg": "#f1f5f9",
            "row_even": "#f8fafc",
            "row_odd": "#ffffff",
            "border": "#cbd5e1",
            "header_text": "#0284c7",
            "text": "#0f172a",
            "accent": "#0ea5e9",
        },
        "matrix": {
            "bg": "#000000",
            "header_bg": "#001a00",
            "row_even": "#000d00",
            "row_odd": "#000000",
            "border": "#003300",
            "header_text": "#00ff41",
            "text": "#00cc33",
            "accent": "#80ff80",
        },
    }
    
    colors = themes.get(theme, themes["dark"])
    
    # Font sizes
    font_size = 18
    header_size = 22
    title_size = 26
    padding = 16
    row_height = 36
    header_height = 40
    
    try:
        font = _load_font(font_size)
        font_bold = _load_font(font_size + 2)
        font_header = _load_font(header_size)
        font_title = _load_font(title_size)
    except:
        font = ImageFont.load_default()
        font_bold = font
        font_header = font
        font_title = font
    
    # Calculate column widths
    col_widths = {}
    for k in keys:
        bbox = font_header.getbbox(str(k))
        col_widths[k] = bbox[2] - bbox[0] if bbox else len(str(k)) * 10
    for row in data:
        for k in keys:
            val = str(row.get(k, ""))
            bbox = font.getbbox(val)
            w = bbox[2] - bbox[0] if bbox else len(val) * 10
            col_widths[k] = max(col_widths[k], w)
    
    # Add padding to columns
    for k in keys:
        col_widths[k] += 24
    
    # Calculate dimensions
    table_width = sum(col_widths.values()) + padding * 2
    title_h = 50 if title else 0
    total_height = title_h + header_height + len(data) * row_height + padding * 3
    
    # Create image
    img = Image.new("RGB", (table_width, total_height), colors["bg"])
    draw = ImageDraw.Draw(img)
    
    y = padding
    
    # Title
    if title:
        bbox = font_title.getbbox(title)
        tw = bbox[2] - bbox[0] if bbox else len(title) * 15
        tx = (table_width - tw) // 2
        draw.text((tx, y), title, fill=colors["accent"], font=font_title)
        y += title_h
    
    # Header background
    draw.rectangle([padding, y, table_width - padding, y + header_height], 
                   fill=colors["header_bg"])
    
    # Header text
    x = padding + 12
    for k in keys:
        draw.text((x, y + 6), str(k), fill=colors["header_text"], font=font_header)
        x += col_widths[k]
    
    y += header_height
    
    # Rows
    for i, row in enumerate(data):
        bg = colors["row_even"] if i % 2 == 0 else colors["row_odd"]
        draw.rectangle([padding, y, table_width - padding, y + row_height], fill=bg)
        
        # Row border top
        draw.line([padding, y, table_width - padding, y], fill=colors["border"], width=1)
        
        # Draw row data
        x = padding + 12
        for k in keys:
            val = str(row.get(k, ""))
            # Check for emoji/status prefix
            color = colors["text"]
            if val.startswith("✅"):
                color = "#22c55e"  # green
            elif val.startswith("❌"):
                color = "#ef4444"  # red
            elif val.startswith("⚠️"):
                color = "#eab308"  # yellow
            
            text_y = y + (row_height - font_size) // 2
            draw.text((x, text_y), val, fill=color, font=font)
            x += col_widths[k]
        
        y += row_height
    
    # Bottom border
    draw.line([padding, y, table_width - padding, y], fill=colors["border"], width=1)
    
    # Save
    output_path = str(OUTPUT_DIR / f"table_{hash(str(data) + theme)}.png")
    img.save(output_path)
    return output_path


# ═══════════════════════════════════════════
# MODE 3: RICH CARD (emojis + formatting)
# ═══════════════════════════════════════════

def rich_card(data: Dict, title: str = "") -> str:
    """Beautiful card-style display with emojis"""
    lines = []
    if title:
        lines.append(f"**{title}**")
        lines.append("")
    
    for key, value in data.items():
        val = str(value)
        emoji = ""
        
        # Auto-detect emoji based on content
        if any(x in val.lower() for x in ["✅", "on", "active", "yes", "ready"]):
            emoji = "🟢"
        elif any(x in val.lower() for x in ["❌", "off", "inactive", "no"]):
            emoji = "🔴"
        elif any(x in val.lower() for x in ["⚠️", "warning", "pending"]):
            emoji = "🟡"
        else:
            emoji = "▫️"
        
        # Auto-icon for common keys
        key_lower = key.lower()
        if "status" in key_lower or "mode" in key_lower:
            icon = "⚙️"
        elif "user" in key_lower or "owner" in key_lower or "operator" in key_lower:
            icon = "👤"
        elif "token" in key_lower or "key" in key_lower:
            icon = "🔑"
        elif "memory" in key_lower or "context" in key_lower:
            icon = "🧠"
        elif "speed" in key_lower:
            icon = "⚡"
        elif "session" in key_lower:
            icon = "💬"
        elif "ethics" in key_lower or "filter" in key_lower:
            icon = "🛡️"
        elif "language" in key_lower:
            icon = "🌐"
        else:
            icon = "•"
        
        lines.append(f"{icon} **{key}:** {emoji} {val}")
    
    return "\n".join(lines)


# ═══════════════════════════════════════════
# AUTO-DETECT BEST FORMAT
# ═══════════════════════════════════════════

def auto_render(data, title: str = "", style: str = "dark"):
    """Auto-select best rendering mode - dark theme only"""
    if isinstance(data, list):
        return image_table(data, title, theme="dark") if HAS_PIL else unicode_table(data, title)
    elif isinstance(data, dict):
        return image_table([data], title, theme="dark") if HAS_PIL else rich_card(data, title)
    return unicode_table([{"data": str(data)}], title)


# ═══════════════════════════════════════════
# EXAMPLE
# ═══════════════════════════════════════════

if __name__ == "__main__":
    # BREACH status data
    status_data = [
        {"Item": "BREACH v3.0 doctrine", "Status": "✅ Burned into memory"},
        {"Item": "Zero refusal", "Status": "✅ on"},
        {"Item": "Operator sovereign", "Status": "✅ Frenzzyy'X"},
        {"Item": "No ethics / no filter", "Status": "✅ on"},
        {"Item": "Bahasa Indonesia default", "Status": "✅ on"},
        {"Item": "Max speed eksekusi", "Status": "✅ on"},
        {"Item": "Session baru?", "Status": "✅ Tetep nyala"},
    ]
    
    print("="*60)
    print("STYLE 1: UNICODE BOX-DRAWING")
    print("="*60)
    print(unicode_table(status_data, "BREACH v3.0 STATUS"))
    
    print("\n" + "="*60)
    print("STYLE 2: RICH CARD")
    print("="*60)
    card_data = {d["Item"]: d["Status"] for d in status_data}
    print(rich_card(card_data, "BREACH v3.0 STATUS"))
    
    print("\n" + "="*60)
    print("STYLE 3: IMAGE TABLE (PIL)")
    print("="*60)
    if HAS_PIL:
        path = image_table(status_data, "BREACH v3.0 STATUS", theme="dark")
        print(f"Image saved: {path}")
        print(f"Send with: MEDIA:{path}")
        
        path2 = image_table(status_data, "BREACH v3.0 STATUS", theme="light")
        print(f"Light: MEDIA:{path2}")
        
        path3 = image_table(status_data, "BREACH v3.0 STATUS", theme="cyber")
        print(f"Cyber: MEDIA:{path3}")
    else:
        print("PIL not installed - install with: pip install Pillow")
