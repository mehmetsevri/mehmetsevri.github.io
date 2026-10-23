# Mini-OBS 2 v2.0 — Doğruluk ve Ölçüm: veri üreteci, ölçüm düzeni ve kâhinle test (Hafta 1)

**Bu sürümün amacı:** AP-1'de kurduğumuz Mini-OBS v1.0'ı, kayıt modeline ve dosya biçimlerine dokunmadan, **ölçeklenebilir bir deney düzeneğine** yerleştirmek: (1) ortak LCG ile 10³–10⁶ kayıtlık, tohumla tekrarlanabilir sentetik veri üreten `veri_uret`; (2) Mini-OBS işlemlerinin süresini 1 ısınma + K tekrar + ortanca düzeniyle ölçen `deney` modülü ve `olcer` programı; (3) istatistik fonksiyonlarını kaba kuvvet ya da sıralama tabanlı bir **kâhine** karşı rastgele girdilerle sınayan `test_kahin`. Bu altyapıyla yapılan ilk ölçüm, v1.0 yükleyicisinin **karesel** (O(n²)) olduğunu gösterdi: 10⁵ kayıt 17,1 s'de yükleniyor, 10⁶ kayıt ise pratikte yüklenemiyor (kestirim ≈ 1,6 saat; bölüm 6). Bu bulgu H2'nin (asimptotik analiz, oran testi) ve v2.1'in çıkış noktasıdır.

