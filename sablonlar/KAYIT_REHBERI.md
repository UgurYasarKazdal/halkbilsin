# Kayıt rehberi

Kayıtlar artık elle HTML yazılarak değil, `veri/kayitlar/<slug>.json` olarak girilir; `python3 araclar/uret.py` sayfayı üretir ve kuralları makinece denetler ([veri/README.md](../veri/README.md)). [kayit.html](kayit.html) yalnızca görsel şablon örneğidir. Yayından önce aşağıdaki kontrol listesi tamamlanır; tamamlanmayan kayıt yayımlanmaz.

## Zorunlu alanlar
1. **Kaynak durumu** (● okundu / ◐ ikincil / ○ doğrulanmadı) — başlığın üstünde, yazıyla birlikte.
2. **Resmî başlık, tür, sayı, kurum.**
3. **Dört tarih** ayrı ayrı: kabul, Resmî Gazete'de yayım, yürürlük, geçerlilik. Bilinmeyen tarih "bilinmiyor"; tahmin yok. Yürürlük ve geriye etki için madde numarası.
4. **Kaynak bağlantısı + okunma tarihi.** Birincil kaynak (Resmî Gazete, TBMM, kurum sayfası) tercih edilir.
5. **Düzeltme notları** bölümü (boş olsa da görünür).

## Koşullu alan
- **Şu an kapalı:** `veri/kisitlar.json` içinde `eylem_bolumu: false`; üretici eylemli kaydı reddeder. Hukuki inceleme (Avukatlık Kanunu m.35, TBK m.115) bitmeden açılmaz.
- **"Ne yapmanız gerekebilir"** yalnızca kaynak durumu ● olduğunda. Her madde için madde numarası; tavsiye dili ("yapın", "mutlaka") yok; "istenmektedir", "öngörülmektedir" gibi metne bağlı ifadeler.

## Dil
- "Siz" dili, kısa cümle, günlük sözcük; kısaltmanın açılımı ilk geçtiği yerde.
- Nötr fiiller: teklif verdi, oy kullandı, kabul edildi, oylandı, kabul edilmedi. Kullanılmayacaklar: reddetti, engelledi, savundu ve benzeri yargı fiilleri.
- Parti rengi, puan, sıralama, "karne" yok. Sayılar bağlamsız gösterilmez.

## Kontrol listesi (yayından önce)
- [ ] Metni resmî kaynaktan ben okudum (haberden değil).
- [ ] Dört tarih kaynakta karşılığıyla eşleşti; madde numaraları doğru.
- [ ] "Ne yapmanız gerekebilir" maddelerinin her birinde madde no var.
- [ ] Yargı fiili, tavsiye dili ve siyasi çağrışım yok.
- [ ] İkinci bir kişi (proje sahibi ya da uzman) tarihleri ve maddeleri metinle karşılaştırdı.
- [ ] Bağlantılar açılıyor; sayfa dar ekranda ve koyu temada okunuyor.
- [ ] `sitemap.xml`'e eklendi; `noindex` kaldırıldı.

## Düzeltme
Hata bildirimi → kaynakla kontrol → doğrulanırsa düzeltilir ve "Düzeltme notları"na **tarihiyle** eklenir. Eski ifade sessizce silinmez.
