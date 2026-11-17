#!/usr/bin/env python3
"""Move to Social — blog yazısından Instagram carousel ve LinkedIn seti üretir.

Girdi:  _sosyal/<slug>/set.json
Çıktı:  _sosyal/<slug>/instagram-carousel-01.png ... (1080x1350)
        _sosyal/<slug>/linkedin-carousel.pdf      (aynı slaytlar, LinkedIn belge gönderisi için)
        _sosyal/<slug>/instagram-aciklama.txt     (açıklama + tam 5 hashtag)
        _sosyal/<slug>/linkedin-metin.txt

set.json:
{
  "slug": "...",
  "slaytlar": [
    {"tip": "kapak", "etiket": "Veri", "beyaz": "Türkiye'de", "yesil": "61 milyon kişi", "alt": "sosyal medyada. Peki hangi platformda?"},
    {"tip": "rakam", "rakam": "60,2 M", "baslik": "Instagram", "metin": "...", "kaynak": "DataReportal, Ekim 2026"},
    {"tip": "madde", "no": "01", "baslik": "...", "metin": "..."},
    {"tip": "liste", "baslik": "...", "maddeler": ["...", "..."]},
    {"tip": "cta", "baslik": "Yazının tamamı blogumuzda", "metin": "..."}
  ],
  "instagram": {"aciklama": "...", "hashtag": ["#a", "#b", "#c", "#d", "#e"]},
  "linkedin": "..."
}
Kullanım:  python3 _tools/sosyal.py <slug>    (CHROME=/yol/chrome isteğe bağlı)
"""
import json, sys, os, base64, html, pathlib

KOK = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(KOK / "_tools"))
from kapak import font_css, svg_data  # noqa: E402

e = html.escape
W, H = 1080, 1350


