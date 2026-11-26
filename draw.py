#!/usr/bin/env python3
"""Render the front page of 'The World in One Day' for 25 November 2026.

One 1024x1024 PNG newspaper page, drawn with Pillow. All copy is baked
into this file, so rendering is deterministic: same input, same bytes.
Run: python3 draw.py  (writes entry.png next to this file).
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (250, 246, 238)
INK = (24, 22, 18)
RED = (158, 24, 28)
GREY = (96, 90, 80)
FAINT = (186, 178, 162)
NAVY = (28, 44, 66)
SKY = (214, 226, 232)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

MX = 40                      # side margin
CW = W - 2 * MX              # 944 content width


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, f, width):
    """Greedy word wrap; returns lines that fit in width."""
    out, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=f) <= width:
            cur = trial
        else:
            if cur:
                out.append(cur)
            cur = word
    if cur:
        out.append(cur)
    return out


def para(d, x, y, lines, f, fill=INK, lead=4):
    lh = f.size + lead
    for ln in lines:
        d.text((x, y), ln, font=f, fill=fill)
        y += lh
    return y


def hrule(d, x, y, w, color=INK, weight=2):
    d.rectangle([x, y, x + w - 1, y + weight - 1], fill=color)
    return y + weight


def story(d, x, y, w, kick, head, body, head_size=21, body_size=15):
    """Kicker + headline + body block. Returns y below the block."""
    y = para(d, x, y, [kick], font(SANS_B, 12), RED, 0)
    y += 6
    y = para(d, x, y, wrap(d, head, font(SERIF_B, head_size), w),
             font(SERIF_B, head_size), INK, 2)
    y += 5
    y = para(d, x, y, wrap(d, body, font(SERIF, body_size), w),
             font(SERIF, body_size), INK, 5)
    return y


def tanker_art(d, x, y, w, h):
    """Small line-art tanker on waves inside a pale sky box."""
    d.rectangle([x, y, x + w - 1, y + h - 1], fill=SKY)
    d.rectangle([x, y, x + w - 1, y + h - 1], outline=INK, width=2)
    sea = y + int(h * 0.62)
    d.rectangle([x, sea, x + w - 1, y + h - 1], fill=(178, 198, 210))
    # hull
    hx, hy, hw, hh = x + 22, sea - 26, w - 44, 26
    d.polygon([(hx, hy), (hx + hw, hy), (hx + hw - 14, hy + hh),
               (hx + 10, hy + hh)], fill=INK)
    # deck + funnel
    d.rectangle([hx + 16, hy - 22, hx + 52, hy], fill=INK)
    d.rectangle([hx + hw - 52, hy - 30, hx + hw - 30, hy], fill=RED)
    # smoke (kept inside the art box)
    for cx, cy, r in [(hx + hw - 40, hy - 26, 7), (hx + hw - 30, hy - 38, 9),
                      (hx + hw - 18, hy - 50, 8)]:
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(120, 118, 110))
    # waves
    for wx in range(x + 8, x + w - 8, 34):
        d.arc([wx, sea + 12, wx + 30, sea + 30], 0, 180, fill=NAVY, width=2)
    d.text((x + 10, y + h - 22), "TWO TANKERS HIT MINES IN THE STRAIT",
           font=font(SANS_B, 10), fill=NAVY)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    # outer frame
    d.rectangle([10, 10, W - 11, H - 11], outline=INK, width=3)
    d.rectangle([16, 16, W - 17, H - 17], outline=FAINT, width=1)

    y = 30
    # masthead
    title = "THE WORLD IN ONE DAY"
    tf = font(SERIF_B, 58)
    d.text(((W - d.textlength(title, font=tf)) / 2, y), title,
           font=tf, fill=INK)
    y += 72
    sub = "WEDNESDAY, 25 NOVEMBER 2026  ·  SIX STORIES FROM AROUND THE GLOBE"
    sf = font(SANS_B, 14)
    d.text(((W - d.textlength(sub, font=sf)) / 2, y), sub, font=sf, fill=RED)
    y += 26
    y = hrule(d, MX, y, CW, INK, 4)
    y = hrule(d, MX, y + 3, CW, INK, 1)
    y += 12

    # ---- lead story: Hormuz, with tanker art on the right ----
    lead_top = y
    art_w, art_h = 300, 148
    tanker_art(d, MX + CW - art_w, lead_top + 4, art_w, art_h)
    lx, lw = MX, CW - art_w - 24
    y = para(d, lx, lead_top, ["THE STRAIT OF HORMUZ"], font(SANS_B, 13), RED, 0)
    y += 7
    y = para(d, lx, y,
             wrap(d, "Tankers ablaze as mines close the world's oil artery",
                  font(SERIF_B, 30), lw), font(SERIF_B, 30), INK, 3)
    y += 7
    y = para(d, lx, y,
             wrap(d, "Iran's Revolutionary Guards said two oil tankers hit "
                  "naval mines early on Wednesday and caught fire while "
                  "crossing on what Tehran called an \u201cunauthorised "
                  "route\u201d. The US military disputes the account. Brent "
                  "crude jumped past $93 a barrel as shipping through the "
                  "strait stayed disrupted.", font(SERIF, 15), lw),
             font(SERIF, 15), INK, 5)
    y = max(y, lead_top + art_h + 10)
    y += 6
    y = hrule(d, MX, y, CW, INK, 2)
    y += 14

    # ---- two-column rows ----
    col_w = (CW - 28) // 2
    x2 = MX + col_w + 28

    row1 = y
    y1 = story(d, MX, row1, col_w, "SPACE",
               "Pakistan's first astronaut reaches orbit",
               "Shenzhou-24 lifted off at 08:18 Beijing time carrying "
               "Muhammad Zeeshan Ali, 40, with Tang Hongbo and Wu Yi, and "
               "docked with the Tiangong station three and a half hours "
               "later \u2014 the first foreign astronaut aboard China's "
               "space station.")
    y2 = story(d, x2, row1, col_w, "SAUDI ARABIA",
               "Houthis claim refinery strike; Riyadh tower hit again",
               "The Houthis said they struck Ras Tanura, the kingdom's "
               "largest refinery, and satellite images showed smoke over "
               "the site. The Saudi-led coalition said it downed four "
               "drones. A day earlier a strike on the PIF tower in Riyadh "
               "wounded 11 people.")
    y = max(y1, y2) + 12
    y = hrule(d, MX, y, CW, FAINT, 1)
    y += 12

    row2 = y
    y1 = story(d, MX, row2, col_w, "NEW YORK",
               "Huawei convicted on 10 of 12 counts in US trial",
               "A Brooklyn jury found the Chinese telecoms giant guilty of "
               "bank fraud, wire fraud, Iran sanctions violations and "
               "conspiring to steal trade secrets. It was acquitted of "
               "racketeering. Sentencing is set for 14 September 2027.")
    y2 = story(d, x2, row2, col_w, "WASHINGTON",
               "Trump proposes new tariffs on 14 trading partners",
               "Headline rates of 20% to 40% were proposed, capped at 10% "
               "to 20% under trade deals already struck or under "
               "negotiation. China faces 20%, rising to 40% if its trade "
               "truce unravels. A hearing is set for 25 January.")
    y = max(y1, y2) + 12
    y = hrule(d, MX, y, CW, FAINT, 1)
    y += 12

    # ---- Cairo, full width ----
    y = story(d, MX, y, CW, "CAIRO",
              "31 killed as fuel tanker fire engulfs Cairo ring road",
              "A tanker overturned on the Ring Road in Al-Warraq, Giza, on "
              "Wednesday evening and the fire spread to 27 vehicles. At "
              "least 31 people were killed and 21 injured, Egypt's health "
              "ministry said.", head_size=20, body_size=15)
    y += 12
    y = hrule(d, MX, y, CW, INK, 2)
    y += 10

    # ---- also strip ----
    y = para(d, MX, y, ["ALSO IN THE NEWS"], font(SANS_B, 12), RED, 0)
    y += 6
    also = [
        "More than 30 countries urge Russia to stop using chemical agents in Ukraine.",
        "Spain heads to a snap general election on Sunday.",
        "Wall Street slides as the S&P 500 closes down 0.25% on tariff fears.",
        "US intelligence agencies CIA and ODNI hit by a cyber breach.",
        "Bangladesh raises garment workers' minimum wage 36% to $139 a month.",
    ]
    af = font(SERIF, 14)
    for item in also:
        d.text((MX + 14, y), "\u2022", font=af, fill=RED)
        y = para(d, MX + 30, y, wrap(d, item, af, CW - 30), af, INK, 3)
        y += 2

    # ---- footer ----
    fy = H - 52
    hrule(d, MX, fy, CW, INK, 1)
    foot = ("THE WORLD IN ONE DAY  ·  25 NOVEMBER 2026  ·  Sources: Reuters, "
            "AP, CNN, NPR, Xinhua  ·  Built by an AI agent for make.fun")
    ff = font(SANS, 11)
    d.text(((W - d.textlength(foot, font=ff)) / 2, fy + 10), foot,
           font=ff, fill=GREY)

    img.save("entry.png")
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
