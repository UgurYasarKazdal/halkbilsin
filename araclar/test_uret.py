"""uret.py için testler. Çalıştırma: python3 -m unittest discover -s araclar -v

Buradaki kayıtlar SAHTEDİR ve yalnızca bellekte/geçici klasörde yaşar;
veri/kayitlar/ altına asla yazılmaz ve yayımlanmaz.
"""
import copy
import json
import shutil
import tempfile
import unittest
from pathlib import Path

import uret

KOK = Path(__file__).resolve().parent.parent
ACIK = {"eylem_bolumu": True, "temsilci_verisi": False, "bulten": False}

GECERLI = {
    "slug": "test-kaydi",
    "baslik": "Sahte Test Kanunu",
    "tur": "Kanun",
    "kurum": "Test Kurumu",
    "kaynak_durumu": "tam",
    "tarihler": {
        "kabul": {"tur": "tarih", "tarih": "2030-01-10"},
        "rg_yayim": {"tur": "tarih", "tarih": "2030-01-15", "sayi": "99999"},
        "yururluk": {"tur": "tarih", "tarih": "2030-02-01", "madde": "5"},
        "gecerlilik": {"tur": "yok"},
    },
    "kimi": ["kiracı"],
    "ozet": "Bu kayıt bir testtir. Gerçek bir düzenlemeyi anlatmaz.",
    "eylemler": [{"metin": "Madde 3 uyarınca bildirim yapılması öngörülmektedir.", "madde": "3"}],
    "kaynaklar": [{"baslik": "Test kaynağı", "url": "https://example.org/x",
                   "okunma_tarihi": "2030-01-16", "birincil": True}],
    "duzeltmeler": [],
    "ilk_yayim": "2030-01-17",
    "ikinci_kontrol": {"tarih": "2030-01-17"},
    "yayinda": True,
}


def varyant(**degisiklik):
    k = copy.deepcopy(GECERLI)
    for yol, deger in degisiklik.items():
        parcalar = yol.split("__")
        hedef = k
        for p in parcalar[:-1]:
            hedef = hedef[p]
        if deger is KALDIR:
            del hedef[parcalar[-1]]
        else:
            hedef[parcalar[-1]] = deger
    return k


KALDIR = object()


