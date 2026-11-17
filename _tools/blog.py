#!/usr/bin/env python3
"""Move to Social blog derleyici.

Kaynaklar:  _kaynak/<slug>.json  (bilgiler)  +  _kaynak/<slug>.html  (yazı gövdesi)
Üretilenler:
  blog/<slug>/index.html   yazı sayfası
  blog/<slug>/kapak.png    kapak (yoksa _tools/kapak.py ile üretilir)
  blog/index.html          tüm yazılar
  index.html               ana sayfadaki BLOG-START/BLOG-END arası (son 3 yazı)
  sitemap.xml

Kullanım:  python3 _tools/blog.py            (CHROME=/yol/chrome isteğe bağlı)
Kurallar:  _tools/BLOG-KURALLARI.md
"""
import json, re, html, pathlib, subprocess, sys, datetime, urllib.parse

KOK = pathlib.Path(__file__).resolve().parent.parent
KAYNAK = KOK / "_kaynak"
SITE = "https://www.movetosocial.com.tr"
AYLAR = ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"]
e = html.escape


def mts():
    s = (KOK / "index.html").read_text()
    g = lambda k: re.search(k + r':\s*"([^"]*)"', s).group(1)
    return {k: g(k) for k in ("whatsapp", "telefonGorunen", "eposta", "instagram", "waMesaj")}


def tr_tarih(d):
    y, m, g = map(int, d.split("-"))
    return f"{g} {AYLAR[m-1]} {y}"


def okuma(govde):
    kelime = len(re.sub(r"<[^>]+>", " ", govde).split())
    return max(2, round(kelime / 200))


def slugla(t):
    t = t.lower()
    for a, b in zip("çğıöşüâîû", "cgiosuaiu"):
        t = t.replace(a, b)
    return re.sub(r"[^a-z0-9]+", "-", t).strip("-")


def yukle():
    yazilar = []
    for j in sorted(KAYNAK.glob("*.json")):
        m = json.loads(j.read_text())
        m["govde"] = (KAYNAK / f"{m['slug']}.html").read_text()
        zorunlu = ["slug", "baslik", "aciklama", "ozet", "kategori", "etiketler", "tarih", "kapak", "alt", "kaynaklar"]
        eksik = [k for k in zorunlu if k not in m]
        if eksik:
            sys.exit(f"{j.name}: eksik alan {eksik}")
        if len(m["baslik"]) > 60:
            print(f"UYARI {m['slug']}: başlık {len(m['baslik'])} karakter (en fazla 60)")
        if not 150 <= len(m["aciklama"]) <= 165:
            print(f"UYARI {m['slug']}: meta açıklama {len(m['aciklama'])} karakter (155-165 hedef)")
        if len(m["ozet"]) > 500:
            print(f"UYARI {m['slug']}: özet {len(m['ozet'])} karakter (en fazla 500)")
        yazilar.append(m)
    yazilar.sort(key=lambda m: m["tarih"], reverse=True)
    return yazilar


IG_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r=".6" fill="currentColor"/></svg>'
IGAD = "movetosocialtr"


WA_SVG = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M17.5 14.4c-.3-.1-1.8-.9-2-1-.3-.1-.5-.1-.7.1-.2.3-.8 1-.9 1.2-.2.2-.3.2-.6.1-.3-.1-1.3-.5-2.4-1.5-.9-.8-1.5-1.8-1.7-2.1-.2-.3 0-.5.1-.6l.4-.5c.2-.2.2-.3.3-.5.1-.2 0-.4 0-.5l-.9-2.2c-.2-.6-.5-.5-.7-.5h-.6c-.2 0-.5.1-.8.4-.3.3-1 1-1 2.5s1.1 2.9 1.2 3.1c.1.2 2.1 3.2 5.1 4.5.7.3 1.3.5 1.7.6.7.2 1.4.2 1.9.1.6-.1 1.8-.7 2-1.4.2-.7.2-1.3.2-1.4-.1-.1-.3-.2-.6-.3zM12 21.8c-1.8 0-3.5-.5-5-1.4l-.4-.2-3.7 1 1-3.6-.2-.4c-1-1.6-1.5-3.4-1.5-5.2 0-5.4 4.4-9.8 9.8-9.8 2.6 0 5.1 1 6.9 2.9 1.9 1.9 2.9 4.3 2.9 6.9 0 5.4-4.4 9.8-9.8 9.8zm8.4-18.2C18.1 1.3 15.1 0 12 0 5.5 0 .2 5.3.2 11.8c0 2.1.5 4.1 1.6 5.9L0 24l6.4-1.7c1.7.9 3.7 1.4 5.6 1.4 6.5 0 11.8-5.3 11.8-11.8 0-3.2-1.2-6.1-3.4-8.3z"/></svg>'


