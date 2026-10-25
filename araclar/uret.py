#!/usr/bin/env python3
"""Halk Bilsin kayıt üreticisi.

veri/kayitlar/*.json dosyalarını doğrular ve kayitlar/ altında HTML üretir.
Yalnızca standart kütüphane kullanır. Çıktı belirlidir (zaman damgası yok).

Kullanım:
  python3 araclar/uret.py            # doğrula + üret
  python3 araclar/uret.py --kontrol  # yalnızca doğrula (hata varsa 1 ile çıkar)

Kurallar sablonlar/KAYIT_REHBERI.md ile aynıdır; burada makinece denetlenir.
"""
import argparse
import datetime as dt
import html
import json
import re
import sys
from pathlib import Path

DURUMLAR = {
    "tam": "Resmî metinden okundu",
    "yarim": "İkincil kaynak",
    "bos": "Doğrulanmadı",
}
AYLAR = ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz",
         "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"]
TARIH_ALANLARI = {
    # alan: (başlık, izinli türler)
    "kabul": ("Kabul", {"tarih", "bilinmiyor"}),
    "rg_yayim": ("Resmî Gazete’de yayım", {"tarih", "henuz_yok", "bilinmiyor"}),
    "yururluk": ("Yürürlük", {"tarih", "yayim_tarihinde", "bilinmiyor"}),
    "gecerlilik": ("Geçerlilik", {"tarih", "yok", "bilinmiyor"}),
}
TUR_METNI = {
    "bilinmiyor": "Bilinmiyor",
    "henuz_yok": "Henüz yok",
    "yayim_tarihinde": "Yayım tarihinde",
    "yok": "Yok",
}
KIMI = {
    "kiracı", "ev sahibi", "esnaf", "veli", "öğrenci", "emekli", "çalışan",
    "işveren", "yatırım fonu sahibi", "sürücü", "çiftçi", "engelli",
    "yeni anne-baba", "tüketici",
}
# Yargı taşıyan fiiller ve tavsiye/emir dili (kök eşleşmesi, küçük harfle)
YASAKLI = [
    "reddetti", "engelledi", "savundu", "skandal", "rezalet", "fiyasko",
    "mutlaka", "kesinlikle", "sakın", "yapın", "yapınız", "etmeyin", "gidin",
    "başvurun", "ödeyin",
]
KISIT_VARSAYILAN = {"eylem_bolumu": False, "temsilci_verisi": False, "bulten": False}
KISISEL_VERI = [
    ("TC kimlik numarası benzeri 11 haneli sayı", re.compile(r"(?<!\d)[1-9]\d{10}(?!\d)")),
    ("telefon numarası", re.compile(r"(?<!\d)(?:\+?90[\s.-]?)?\(?0?5\d{2}\)?[\s.-]?\d{3}[\s.-]?\d{2}[\s.-]?\d{2}(?!\d)")),
    ("e-posta adresi", re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+")),
    ("IBAN", re.compile(r"\bTR\d{2}(?:\s?\d{4}){5}\s?\d{2}\b", re.I)),
]
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
ISO_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def tr_kucuk(s):
    return s.replace("İ", "i").replace("I", "ı").lower()


def iso(s):
    if not isinstance(s, str) or not ISO_RE.match(s):
        raise ValueError(f"geçersiz tarih biçimi: {s!r} (YYYY-AA-GG olmalı)")
    return dt.date.fromisoformat(s)


def tarih_yaz(s):
    d = iso(s)
    return f"{d.day} {AYLAR[d.month - 1]} {d.year}"


def kisisel_veri_bul(metin):
    return [ad for ad, rx in KISISEL_VERI if rx.search(metin)]


def yasakli_bul(metin):
    k = tr_kucuk(metin)
    return [w for w in YASAKLI if w in k]


def dogrula(kayit, ad="kayıt", kisitlar=None):
    """Hata listesi döndürür; boşsa kayıt geçerlidir.

    kisitlar verilmezse en kısıtlı varsayılan uygulanır (eylem bölümü kapalı).
    """
    kisitlar = KISIT_VARSAYILAN if kisitlar is None else kisitlar
    h = []
    e = h.append
    if not isinstance(kayit, dict):
        return [f"{ad}: kök nesne olmalı"]
    zorunlu = ["slug", "baslik", "tur", "kurum", "kaynak_durumu", "tarihler",
               "ozet", "kaynaklar", "yayinda"]
    for z in zorunlu:
        if z not in kayit:
            e(f"{ad}: zorunlu alan eksik: {z}")
    if h:
        return h
    slug = kayit["slug"]
    if not isinstance(slug, str) or not SLUG_RE.match(slug):
        e(f"{ad}: slug küçük harf, rakam ve tire içermeli")
    for a in ("baslik", "tur", "kurum", "ozet"):
        if not isinstance(kayit[a], str) or not kayit[a].strip():
            e(f"{ad}: {a} boş olamaz")
    durum = kayit["kaynak_durumu"]
    if durum not in DURUMLAR:
        e(f"{ad}: kaynak_durumu {sorted(DURUMLAR)} içinden biri olmalı")

    # tarihler
    t = kayit["tarihler"]
    if not isinstance(t, dict):
        e(f"{ad}: tarihler nesne olmalı")
        t = {}
    for alan, (_, izinli) in TARIH_ALANLARI.items():
        v = t.get(alan)
        if not isinstance(v, dict) or "tur" not in v:
            e(f"{ad}: tarihler.{alan} eksik (tur zorunlu; bilinmiyorsa 'bilinmiyor')")
            continue
        if v["tur"] not in izinli:
            e(f"{ad}: tarihler.{alan}.tur {sorted(izinli)} içinden biri olmalı")
            continue
        if v["tur"] == "tarih":
            try:
                iso(v.get("tarih"))
            except ValueError as x:
                e(f"{ad}: tarihler.{alan}: {x}")
        if alan == "rg_yayim" and v["tur"] == "tarih" and not v.get("sayi"):
            e(f"{ad}: tarihler.rg_yayim için Resmî Gazete sayısı ('sayi') zorunlu")
        if alan in ("yururluk", "gecerlilik") and v["tur"] == "tarih" and not v.get("madde"):
            e(f"{ad}: tarihler.{alan} için madde numarası ('madde') zorunlu")
    try:
        k, r = t["kabul"], t["rg_yayim"]
        if k["tur"] == "tarih" and r["tur"] == "tarih" and iso(k["tarih"]) > iso(r["tarih"]):
            e(f"{ad}: kabul tarihi Resmî Gazete yayımından sonra olamaz")
        if r["tur"] == "henuz_yok" and t["yururluk"]["tur"] == "tarih" and not t["yururluk"].get("madde"):
            e(f"{ad}: yayım yokken yürürlük tarihi madde numarasıyla desteklenmeli")
    except (KeyError, ValueError, TypeError):
        pass

    # kimi
    for x in kayit.get("kimi", []):
        if x not in KIMI:
            e(f"{ad}: bilinmeyen 'kimi' değeri: {x!r} (izinli: {sorted(KIMI)})")

    # kaynaklar
    kaynaklar = kayit["kaynaklar"]
    if not isinstance(kaynaklar, list) or not kaynaklar:
        e(f"{ad}: en az bir kaynak zorunlu")
        kaynaklar = []
    birincil = 0
    for i, s in enumerate(kaynaklar):
        if not isinstance(s, dict):
            e(f"{ad}: kaynaklar[{i}] nesne olmalı")
            continue
        if not str(s.get("url", "")).startswith("https://"):
            e(f"{ad}: kaynaklar[{i}].url https:// ile başlamalı")
        if not s.get("baslik"):
            e(f"{ad}: kaynaklar[{i}].baslik zorunlu")
        try:
            iso(s.get("okunma_tarihi"))
        except ValueError as x:
            e(f"{ad}: kaynaklar[{i}].okunma_tarihi: {x}")
        if s.get("birincil") is True:
            birincil += 1
    if durum == "tam" and birincil == 0:
        e(f"{ad}: 'tam' durum için en az bir birincil (resmî) kaynak zorunlu")

    # eylemler: yalnızca tam
    eylemler = kayit.get("eylemler", [])
    if eylemler and not kisitlar.get("eylem_bolumu"):
        e(f"{ad}: 'ne yapmanız gerekebilir' bölümü hukuki inceleme tamamlanana kadar kapalı (veri/kisitlar.json)")
    if eylemler and durum != "tam":
        e(f"{ad}: 'ne yapmanız gerekebilir' yalnızca kaynak_durumu 'tam' iken yazılır")
    for i, ey in enumerate(eylemler):
        if not isinstance(ey, dict) or not ey.get("metin") or not ey.get("madde"):
            e(f"{ad}: eylemler[{i}] için metin ve madde numarası zorunlu")

    # dil denetimi
    metinler = [kayit["baslik"], kayit["ozet"]]
    metinler += [ey.get("metin", "") for ey in eylemler if isinstance(ey, dict)]
    metinler += [d.get("not", "") for d in kayit.get("duzeltmeler", []) if isinstance(d, dict)]
    metinler += [str(s.get("baslik", "")) for s in kayit.get("kaynaklar", []) if isinstance(s, dict)]
    metinler += [str(d.get(z, "")) for d in kayit.get("duzeltmeler", []) if isinstance(d, dict) for z in ("eski", "yeni")]
    for m in metinler:
        kv = kisisel_veri_bul(str(m))
        if kv:
            e(f"{ad}: metinde kişisel veri kalıbı ({', '.join(kv)}) — maskeleyin/çıkarın: {str(m)[:50]!r}")
    for m in metinler:
        bulunan = yasakli_bul(str(m))
        if bulunan:
            e(f"{ad}: yasak dil/yargı ifadesi {bulunan} — {str(m)[:60]!r}")
    if len(kayit["ozet"]) > 500:
        e(f"{ad}: özet 500 karakteri geçmemeli")
    if len(re.findall(r"[.!?](?:\s|$)", kayit["ozet"])) > 3:
        e(f"{ad}: özet en fazla üç cümle olmalı")

    # düzeltmeler
    for i, d in enumerate(kayit.get("duzeltmeler", [])):
        try:
            iso(d.get("tarih"))
        except (ValueError, AttributeError) as x:
            e(f"{ad}: duzeltmeler[{i}].tarih: {x}")
        if not (isinstance(d, dict) and d.get("not")):
            e(f"{ad}: duzeltmeler[{i}].not zorunlu")
        for z in ("eski", "yeni"):
            if not (isinstance(d, dict) and d.get(z)):
                e(f"{ad}: duzeltmeler[{i}].{z} zorunlu (eski ifade silinmez, eski/yeni birlikte gösterilir)")

    # tarih damgaları (m.4/4 gönüllü uygulama: değişmeyen ilk yayım / son güncelleme)
    ilk, son = kayit.get("ilk_yayim"), kayit.get("son_guncelleme")
    if kayit.get("yayinda") is True and not ilk:
        e(f"{ad}: yayinda=true için ilk_yayim zorunlu")
    for alan, v in (("ilk_yayim", ilk), ("son_guncelleme", son)):
        if v is not None:
            try:
                iso(v)
            except ValueError as x:
                e(f"{ad}: {alan}: {x}")
    try:
        if ilk and son and iso(son) < iso(ilk):
            e(f"{ad}: son_guncelleme ilk_yayim'dan önce olamaz")
        if kayit.get("duzeltmeler") and ilk:
            son_duz = max(iso(d["tarih"]) for d in kayit["duzeltmeler"])
            if iso(son or ilk) < son_duz:
                e(f"{ad}: son_guncelleme son düzeltme tarihinden önce olamaz")
    except (ValueError, KeyError, TypeError):
        pass

    # yayın koşulu
    if kayit["yayinda"] is True:
        ik = kayit.get("ikinci_kontrol")
        if not isinstance(ik, dict):
            e(f"{ad}: yayinda=true için ikinci_kontrol zorunlu")
        else:
            try:
                iso(ik.get("tarih"))
            except ValueError as x:
                e(f"{ad}: ikinci_kontrol.tarih: {x}")
    elif kayit["yayinda"] is not False:
        e(f"{ad}: yayinda true ya da false olmalı")
    return h


# ---------- HTML ----------
ANA_ACILIS = '<main id="icerik" class="wrap prose">'


def kabuk(kok):
    s = (kok / "yontem.html").read_text(encoding="utf-8")
    i = s.index(ANA_ACILIS)
    j = s.index("</main>")
    return s[:i], s[j:]


def ust_ayarla(ust, baslik, aciklama, noindex):
    ust = re.sub(r"<title>.*?</title>", f"<title>{html.escape(baslik)} — Halk Bilsin</title>", ust)
    for p in (r'(<meta name="description" content=")[^"]*(")',
              r'(<meta property="og:description" content=")[^"]*(")'):
        ust = re.sub(p, lambda m: m.group(1) + html.escape(aciklama, quote=True) + m.group(2), ust)
    ust = re.sub(r'(<meta property="og:title" content=")[^"]*(")',
                 lambda m: m.group(1) + html.escape(baslik + " — Halk Bilsin", quote=True) + m.group(2), ust)
    ust = ust.replace('<meta name="robots" content="noindex">\n', "")
    if noindex:
        ust = ust.replace('<meta charset="utf-8">', '<meta charset="utf-8">\n<meta name="robots" content="noindex">', 1)
    return ust


def tarih_hucre(alan, v):
    baslik = TARIH_ALANLARI[alan][0]
    if v["tur"] == "tarih":
        metin = tarih_yaz(v["tarih"])
        ek = []
        if v.get("sayi"):
            ek.append(f"sayı {v['sayi']}")
        if v.get("madde"):
            m = str(v["madde"])
            ek.append(f"madde {m}" if m.isdigit() else m)
        if ek:
            metin += f" ({', '.join(ek)})"
    else:
        metin = TUR_METNI[v["tur"]]
    sinif = ' class="warn"' if v["tur"] in ("henuz_yok", "bilinmiyor") else ""
    return (f"<div><dt>{html.escape(baslik)}</dt>"
            f"<dd{sinif}>{html.escape(metin)}</dd></div>")


def kayit_govdesi(k):
    E = html.escape
    sinif = {"tam": "tam", "yarim": "yarim", "bos": "bos"}[k["kaynak_durumu"]]
    out = [f'<p class="st"><span class="mk {sinif}" aria-hidden="true"></span>'
           f'{E(DURUMLAR[k["kaynak_durumu"]])}</p>']
    if k["kaynak_durumu"] != "tam":
        out.append('<p class="note">Resmî metin bu kayıt için henüz okunmadı; '
                   "“ne yapmanız gerekebilir” bölümü bu yüzden yoktur.</p>")
    out.append(f"<h1>{E(k['baslik'])}</h1>")
    out.append(f'<p class="meta">{E(k["tur"])} · {E(k["kurum"])}</p>')
    out.append("<h2>Tarihler</h2>")
    hucreler = "\n".join(tarih_hucre(a, k["tarihler"][a]) for a in TARIH_ALANLARI)
    out.append(f'<dl class="dates">\n{hucreler}\n</dl>')
    if k.get("kimi"):
        chips = "".join(f'<span class="chip tag">{E(x)}</span>' for x in k["kimi"])
        out.append("<h2>Kimi ilgilendirebilir</h2>")
        out.append(f'<div class="chips">{chips}</div>')
        out.append('<p class="note">Süzme bir yardımcıdır, güvence değildir. '
                   "Sizi ilgilendirmediğini düşünseniz bile metne bakın.</p>")
    out.append("<h2>Kısaca</h2>")
    out.append(f"<p>{E(k['ozet'])}</p>")
    if k["kaynak_durumu"] == "tam" and k.get("eylemler"):
        out.append("<h2>Ne yapmanız gerekebilir</h2>")
        li = "\n".join(f'<li>{E(ey["metin"])} <span class="note">(Madde {E(str(ey["madde"]))})</span></li>'
                       for ey in k["eylemler"])
        out.append(f"<ul>\n{li}\n</ul>")
    out.append("<h2>Kaynak</h2>")
    li = "\n".join(
        f'<li><a href="{E(s["url"], quote=True)}">{E(s["baslik"])}</a> — okunma tarihi: {E(tarih_yaz(s["okunma_tarihi"]))}</li>'
        for s in k["kaynaklar"])
    out.append(f"<ul>\n{li}\n</ul>")
    out.append("<h2>Düzeltme notları</h2>")
    if k.get("duzeltmeler"):
        li = "\n".join(f'<li><strong>{E(tarih_yaz(d["tarih"]))}:</strong> {E(d["not"])} '
                       f'<span class="note">Eski: “{E(d["eski"])}” · Yeni: “{E(d["yeni"])}”</span></li>'
                       for d in k["duzeltmeler"])
        out.append(f"<ul>\n{li}\n</ul>")
    out.append('<p class="note">'
               + ("Henüz düzeltme yok. " if not k.get("duzeltmeler") else "")
               + 'Hata için: <a href="mailto:iletisim@halkbilsin.tr">iletisim@halkbilsin.tr</a>. '
               '<a href="/yontem.html">Yöntemimiz</a>.</p>')
    damga = []
    if k.get("ilk_yayim"):
        damga.append(f"İlk yayım: {tarih_yaz(k['ilk_yayim'])}")
        damga.append(f"Son güncelleme: {tarih_yaz(k.get('son_guncelleme') or k['ilk_yayim'])}")
    if k.get("ikinci_kontrol"):
        damga.append(f"İkinci kontrol: {tarih_yaz(k['ikinci_kontrol']['tarih'])}")
    if damga:
        out.append(f'<p class="note">{E(" · ".join(damga))}.</p>')
    return "\n".join(out)



def deneyin_govdesi(kayitlar):
    """Ana sayfadaki 'Deneyin' bölümünün içini üretir (yalnızca yayında olanlardan)."""
    E = html.escape
    yay = [k for k in kayitlar if k.get("yayinda") is True]
    if not yay:
        return ('<h2 id="deneyin-baslik">Nasıl çalışıyor</h2>\n'
                '<p class="lead narrow">Henüz yayımlanmış kayıt yok; ilk kayıtlar hazırlanıyor.</p>')

    def rg_metin(k):
        v = k["tarihler"]["rg_yayim"]
        if v["tur"] == "tarih":
            return "Resmî Gazete: " + tarih_yaz(v["tarih"])
        return "Resmî Gazete: " + TUR_METNI[v["tur"]].lower()

    def anahtar(k):
        v = k["tarihler"]["rg_yayim"]
        return v["tarih"] if v["tur"] == "tarih" else "9999-99-99"

    sirali = sorted(yay, key=anahtar, reverse=True)
    kimiler = sorted({x for k in yay for x in k.get("kimi", [])})
    chips = "\n".join(
        f'<button type="button" class="chip secim" data-kimi="{E(x)}" aria-pressed="false">{E(x)}</button>'
        for x in kimiler)
    li = []
    for k in sirali:
        s = k["kaynak_durumu"]
        tarihler = "\n".join(tarih_hucre(alan, k["tarihler"][alan]) for alan in TARIH_ALANLARI)
        kimi = ", ".join(k.get("kimi", []))
        li.append(
            f'<li data-kimi="{E("|".join(k.get("kimi", [])))}">'
            f'<p class="st"><span class="mk {s}" aria-hidden="true"></span>{E(DURUMLAR[s])}</p>\n'
            f'<h3><a href="/kayitlar/{E(k["slug"])}.html">{E(k["baslik"])}</a></h3>\n'
            f'<dl class="dates">\n{tarihler}\n</dl>\n'
            f'<p class="note">Kimi ilgilendirebilir: {E(kimi)} · '
            f'<a href="/kayitlar/{E(k["slug"])}.html">Özet, kaynak ve ayrıntı</a></p></li>')
    n = len(sirali)
    return ('<h2 id="deneyin-baslik">Nasıl çalışıyor</h2>\n'
            '<p class="lead narrow">Profilinizi seçin; sizi ilgilendiren kayıtlar, tarihleri ve kaynağıyla çıksın. '
            'Ad ya da kimlik numarası sormayız; seçiminiz tarayıcınızda kalır, hiçbir yere gönderilmez.</p>\n'
            '<h3 class="adim">1 · Size uyanları işaretleyin</h3>\n'
            '<p class="note">Birden fazla seçebilirsiniz.</p>\n'
            '<div class="chips" role="group" aria-label="Profilinizi seçin">\n' + chips + '\n</div>\n'
            '<h3 class="adim">2 · Sizi ilgilendiren kayıtlar</h3>\n'
            '<p id="deneyin-bos" class="note" hidden>Henüz seçim yapmadınız; yukarıdan durumunuzu işaretleyin.</p>\n'
            '<ul class="kayit-listesi deneyin-liste">\n' + "\n".join(li) + '\n</ul>\n'
            '<p id="deneyin-sayac" class="note" role="status" aria-live="polite"></p>\n'
            f'<p class="note">Şu an {n} kayıt yayında; kapsam henüz dar. '
            '<a href="/kayitlar/">Tüm kayıtlar</a>.</p>')


def varliklari_surumle(kok, yaz=True):
    """style.css ve suz.js bağlantılarına içerik özeti ekler (?v=xxxxxxxx).

    Tarayıcı ve ara önbellekler dosya adını anahtar aldığı için, içerik
    değişince adres de değişir ve bayat stil/JS kalmaz.
    """
    import hashlib
    surumler = {}
    for ad in ("style.css", "suz.js"):
        p = kok / ad
        if p.exists():
            surumler[ad] = hashlib.sha256(p.read_bytes()).hexdigest()[:8]
    if not surumler:
        return
    hedefler = list(kok.glob("*.html"))
    if (kok / "kayitlar").exists():
        hedefler += list((kok / "kayitlar").glob("*.html"))
    for hp in hedefler:
        s = hp.read_text(encoding="utf-8")
        y = s
        for ad, hv in surumler.items():
            y = re.sub(r"(/?)" + re.escape(ad) + r"(\?v=[0-9a-f]{8})?",
                       lambda m, ad=ad, hv=hv: m.group(1) + ad + "?v=" + hv, y)
        if yaz and y != s:
            hp.write_text(y, encoding="utf-8")


DENEYIN_BASLA = "<!-- deneyin:basla -->"
DENEYIN_BITIR = "<!-- deneyin:bitir -->"


def deneyin_yerlestir(kok, kayitlar, yaz=True):
    """index.html'deki işaretçilerin arasını doldurur; işaretçi yoksa dokunmaz."""
    yol = kok / "index.html"
    if not yol.exists():
        return False
    s = yol.read_text(encoding="utf-8")
    if DENEYIN_BASLA not in s or DENEYIN_BITIR not in s:
        return False
    bas = s.index(DENEYIN_BASLA) + len(DENEYIN_BASLA)
    bit = s.index(DENEYIN_BITIR)
    yeni = s[:bas] + "\n" + deneyin_govdesi(kayitlar) + "\n" + s[bit:]
    if yaz and yeni != s:
        yol.write_text(yeni, encoding="utf-8")
    return True


def liste_govdesi(kayitlar):
    E = html.escape
    if not kayitlar:
        return ('<p class="eyebrow">Kayıtlar</p>\n<h1>Kayıtlar</h1>\n'
                '<p class="lead narrow">Henüz yayımlanmış kayıt yok. İlk kayıt, resmî metin okunup '
                "kontrol edildikten sonra burada yayımlanacak; hazır olmayan içeriği göstermiyoruz.</p>\n"
                '<p>Nasıl hazırlayacağımızı <a href="/yontem.html">Yöntem</a> sayfasında okuyabilirsiniz.</p>')
    li = []
    for k in kayitlar:
        sinif = k["kaynak_durumu"]
        li.append(f'<li><p class="st"><span class="mk {sinif}" aria-hidden="true"></span>'
                  f'{E(DURUMLAR[sinif])}</p>'
                  f'<h2><a href="/kayitlar/{E(k["slug"])}.html">{E(k["baslik"])}</a></h2>'
                  f'<p class="note">{E(k["tur"])} · {E(k["kurum"])}</p></li>')
    return ('<p class="eyebrow">Kayıtlar</p>\n<h1>Kayıtlar</h1>\n'
            '<ul class="kayit-listesi">\n' + "\n".join(li) + "\n</ul>")


def sirala_anahtari(k):
    for alan in ("rg_yayim", "kabul"):
        v = k["tarihler"][alan]
        if v["tur"] == "tarih":
            return v["tarih"]
    return "0000-00-00"


STATIK = ["", "yontem.html", "gizlilik.html"]


def sitemap(kayitlar):
    urls = ["https://halkbilsin.tr/" + p for p in STATIK]
    if kayitlar:
        urls.append("https://halkbilsin.tr/kayitlar/")
        urls += [f"https://halkbilsin.tr/kayitlar/{k['slug']}.html" for k in kayitlar]
    govde = "\n".join(f"<url><loc>{u}</loc></url>" for u in urls)
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + govde + "\n</urlset>\n")


