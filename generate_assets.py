# -*- coding: utf-8 -*-
"""
Instagram Pro Kit — asset generator
Dark premium tech identity for a software-engineering + cybersecurity duo.

Edit HANDLE below, rerun:  python generate_assets.py
"""
import os
import math
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HANDLE = "@your.handle"          # <-- put your real Instagram handle here

ROOT = os.path.dirname(os.path.abspath(__file__))
DIR_HL = os.path.join(ROOT, "assets", "highlights")
DIR_POST = os.path.join(ROOT, "assets", "posts")
for d in (DIR_HL, DIR_POST):
    os.makedirs(d, exist_ok=True)

# ---------------------------------------------------------------- palette
# no blue / no purple anywhere — terminal green + warm accents only
BG     = (6, 10, 8)        # near-black with a green tint
CARD   = (12, 18, 14)
GREEN  = (74, 222, 128)    # primary accent — terminal green
ORANGE = (251, 146, 60)
RED    = (248, 113, 113)   # security / red-team accent
AMBER  = (255, 189, 46)
WHITE  = (248, 250, 252)
MUTED  = (150, 160, 150)
# legacy names kept so call sites stay valid after the recolor
CYAN   = GREEN             # primary accent (was blue — removed)
VIOLET = ORANGE            # warm accent (was purple — removed)

FONT_DIR = "C:/Windows/Fonts"

def font(kind, size):
    cands = {
        "bold": ["segoeuib.ttf", "arialbd.ttf"],
        "semib": ["segoeuisb.ttf", "segoeuib.ttf", "arialbd.ttf"],
        "reg":  ["segoeui.ttf", "arial.ttf"],
        "italic": ["segoeuili.ttf", "segoeui.ttf", "arial.ttf"],
        "mono": ["consolab.ttf", "consola.ttf", "courbd.ttf", "cour.ttf"],
        "monor": ["consola.ttf", "cour.ttf"],
    }[kind]
    for c in cands:
        p = os.path.join(FONT_DIR, c)
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()

# ---------------------------------------------------------------- canvas
def canvas(w, h, spots):
    """Dark bg + soft color glows + faint engineering grid."""
    img = Image.new("RGB", (w, h), BG)
    if spots:
        ov = Image.new("RGB", (w, h), BG)
        d = ImageDraw.Draw(ov)
        for (cx, cy, r, col) in spots:
            d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)
        ov = ov.filter(ImageFilter.GaussianBlur(170))
        img = Image.blend(img, ov, 0.6)
    grid = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    gd = ImageDraw.Draw(grid)
    for x in range(0, w, 120):
        gd.line([(x, 0), (x, h)], fill=(255, 255, 255, 7), width=1)
    for y in range(0, h, 120):
        gd.line([(0, y), (w, y)], fill=(255, 255, 255, 7), width=1)
    return Image.alpha_composite(img.convert("RGBA"), grid)

def alpha_layer(img):
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    return lay, ImageDraw.Draw(lay)

# ---------------------------------------------------------------- text utils
def text_ls(d, xy, s, f, fill, ls=10):
    """Letter-spaced text, horizontally centered on xy[0], middle-anchored on xy[1]."""
    widths = [d.textlength(ch, font=f) for ch in s]
    total = sum(widths) + ls * (len(s) - 1)
    x, y = xy[0] - total / 2, xy[1]
    for ch, wd in zip(s, widths):
        d.text((x, y), ch, font=f, fill=fill, anchor="lm")
        x += wd + ls
    return total

def wrap(d, s, f, maxw):
    out, cur = [], ""
    for word in s.split():
        t = (cur + " " + word).strip()
        if d.textlength(t, font=f) <= maxw or not cur:
            cur = t
        else:
            out.append(cur)
            cur = word
    if cur:
        out.append(cur)
    return out

# ---------------------------------------------------------------- icons (line style)
def _closed(d, pts, col, wd):
    d.line(pts + [pts[0]], fill=col, width=wd, joint="curve")