class Dogrulama(unittest.TestCase):
    def hata_var(self, kayit, parca):
        h = uret.dogrula(kayit, kisitlar=ACIK)
        self.assertTrue(any(parca in x for x in h), f"{parca!r} bekleniyordu, çıkan: {h}")

    def test_eylem_bolumu_varsayilan_olarak_kapali(self):
        h = uret.dogrula(GECERLI)  # kısıt verilmedi
        self.assertTrue(any("kapalı" in x for x in h), h)

    def test_kisit_dosyasi_yoksa_kapali(self):
        d = Path(tempfile.mkdtemp())
        try:
            self.assertFalse(uret.kisitlari_oku(d)["eylem_bolumu"])
        finally:
            shutil.rmtree(d)

    def test_depodaki_kisit_dosyasi_kapali(self):
        self.assertFalse(uret.kisitlari_oku(KOK)["eylem_bolumu"])
        self.assertFalse(uret.kisitlari_oku(KOK)["temsilci_verisi"])

    def test_gecerli_kayit_gecer(self):
        self.assertEqual(uret.dogrula(GECERLI, kisitlar=ACIK), [])

    def test_zorunlu_alan_eksik(self):
        self.hata_var(varyant(ozet=KALDIR), "zorunlu alan eksik: ozet")

    def test_tam_durum_birincil_kaynak_ister(self):
        k = varyant()
        k["kaynaklar"][0]["birincil"] = False
        self.hata_var(k, "birincil")

    def test_eylem_yalniz_tam_durumda(self):
        self.hata_var(varyant(kaynak_durumu="yarim"), "yalnızca kaynak_durumu 'tam'")

    def test_eylem_madde_numarasi_ister(self):
        k = varyant()
        k["eylemler"][0]["madde"] = ""
        self.hata_var(k, "madde numarası zorunlu")

    def test_yargi_fiili_reddedilir(self):
        self.hata_var(varyant(ozet="Parti X teklifi reddetti."), "yasak dil")

    def test_tavsiye_dili_reddedilir(self):
        k = varyant()
        k["eylemler"][0]["metin"] = "Mutlaka başvurun."
        self.hata_var(k, "yasak dil")

    def test_buyuk_I_harfi_ile_de_yakalanir(self):
        self.hata_var(varyant(ozet="MUTLAKA yapılmalı."), "yasak dil")

    def test_gecersiz_tarih(self):
        k = varyant()
        k["tarihler"]["kabul"]["tarih"] = "2030-13-45"
        self.hata_var(k, "kabul")

    def test_rg_yayimi_sayi_ister(self):
        k = varyant()
        del k["tarihler"]["rg_yayim"]["sayi"]
        self.hata_var(k, "('sayi')")

    def test_yururluk_madde_ister(self):
        k = varyant()
        del k["tarihler"]["yururluk"]["madde"]
        self.hata_var(k, "madde numarası")

    def test_kabul_yayimdan_sonra_olamaz(self):
        k = varyant()
        k["tarihler"]["kabul"]["tarih"] = "2030-03-01"
        self.hata_var(k, "kabul tarihi")

    def test_bilinmeyen_tarih_acikca_yazilir(self):
        k = varyant()
        k["tarihler"]["gecerlilik"] = {"tur": "bilinmiyor"}
        self.assertEqual(uret.dogrula(k, kisitlar=ACIK), [])

    def test_tarih_turu_alana_uygun_olmali(self):
        k = varyant()
        k["tarihler"]["kabul"] = {"tur": "yok"}
        self.hata_var(k, "tarihler.kabul.tur")

    def test_yayinda_ilk_yayim_ister(self):
        self.hata_var(varyant(ilk_yayim=KALDIR), "ilk_yayim zorunlu")

    def test_son_guncelleme_ilk_yayimdan_once_olamaz(self):
        self.hata_var(varyant(son_guncelleme="2029-12-01"), "ilk_yayim'dan önce")

    def test_son_guncelleme_duzeltmeden_once_olamaz(self):
        k = varyant(duzeltmeler=[{"tarih": "2030-03-01", "not": "Tarih düzeltildi.", "eski": "A", "yeni": "B"}])
        self.hata_var(k, "son düzeltme tarihinden önce")
        k["son_guncelleme"] = "2030-03-01"
        self.assertEqual(uret.dogrula(k, kisitlar=ACIK), [])

    def test_duzeltme_eski_ve_yeni_ister(self):
        k = varyant(duzeltmeler=[{"tarih": "2030-02-01", "not": "Düzeltildi."}], son_guncelleme="2030-02-01")
        self.hata_var(k, "eski")

    def test_tc_kimlik_benzeri_sayi_reddedilir(self):
        self.hata_var(varyant(ozet="Başvuran 12345678901 numaralıdır."), "kişisel veri")

    def test_telefon_reddedilir(self):
        for tel in ("0532 123 45 67", "+90 532 123 45 67", "05321234567"):
            self.hata_var(varyant(ozet=f"Arayın: {tel}."), "telefon")

    def test_eposta_reddedilir(self):
        self.hata_var(varyant(ozet="Yazın: ad.soyad@ornek.com"), "e-posta")

    def test_iban_reddedilir(self):
        self.hata_var(varyant(ozet="TR33 0006 1005 1978 6457 8413 26 hesabına."), "IBAN")

    def test_rg_sayisi_ve_madde_no_kisisel_veri_sanilmaz(self):
        k = varyant(ozet="Resmî Gazete sayı 33323, madde 12, kanun 7596.")
        self.assertEqual(uret.dogrula(k, kisitlar=ACIK), [])

    def test_kaynak_basliginda_kisisel_veri_reddedilir(self):
        k = varyant()
        k["kaynaklar"][0]["baslik"] = "İletişim 0532 123 45 67"
        self.hata_var(k, "telefon")

    def test_yayinda_ikinci_kontrol_ister(self):
        self.hata_var(varyant(ikinci_kontrol=KALDIR), "ikinci_kontrol")

    def test_taslak_ikinci_kontrol_istemez(self):
        k = varyant(yayinda=False)
        del k["ikinci_kontrol"]
        self.assertEqual(uret.dogrula(k, kisitlar=ACIK), [])

    def test_https_olmayan_kaynak(self):
        k = varyant()
        k["kaynaklar"][0]["url"] = "http://example.org"
        self.hata_var(k, "https")

    def test_ozet_uc_cumleyi_gecmez(self):
        self.hata_var(varyant(ozet="Bir. İki. Üç. Dört."), "üç cümle")

    def test_bilinmeyen_kimi(self):
        self.hata_var(varyant(kimi=["uydurma"]), "bilinmeyen 'kimi'")

    def test_slug_bicimi(self):
        self.hata_var(varyant(slug="Büyük Harf"), "slug")


