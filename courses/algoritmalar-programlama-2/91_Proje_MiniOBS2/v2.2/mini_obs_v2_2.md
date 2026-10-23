# Mini-OBS 2 v2.2 — Özyineleme ve Geri İzleme: AKTS aralığına uyan seçmeli ders kümeleri (Hafta 3)

**Bu sürümün amacı:** Mini-OBS'ye üstel bir arama problemi eklemek ve **budamanın** etkisini ölçmek. Öğrenci, bir seçmeli ders havuzundan (12–16 ders; kod, ad, AKTS; dosyadan okunur) AKTS toplamı **[alt, ust]** aralığında kalan — isteğe bağlı olarak en çok K ders içeren — **bütün** ders kümelerini görmek ister. `secim_yap` bu kümeleri **geri izlemeyle** (backtracking) ve **sözlük sırasında** üretir; üç sürümü vardır: budamasız (ağacın tamamı, 2ⁿ düğüm), üst sınır budamalı ("toplam > ust ise dur") ve üst + alt sınır budamalı ("kalan derslerin hepsi alınsa bile alt sınıra ulaşılamıyorsa dur"). Doğruluk, **bit maskesi kaba kuvvet kâhiniyle** (0 … 2ⁿ − 1) aynı kümeleri aynı sırada vermesiyle sınanır. Ölçüm: 30 derslik sentetik havuzda üst budama 1 073 741 824 düğümlük ağacında yalnızca 1 434 525 düğüm (≈ %0,13) ziyaret eder ve 715 kat hızlıdır ([24, 30] aralığı); aralık "ortaya" kaydıkça ([60, 70]) budamanın kazancı küçülür, çünkü uygun küme sayısının kendisi üstel büyür. H13'te aynı problem dinamik programlamayla (0/1 sırt çantası) yeniden ele alınacaktır.

Dosyalar (satır sayılarıyla): `secmeli.h` (102) · `secmeli.c` (330) · `ders_sec.c` (184) · `olcer.c` (455) · `test_obs.c` (854) · `test_kahin.c` (855) · `obs.h` (130) · `obs.c` (649) · `metin.h` (35) · `metin.c` (340) · `dosya.h` (66) · `dosya.c` (329) · `main.c` (292) · `sayac.h` (41) · `sayac.c` (17) · `yinelenen.h` (43) · `yinelenen.c` (71) · `denetle.c` (140) · `uretec.h` (54) · `uretec.c` (160) · `veri_uret.c` (94) · `deney.h` (28) · `deney.c` (32) · `ortak_rastgele.h` (42) · `ortak_rastgele.c` (50) · `zamanlayici.h` (30) · `zamanlayici.c` (55) · `Makefile` (166) · `ornek_veri/secmeli_dersler.csv` (14 ders, toplam 63 AKTS) · `testler/havuz_kucuk.csv` (4 ders; elle izleme), `testler/havuz_bozuk.csv`, `testler/havuz_tekrar_kod.csv` ve önceki sürümlerin test girdileri · `olcum/geri_izleme_a.csv`, `olcum/geri_izleme_b.csv`, `olcum/OLCUM_ORTAMI.txt` · `mini_obs_v2_2_ciktilar.txt` (445 satır, gerçek çıktılar). Şekil: `mini_obs_v2_2_agac.png`; grafikler: `mini_obs_v2_2_olcum_dugum.png`, `mini_obs_v2_2_olcum_sure.png`.

Derleme: `make` (`mini_obs`, `veri_uret`, `olcer`, `denetle`, `ders_sec`), `make test`, `make olcum` (bu makinede 34 s), `make ornek`, `make asan`, `make valgrind`, `make temiz`. Bayraklar `-std=c17 -Wall -Wextra -pedantic -O2 -g`; 17 kaynak dosya `-O0 … -Os` düzeylerinde `-Werror` ile uyarısız. Çıkış kodları: 0, 1 (havuz okunamadı, bellek yetersiz ya da yöntemler uyuşmadı; testlerde uyuşmazlık), 2 (hatalı kullanım).

## 1. Amaç ve haftanın kavramıyla bağı

Hafta 3'ün Büyük Sorusu sekiz vezir bulmacasıdır: yaklaşık 4,4 milyar yerleşimi tek tek denemeden 92 çözüm nasıl bulunur? Yanıt, **durum uzayı ağacında geri izleme ve budamadır** (Wirth, 1971). Mini-OBS'deki karşılığı ders seçimidir:

- **Üretme algoritmaları** (ÖÇ 3.3): n derslik havuzun 2ⁿ alt kümesi vardır; her biri "başlangıç indisli" özyinelemeyle bir kez üretilir. Bit maskesiyle (0 … 2ⁿ − 1) özyinelemesiz üretim kâhin olarak kullanılır.
- **Geri izleme ve budama** (ÖÇ 3.4; Skiena, 2020): seç → dene → (çözüm mü?) → geri al. AKTS değerleri pozitif olduğu için "toplam üst sınırı aştı" denetimi bir düğümün bütün torunlarını eler; "kalan dersler alt sınıra yetmez" denetimi aramayı tersinden daraltır.
- **Uygulanabilirlik sınırı** (ÖÇ 3.5): budamasız arama 2ⁿ düğüm ziyaret eder; n = 30'da ≈ 10⁹ düğüm bu makinede 5,2 s sürer, bit maskesi kaba kuvvet ise ≈ 79 s (kestirim).
- **Mühendis gözüyle:** kaba kuvvet ilk doğru çözümdür ve daha hızlı algoritmaların kâhini olarak saklanır; arama uzayının büyüklüğü kod yazılmadan önce hesaplanır.

Yol haritasındaki karşılığı (Tablo A.1): **H3 · v2.2 · AKTS aralığına uyan ders kombinasyonları · Geri izleme, budama.** Sarmal (Tablo 4.2, "Ders seçimi"): H3 geri izleme O(2ⁿ) → H12 açgözlü (yanlış sonuç) → H13 0/1 sırt çantası O(n·W) → H14 NP-tamlık ve sözde polinom zaman.