def _poly_inset(pts, delta):
    """Inset a convex polygon by delta: intersect consecutive inward-offset edges."""
    n = len(pts)
    cx_ = sum(p[0] for p in pts) / n
    cy_ = sum(p[1] for p in pts) / n
    lines = []
    for i in range(n):
        p, q = pts[i], pts[(i + 1) % n]
        ex, ey = q[0] - p[0], q[1] - p[1]
        L = math.hypot(ex, ey)
        ex, ey = ex / L, ey / L
        nx, ny = ey, -ex
        mx, my = (p[0] + q[0]) / 2, (p[1] + q[1]) / 2
        if math.hypot(mx + nx - cx_, my + ny - cy_) > math.hypot(mx - cx_, my - cy_):
            nx, ny = -nx, -ny  # keep the inward normal
        lines.append((nx, ny, nx * (p[0] + nx * delta) + ny * (p[1] + ny * delta)))
    out = []
    for i in range(n):
        a1, b1, c1 = lines[i - 1]
        a2, b2, c2 = lines[i]
        det = a1 * b2 - a2 * b1
        if abs(det) < 1e-9:
            out.append(pts[i])
        else:
            out.append(((c1 * b2 - c2 * b1) / det, (a1 * c2 - a2 * c1) / det))
    return out

def icon_shield(img, d, cx, cy, s, col, wd, inner_check=False):
    """Shield outline drawn as fill + inset erase (crisp mitered corners,
    unlike line(joint='curve') which spikes on the sharp shield angles)."""
    col = tuple(col) + (255,) if len(col) == 3 else tuple(col)
    pts = [
        (cx - 0.95 * s, cy - 0.55 * s), (cx - 0.40 * s, cy - 0.92 * s),
        (cx + 0.40 * s, cy - 0.92 * s), (cx + 0.95 * s, cy - 0.55 * s),
        (cx + 0.72 * s, cy + 0.28 * s), (cx, cy + 0.95 * s),
        (cx - 0.72 * s, cy + 0.28 * s),
    ]
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    ld.polygon(pts, fill=col)
    ld.polygon(_poly_inset(pts, wd / 2), fill=(0, 0, 0, 0))
    img.alpha_composite(layer)
    if inner_check:
        d.line([(cx - 0.38 * s, cy + 0.02 * s), (cx - 0.10 * s, cy + 0.32 * s),
                (cx + 0.42 * s, cy - 0.30 * s)], fill=col, width=wd, joint="curve")

def icon_code(d, cx, cy, s, col, wd, txt="</>"):
    f = font("mono", int(1.15 * s))
    d.text((cx, cy), txt, font=f, fill=col, anchor="mm")

def icon_grid(d, cx, cy, s, col, wd):
    g = 0.40 * s
    for dx in (-g, g):
        for dy in (-g, g):
            d.rounded_rectangle([cx + dx - 0.36 * s, cy + dy - 0.36 * s,
                                 cx + dx + 0.36 * s, cy + dy + 0.36 * s],
                                radius=int(0.12 * s), outline=col, width=wd)

def icon_star(d, cx, cy, s, col, wd):
    pts = []
    for i in range(10):
        r = s if i % 2 == 0 else 0.45 * s
        a = -math.pi / 2 + i * math.pi / 5
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    _closed(d, pts, col, wd)

def icon_duo(d, cx, cy, s, col, wd):
    """Two people: each = head circle + shoulders arc, side by side."""
    for dx in (-0.42 * s, 0.42 * s):
        d.ellipse([cx + dx - 0.24 * s, cy - 0.80 * s,
                   cx + dx + 0.24 * s, cy - 0.32 * s], outline=col, width=wd)
        d.arc([cx + dx - 0.44 * s, cy - 0.02 * s,
               cx + dx + 0.44 * s, cy + 0.86 * s], start=180, end=360,
              fill=col, width=wd)

def icon_bulb(d, cx, cy, s, col, wd):
    d.ellipse([cx - 0.55 * s, cy - 0.80 * s, cx + 0.55 * s, cy + 0.30 * s],
              outline=col, width=wd)
    d.line([(cx - 0.22 * s, cy + 0.42 * s), (cx + 0.22 * s, cy + 0.42 * s)], fill=col, width=wd)
    d.line([(cx - 0.22 * s, cy + 0.68 * s), (cx + 0.22 * s, cy + 0.68 * s)], fill=col, width=wd)

