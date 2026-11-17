#!/usr/bin/env python3
"""Move to Social blog kapak üretici.

Kullanım:
  python3 _tools/kapak.py --beyaz "Instagram Reklam" --yesil "Fiyatları 2026" \
      --etiket "Reklam" --cikti blog/gorseller/instagram-reklam-fiyatlari/kapak.png

Çıktı: 1200x630 PNG (blog kapağı + Open Graph paylaşım görseli).
Gerekli: playwright + chromium (CHROME yolu ortam değişkeniyle verilebilir).
"""
import argparse, base64, os, pathlib, html

KOK = pathlib.Path(__file__).resolve().parent.parent
FONT = KOK / "_tools" / "fonts"


def font_css():
    rng_latin = "U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD"
    rng_ext = "U+0100-02BA,U+02BD-02C5,U+02C7-02CC,U+02CE-02D7,U+02DD-02FF,U+0304,U+0308,U+0329,U+1D00-1DBF,U+1E00-1E9F,U+1EF2-1EFF,U+2020,U+20A0-20AB,U+20AD-20C0,U+2113,U+2C60-2C7F,U+A720-A7FF"
    out = []
    for w in (500, 700, 800):
        for sub, rng in (("latin-ext", rng_ext), ("latin", rng_latin)):
            f = FONT / f"dm-sans-{sub}-{w}-normal.woff2"
            b = base64.b64encode(f.read_bytes()).decode()
            out.append(f"@font-face{{font-family:'DM Sans';font-weight:{w};src:url(data:font/woff2;base64,{b}) format('woff2');unicode-range:{rng}}}")
    return "\n".join(out)


def svg_data(path):
    return "data:image/svg+xml;base64," + base64.b64encode(pathlib.Path(path).read_bytes()).decode()


def sayfa(beyaz, yesil, etiket):
    logo = svg_data(KOK / "assets" / "logo-beyaz.svg")
    ikon = svg_data(KOK / "assets" / "ikon-yesil.svg")
    e = html.escape
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{font_css()}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:1200px;height:630px;overflow:hidden;background:#030A07;font-family:'DM Sans',sans-serif;color:#fff;position:relative}}
.glow{{position:absolute;left:50%;top:-260px;width:1100px;height:620px;transform:translateX(-50%);background:radial-gradient(closest-side,rgba(35,127,82,.42),transparent)}}
.arc{{position:absolute;left:50%;top:505px;width:2300px;height:2300px;transform:translateX(-50%);border-radius:50%;
 background:radial-gradient(circle at 50% 0%,#0E3B28 0%,#06140E 9%,#030A07 18%);
 box-shadow:0 -2px 0 #D9FFEE,0 -8px 30px rgba(185,245,216,.8),0 -40px 140px 14px rgba(53,212,142,.5),inset 0 34px 90px -20px rgba(53,212,142,.6)}}
.ikon{{position:absolute;right:-70px;top:120px;width:470px;opacity:.07}}
.logo{{position:absolute;left:72px;top:58px;width:150px}}
.etiket{{position:absolute;right:72px;top:72px;padding:10px 22px;border-radius:999px;font-weight:700;font-size:20px;color:#B9F5D8;background:rgba(53,212,142,.1);border:1.5px solid rgba(53,212,142,.4)}}
h1{{position:absolute;left:72px;right:150px;top:200px;font-weight:800;font-size:76px;line-height:1.04;letter-spacing:-.035em}}
h1 .b{{display:block;background:linear-gradient(180deg,#fff 30%,#B8CBC2);-webkit-background-clip:text;color:transparent}}
h1 .y{{display:block;background:linear-gradient(95deg,#5BE3A8,#2FA36C);-webkit-background-clip:text;color:transparent;padding-bottom:6px}}
.alt{{position:absolute;left:72px;bottom:34px;font-weight:500;font-size:20px;color:rgba(222,236,229,.75);letter-spacing:.01em}}
</style></head><body>
<div class="glow"></div><img class="ikon" src="{ikon}"><div class="arc"></div>
<img class="logo" src="{logo}"><div class="etiket">{e(etiket)}</div>
<h1><span class="b">{e(beyaz)}</span><span class="y">{e(yesil)}</span></h1>
<div class="alt">movetosocial.com.tr/blog</div>
</body></html>"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--beyaz", required=True, help="Başlığın beyaz kısmı")
    ap.add_argument("--yesil", required=True, help="Başlığın yeşil kısmı")
    ap.add_argument("--etiket", required=True, help="Kategori etiketi")
    ap.add_argument("--cikti", required=True)
    a = ap.parse_args()
    from playwright.sync_api import sync_playwright
    cikti = pathlib.Path(a.cikti)
    cikti.parent.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        kw = {}
        if os.environ.get("CHROME"):
            kw["executable_path"] = os.environ["CHROME"]
        b = p.chromium.launch(**kw)
        pg = b.new_page(viewport={"width": 1200, "height": 630})
        pg.set_content(sayfa(a.beyaz, a.yesil, a.etiket))
        pg.wait_for_timeout(400)
        pg.screenshot(path=str(cikti))
        b.close()
    print(cikti)


if __name__ == "__main__":
    main()