def bas(baslik, aciklama, yol, gorsel=None, gorsel_alt="", jsonld=None, tur="website"):
    og = ""
    if gorsel:
        og = (f'<meta property="og:image" content="{SITE}{gorsel}">\n<meta property="og:image:width" content="1200">\n'
              f'<meta property="og:image:height" content="630">\n<meta property="og:image:alt" content="{e(gorsel_alt)}">\n'
              f'<meta name="twitter:image:alt" content="{e(gorsel_alt)}">\n')
    ld = "".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>\n' for x in (jsonld or []))
    return f"""<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(baslik)}</title>
<meta name="description" content="{e(aciklama)}">
<link rel="canonical" href="{SITE}{yol}">
<meta name="theme-color" content="#030A07">
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" type="image/svg+xml" href="/assets/favicon.svg">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<meta property="og:type" content="{tur}">
<meta property="og:locale" content="tr_TR">
<meta property="og:site_name" content="Move to Social">
<meta property="og:title" content="{e(baslik)}">
<meta property="og:description" content="{e(aciklama)}">
<meta property="og:url" content="{SITE}{yol}">
{og}<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:opsz,wght@9..40,400;9..40,500;9..40,600;9..40,700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/blog.css">
{ld}</head>
<body>
<header>
  <div class="wrap nav" id="nav">
    <a href="/" aria-label="Move to Social ana sayfa"><img class="logo" src="/assets/logo-beyaz.svg" alt="Move to Social" width="104" height="49"></a>
    <ul>
      <li><a href="/#hizmetler">Hizmetler</a></li>
      <li><a href="/#sektorler">Sektörler</a></li>
      <li><a href="/#egitimler">Eğitimler</a></li>
      <li><a href="/blog/" class="on">Blog</a></li>
      <li><a href="/#sss">SSS</a></li>
    </ul>
    <div class="act">
      <a class="ig" href="https://www.instagram.com/{IGAD}/" target="_blank" rel="noopener" aria-label="Instagram: @{IGAD}">{IG_SVG}</a>
      <a class="btn b-main js-wa" href="/#iletisim">Teklif Alın</a>
      <button class="menu-btn" aria-label="Menüyü aç" onclick="document.getElementById('nav').classList.toggle('open')">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M4 7h16M4 12h16M4 17h16"/></svg>
      </button>
    </div>
  </div>
</header>
<main>
"""


def son(c, ekstra_js="", mesaj=None):
    mesaj = mesaj or "Merhaba, Move to Social'dan teklif almak istiyorum."
    wa = "https://wa.me/" + c["whatsapp"] + "?text=" + urllib.parse.quote(mesaj)
    return f"""</main>
<footer>
  <div class="wrap bot">
    <span>© {datetime.date.today().year} Move to Social. Tüm hakları saklıdır.</span>
    <nav><a href="/#hizmetler">Hizmetler</a><a href="/#sektorler">Sektörler</a><a href="/#egitimler">Eğitimler</a><a href="/blog/">Blog</a><a href="/#iletisim">İletişim</a><a class="igl" href="https://www.instagram.com/{IGAD}/" target="_blank" rel="noopener">{IG_SVG}@{IGAD}</a></nav>
  </div>
</footer>
<a class="wa js-wa" href="{wa}" target="_blank" rel="noopener" aria-label="WhatsApp'tan yazın">{WA_SVG}</a>
<script>
{{
  document.querySelectorAll(".js-wa").forEach(a => {{ a.href = "{wa}"; a.target = "_blank"; a.rel = "noopener"; }});
  {ekstra_js}
}}
</script>
</body>
</html>
"""


def kart(m, h="h3"):
    return (f'<a class="bcard" href="/blog/{m["slug"]}/" data-k="{e(m["kategori"])}">'
            f'<img src="/blog/{m["slug"]}/kapak.png" alt="{e(m["alt"][0])}" width="1200" height="630" loading="lazy">'
            f'<div class="bc"><div class="meta"><span>{e(m["kategori"])}</span><span>{tr_tarih(m["tarih"])}</span><span>{okuma(m["govde"])} dk okuma</span></div>'
            f'<{h}>{e(m["baslik"])}</{h}><p>{e(m["kart"] if m.get("kart") else m["aciklama"])}</p></div></a>')


def ilgili(m, hepsi):
    if m.get("ilgili"):
        secili = [x for s in m["ilgili"] for x in hepsi if x["slug"] == s]
    else:
        secili = []
    digerleri = [x for x in hepsi if x["slug"] != m["slug"] and x not in secili]
    digerleri.sort(key=lambda x: (len(set(x["etiketler"]) & set(m["etiketler"])) + (2 if x["kategori"] == m["kategori"] else 0), x["tarih"]), reverse=True)
    return (secili + digerleri)[:3]