def icon_mail(d, cx, cy, s, col, wd):
    d.rounded_rectangle([cx - 0.90 * s, cy - 0.60 * s, cx + 0.90 * s, cy + 0.60 * s],
                        radius=int(0.16 * s), outline=col, width=wd)
    d.line([(cx - 0.90 * s, cy - 0.60 * s), (cx, cy + 0.10 * s), (cx + 0.90 * s, cy - 0.60 * s)],
           fill=col, width=wd, joint="curve")

def icon_chat(d, cx, cy, s, col, wd):
    d.rounded_rectangle([cx - 0.9 * s, cy - 0.7 * s, cx + 0.9 * s, cy + 0.35 * s],
                        radius=int(0.28 * s), outline=col, width=wd)
    d.polygon([(cx - 0.30 * s, cy + 0.35 * s), (cx - 0.02 * s, cy + 0.35 * s),
               (cx - 0.42 * s, cy + 0.8 * s)], fill=col)
    d.line([(cx - 0.5 * s, cy - 0.15 * s), (cx + 0.5 * s, cy - 0.15 * s)], fill=col, width=wd)
    d.line([(cx - 0.5 * s, cy + 0.12 * s), (cx + 0.15 * s, cy + 0.12 * s)], fill=col, width=wd)

def icon_check(d, cx, cy, s, col, wd):
    d.line([(cx - s, cy + 0.1 * s), (cx - 0.25 * s, cy + 0.75 * s), (cx + s, cy - 0.8 * s)],
           fill=col, width=wd, joint="curve")

def icon_arrow(d, cx, cy, s, col, wd):
    d.line([(cx - s, cy), (cx + 0.45 * s, cy)], fill=col, width=wd)
    d.polygon([(cx + 0.45 * s, cy - 0.42 * s), (cx + 0.45 * s, cy + 0.42 * s),
               (cx + s, cy)], fill=col)

# ---------------------------------------------------------------- shared components
def mini_logo(img, d, cx, cy, r, accent):
    icon_shield(img, d, cx, cy, r, accent, max(3, int(r * 0.16)))
    f = font("mono", int(r * 0.78))
    d.text((cx, cy + r * 0.06), "</>", font=f, fill=WHITE, anchor="mm")

def pill_cta(d, cy, text, accent=CYAN):
    f = font("bold", 40)
    tw = d.textlength(text, font=f)
    w = tw + 130
    x0, x1 = 540 - w / 2, 540 + w / 2
    d.rounded_rectangle([x0, cy - 46, x1, cy + 46], radius=46, fill=accent)
    d.text((540, cy), text, font=f, fill=BG, anchor="mm")

def terminal_block(d, x0, y0, x1, lines, mono_size=34):
    """lines: list of (prompt, text, color)"""
    lh = int(mono_size * 1.8)
    h = 96 + lh * len(lines) + 26
    d.rounded_rectangle([x0, y0, x1, y0 + h], radius=26, fill=(5, 8, 15),
                        outline=(255, 255, 255, 26), width=2)
    for i, c in enumerate((RED, AMBER, GREEN)):
        d.ellipse([x0 + 34 + i * 34, y0 + 30, x0 + 54 + i * 34, y0 + 50], fill=c)
    fp = font("monor", mono_size)
    y = y0 + 96
    for prompt, txt, col in lines:
        if prompt:
            d.text((x0 + 40, y), prompt, font=fp, fill=CYAN, anchor="lm")
        d.text((x0 + 40 + (d.textlength(prompt, font=fp) if prompt else 0) + 14, y),
               txt, font=fp, fill=col, anchor="lm")
        y += lh
    return y0 + h  # bottom y