## 2. v2.1'den ne değişti?

| Konu | v2.1 (H2) | v2.2 (H3) |
|---|---|---|
| Problem | yinelenen numara (O(n²)) | + seçmeli ders kümeleri: AKTS ∈ [alt, ust], en çok K ders (O(2ⁿ)) |
| Modül | — | `secmeli.h/.c`: havuz okuma (`kod;ad;akts`), sentetik havuz, `secim_yap` (4 yöntem), maske yardımcıları |
| Program | `mini_obs`, `veri_uret`, `olcer`, `denetle` | + **`ders_sec`** (kümeleri listeler; `--yontem hepsi` dört yöntemi kâhinle karşılaştırır) |
| `olcer` | kayıt işlemleri | + `budamasiz`, `ust`, `ust_alt`, `bitmaske` (n = havuzdaki ders sayısı; `--alt`, `--ust`, `--en-fazla`; CSV'de `cozum;ziyaret;budanan`) |
| Veri | öğrenci CSV'si | + `ornek_veri/secmeli_dersler.csv` (14 ders), `testler/havuz_*.csv` |
| Testler | 134 birim; kâhin 57 242 denetim | 150 birim (+16 seçmeli); kâhin 59 342 denetim (+ geri izleme ↔ bit maskesi); `--hata-goster budama` |
| `make olcum` | oran testi | budamanın etkisi: iki senaryo (A [24, 30], B [60, 70]), n = 10 … 30 |

Öğrenci kayıtları, yükleyici, sayaçlar ve yinelenen tespiti v2.1'deki gibidir; menü değişmedi.

## 3. Mimari

| Modül / program | Sorumluluk | Başlıca öğeler |
|---|---|---|
| `secmeli.h/.c` (**yeni**) | havuz, geri izleme, kâhin | `DersHavuzu`, `SecimKisiti {alt, ust, en_fazla}`, `SecimSonucu {maske[], n, ziyaret, budanan}`, `havuz_oku/yukle`, `havuz_uret`, `secim_yap`, `maske_sozluk_karsilastir` |
| `ders_sec.c` (**yeni**) | komut satırı aracı | havuzu ve kısıtı yazar, kümeleri listeler, yöntem tablosu |
| `olcer.c` | ölçüm | seçim işlemleri için sentetik havuz ve ayrı CSV sütunları |
| `test_obs.c`, `test_kahin.c` | testler | elle izlenmiş 4 derslik havuz; rastgele havuzlarda kâhin |
| diğerleri | v2.1'den aynen | — |

`secmeli` yalnızca `dosya.h` (durum kodları), `metin.h` (`tamsayi_coz`, `ad_gecerli_mi`) ve `ortak_rastgele.h`'ye bağlıdır; öğrenci kaydını bilmez. Böylece v3.0'da menüye bağlanırken ya da H13'te DP sürümüyle karşılaştırılırken bağımsız kalır.

## 4. Algoritma

### 4.1 Durum uzayı ağacı

Her düğüm bir ders kümesidir (bit maskesiyle saklanır); kök boş kümedir. Bir düğümün çocukları, kümedeki en büyük indisten **sonra** gelen bir dersin eklenmesiyle oluşur. Bu "başlangıç indisli" ağaçta her alt küme **tam bir kez** görünür (2ⁿ düğüm) ve ön sıra dolaşım kümeleri ders indislerinin **sözlük sırasında** verir: {} < {0} < {0, 1} < {0, 1, 2} < {0, 2} < {1} < …

![Durum uzayı ağacı](mini_obs_v2_2_agac.png)

*Şekil 1. 4 derslik havuzda (A 5, B 4, C 6, D 3 AKTS) [7, 9] aralığı için üst sınır budamalı geri izleme. Düğümlerde küme ve AKTS toplamı yazılıdır. Toplamı 9'u aşan düğüm (kesikli) girilir ama genişletilmez; altındaki 3 düğüm hiç üretilmez. Sayılar `ders_sec` ve birim testleriyle doğrulanmıştır (bölüm 5.1).*

```
algoritma GERİ-İZLE(bas, toplam, adet, seçili)
    ziyaret ← ziyaret + 1
    eğer toplam > üst ise                         ▷ budama 1 (AKTS > 0)
        budanan ← budanan + 1; dön
    eğer [alt budaması açık] ve toplam + kalan[bas] < alt ise   ▷ budama 2
        budanan ← budanan + 1; dön
    eğer alt ≤ toplam ≤ üst ve (K = 0 ya da adet ≤ K) ise
        seçili kümesini kaydet                    ▷ sözlük sırasında
    eğer K > 0 ve adet = K ise dön                ▷ ders sayısı sınırı
    j ← bas'tan n−1'e kadar her j için            ▷ seç → dene → geri al
        GERİ-İZLE(j+1, toplam + akts[j], adet + 1, seçili ∪ {j})
```

`kalan[b] = akts[b] + … + akts[n−1]` önceden hesaplanır (sonek toplamı). Toplam, adet ve maske **değer olarak** aktarıldığı için "geri al" adımı kendiliğinden gerçekleşir; özyineleme derinliği en çok n + 1 ≤ 31'dir.

**Doğruluk.** Budama 1 güvenlidir, çünkü her AKTS ≥ 1'dir: bir düğümün toplamı üst sınırı aştıysa bütün torunlarınınki de aşar (negatif değerlerde bu kural yanlış olurdu; havuz okuyucu AKTS'yi 1..30 aralığında denetler). Budama 2 güvenlidir, çünkü `kalan[bas]` torunların ekleyebileceği en büyük toplamdır; buna rağmen alt sınıra ulaşılamıyorsa hiçbir torun çözüm olamaz. Budama hiçbir çözümü atmadığı için çıktı, ağacın tamamını dolaşan budamasız sürümle aynıdır — ve kâhinle karşılaştırma bunu denetler.

