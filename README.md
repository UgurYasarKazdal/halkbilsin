# Halk Bilsin

Seni ilgilendiren kanun, yönetmelik ve belediye kararlarını, yürürlük tarihleri ve kaynaklarıyla sade Türkçe ile göstermeyi hedefleyen açık kaynaklı bir sivil proje.

**Durum: erken taslak.** Bu depodaki şey şimdilik yalnızca projenin tanıtım sayfasıdır; çalışan bir hizmet yoktur.

- Alan adı: halkbilsin.tr
- İlkeler: [TARAFSIZLIK.md](TARAFSIZLIK.md)

## Bu sayfa nasıl çalışıyor

Derleme adımı yok: `index.html` ve `style.css` doğrudan yayımlanır. Harici yazı tipi, izleme kodu ya da çerez kullanılmaz. (Barındırma şirketleri teknik olarak bağlantı kayıtları tutabilir.)

Yerelde görmek için bir klasör sunucusu yeterli:

```bash
python3 -m http.server 8000
# sonra tarayıcıda http://localhost:8000
```

## Yayına alma (GitHub Pages)

1. Depoyu GitHub’da oluştur (örn. `halkbilsin`), dosyaları `main` dalına gönder.
2. Depoda **Settings → Pages**: *Source* = “Deploy from a branch”, branch = `main`, klasör = `/ (root)`.
3. **Custom domain** alanına `halkbilsin.tr` yaz (depodaki `CNAME` dosyası da bunu söyler). *Enforce HTTPS* kutusunu, kullanılabilir olduğunda işaretle.
4. Alan adı sağlayıcının DNS ekranında, GitHub’ın güncel belgesindeki kayıtları ekle (apex alan adı için A/AAAA kayıtları, varsa `www` için CNAME). Güncel IP değerleri için GitHub Pages belgesine bak; buraya yazmıyorum çünkü değişebilir.
5. DNS yayılması birkaç dakikadan birkaç saate kadar sürebilir.

## Yapılacaklar (yayımlamadan önce)

- İletişim e-posta adresi eklenecekse sayfadaki “Fikrini söyle” bölümüne ekle.
- Sayfadaki örnek kaydın (7596 sayılı Kanun) tarihleri 25 Ekim 2026 itibarıyla yazıldı; durum değiştiyse güncelle ya da kaldır.
- Lisans seçimi: kod için bir lisans (örn. MIT veya AGPL) ve içerik için ayrı bir lisans kararı verilmeli; bu karar verilene kadar `LICENSE` dosyası yok.

## Katkı

Hata, öneri ya da fikir için GitHub Issues kullanılabilir. Veri eklenirken [TARAFSIZLIK.md](TARAFSIZLIK.md) kuralları geçerlidir.