# ---------------------------------------------------------------- highlight covers
def highlight(name, icon_fn, accent):
    img = canvas(1080, 1920, [(540, 960, 620, (8, 36, 20)), (540, 1750, 500, (36, 26, 8))])
    lay, ld = alpha_layer(img)
    ld.ellipse([540 - 386, 960 - 386, 540 + 386, 960 + 386], outline=accent + (46,), width=3)
    ld.ellipse([540 - 336, 960 - 336, 540 + 336, 960 + 336], outline=accent + (230,), width=7)
    img = Image.alpha_composite(img, lay)
    d = ImageDraw.Draw(img)
    icon_fn(img, d, 540, 960, 190, WHITE, 22)
    img.convert("RGB").save(os.path.join(DIR_HL, name + ".png"))

# ---------------------------------------------------------------- feed posts
def post(fname, kicker, headline, accent=CYAN, hl_size=84, body=None,
         chips=None, rows=None, row_gap=128, checklist=None, terminal=None, quote=None,
         counter=None, big_icon=None, cta='DM "PROJECT" to start', y_start=248):
    img = canvas(1080, 1350, [(900, 180, 420, (8, 36, 20)), (140, 1240, 460, (36, 26, 8))])
    d = ImageDraw.Draw(img)

    # top bar
    mini_logo(img, d, 132, 104, 36, accent)
    d.text((980, 104), HANDLE, font=font("monor", 34), fill=MUTED, anchor="rm")
    d.line([(96, 168), (984, 168)], fill=(255, 255, 255, 26), width=2)

    y = y_start
    text_ls(d, (540, y), kicker.upper(), font("bold", 34), accent, ls=12)
    y += 40

    fh = font("bold", hl_size)
    for line in wrap(d, headline, fh, 890):
        d.text((540, y + hl_size * 0.62), line, font=fh, fill=WHITE, anchor="mm")
        y += int(hl_size * 1.18)
    if counter:
        d.text((984, 248), counter, font=font("monor", 34), fill=MUTED, anchor="rm")

    y += 16
    if body:
        fb = font("reg", 42)
        for line in wrap(d, body, fb, 860):
            d.text((540, y + 28), line, font=fb, fill=MUTED, anchor="mm")
            y += 60
        y += 20

    if big_icon:
        icon_fn, s = big_icon
        icon_fn(img, d, 540, y + s + 20, s, accent, 18)
        y += 2 * s + 40

    if chips:
        fch = font("bold", 32)
        widths = [d.textlength(c, font=fch) + 64 for c in chips]
        total = sum(widths) + 20 * (len(chips) - 1)
        x = 540 - total / 2
        for c, w in zip(chips, widths):
            d.rounded_rectangle([x, y, x + w, y + 66], radius=33, outline=accent, width=3)
            d.text((x + w / 2, y + 33), c, font=fch, fill=WHITE, anchor="mm")
            x += w + 20
        y += 66 + 30

    if rows:
        for icon_fn, title, sub in rows:
            icon_fn(img, d, 168, y + 52, 30, accent, 8)
            d.text((240, y + 18), title, font=font("bold", 46), fill=WHITE, anchor="lm")
            d.text((240, y + 74), sub, font=font("reg", 36), fill=MUTED, anchor="lm")
            y += row_gap
        y += 6

    if checklist:
        for item in checklist:
            icon_check(d, 160, y + 30, 22, GREEN, 8)
            d.text((212, y + 30), item, font=font("reg", 42), fill=WHITE, anchor="lm")
            y += 70
        y += 8

    if quote:
        text_, author = quote
        d.text((140, y + 40), '"', font=font("bold", 300), fill=VIOLET, anchor="la")
        fq = font("italic", 56)
        yy = y + 210
        for line in wrap(d, text_, fq, 820):
            d.text((540, yy + 34), line, font=fq, fill=WHITE, anchor="mm")
            yy += 76
        d.text((540, yy + 40), author, font=font("bold", 40), fill=VIOLET, anchor="mm")

    if terminal:
        bottom = terminal_block(d, 120, y, 960, terminal)
        assert bottom < 1150, fname + ": terminal overflows (" + str(bottom) + ")"

    pill_cta(d, 1240, cta, accent)
    assert y < 1170 or terminal, fname + ": content overflow (" + str(y) + ")"
    img.convert("RGB").save(os.path.join(DIR_POST, fname + ".png"))
    print("post:", fname, "content-bottom:", int(y))

