# mehmetsevri.github.io

Dr. Öğr. Üyesi **Mehmet Sevri**’nin iki dilli (TR/EN) kişisel akademik web sitesi.
Yayın adresi: <https://mehmetsevri.github.io/>

Site tamamen statiktir (HTML + CSS + JavaScript). Sunucuda derleme adımı yoktur; GitHub Pages
dosyaları olduğu gibi yayınlar. Sayfa `file://` ile doğrudan açıldığında da çalışır.

## Klasör yapısı

```
index.html                         Ana sayfa (iskelet + SEO meta + JSON-LD)
404.html                           Bulunamayan sayfalar için (GitHub Pages otomatik kullanır)
.nojekyll                          GitHub Pages’in Jekyll işlemesini kapatır (boş dosya)
assets/
  css/main.css                     Tüm stiller (açık/koyu tema token’ları)
  js/main.js                       Arayüz metinleri (I18N), çizim/render ve etkileşimler
  js/data.js                       ÜRETİLEN dosya — elle düzenlemeyin
  img/                             Portre, yayın şekilleri, laboratuvar görselleri, ikonlar
    favicon.svg, apple-touch-icon.png, og-image.jpg
    pubs/                          Yayın şekilleri (.webp)
    lab/                           AISEC Lab logosu, fotoğrafları, haber görselleri
    lab/members/                   Ekip fotoğrafları (.webp, kare)
data/site-data.json                TEK VERİ KAYNAĞI (profil, yayınlar, projeler, patentler, lab…)
tools/build_data.py                site-data.json → assets/js/data.js
tools/make_images.py               favicon, apple-touch-icon ve og-image üretir (Pillow)
courses/algoritmalar-programlama-1/  Ders sitesi (şimdilik “hazırlanıyor” sayfası)
_tema-onerileri/                   Tasarım önerileri (sitenin parçası değildir)
```

## İçerik nasıl güncellenir?

1. `data/site-data.json` dosyasını düzenleyin (UTF-8).
2. Depo kök klasöründe şu komutu çalıştırın:

   ```bash
   python tools/build_data.py
   ```

   Bu komut `assets/js/data.js` dosyasını yeniden üretir, verideki görsel yolları
   bulunamazsa uyarı verir ve `index.html` / `404.html` içindeki CSS/JS bağlantılarına
   içerik özetinden bir sürüm etiketi (`main.css?v=…`) yazar. Böylece ziyaretçilerin
   tarayıcısı eski CSS/JS'i önbellekte tutmaz. `main.css` veya `main.js` dosyasını elle
   değiştirdiğinizde de bu komutu çalıştırın.
3. Değişiklikleri kontrol edip (aşağıdaki “Yerelde önizleme”) commit + push yapın.

> Site verileri çalışma anında `fetch()` ile okunmaz; `data.js` bir `<script>` etiketiyle
> yüklenir. Bu sayede sayfa `file://` üzerinden de çalışır. JSON’u değiştirdikten sonra
> `build_data.py` çalıştırmayı unutmayın.

### Sık yapılan güncellemeler

- **Yeni yayın:** `publications` dizisine yeni bir nesne ekleyin (`id` benzersiz olmalı, örn. `p35`).
  Önemli alanlar: `category` (`article` | `proceeding` | `book`), `type`, `title`, `authors`,
  `venue` (Türkçe kısaltmalarla: `cilt.`, `sa.`, `ss.` — İngilizce görünümde otomatik
  `vol.`, `no.`, `pp.` olur), `year`, `doi`, `abstract` (varsa `abstract_en`), `keywords`,
  `citations`, `indexes`, `avesis_url`, `open_access_pdf`, `figures`.
  Şekil eklemek için görseli `assets/img/pubs/` altına koyun, yolunu `figures` dizisine ve
  açıklamasını üst düzeydeki `figures` sözlüğüne (`w`, `h`, `caption_tr`, `caption_en`) ekleyin.
- **Öne çıkan yayınlar / son makale / öne çıkan proje:** `site.featured_publications`,
  `site.latest_paper`, `site.featured_project`, `site.project_order`.