def toc_ve_govde(govde):
    basliklar = []

    def ekle(mt):
        metin = re.sub(r"<[^>]+>", "", mt.group(2))
        kimlik = slugla(metin)[:60]
        basliklar.append((kimlik, metin))
        return f'<h2{mt.group(1)} id="{kimlik}">{mt.group(2)}</h2>'

    govde = re.sub(r"<h2([^>]*)>(.*?)</h2>", ekle, govde)
    return basliklar, govde


def yazi_sayfasi(m, hepsi, c):
    yol = f"/blog/{m['slug']}/"
    kapak = f"/blog/{m['slug']}/kapak.png"
    basliklar, govde = toc_ve_govde(m["govde"])
    toc = ""
    if len(basliklar) >= 3:
        toc = '<nav class="toc" aria-label="İçindekiler"><strong>İçindekiler</strong><ol>' + "".join(
            f'<li><a href="#{k}">{e(t)}</a></li>' for k, t in basliklar) + "</ol></nav>"
    sss = ""
    if m.get("sss"):
        sss = '<section class="faq"><h2 id="sik-sorulan-sorular">Sık sorulan sorular</h2>' + "".join(
            f"<details><summary>{e(q['s'])}</summary><p>{e(q['c'])}</p></details>" for q in m["sss"]) + "</section>"
    kaynak = '<section class="srcs"><h2>Kaynaklar</h2><ol>' + "".join(
        f'<li><a href="{e(k["url"])}" target="_blank" rel="noopener">{e(k["ad"])}</a></li>' for k in m["kaynaklar"]) + "</ol></section>"
    etiket = '<div class="tags">' + "".join(f"<span>{e(t)}</span>" for t in m["etiketler"]) + "</div>"
    cta = m.get("cta") or {"baslik": "Markanızın sosyal medyasını birlikte büyütelim", "metin": "İhtiyacınızı WhatsApp'tan kısaca yazın, size özel teklifimizle dönelim."}
    ilg = ilgili(m, hepsi)
    ilgili_html = ""
    if ilg:
        ilgili_html = '<section class="related"><div class="wrap"><h2>İlgili yazılar</h2><div class="bgrid">' + "".join(kart(x) for x in ilg) + "</div></div></section>"
    ld = [
        {"@context": "https://schema.org", "@type": "BlogPosting", "headline": m["baslik"], "description": m["aciklama"],
         "image": SITE + kapak, "datePublished": m["tarih"], "dateModified": m.get("guncelleme", m["tarih"]),
         "inLanguage": "tr-TR", "mainEntityOfPage": SITE + yol, "keywords": ", ".join(m["etiketler"]),
         "author": {"@type": "Organization", "name": "Move to Social", "url": SITE + "/"},
         "publisher": {"@type": "Organization", "name": "Move to Social", "logo": {"@type": "ImageObject", "url": SITE + "/assets/logo-siyah.svg"}}},
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Ana sayfa", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": "Blog", "item": SITE + "/blog/"},
            {"@type": "ListItem", "position": 3, "name": m["baslik"], "item": SITE + yol}]},
    ]
    if m.get("sss"):
        ld.append({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q["s"], "acceptedAnswer": {"@type": "Answer", "text": q["c"]}} for q in m["sss"]]})
    sayfa = bas(f'{m["baslik"]} | Move to Social', m["aciklama"], yol, kapak, m["alt"][1], ld, "article")
    sayfa += f"""<article>
<div class="narrow">
  <div class="crumb"><a href="/">Ana sayfa</a> › <a href="/blog/">Blog</a> › {e(m["kategori"])}</div>
  <div class="post-head">
    <span class="badge">{e(m["kategori"])}</span>
    <h1>{e(m.get("h1", m["baslik"]))}</h1>
    <div class="post-meta"><span>Move to Social</span><span>{tr_tarih(m["tarih"])}</span><span>{okuma(m["govde"])} dk okuma</span></div>
  </div>
</div>
<div class="wrap" style="max-width:980px"><figure class="cover"><img src="{kapak}" alt="{e(m["alt"][0])}" width="1200" height="630"></figure></div>
<div class="narrow">
  <div class="tldr"><strong>Kısaca</strong><p>{e(m["ozet"])}</p></div>
  {toc}
  <div class="prose">
{govde}
  </div>
  {sss}
  <div class="cta"><h2>{e(cta["baslik"])}</h2><p>{e(cta["metin"])}</p><a class="btn b-main js-wa" href="/#iletisim">{WA_SVG}WhatsApp'tan Teklif Alın</a></div>
  {etiket}
  {kaynak}
</div>
</article>
{ilgili_html}
"""
    sayfa += son(c)
    hedef = KOK / "blog" / m["slug"] / "index.html"
    hedef.parent.mkdir(parents=True, exist_ok=True)
    hedef.write_text(sayfa)