# ---------------------------------------------------------------- previews
def grid_preview():
    files = sorted(os.listdir(DIR_POST))[:9]
    cell, gap = 340, 22
    size = cell * 3 + gap * 2
    sheet = Image.new("RGB", (size, size), BG)
    for i, fn in enumerate(files):
        im = Image.open(os.path.join(DIR_POST, fn)).resize((cell, cell), Image.LANCZOS)
        r, c = divmod(i, 3)
        sheet.paste(im, (c * (cell + gap), r * (cell + gap)))
    sheet.save(os.path.join(ROOT, "assets", "grid-preview.png"))

def covers_sheet():
    files = sorted(os.listdir(DIR_HL))
    cw, ch, gap = 290, 516, 18
    sheet = Image.new("RGB", (cw * 4 + gap * 5, ch * 2 + gap * 3), BG)
    for i, fn in enumerate(files):
        im = Image.open(os.path.join(DIR_HL, fn)).resize((cw, ch), Image.LANCZOS)
        r, c = divmod(i, 4)
        sheet.paste(im, (gap + c * (cw + gap), gap + r * (ch + gap)))
    sheet.save(os.path.join(ROOT, "assets", "covers-sheet.png"))

def logo():
    S = 2  # supersample for smooth edges, then downscale
    img = canvas(1024 * S, 1024 * S,
                 [(512 * S, 380 * S, 380 * S, (8, 36, 20)), (512 * S, 760 * S, 340 * S, (36, 26, 8))])
    d = ImageDraw.Draw(img)
    d.ellipse([512 * S - 356 * S, 512 * S - 356 * S, 512 * S + 356 * S, 512 * S + 356 * S],
              outline=CYAN + (60,), width=3 * S)
    icon_shield(img, d, 512 * S, 512 * S, 250 * S, CYAN, 26 * S)
    d.text((512 * S, 528 * S), "</>", font=font("mono", 130 * S), fill=WHITE, anchor="mm")
    img.resize((1024, 1024), Image.LANCZOS).convert("RGB").save(
        os.path.join(ROOT, "assets", "logo.png"))

    tr = Image.new("RGBA", (1024 * S, 1024 * S), (0, 0, 0, 0))
    d = ImageDraw.Draw(tr)
    icon_shield(tr, d, 512 * S, 512 * S, 250 * S, CYAN + (255,), 26 * S)
    d.text((512 * S, 528 * S), "</>", font=font("mono", 130 * S), fill=WHITE, anchor="mm")
    tr.resize((1024, 1024), Image.LANCZOS).save(
        os.path.join(ROOT, "assets", "logo-transparent.png"))