def kisitlari_oku(kok):
    p = kok / "veri" / "kisitlar.json"
    if not p.exists():
        return dict(KISIT_VARSAYILAN)  # dosya yoksa en kısıtlı hâl
    k = dict(KISIT_VARSAYILAN)
    k.update({a: b is True for a, b in json.loads(p.read_text(encoding="utf-8")).items() if a in KISIT_VARSAYILAN})
    return k


def yukle(kok):
    kisitlar = kisitlari_oku(kok)
    klasor = kok / "veri" / "kayitlar"
    kayitlar, hatalar = [], []
    slugs = set()
    for p in sorted(klasor.glob("*.json")):
        try:
            k = json.loads(p.read_text(encoding="utf-8"))
        except json.JSONDecodeError as x:
            hatalar.append(f"{p.name}: JSON hatası: {x}")
            continue
        h = dogrula(k, p.name, kisitlar)
        if not h and k["slug"] != p.stem:
            h.append(f"{p.name}: slug dosya adıyla ({p.stem}) aynı olmalı")
        if not h and k["slug"] in slugs:
            h.append(f"{p.name}: yinelenen slug")
        hatalar += h
        if not h:
            slugs.add(k["slug"])
            kayitlar.append(k)
    return kayitlar, hatalar


def uret(kok, yaz=True):
    kayitlar, hatalar = yukle(kok)
    if hatalar:
        return hatalar, [], []
    yayindakiler = sorted((k for k in kayitlar if k["yayinda"]), key=sirala_anahtari, reverse=True)
    taslaklar = [k["slug"] for k in kayitlar if not k["yayinda"]]
    if not yaz:
        return [], yayindakiler, taslaklar
    ust, alt = kabuk(kok)
    hedef = kok / "kayitlar"
    hedef.mkdir(exist_ok=True)
    beklenen = {"index.html"}
    for k in yayindakiler:
        aciklama = k["ozet"][:160]
        sayfa = (ust_ayarla(ust, k["baslik"], aciklama, noindex=False)
                 + ANA_ACILIS + "\n" + kayit_govdesi(k) + "\n" + alt)
        (hedef / f"{k['slug']}.html").write_text(sayfa, encoding="utf-8")
        beklenen.add(f"{k['slug']}.html")
    liste = (ust_ayarla(ust, "Kayıtlar",
                        "Halk Bilsin kayıtları." if yayindakiler else "Halk Bilsin kayıtları. Henüz yayımlanmış kayıt yok.",
                        noindex=not yayindakiler)
             + ANA_ACILIS + "\n" + liste_govdesi(yayindakiler) + "\n" + alt)
    (hedef / "index.html").write_text(liste, encoding="utf-8")
    for p in hedef.glob("*.html"):
        if p.name not in beklenen:
            p.unlink()  # yayından kaldırılan kayıt sayfası
    (kok / "sitemap.xml").write_text(sitemap(yayindakiler), encoding="utf-8")
    deneyin_yerlestir(kok, yayindakiler, yaz=yaz)
    if yaz:
        varliklari_surumle(kok, yaz=yaz)
    return [], yayindakiler, taslaklar


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--kontrol", action="store_true", help="yalnızca doğrula")
    ap.add_argument("--kok", default=str(Path(__file__).resolve().parent.parent))
    a = ap.parse_args(argv)
    hatalar, yayin, taslak = uret(Path(a.kok), yaz=not a.kontrol)
    if hatalar:
        print("HATA:", *hatalar, sep="\n  ")
        return 1
    print(f"Tamam: {len(yayin)} yayında, {len(taslak)} taslak.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