**Karmaşıklık.** Budamasız: tam 2ⁿ düğüm, düğüm başına O(1) iş (çözüm kaydı hariç) → Θ(2ⁿ) (Cormen vd., 2022). Bit maskesi: 2ⁿ maskenin her biri için n bit → Θ(n · 2ⁿ). Budama en kötü durumu değiştirmez (O(2ⁿ)); kazancı aralığa ve havuza bağlıdır. Ayrıca hiçbir yöntem **uygun küme sayısının** altına inemez: çıktının kendisi üstelse (bölüm 7.3) iş de üsteldir.

### 4.2 Kâhin: bit maskesi

```
algoritma BİT-MASKESİ(akts[0..n−1])
    m ← 0'dan 2ⁿ − 1'e kadar her m için           ▷ 64 bitlik sayaç: 1ULL << n
        toplam ← Σ { akts[i] : m'nin i. biti 1 }
        eğer koşullar sağlanıyorsa m'yi kaydet
    kayıtları sözlük sırasına diz (qsort; yalnızca kâhin)
```

Maskeler sayısal sırada gezilir; bu sıra sözlük sırası değildir ({0, 1} = 3, {2} = 4 iken sözlük sırasında {0, 1} < {0, 2} = 5 < {1} = 2 …). Bu yüzden kâhinin sonucu `maske_sozluk_karsilastir` ile sıralanır. Karşılaştırıcının kuralı: ilk farklı indis i olsun; i'yi içeren küme, öteki kümede i'den büyük bir indis **varsa** önce gelir, **yoksa** öteki küme onun öneki olduğu için sonra gelir.

## 5. Kullanım

### 5.1 `ders_sec`

```
./ders_sec --alt A --ust U [--havuz dosya.csv] [--en-fazla K]
           [--yontem budamasiz|ust|ust_alt|bitmaske|hepsi] [--sayi] [--goster M]
  varsayılan havuz ornek_veri/secmeli_dersler.csv; varsayılan yöntem ust_alt
  hepsi : dört yöntemi çalıştırır, sonuçları kâhinle (bit maskesi) karşılaştırır
  --sayi: kümeleri yazmadan say · --goster M: en çok M küme (50)
```

Havuz dosyası `;` ayraçlı UTF-8 CSV'dir: `kod;ad;akts` başlığı (isteğe bağlı), kod 1–11 karakter (A–Z, 0–9) ve havuzda benzersiz, ad 1–63 bayt (harf, boşluk, kesme işareti, kısa çizgi), AKTS 1..30; en az 1, en çok 30 ders. Elle izlenen küçük havuz (Şekil 1):

```
$ ./ders_sec --havuz testler/havuz_kucuk.csv --alt 7 --ust 9 --yontem hepsi
Havuz: testler/havuz_kucuk.csv · 4 ders · toplam 18 AKTS
   1) A        Algoritma Analizi           5 AKTS
   2) B        Bulut Bilişim               4 AKTS
   3) C        Kriptografi                 6 AKTS
   4) D        Doğal Dil İşleme            3 AKTS
Kısıt: AKTS toplamı [7, 9]
Uygun küme sayısı: 4
      1) A + B                                        =  9 AKTS (2 ders)
      2) A + D                                        =  8 AKTS (2 ders)
      3) B + D                                        =  7 AKTS (2 ders)
      4) C + D                                        =  9 AKTS (2 ders)
Yöntem       Ziyaret edilen düğüm   Budanan   Küme   Kâhinle aynı
budamasiz                      16         0      4   EVET
ust                            13         4      4   EVET
ust_alt                        13         5      4   EVET
bitmaske                       16         0      4   (kâhin)
Kuramsal düğüm sayısı (budamasız ağaç ve bit maskesi): 2^4 = 16
Süre (budamasiz): 0.001 ms
Süre (ust): 0.000 ms
Süre (ust_alt): 0.000 ms
Süre (bitmaske): 0.001 ms
[çıkış kodu: 0]
```

Örnek havuz, "bu dönem seçmeli derslerden 18–20 AKTS alacağım, en fazla 4 ders":

```
$ ./ders_sec --alt 18 --ust 20 --en-fazla 4 --goster 12
Havuz: ornek_veri/secmeli_dersler.csv · 14 ders · toplam 63 AKTS
   1) BIL331   Veri Madenciliği            5 AKTS
   2) BIL333   Bilgisayar Grafiği          5 AKTS
   3) BIL335   Mobil Programlama           4 AKTS
   4) BIL337   Siber Güvenliğe Giriş       5 AKTS
   5) BIL339   Görüntü İşleme              6 AKTS
   6) BIL341   Yapay Zekâ                  6 AKTS
   7) BIL343   Web Programlama             4 AKTS
   8) BIL345   Bulut Bilişim               3 AKTS
   9) BIL347   Oyun Programlama            4 AKTS
  10) BIL349   Gömülü Sistemler            6 AKTS
  11) BIL351   Doğal Dil İşleme            5 AKTS
  12) BIL353   Nesnelerin İnterneti        4 AKTS
  13) BIL355   Kriptografi                 3 AKTS
  14) BIL357   Bilgi Erişim                3 AKTS
Kısıt: AKTS toplamı [18, 20] · en fazla 4 ders
Uygun küme sayısı: 519
      1) BIL331 + BIL333 + BIL335 + BIL337            = 19 AKTS (4 ders)
      2) BIL331 + BIL333 + BIL335 + BIL339            = 20 AKTS (4 ders)
      3) BIL331 + BIL333 + BIL335 + BIL341            = 20 AKTS (4 ders)
      4) BIL331 + BIL333 + BIL335 + BIL343            = 18 AKTS (4 ders)
      5) BIL331 + BIL333 + BIL335 + BIL347            = 18 AKTS (4 ders)
      6) BIL331 + BIL333 + BIL335 + BIL349            = 20 AKTS (4 ders)
      7) BIL331 + BIL333 + BIL335 + BIL351            = 19 AKTS (4 ders)
      8) BIL331 + BIL333 + BIL335 + BIL353            = 18 AKTS (4 ders)
      9) BIL331 + BIL333 + BIL337 + BIL343            = 19 AKTS (4 ders)
     10) BIL331 + BIL333 + BIL337 + BIL345            = 18 AKTS (4 ders)
     11) BIL331 + BIL333 + BIL337 + BIL347            = 19 AKTS (4 ders)
     12) BIL331 + BIL333 + BIL337 + BIL351            = 20 AKTS (4 ders)
```

