# Mini-OBS 2 v2.1 — Asimptotik Analiz: işlem sayaçları, yinelenen numara tespiti ve oran testi (Hafta 2)

**Bu sürümün amacı:** v2.0'ın bulgusunu (v1.0 yükleyicisi karesel) bir **analiz problemine** dönüştürmek. (1) İstatistik ve arama fonksiyonlarına açılıp kapatılabilen **işlem sayaçları** eklenir ve her birinin T(n)'si kapalı biçimde yazılıp sayaçla birebir doğrulanır. (2) Yinelenen öğrenci numarası tespitinin **kaba kuvvet (tüm çiftler) sürümü** yazılır: `yinelenen_bul` her durumda tam n(n − 1)/2 karşılaştırma yapar; `yinelenen_var_mi` ilk eşitlikte durur (en iyi 1, en kötü n(n − 1)/2). (3) 10³–1,28·10⁵ kayıtta **oran testi** yapılır: n ikiye katlanınca süre ≈ 4 katına çıkar (bu makinede n ≥ 4 000 için ölçülen oranlar 3,78–4,48, log–log eğim 2,02). Bu sürüm, yinelenen tespiti sarmalının ilk halkasıdır ve sonraki sürümlerin (v2.5 sıralama, v2.9 karma tablosu) **kâhinidir**.

Dosyalar (satır sayılarıyla): `obs.h` (130) · `obs.c` (649) · `metin.h` (35) · `metin.c` (340) · `dosya.h` (66) · `dosya.c` (329) · `main.c` (292) · `sayac.h` (41) · `sayac.c` (17) · `yinelenen.h` (43) · `yinelenen.c` (71) · `denetle.c` (140) · `uretec.h` (54) · `uretec.c` (160) · `veri_uret.c` (94) · `deney.h` (28) · `deney.c` (32) · `olcer.c` (388) · `test_obs.c` (716) · `test_kahin.c` (695) · `ortak_rastgele.h` (42) · `ortak_rastgele.c` (50) · `zamanlayici.h` (30) · `zamanlayici.c` (55) · `Makefile` (158) · `ornek_veri/` · `testler/` (v1.0 oturumları, `bozuk.csv`, **`yinelenen_k3.csv`**: 30 kayıt, 3 kasıtlı yinelenen) · `olcum/*.csv`, `olcum/OLCUM_ORTAMI.txt` · `mini_obs_v2_1_ciktilar.txt` (315 satır, gerçek çıktılar). Şekil: `mini_obs_v2_1_ciftler.png`; grafikler: `mini_obs_v2_1_olcum_oran.png`, `mini_obs_v2_1_olcum_ns.png`.