def ortak_css():
    return font_css() + """
*{margin:0;padding:0;box-sizing:border-box}
body{width:1080px;height:1350px;overflow:hidden;background:#030A07;font-family:'DM Sans',sans-serif;color:#EEF5F1;position:relative}
.glow{position:absolute;left:50%;top:-360px;width:1200px;height:800px;transform:translateX(-50%);background:radial-gradient(closest-side,rgba(35,127,82,.42),transparent)}
.cat{position:absolute;right:-120px;bottom:150px;width:620px;opacity:.06}
.logo{position:absolute;left:80px;top:72px;width:150px}
.sayfa{position:absolute;right:80px;top:84px;font-weight:700;font-size:26px;color:rgba(222,236,229,.55);letter-spacing:.02em}
.alt{position:absolute;left:80px;right:80px;bottom:64px;display:flex;justify-content:space-between;align-items:center;font-weight:500;font-size:26px;color:rgba(222,236,229,.7)}
.alt b{display:inline-flex;align-items:center;gap:10px;color:#B9F5D8;font-weight:700}
.alt b svg{width:30px;height:30px}
.icerik{position:absolute;left:80px;right:80px;top:230px;bottom:190px;display:flex;flex-direction:column;justify-content:center}
.badge{align-self:flex-start;padding:12px 26px;border-radius:999px;font-weight:700;font-size:28px;color:#B9F5D8;background:rgba(53,212,142,.1);border:2px solid rgba(53,212,142,.4);margin-bottom:40px}
.b{background:linear-gradient(180deg,#fff 30%,#B8CBC2);-webkit-background-clip:text;color:transparent}
.y{background:linear-gradient(95deg,#5BE3A8,#2FA36C);-webkit-background-clip:text;color:transparent}
h1{font-weight:800;font-size:112px;line-height:1.02;letter-spacing:-.04em}
h1 span{display:block;padding-bottom:6px}
h2{font-weight:700;font-size:72px;line-height:1.08;letter-spacing:-.035em;color:#fff}
p{font-weight:500;font-size:40px;line-height:1.4;color:rgba(238,245,241,.85)}
.altbaslik{margin-top:36px;font-size:44px}
.no{font-weight:800;font-size:150px;line-height:1;letter-spacing:-.05em;margin-bottom:28px}
.rakam{white-space:nowrap;font-weight:800;font-size:200px;line-height:1;letter-spacing:-.05em;margin-bottom:24px}
.kaynak{margin-top:40px;font-size:26px;color:rgba(222,236,229,.55)}
ul{list-style:none;margin-top:44px;display:grid;gap:26px}
li{position:relative;padding-left:58px;font-weight:500;font-size:40px;line-height:1.35;color:rgba(238,245,241,.9)}
li::before{content:"";position:absolute;left:4px;top:14px;width:22px;height:13px;border-left:5px solid #35D48E;border-bottom:5px solid #35D48E;transform:rotate(-45deg)}
.kart{padding:56px 54px;border-radius:40px;border:2px solid rgba(255,255,255,.1);background:linear-gradient(180deg,rgba(255,255,255,.06),rgba(255,255,255,.015))}
.arc{position:absolute;left:50%;top:1150px;width:2600px;height:2600px;transform:translateX(-50%);border-radius:50%;background:radial-gradient(circle at 50% 0%,#0E3B28 0%,#06140E 8%,#030A07 16%);box-shadow:0 -2px 0 #D9FFEE,0 -8px 32px rgba(185,245,216,.8),0 -40px 150px 16px rgba(53,212,142,.5),inset 0 34px 90px -20px rgba(53,212,142,.6)}
.cta-ic{text-align:center;align-items:center}
.cta-ic .orb{width:150px;height:150px;border-radius:50%;margin:0 auto 50px;display:grid;place-items:center;background:radial-gradient(circle at 35% 30%,#3FCB8B,#1B6A43);box-shadow:0 0 0 14px rgba(53,212,142,.1),0 0 90px rgba(53,212,142,.6)}
.cta-ic .orb img{width:84px}
.btn{display:inline-block;margin-top:50px;padding:26px 48px;border-radius:999px;font-weight:700;font-size:36px;color:#fff;background:linear-gradient(180deg,#2E9E67,#1F7449);box-shadow:0 0 0 2px rgba(53,212,142,.4),0 16px 50px -10px rgba(53,212,142,.7)}
"""


OK = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'


