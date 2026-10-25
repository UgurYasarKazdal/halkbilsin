# Halk Bilsin — marka rehberi (v1)

Bu rehber, projenin amacıyla tutarlı olsun diye yazıldı: **iktidar ya da muhalefet fark etmez, vatandaşın yanında duran, yardımcı bir bilgi hizmeti.** Marka bu amaca hizmet ediyorsa vardır; süs olarak değil.

**Durum: v1.** TÜRKPATENT sorgusu ve renk/isim çağrışım testi yapılana kadar kesin değildir.

## Ne yaptık, ne yapmadık
- Hiçbir kurumun, partinin ya da mevcut bir ürünün görünümünü taklit etmedik. Kullandığımız uluslararası standartlar yöntemdir, görünüm değil: WCAG 2.2 AA, ISO 24495-1 (sade dil).
- Logo özgündür: yazı tipinden çizilmiş yazı logosu; "bilsin" sözcüğündeki iki noktası dolu ve boş daire.
- Tüm yazı tipleri açık lisanslıdır (SIL OFL 1.1), sitenin kendisinden sunulur; Google Fonts gibi dış bağlantı yoktur.

## Renk
| Rol | Açık | Koyu |
|---|---|---|
| Zemin | #F6F1E9 | #1A1714 |
| Yüzey (kart) | #FFFFFF | #2A2520 |
| Metin | #1F1D1A | #F2ECE2 |
| İkincil metin | #5C5750 | #B9B0A3 |
| Vurgu (toprak) | #7A4E2D | #D2A67E |
| Çizgi | #D9CCB9 | #4A4238 |

Toprak ve grafit tonları seçildi; çünkü kırmızı, turuncu, mavi, turkuaz ve yeşil-mor-sarı kombinasyonları Türkiye'de partilerle ilişkilendirilebilir. **[H]** Bu bir hipotezdir; çağrışım testiyle sınanmadı.

Ölçülen karşılaştırma oranları (WCAG, en az 4,5:1): metin/zemin 14,95 · vurgu/zemin 6,32 · ikincil/zemin 6,37 · koyu metin/zemin 15,19 · koyu vurgu/zemin 8,07. Düğme metni vurgu üzerinde 7,11 (açık) ve 8,07 (koyu).

## Durum işaretleri (anlam renkle taşınmaz)
| İşaret | Anlam |
|---|---|
| ● dolu | Resmî metinden okundu |
| ◐ yarım | İkincil kaynak |
| ○ boş | Doğrulanmadı |

İşaret her zaman yazıyla birlikte gösterilir (WCAG 1.4.1). Yeşil/kehribar/gri etiketler kaldırıldı: "yeşil = iyi, kırmızı = kötü" gibi bir yargı çağrıştırmasın.

## Yazı
- Başlık: Source Serif 4 (600/700). Gövde: Source Sans 3 (400/600). Türkçe karakterler (ğ ş ı İ ö ü ç) doğrulandı.
- Dosyalar `fonts/` altında, lisansları yanlarında.

## Dil
- **"Siz"** ile hitap: resmî konuları ele alan kamusal bir hizmet için saygılı ve herkese uygun.
- Kısa cümle, günlük sözcük, kısaltma varsa açılımı. Yargı taşıyan fiil yok ([TARAFSIZLIK.md](TARAFSIZLIK.md)).
- Emin olunmayan şey emin gibi yazılmaz; "bilinmiyor" denir.

## Dosyalar
`logo.svg` (açık zemin) · `logo-koyu.svg` (koyu zemin) · `favicon.svg`

## Açık maddeler
- TÜRKPATENT'te "Halk Bilsin" sorgusu (sınıf 9/35/38/41/42).
- 15–20 kişiyle 5 saniyelik isim ve renk çağrışım testi.
- Kod ve içerik lisansı seçimi.
