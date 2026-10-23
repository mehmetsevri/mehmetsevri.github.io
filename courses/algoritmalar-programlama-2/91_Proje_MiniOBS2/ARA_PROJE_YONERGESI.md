# AP-2 Ara Proje Yönergesi — Mini-OBS 2 v2.6 ve sıralama ölçüm raporu (Hafta 7)

**Ders:** Algoritma ve Programlama – II (C17) · RTEÜ Bilgisayar Mühendisliği, 1. sınıf, bahar yarıyılı · Dr. Öğr. Üyesi Mehmet Sevri

**Kapsam:** Mini-OBS 2 v2.3–v2.6 (H4–H7: arama ve sıralama) · **Veriliş:** H7 · **Teslim:** H8'in ilk dersinin başı · **Çalışma biçimi:** bireysel · Kesin tarih, saat ve teslim ortamı derste ve ders sayfasında duyurulur.

Ara proje, dönemin ikinci modülünü (H4–H7) bütünleştirir. İki ürün teslim edeceksiniz: (1) H4–H7'de eklenen bütün arama ve sıralama yeteneklerini taşıyan, kendi başına derlenen **Mini-OBS 2 v2.6**; (2) v2.4–v2.6'da yazdığınız sıralama yöntemlerini C kütüphanesinin `qsort`'uyla birlikte aynı ölçüm düzeneğinde karşılaştıran bir **ölçüm raporu**. Raporun bölümleri ve zorunlu tablo/grafikleri [rapor şablonunda](ARA_PROJE_RAPOR_SABLONU.md), bir başvuru örneği [v2.6 ölçüm raporunda](v2.6/mini_obs_v2_6_olcum_raporu.md) verilmiştir. Ara projenin ölçme planındaki yeri Yol Haritası Tablo 10.1'dedir; ağırlığı dersin ölçme planında belirtilir.

## 1. Amaç ve öğrenme çıktıları

Ara proje, aşağıdaki öğrenme çıktılarını tek bir programda ve tek bir deneyde bir arada ölçer:

| Sürüm | Öğrenme çıktısı (Yol Haritası, bölüm 5) | Projede karşılığı |
|---|---|---|
| v2.3 (H4) | ÖÇ 4.2, 4.3 — ikili arama, lower_bound, ekleme konumu | numarayla bulma, sıralı ekleme, soyad önekiyle arama |
| v2.4 (H5) | ÖÇ 5.2, 5.4, 5.5 — temel sıralamalar, karşılaştırıcı, kararlılık | çok ölçütlü listeler, Türkçe karşılaştırıcı |
| v2.5 (H6) | ÖÇ 6.2, 6.3, 6.5 — birleştirmeli ve hızlı sıralama, quickselect | toplu yükleme, yinelenen tespiti, şube birleştirme, ortanca |
| v2.6 (H7) | ÖÇ 7.2, 7.3, 7.4 — öbek, öncelik kuyruğu, sayma ve taban sıralaması | not dağılımı, ilk-k listesi, numaraya taban sıralaması, k şubenin birleştirilmesi |
| rapor | **ÖÇ 7.5** — veri özelliklerine göre gerekçeli algoritma seçimi | ölçüm raporu ve seçim rehberi |

Proje ayrıca dönem boyunca kurduğunuz mühendislik alışkanlıklarını değerlendirir: kâhinle test, deterministik çıktı, tekrarlanabilir ölçüm ve dürüst raporlama.

## 2. Kapsam

v2.6, önceki sürümlerin bütün yeteneklerini taşır. Her sürümün ayrıntılı gereksinimleri, kabul ölçütleri ve test senaryoları sürüm belgesinin "Ders notu için özet" bölümündedir: [v2.3](v2.3/mini_obs_v2_3.md), [v2.4](v2.4/mini_obs_v2_4.md), [v2.5](v2.5/mini_obs_v2_5.md), [v2.6](v2.6/mini_obs_v2_6.md) (her birinde bölüm 9). Zorunlu modüller ve programlar:

| Sürüm | Modül ve fonksiyonlar | Program ve seçenekler | Kâhin · kasıtlı hata |
|---|---|---|---|
| v2.3 | `arama`: `ikili_ara_no_say` (yarı açık), `ikili_ara_no_kapali_say`, `no_alt_sinir_say`, `sinif_sirali_ekle_say`, `soyad_dizini_kur`, `soyad_onek_ara`; kayıt dizisi her an numaraya göre sıralı | `ara --no N [--izle] [--dogrusal]`, `ara --soyad ÖNEK`; menü 3'te önek araması | doğrusal arama · `--hata-goster ikili` |
| v2.4 | `turkce`: `tr_karsilastir`; `siralama`: seçmeli, kabarcık, araya ekleme (qsort arayüzü, sayaçlar); `liste`: basari, soyad, no ve ders ölçütleri, numarayla tamamlanmış karşılaştırıcılar | `listele --olcut Ö --yontem Y [--ilk K] [--denetle]` | qsort + numara · `--hata-goster kesme`, `kararsiz` |
| v2.5 | `bolfethet`: birleştirmeli, hızlı (Hoare, üçün ortancası), `k_inci_kucuk`, `ortanca_quickselect`; toplu yükleyici; `yinelenen_bul_siralama`; `sube_birlestir` | `denetle [--yontem siralama/ciftler]`, `birlestir A B`, `ortanca [--ders D] [--denetle]`; `listele`'ye `birlestirmeli`, `hizli` | v1.0 yükleyicisi, v2.1 tüm çiftler, qsort · `--hata-goster kuyruk`, `hoare` |
| v2.6 | `obek`: aşağı süzme, öbek kurma, öbek sıralaması, `ilk_k_say`; `dogrusal`: kararlı sayma, LSD taban (256); `subeler_birlestir` (k yollu) | `dagilim [--ders D] [--genislik G] [--liste K] [--denetle]`, `ilk_k [--k K] [--olcut Ö] [--denetle]`, `birlestir A B C …`; `listele`'ye `obek`, `sayma`, `taban` | qsort + kimlik, bütün liste · `--hata-goster lsd`, `suzme` |

**Ölçüm aracı.** `olcer` en az şu işlemleri sunar: `kiyas_secmeli`, `kiyas_kabarcik`, `kiyas_araya`, `kiyas_birlestirmeli`, `kiyas_hizli`, `kiyas_obek`, `kiyas_sayma`, `kiyas_taban`, `kiyas_qsort` (`--sira karisik/artan/azalan/tekrarli`); `aralik_sayma`, `aralik_taban`, `aralik_birlestirmeli` (`--k K`); `liste_ilk_k`; `subeler_obek`; ve önceki sürümlerin `dogrusal`, `ikili`, `yukleme`, `yukleme_v10`, `yukleme_toplu`, `yinelenen`, `yinelenen_siralama` işlemleri.

**Ne verilir, ne yazılır?**

- **Verilir:** bütün başlık dosyaları (sözleşmeler, sayaç tanımları; `obek.h`, `dogrusal.h` dahil), `ornek_veri/` ve `testler/` dosyaları, `olcer`'in ölçüm düzeneği (veri hazırlama, öğe türü, girdi türleri, kontrol sağlaması), ortak modüller, referans sürüm belgeleri, bu yönerge ve rapor şablonu.
- **Siz yazarsınız:** algoritma modüllerinin `.c` dosyaları, programlar, testler (birim + kâhin + kasıtlı hata), `Makefile`'ın yeni hedefleri, ölçüm raporu ve raporun tablolarını/grafiklerini CSV'den üreten betik.
- **Değiştirilmez:** v1.0 veri modeli, dosya biçimleri ve not kuralları; başlıklardaki fonksiyon imzaları; ortak modüller (`ortak_rastgele`, `zamanlayici`).
- **Haftalık adımlarda eksik kalan modüller:** v2.3–v2.5'te tamamlayamadığınız bir modül için referans sürümün dosyasını kullanabilirsiniz; dosyayı raporun beyan ekinde **adıyla** belirtin. Referanstan alınan dosyanın işlevleri, işlevsel doğruluk ölçütünde ilgili sürümün payından puan almaz (bölüm 8); diğer ölçütler (test, ölçüm, rapor) bundan etkilenmez.

## 3. Zaman çizelgesi