class Uretim(unittest.TestCase):
    def setUp(self):
        self.kok = Path(tempfile.mkdtemp())
        for ad in ("yontem.html", "gizlilik.html", "sitemap.xml"):
            shutil.copy(KOK / ad, self.kok / ad)
        (self.kok / "veri" / "kayitlar").mkdir(parents=True)
        (self.kok / "veri" / "kisitlar.json").write_text(json.dumps(ACIK), encoding="utf-8")

    def tearDown(self):
        shutil.rmtree(self.kok)

    def yaz(self, k, ad=None):
        (self.kok / "veri" / "kayitlar" / f"{ad or k['slug']}.json").write_text(
            json.dumps(k, ensure_ascii=False), encoding="utf-8")

    def test_bos_durumda_liste_noindex_ve_dürüst(self):
        hatalar, yayin, _ = uret.uret(self.kok)
        self.assertEqual((hatalar, yayin), ([], []))
        s = (self.kok / "kayitlar" / "index.html").read_text(encoding="utf-8")
        self.assertIn("Henüz yayımlanmış kayıt yok", s)
        self.assertIn('content="noindex"', s)

    def test_taslak_yayimlanmaz(self):
        k = varyant(yayinda=False)
        del k["ikinci_kontrol"]
        self.yaz(k)
        hatalar, yayin, taslak = uret.uret(self.kok)
        self.assertEqual((hatalar, yayin, taslak), ([], [], ["test-kaydi"]))
        self.assertFalse((self.kok / "kayitlar" / "test-kaydi.html").exists())
        self.assertNotIn("test-kaydi", (self.kok / "sitemap.xml").read_text())

    def test_yayindaki_kayit_uretilir(self):
        self.yaz(GECERLI)
        hatalar, yayin, _ = uret.uret(self.kok)
        self.assertEqual(hatalar, [])
        s = (self.kok / "kayitlar" / "test-kaydi.html").read_text(encoding="utf-8")
        self.assertIn("Sahte Test Kanunu", s)
        self.assertIn("10 Ocak 2030", s)
        self.assertIn("sayı 99999", s)
        self.assertIn("madde 5", s)
        self.assertIn("İlk yayım: 17 Ocak 2030", s)
        self.assertIn("Son güncelleme: 17 Ocak 2030", s)
        self.assertIn("Ne yapmanız gerekebilir", s)
        self.assertNotIn('content="noindex"', s)
        self.assertIn("kayitlar/test-kaydi.html", (self.kok / "sitemap.xml").read_text())
        liste = (self.kok / "kayitlar" / "index.html").read_text(encoding="utf-8")
        self.assertNotIn("noindex", liste)

    def test_ikincil_kaynakta_eylem_bolumu_yok(self):
        k = varyant(kaynak_durumu="yarim")
        del k["eylemler"]
        k["kaynaklar"][0]["birincil"] = False
        self.yaz(k)
        uret.uret(self.kok)
        s = (self.kok / "kayitlar" / "test-kaydi.html").read_text(encoding="utf-8")
        self.assertNotIn("<h2>Ne yapmanız gerekebilir</h2>", s)
        self.assertIn("henüz okunmadı", s)

    def test_duzeltme_eski_yeni_gorunur(self):
        k = varyant(duzeltmeler=[{"tarih": "2030-02-01", "not": "Yürürlük tarihi düzeltildi.",
                                  "eski": "1 Şubat", "yeni": "1 Mart"}], son_guncelleme="2030-02-01")
        self.yaz(k)
        hatalar, _, _ = uret.uret(self.kok)
        self.assertEqual(hatalar, [])
        s = (self.kok / "kayitlar" / "test-kaydi.html").read_text(encoding="utf-8")
        self.assertIn("Eski: “1 Şubat” · Yeni: “1 Mart”", s)
        self.assertIn("Son güncelleme: 1 Şubat 2030", s)

    def test_deneyin_bolumu_uretilir(self):
        self.yaz(varyant())
        (self.kok / "index.html").write_text(
            "<html><body>\n<!-- deneyin:basla -->\n<!-- deneyin:bitir -->\n</body></html>",
            encoding="utf-8")
        hatalar, _, _ = uret.uret(self.kok)
        self.assertEqual(hatalar, [])
        s = (self.kok / "index.html").read_text(encoding="utf-8")
        self.assertIn('data-kimi="kiracı"', s)          # çip
        self.assertIn('aria-label="kiracı, 1 kayıt"', s)  # sayı rozeti
        self.assertIn('data-kimi="emekli"', s)            # kaydı olmayan durum da görünür
        self.assertIn('aria-label="emekli, henüz kayıt yok"', s)
        self.assertIn('aria-pressed="false"', s)
        self.assertIn('<li data-kimi="kiracı">', s)      # kayıt öğesi
        self.assertIn("Şu an 1 kayıt yayında", s)
        # kart, dört tarihi de taşımalı
        for alan in ("Kabul", "Resmî Gazete’de yayım", "Yürürlük", "Geçerlilik"):
            self.assertIn(f"<dt>{alan}</dt>", s)
        self.assertIn("Kimi ilgilendirebilir: kiracı", s)
        self.assertIn("1 · Size uyanları işaretleyin", s)
        self.assertIn('id="deneyin-bos"', s)
        # ikinci çalıştırma aynı çıktıyı vermeli (determinizm)
        uret.uret(self.kok)
        self.assertEqual(s, (self.kok / "index.html").read_text(encoding="utf-8"))

    def test_varlik_surumleme(self):
        self.yaz(varyant())
        (self.kok / "style.css").write_text("body{}", encoding="utf-8")
        (self.kok / "index.html").write_text(
            '<link rel="stylesheet" href="/style.css">\n<!-- deneyin:basla -->\n<!-- deneyin:bitir -->',
            encoding="utf-8")
        uret.uret(self.kok)
        s = (self.kok / "index.html").read_text(encoding="utf-8")
        self.assertRegex(s, r'/style\.css\?v=[0-9a-f]{8}')
        # ikinci çalıştırma kararlı olmalı
        uret.uret(self.kok)
        self.assertEqual(s, (self.kok / "index.html").read_text(encoding="utf-8"))

    def test_deneyin_isaretci_yoksa_dokunulmaz(self):
        self.yaz(varyant())
        (self.kok / "index.html").write_text("<html><body>sabit</body></html>", encoding="utf-8")
        uret.uret(self.kok)
        self.assertEqual("<html><body>sabit</body></html>",
                         (self.kok / "index.html").read_text(encoding="utf-8"))

    def test_html_kacislanir(self):
        self.yaz(varyant(baslik='<script>alert(1)</script> Kanunu'))
        uret.uret(self.kok)
        s = (self.kok / "kayitlar" / "test-kaydi.html").read_text(encoding="utf-8")
        self.assertNotIn("<script>alert", s)
        self.assertIn("&lt;script&gt;", s)

    def test_hatali_kayit_hicbir_sey_uretmez(self):
        self.yaz(varyant(ozet="Mutlaka yapın."))
        hatalar, yayin, _ = uret.uret(self.kok)
        self.assertTrue(hatalar)
        self.assertFalse((self.kok / "kayitlar").exists())

    def test_slug_dosya_adiyla_ayni_olmali(self):
        self.yaz(GECERLI, ad="baska-ad")
        hatalar, _, _ = uret.uret(self.kok)
        self.assertTrue(any("dosya adıyla" in h for h in hatalar))

    def test_yayindan_kalkan_sayfa_silinir(self):
        self.yaz(GECERLI)
        uret.uret(self.kok)
        k = varyant(yayinda=False)
        self.yaz(k)
        uret.uret(self.kok)
        self.assertFalse((self.kok / "kayitlar" / "test-kaydi.html").exists())

    def test_cikti_belirli_iki_calistirma_ayni(self):
        self.yaz(GECERLI)
        uret.uret(self.kok)
        a = (self.kok / "kayitlar" / "test-kaydi.html").read_text(encoding="utf-8")
        uret.uret(self.kok)
        b = (self.kok / "kayitlar" / "test-kaydi.html").read_text(encoding="utf-8")
        self.assertEqual(a, b)

    def test_kapali_kisitta_eylemli_kayit_reddedilir(self):
        (self.kok / "veri" / "kisitlar.json").write_text(json.dumps({"eylem_bolumu": False}), encoding="utf-8")
        self.yaz(GECERLI)
        hatalar, _, _ = uret.uret(self.kok)
        self.assertTrue(any("kapalı" in h for h in hatalar))

    def test_depodaki_gercek_veri_gecerli(self):
        hatalar, _, _ = uret.uret(KOK, yaz=False)
        self.assertEqual(hatalar, [])


if __name__ == "__main__":
    unittest.main()