- **Yeni proje:** `projects` dizisine ekleyin. `id`, `title_tr`/`title_en`, `funder` (rozet metni),
  `kind`/`kind_en`, `program`/`program_en`, `start`/`end` (“Eylül 2026” ya da “2026-09”),
  `role_tr`/`role_en` (rol yoksa `null` bırakın; rozet gösterilmez), `short_tr`/`short_en`,
  `summary_tr`/`summary_en`, `team`, `related_publications`, `art` (çizim anahtarı:
  `pree`, `twin`, `renew`, `nu`, `hydro`, `drone`, `recy`, `safe`, `pharma`, `dcpt`).
  Proje durumu (devam ediyor / tamamlandı / başlayacak) bugünün tarihine göre otomatik hesaplanır.
- **Patentler:** `patents` dizisi. Ana sayfadaki sayı bu diziden hesaplanır
  (şu an 7 başvuru, 1’i PCT). `pct: true` olan kayıt zaman çizelgesinde vurgulanır;
  `art`: `rfid`, `mirror`, `modem`, `uav`, `pest`, `wafpct`, `waftr`.
- **AISEC Lab:** `lab` nesnesi. Üye eklemek için `lab.members` dizisine
  `{ "name", "group": "lead|academic|research|student", "role_tr", "role_en", "photo" }` ekleyin.
  Fotoğraf yoksa `"photo": null` bırakın; baş harflerden oluşan avatar gösterilir.
  Haberler `lab.news`, fotoğraflar `lab.photos` (+ `photo_alts_tr` / `photo_alts_en`),
  laboratuvar sekmesindeki projeler `lab.project_ids` ile yönetilir.
- **Arayüz metinleri** (başlıklar, düğmeler vb.) `assets/js/main.js` içindeki `I18N`
  sözlüğündedir; her anahtar hem `tr` hem `en` altında bulunmalıdır.

## Ders sitesi ekleme

Ders siteleri `courses/<klasör-adı>/` altında bağımsız statik siteler olarak durur.

1. Ders sitesinin dosyalarını (en azından bir `index.html`) örneğin
   `courses/algoritmalar-programlama-1/` klasörüne koyun. Mevcut “hazırlanıyor” sayfası
   bu klasördeki `index.html` dosyasıdır; gerçek ders sitesi geldiğinde klasörün içeriğini
   onunla değiştirmeniz yeterlidir (ana sayfadaki bağlantılar aynı yolu kullanır).
2. Yeni bir ders için `data/site-data.json` → `courses` dizisindeki ilgili derse
   `"site": "courses/<klasör-adı>/"` alanını ekleyin ve `python tools/build_data.py` çalıştırın.
   `site` alanı olan ders, “Dersler” bölümünde büyük kart olarak öne çıkar.
3. Ders sitesindeki bağlantılar göreli olmalıdır (örn. ana sayfaya dönüş için `../../`).

## Yerelde önizleme

Depo kök klasöründe:

```bash
python -m http.server 8000
```

ardından tarayıcıda <http://localhost:8000/> adresini açın. İngilizce görünüm için
<http://localhost:8000/?lang=en>. `index.html` dosyasını çift tıklayarak (`file://`) da
açabilirsiniz.

## Dil, tema ve diğer ayrıntılar

- Varsayılan dil Türkçedir. Seçim tarayıcıda `ms-lang` anahtarıyla saklanır; URL’deki
  `?lang=en` / `?lang=tr` parametresi açılışta bu tercihi geçersiz kılar.
- Tema (açık/koyu) `ms-theme` anahtarıyla saklanır; seçim yoksa işletim sistemi tercihi kullanılır.
- Animasyonlar `prefers-reduced-motion` ayarına uyar; hiçbir içerik görünmek için animasyona
  bağlı değildir (2 saniyelik güvenlik zamanlayıcısı her şeyi görünür yapar).
- Sosyal medya kartı görseli `assets/img/og-image.jpg` dosyasıdır; değiştirmek için
  `python tools/make_images.py` (Pillow gerekir) komutunu kullanabilirsiniz.

## Yayınlama (GitHub Pages)

Depo adı `mehmetsevri.github.io` olmalı; *Settings → Pages* bölümünde kaynak olarak
`main` dalı ve `/ (root)` klasörü seçilmelidir. `_tema-onerileri/` klasörü yalnızca
tasarım önerilerini içerir; yayında görünmesini istemiyorsanız depodan çıkarabilirsiniz.