Derleme: `make` (`mini_obs`, `veri_uret`, `olcer`, `denetle`), `make test`, `make olcum` (bu makinede 1 dk 50 s), `make asan`, `make valgrind`, `make temiz`. Bayraklar `-std=c17 -Wall -Wextra -pedantic -O2 -g`; 15 kaynak dosya `-O0 … -Os` düzeylerinde `-Werror` ile uyarısız. Çıkış kodları: 0, 1 (dosya/bellek hatası; `denetle`'de "yinelenen VAR"; testlerde uyuşmazlık), 2 (hatalı kullanım).

## 1. Amaç ve haftanın kavramıyla bağı

Hafta 2'nin Büyük Sorusu: 10⁶ elemanda 1 saniyede çalışan bir program 10⁹ elemanda ne kadar sürer ve bu soru neden programın dilinden daha önemlidir? Yanıt büyüme sınıfındadır: doğrusal bir program ≈ 1 000 s (≈ 17 dakika), karesel bir program ≈ 10⁶ s (≈ 11,6 gün) sürer. v2.1 bu soruyu Mini-OBS üzerinde sorar:

- **RAM modeli ve temel işlem** (ÖÇ 2.1): sayaçlar yalnızca *veri değerleri* arasındaki karşılaştırmaları, toplama/çıkarmaları ve çarpma/bölmeleri sayar; döngü denetimi sayılmaz. Her fonksiyonun T(n)'si kapalı biçimde yazılır ve sayaç bu formülle **birebir** karşılaştırılır.
- **En iyi / en kötü durum** (ÖÇ 2.2): `sinif_numara_bul` (1 ya da n) ve `yinelenen_var_mi` (1 ya da n(n − 1)/2) aynı problemde iki uç durumu gösterir; `yinelenen_bul` ise her girdide aynı sayıda karşılaştırma yapar (en iyi = en kötü).
- **Bağımlı iç içe döngü** (ÖÇ 2.4): `for i … for j = i + 1 …` döngüsünde iç döngü n − 1 − i kez döner: (n − 1) + (n − 2) + … + 1 = n(n − 1)/2.
- **Oran testi** (ÖÇ 2.4; Sedgewick & Wayne, 2011): n'i ikiye katlayıp süre oranını ölçmek; log–log grafikte eğimi okumak.
- **Gizli karesel kod**: GTA Online örneğinde yaklaşık 63 000 kaydın her biri eklenirken bütün diziyle karşılaştırılıyordu, yani ≈ n²/2 ≈ 1,98 milyar karşılaştırma (t0st, 2021). v2.0'da ölçtüğümüz v1.0 yükleyicisi aynı desendedir.

Yol haritasındaki karşılığı (Tablo A.1): **H2 · v2.1 · İşlem sayaçlı istatistikler; yinelenen numara tespiti (O(n²)) · Asimptotik analiz, oran testi.**

## 2. v2.0'dan ne değişti?

| Konu | v2.0 (H1) | v2.1 (H2) |
|---|---|---|
| Sayaçlar | yok | `sayac.h/.c`: `Sayac { karsilastirma, toplama, carpma }`, `SAYAC_EKLE`; `NULL` → kapalı |
| İstatistik ve arama | `dizi_ortalama`, `standart_sapma`, `min_max_indis`, `ders_istatistigi`, `sinif_numara_bul` | aynıları + sayaçlı sürümleri (`…_say`); eski adlar sayaçlıları `NULL` ile çağırır, sonuçlar AYNI |
| Yinelenen tespiti | yalnızca yükleyicinin içinde (ilk yinelenende durur) | `yinelenen.h/.c`: `yinelenen_var_mi` (erken çıkış), `yinelenen_bul` (tüm çiftler, bütün eşit çiftleri listeler), `tum_ciftler` |
| CSV okuma | `csv_oku` (mükerrer numara kuralı her zaman) | + `csv_oku_secenekli(…, numara_denetimi)`; yükleyici değişmedi, kuralsız okuma yalnızca `denetle` içindir |
| Programlar | `mini_obs`, `veri_uret`, `olcer`, `test_kahin` | + **`denetle`** (CSV'deki bütün yinelenenleri raporlar); `olcer`'e `yinelenen`, `erken` işlemleri, sayaç sütunları, kuram denetimi, `--sayac`, `--yinelenen`, katlama oranı |
| Testler | 110 birim; kâhin 12 000 denetim | 134 birim (+11 sayaç, +13 yinelenen); kâhin 57 242 denetim (+ yinelenen ve sayaç kâhinleri); `--hata-goster minmax|yinelenen` |
| `make olcum` | yükleme, tarama, doğrusal işlemler | oran testi (`yinelenen`, `erken`, `istatistik`), sayaç maliyeti, yinelenen sayısının erken çıkışa etkisi, hizalama deneyi |

## 3. Mimari

| Modül | Durum | Sorumluluk |
|---|---|---|
| `sayac.h/.c` | **yeni** | `Sayac` yapısı, `SAYAC_EKLE(sy, alan, k)` (sy `NULL` ise etkisiz), `sayac_sifirla`, `sayac_yaz` |
| `obs.h/.c` | genişletildi | `…_say` sürümleri; eski fonksiyonlar ince sarmalayıcı |
| `yinelenen.h/.c` | **yeni** | yinelenen numara tespiti (tüm çiftler / erken çıkış); H6 ve H10 sürümlerinin kâhini |
| `dosya.h/.c` | küçük ek | `csv_oku_secenekli` |
| `denetle.c` | **yeni program** | CSV'yi kuralsız okur, çiftleri raporlar, karşılaştırma sayısını kuramsal değerle birlikte yazar |
| `olcer.c` | genişletildi | sayım çalıştırması + süre ölçümü; kuram denetimi; katlama oranı |
| `metin`, `uretec`, `deney`, `veri_uret`, `main`, ortak modüller | v2.0'dan aynen | — |

Bağımlılık: `yinelenen` → `obs` + `sayac`; `obs` → `sayac` (yalnızca makro ve yapı); `denetle` → `dosya` + `yinelenen` + `zamanlayici`. Menü (`main.c`) değişmedi.

## 4. Algoritmalar ve işlem sayıları

### 4.1 Sayaçlı fonksiyonların T(n)'si

| Fonksiyon | Sayılan işlem | T(n) (kapalı biçim) | En iyi = en kötü? |
|---|---|---|---|
| `dizi_ortalama_say` | toplama n, çarpma (bölme) 1 | n + 1 | evet |
| `standart_sapma_say` | toplama 3n (μ için n, sapmalar için 2n), çarpma n + 2 | 4n + 2 | evet |
| `min_max_indis_say` | karşılaştırma 2(n − 1) | 2n − 2 | evet |
| `ders_istatistigi_say` | karşılaştırma 2n − 2, toplama 4n, çarpma n + 3 | 7n + 1 | evet |
| `sinif_numara_bul_say` | karşılaştırma: i. kayıtta bulunursa i + 1, yoksa n | 1 … n | **hayır** |
| `yinelenen_bul` | karşılaştırma n(n − 1)/2 | n(n − 1)/2 | evet (her girdide aynı) |
| `yinelenen_var_mi` | karşılaştırma: ilk çift (i, j) ise Σ_{a<i} (n − 1 − a) + (j − i) | 1 … n(n − 1)/2 | **hayır** |

**Gözlem (sayacın ortaya çıkardığı gizli iş):** `ders_istatistigi` ortalamayı bir kez kendisi, bir kez de `standart_sapma` içinde hesaplar; toplama sayısı 3n yerine 4n'dir. Asimptotik sınıf (Θ(n)) değişmez, sabit çarpan büyür. Bu sürümde bilerek düzeltilmedi; bir alıştırma olarak bırakılmıştır (bölüm 9).

### 4.2 Tüm çiftler ve erken çıkış

![Tüm çiftler ve erken çıkış (n = 6)](mini_obs_v2_1_ciftler.png)

*Şekil 1. n = 6 kayıtlık örnek (numaralar 7, 3, 7, 5, 3, 7): i < j olan 15 hücre bir kez karşılaştırılır; dört eşit çift (yeşil) sözlük sırasında (0,2), (0,5), (1,4), (2,5). Erken çıkışlı sürüm (kırmızı çerçeve) 2 karşılaştırmada durur. Değerler birim testindeki örnekle aynıdır.*

```
algoritma YİNELENEN-BUL(no[0..n−1])            ▷ tüm çiftler
    çiftler ← boş liste
    i ← 0'dan n−2'ye kadar her i için
        j ← i+1'den n−1'e kadar her j için      ▷ iç döngü n−1−i kez
            eğer no[i] = no[j] ise çiftler'e (i, j) ekle
    döndür çiftler                              ▷ tam n(n−1)/2 karşılaştırma
```

Değişmez (dış döngü; Cormen vd., 2022'deki başlatma–koruma–sonlanma kalıbıyla): i. adımın başında, ilk eleman indisi i'den küçük olan **bütün** eşit çiftler listededir ve sözlük sırasındadır. Sonlanmada (i = n − 1) bütün çiftler bulunmuştur. Erken çıkışlı sürüm aynı sırayla tarar ve ilk eşitlikte döner; bu yüzden bulduğu çift sözlük sırasında **ilk** çifttir.

## 5. Kullanım

### 5.1 `denetle` — yinelenen numara raporu

```
./denetle dosya.csv [--erken] [--goster K]
  dosya v1.0 kurallarıyla okunur, YALNIZCA mükerrer numara kuralı uygulanmaz
  --erken: yalnızca ilk çift (yinelenen_var_mi) · --goster K: en çok K çift (20)
  çıkış: 0 yinelenen yok · 1 dosya okunamadı ya da yinelenen VAR · 2 hatalı kullanım
```

```
$ ./denetle testler/yinelenen_k3.csv
Dosya: testler/yinelenen_k3.csv · kayıt: 30
Yöntem: tüm çiftler (yinelenen_bul)
Karşılaştırma: 435 (n(n-1)/2 = 435)
Yinelenen çift: 3
  sıra      8 ↔ sıra     11 · numara 2400000017 · MEHMET KESKİN / ŞULE KAYA
  sıra     10 ↔ sıra     29 · numara 2400000028 · ECE KOÇ / NİSA CAN
  sıra     17 ↔ sıra     30 · numara 2400000023 · ZEYNEP ASLAN / TOLGA KESKİN
Sonuç: yinelenen numara VAR; dosya mini_obs ile yüklenemez.
Süre: 0.001 ms
[çıkış kodu: 1]
```

```
$ ./denetle testler/yinelenen_k3.csv --erken
Dosya: testler/yinelenen_k3.csv · kayıt: 30
Yöntem: erken çıkışlı (yinelenen_var_mi)
Karşılaştırma: 185 (en kötü durum n(n-1)/2 = 435)
İlk yinelenen çift:
  sıra      8 ↔ sıra     11 · numara 2400000017 · MEHMET KESKİN / ŞULE KAYA
Sonuç: yinelenen numara VAR; dosya mini_obs ile yüklenemez.
Süre: 0.000 ms
[çıkış kodu: 1]
```

Erken çıkışlı sürüm ilk çifti (sıra 8 ↔ 11, yani indis (7, 10)) Σ_{a<7} (29 − a) + (10 − 7) = 182 + 3 = **185** karşılaştırmada bulur; tüm çiftler 435 karşılaştırma yapar. Aynı dosya `mini_obs` ile yüklenmek istenirse yükleyici ilk yinelenen satırda durur ("satır 12" = sıra 11).

### 5.2 `olcer` — yeni işlemler ve sayaçlar

```
./olcer İŞLEM [--n N1,N2,...] [--tekrar K] [--tohum T] [--yinelenen Y] [--sayac]
               [--csv dosya.csv [--ekle]]
  yinelenen  tüm çiftler (yinelenen_bul; numara dizisinde)
  erken      erken çıkışlı (yinelenen_var_mi; kayıt dizisinde)
  --yinelenen Y  veri Y kasıtlı yinelenenle üretilir · --sayac  süre sayaç AÇIKKEN ölçülür
```

Her n için önce sayaç açık **bir sayım çalıştırması** yapılır; sayılar ve (biliniyorsa) kuramsal değerle uyum stdout'a yazılır. Süreler ayrı çalıştırmalarda, sayaç **kapalıyken** ölçülür. Liste içinde n bir öncekinin iki katıysa stderr'e `oran T(n)/T(n/2)` eklenir:

```
$ ./olcer istatistik --n 1000,2000,4000 --tekrar 3
istatistik n =     1000  kontrol = 326298157  sayaç: karşılaştırma 5994 · toplama 12000 · çarpma 3009  kuram: UYUMLU
istatistik n=1000: ortanca 0.0622 ms (en az 0.0584, en çok 0.0851; ilk 0.0622; ısınma 0.0665; 3 tekrar × 1 işlem)
istatistik n =     2000  kontrol = 434118639  sayaç: karşılaştırma 11994 · toplama 24000 · çarpma 6009  kuram: UYUMLU
istatistik n=2000: ortanca 0.1354 ms (en az 0.1326, en çok 0.1719; ilk 0.1719; ısınma 0.1380; 3 tekrar × 1 işlem) · oran T(n)/T(n/2) = 2.18
istatistik n =     4000  kontrol = 647861954  sayaç: karşılaştırma 23994 · toplama 48000 · çarpma 12009  kuram: UYUMLU
istatistik n=4000: ortanca 0.2897 ms (en az 0.2823, en çok 0.3052; ilk 0.2823; ısınma 0.3705; 3 tekrar × 1 işlem) · oran T(n)/T(n/2) = 2.14
[çıkış kodu: 0]
```

CSV sütunları: `islem;n;yinelenen;sayac_acik;tekrar;ic_tekrar;ortanca_ms;ortalama_ms;en_az_ms;en_cok_ms;ilk_ms;isinma_ms;kontrol;karsilastirma;toplama;carpma` (sayaçlar bir ölçüm çağrısının toplamıdır).

### 5.3 `test_kahin`

`./test_kahin [--deneme D] [--tohum T] [--hata-goster minmax|yinelenen]` — v2.0'daki seçenek artık hangi kasıtlı hatanın sınanacağını alır.

## 6. Tasarım kararları

1. **Sayaç bir parametredir, global değildir.** Sayılan fonksiyonlar son parametre olarak `Sayac *` alır; `NULL` "kapalı" demektir. Böylece aynı anda iki ayrı ölçüm yapılabilir ve sayacın kimin işini saydığı çağrıdan bellidir.
2. **Yerel sayım, sonda tek ekleme.** Döngüde `sy->karsilastirma++` yazmak yerine yerel bir değişken artırılır ve fonksiyon sonunda `SAYAC_EKLE` ile bir kez eklenir. C'de `long long` ve `unsigned long long` birbirinin takma adı (alias) olabildiği için iç döngüde sayaca yapılan her yazma, derleyiciyi `no` değerlerini yeniden okumaya zorlayabilirdi. Ölçülen maliyet: 32 000 kayıtta sayaç kapalı 324,9 ms, açık 341,6 ms (fark %5,1; tekrarlar arası yayılımın içinde, bölüm 7.6).
3. **Eski API korunur.** `dizi_ortalama(a, n)` artık `dizi_ortalama_say(a, n, NULL)`'dır; v1.0'dan gelen bütün çağrılar ve 99 eski test değişmeden geçer. Sayaçlı ve sayaçsız sürümün aynı sonucu verdiği ayrıca sınanır.
4. **Tüm çiftlerde numaralar ayrı bir diziye kopyalanır.** Karşılaştırmada yalnızca 8 baytlık numara gerekir; 144 baytlık kayıtlar üzerinde tarama her karşılaştırmada ayrı bir önbellek satırı getirir. `yinelenen_bul` önce numaraları bitişik bir `long long` dizisine kopyalar (Θ(n) zaman ve bellek; Θ(n²) işin yanında önemsiz): 10⁵ numara 800 KB'tır ve L2'ye sığar. Etki bölüm 7.4'te ölçülmüştür.
5. **Erken çıkışlı sürüm kopyalamaz.** `yinelenen_var_mi`'nin en iyi durumu tek karşılaştırmadır; Θ(n)'lik bir kopya bu en iyi durumu Θ(n)'e çıkarırdı. Bu yüzden kayıt dizisinde doğrudan çalışır. (Aynı problemde iki sürümün farklı bellek düzeni seçmesi, "en iyi durum" kavramının yalnızca karşılaştırma sayısıyla değil gerçek işle ilgili olduğunu gösterir.)
6. **Çiftler sözlük sırasında, sınırlı tamponla.** `yinelenen_bul` en çok `azami` çifti yazar ama toplam çift sayısını her zaman döndürür; `azami = 0` ile yalnızca sayar. Bir numara m kez geçiyorsa m(m − 1)/2 çift oluşur; bu yüzden çift sayısı "fazladan kayıt" sayısından büyük olabilir.
7. **Yükleyici değişmedi.** `csv_oku` mükerrer numara kuralını her zaman uygular; kuralsız okuma (`csv_oku_secenekli(…, false)`) yalnızca bütün yinelenenleri raporlamak isteyen `denetle` içindir. v1.0'ın davranışı ve v2.0'ın ölçümü geçerliliğini korur.
8. **Kuram stdout'ta.** `olcer` sayaçları kapalı biçim formüllerle karşılaştırıp `kuram: UYUMLU` yazar; ölçüm raporu bu satırları doğrudan kanıt olarak kullanabilir.

## 7. Ölçümler

### 7.1 Ölçüm düzeni ve ortam

Makine: Intel(R) Xeon(R) Processor @ 2.80GHz, 2 çekirdek (sanal makine), L2 2 MiB (2 × 1 MiB), L3 33 MiB; gcc 13.3.0 (Ubuntu 13.3.0-6ubuntu2~24.04.1), `-std=c17 -Wall -Wextra -pedantic -O2 -g`; tarih 2026-10-12 22:47. Düzen: her n için 1 sayım çalıştırması (sayaç açık), 1 ısınma ve 5 tekrar (sayaç kapalı), **ortanca**; `erken` 64 000 kayıtta ≈ 6,5 s sürdüğü için bu boyutta 1 tekrar. Veri `uretec_sinif` ile bellekte, tohum 42 ile üretilir (yinelenen yok: en kötü durum). `make olcum` toplam 1 dk 50 s sürdü; günlüğü `mini_obs_v2_1_ciktilar.txt`'dedir.

### 7.2 Sayaçlar kuramla birebir: ders istatistiği

| n | karşılaştırma | toplama | çarpma | = (6n−6, 12n, 3n+9) | süre (ortanca) | T(n) / T(n/2) |
|--:|--:|--:|--:|:-:|--:|--:|
| 1 000 | 5 994 | 12 000 | 3 009 | ✓ | 62,7 µs | — |
| 2 000 | 11 994 | 24 000 | 6 009 | ✓ | 132,8 µs | 2,12 |
| 4 000 | 23 994 | 48 000 | 12 009 | ✓ | 311,9 µs | 2,35 |
| 8 000 | 47 994 | 96 000 | 24 009 | ✓ | 631,6 µs | 2,03 |
| 16 000 | 95 994 | 192 000 | 48 009 | ✓ | 1,3 ms | 2,04 |
| 32 000 | 191 994 | 384 000 | 96 009 | ✓ | 2,6 ms | 2,03 |
| 64 000 | 383 994 | 768 000 | 192 009 | ✓ | 6,2 ms | 2,37 |
| 128 000 | 767 994 | 1 536 000 | 384 009 | ✓ | 14,3 ms | 2,31 |
| 256 000 | 1 535 994 | 3 072 000 | 768 009 | ✓ | 31,3 ms | 2,18 |
| 512 000 | 3 071 994 | 6 144 000 | 1 536 009 | ✓ | 58,9 ms | 1,88 |
| 1 024 000 | 6 143 994 | 12 288 000 | 3 072 009 | ✓ | 119,9 ms | 2,04 |

*Tablo 1. Üç dersin istatistiği (`ders_istatistigi_say` × 3): sayaçlar kapalı biçimle (3 × (2n − 2), 3 × 4n, 3 × (n + 3)) her n'de birebir aynıdır. Süre için log–log eğim 1,10: doğrusal.*

Katlama oranları 1,88 ile 2,37 arasındadır: Θ(n) için beklenen 2'ye yakın. Süre ölçümü gürültülü olabilir, **sayaç olamaz**: aynı girdide her zaman aynı sayıyı verir. Bu yüzden kabul ölçütleri önce sayaçlar üzerinden, sonra süreler üzerinden tanımlanır.

### 7.3 Oran testi: tüm çiftler

| n | karşılaştırma (sayaç) | = n(n−1)/2 | süre (ortanca) | en az – en çok | T(n) / T(n/2) | ns / karşılaştırma |
|--:|--:|:-:|--:|--:|--:|--:|
| 1 000 | 499 500 | ✓ | 310,2 µs | 302,8 µs – 329,3 µs | — | 0,62 |
| 2 000 | 1 999 000 | ✓ | 1,3 ms | 1,2 ms – 1,4 ms | 4,05 | 0,63 |
| 4 000 | 7 998 000 | ✓ | 5,1 ms | 4,9 ms – 5,6 ms | 4,02 | 0,63 |
| 8 000 | 31 996 000 | ✓ | 22,7 ms | 21,9 ms – 24,9 ms | 4,48 | 0,71 |
| 16 000 | 127 992 000 | ✓ | 88,6 ms | 80,2 ms – 102,8 ms | 3,91 | 0,69 |
| 32 000 | 511 984 000 | ✓ | 335,2 ms | 325,9 ms – 353,1 ms | 3,78 | 0,65 |
| 64 000 | 2 047 968 000 | ✓ | 1,34 s | 1,29 s – 1,42 s | 4,00 | 0,65 |
| 128 000 | 8 191 936 000 | ✓ | 5,57 s | 5,45 s – 5,74 s | 4,16 | 0,68 |

*Tablo 2. `yinelenen_bul` (tüm çiftler, numara dizisi; yinelenen yok). Sayaç her n'de tam n(n − 1)/2'dir; ortanca 5 tekrar.*

![Oran testi: log–log](mini_obs_v2_1_olcum_oran.png)

*Şekil 2. Log–log grafik: tüm çiftler (eğim 2,02), kayıt dizisinde erken çıkışlı sürümün en kötü durumu (eğim 2,55) ve ders istatistiği (eğim 1,10). Noktalı çizgi eğim 2 kılavuzudur.*

Yorum: n ≥ 4 000 için bütün katlama oranları 3,78 ile 4,48 arasındadır ve log–log eğim **2,02** olarak ölçülür (n ≥ 8 000 için 1,98). Karşılaştırma başına süre 10³'ten 1,28·10⁵'e kadar ≈ 0,62–0,71 ns aralığında kalır: numara dizisi en büyük boyutta bile 1 MB'tır ve L2'ye sığar. Kuram (Θ(n²)) ve ölçüm burada birbirini tam olarak doğrular. **Kestirim:** aynı sabitle 10⁶ kayıt ≈ 340 s (≈ 5,7 dakika), 10⁷ kayıt ≈ 9,5 saat sürerdi (numara dizisi 8 MB ve 80 MB olacağı için gerçek değer daha büyük olabilir; ölçülmedi). Karşılaştırma için ders istatistiği 1,024·10⁶ kayıtta 119,9 ms sürer; 10⁷ kayıtta ≈ 1,2 s olacağı kestirilir. Büyük Soru'nun yanıtı budur: büyüme sınıfı farkı, sabit çarpan farkını n büyüdükçe ezer.

### 7.4 Aynı karşılaştırma sayısı, farklı süre: bellek düzeni ve kod hizalaması

`erken` işlemi, yinelenen yokken en kötü durumda çalışır ve `yinelenen_bul` ile **aynı sayıda** (n(n − 1)/2) karşılaştırma yapar; tek fark kayıt dizisinde (144 bayt adımla) taramasıdır. `make olcum` ayrıca aynı kaynağı GNU assembler'ın `-mbranches-within-32B-boundaries` seçeneğiyle derleyip (`olcer_hizali`) iki işlemi yeniden ölçer:

| n | numara dizisi | kayıt dizisi | numara (hizalı) | kayıt (hizalı) | kayıt: T(n)/T(n/2) | kayıt / numara (süre) |
|--:|--:|--:|--:|--:|--:|--:|
| 1 000 | 0,62 | 0,42 | 0,33 | 0,61 | — | 0,7 |
| 2 000 | 0,63 | 0,43 | 0,32 | 0,63 | 4,03 | 0,7 |
| 4 000 | 0,63 | 0,48 | 0,31 | 0,62 | 4,49 | 0,8 |
| 8 000 | 0,71 | 0,49 | 0,33 | 0,69 | 4,05 | 0,7 |
| 16 000 | 0,69 | 1,31 | 0,33 | 1,09 | 10,81 | 1,9 |
| 32 000 | 0,65 | 2,60 | 0,33 | 2,57 | 7,90 | 4,0 |
| 64 000 | 0,65 | 3,18 | — | — | 4,90 | 4,9 |

*Tablo 3. Karşılaştırma başına süre (ns) ve kayıt dizisindeki katlama oranları; "hizalı" sütunları `olcer_hizali` ile ölçüldü (64 000 ve 128 000 kayıt yalnızca standart derlemede).*

![Karşılaştırma başına süre](mini_obs_v2_1_olcum_ns.png)

*Şekil 3. Karşılaştırma başına süre: düz çizgiler standart derleme, kesikli çizgiler hizalı derleme; noktalı dikey çizgiler L2'ye (1 MiB) sığan kayıt (≈ 7 281) ve numara (131 072) sayısı.*

İki gözlem:

1. **Bellek düzeni.** Kayıt dizisinde karşılaştırma başına süre, dizi L2'den taştıktan sonra 8 000 → 32 000 aralığında standart derlemede 5,3, hizalı derlemede 3,7 kat artar; bu aralıkta katlama oranları 10,8 ve 7,9 olarak ölçülür ve log–log eğim 2,55 olur. Numara dizisinde süre düz kalır. 32 000 kayıtta kayıt dizisi numara dizisinden 4,0 kat (standart), 7,9 kat (hizalı) yavaştır. `denetle` 20 000 kayıtlık dosyada da aynı şeyi gösterdi: erken çıkışlı sürüm 4,8 kat az karşılaştırma yaptığı hâlde daha uzun sürdü (karşılaştırma başına 2,47 ns'ye karşı 0,36 ns; çıktılar bölüm 2).
2. **Kod hizalaması.** Aynı `yinelenen_bul` kodu, yalnızca makine komutlarının bellekteki yerleşimi değişince karşılaştırma başına ≈ 0,62–0,71 ns'den ≈ 0,31–0,33 ns'ye iner; `yinelenen_var_mi` ise küçük n'de tersine yavaşlar (0,42 ns yerine 0,61 ns). Bu işlemci ailesinde (Skylake türevi Intel Xeon) koşullu atlama komutlarının 32 baytlık sınırlara göre konumunun döngü hızını etkilediği bilinmektedir; ölçtüğümüz fark bu etkiyle tutarlıdır. Ders: **sabit çarpan kırılgandır** — derleyici seçeneği, işlemci ve hatta fonksiyonun ikili dosyadaki yeri onu iki kat değiştirebilir. Büyüme sınıfı (oran ≈ 4, eğim ≈ 2) ise her iki derlemede aynıdır. Bu yüzden iki algoritmayı karşılaştırırken **aynı programda, aynı derlemeyle** ölçün ve sonucu sayaçla destekleyin.

### 7.5 Erken çıkış ve yinelenen sayısı

| kasıtlı yinelenen k | karşılaştırma (erken çıkış) | n(n−1)/2'ye oranı | süre (ortanca) |
|--:|--:|--:|--:|
| 0 (en kötü durum) | 511 984 000 | %100 | 1,33 s |
| 1 | 332 752 031 | %65,0 | 975,5 ms |
| 10 | 45 786 932 | %8,9 | 116,6 ms |
| 100 | 3 557 900 | %0,7 | 11,0 ms |

*Tablo 4. `yinelenen_var_mi`, n = 32 000, veri k kasıtlı yinelenenle (rastgele konumlarda) üretildi.*

Tek bir yinelenen bile, rastgele konumdaysa, aramayı ortalama olarak önemli ölçüde kısaltır; k arttıkça ilk çift daha erken bulunur. Bu, en kötü durumun (yinelenen yok) gerçek veride ne kadar sık olduğuna göre "beklenen" maliyetin değiştiğini gösterir. Ancak Mini-OBS'nin kullanım senaryosunda (temiz dosya) en kötü durum tipik durumdur: dosya geçerliyse erken çıkış hiçbir şey kazandırmaz.

### 7.6 Sayacın maliyeti

| sayaç | ortanca | en az | en çok |
|:--|--:|--:|--:|
| kapalı (NULL) | 324,9 ms | 318,4 ms | 343,7 ms |
| açık | 341,6 ms | 326,5 ms | 395,9 ms |

*Tablo 5. `yinelenen_bul`, n = 32 000, sayaç kapalı ve açık (5 tekrar).*

İki ortanca arasındaki fark %5,1 düzeyindedir ve en az–en çok aralıkları örtüşür: sayaç ölçümü bozmaz. Yerel sayaç değişkeni derleyici tarafından döngüden çıkarılabilir (iç döngü sayısı kapalı biçimde hesaplanır), bu yüzden sayaç açıkken bile iç döngüye ek iş girmez.

## 8. Testler

- **Birim testleri** (`obs_test`): `134 doğrulama: 37 kural + 22 metin + 24 yapı + 16 dosya + 11 üreteç + 11 sayaç + 13 yinelenen`. Sayaç testleri: her `…_say` fonksiyonunun kesin sayıları (n = 5 için 5/1, 15/7, 8, ders istatistiğinde 8/20/8), `NULL` ile çökmeme, sayacın birikmesi, sayaçlı ve sayaçsız sürümün aynı sonucu. Yinelenen testleri: `tum_ciftler` (0, 1, 2, 100 000 için), yinelenen yokken 10 karşılaştırma ve 0 çift, örnek `{7, 3, 7, 5, 3, 7}` için dört çiftin sözlük sırası, `azami` ile kırpma ve yalnızca sayma, erken çıkışta 2 karşılaştırma, en iyi durum (1), yalnızca son iki kayıt aynı (ilk çift aynı zamanda son çifttir: 5 + 4 + 3 + 2 + 1 = 15 karşılaştırma, en kötü durumla aynı), n = 0 ve n = 1, kuralsız CSV okuma.
- **Kâhin testleri** (`test_kahin`): 300 denemede 57 242, 1 000 denemede 182 277 denetim, uyuşmazlık yok. Yinelenen kâhini: (numara, indis) çiftleri `qsort` ile sıralanır, her eşit numara grubunun bütün indis çiftleri üretilir ve çiftler sözlük sırasına dizilir; erken çıkışın ilk çifti grupların en küçük (ilk, ikinci) indisidir ve karşılaştırma sayısı kapalı biçimle denetlenir. Veriler küçük bir aralıktan çekilen numaralarla üretilir (çok sayıda ikili ve üçlü yinelenen).
- **Kasıtlı hata** (`--hata-goster yinelenen`): iç döngü sınırı `j < n − 1` olan sürüm son kaydı hiç karşılaştırmaz. Bu denemede son kaydın yinelenen çifti olmadığı için çift listesi **doğru görünür**, ama sayaç sınır hatasını yakalar:

```
$ ./test_kahin --hata-goster yinelenen
KÂHİN UYUŞMAZLIĞI (tohum 1)
  İşlev      : yinelenen_bul
  n          : 246
  Beklenen   : 80 çift, 30135 karşılaştırma
  Bulunan    : 80 çift, 29890 karşılaştırma
  Yeniden üretmek için: ./test_kahin --tohum 1 --deneme 1 --hata-goster yinelenen
[çıkış kodu: 1]
```

  Fark 30 135 − 29 890 = 245 = n − 1'dir: kaçan, son kaydı içeren n − 1 çifttir. Yalnızca çıktıyı denetleyen bir test bu hatayı bu girdide göremezdi; **işlem sayısı da bir sözleşmedir.**
- **Bellek**: `make asan` temiz; sanitizer hataları 99 koduyla çıkar (`denetle`'nin "yinelenen VAR" kodu 1 ile karışmasın diye).

## 9. Ders notu için özet (Hafta 2 · Mini-OBS 2 adımı)

**Bu hafta:** v2.0'da yüklemenin karesel olduğunu ölçtük. Şimdi işlemleri sayarak T(n)'yi yazıyor, yinelenen numara tespitinin kaba kuvvet sürümünü kuruyor ve oran testiyle büyüme sınıfını deneysel olarak doğruluyoruz.

### Gereksinimler

- `sayac.c`: `sayac.h`'deki `Sayac` yapısı, `SAYAC_EKLE` makrosu, `sayac_sifirla`, `sayac_yaz`.
- `obs.c`: `dizi_ortalama_say`, `standart_sapma_say`, `min_max_indis_say`, `ders_istatistigi_say`, `sinif_numara_bul_say`; eski adlar bunları `NULL` ile çağıran sarmalayıcılar olmalı. Her fonksiyonun başına T(n)'yi yorum olarak yazın.
- `yinelenen.c`: `yinelenen_var_mi` (erken çıkış; kayıt dizisinde), `yinelenen_bul` (tüm çiftler; çiftleri sözlük sırasında `azami` sınırıyla yazar, toplamı döndürür), `tum_ciftler`.
- `olcer.c`: `yinelenen` ve `erken` işlemleri; her n için sayım çalıştırması + sayaç kapalı süre ölçümü; CSV'de karşılaştırma sayısı.
- `denetle.c` (önerilen): bir CSV'deki bütün yinelenen numaraları sıra numaralarıyla listeleyen araç; yinelenen varsa çıkış kodu 1.
- `test_obs.c` ve `test_kahin.c`: sayaç formülleri ve yinelenen tespiti için birim ve kâhin testleri.
- Ölçüm raporu: n = 10³, 2·10³, …, ≥ 6,4·10⁴ için tablo (n, karşılaştırma, süre, oran), log–log grafik, eğim ve yorum; makine bilgisi.

### İpuçları

- Temel işlemi önce **yazıyla** seçin ("iki numaranın karşılaştırılması"); sonra yalnızca onu sayın. Döngü sayaçları ve dizi indeksleri sayılmaz.
- Sayacı iç döngüde bir işaretçi üzerinden artırmayın; yerel değişkende toplayıp sonda ekleyin.
- `for (j = i + 1; …)`: iç döngünün `i + 1`'den başlaması hem her çifti **bir kez** saymayı hem de kaydın kendisiyle karşılaştırılmamasını sağlar. `j = 0`'dan başlayan sürüm n² − n karşılaştırma yapar ve her çifti iki kez bulur.
- `n(n − 1)/2`'yi `int` ile hesaplamayın: n = 10⁵'te 4 999 950 000 değeri 32 bitlik `int`'i aşar; `unsigned long long` kullanın.
- Oran testinde n'i **katlayın**; tek bir ölçüm yerine ortanca kullanın; en küçük n'leri (sabit maliyetlerin baskın olduğu bölge) yorumdan ayırın.
- Karşılaştırdığınız iki algoritmayı aynı programda, aynı derlemeyle ölçün (bölüm 7.4).

### Kabul ölçütleri (denetlenebilir)

1. `make` ve `make test` sıfır uyarıyla derlenir; bütün birim ve kâhin testleri geçer.
2. Sayaçlar kapalı biçimlerle **birebir** aynıdır: `dizi_ortalama_say` (n, 1), `standart_sapma_say` (3n, n + 2), `min_max_indis_say` 2(n − 1), `ders_istatistigi_say` (2n − 2, 4n, n + 3), `sinif_numara_bul_say` i + 1 ya da n. `./olcer istatistik --n 1000,2000,4000` her satırda `kuram: UYUMLU` yazar.
3. `yinelenen_bul`'un karşılaştırma sayısı her girdide tam n(n − 1)/2'dir (yinelenen olsun olmasın); `yinelenen_var_mi` yinelenen yokken n(n − 1)/2, ilk iki kayıt aynıyken 1 karşılaştırma yapar.
4. `./denetle testler/yinelenen_k3.csv`: 435 karşılaştırma, 3 çift (sıra 8 ↔ 11, 10 ↔ 29, 17 ↔ 30), çıkış kodu 1; `--erken`: 185 karşılaştırma, ilk çift 8 ↔ 11; `./denetle ornek_veri/ogrenciler.csv`: 28 karşılaştırma, 0 çift, çıkış 0.
5. Oran testi (kendi makinenizde, tüm çiftler, numara dizisi): n ≥ 4 000 için her katlama oranı **3,5 ile 4,5 arasında**; en az 7 katlamalı ölçümden hesaplanan log–log eğim **1,9 ile 2,1 arasında**. Ders istatistiği için eğim 0,8–1,3 (doğrusal).
6. Sayaç açık ve kapalı ölçümler arasındaki fark, tekrarların en az–en çok aralığı içinde kalır (bu makinede %5,1).
7. `--hata-goster yinelenen` ile kâhin hatalı sürümü yakalar (karşılaştırma sayısı ya da çift listesi farklı), 1 ile çıkar.
8. `make asan` temiz.

### Test senaryoları

| # | Girdi | Beklenen çıktı / davranış |
|---|---|---|
| 1 | numaralar {11, 22, 33, 44, 55} | `yinelenen_bul` 0 çift, 10 karşılaştırma; `yinelenen_var_mi` false, 10 |
| 2 | {7, 3, 7, 5, 3, 7} | 4 çift: (0,2) (0,5) (1,4) (2,5); 15 karşılaştırma; erken: (0,2), 2 karşılaştırma |
| 3 | {9, 9, 1, 2, 3, 4} | erken: 1 karşılaştırma (en iyi durum) |
| 4 | {1, 2, 3, 4, 8, 8} | erken: (4,5), 5 + 4 + 3 + 2 + 1 = 15 karşılaştırma (son çift) |
| 5 | n = 0 ve n = 1 | 0 çift, 0 karşılaştırma |
| 6 | `azami = 2`, örnek 2 | dönüş 4; yalnızca (0,2) ve (0,5) yazılır |
| 7 | a = {4, 1, 3, 1, 4} | `min_max_indis_say`: enk 1, enb 0 (ilk indisler), 8 karşılaştırma |
| 8 | `./denetle testler/yinelenen_k3.csv` | 3 çift, 435 karşılaştırma, çıkış 1 |
| 9 | `./denetle testler/bozuk.csv` | "dosya biçimi hatalı (satır 3)", çıkış 1 |
| 10 | `./denetle` | kullanım iletisi, çıkış 2 |
| 11 | `./olcer yinelenen --n 1000,2000,4000,8000` | sayaç 499 500 · 1 999 000 · 7 998 000 · 31 996 000, `kuram: UYUMLU`; stderr'de oran ≈ 4 |
| 12 | `./test_kahin --hata-goster yinelenen` | "KÂHİN UYUŞMAZLIĞI", karşılaştırma farkı n − 1, çıkış 1 |

### Başlangıç noktası (öğrenciye verilenler)

- **Verilir:** kendi v2.0'ınız (ya da referans v2.0), `sayac.h`, `yinelenen.h` (bildirimler ve sözleşmeler), `testler/yinelenen_k3.csv`.
- **Yazılır / değiştirilir:** `sayac.c`, `yinelenen.c`, `denetle.c` (yeni); `obs.h/.c` (`…_say` sürümleri ve sarmalayıcılar); `dosya.h/.c` (`csv_oku_secenekli`); `olcer.c` (`yinelenen`, `erken` işlemleri ve sayaç sütunları); `test_obs.c`, `test_kahin.c`; `Makefile` (`denetle`, `olcum`).
- **Değiştirilmez:** yükleyicinin davranışı (`csv_oku` kuralı her zaman uygular), kayıt modeli, ortak modüller.
- **Alıştırma önerisi:** `ders_istatistigi`'nde ortalamanın iki kez hesaplanmasını kaldırın (`standart_sapma`'ya μ'yü parametre olarak verin); toplama sayısının 4n'den 3n'e indiğini sayaçla, sürenin değişimini oran testiyle gösterin.

## 10. Bilinen sınırlılıklar

- Tüm çiftler yalnızca 1,28·10⁵ kayda kadar ölçüldü (≈ 5,6 s); 10⁶ ve 10⁷ için verilen değerler **kestirimdir** ve dizinin L2'den taşmasının etkisini içermez.
- Kayıt dizisindeki erken çıkışlı sürüm 64 000 kayıtta tek tekrarla ölçüldü (≈ 6,5 s).
- Sayaçlar başarılı/şartlı sınıflamasındaki karşılaştırmaları ve `sqrt`'i saymaz; T(n) formülleri yalnızca bölüm 4.1'de tanımlanan işlemler içindir.
- Karşılaştırma başına süreler kod hizalamasına duyarlıdır (bölüm 7.4); mutlak ns değerleri başka bir derlemede iki kata kadar değişebilir. Büyüme oranları ve sayaçlar bundan etkilenmez.
- `denetle` yinelenenleri **kayıt sırasıyla** raporlar; dosyada boş satır varsa sıra numarası satır numarasından farklı olabilir.
- Hizalama deneyi GNU assembler'a (binutils) özgü `-Wa,-mbranches-within-32B-boundaries` seçeneğini kullanır; başka bir derleme zincirinde `make olcum`'dan bu iki satır çıkarılabilir.

## 11. Kaynaklar

- Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2022). *Introduction to algorithms* (4th ed.). MIT Press.
- Sedgewick, R., & Wayne, K. (2011). *Algorithms* (4th ed.). Addison-Wesley.
- t0st. (2021, February 28). *How I cut GTA Online loading times by 70%*. https://nee.lv/2021/02/28/How-I-cut-GTA-Online-loading-times-by-70/
