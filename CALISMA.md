# Çalışma usulü

Halk Bilsin'i birlikte (proje sahibi + yapay zekâ yardımcısı) nasıl yürüttüğümüzün kaydı. Amaç: aynı hataları tekrarlamamak ve bir sonraki oturumun kaldığı yerden devam edebilmesi. Son güncelleme: 25 Ekim 2026.

## Kurallar

1. **Her bulgu etiketlenir:** [D] doğrulandı, [H] hipotez, [?] bilinmiyor. Bilinmeyen şey "bilmiyorum" diye yazılır; tahmin bilgi gibi sunulmaz.
2. **Önce kaynak, sonra metin.** Resmî metin okunmadan "ne yapmanız gerekebilir" yazılmaz. Haber ve yorum yalnızca ikincil kaynaktır (◐).
3. **Erişim sınırları aşılmaz.** Bir site ya da araç içerik vermiyorsa (robots, engel, bayat önbellek) başka yoldan dolanılmaz; söylenir ve içerik kullanıcıdan istenir.
4. **Yayımlanan her şeyde vaat–kanıt kontrolü.** Henüz çalışmayan şey "var" diye yazılmaz ("olacak"); sayfalar ve gönderiler birbiriyle çelişmemeli (bugünkü örnek: "yalnızca resmî kayıttaki gerçekler" ↔ "ikincil kaynak").
5. **Dış platformların kuralı yayından önce kontrol edilir** (görsel boyutu, kırpma, karakter sınırı). Bugünkü örnek: Instagram ızgarası dikey (3:4) kırpıyor; 1080×1080 görseller yarım çıktı.
6. **Hata hemen söylenir, düzeltilir, kayda geçer.** Sessiz düzeltme yok.
7. **Gizli bilgi sohbete yazılmaz** (parola, jeton). Hesap işlemleri (Cloudflare, Instagram, X) sahibinde kalır; yardımcı alan alan yönlendirir.
8. **Kopya yok.** Uluslararası standartlar (WCAG 2.2 AA, ISO 24495-1) yöntem olarak kullanılır; başkasının görünümü, logosu ya da metni taklit edilmez.
9. **Tarafsızlık her çıktıda geçerli:** parti rengi, puan, karne, yargı fiili, siyasi etiket ve hesap etiketleme yok ([TARAFSIZLIK.md](TARAFSIZLIK.md)).
10. **Git:** küçük, açıklamalı commit'ler; `--amend` yok; her push sonrası yerel ve uzak `main` karşılaştırılır.

## Model ve effort [H]

| İş | Öneri |
|---|---|
| Sayfa, CSS, görsel, depo | Sonnet 5.5, orta effort |
| Resmî metinden kayıt çıkarma | En güçlü model, yüksek effort; yayından önce insan kontrolü |
| Derin araştırma | Araştırma aracı + güçlü model; bulgular etiketli |
| Gönderi metni | Sonnet yeterli; yayından önce sahibi okur |

Model seçimi insan kontrolünün yerini tutmaz.

## Yayın öncesi kontrol listesi

- [ ] Her iddianın kaynağı ya da etiketi var mı?
- [ ] Sayfalar/gönderiler birbiriyle ve ilkelerle çelişiyor mu?
- [ ] Hedef platformun boyut/kırpma kuralına baktım mı?
- [ ] Bağlantılar açılıyor mu, kırık dosya var mı? (yerel sunucuda dene)
- [ ] Koyu tema, dar ekran, yatay taşma
- [ ] Doğrulayamadıklarım açık maddelere yazıldı mı?

## Bugünün (25 Ekim 2026) dersleri

**İyi gidenler:** isim ve alan adı kararını sahibinin ölçütüyle vermek; markayı amaç ölçütlerine göre kurmak (renk çağrışımı, durum anlamının renge bağlı olmaması); kontrast oranlarını hesaplamak; hataları (kare görseller, aşırı iddia) bulunur bulunmaz düzeltmek.

**Kötü gidenler:** Instagram kırpmasına bakmadan kare görsel üretmek; "işaret var" ve "yalnızca resmî kayıttaki gerçekler" gibi taahhütleri erken yazmak; ilk anda dış bağımlılığı (GitHub'dan yazı tipi indirme) denemek; tek seferde fazla şeyi sormadan varsaymak (X/Instagram bağlantılarını kullanıcı adı doğrulanmadan sayfaya eklemek).

## Açık maddeler [?]

7596 sayılı Kanun'un Resmî Gazete durumu ve nihai metni · "çerez yok" ifadesinin barındırıcı tarafı · TÜRKPATENT benzer marka taraması · çağrışım testi · hesap bağlantılarının tıklama kontrolü · gizlilik metninin hukuki incelemesi · kayıt içeriği lisansı.