Hatalı havuzlar satır numarasıyla reddedilir: `Hata: testler/havuz_bozuk.csv okunamadı: dosya biçimi hatalı (satır 3)` (AKTS 0) ve `Hata: testler/havuz_tekrar_kod.csv okunamadı: dosya biçimi hatalı (satır 4)` (yinelenen kod); ikisinde de çıkış kodu 1.

### 5.2 `olcer` — seçim işlemleri

```
./olcer budamasiz|ust|ust_alt|bitmaske --n N1,N2,... [--alt A --ust U --en-fazla K]
        [--tekrar T] [--tohum S] [--csv dosya.csv [--ekle]]
```

n burada havuzdaki ders sayısıdır (1..30); havuz `havuz_uret(n, tohum)` ile üretilir (AKTS 3..7, ortak LCG; aynı tohum → aynı havuz → **aynı düğüm sayıları**). Kümeler saklanmaz, yalnızca sayılır. stdout'a `kontrol` (uygun küme sayısı), `ziyaret`, `budanan` ve 2ⁿ; stderr'e süre ve `oran T(n)/T(önceki n)`. CSV sütunları: `islem;n;alt;ust;en_fazla;tekrar;ortanca_ms;ortalama_ms;en_az_ms;en_cok_ms;ilk_ms;isinma_ms;cozum;ziyaret;budanan`.

## 6. Tasarım kararları