- **H7 dersi:** yönerge ve şablon verilir; v2.6'nın gereksinimleri işlenir; atölyede ara proje çalışma oturumu ve kod incelemesi.
- **Önerilen plan (H7 → H8, yaklaşık bir hafta):**
  1. 1.–2. gün: `obek.c`, `dogrusal.c`; elle izlenen birim testleri; kâhin denemeleri; `--hata-goster lsd` ve `suzme`.
  2. 3. gün: `dagilim`, `ilk_k`, çok yollu `birlestir`; `listele`'ye üç yöntem; `make test`, `make asan`.
  3. 4. gün: `make olcum` — prize takılı, diğer programlar kapalı, tek oturumda (referans makinede dört sürümün ölçümleri toplam 8 dakika 13 s; v2.6'nın ölçümü 1 dakika 33 s).
  4. 5.–6. gün: rapor — önce tabloları ve grafikleri betikle CSV'den üretin, sonra yorumu yazın.
  5. 7. gün: teslim öncesi denetim listesi (bölüm 11), temiz bir kopyada.
- **Teslim:** H8'in ilk dersinin başı. Geç teslim ve mazeret durumları ders izlencesindeki ve kurumun ölçme–değerlendirme yönetmeliğindeki kurallara göre değerlendirilir (Recep Tayyip Erdoğan Üniversitesi, 2025).

## 4. Teknik kurallar

### 4.1 Dil ve derleme

- Yalnızca **C17**: `gcc -std=c17 -Wall -Wextra -pedantic -O2 -g`; **sıfır uyarı**. `-O0 … -Os` düzeylerinde de uyarısız derlemeniz önerilir.
- Yalnızca standart kütüphane. Algoritmanın kendisi kütüphaneye devredilmez: `qsort`/`bsearch` yalnızca kâhin olarak ve `kiyas_qsort` gibi açıkça karşılaştırma için kullanılır.
- `rand()` kullanılmaz; rastgelelik ortak LCG'den (`ortak_rastgele`) gelir ve tohumla raporlanır.

### 4.2 Modüler yapı ve kod alışkanlıkları

- v1.0'ın dört modülü (`metin`, `obs`, `dosya`, `main`) korunur; her yeni yetenek kendi modülündedir. Adlar Türkçe, ASCII, `snake_case`; satırlar ≤ 80 sütun.
- Her fonksiyonda ön/son koşul; döngülerde değişmez; analiz edilen fonksiyonlarda karmaşıklık yorumu (Yol Haritası 6.5).
- Bellek: her `malloc` denetlenir, tek temizlik yolu; ASan/UBSan temiz.

### 4.3 Makefile hedefleri

| Hedef | Ne yapar? |
|---|---|
| `make` | bütün programları derler |
| `make test` | birim testleri ve kâhin testlerini derler ve çalıştırır; biri başarısızsa hata verir |
| `make olcum` | raporun bütün ölçümlerini yapar: `olcum/*.csv` ve `olcum/OLCUM_ORTAMI.txt` (kendi makinenizde ≈ 5 dakikayı aşmamalı) |
| `make asan` | `-fsanitize=address,undefined -fno-sanitize-recover=all` ile testler ve örnek çalıştırmalar; rapor çıkmamalı |
| `make temiz` | derleme ürünlerini ve geçici dosyaları siler |

`make valgrind` isteğe bağlıdır. AddressSanitizer MinGW'de desteklenmez; `make asan` için WSL ya da Linux kullanın.

### 4.4 Çıktı sözleşmesi (otomatik değerlendirme buna dayanır)

- **stdout deterministiktir:** aynı girdi ve argümanlarla bayt bayt aynı. **Süreler yalnızca stderr'e** ya da CSV'ye yazılır.
- **Çıkış kodları:** 0 başarı; 1 dosya/bellek hatası, `--denetle` uyuşmazlığı, şube çakışması, yinelenen numara, başarısız test; 2 hatalı kullanım (eksik/geçersiz argüman, uygulanamaz yöntem–ölçüt birleşimi).
- **Program ve seçenek adları** sürüm belgelerindeki gibidir (bölüm 2).
- **Çıktı biçimi serbesttir;** ancak denetlenen değerler — öğrenci numaraları, sayaçlar, ortanca ve ortalamalar — programın çıktısında **ondalık noktayla ve binlik ayırıcısız** yazılır (ör. `77.5`, `4932`). Rapor ise Türkçe sayı biçimini kullanır (77,5; 4 932).

### 4.5 Test

- v1.0'ın 99 doğrulaması ve önceki sürümlerin bütün testleri her zaman geçer (regresyon).
- Her yeni algoritmanın **elle izlenmiş** en az bir birim testi (sonuç ve sayaçlar) ve **kâhinle** rastgele testleri vardır; kâhin, sınanan koddan farklı bir yoldan hesaplar.
- Uyuşmazlıkta tohum, n, beklenen/bulunan ve küçük bir karşı örnek basılır; `--tohum t --deneme 1` hatayı yeniden üretir.
- v2.6'nın iki kasıtlı hatası (`--hata-goster lsd`: kararsız ara sıralama; `--hata-goster suzme`: hatalı aşağı süzme) kâhine yakalatılır.

## 5. Ölçüm raporu (özet)

Ayrıntılar ve tablo/grafik listesi [şablondadır](ARA_PROJE_RAPOR_SABLONU.md). Asgari kapsam:

- **Dokuz yöntem × dört girdi türü × n:** seçmeli, kabarcık, araya ekleme, birleştirmeli, hızlı, öbek, sayma, taban ve `qsort`; karışık, sıralı, ters ve çok tekrarlı girdi; karesel üçlü n = 1 000–8 000 (karışıkta 16 000 önerilir), diğerleri n = 10³–10⁶.
- **Düzen:** her nokta için 1 ısınma + en az 5 tekrar, ortanca (10⁶'da en az 3 tekrar); `-O2`; sayaçlar süreden ayrı çalıştırmada (Sedgewick & Wayne, 2011).
- **Ek deneyler:** anahtar aralığı (n = 10⁵; K = 10 … 10⁷), ilk-k (k = 1 … 10⁵), çok yollu birleştirme (k = 2 … 64) ve Mini-OBS'ye yansıma (v2.3–v2.5 ölçümlerinizden: numarayla bulma, yükleme, yinelenen tespiti).
- **Kuramla karşılaştırma:** oran testleri, log–log eğimler, karşılaştırma sayısının n log₂ n'ye oranı ve log₂ n! alt sınırı, kapalı biçim sayaçlar (Cormen vd., 2022; Knuth, 1998).
- **Tartışma:** kararlılık sağlaması, önbellek ve sabitlerin etkisi, algoritma seçim rehberi, sınırlılıklar, makine bilgisi.
- **Biçim:** en çok 12 sayfa (ekler hariç), PDF + Markdown kaynağı; her sayı teslim edilen CSV'lerden betikle üretilir.

Referans rapordaki sayıları değil **kendi makinenizin** sayılarını raporlayın: süreler farklı olacaktır; büyüme sınıfları, sayaçlar ve karşılaştırmaların yönü aynı kalmalıdır.

## 6. Teslim edilecekler

1. **Kod:** `v2.6/` — kendi başına derlenir; `make temiz` yapılmış hâliyle.
2. **Testler:** `test_obs.c`, `test_kahin.c` (kasıtlı hata gösterimleriyle) ve `testler/` girdileri.
3. **Ölçüm verisi:** `olcum/*.csv` ve `olcum/OLCUM_ORTAMI.txt` — raporda kullanılan çalıştırmanın kendisi.
4. **Rapor:** `rapor/ara_proje_raporu.pdf`, Markdown kaynağı, şekiller ve tabloları/grafikleri üreten betik.
5. **`v2.6/RAPOR.md`:** v2.3–v2.6 kabul ölçütleri ✓/✗ (her sürüm belgesinin listesi) ve bilinen eksikler.
6. **Beyan:** raporun Ek C'si — yararlanılan kaynaklar, referans sürümden alınan dosyalar, kullanılan araçlar ve amaçları.

```
numara_ad_soyad_ara_proje/
├── v2.6/
│   ├── *.h  *.c  Makefile  RAPOR.md
│   ├── ornek_veri/  testler/
│   └── olcum/        ← *.csv, OLCUM_ORTAMI.txt
└── rapor/
    ├── ara_proje_raporu.md  ara_proje_raporu.pdf
    ├── sekiller/     ← *.png
    └── uret.py       ← CSV → tablo ve grafik (ya da eşdeğeri)
```

Teslim biçimi (arşiv ya da depo bağlantısı + `v2.6` etiketi) duyuruyla bildirilir. Derleme ürünleri (`*.o`, programlar) ve büyük veri dosyaları (ör. 10⁶ kayıtlık CSV) teslime konmaz; veri `veri_uret` komutu ve tohumuyla belgelenir.

## 7. Kabul ölçütleri

### 7.1 Değerlendirmeye alınma koşulları

- [ ] `make temiz && make` derleme hatası vermez (hata değerlendirmeyi durdurur; uyarılar kod kalitesinden puan kaybettirir).
- [ ] `make test` çalışır; v1.0'ın 99 doğrulaması geçer.
- [ ] Rapor (PDF) ve raporun sayılarını üreten CSV'ler teslimdedir; rapordaki sayılar CSV'lerle tutarlıdır.
- [ ] Teslimde derleme ürünü ve büyük veri dosyası yoktur.

### 7.2 İşlevsel kabul listesi

Değerlendirmede aşağıdaki komutlar (ve benzerleri) teslim ettiğiniz klasörde otomatik çalıştırılır. Değerler stdout'ta bu sırayla görünmelidir; çıkış kodları birebir denetlenir. Ayrıntılı listeler sürüm belgelerindedir.

| # | Komut (`v2.6/` içinde) | Beklenen |
|---|---|---|
| 1 | `./ara ornek_veri/ogrenciler.csv --soyad yıl` | 2301010045, 2301010048 (yalnız bu ikisi); çıkış 0 |
| 2 | `./mini_obs testler/yinelenen_k3.csv` | "satır 12" (v1.0 ile aynı); çıkış 1 |
| 3 | `./olcer yukleme --sira azalan --n 1000 --tekrar 1` | taşıma 499500; `kuram: UYUMLU` |
| 4 | `./listele ornek_veri/ogrenciler.csv --olcut soyad` | 2301010049, …050, …051, …046, …047, …052, …045, …048 (Türkçe sıra) |
| 5 | `./listele testler/kararlilik.csv --yontem secmeli --denetle` | çıkış 1 (kararsız); `--yontem araya`: çıkış 0 |
| 6 | `./olcer anahtar_birlestirmeli --sira artan --n 1000 --tekrar 1` | karşılaştırma 4932, taşıma 19952; `--sira azalan`: 5044 |
| 7 | `./olcer anahtar_hizli --sira artan --n 1024 --tekrar 1` | derinlik 11 |
| 8 | `./denetle testler/yinelenen_k3.csv` (ve `--yontem ciftler`) | 2400000017, 2400000028, 2400000023 bu sırayla; çıkış 1 |
| 9 | `./ortanca ornek_veri/ogrenciler.csv --denetle` | 77.50, 69.30, 55.30; çıkış 0 |
| 10 | `./birlestir ornek_veri/ogrenciler.csv testler/sube_cakisma.csv` | çakışma 2301010047; çıkış 1 |
| 11 | `./dagilim ornek_veri/ogrenciler.csv --liste 5 --denetle` | ortanca 77.5; 2301010050, …047, …048, …045, …049; çıkış 0 |
| 12 | `./ilk_k ornek_veri/ogrenciler.csv --k 3 --denetle` | 2301010050, …045, …048; çıkış 0 |
| 13 | `./birlestir ornek_veri/ogrenciler.csv ornek_veri/sube_b.csv ornek_veri/sube_c.csv` | 20 kayıt; ilk kayıt 2301010040; çıkış 0 |
| 14 | `./listele testler/kararlilik.csv --yontem obek --denetle` | çıkış 1 (kararsız); `--yontem sayma`: çıkış 0 |
| 15 | `./olcer kiyas_taban --n 1000 --tekrar 1` | toplama 5024, taşıma 4000 (4 geçiş); `kuram: UYUMLU` |
| 16 | `./listele ornek_veri/ogrenciler.csv --olcut soyad --yontem sayma` | çıkış 2 (uygulanamaz) |
| 17 | eşit ALG ortalamalı iki kayıt (ZEN 3/0, AK 0/2; v2.6 belgesi bölüm 4.7), `--olcut alg` | AK, ZEN'den önce |
| 18 | `./test_kahin --hata-goster lsd` / `suzme` | uyuşmazlık ve küçük karşı örnek; çıkış 1 |

### 7.3 Ölçümle ilgili kabul ölçütleri (kendi makinenizde)

| Ölçüt (sürüm belgesi) | Eşik | Referans makinede |
|---|---|---|
| 10⁵ kayıtta ikili arama / doğrusal arama (v2.3 #8) | ≥ 100 kat | 730 kat |
| n = 4 000 listede araya ekleme: karışık / sıralı (v2.4 #8) | ≥ 50 kat | 162 kat |
| 10⁶ kaydın toplu yüklenmesi (v2.5 #9) | < 1 dakika | 2,28 s |
| 10⁵ kayıtta yinelenen tespiti: v2.1 / v2.5 (v2.5 #9) | ≥ 50 kat | 187 kat |
| 10⁶ karışık numara: birleştirmeli / taban (v2.6 #10) | > 1 (taban daha hızlı) | 3,4 kat |
| 10⁵ kayıtta bütün liste / ilk-10 (v2.6 #10) | ≥ 10 kat | 61 kat |

Bir eşik kendi makinenizde sağlanmıyorsa bu otomatik bir kayıp değildir: nedenini raporda ölçümle tartışın (ör. sanal makine, güç tasarrufu, önbellek boyutu). Açıklanmayan sapma puan kaybettirir.

## 8. Puanlama (100 puan)

Rubrik, Yol Haritası Tablo 10.3'teki final projesi rubriğinin ara projeye uyarlanmış biçimidir: ara projenin ürünü bir deney raporu olduğu için **ölçüm raporu** ağırlığı %15'ten %25'e çıkarılmış, **algoritma seçimi ve analiz** %25'ten %20'ye indirilmiş, final projesinin **sunumu** (%10) yerine 5 puanlık **kısa savunma** konmuştur.

| Ölçüt | Puan | Yetkin (%90–100) | Gelişmiş (%70–89) | Gelişmekte (%40–69) | Yetersiz (%0–39) |
|---|---|---|---|---|---|
| **İşlevsel doğruluk** | 25 | v2.3–v2.6'nın bütün kabul ölçütleri sağlanır; sınır durumları (n = 0, 1; boş önek; aralık dışı anahtar; çakışma) doğru; çıktı sözleşmesine tam uyum | bir iki küçük sapma (ileti, çıkış kodu); algoritmaların sonuçları doğru | bir sürümün yeteneği eksik ya da bazı girdilerde yanlış (ör. kararsız sayma, çift n'de yanlış ortanca) | birden çok yetenek eksik; yanlış sonuçlar ya da çökme |
| **Algoritma seçimi ve analiz** | 20 | kimlik kartları ve karmaşıklıklar doğru; değişmez ve ön/son koşul yorumları eksiksiz; sayaçların kapalı biçimleri doğru; Mini-OBS'deki her iş için seçim ölçümle gerekçeli | analiz doğru, gerekçelerde küçük boşluklar | karmaşıklık ya da kararlılık iddialarında hatalar; gerekçe yüzeysel | analiz yok ya da büyük ölçüde yanlış |
| **Test ve doğrulama** | 15 | elle izlenmiş birim testleri; farklı yoldan hesaplayan, tohumlu kâhinler; sınır durumlarına yönlendirilmiş denemeler; kasıtlı hatalar ve küçük karşı örnekler; `make test` otomatik | kâhin var, sınır durumları ya da karşı örnek eksik | yalnızca birkaç elle test; kâhin sınanan fonksiyonu çağırıyor | test yok ya da çalışmıyor |
| **Ölçüm raporu** | 25 | şablonun bütün bölümleri; ortanca ve tekrar; okunur log–log grafikler; eğim, oran ve sayaçlarla kuram karşılaştırması; sapmalar açıklanmış; seçim rehberi ve sınırlılıklar; yeniden üretilebilir | eksik bir deney ya da zayıf yorum; biçim kusurları | tablolar var ama kuramla karşılaştırma ya da düzen bilgisi eksik; doğrusal eksen; tek ölçüm | rapor yok; sayılar CSV ile tutarsız ya da ölçülmemiş |
| **Kod kalitesi ve bellek güvenliği** | 10 | sıfır uyarı; ASan/UBSan temiz; modüler, sözleşmeli, okunur kod; bütün Makefile hedefleri | birkaç uyarı ya da biçim kusuru | ASan raporu ya da sızıntı; dağınık modüller | derleme sorunları, çok sayıda bellek hatası |
| **Kısa savunma** | 5 | kendi kodundan istenen fonksiyonu ve raporundan istenen bulguyu doğru ve akıcı açıklar | küçük eksiklerle açıklar | yüzeysel açıklar | açıklayamaz |

**Puanın dağılımı (ölçüt içinde).**

- *İşlevsel doğruluk (25):* v2.3 5 · v2.4 5 · v2.5 6 · v2.6 9.
- *Algoritma seçimi ve analiz (20):* kimlik kartları ve karmaşıklık 6 · değişmezler, ön/son koşullar 4 · sayaçların kapalı biçimleri ve kuram denetimleri 4 · Mini-OBS işlerinde seçimin gerekçesi (kararlılık, anahtar aralığı, bellek) 6.
- *Test ve doğrulama (15):* elle izlenmiş birim testleri 4 · kâhin testleri (farklı yol, tohum, sınır durumları) 5 · kasıtlı hata gösterimi ve küçük karşı örnek 3 · otomatik çalıştırma ve regresyon 3.
- *Ölçüm raporu (25):* yöntem ve ortam 4 · tablolar ve grafikler 7 · kuramla karşılaştırma 7 · tartışma ve seçim rehberi 4 · sınırlılıklar ve yeniden üretilebilirlik 3.
- *Kod kalitesi ve bellek güvenliği (10):* uyarısız derleme 2 · ASan/UBSan temiz 3 · modülerlik, adlandırma, sözleşme yorumları, 80 sütun 3 · Makefile hedefleri 2.
- *Kısa savunma (5):* yaklaşık 5 dakika; kendi kodunuzdan bir fonksiyon ve raporunuzdan bir bulgu.

## 9. Akademik dürüstlük ve yapay zekâ kullanımı

- Ara proje bireysel bir çalışmadır. Kurumun akademik dürüstlüğe ilişkin ilke ve düzenlemeleri ile ders izlencesindeki kurallar geçerlidir.
- Kitap, ders materyali, referans sürümler ve çevrim içi kaynaklardan yararlanabilirsiniz; yararlandığınız her kaynağı ve referans sürümden aldığınız her dosyayı beyan ekinde belirtin.
- **Yapay zekâ araçları:** kullanımları, kurumun ve dersin yürürlükteki politikasına bağlıdır. Kullandıysanız beyan ekinde hangi aracı, hangi amaçla ve hangi bölümler için kullandığınızı yazın. Teslim edilen kodun ve raporun doğruluğundan ve açıklanabilirliğinden siz sorumlusunuz.
- **Ölçüm verisi:** rapordaki her sayı, teslim ettiğiniz CSV'lerden gelen kendi ölçümünüzdür. Başka bir kaynaktaki (referans rapor dahil) sayıları aktarmak ya da ölçülmemiş bir değeri ölçülmüş gibi sunmak veri uydurmadır; ölçülemeyen değerler yöntemiyle birlikte "kestirim" diye verilir.
- Öğretim üyesi, kısa savunmada teslim edilen çalışmanın herhangi bir bölümünü açıklamanızı isteyebilir.

## 10. Sık yapılan hatalar

**Algoritma ve kod**

- İkili aramada yarı açık ve kapalı aralığı karıştırmak (`hi = orta` / `hi = orta − 1`); orta noktayı `(lo + hi) / 2` ile hesaplamak.
- Kararlılığı bozmak: araya eklemede eşitlerde de kaydırmak; birleştirmede eşitlikte sağdan almak.
- Hoare bölümlemesinin döndürdüğü j ile Lomuto'nun p'sini karıştırmak (`--hata-goster hoare`).
- Öbek kurmayı i = 0'dan başlatmak; aşağı süzmede yalnız sol çocuğa bakmak; işaretsiz sayaçla `i >= 0` koşulu (sonsuz döngü).
- Sayma sıralamasında aralık dışı anahtarı denetlememek; yerleştirmeyi sondan başa yaparken "ilk konum" tutmak (kararsız).
- Taban sıralamasında kararsız ara sıralama (`--hata-goster lsd`: [257, 256] sıralanmaz); tek sayıda geçişte sonucu diziye geri kopyalamamak.
- Kayan nokta ortalamalarını eşitlik için doğrudan karşılaştırmak: double'da 0,4 · 3 + 0,6 · 0 ile 0,4 · 0 + 0,6 · 2 farklıdır (v2.6 belgesi bölüm 4.7).
- İlk-k'da ölçütü numarayla tamamlamamak: eşitlerde sonuç tek değildir ve kâhinle karşılaştırma rastgele başarısız olur.

**Test**

- Kâhinin sınanan fonksiyonu çağırması (aynı hata iki tarafta da vardır).
- Yalnızca rastgele girdi: n = 0, 1, 2, eşit anahtarlar, sıralı ve ters girdi denenmemiş.
- Testlerin hatayı yakalayabildiğini kasıtlı bir hatayla göstermemek.

**Ölçüm**

- Her tekrarda zaten sıralanmış diziyi yeniden sıralamak (başlangıç dizisinin kopyası alınmamış).
- Süreyi stdout'a yazmak; `-O0` ile ölçmek; tek ölçüm; ortanca yerine en iyi ya da ilk değeri raporlamak.
- Sayaç artırımlarını süre ölçülen çalıştırmada açık bırakmak.
- Dizüstü bilgisayarda pil ve güç tasarrufu kipinde, başka işler çalışırken ölçmek.
- Sonucu kullanılmayan bir işi ölçmek (derleyici işi silebilir).

**Rapor**

- Karesel ve n log n büyümeyi doğrusal eksenli grafikte karşılaştırmak; eksen adı, birim ya da ölçek türü yazmamak.
- Tablo sayılarını elle kopyalamak (CSV ile tutarsızlık).
- Kestirimi ölçüm gibi sunmak; makine bilgisini ya da sınırlılıkları atlamak.
- "`qsort` kararlıdır" demek: bir C kütüphanesinin bir makinede kararlı davranması, standardın güvencesi değildir.
- "Taban sıralaması doğrusaldır, öyleyse her zaman en hızlısıdır" demek: anahtar uzunluğu, anahtar aralığı ve önbellek etkisi ölçümle tartışılmalıdır.

## 11. Teslim öncesi denetim listesi

- [ ] Temiz bir kopyada `make temiz && make` (sıfır uyarı), `make test`, `make asan`.
- [ ] Bölüm 7.2'deki komutlar kendi klasörünüzde beklenen sonuçları ve çıkış kodlarını veriyor.
- [ ] `make olcum` tek oturumda çalıştırıldı; `olcum/*.csv` ve `OLCUM_ORTAMI.txt` raporla aynı çalıştırmaya ait.
- [ ] Rapordaki tablolar ve grafikler bu CSV'lerden betikle yeniden üretildi; şekillerde yazı okunur (≥ 9 pt), eksenlerde ad, birim ve ölçek var.
- [ ] Rapor şablonun bütün zorunlu bölümlerini içeriyor ve PDF'i açılıyor (≤ 12 sayfa, ekler hariç).
- [ ] `RAPOR.md`'de v2.3–v2.6 kabul ölçütleri işaretlendi; bilinen eksikler yazıldı.
- [ ] Beyan eki dolduruldu.
- [ ] `make temiz`; teslimde `*.o`, programlar ve büyük veri dosyaları yok.

## 12. Derleme, test ve ölçüm komutları

```bash
cd v2.6
make temiz && make && make test
make asan                                   # WSL ya da Linux
make olcum                                  # olcum/*.csv ve olcum/OLCUM_ORTAMI.txt
./olcer kiyas_taban --sira karisik --n 1000000 --tekrar 3   # tek nokta: stdout sayaçlar, stderr süre
./listele testler/kararlilik.csv --yontem hepsi
./test_kahin --hata-goster lsd; echo "[çıkış kodu: $?]"
```

## Kaynaklar

- Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2022). *Introduction to algorithms* (4th ed.). MIT Press.
- Knuth, D. E. (1998). *The art of computer programming: Vol. 3. Sorting and searching* (2nd ed.). Addison-Wesley.
- Recep Tayyip Erdoğan Üniversitesi. (2025). *Recep Tayyip Erdoğan Üniversitesi ön lisans ve lisans eğitim-öğretim ve sınav yönetmeliği* (Resmî Gazete, 14 Aralık 2025, Sayı: 33107; son değişiklik: Resmî Gazete, 27 Şubat 2026, Sayı: 33181).
- Sedgewick, R., & Wayne, K. (2011). *Algorithms* (4th ed.). Addison-Wesley.