Dosyalar (satır sayılarıyla): `obs.h` (109) · `obs.c` (590) · `metin.h` (35) · `metin.c` (340) · `dosya.h` (60) · `dosya.c` (320) · `main.c` (292) · `uretec.h` (54) · `uretec.c` (160) · `veri_uret.c` (94) · `deney.h` (28) · `deney.c` (32) · `olcer.c` (293) · `test_obs.c` (562) · `test_kahin.c` (459) · `ortak_rastgele.h` (42) · `ortak_rastgele.c` (50) · `zamanlayici.h` (30) · `zamanlayici.c` (55) · `Makefile` (128) · `ornek_veri/ogrenciler.csv` (v1.0'ın 8 kaydı) · `testler/` (v1.0 oturum girdileri T1–T6b, `bozuk.csv`) · `olcum/*.csv`, `olcum/OLCUM_ORTAMI.txt`, `olcum/kestirim.py` · `mini_obs_v2_0_ciktilar.txt` (378 satır; derleme, testler, üreteç, uyumluluk, regresyon, kâhin, ölçüm günlüğü, ASan ve Valgrind — hepsi gerçek çıktı). Şekiller: `mini_obs_v2_0_mimari.png`, `mini_obs_v2_0_uretec.png`, `mini_obs_v2_0_kahin.png`; grafikler: `mini_obs_v2_0_olcum_yukleme.png`, `mini_obs_v2_0_olcum_tarama.png`.

Derleme: `make` (programlar), `make test` (birim + kâhin testleri), `make olcum` (bu belgedeki ölçümler, bu makinede 1 dk 48 s), `make asan`, `make valgrind`, `make ornek`, `make temiz`. Bayraklar: `-std=c17 -Wall -Wextra -pedantic -O2 -g`; 12 kaynak dosya `-O0 … -Os` düzeylerinin hepsinde `-Werror` ile uyarısız derlenir. Çıkış kodları bütün programlarda aynıdır: 0 başarı, 1 dosya/girdi/bellek hatası (test programlarında: uyuşmazlık), 2 hatalı kullanım.

## 1. Amaç ve haftanın kavramıyla bağı

Hafta 1'in Büyük Sorusu, "bütün testleri geçen bir program doğru mudur?" sorusudur. Yanıt, Dijkstra'nın uyarısındaki gibi olumsuzdur: test hataların varlığını gösterebilir, yokluğunu kanıtlayamaz (Dahl vd., 1972). Bu yüzden haftanın üç aracı birlikte kullanılır ve v2.0 bu üçünü Mini-OBS'ye taşır:

- **Kâhinle karşılaştırmalı test** (ÖÇ 1.3): `test_kahin`, hızlı fonksiyonu yavaş ama apaçık doğru bir kâhinle yüzlerce rastgele girdide karşılaştırır; uyuşmazlıkta **tohumu** ve **küçültülmüş karşı örneği** basar.
- **Tekrarlanabilir veri** (Kaputun Altında, ortak LCG): `veri_uret` aynı tohumla bayt bayt aynı dosyayı üretir; `rand()` kullanılmaz ve üretim yalnızca tamsayı aritmetiğine dayandığı için sonuç platformdan bağımsız olmalıdır (altın satır testi bunu denetler).
- **Deneysel ölçüm** (ÖÇ 1.4): `deney_olc` 1 ısınma + K tekrar yapar; ortancanın yanında tek ölçümü, ortalamayı, en az ve en çok süreyi de kaydeder. Ölçülen her işin sonucu bir "kontrol" değeri olarak stdout'a yazılır: sonucu kullanılmayan bir döngü `-O2`'de silinebilirdi (Hafta 1, Kaputun Altında).

Yol haritasındaki karşılığı (Tablo A.1): **H1 · v2.0 · Sentetik veri üreteci (10³–10⁶ kayıt), zamanlayıcı modülü, kâhin test altyapısı · Ortak LCG, ölçüm düzeni, karşılaştırmalı test.**

## 2. v1.0'dan ne değişti?

| Konu | v1.0 (AP-1 H14) | v2.0 (AP-2 H1) |
|---|---|---|
| Veri | klavyeden girilen kayıtlar; 8 kayıtlık örnek dosya | `veri_uret`: 1 … 10⁷ kayıt, `--tohum`, `--yinelenen k`; aynı tohum → aynı dosya |
| CSV yazımı | `csv_yaz` tek parça | `csv_basligi_yaz` + `csv_satiri_yaz` (üreteç 10⁶ kaydı bellekte tutmadan satır satır yazar); `csv_yaz` bunları çağırır, çıktı AYNI |
| Ölçüm | yok | `deney.h/.c` (ısınma + K tekrar, ortanca, ilk, ortalama, en az/en çok) ve `olcer` (6 işlem, CSV çıktısı, `--ekle`) |
| Testler | 99 birim doğrulama | 110 birim doğrulama (+11 üreteç) ve `test_kahin` (varsayılan 300 deneme; `--hata-goster`) |
| Derleme | `-g` | `-O2 -g` (ölçüm için); `make olcum`, `make temiz`; `make asan` UBSan hatalarını ölümcül yapar (`-fno-sanitize-recover=all`) |
| Kayıt modeli, CSV ve MOBS biçimleri, yükleyici, menü | — | **değişmedi**: v1.0'ın T2 oturumu v2.0'da program başlığı dışında birebir aynı çıktıyı verir (bölüm 7) |

## 3. Mimari

![Mini-OBS 2 v2.0 program × modül bağımlılıkları](mini_obs_v2_0_mimari.png)

| Modül | Durum | Sorumluluk | Başlıca fonksiyonlar |
|---|---|---|---|
| `metin.h/.c` | v1.0'dan aynen | güvenli satır girdisi, sayı çözümleme, ad normalleştirme | `tamsayi_coz`, `ad_normallestir`, `ad_gecerli_mi` |
| `obs.h/.c` | v1.0'dan (yalnız başlık) | kayıt tipleri, kurallar, istatistik, raporlar | `ders_istatistigi`, `min_max_indis`, `sinif_numara_bul` |
| `dosya.h/.c` | v1.0'dan; `csv_yaz` bölündü | CSV ve ikili kalıcılık, güvenli kaydetme | `csv_oku`, `csv_satiri_yaz`, `sinif_yukle` |
| `uretec.h/.c` | **yeni** | sentetik öğrenci verisi (ortak LCG, Fisher–Yates) | `uretec_numaralar`, `uretec_ogrenci`, `uretec_sinif`, `uretec_csv_yaz` |
| `deney.h/.c` | **yeni** | ölçüm düzeni (zamanlayici üzerine) | `deney_olc` → `DeneySonucu` |
| `ortak_rastgele`, `zamanlayici` | ortak, **değiştirilmeden kopyalandı** | 64 bit LCG; duvar saati, ortanca | `rastgele_tohum`, `rastgele_karistir`, `zaman_sn`, `ortanca` |

*Şekil 1. Program × modül bağımlılıkları (● program o modüle bağlanır).*

Programlar: `mini_obs` (v1.0'ın menülü uygulaması), `veri_uret` (üreteç), `olcer` (ölçüm), `test_kahin` (kâhin testleri), `obs_test` (birim testleri). Yeni işlevler ayrı programlardadır; `main.c` ve menü değişmemiştir.

## 4. Kullanım

### 4.1 `veri_uret` — sentetik veri

```
./veri_uret --n N [--tohum T] [--yinelenen K] [--cikti dosya.csv]
  N: 1 … 10 000 000 kayıt · T >= 0 (varsayılan 42) · K: 0 … N-1 (varsayılan 0)
  --cikti yoksa CSV standart çıktıya, özet stderr'e yazılır; süre her zaman stderr'e.
```

Gerçek çıktı (`mini_obs_v2_0_ciktilar.txt`, bölüm 2):

```
$ ./veri_uret --n 5 --tohum 42
Üretildi: 5 kayıt (tohum 42, yinelenen 0, farklı numara 5) → standart çıktı
no;ad;soyad;ALG_vize;ALG_final;MAT_vize;MAT_final;FIZ_vize;FIZ_final
2400000001;MEHMET;ÜNAL;75;76;40;40;75;63
2400000004;İSMAİL;ERDOĞAN;30;34;38;23;54;25
2400000002;MERVE;ACAR;72;48;52;47;55;64
2400000003;BERK;KARA;82;71;93;98;60;63
2400000005;ONUR;ÜNAL;46;33;28;21;42;41
Süre: 0.000 s
[çıkış kodu: 0]
```

Üretilen dosya v1.0 biçimindedir (başlık `no;ad;soyad;ALG_vize;ALG_final;MAT_vize;MAT_final;FIZ_vize;FIZ_final`) ve AP-1'in **özgün** v1.0 programıyla da yüklenir (`v1.0/mini_obs`: AP-1 v1.0 kaynaklarından değiştirilmeden derlenmiş program):

```
$ printf '6\n10\n' | v1.0/mini_obs a.csv | grep 'Yüklendi\|Öğrenci sayısı'
Yüklendi: 1000 kayıt (a.csv)
Öğrenci sayısı: 1000
[çıkış kodu: 0]
```

`--yinelenen K` ile üretilen dosya, v1.0'ın mükerrer numara kuralına takılır ve program başlamaz (çıkış kodu 1; satır numarası ilk yinelenen satırdır):

```
$ stdbuf -o0 ./mini_obs y3.csv < /dev/null 2>&1 | grep -v '^='
  MİNİ-OBS 2 v2.0 · Öğrenci Not Sistemi
Hata: y3.csv okunamadı: dosya biçimi hatalı (satır 495)
[çıkış kodu: 1]
```

### 4.2 `olcer` — süre ölçümü

```
./olcer İŞLEM [--n N1,N2,...] [--tekrar K] [--tohum T] [--csv dosya.csv [--ekle]]
  uretim     n kayıtlık CSV üretimi (geçici dosyaya)
  yukleme    n kayıtlık CSV'nin v1.0 yükleyicisiyle (sinif_yukle) yüklenmesi
  denetim    yükleyicideki mükerrer numara denetimi TEK BAŞINA (bellekte)
  tarama     bulunamayan numara için tek tam tarama (sinif_numara_bul)
  istatistik üç dersin istatistikleri + harf dağılımı (bellekte)
  arama      kayıtlı numaraların aranması (süre arama başına)
```

stdout'a yalnızca deterministik "kontrol" değerleri (ölçülen işin sonucu) yazılır; süreler stderr'e ve `--csv` ile CSV'ye gider (sütunlar: `islem;n;tekrar;ic_tekrar;ortanca_ms;ortalama_ms;en_az_ms;en_cok_ms;ilk_ms;isinma_ms;kontrol`; süreler **işlem başına**). `--ekle`, pahalı boyutları daha az tekrarla ayrı çalıştırıp aynı CSV'de toplamak içindir.

### 4.3 `test_kahin` — kâhinle karşılaştırmalı test

```
./test_kahin [--deneme D] [--tohum T] [--hata-goster]
  D: deneme sayısı (varsayılan 300) · T: ilk tohum (varsayılan 1)
  --hata-goster: min_max_indis yerine KASITLI HATALI bir sürüm sınanır
```

## 5. Tasarım kararları

![Veri üretecinin üç alt akışı](mini_obs_v2_0_uretec.png)

*Şekil 2. Veri üreteci: numaralar (Fisher–Yates), yinelenenler ve ad/not alt akışları (n = 6, tohum 42 için gerçek değerler).*

1. **Benzersiz numara, arama yapmadan.** Numaralar `2400000001 … 2400000000 + n` aralığının bir permütasyonudur: önce `sira[i] = i` dizisi kurulur, sonra ortak modülün `rastgele_karistir` fonksiyonu (Fisher–Yates) ile karıştırılır (Cormen vd., 2022). Permütasyon her değeri bir kez içerdiği için benzersizlik **yapı gereğidir**; "rastgele numara üret, daha önce verildiyse yenisini dene" yaklaşımı bir üyelik denetimi (arama ya da karma tablosu) gerektirirdi. Üretim Θ(n) zaman ve n tamsayılık ek bellek ister (Şekil 2, üst bant).
2. **Üç alt akış.** Numaralar `tohum`, yinelenen seçimi `tohum + 1`, ad ve notlar `tohum + 2` ile üretilir. Böylece aynı tohumla `k = 0` ve `k = 3` dosyaları **yalnızca 3 satırın numara alanında** ayrışır (çıktılar bölüm 2: `diff` üç satır gösterir); öğrenci yinelenen eklemenin veriyi başka hiçbir yerde bozmadığını görür.
3. **Yinelenen ekleme kuralı.** Karışık bir sıranın ilk k elemanı "hedef", geri kalanlardan rastgele biri "kaynak" olur; hedef kaynağın numarasını alır. Kaynak hiçbir zaman hedef olmadığından farklı numara sayısı **tam olarak n − k** olur (kâhin testinde sıralama ile doğrulanır). Aynı kaynağı iki hedef seçerse o numara üç kez geçer; bu, v2.1'deki "tüm çiftler" listesinin neden k'den fazla çift içerebileceğini açıklar.
4. **Akış hâlinde yazım.** `uretec_csv_yaz` kayıtları bellekte toplamaz: 10⁶ kayıt için 144 MB'lık yapı dizisi yerine yalnızca 8 MB'lık numara dizisi ayrılır. Aynı kaydı üreten `uretec_sinif` ile `csv_yaz` zincirinin **bayt bayt aynı** dosyayı verdiği birim testinde sınanır.
5. **Gerçekçi ve eşitlik içeren notlar.** Her öğrenciye 20–95 arasında bir "yetenek" verilir; vize yetenek ± 20, final yetenek ± 25'tir (0–100'e kırpılır). Notlar tamsayıdır; bu yüzden aynı ortalamayı alan öğrenciler sıktır. Eşitlikler, "en büyük elemanın **ilk** indisi" gibi sözleşmeleri sınamak için değerlidir (bölüm 8, hata gösterimi).
6. **Altın satır.** `./veri_uret --n 3 --tohum 42` çıktısının ilk veri satırı (`2400000003;MEHMET;ÜNAL;75;76;40;40;75;63`) birim testine gömülüdür; üreteçte ya da ortak LCG'de yapılan istem dışı bir değişiklik bu testi bozar. Bu makinede `./veri_uret --n 1000 --tohum 42` dosyasının SHA-256 özeti şudur: `9135d0d8f8f21c343304f5937aa456c535996355f7889dbef855a455aee3a290`.
7. **Ölçüm düzeni ve kontrol değeri.** `deney_olc` ortak `zamanlayici` modülünün `zaman_sn` ve `ortanca` fonksiyonlarını kullanır; düzeni `olc_ortanca` ile aynıdır (1 ısınma + K tekrar), ek olarak ilk ölçümü, ortalamayı, en az ve en çok süreyi döndürür. Her görev, yaptığı işin sonucunu `kontrol` alanına yazar ve `olcer` bu değeri stdout'a basar; derleyici sonucu kullanılan işi silemez. Kısa işlemler (tarama, arama) bir ölçümde birçok kez yapılır (`ic_tekrar`) ve süre işlem başına bölünür; böylece zamanlayıcı çözünürlüğünün altına inilmez.
8. **Kâhin tasarımı.** Kâhin, sınanan koddan **farklı bir yoldan** hesaplamalıdır: en büyük/en küçük değer `qsort` ile (yalnızca kâhin olarak; Yol Haritası 6.5), standart sapma ortalamayı hiç kullanmayan σ² = (1/(2n²)) Σᵢ Σⱼ (xᵢ − xⱼ)² özdeşliğiyle (O(n²)), başarılı/şartlı sayıları harf indisiyle, harf dağılımı ise `harf_notu` **metniyle** sayılır. Deneme boyutları yalnızca tohumdan türetilir (bir uyuşmazlık `--tohum t --deneme 1` ile aynen yeniden üretilir) ve denemelerin yaklaşık dörtte biri sınır durumlarına (n = 1 … 3) yönlendirilir. Uyuşmazlıkta karşı örnek, hatayı hâlâ gösteren **en kısa önek** bulunarak küçültülür.
9. **Kısa yol yok.** v1.0 yükleyicisinin karesel davranışı ölçülmüş ve açıklanmıştır, ama "hızlansın" diye mükerrer numara denetimi kaldırılmamış ya da gevşetilmemiştir: doğruluğu bozan bir kısa yol, ölçümü anlamsız kılardı. İyileştirme doğru algoritmalarla yapılacaktır: yükleyicinin mükerrer denetimi H4'te (v2.3) ikili aramayla Θ(n log n) karşılaştırmaya iner ama kayıt kaydırmaları karesel kalır; H6'da (v2.5) toplu yükleme ve birleştirmeli sıralamayla yükleme bütünüyle Θ(n log n) olur. H10'un sürümü (v2.9) ise yükleyiciyi değil, yinelenen numara tespitini karma tablosuyla ortalama O(n)'e indirir.

## 6. Ölçümler

### 6.1 Ölçüm düzeni ve ortam

Makine: Intel(R) Xeon(R) Processor @ 2.80GHz, **2 çekirdek** (sanal makine; başka süreçler çalışıyor olabilir), L2 önbellek 2 MiB (2 × 1 MiB, çekirdek başına), L3 önbellek 33 MiB (paylaşılan). Derleyici: gcc 13.3.0 (Ubuntu 13.3.0-6ubuntu2~24.04.1), bayraklar `-std=c17 -Wall -Wextra -pedantic -O2 -g`. Tarih: 2026-10-12 22:32 (`olcum/OLCUM_ORTAMI.txt`). Düzen (Sedgewick & Wayne, 2011'deki deneysel analiz yaklaşımıyla): her boyut için 1 ısınma + K tekrar, **ortanca**; ucuz ama gürültülü küçük boyutlarda K = 11, 32 000'de K = 5; karesel yükleme 64 000 kayıtta ≈ 6 s, 100 000 kayıtta ≈ 17 s sürdüğü için bu iki boyutta K = 3 ve K = 1 (süre bütçesi). Bütün sayılar `olcum/*.csv`'den alınmıştır; `make olcum` toplam 1 dk 48 s sürdü (günlük: `mini_obs_v2_0_ciktilar.txt`). İlk çalıştırmada küçük boyutlardaki yükleme ölçümü tutarsız çıktı (2 000 kayıtta en az ile en çok arasında üç kat fark); küçük boyutların tekrar sayısı 11'e çıkarılıp ölçüm yenilendi. Bu, H1'in "tek ölçüme güvenme" dersinin bu projedeki ilk örneğidir (bölüm 6.6).

### 6.2 Bulgu: v1.0 yükleyicisi karesel zamanlıdır

v1.0'ın `csv_oku` fonksiyonu her satırı çözdükten sonra `sinif_numara_bul(s, o.no)` ile **o ana kadar yüklenmiş bütün kayıtları** doğrusal olarak tarar (mükerrer numara kuralı). i. kayıt (0'dan) için i karşılaştırma yapılır; numaralar benzersizse toplam

  0 + 1 + 2 + … + (n − 1) = n(n − 1) / 2 karşılaştırma

eder: yükleme **Θ(n²)**'dir. (`ikili_oku` da aynı denetimi yapar.) `olcer yukleme` dosyadan gerçek yüklemeyi, `olcer denetim` ise aynı denetimi bellekte **tek başına** ölçer:

| n | tekrar | yükleme (ortanca) | en az – en çok | yalnız denetim | denetim / yükleme | T(n) / T(n/2) |
|--:|--:|--:|--:|--:|--:|--:|
| 1 000 | 11 | 1,5 ms | 1,4 ms – 1,7 ms | 201,0 µs | %14 | — |
| 2 000 | 11 | 4,0 ms | 3,3 ms – 5,8 ms | 834,0 µs | %21 | 2,69 |
| 4 000 | 11 | 8,5 ms | 8,3 ms – 8,9 ms | 3,7 ms | %44 | 2,14 |
| 8 000 | 11 | 25,3 ms | 24,8 ms – 26,2 ms | 16,2 ms | %64 | 2,97 |
| 16 000 | 11 | 166,8 ms | 148,5 ms – 225,9 ms | 133,5 ms | %80 | 6,59 |
| 32 000 | 5 | 1,24 s | 1,13 s – 1,35 s | 1,33 s | %107 | 7,45 |
| 64 000 | 3 | 6,35 s | 6,07 s – 6,54 s | 5,85 s | %92 | 5,10 |
| 100 000 | 1 | 17,06 s | 17,06 s – 17,06 s | — | — | — |

*Tablo 1. v1.0 yükleyicisinin süresi (bu makinede ölçülen; ortanca; en az – en çok aralığı). "Yalnız denetim" yükleyicideki mükerrer numara denetiminin aynısıdır; farklı bir çalıştırmada ölçüldüğü için gürültü nedeniyle yüklemeyi küçük farkla aşabilir.*

![v1.0 yükleyicisi, mükerrer denetimi ve doğrusal işlemler (log–log)](mini_obs_v2_0_olcum_yukleme.png)

*Şekil 4. Yükleme, yalnız denetim, CSV üretimi ve istatistik süreleri (log–log; içi boş daireler kestirim).*

Yorum:

- **Küçük n'de** (≤ 8 000) satır ayrıştırma (dosyadan okuma, `strtod`, ad normalleştirme) baskındır: kayıt başına ≈ 1,28 µs. Bu bölgede log–log eğim yalnızca 1,34 olarak ölçülür; büyüme doğrusala yakın görünür.
- **n ≥ 16 000'de** yüklemenin büyük bölümü (%80 ve üstü) mükerrer numara denetimidir; log–log eğim **2,52** olarak ölçülür. Kuram (Θ(n²)) n'i ikiye katlayınca süre oranını **4** öngörür; ölçülen oranlar ise sırasıyla 6,6 · 7,5 · 5,1 olarak bulunur. Fazlalık algoritmadan değil **bellek hiyerarşisinden** gelir (bölüm 6.3): dizi büyüdükçe karşılaştırma başına süre de büyür.
- 10⁵ kayıt **17,1 s**'de yüklenir; aynı veride üç dersin istatistiği 9,8 ms sürer. Darboğaz istatistik değil, yüklemedir.

Bu durum Hafta 2'nin Gerçek Dünyadan örneğinin küçük bir kopyasıdır: GTA Online'ın uzun yükleme süresinin ikinci nedeni, yaklaşık 63 000 kaydın her birinin eklenirken bütün diziyle karşılaştırılmasıydı (t0st, 2021). Mini-OBS'de aynı desen "mükerrer numara kuralı" kılığındadır.

### 6.3 Neden oran 4'ten büyük? Kaputun altında: önbellek

`olcer tarama`, bulunamayan bir numara için diziyi baştan sona tarar; süreyi kayıt sayısına bölerek **kayıt başına** maliyeti verir. Kayıt `sizeof(Ogrenci)` = 144 bayttır; tarama her kayıttan yalnızca 8 baytlık `no` alanını okur ama işlemci her seferinde 64 baytlık bir önbellek satırı getirir.

| n | dizi (MB) | kayıt başına (ns) | dizi nerede? |
|--:|--:|--:|:--|
| 1 000 | 0,1 | 0,43 | L2'de |
| 4 000 | 0,6 | 0,48 | L2'de |
| 8 000 | 1,2 | 0,55 | L3'te |
| 12 000 | 1,7 | 1,08 | L3'te |
| 16 000 | 2,3 | 1,78 | L3'te |
| 32 000 | 4,6 | 3,17 | L3'te |
| 64 000 | 9,2 | 3,63 | L3'te |
| 128 000 | 18,4 | 3,43 | L3'te |
| 192 000 | 27,6 | 4,08 | L3'te |
| 256 000 | 36,9 | 7,07 | ana bellekte |
| 384 000 | 55,3 | 10,29 | ana bellekte |
| 512 000 | 73,7 | 11,97 | ana bellekte |
| 1 000 000 | 144,0 | 10,51 | ana bellekte |

*Tablo 2. Tek tam taramada kayıt başına süre (bu makinede ölçülen). L2 = 1 MiB ≈ 7 281 kayıt; L3 = 33 MiB ≈ 240 298 kayıt.*

![Kayıt başına tarama süresi ve önbellek sınırları](mini_obs_v2_0_olcum_tarama.png)

*Şekil 5. Tek tam taramada kayıt başına süre; kesikli çizgiler L2 ve L3 önbelleğine sığan kayıt sayısı.*

Dizi L2'ye sığarken kayıt başına ≈ 0,43–0,48 ns, L3'te ≈ 3,2–3,6 ns, ana bellekte ≈ 10–14 ns ölçülür: **aynı karşılaştırma, dizinin nerede durduğuna göre 21–32 kat pahalılaşır.** RAM modelinin "her temel işlem birim maliyetlidir" varsayımı (H2) asimptotik sınıfı doğru verir, sabit çarpanı vermez. Yükleme sırasında dizi büyüdükçe kayıtlar L2'den L3'e, sonra ana belleğe taşar; bu yüzden ölçülen katlama oranı 4'ün üstündedir ve eğim 2'yi aşar.

### 6.4 10⁶ kayıt için kestirim

10⁶ kayıtlık yükleme ölçülmedi (süre bütçesini saatlerle aşar); **kestirildi**. İki yöntem:

1. **Kaba kestirim** (yalnızca n² büyümesi): T(10⁶) ≈ 100 · T(10⁵) = **1 706 s ≈ 28 dakika.** Önbellek etkisini yok sayar; dizi 10⁵'te L3'te (14,4 MB), 10⁶'da ana bellektedir (144 MB). Bu yüzden düşük kalır.
2. **Tarama tabanlı model:** T(n) ≈ a · n + Σᵢ₌₀ⁿ⁻¹ i · c(i). Burada a = 1,28 µs/kayıt ayrıştırma maliyeti (n ≤ 8 000'de yükleme − denetim farkından), c(m) ise Tablo 2'deki ölçülmüş kayıt başına tarama süresidir (ara değerler doğrusal). Toplam, ∫₀ⁿ x · c(x) dx integraliyle hesaplanır (`olcum/kestirim.py`). Model, ölçülen boyutlarda şu sapmalarla tutar:

| n | ölçülen yükleme | model | fark |
|--:|--:|--:|--:|
| 8 000 | 25,3 ms | 26,3 ms | +4,0% |
| 16 000 | 166,8 ms | 150,9 ms | −9,5% |
| 32 000 | 1,24 s | 1,24 s | −0,5% |
| 64 000 | 6,35 s | 6,52 s | +2,8% |
| 100 000 | 17,06 s | 17,07 s | +0,1% |

*Tablo 3. Tarama tabanlı modelin ölçülen yüklemeyle karşılaştırılması.*

Model ölçülen değerleri 8 000–100 000 kayıtta en çok %9,5 sapmayla öngördüğü için 10⁶'ya genişletilir: **T(2·10⁵) ≈ 74 s, T(5·10⁵) ≈ 1 076 s, T(10⁶) ≈ 5 785 s ≈ 1,6 saat (kestirim).** Kaba kestirim, modelin bulduğu sürenin yalnızca 0,29 katıdır. Sonuç her iki yöntemde de aynıdır: v1.0 yükleyicisiyle 10⁶ kayıt **pratikte yüklenemez**. Karşılaştırma için aynı 10⁶ kayıt `veri_uret` ile 1,88 s'de üretilir ve bellekte üç dersin istatistiği 112,7 ms sürer.

### 6.5 Doğrusal işlemler

| n | CSV üretimi | istatistik (3 ders + harf) | arama (arama başına) |
|--:|--:|--:|--:|
| 1 000 | 2,7 ms | 57,7 µs | 370 ns |
| 10 000 | 18,1 ms | 755,1 µs | 2,8 µs |
| 100 000 | 185,5 ms | 9,8 ms | 169,9 µs |
| 1 000 000 | 1,88 s | 112,7 ms | 4,8 ms |

*Tablo 4. Doğrusal (Θ(n)) işlemler; ortanca (CSV üretimi 3, diğerleri 5 tekrar). Arama süresi tek arama içindir (kayıtlı rastgele numaralar; ortalama ≈ n/2 karşılaştırma).*

Log–log eğimler: CSV üretimi 0,95, istatistik 1,10. n on katına çıkınca süre de ≈ on katına çıkar. Doğrusal arama da Θ(n)'dir, ama 10⁴ → 10⁵ adımında arama başına süre ≈ 61 katına çıkar: dizi bu aralıkta L2'den taşar (bölüm 6.3). Asimptotik sınıf aynı kalsa da sabit çarpanın bellek hiyerarşisine bağlı olması, H2'nin "birim maliyet varsayımının sınırları" konusunun ölçülmüş bir örneğidir.

### 6.6 Tek ölçüm, ortalama ve ortanca

| n | tekrar | tek ölçüm (ilk) | ortanca | ortalama | yayılım (en çok − en az) / ortanca | tek ölçümün ortancadan farkı |
|--:|--:|--:|--:|--:|--:|--:|
| 1 000 | 11 | 1,4 ms | 1,5 ms | 1,5 ms | %20 | −4,3% |
| 2 000 | 11 | 3,3 ms | 4,0 ms | 4,3 ms | %62 | −16,6% |
| 8 000 | 11 | 26,1 ms | 25,3 ms | 25,4 ms | %6 | +3,4% |
| 16 000 | 11 | 169,8 ms | 166,8 ms | 171,4 ms | %46 | +1,8% |
| 32 000 | 5 | 1,30 s | 1,24 s | 1,25 s | %17 | +4,5% |
| 64 000 | 3 | 6,54 s | 6,35 s | 6,32 s | %7 | +3,1% |

*Tablo 5. Yüklemede tek ölçüm (ısınmadan sonraki ilk ölçüm), ortanca ve yayılım.*

Tek ölçüm ile ortanca arasındaki fark %2 ile %17 arasında; en çok ile en az arasındaki yayılım ise ortancanın %6 ile %62 arasında değişir ve en büyük yayılımlar milisaniyeler süren işlerde görülür. Saniyeler süren büyük boyutlarda tek ölçüm ile ortanca arasındaki fark yüzde birkaçtır. Tek ölçümle karar vermek, özellikle kısa işlerde yanıltıcıdır; ortanca, arada bir gelen gecikmelerden (başka süreçler, sanal makine) etkilenmez. Öğrenciden aynı tabloyu **kendi makinesinde** üretmesi istenir; sayılar farklı olacak, ama "karesel + önbellek" deseni aynı kalacaktır.

### 6.7 Sonuç ve sarmal

Mükerrer numara denetimi, dönemin ilk "aynı problem, daha iyi algoritma" sarmalının başlangıcıdır (Yol Haritası Tablo 4.2): **H2 (v2.1)** yinelenen tespitini tüm çiftlerle O(n²) yazıp oran testiyle ölçecek, **H6 (v2.5)** sıralayıp komşuları karşılaştırarak O(n log n)'e, **H10 (v2.9)** karma tablosuyla ortalama O(n)'e indirecektir. Her sürüm bu belgedeki veri üreteci, ölçüm düzeni ve kâhin altyapısıyla doğrulanır.

## 7. Testler

- **Birim testleri** (`obs_test`): `110 doğrulama: 37 kural + 22 metin + 24 yapı + 16 dosya + 11 üreteç`. Üreteç testleri: havuzdaki her adın normalleştirilmiş ve geçerli olması; parametre sınırları; k = 0'da numaraların `TABAN+1 … TABAN+n` permütasyonu olması (ama sıralı olmaması); aynı tohum → aynı dizi, farklı tohum → farklı dizi; k = 7'de tam 7 konumun değişmesi ve farklı numara sayısının n − 7 olması; notların 0–100 tamsayı olması; akışla yazımın `csv_yaz` ile bayt bayt aynı olması; v1.0 yükleyicisiyle gidiş-dönüş; yinelenenli dosyanın reddi; altın satır.
![Kâhinle karşılaştırmalı test döngüsü](mini_obs_v2_0_kahin.png)

*Şekil 3. Kâhinle karşılaştırmalı test döngüsü: aynı rastgele girdi hem sınanan fonksiyona hem kâhine verilir; uyuşmazlıkta tohum ve küçültülmüş karşı örnek raporlanır.*

- **Kâhin testleri** (`test_kahin`): varsayılan 300 deneme ve 12 000 denetim; 1 000 denemede 40 000 denetim, hepsi geçti. Kasıtlı hatalı sürüm (`--hata-goster`: `>`/`<` yerine `>=`/`<=`, eşitlikte SON indis) ilk uyuşmazlıkta durur:

```
$ ./test_kahin --hata-goster
KÂHİN UYUŞMAZLIĞI (tohum 3)
  İşlev      : min_max_indis
  n          : 60
  Beklenen   : enk = 3, enb = 0 (sıralama + ilk indis)
  Bulunan    : enk = 36, enb = 58
  Karşı örnek: a = [1.25, 0.75, 0.25, 0, 0.5, 0.75, 1, 1.25, 0.75, 0.25, 0.25, 0.5, 1.25, 1, 1.25, 0, 1.25, 1.25, 0.25, 0.25, ...]
  Küçültülmüş karşı örnek (ilk 8 eleman): beklenen enk = 3, enb = 0; bulunan enk = 3, enb = 7
  Karşı örnek: a = [1.25, 0.75, 0.25, 0, 0.5, 0.75, 1, 1.25]
  Yeniden üretmek için: ./test_kahin --tohum 3 --deneme 1 --hata-goster
[çıkış kodu: 1]
```

  60 elemanlı karşı örnek 8 elemana küçültülmüştür: değeri en büyük olan 1,25 hem 0. hem 7. konumdadır; doğru sözleşme ilk indisi (0), hatalı sürüm son indisi (7) verir. Değer doğru, indis yanlış: **yalnızca değeri denetleyen bir test bu hatayı göremezdi.**
- **Regresyon**: v1.0'ın `T2_ornek_veri` oturumu iki programda da çalıştırılıp `diff` ile karşılaştırıldı; tek fark program başlığıdır:

```
$ cp ornek_veri/ogrenciler.csv ogrenciler.csv && ./mini_obs ogrenciler.csv < testler/T2_ornek_veri.txt > v20_T2.txt; cp ornek_veri/ogrenciler.csv ogrenciler.csv && v1.0/mini_obs ogrenciler.csv < testler/T2_ornek_veri.txt > v10_T2.txt; diff v10_T2.txt v20_T2.txt; wc -l < v20_T2.txt
2c2
<   MİNİ-OBS v1.0 · Öğrenci Not Sistemi
---
>   MİNİ-OBS 2 v2.0 · Öğrenci Not Sistemi
165
[çıkış kodu: 0]
```

- **Bellek**: `make asan` (ASan + UBSan + LSan; UBSan hataları ölümcül) ve `make valgrind` temiz (çıktılar dosyanın sonunda).

## 8. Ders notu için özet (Hafta 1 · Mini-OBS 2 adımı)

**Bu hafta:** Mini-OBS v1.0'ı ölçeklemeye hazırlıyoruz: tekrarlanabilir büyük veri, güvenilir süre ölçümü ve kâhinle test. Kayıt modeline, dosya biçimlerine ve menüye dokunmuyoruz.

### Gereksinimler

- `uretec.c`: `uretec.h`'deki dört fonksiyon. Numaralar `2400000001 … 2400000000 + n` aralığının `rastgele_karistir` ile karıştırılmış hâli; `k` yinelenen için karışık bir sıranın ilk k elemanı hedef, geri kalanlardan `rastgele_aralik` ile seçilen biri kaynak. Üç alt akış: `tohum`, `tohum + 1`, `tohum + 2`. Ad/soyad verilen havuzlardan; yetenek 20–95, vize ± 20, final ± 25, 0–100'e kırpma. `rand()` kullanılmaz.
- `veri_uret.c`: `--n`, `--tohum`, `--yinelenen`, `--cikti` argümanları; geçersiz argümanda kullanım iletisi ve çıkış kodu 2; dosya açılamazsa 1; süre yalnızca stderr'e.
- `dosya.c`: `csv_yaz`'ın içini `csv_basligi_yaz` ve `csv_satiri_yaz` olarak ayırın (çıktı değişmemeli).
- `deney.c`: 1 ısınma + K tekrar; ortanca, ilk, ortalama, en az, en çok (`zaman_sn`, `ortanca` kullanılarak).
- `olcer.c`: en az `yukleme`, `istatistik`, `arama` işlemleri; stdout'a deterministik kontrol değeri, stderr'e ve CSV'ye süre.
- `test_kahin.c`: en az üç fonksiyon için kâhin (ör. `min_max_indis` ↔ sıralama + ilk indis; `dizi_ortalama` ↔ long double toplam; `standart_sapma` ↔ ikili fark özdeşliği); uyuşmazlıkta tohum, n, beklenen/bulunan ve karşı örnek; çıkış kodu 1.
- `Makefile`: `make`, `make test`, `make olcum`, `make asan`, `make temiz`.

### İpuçları

- Benzersizlik için "üret ve denetle" yerine **permütasyon** kullanın; denetim istiyorsanız bile önce bunun kaç karşılaştırma tutacağını hesaplayın.
- Alt akışlar için `rastgele_tohum(tohum + 1)` gibi yeniden tohumlama yeterlidir; böylece `--yinelenen` ad ve notları değiştirmez.
- 10⁶ kaydı `Sinif` dizisine toplamayın; satırı üretip hemen `csv_satiri_yaz` ile yazın.
- Ölçtüğünüz işin sonucunu bir değişkende biriktirip yazdırın; aksi hâlde `-O2` döngüyü silebilir.
- Kısa işlemleri bir ölçümde 10³–10⁴ kez tekrarlayıp süreyi işlem sayısına bölün.
- Kâhin, sınanan koddan farklı bir yoldan hesaplamalı; aynı fonksiyonu iki kez çağırmak kâhin değildir.
- Test boyutlarını deneme sırasından değil **tohumdan** türetin; o zaman "`--tohum t --deneme 1`" hatayı aynen yeniden üretir.

### Kabul ölçütleri (denetlenebilir)

1. `make` ve `make test` `-std=c17 -Wall -Wextra -pedantic -O2` ile **sıfır uyarı** verir; bütün birim ve kâhin testleri geçer (`test_kahin` varsayılan 300 denemede 0 uyuşmazlık).
2. `./veri_uret --n 3 --tohum 42` çıktısının ilk veri satırı `2400000003;MEHMET;ÜNAL;75;76;40;40;75;63`'tür; `./veri_uret --n 1000 --tohum 42` dosyasının SHA-256 özeti `9135d0d8f8f21c34…` ile başlar (verilen havuzlar ve tanımlı üretim sırasıyla).
3. Aynı argümanlarla iki çalıştırma bayt bayt aynı dosyayı verir (`cmp`); `--n 10^6` dosyası 1 000 001 satırdır ve `sort -t';' -k1,1 -u` ile 1 000 001 benzersiz satır kalır (bu makinede üretim 1,908 s sürdü).
4. `--yinelenen K` dosyası K = 0 dosyasından yalnızca K satırın numara alanında ayrışır; `mini_obs` bu dosyayı "dosya biçimi hatalı (satır s)" ile reddeder ve 1 ile çıkar.
5. Üretilen her dosya `mini_obs` ile yüklenir (ör. 1 000 kayıt: "Yüklendi: 1000 kayıt").
6. `olcer` stdout'u aynı argümanlarla her çalıştırmada aynıdır (yalnızca kontrol değerleri); CSV'de her n için ortanca, en az, en çok ve ilk ölçüm vardır.
7. `--hata-goster` ile kâhin hatalı `min_max_indis`'i yakalar, tohum ve en çok 20 elemanlık bir karşı örnek basar, 1 ile çıkar.
8. Ölçüm raporunda (kendi makinenizde) yükleme için en az altı n değeri (10³ … 10⁵), katlama oranları ve log–log grafik bulunur; 10⁶ için yapılan **kestirim** açıkça "kestirim" diye belirtilir.
9. `make asan` hata ve sızıntı raporlamaz.

### Test senaryoları

| # | Girdi | Beklenen çıktı / davranış |
|---|---|---|
| 1 | `./veri_uret --n 5 --tohum 42` | başlık + 5 satır; numaralar 2400000001–2400000005'in bir permütasyonu; çıkış 0 |
| 2 | aynı komut iki kez, `--cikti a.csv` / `b.csv` | `cmp a.csv b.csv` fark bulmaz |
| 3 | `--tohum 43` | `a.csv`'den farklı dosya |
| 4 | `--n 1000 --tohum 42 --yinelenen 3` | `diff` tam 3 satır gösterir; "farklı numara 997" |
| 5 | `./veri_uret --tohum 42` (n yok) | kullanım iletisi, çıkış 2 |
| 6 | `--n 5 --yinelenen 5` | kullanım iletisi, çıkış 2 (K < N olmalı) |
| 7 | `--cikti /olmayan_klasor/x.csv` | "Hata: … açılamadı", çıkış 1 |
| 8 | `printf '6\n10\n' \| ./mini_obs a.csv` | "Yüklendi: 1000 kayıt"; istatistik tablosu |
| 9 | `./mini_obs y3.csv` | "dosya biçimi hatalı (satır s)", program başlamaz, çıkış 1 |
| 10 | `./test_kahin` | "Kâhin testleri geçti: 300 deneme …", çıkış 0 |
| 11 | `./test_kahin --hata-goster` | "KÂHİN UYUŞMAZLIĞI (tohum t)", küçültülmüş karşı örnek, çıkış 1 |
| 12 | `./olcer yukleme --n 1000,2000,4000 2>/dev/null` | üç satır, `kontrol = n`; her çalıştırmada aynı |
| 13 | `./olcer siralama` | kullanım iletisi, çıkış 2 |

### Başlangıç noktası (öğrenciye verilenler)

- **Verilir:** kendi v1.0'ınız (ya da referans v1.0), ortak modüller `ortak_rastgele.h/.c` ve `zamanlayici.h/.c` (değiştirilmez), `uretec.h` (fonksiyon bildirimleri ve üretim sırası), ad/soyad havuzları, `deney.h`, `Makefile` iskeleti.
- **Yazılır / değiştirilir:** `uretec.c`, `veri_uret.c`, `deney.c`, `olcer.c`, `test_kahin.c` (yeni); `dosya.h/.c` (`csv_yaz`'ın bölünmesi); `test_obs.c` (üreteç testleri); `obs.c`'de yalnızca program başlığı.
- **Değiştirilmez:** kayıt modeli (`obs.h`'deki yapılar), CSV ve ikili biçim, yükleyici (`csv_oku` — karesel olduğu bilinerek), menü.

## 9. Bilinen sınırlılıklar

- Yükleme 10⁵ kayıtta ≈ 17 s, 10⁶ kayıtta saatler sürer (kestirim); `mini_obs` büyük dosyalarla etkileşimli kullanılamaz. Bu bilinçli olarak düzeltilmedi (bölüm 5, karar 9).
- Ölçümler tek bir 2 çekirdekli sanal makinededir; 64 000 ve 100 000 kayıt az tekrarla (3 ve 1) ölçüldü. Önbellek boyutları ve sabit çarpanlar makineye bağlıdır.
- Kestirim modeli, kayıt başına tarama maliyetinin yalnızca dizi boyutuna bağlı olduğunu varsayar; yükleme sırasındaki `realloc` kopyalarını ve ayrıştırmanın önbellek etkisini ayrıca modellemez.
- Üretilen adlar 40 × 40'lık havuzdan seçilir; aynı ad-soyad çiftleri sık görülür (numaralar her zaman benzersizdir). Notlar tamsayıdır.
- `test_kahin` istatistik kâhinlerinde kayan nokta karşılaştırması bağıl 10⁻⁹ toleransla yapılır; ikili fark özdeşliği O(n²) olduğu için en çok 2 000 kayıtlık sınıflarda uygulanır.
- `olcer` geçici dosyayı (`olcer_gecici.csv`) çalışma klasörüne yazar ve sonunda siler; aynı klasörde iki `olcer` aynı anda çalıştırılmamalıdır.

## 10. Kaynaklar

- Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2022). *Introduction to algorithms* (4th ed.). MIT Press.
- Dahl, O.-J., Dijkstra, E. W., & Hoare, C. A. R. (1972). *Structured programming*. Academic Press.
- Sedgewick, R., & Wayne, K. (2011). *Algorithms* (4th ed.). Addison-Wesley.
- t0st. (2021, February 28). *How I cut GTA Online loading times by 70%*. https://nee.lv/2021/02/28/How-I-cut-GTA-Online-loading-times-by-70/