1. **"Başlangıç indisli" ağaç, "dahil et/etme" ağacı değil.** İkili dahil et/etme ağacında 2ⁿ⁺¹ − 1 düğüm vardır ve kümeler yalnızca yapraklarda oluşur; başlangıç indisli ağaçta **her düğüm bir kümedir** (2ⁿ düğüm). Böylece budamasız ağacın düğüm sayısı bit maskesinin denediği maske sayısına eşit olur ve iki yöntemin "ziyaret" sayaçları doğrudan karşılaştırılabilir. Ön sıra dolaşım deterministik sözlük sırasını bedavaya verir.
2. **Budama düğüme girişte.** Kural, çocuk üretildikten sonra çocuğun girişinde denetlenir; budanan düğüm "ziyaret edilmiş" sayılır. (Denetimi çocuğu üretmeden yapmak daha az düğüm sayardı; seçim tutarlı olduğu sürece yöntemler arası karşılaştırma geçerlidir. Bu seçim Şekil 1'deki kesikli düğümleri görünür kılar.)
3. **Budama 2 için sonek toplamı.** "Kalan derslerin hepsi" en basit güvenli üst sınırdır ve O(n) ön hesapla O(1)'de denetlenir. Ders sayısı kısıtı (K) varken daha sıkı bir sınır (kalan derslerin en büyük K − adet tanesi) mümkündür; ileri alıştırma olarak bırakıldı.
4. **Değerle aktarılan durum.** `toplam`, `adet` ve `secili` parametrelerle taşınır; yerinde değiştirip geri alma gerekmez, "geri almayı unutmak" hatası (H3 Hata Avcısı) yapısal olarak önlenir.
5. **Maskeler `uint32_t`, döngü sınırı `uint64_t`.** n ≤ 30 olduğundan küme 32 bite sığar; ama `int` türündeki `1 << n` ifadesi n = 31'de işaret bitine taşar, n ≥ 32'de ise kaydırma miktarı türün genişliğini aşar: ikisi de tanımsız davranıştır. Bu yüzden bit maskesi döngüsünün sınırı `1ULL << n` ile kurulur (H3 Hata Avcısı).
6. **Saklamak ya da saymak.** `SecimSonucu.sakla = false` ise kümeler saklanmaz, yalnızca sayılır; ölçümler milyonlarca kümeyi bellekte tutmadan yapılır. Saklama dizisi 64'ten başlayıp ikiye katlanarak büyür.
7. **Kâhin sıralaması yalnızca kâhinde.** `qsort` yalnızca bit maskesi kâhininin sonucunu sözlük sırasına koymak için kullanılır (Yol Haritası 6.5); geri izleme sürümü sırayı kendi dolaşımından alır.
8. **Havuz okuma kuralları.** Dosyadan gelen veri güvenilmez girdidir: alan sayısı, kod biçimi, ad geçerliliği (`ad_gecerli_mi`), AKTS aralığı ve kod benzersizliği denetlenir. Benzersizlik n ≤ 30'da doğrusal aramayla denetlenir (en çok 435 karşılaştırma; bilinçli olarak basit).
9. **Sentetik havuz.** Ölçümler için `havuz_uret` AKTS'yi 3..7 aralığında üretir; ders kodları SEC101, SEC103, …, adlar "Seçmeli Ders A" … biçimindedir. Ortak LCG sayesinde düğüm sayıları **tamamen deterministiktir** ve kabul ölçütü olarak kullanılabilir.

## 7. Ölçümler

### 7.1 Ölçüm düzeni ve ortam

Makine: Intel(R) Xeon(R) Processor @ 2.80GHz, 2 çekirdek (sanal makine), L2 2 MiB (2 × 1 MiB), L3 33 MiB; gcc 13.3.0 (Ubuntu 13.3.0-6ubuntu2~24.04.1), `-std=c17 -Wall -Wextra -pedantic -O2 -g`; tarih 2026-10-12 22:22. Düzen: her n için 1 ısınma + 5 tekrar, ortanca (Sedgewick & Wayne, 2011). Bit maskesi 26 derste ≈ 4 s, budamasız ağaç 28 ve 30 derste ≈ 1,3 ve 5,2 s sürdüğü için bu boyutlar 1 tekrarla ölçüldü (tabloda "(1)"); bit maskesi 28 ve 30 derste **kestirildi** (T(26) · 4 · (n/26) ve T(26) · 16 · (n/26), Θ(n · 2ⁿ) varsayımıyla). Havuzlar `havuz_uret(n, 42)`; `make olcum` toplam 34 s sürdü. Düğüm sayıları sayaçtır (deterministik), süreler bu makineye özgüdür.

### 7.2 Senaryo A: tipik dönem planı, [24, 30] AKTS

| n | 2ⁿ | uygun küme | ziyaret: üst budama | ziyaret: üst + alt | üst / 2ⁿ | ziyaret: budamasız |
|--:|--:|--:|--:|--:|--:|--:|
| 10 | 1 024 | 321 | 853 | 720 | %83,3 | 1 024 |
| 12 | 4 096 | 1 121 | 2 728 | 2 572 | %66,6 | 4 096 |
| 14 | 16 384 | 2 928 | 8 045 | 7 915 | %49,1 | 16 384 |
| 16 | 65 536 | 6 193 | 19 309 | 19 228 | %29,5 | 65 536 |
| 18 | 262 144 | 13 734 | 42 613 | 42 368 | %16,3 | 262 144 |
| 20 | 1 048 576 | 22 486 | 84 472 | 84 407 | %8,1 | 1 048 576 |
| 22 | 4 194 304 | 36 338 | 148 698 | 148 560 | %3,5 | 4 194 304 |
| 24 | 16 777 216 | 67 480 | 247 822 | 247 329 | %1,5 | 16 777 216 |
| 26 | 67 108 864 | 132 564 | 452 697 | 451 085 | %0,67 | 67 108 864 |
| 28 | 268 435 456 | 232 705 | 824 081 | 822 527 | %0,31 | 268 435 456 |
| 30 | 1 073 741 824 | 428 227 | 1 434 525 | 1 431 611 | %0,13 | 1 073 741 824 |

*Tablo 1. Ziyaret edilen düğüm sayıları (senaryo A). Budamasız ağaç ve bit maskesi her n'de tam 2ⁿ düğüm/maske dener; uygun küme sayısı dört yöntemde aynıdır.*

| n | bit maskesi | budamasız | oran | üst budamalı | oran | üst + alt | budamasız / üst |
|--:|--:|--:|--:|--:|--:|--:|--:|
| 10 | 39,3 µs | 5,0 µs | — | 5,2 µs | — | 4,1 µs | 1 |
| 12 | 173,6 µs | 19,6 µs | 3,90 | 16,0 µs | 3,05 | 14,5 µs | 1 |
| 14 | 755,3 µs | 77,7 µs | 3,98 | 43,6 µs | 2,73 | 42,7 µs | 2 |
| 16 | 3,1 ms | 302,8 µs | 3,90 | 98,2 µs | 2,25 | 98,5 µs | 3 |
| 18 | 13,2 ms | 1,2 ms | 4,12 | 218,2 µs | 2,22 | 217,0 µs | 6 |
| 20 | 56,3 ms | 5,1 ms | 4,10 | 428,7 µs | 1,97 | 403,6 µs | 12 |
| 22 | 243,1 ms | 19,5 ms | 3,80 | 711,0 µs | 1,66 | 714,3 µs | 27 |
| 24 | 1,03 s | 75,6 ms | 3,89 | 1,2 ms | 1,69 | 1,3 ms | 63 |
| 26 | 4,27 s (1) | 322,5 ms | 4,27 | 2,3 ms | 1,91 | 2,3 ms | 141 |
| 28 | kestirim ≈ 18 s | 1,25 s (1) | 3,89 | 4,2 ms | 1,81 | 4,2 ms | 302 |
| 30 | kestirim ≈ 79 s | 5,17 s (1) | 4,13 | 7,2 ms | 1,74 | 7,3 ms | 715 |

*Tablo 2. Süreler (ortanca; "(1)": tek tekrar). "oran" sütunları n iki artınca süre oranıdır; son sütun budamasız sürenin üst budamalı süreye oranı.*

![Ziyaret edilen düğüm sayısı](mini_obs_v2_2_olcum_dugum.png)

*Şekil 2. Ziyaret edilen düğüm sayısı (y logaritmik): budamasız ağaç ve bit maskesi 2ⁿ; üst budama senaryo A'da çok daha yavaş büyür; senaryo B'de (kesikli) iki budama da 2ⁿ'ye yaklaşır.*

![Süreler](mini_obs_v2_2_olcum_sure.png)

*Şekil 3. Süreler (y logaritmik): bit maskesi (içi boş üçgenler: kestirim), budamasız geri izleme, üst ve üst + alt budamalı geri izleme (senaryo A).*

Yorum:

- **Budamasız ağaç Θ(2ⁿ):** n iki artınca süre 3,80–4,27 katına çıkar (kuram 2² = 4). Bit maskesi her düğümde n bit taradığı için 26 derste budamasız ağaçtan 13 kat yavaştır (4,27 s ve 322,5 ms); Θ(n · 2ⁿ) ile Θ(2ⁿ) arasındaki fark, sabit çarpan değil, büyüme sınıfı farkıdır.
- **Üst budama:** ziyaret edilen düğüm sayısı n iki artınca yalnızca 1,67–2,40 katına çıkar; ziyaret edilen düğümlerin 2ⁿ'ye oranı 24 derste %1,48, 30 derste %0,13 olarak ölçülür. Sebep: [24, 30] aralığı, AKTS'si 3–7 olan derslerden en çok ≈ 4–10 tanesini alabilir; ağacın derin dalları ilk birkaç adımda budanır. 30 derste üst budamalı arama 7,2 ms, budamasız arama 5,17 s sürer (715 kat).
- **Alt budama bu senaryoda neredeyse etkisizdir:** üst + alt sürümü, üst sürümüne göre küçük havuzda %16, 30 derste yalnızca %0,2 daha az düğüm ziyaret eder (Tablo 1), çünkü 24 AKTS'lik alt sınır, havuzun geri kalanı çok büyükken (sonek toplamı ≫ 24) hiçbir şeyi elemez. Süre farkı ölçüm gürültüsü içindedir.

### 7.3 Senaryo B: yüksek aralık, [60, 70] AKTS

| n | 2ⁿ | uygun küme | ziyaret: üst | ziyaret: üst + alt | üst + alt / üst | budamasız | üst budamalı | üst + alt |
|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| 10 | 1 024 | 0 | 1 024 | 1 | %0,1 | 3,8 µs | 6,0 µs | 0 ns |
| 12 | 4 096 | 1 | 4 096 | 79 | %1,9 | 15,7 µs | 23,6 µs | 238 ns |
| 14 | 16 384 | 172 | 16 384 | 1 645 | %10,0 | 65,8 µs | 95,4 µs | 8,1 µs |
| 16 | 65 536 | 4 254 | 65 501 | 21 756 | %33,2 | 267,3 µs | 417,9 µs | 116,8 µs |
| 18 | 262 144 | 36 662 | 260 469 | 127 696 | %49,0 | 1,1 ms | 1,7 ms | 719,3 µs |
| 20 | 1 048 576 | 261 492 | 1 007 009 | 738 700 | %73,4 | 4,9 ms | 6,2 ms | 4,3 ms |
| 22 | 4 194 304 | 1 260 105 | 3 643 182 | 3 085 675 | %84,7 | 20,5 ms | 22,6 ms | 18,2 ms |
| 24 | 16 777 216 | 4 989 820 | 12 213 788 | 10 525 734 | %86,2 | 84,6 ms | 77,7 ms | 65,7 ms |

*Tablo 3. Senaryo B (n = 10 … 24). 10 derslik havuzun toplamı 60'tan küçük olduğu için alt budama aramayı **kökte** keser (1 düğüm; süre zamanlayıcı çözünürlüğünün altında).*

Bu senaryoda aralık, havuzun toplam AKTS'sinin "ortasına" düşer: uygun küme sayısı n ile birlikte üstel büyür (24 derste 4 989 820 küme) ve üst budama ağacın büyük bölümünü dolaşmak zorunda kalır. Alt budama küçük havuzlarda belirgin kazanç sağlar (12 derste 79, 16 derste 21 756 düğüm; üst budamayla 4 096 ve 65 501), ama n büyüdükçe kazanç %14 düzeyine iner. Dersin kimlik kartındaki cümle burada ölçülmüş olur: **alt kümeleri listelemek çıktı boyutu kadar iş ister; çıktı üstelse hiçbir budama onu polinoma indiremez.**

### 7.4 Örnek havuz (14 ders)

| kısıt | uygun küme | budamasız | üst: ziyaret / budanan | üst + alt: ziyaret / budanan | bit maskesi | kâhinle aynı |
|:--|--:|--:|--:|--:|--:|:-:|
| [18, 20], en fazla 4 ders | 519 | 16 384 | 1 471 / 716 | 1 362 / 976 | 16 384 | EVET |
| [30, 30] | 728 | 16 384 | 9 901 / 2 455 | 7 483 / 4 533 | 16 384 | EVET |
| [15, 18] | 719 | 16 384 | 2 290 / 1 179 | 2 253 / 1 283 | 16 384 | EVET |

*Tablo 4. `ders_sec --yontem hepsi` ile örnek havuzda üç kısıt (çıktılar bölüm 2). Bütün yöntemler kâhinle aynı kümeleri aynı sırada verir.*

[30, 30] kısıtında üst budama 16 384 düğümün 9 901'ini ziyaret eder (alt sınır 30 iken alt budama devreye girer ve sayıyı 7 483'e indirir); en çok 4 ders kısıtı ([18, 20]) ise ağacı 4. düzeyde keserek ziyareti 1 471'e indirir. 14 derste bütün yöntemler 1 ms'nin altında biter: **bu boyutta budama gerekli değildir; budamanın değeri n büyüdükçe ortaya çıkar** (bölüm 7.2).

