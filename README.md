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
tools/sync_course.py               Ders sitelerini OneDrive'daki kaynak klasörlerden eşitler
tools/serve.py                     Yerel önizleme sunucusu
courses/algoritmalar-programlama-1/  AP-I ders sitesi (tools/sync_course.py ile üretilir)
courses/algoritmalar-programlama-2/  AP-II ders sitesi (tools/sync_course.py ile üretilir)
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
  (şu an 8 başvuru: 2’si tescilli, 1’i PCT). `pct: true` olan kayıt zaman çizelgesinde vurgulanır;
  `"status": "granted"` olan kayıtta altın “Tescilli patent” rozeti ve “TESCİL” damgası görünür.
  İsteğe bağlı alanlar: `desc_tr`/`desc_en` (kısa açıklama), `inventors` (`name`, `title_tr`, `title_en`).
  `art`: `forest`, `rfid`, `mirror`, `modem`, `uav`, `pest`, `wafpct`, `waftr`.
- **Sanayi danışmanlıkları:** `consultancies` dizisi (proje kaydıyla aynı alanlar; rol “Danışman”).
- **AISEC Lab:** `lab` nesnesi. Üye eklemek için `lab.members` dizisine
  `{ "name", "group": "lead|academic|research|student", "role_tr", "role_en", "photo" }` ekleyin.
  Fotoğraf yoksa `"photo": null` bırakın; baş harflerden oluşan avatar gösterilir.
  Haberler `lab.news`, fotoğraflar `lab.photos` (+ `photo_alts_tr` / `photo_alts_en`),
  laboratuvar sekmesindeki projeler `lab.project_ids` ile yönetilir.
- **Arayüz metinleri** (başlıklar, düğmeler vb.) `assets/js/main.js` içindeki `I18N`
  sözlüğündedir; her anahtar hem `tr` hem `en` altında bulunmalıdır.

## Ders siteleri

Algoritmalar ve Programlama I ve II ders siteleri OneDrive'daki kaynak klasörlerden
(`DERSLER/Algoritma ve Programlama - 1|2/Sunum ve Materyaller`) eşitlenir:

```bash
python tools/sync_course.py               # iki ders
python tools/sync_course.py --course ap2  # yalnız AP-II
```

- Yalnızca `99_Web_Crash_Course/index.html` sayfasının başvurduğu dosyalar kopyalanır;
  `92_Degerlendirme` (çözümler, soru bankası) asla yayına girmez.
- Ders notu PDF'leri, kod ZIP'leri ve proje yönergeleri yayınlanır; PPTX sunumlar
  PowerPoint ile PDF'e çevrilir; DOCX dosyaları yayınlanmaz.
- AP-II'deki Mini-OBS 2 v3.0 belgeleri (final projesi referans çözümü) yayınlanmaz;
  sayfadaki bağlantıları "dersin klasöründe" olarak pasif görünür
  (`tools/sync_course.py` içindeki `COURSES[...]["private"]`).
- Yeni bir ders için `COURSES` sözlüğüne kaynak/hedef ekleyin ve `data/site-data.json`
  → `courses` dizisindeki derse `id`, `"site": "courses/<klasör>/"` ve
  `site_desc_tr`/`site_desc_en` alanlarını yazın. `site` alanı olan dersler “Dersler”
  bölümünde ilk satırda büyük kart olarak yan yana gösterilir.

## Yerelde önizleme

Depo kök klasöründe:

```bash
python tools/serve.py        # http://localhost:8080
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