def slayt_html(s, i, n):
    logo = svg_data(KOK / "assets" / "logo-beyaz.svg")
    ikon_y = svg_data(KOK / "assets" / "ikon-yesil.svg")
    ikon_b = svg_data(KOK / "assets" / "ikon-beyaz.svg")
    t = s["tip"]
    son = i == n
    alt_sag = "" if son else f"<b>Kaydır {OK}</b>"
    arka = f'<div class="glow"></div><img class="cat" src="{ikon_y}">'
    if t == "kapak":
        govde = (f'<div class="icerik"><span class="badge">{e(s["etiket"])}</span>'
                 f'<h1><span class="b">{e(s["beyaz"])}</span><span class="y">{e(s["yesil"])}</span></h1>'
                 + (f'<p class="altbaslik">{e(s["alt"])}</p>' if s.get("alt") else "") + "</div>")
        arka += '<div class="arc"></div>'
    elif t == "rakam":
        govde = (f'<div class="icerik"><div class="kart"><div class="rakam y">{e(s["rakam"])}</div>'
                 f'<h2>{e(s["baslik"])}</h2>' + (f'<p style="margin-top:26px">{e(s["metin"])}</p>' if s.get("metin") else "")
                 + (f'<p class="kaynak">Kaynak: {e(s["kaynak"])}</p>' if s.get("kaynak") else "") + "</div></div>")
    elif t == "madde":
        govde = (f'<div class="icerik"><div class="no y">{e(s["no"])}</div><h2>{e(s["baslik"])}</h2>'
                 f'<p style="margin-top:34px">{e(s["metin"])}</p></div>')
    elif t == "liste":
        govde = (f'<div class="icerik"><h2>{e(s["baslik"])}</h2><ul>' + "".join(f"<li>{e(m)}</li>" for m in s["maddeler"]) + "</ul></div>")
    elif t == "cta":
        govde = (f'<div class="icerik cta-ic"><div class="orb"><img src="{ikon_b}"></div><h2>{e(s["baslik"])}</h2>'
                 f'<p style="margin-top:30px">{e(s["metin"])}</p><span class="btn">movetosocial.com.tr/blog</span></div>')
        arka += '<div class="arc" style="top:1210px"></div>'
    else:
        raise SystemExit(f"bilinmeyen slayt tipi: {t}")
    # metin taşarsa yazıları küçült
    sigdir = """<script>
document.fonts.ready.then(()=>{
document.querySelectorAll('.rakam,h1 span').forEach(r=>{let fs=parseFloat(getComputedStyle(r).fontSize);r.style.whiteSpace='nowrap';while(r.scrollWidth>r.clientWidth+1&&fs>40){fs-=4;r.style.fontSize=fs+'px'}});
const k=document.querySelector('.icerik');let f=1;
while(k.scrollHeight>k.clientHeight+2&&f>0.6){f-=0.04;k.style.zoom=f}
window.__hazir=true;});
</script>"""
    return (f"<!DOCTYPE html><html><head><meta charset='utf-8'><style>{ortak_css()}</style></head><body>{arka}"
            f'<img class="logo" src="{logo}"><div class="sayfa">{i}/{n}</div>{govde}'
            f'<div class="alt"><span>@movetosocialtr</span>{alt_sag}</div>{sigdir}</body></html>')


def main():
    if len(sys.argv) != 2:
        raise SystemExit("Kullanım: python3 _tools/sosyal.py <slug>")
    slug = sys.argv[1]
    klasor = KOK / "_sosyal" / slug
    d = json.loads((klasor / "set.json").read_text())
    tags = d["instagram"]["hashtag"]
    if len(tags) != 5:
        raise SystemExit(f"Instagram açıklamasında tam 5 hashtag olmalı (şu an {len(tags)})")
    for eski in klasor.glob("instagram-carousel-*.png"):
        eski.unlink()
    from playwright.sync_api import sync_playwright
    yollar = []
    with sync_playwright() as p:
        kw = {"executable_path": os.environ["CHROME"]} if os.environ.get("CHROME") else {}
        b = p.chromium.launch(**kw)
        pg = b.new_page(viewport={"width": W, "height": H})
        n = len(d["slaytlar"])
        for i, s in enumerate(d["slaytlar"], 1):
            pg.set_content(slayt_html(s, i, n))
            pg.wait_for_function("window.__hazir===true", timeout=10000)
            pg.wait_for_timeout(150)
            tasma = pg.evaluate("(()=>{const k=document.querySelector('.icerik');return k.scrollHeight>k.clientHeight+2})()")
            if tasma:
                print(f"UYARI: {i}. slaytta metin sığmıyor, kısaltın")
            yol = klasor / f"instagram-carousel-{i:02d}.png"
            pg.screenshot(path=str(yol))
            yollar.append(yol)
        b.close()
    from PIL import Image
    imgs = [Image.open(y).convert("RGB") for y in yollar]
    imgs[0].save(klasor / "linkedin-carousel.pdf", save_all=True, append_images=imgs[1:], resolution=150)
    blog = f"https://www.movetosocial.com.tr/blog/{slug}/"
    (klasor / "instagram-aciklama.txt").write_text(d["instagram"]["aciklama"].strip() + "\n\n" + " ".join(tags) + "\n")
    (klasor / "linkedin-metin.txt").write_text(d["linkedin"].strip().replace("{link}", blog) + "\n")
    print(f"{len(yollar)} slayt, linkedin-carousel.pdf ve metinler hazır: {klasor}")


if __name__ == "__main__":
    main()