### 7.5 Sonuç ve H13'e köprü

Geri izleme, "bütün kümeleri listele" sorusunun doğal yanıtıdır; budama, aralık dar olduğunda üstel aramayı pratikte küçük bir ağaca indirir. Ancak soru "**kaç** küme var?" ya da "**en iyi** küme hangisi?" olduğunda listelemek gerekmez: H13'te aynı problem 0/1 sırt çantası olarak dinamik programlamayla O(n · U) zamanda (U: AKTS üst sınırı) çözülecek ve v2.12 bu sürümün sonuçlarıyla karşılaştırılacaktır. v2.2'nin `secim_yap`'ı (bit maskesi kâhiniyle birlikte) o sürümün kâhini olur.

## 8. Testler

- **Birim testleri** (`obs_test`): `150 doğrulama: 37 kural + 22 metin + 24 yapı + 16 dosya + 11 üreteç + 11 sayaç + 13 yinelenen + 16 seçmeli`. Seçmeli testleri: sözlük sırası karşılaştırıcısı (8 kümelik zincir, eşitlik, 31. bit), `maske_ders_sayisi`; 4 derslik havuzda [7, 9] için kümeler (A+B, A+D, B+D, C+D) ve **elle izlenmiş düğüm sayıları** (üst budama 13 ziyaret / 4 budanan; budamasız ve bit maskesi 16; üst + alt 13 / 5); ders sayısı kısıtı; [0, 0] → yalnızca boş küme; alt > toplam → kökte budama (1 düğüm); bütün havuz [18, 18]; ön koşul ihlali (alt > ust); yalnızca sayma; havuz dosyası (başlık, CRLF, boş satır, "Yapay Zekâ") ve altı hatalı dosya (AKTS 0, yinelenen kod, küçük harfli kod, adda rakam, eksik alan, boş havuz; satır numaralarıyla); 31. ders; sentetik havuzun tekrarlanabilirliği.
- **Kâhin testleri** (`test_kahin`): 300 denemede 59 342, 1 000 denemede 189 277 denetim (geri izleme ↔ bit maskesi: 7 000), uyuşmazlık yok. Her denemede 0–14 derslik rastgele havuz (AKTS 1..10), rastgele [alt, ust] ve isteğe bağlı K; dört yöntemin kümeleri, sırası ve düğüm sayıları (budamasız = bit maskesi = 2ⁿ, üst ≤ 2ⁿ, üst + alt ≤ üst) denetlenir.
- **Kasıtlı hata** (`--hata-goster budama`): üst budama koşulu `toplam > ust` yerine `toplam >= ust` yazılırsa toplamı **tam ust** olan kümeler kayda ulaşmadan budanır:

```
$ ./test_kahin --hata-goster budama
KÂHİN UYUŞMAZLIĞI (tohum 1)
  İşlev      : ust
  n          : 9
  Beklenen   : 66 küme (bit maskesi kâhini)
  Bulunan    : 53 küme
  Karşı örnek: havuz AKTS = [2, 3, 4, 10, 5, 6, 7, 7, 5], aralık [5, 14], en fazla 0 ders (0: sınırsız)
  Kaçırılan küme: {K0, K1, K2, K4} = 14 AKTS
  Kaçırılan küme: {K0, K1, K2, K8} = 14 AKTS
  Yeniden üretmek için: ./test_kahin --tohum 1 --deneme 1 --hata-goster budama
```

  Hatalı kural toplamı **tam** üst sınır olan her düğümü kayda ulaşmadan budar; bu yüzden kaybolan 66 − 53 = 13 kümenin hepsinin toplamı 14'tür. Kâhin, ilk sekiz kâhin kümesi içinden kaçırılan ikisini adlarıyla gösterir. Sınır değerleri (≤ ile <) geri izlemede en sık yapılan hatadır ve küçük örnekte bile gözden kaçabilir.
- **Bellek**: `make asan` temiz (`ders_sec` ve `olcer` seçim işlemleri dahil).

## 9. Ders notu için özet (Hafta 3 · Mini-OBS 2 adımı)

**Bu hafta:** Mini-OBS'ye bir seçmeli ders planlayıcısı ekliyoruz: AKTS toplamı belirli bir aralıkta kalan bütün ders kümelerini geri izlemeyle üretiyor, budamanın kazancını düğüm sayacıyla ve süreyle ölçüyor, sonucu bit maskesi kaba kuvvetiyle doğruluyoruz.

### Gereksinimler

- `secmeli.c`: `havuz_oku`/`havuz_yukle` (CSV `kod;ad;akts`, kurallar bölüm 5.1), `secim_yap` (budamasız, üst budamalı, üst + alt budamalı geri izleme ve bit maskesi), `maske_sozluk_karsilastir`, `maske_akts`, `maske_ders_sayisi`; ziyaret ve budanan düğüm sayaçları.
- Kümeler **sözlük sırasında** üretilmeli (geri izlemede ön sıra dolaşımdan; bit maskesinde sıralamayla).
- İsteğe bağlı en çok K ders kısıtı (K = 0: sınırsız).
- `ders_sec.c`: `--alt`, `--ust`, `--havuz`, `--en-fazla`, `--yontem`, `--sayi`, `--goster`; geçersiz kullanımda 2, havuz hatasında 1.
- `olcer.c`: en az `budamasiz`, `ust` ve `bitmaske` işlemleri (n = havuzdaki ders sayısı); CSV'de ziyaret ve süre.
- `test_obs.c` ve `test_kahin.c`: 4 derslik havuzun elle izlenmiş sonuçları; rastgele havuzlarda bit maskesi kâhini.
- Ölçüm raporu: n = 10, 12, …, ≥ 24 için düğüm sayısı ve süre tablosu, yarı logaritmik grafik, budamanın etkisinin yorumu; ölçülemeyen boyutlar için kestirim.

### İpuçları

- Önce ağacı **kâğıda** çizin: 4 derslik havuzda 16 düğüm; hangi düğümler budanır?
- Durumu (toplam, adet, maske) parametreyle taşıyın; global bir dizide tutarsanız her dönüşte geri almayı unutmayın.
- Budama koşulunda `>` ile `>=` arasındaki fark bir hatadır: toplamı tam üst sınır olan küme geçerlidir.
- "Toplam aşıldı" budaması yalnızca **pozitif** değerlerde doğrudur; AKTS'yi okurken 1'den küçük değerleri reddedin.
- `1 << n` yerine `1u << n` (maske) ve `1ULL << n` (döngü sınırı) yazın; `int` ile n = 31 ve n ≥ 32 tanımsız davranıştır.
- Ölçerken kümeleri saklamayın, yalnızca sayın; yoksa ölçtüğünüz şey `realloc` olur.
- Kâhinin sonucunu karşılaştırmadan önce sözlük sırasına koyun; bit maskesinin sayısal sırası sözlük sırası değildir.

### Kabul ölçütleri (denetlenebilir)