# ---------------------------------------------------------------- build
if __name__ == "__main__":
    print("brand handle:", HANDLE)

    # highlights
    highlight("01-services", lambda i, d, x, y, s, c, w: icon_grid(d, x, y, s, c, w), CYAN)
    highlight("02-work",     lambda i, d, x, y, s, c, w: icon_code(d, x, y, s, c, w, "</>"), CYAN)
    highlight("03-security", lambda i, d, x, y, s, c, w: icon_shield(i, d, x, y, s, c, w, inner_check=True), RED)
    highlight("04-python",   lambda i, d, x, y, s, c, w: icon_code(d, x, y, s, c, w, "{py}"), VIOLET)
    highlight("05-reviews",  lambda i, d, x, y, s, c, w: icon_star(d, x, y, s, c, w), VIOLET)
    highlight("06-about",    lambda i, d, x, y, s, c, w: icon_duo(d, x, y, s, c, w), CYAN)
    highlight("07-tips",     lambda i, d, x, y, s, c, w: icon_bulb(d, x, y, s, c, w), AMBER)
    highlight("08-contact",  lambda i, d, x, y, s, c, w: icon_mail(d, x, y, s, c, w), CYAN)
    print("highlights: 8 done")

    # posts
    post("01-intro",
         kicker="who we are",
         headline="Software, built right. Security, proven.",
         body="A team of two: one software engineer, one cybersecurity specialist. We build your product, then attack it the way real attackers would, so your users never have to.",
         chips=["SOFTWARE DEV", "CYBERSECURITY", "PYTHON"],
         big_icon=(lambda i, d, x, y, s, c, w: icon_duo(d, x, y, s, c, w), 108))

    post("02-services",
         kicker="what we do",
         headline="Three ways we can help",
         rows=[
             (lambda i, d, x, y, s, c, w: icon_code(d, x, y, s, c, w, "</>"),
              "Custom Software", "Web apps, dashboards, MVPs"),
             (lambda i, d, x, y, s, c, w: icon_shield(i, d, x, y, s, c, w, inner_check=True),
              "Cybersecurity", "Audits, pentesting, hardening"),
             (lambda i, d, x, y, s, c, w: icon_code(d, x, y, s, c, w, "{py}"),
              "Python Automation", "Bots, scripts, data pipelines"),
         ])

    post("03-service-dev",
         kicker="service 01", counter="01 / 03", hl_size=74,
         headline="Custom software development",
         body="From idea to deployed product, with code your next developer will thank you for.",
         checklist=["Web apps & internal tools", "MVPs for startups",
                    "APIs & integrations", "Clean, documented code"],
         big_icon=(lambda i, d, x, y, s, c, w: icon_code(d, x, y, s, c, w, "</>"), 85))

    post("04-service-security",
         kicker="service 02", counter="02 / 03", accent=RED, hl_size=74,
         headline="Cybersecurity, on your side",
         body="We think like attackers so your business never becomes the headline.",
         checklist=["Security audits", "Penetration testing",
                    "Clear fix-it reports", "Team security training"],
         big_icon=(lambda i, d, x, y, s, c, w: icon_shield(i, d, x, y, s, c, w, inner_check=True), 85))

    post("05-service-python",
         kicker="service 03", counter="03 / 03", accent=VIOLET, hl_size=74,
         headline="Python automation & data",
         body="Stop doing robot work. Let robots do it.",
         checklist=["Bots & scrapers", "Workflow automation",
                    "Data pipelines & reports", "Custom scripts & tools"],
         big_icon=(lambda i, d, x, y, s, c, w: icon_code(d, x, y, s, c, w, "{py}"), 85))

    post("06-testimonial",
         kicker="client love",
         headline="",
         quote=("They delivered ahead of schedule and found security issues we did not know existed.", "--  Client Name, Company"),
         cta="Your project next?  DM us")

    post("07-tip",
         kicker="free tip",
         headline="Your password policy is lying to you",
         terminal=[
             ("$", "audit --passwords", WHITE),
             ("", "[!] 3 users share: Summer2024!", AMBER),
             ("", "[+] fix: 12+ chars, unique, 2FA", GREEN),
         ])

    post("08-cta",
         kicker="let's work",
         headline="Got an idea? We ship it. Safely.",
         body="Free 15-minute chat. We tell you honestly if we are the right team for it.",
         terminal=[
             ("$", "hire_us --now", WHITE),
             ("", "> status: accepting projects", GREEN),
             ("", "> next step: DM " + HANDLE, CYAN),
         ])

    post("09-why-us",
         kicker="why us", y_start=300, row_gap=160,
         headline="We build it. Then we protect it.",
         rows=[
             (lambda i, d, x, y, s, c, w: icon_check(d, x, y, s, GREEN, w),
              "Fixed quotes", "No surprise invoices, ever"),
             (lambda i, d, x, y, s, c, w: icon_chat(d, x, y, s, AMBER, w),
              "No jargon", "Reports a manager can read"),
             (lambda i, d, x, y, s, c, w: icon_shield(i, d, x, y, s, c, w, inner_check=True),
              "Security baked in", "Not bolted on at the end"),
         ])

    logo()
    grid_preview()
    covers_sheet()
    print("done.")
