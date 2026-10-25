# Kayıt verisi

Her kayıt `veri/kayitlar/<slug>.json` dosyasıdır. `python3 araclar/uret.py` kayıtları doğrular ve `kayitlar/` altında HTML üretir; `sitemap.xml` de aynı komutla güncellenir.

## Önemli: bu klasör herkese açıktır
Cloudflare Pages tüm depoyu yayımlar; `veri/kayitlar/*.json` dosyaları `halkbilsin.tr/veri/kayitlar/...` adresinden okunabilir (açık veri olarak bilerek). Bu yüzden:

- **Taslaklar bu depoya konmaz.** Taslak ve henüz kontrol edilmemiş kayıtlar özel depoda (`gulnia-ic/halkbilsin/`) hazırlanır; ikinci kontrolden geçince buraya `yayinda: true` ile taşınır.
- `yayinda: false` kaydın sayfası üretilmez, ama JSON dosyası yine de açıktır; bu yüzden yalnızca yayına hazır kayıtları buraya koyun.

## Alanlar
| Alan | Zorunlu | Açıklama |
|---|---|---|
| `slug` | evet | Dosya adıyla aynı; küçük harf, rakam, tire |
| `baslik`, `tur`, `kurum` | evet | Resmî başlık; Kanun/Yönetmelik/Karar; yayımlayan |
| `kaynak_durumu` | evet | `tam` (● okundu), `yarim` (◐ ikincil), `bos` (○ doğrulanmadı) |
| `tarihler` | evet | `kabul`, `rg_yayim`, `yururluk`, `gecerlilik`; her biri `{"tur": ...}` |
| `kimi` | hayır | Listeden: kiracı, ev sahibi, esnaf, veli, öğrenci, emekli, ... |
| `ozet` | evet | En çok 3 cümle, en çok 500 karakter, yargı yok |
| `eylemler` | hayır | Yalnızca `tam` iken; her biri `{metin, madde}` |
| `kaynaklar` | evet | `{baslik, url (https), okunma_tarihi, birincil}`; `tam` için en az bir `birincil: true` |
| `ilk_yayim` | `yayinda: true` için | `YYYY-AA-GG`; bir kez yazılır, sonradan değişmez |
| `son_guncelleme` | hayır | `YYYY-AA-GG`; `ilk_yayim` ve son düzeltme tarihinden önce olamaz; yoksa ilk yayım tarihi gösterilir |
| `duzeltmeler` | hayır | `{tarih, not, eski, yeni}`; eski ve yeni ifade birlikte gösterilir, eski ifade silinmez |
| `ikinci_kontrol` | `yayinda: true` için | `{tarih}` (kişi adı yazılmaz) |
| `yayinda` | evet | `true` ise sayfa üretilir |

### Tarih türleri
- `kabul`: `tarih` | `bilinmiyor`
- `rg_yayim`: `tarih` (+ `sayi` zorunlu) | `henuz_yok` | `bilinmiyor`
- `yururluk`: `tarih` (+ `madde` zorunlu) | `yayim_tarihinde` | `bilinmiyor`
- `gecerlilik`: `tarih` (+ `madde` zorunlu) | `yok` | `bilinmiyor`

Tarihler `YYYY-AA-GG` yazılır. Bilinmeyen tarih tahmin edilmez, `bilinmiyor` yazılır.

## Makinece denetlenen kurallar
Kayıt reddedilir: kaynak durumu `tam` olup birincil kaynak yoksa · `eylemler` var ama durum `tam` değilse · eylemde madde numarası yoksa · metinde yargı fiili ("reddetti", "engelledi", "savundu"...) ya da emir dili ("mutlaka", "yapın"...) varsa · metinde kişisel veri kalıbı (11 haneli TC kimlik no benzeri sayı, telefon, e-posta, IBAN) varsa · düzeltmede eski/yeni ifade yoksa · `yayinda: true` iken `ilk_yayim` yoksa · tarih geçersizse · Resmî Gazete yayımı sayısız ise · `yayinda: true` iken ikinci kontrol yoksa.

## Komutlar
```bash
python3 araclar/uret.py --kontrol           # yalnızca doğrula
python3 araclar/uret.py                     # doğrula + üret
python3 -m unittest discover -s araclar -v  # testler
```