1. `make` ve `make test` sıfır uyarıyla derlenir; bütün birim testleri ve `test_kahin` (300 deneme) geçer.
2. `./ders_sec --havuz testler/havuz_kucuk.csv --alt 7 --ust 9 --yontem hepsi`: 4 küme sırasıyla A+B (9), A+D (8), B+D (7), C+D (9); ziyaret: budamasız 16, üst 13 (budanan 4), üst + alt 13 (budanan 5), bit maskesi 16; her satırda "Kâhinle aynı: EVET".
3. Örnek havuz (`ornek_veri/secmeli_dersler.csv`): [18, 20] ve en fazla 4 ders → **519** küme; [30, 30] → **728**; [15, 18] → **719**; dört yöntem aynı.
4. Sınır durumları: [0, 0] → yalnızca boş küme (1); 4 derslik havuzda [19, 30] → 0 küme ve üst + alt budamada 1 ziyaret; `--alt 20 --ust 10` → çıkış 2; AKTS'si 0 olan satır → "dosya biçimi hatalı (satır 3)", çıkış 1.
5. Deterministik düğüm sayıları (`havuz_uret`, tohum 42, [24, 30]): `./olcer ust --n 20` → kontrol 22 486, ziyaret 84 472, budanan 55 568; `./olcer ust_alt --n 20` → ziyaret 84 407; `./olcer budamasiz --n 20` → ziyaret 1 048 576.
6. Budamanın etkisi (kendi makinenizde, senaryo A, n = 24): üst budamalı arama 2²⁴ düğümün %2'sinden azını ziyaret eder ve budamasız aramadan en az 20 kat hızlıdır (bu makinede %1,48 ve 63 kat).
7. Budamasız arama için n iki artınca süre oranı 3,5–4,5 arasındadır (n ≥ 16).
8. `--hata-goster budama` ile kâhin hatalı budamayı yakalar, kaçırılan kümeleri basar, 1 ile çıkar.
9. `make asan` temiz.

### Test senaryoları

| # | Girdi | Beklenen çıktı / davranış |
|---|---|---|
| 1 | 4 derslik havuz, [7, 9] | A+B, A+D, B+D, C+D; düğümler 16 / 13 / 13 / 16 |
| 2 | aynı havuz, [7, 9], en fazla 1 ders | 0 küme |
| 3 | aynı havuz, [0, 0] | 1 küme: {} (0 AKTS, 0 ders) |
| 4 | aynı havuz, [18, 18] | 1 küme: A+B+C+D |
| 5 | aynı havuz, [19, 30] | 0 küme; üst + alt budamada kök budanır (1 düğüm) |
| 6 | örnek havuz, [18, 20], en fazla 4 | 519 küme; ilk küme BIL331 + BIL333 + BIL335 + BIL337 (19 AKTS) |
| 7 | örnek havuz, [30, 30], `--yontem hepsi --sayi` | 728 küme; üst 9 901, üst + alt 7 483 düğüm |
| 8 | `--alt 20 --ust 10` | kullanım iletisi, çıkış 2 |
| 9 | `testler/havuz_bozuk.csv` | "dosya biçimi hatalı (satır 3)", çıkış 1 |
| 10 | `testler/havuz_tekrar_kod.csv` | "dosya biçimi hatalı (satır 4)", çıkış 1 |
| 11 | `./olcer budamasiz --n 10,12,14` | ziyaret 1 024 · 4 096 · 16 384 (= 2ⁿ) |
| 12 | `./test_kahin --hata-goster budama` | "KÂHİN UYUŞMAZLIĞI", kaçırılan kümeler (toplamı tam üst sınır), çıkış 1 |

### Başlangıç noktası (öğrenciye verilenler)

- **Verilir:** kendi v2.1'iniz (ya da referans v2.1), `secmeli.h` (yapılar, bildirimler, sözleşmeler), `ornek_veri/secmeli_dersler.csv`, `testler/havuz_kucuk.csv`, `testler/havuz_bozuk.csv`, `testler/havuz_tekrar_kod.csv`, `havuz_uret` (deterministik düğüm sayıları için hazır).
- **Yazılır:** `secmeli.c` (havuz okuma, geri izleme, bit maskesi, karşılaştırıcı), `ders_sec.c`; `olcer.c`'ye seçim işlemleri; `test_obs.c` ve `test_kahin.c`'ye seçim testleri; `Makefile`'a `ders_sec` ve yeni `olcum` adımları.
- **Değiştirilmez:** v2.1'in modülleri (`obs`, `dosya`, `sayac`, `yinelenen`, `uretec`), ortak modüller.
- **Meydan okuma:** (a) en çok K ders kısıtında budama 2'yi "kalan derslerin en büyük K − adet tanesi" ile sıkılaştırın ve düğüm sayısındaki azalmayı ölçün; (b) havuzu AKTS'ye göre azalan sırada dolaşmanın budamaya etkisini ölçün (dikkat: çıktı sırası değişir; kâhinle karşılaştırmadan önce sıralayın).

## 10. Bilinen sınırlılıklar

- Havuz en çok 30 derstir (`uint32_t` maske); 30 derste budamasız arama ≈ 5 s, bit maskesi ≈ 79 s (kestirim) sürer. Uygun küme sayısı çok büyükse (ör. geniş aralık) listeleme belleği ve ekranı doldurur; `--sayi` kullanılmalıdır.
- Alt budamanın sınırı (sonek toplamı) en çok K ders kısıtını hesaba katmaz; bu yüzden K'li sorgularda gerekenden fazla düğüm ziyaret edilebilir.
- Ders adları dosyadaki gibi yazılır (normalleştirilmez); kodlar büyük harf olmalıdır.
- `ders_sec` henüz `mini_obs` menüsüne bağlı değildir (v3.0'da bütünleştirilecek); öğrenci bazlı (ör. alınmış dersler, önkoşullar) kısıtlar yoktur (önkoşullar H11'de, v2.10).
- Süreler tek bir sanal makinede ölçülmüştür; küçük n'lerde (< 0,1 ms) zamanlayıcı çözünürlüğü ve gürültü nedeniyle oranlar güvenilmezdir. Düğüm sayıları ise makineden bağımsızdır.

## 11. Kaynaklar

- Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2022). *Introduction to algorithms* (4th ed.). MIT Press.
- Sedgewick, R., & Wayne, K. (2011). *Algorithms* (4th ed.). Addison-Wesley.
- Skiena, S. S. (2020). *The algorithm design manual* (3rd ed.). Springer.
- Wirth, N. (1971). Program development by stepwise refinement. *Communications of the ACM, 14*(4), 221–227. https://doi.org/10.1145/362575.362577