def kapak_uret(m):
    hedef = KOK / "blog" / m["slug"] / "kapak.png"
    if hedef.exists():
        return
    subprocess.run([sys.executable, str(KOK / "_tools" / "kapak.py"), "--beyaz", m["kapak"]["beyaz"], "--yesil", m["kapak"]["yesil"],
                    "--etiket", m["kategori"], "--cikti", str(hedef)], check=True)


def liste_sayfasi(hepsi, c):
    kategoriler = []
    for m in hepsi:
        if m["kategori"] not in kategoriler:
            kategoriler.append(m["kategori"])
    filt = '<div class="filt" role="group" aria-label="Kategoriler"><button class="on" data-f="">Tümü</button>' + "".join(
        f'<button data-f="{e(k)}">{e(k)}</button>' for k in kategoriler) + "</div>"
    ld = [{"@context": "https://schema.org", "@type": "Blog", "name": "Move to Social Blog", "url": SITE + "/blog/", "inLanguage": "tr-TR",
           "blogPost": [{"@type": "BlogPosting", "headline": m["baslik"], "url": f"{SITE}/blog/{m['slug']}/", "datePublished": m["tarih"]} for m in hepsi]}]
    sayfa = bas("Sosyal Medya Blogu: Rehberler ve Veriler | Move to Social",
                "Move to Social blogu: sosyal medya istatistikleri, Instagram ve reklam rehberleri, sektöre özel içerik fikirleri. Kaynaklı, güncel ve uygulanabilir yazılar.",
                "/blog/", "/assets/og-gorsel.png", "Move to Social logosu", ld)
    sayfa += f"""<section class="bhero"><div class="wrap">
  <span class="badge">Blog</span>
  <h1>Sosyal medya için <span class="hl">rehberler ve veriler</span></h1>
  <p>İstatistikler, uygulanabilir taktikler ve sektöre özel fikirler. Her rakamın kaynağıyla.</p>
  {filt}
</div></section>
<section><div class="wrap"><div class="bgrid" id="liste">{"".join(kart(m, "h2") for m in hepsi)}</div></div></section>
"""
    js = ('const bs=document.querySelectorAll(".filt button"),ks=document.querySelectorAll("#liste .bcard");'
          'bs.forEach(b=>b.addEventListener("click",()=>{bs.forEach(x=>x.classList.toggle("on",x===b));'
          'ks.forEach(k=>{k.style.display=(!b.dataset.f||k.dataset.k===b.dataset.f)?"":"none"})}));')
    sayfa += son(c, js)
    (KOK / "blog").mkdir(exist_ok=True)
    (KOK / "blog" / "index.html").write_text(sayfa)


def ana_sayfa(hepsi):
    p = KOK / "index.html"
    s = p.read_text()
    kartlar = "".join(kart(m) for m in hepsi[:3])
    blok = f"""<!--BLOG-START-->
<section id="blog">
  <div class="wrap">
    <div class="head" data-r>
      <span class="badge"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 4h12l4 4v12H4Z"/><path d="M8 10h8M8 14h8M8 18h5"/></svg>Blog</span>
      <h2><span class="soft">Sosyal medyada</span><span class="hl">güncel kalın</span></h2>
      <p>Kaynaklı istatistikler, uygulanabilir rehberler ve sektöre özel fikirler.</p>
    </div>
    <div class="bgrid" data-r>{kartlar}</div>
    <div class="bmore" data-r><a class="btn b-ghost" href="/blog/">Tüm yazılar</a></div>
  </div>
</section>
<!--BLOG-END-->"""
    s = re.sub(r"<!--BLOG-START-->.*?<!--BLOG-END-->", lambda _: blok, s, flags=re.S)
    p.write_text(s)


def site_haritasi(hepsi):
    bugun = datetime.date.today().isoformat()
    son_yazi = hepsi[0]["tarih"] if hepsi else bugun
    satirlar = [f"  <url><loc>{SITE}/</loc><lastmod>{son_yazi}</lastmod></url>",
                f"  <url><loc>{SITE}/blog/</loc><lastmod>{son_yazi}</lastmod></url>"]
    for m in hepsi:
        satirlar.append(f"  <url><loc>{SITE}/blog/{m['slug']}/</loc><lastmod>{m.get('guncelleme', m['tarih'])}</lastmod></url>")
    (KOK / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                                     + "\n".join(satirlar) + "\n</urlset>\n")


def main():
    c = mts()
    hepsi = yukle()
    for m in hepsi:
        kapak_uret(m)
        yazi_sayfasi(m, hepsi, c)
    liste_sayfasi(hepsi, c)
    ana_sayfa(hepsi)
    site_haritasi(hepsi)
    print(f"{len(hepsi)} yazı derlendi.")


if __name__ == "__main__":
    main()
