# Move to Social blog — yazı kuralları

Bu dosya hem elle yazılan hem de zamanlanmış görevle otomatik yayınlanan yazılar için geçerlidir.
Yazılar onay beklemeden yayına girer; o yüzden kurallar eksiksiz uygulanmalıdır.

## Yeni yazı nasıl eklenir
1. `_kaynak/<slug>.json` (bilgiler) ve `_kaynak/<slug>.html` (gövde) oluştur. Mevcut yazıları örnek al.
2. `python3 _tools/blog.py` çalıştır (Chrome yolu gerekirse `CHROME=/usr/bin/google-chrome`).
   Kapak, yazı sayfası, /blog listesi, ana sayfadaki son 3 yazı ve sitemap kendiliğinden üretilir.
3. Betik uyarı verirse (başlık, meta, özet uzunluğu) düzelt ve tekrar çalıştır.
4. Sayfayı tarayıcıda masaüstü (1440) ve mobil (390) genişlikte kontrol et: taşma, kırık link, konsol hatası olmamalı.
5. İlgili eski yazılardan en az birine yeni yazıya giden bir iç link ekle (gövdede, doğal bir cümleyle) ve yeniden derle.
6. `main` dalına commit + push. Site 1-2 dakikada yayına girer.

## İçerik kuralları
- Dil: Türkçe. Yazar: "Move to Social".
- Kitle: her sektörden işletme sahipleri ve pazarlama sorumluları. Gayrimenkul yalnızca sektörlerden biridir; blog ona ağırlık vermez.
- Konu türleri dönüşümlü: (a) satın almaya yakın aramalar (fiyat, ajans, reklam bütçesi), (b) sektöre özel rehberler (restoran, klinik, güzellik, e-ticaret, eğitim, otomotiv, turizm, moda, inşaat, hukuk, spor, gayrimenkul...), (c) nasıl yapılır / platform rehberleri (Instagram, Reels, Meta reklam, TikTok, LinkedIn, Google), (d) veri / istatistik yazıları.
- Mevcut yazılarla aynı konuyu tekrar yazma; `_kaynak/` içindeki başlıkları kontrol et.
- Uzunluk: 900-1600 kelime arası, okunaklı, kısa paragraflar.

## SEO kuralları
- `baslik`: en fazla 60 karakter; odak kelime ilk 30 karakterde; başlık soruyu tekrarlamasın, cevabı/cevabın şeklini taşısın (rakam, süre, adım sayısı, net yargı); iki nokta üst üsteden sonra tek vaat; soru işaretiyle bitmesin; "bilmeniz gereken her şey / eksiksiz rehber / etkili yöntemle" gibi kalıplar yasak; başlıkta rakam varsa yıl da olsun.
- Odak kelime: başlıkta, `aciklama` (meta) içinde, en az bir `<h2>`'de ve gövdenin ilk paragrafında geçmeli.
- `aciklama` (meta açıklama): 155-165 karakter.
- `ozet`: en fazla 500 karakter; yazının başında "Kısaca" kutusunda görünür, soruya doğrudan cevap vermeli.
- `etiketler`: 5-8 etiket.
- `alt`: kapak için SEO uyumlu 2 ayrı alt metin (1. görselin alt'ı, 2. paylaşım önizlemesinin alt'ı).
- `sss`: 2-4 soru-cevap (Google'da SSS sonucu için).

## Görsel kuralları
- Kapak: `kapak.beyaz` (üst satır, beyaz) + `kapak.yesil` (alt satır, yeşil); her satır en fazla ~22 karakter. Logo ve kategori etiketi kendiliğinden eklenir. Fotoğraf yok.
- Gövdede en az 1 görsel öğe: `.stats` istatistik kartları ve/veya `.chart` çubuk grafik ve/veya `.steps` adım şeması.
- Çubuk grafikte `--w` yüzdesi = değer / en büyük değer × 100 (yuvarla). Her grafiğin altında `.src` ile kaynak linki.

## İstatistik kuralları (çok önemli)
- Her rakam yazı hazırlanırken web'de araştırılıp kaynağından doğrulanmalı. Kaynağı bulunamayan rakam yazıya girmez.
- Kaynak tercihi: resmi kurumlar, platformların kendi açıklamaları, DataReportal/We Are Social, akademik çalışmalar, bilinen araştırma şirketleri. Forum ve içerik çiftliği siteleri kaynak olmaz.
- Her rakamın hangi ülke, hangi tarih ve hangi örneklemden geldiği metinde belirtilmeli (ör. "ABD'de yapılan anket").
- Tüm kaynaklar `kaynaklar` listesinde linkli olmalı; metin içinde de ilgili yerde link verilebilir.
- Fiyat yazılarında kesin fiyat uydurma; aralık ya da belirleyen faktörleri anlat, varsa resmi kaynaktan doğrula.

## Sosyal medya seti (her yazı için zorunlu)
Blog yazısıyla birlikte aynı konudan bir Instagram carousel'i ve bir LinkedIn paylaşımı hazırlanır.
1. `_sosyal/<slug>/set.json` yaz (mevcut setleri örnek al). Slayt tipleri: `kapak`, `rakam`, `madde`, `liste`, `cta`.
   - 6-8 slayt: ilk slayt `kapak`, son slayt `cta`. Arada yazının en çarpıcı rakamları ve ana fikirleri.
   - Slaytlarda yalnızca yazıda geçen, kaynağı doğrulanmış rakamlar; `rakam` slaytında `kaynak` zorunlu.
   - Kısa yaz: başlık 1-2 satır, liste en fazla 6 madde, madde başına tek satır. Betik "sığmıyor" uyarısı verirse metni kısalt.
   - Instagram açıklaması: kanca cümle, 2-3 kısa paragraf, "Kaydırın", blog adresi (movetosocial.com.tr/blog), "Kaydedin, ... lazım olacak" kapanışı; `hashtag` listesinde **tam 5** hashtag, biri #movetosocial.
   - LinkedIn metni: profesyonel ton, kanca + 3-5 madde + çıkarım + `{link}` (betik yazının adresiyle değiştirir) + 3 hashtag.
2. `python3 _tools/sosyal.py <slug>` çalıştır. Çıktılar: `instagram-carousel-01..NN.png` (1080x1350), `linkedin-carousel.pdf` (LinkedIn belge gönderisi), `instagram-aciklama.txt`, `linkedin-metin.txt`.
3. Slaytları tek tek aç ve bak: taşan, kesilen ya da üst üste binen yazı olmamalı.
4. Tüm dosyaları kullanıcıya tek tek gönder (ZIP değil). Her gönderide hangi platform için olduğunu yaz: "Instagram carousel", "LinkedIn belge gönderisi (PDF)", "Blog kapağı".

## İç link kuralları
- Gövdede en az 2 iç link: ilgili blog yazılarına (`/blog/<slug>/`) ve ilgili hizmete (`/#hizmetler`, `/#egitimler`, `/#sektorler`).
- `ilgili` alanına en alakalı 2-3 yazının slug'ını yaz (yoksa betik etiket ve kategoriye göre seçer).
- Yazı sonunda CTA kutusu ve WhatsApp butonu betikle otomatik eklenir.
