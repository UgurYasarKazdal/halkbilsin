# Halk Bilsin

Seni ilgilendiren kanun, yönetmelik ve belediye kararlarını, yürürlük tarihleri ve kaynaklarıyla sade Türkçe ile göstermeyi hedefleyen açık kaynaklı bir sivil proje.

**Durum: erken taslak.** Bu depodaki şey şimdilik yalnızca projenin tanıtım sayfasıdır; çalışan bir hizmet yoktur.

- Alan adı: halkbilsin.tr
- İlkeler: [TARAFSIZLIK.md](TARAFSIZLIK.md)
- Marka: [BRAND.md](BRAND.md)

## Bu sayfa nasıl çalışıyor

Derleme adımı yok: `index.html` ve `style.css` doğrudan yayımlanır. Harici yazı tipi, izleme kodu ya da çerez kullanılmaz. (Barındırma şirketleri teknik olarak bağlantı kayıtları tutabilir.)

Yerelde görmek için bir klasör sunucusu yeterli:

```bash
python3 -m http.server 8000
# sonra tarayıcıda http://localhost:8000
```

## Yayına alma (Cloudflare Pages)

1. Alan adının DNS'i Cloudflare'dedir (nameserver'lar Cloudflare'in verdiği ikiliye çevrilmiştir). Cloudflare panelinde alan adı "Active" olmalı.
2. Cloudflare panelinde **Workers & Pages → Create → Pages → Connect to Git** ile bu depoyu seç.
3. Build komutu boş, çıktı klasörü `/` (kök). Derleme adımı yoktur.
4. İlk yayın `*.pages.dev` adresinde açılır. Sonra Pages projesinde **Custom domains** bölümüne `halkbilsin.tr` ekle; DNS kaydı ve HTTPS sertifikası Cloudflare tarafından kurulur.
5. Her `main` dalına gönderimde site kendiliğinden güncellenir.
6. İletişim için Cloudflare **Email Routing** ile alan adı adresi (örn. `iletisim@halkbilsin.tr`) açıp kendi e-postana yönlendirmek mümkündür.

## Yapılacaklar (yayımlamadan önce)

- İletişim e-posta adresi eklenecekse sayfadaki “Fikrini söyle” bölümüne ekle.
- Sayfadaki örnek kaydın (7596 sayılı Kanun) tarihleri 25 Ekim 2026 itibarıyla yazıldı; durum değiştiyse güncelle ya da kaldır.
- Lisans seçimi: kod için bir lisans (örn. MIT veya AGPL) ve içerik için ayrı bir lisans kararı verilmeli; bu karar verilene kadar `LICENSE` dosyası yok.

## Katkı

Hata, öneri ya da fikir için GitHub Issues kullanılabilir. Veri eklenirken [TARAFSIZLIK.md](TARAFSIZLIK.md) kuralları geçerlidir.
