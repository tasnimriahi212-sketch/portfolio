# 🚀 Instagram Pro Kit — START HERE

Everything you need to make your page look like a professional studio, in one folder. Built for a **software engineer + cybersecurity + Python** duo.

## What's in the kit

| Path | What it is |
|---|---|
| `assets/highlights/` (8 files) | Story-highlight covers, matching set — upload in the order below |
| `assets/posts/` (9 files) | Ready-to-post feed graphics (1080×1350) |
| `assets/logo.png` + `logo-transparent.png` | Brand mark (profile pic, watermarks, docs) |
| `assets/grid-preview.png` | Preview of how your 9 posts look as a 3×3 grid |
| `assets/covers-sheet.png` | All 8 highlight covers on one sheet |
| `01-brand-and-bio.md` | Bio options, name field, highlight order, pinned posts |
| `02-content-strategy.md` | Content pillars + full 30-day posting calendar |
| `03-captions-and-hashtags.md` | Copy-paste captions + hashtag sets |
| `link-in-bio/index.html` | Your own link-in-bio page (replace Linktree, $0/month) |
| `generate_assets.py` | The generator — change text/colors, rerun, get fresh graphics |

## Do this week (≈1 hour)

1. **Profile pic** → `logo.png`
2. **Name field** → `YourName | Software Dev & Cybersecurity` (it's searchable!)
3. **Bio** → copy Option A from `01-brand-and-bio.md`
4. **Highlights** → create in this order: Services → Work → Security → About → Reviews → Python → Tips → Contact (covers in `assets/highlights/`)
5. **Pin 3 posts** → `01-intro`, `02-services`, `06-testimonial` (replace placeholder quote with a real one ASAP)
6. **Link in bio** → host `link-in-bio/index.html` free on [GitHub Pages](https://pages.github.com) or [Netlify Drop](https://app.netlify.com/drop) (drag & drop the folder), then edit the 6 link placeholders inside the file
7. **Start Day 1** of the calendar in `02-content-strategy.md`

## Make it yours (2 minutes)

Everything currently uses the placeholder `@your.handle`. Open `generate_assets.py`, set:

```python
HANDLE = "@your.real.handle"
```

then run `py -3 generate_assets.py` — all 20 graphics regenerate with your handle baked in. Want different colors or wording? The palette and every headline live at the top of the same file in plain text.

## The 3 rules that keep you looking pro

1. **Same dark background + one accent color** on every post (the templates already do this)
2. **Reels 2×/week** — that's how new clients find you; feed posts are for people who already follow you
3. **Every caption ends with a question or "DM PROJECT"** — followers don't hire you, DMs do
