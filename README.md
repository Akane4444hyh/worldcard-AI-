# world-card

單一 HTML 檔案的單字卡應用，由 Python 腳本生成。UI 使用繁體中文，字型採用 Maple Mono。

## Features

- **Single HTML file** — no server, no dependencies. Open `world-card.html` in any browser.
- **Maple Mono font** — clean monospace typeface loaded via CDN, with Noto Sans SC fallback.
- **Dark / Light mode** — purple dark theme + pink-white light theme, persisted.
- **Group-based word management** — vertical group tabs, per-group counts and navigation.
- **Import** — supports `.json` (CET-6 format) and `.txt` files, or paste directly.
- **Slay & Restore** — mark words as known ("slay"), batch restore with drag-to-select.
- **Shuffle / Reset order** — alphabetical sort is the default; shuffle and restore anytime.
- **All data in localStorage** — no account, no server. Everything stays in your browser.

## Quick start

Open `world-card.html` in your browser — double-click the file, or from the command line:

```bash
# macOS
open world-card.html

# Windows
start world-card.html

# Linux
xdg-open world-card.html
```

To regenerate from the Python template (after editing `world-card.py`):

```bash
# macOS / Linux
python3 world-card.py

# Windows
python world-card.py
```

## Import formats

**TXT** — one word per line, separator can be ` — `, ` | `, tab, or space:
```
abandon — v. 放棄；遺棄
abuse — v. 濫用, n. 虐待
```

**JSON** — CET-6 format with `translations` and `phrases` arrays:
```json
[
  {
    "word": "abandon",
    "translations": [{"type": "v.", "translation": "放棄"}],
    "phrases": [{"phrase": "abandon oneself to", "translation": "沉溺於"}]
  }
]
```

## Keyboard shortcuts

| Key | Action |
|-----|--------|
| `←` `→` | Previous / Next card |
| `Space` / Click card | Flip |
| `K` | Slay (remove from study pool) |
| `R` | Reset to alphabetical order |
| `Escape` | Unflip card |

## Project structure

```
world-card.py   — Python template that generates world-card.html
world-card.html          — The app (can be used directly or regenerated from .py)
```
