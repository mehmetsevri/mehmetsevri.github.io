# Mini-OBS 2 v2.12 — Dinamik programlama: ders seçimi (0/1 sırt çantası) ve "Bunu mu demek istediniz?" (Hafta 13)

**Bu sürümün amacı:** Hafta 13'ün dinamik programlamasını (Bellman, 1957) Mini-OBS'nin iki sorusuna uygulamak. (1) **Ders seçimi:** AKTS üst sınırı W altında öğrencinin tercih puanları toplamını en büyük yapan ders kümesi bir **0/1 sırt çantası** problemidir; tam DP tablosu (Θ(n·W)) en iyi değeri ve **geri çıkarmayla** seçilen dersleri verir, eşitlikte belirleyici bir kuralla (en büyük indisli farklı dersi ALMA). Aynı problem dört stratejiyle yan yana çözülür (yol haritası H13): v2.2'nin **geri izleme** ağacı (aynı düğüm sayısı, kâhinle doğrulanır), **dal ve sınır** (H12'nin kesirli sırt çantası sınırıyla), **açgözlü** (puan/AKTS oranı — örnekte en iyiden 20 puan az) ve **kaba kuvvet** (n ≤ 25). (2) **"Bunu mu demek istediniz?":** menüdeki ad araması sonuç vermezse ad, soyad ve tam ad terimlerinden **düzenleme (Levenshtein) uzaklığı** en küçük olanlar önerilir; uzaklık v2.4/v2.9'un Türkçe katlamasıyla büyük/küçük harf duyarsız ve **kod noktası** düzeyindedir (bayt düzeyinde "SAHIN" ↔ "ŞAHİN" 2 değil 4 olurdu, § 4.5). Ölçüm (§ 8): W = 30'da geri izlemenin düğüm sayısı n = 10'dan 50'ye 896 → 147 198 469 olurken DP'nin hücresi 341 → 1 581 olur; W = 45, n = 35'te geri izleme 651,9 ms, DP 1,6 µs sürer, n = 60'ta geri izleme ≈ 7 dakika sürerdi (**kestirim**, düğüm sayısı kesin hesaplandı). 100 000 kayıtta öneri sorgusu sözlükle 272,1 µs, sözlüksüz (her kaydın üç terimiyle DP) 38,1 ms sürer: aynı terim için DP'yi bir kez çalıştırmak (300 000 terim → 1 679 farklı terim) 140 kat kazandırır; uzunluk farkı budaması (kovalarla) DP hücrelerinden k = 5'te %11 kadarını, k = 1'de %42 kadarını atlar.

Dosyalar (satır sayılarıyla): **`secim.h`** (134) · **`secim.c`** (458) · **`oneri.h`** (137) · **`oneri.c`** (458) · **`ders_secimi.c`** (512) · **`olcer_dp.c`** (552) · `main.c` (351) · `ara.c` (556) · `test_obs.c` (3587) · `test_kahin.c` (6270) · `Makefile` (871) · önceki sürümlerin bütün dosyaları · `ornek_veri/tercihler.csv` (18 satır) · `ornek_veri/tercihler_katalog.csv` (53 satır) · `testler/tercih_bozuk.csv` · `testler/T7_oneri.txt` (menü oturumu) · `olcum/sirt.csv`, `olcum/dp_buyuk.csv`, `olcum/oneri.csv`, `olcum/oneri_k.csv`, `olcum/OLCUM_ORTAMI.txt` · `mini_obs_v2_12_ciktilar.txt` (1766 satır, gerçek çıktılar). Şekiller: `mini_obs_v2_12_tablo.png`, `mini_obs_v2_12_levenshtein.png`; grafik: `mini_obs_v2_12_olcum.png`.

Derleme: `make` (önceki programlar + **`ders_secimi`**, **`olcer_dp`**; `mini_obs` ve `ara` artık `oneri.o`'yu bağlar), `make test`, `make olcum` (bu makinede 38 s), `make ornek`, `make asan`, `make valgrind`, `make temiz`. Bayraklar `-std=c17 -Wall -Wextra -pedantic -O2 -g`; 55 kaynak dosya `-O0 … -Os` düzeylerinde `-Werror` ile uyarısız. Çıkış kodları: 0; 1 (dosya okunamadı ya da biçim hatası, öğrenci bulunamadı, bellek yetersiz, yöntemler ya da öneriler uyuşmadı; testlerde uyuşmazlık); 2 (hatalı kullanım, bilinmeyen ders kodu ve sınır dışı n, W, k dahil).

## 1. Amaç ve haftanın kavramıyla bağı

Haftanın Büyük Sorusu: "Açgözlü yöntemin başarısız olduğu bir bozuk para sisteminde (H12), tüm olasılıkları denemeden en iyi yanıtı nasıl buluruz?" Mini-OBS'de aynı soru ders seçiminde sorulur (puan/AKTS oranıyla açgözlü seçim en iyiyi kaçırır) ve iki DP yanıtı vardır (Kleinberg ve Tardos, 2006; Cormen vd., 2022; yöntemin adının öyküsü için Bellman, 1984):

- **0/1 sırt çantası** (Konu: "O(nW) tablo; sözde polinom zaman kavramı; tek satıra indirgeme (ters yönlü döngü)"; Örnek 10–11; ÖÇ 13.3–13.4): durum (i, c) = "ilk i ders, en çok c AKTS"; geçiş "al ya da alma"; temel durum T[0][c] = 0; hesaplama sırası satır satır; yanıt T[n][W]; çözüm tablodan **geri çıkarılır** (§ 4.1). Tek satırlı sürüm yalnız değeri verir — bellek–zaman ödünleşimi (Mühendis Gözüyle).
- **Aynı problem dört stratejiyle** (Konu; ÖÇ 13.5; Atölye "Strateji turnuvası"): v2.2'nin geri izlemesi O(2ⁿ), H12'nin açgözlüsü (yanlış), dal ve sınır, DP; kaba kuvvet n ≤ 25'te durdurulur, ötesi kestirilir (§ 4.3, § 8.1).
- **Düzenleme uzaklığı ve "Bunu mu demek istediniz?"** (Konu: "2B DP: … düzenleme (Levenshtein) uzaklığı"; Örnek 9; Atölye "Yazım düzeltici: Türkçe kelime listesiyle"): iki satırlık tamponla Θ(m·n) zaman, Θ(n) bellek (Kaputun Altında: "O(nm) tablodan iki satıra geçiş; çözümü geri çıkarma olanağının kaybedilmesi") (§ 4.5).
- **Örtüşen alt problemler, büyük ölçekte:** 100 000 kayıtta 300 000 terimden farklı olanların sayısı yalnız 1 679. Sözlük, aynı terimin uzaklığını bir kez hesaplar — memoization'ın veri düzeyindeki karşılığı (§ 4.6, § 8.3).
- **Hata Avcısı:** "Tek satırlı 0/1 sırt çantasında kapasitenin artan sırada dolaşılması" kasıtlı hata olarak kâhine yakalatılır (`--hata-goster sinirsiz`, § 9).

Yol haritasındaki karşılığı (Tablo A.1): **H13 · v2.12 · Ders seçimi optimizasyonu; "Bunu mu demek istediniz?" · 0/1 sırt çantası, düzenleme uzaklığı.**

## 2. v2.11'den ne değişti?

| Konu | v2.11 (H12) | v2.12 (H13) |
|---|---|---|
| Ders seçimi | v2.2: AKTS aralığına uyan bütün kombinasyonlar (geri izleme) | **`secim.h/.c`**: aday listesi ve tercih dosyası, 0/1 sırt çantası — tam tablo + geri çıkarma, tek satır, v2.2 ağacında geri izleme, dal ve sınır, açgözlü, kesirli sınır, kaba kuvvet, v2.2 düğüm sayısının sayım DP'siyle hesabı |
| Öneri | — | **`oneri.h/.c`**: kod noktası ve bayt düzeyinde Levenshtein, katlama + kod noktası çözme, terim sözlüğü (ad, soyad, tam ad; Türkçe sıra, kayıt sayısı, tür), en yakın k (üç budama), menü önerisi |
| Menü (`mini_obs`) | 3) Ara: sonuç yoksa "Eşleşen kayıt yok" | + "Bunu mu demek istediniz? …" (en çok 3 öneri, eşik m / 3 + 1); sonuç bulunan aramalar aynı |
| `ara` | `--no`, `--soyad`, `--icinde` | + `--oneri SORGU [--k K] [--budama yok\|uzunluk\|kova\|hepsi]` |
| Programlar | `sinav_programi`, `olcer_sinav` | + **`ders_secimi`** (havuz ve katalog kipi, DP tablosu ve geri çıkarma izi), **`olcer_dp`** (strateji turnuvası, öneri ölçümleri) |
| Testler | 426 birim; kâhin 678 664 denetim | 439 birim (+13 seçim-öneri); kâhin 686 464 denetim; `--hata-goster sinirsiz`, `--hata-goster bayt` |

v1.0'ın T2 oturumu yine yalnızca başlık ve arama istemi satırlarında farklıdır (`mini_obs_v2_12_ciktilar.txt`, Regresyon bölümü): öneri satırı yalnız sonuç vermeyen aramada basılır.

## 3. Mimari

| Modül / program | Sorumluluk | Bağımlılık |
|---|---|---|
| `secim` (**yeni**) | aday listesi, tercih dosyası, sırt çantası yöntemleri, düğüm sayımı | `dosya` (durum kodları), `metin`, `ortak_rastgele` |
| `oneri` (**yeni**) | Levenshtein, katlama, terim sözlüğü, en yakın k, menü önerisi | `turkce` (utf8_coz, tr_katla, tr_karsilastir), `obs` (Sinif) |
| `ders_secimi.c` (**yeni**) | havuz kipi (v2.2 havuzu) ve katalog kipi (v2.10 alınabilir dersler), dört strateji, v2.2 `secim_yap` ile düğüm kıyası, önkoşul denetimi | `secim`, `secmeli`, `onkosul`, `graf`, `karma`, `zamanlayici` |
| `olcer_dp.c` (**yeni**) | strateji turnuvası (süre bütçeli kestirim), büyük n·W'de DP, öneri ölçümleri ve sözlüksüz taban çizgisi | `secim`, `oneri`, `uretec`, `deney` |
| `main.c`, `ara.c` | + öneri | `oneri` |
| diğerleri | v2.11'den aynen | — |

`secim` kayıt yapısını (`Ogrenci`) bilmez: adaylar (kod, ad, AKTS, puan) dışarıdan gelir; bu yüzden aynı modül hem v2.2'nin seçmeli havuzunu hem v2.10'un kataloğunu çözer. `oneri` ise yalnız `Sinif`'in ad ve soyad alanlarını okur.

## 4. Algoritmalar ve veri yapıları

### 4.1 0/1 sırt çantası: tablo, geri çıkarma ve tek satır

**DP reçetesi** (yol haritası H13):

1. **Durum:** T[i][c] = ilk i dersten, AKTS toplamı en çok c olan bir kümenin en büyük tercih puanı (0 ≤ i ≤ n, 0 ≤ c ≤ W).
2. **Geçiş:** i. dersi ya almayız ya alırız: T[i][c] = max(T[i−1][c], v_i + T[i−1][c − w_i]) (ikincisi yalnız w_i ≤ c iken).
3. **Temel durum:** T[0][c] = 0 (ders yok).
4. **Hesaplama sırası:** satır satır (i artan); her satır yalnız bir öncekine bağlıdır.
5. **Yanıt:** T[n][W].
6. **Geri çıkarma:** c = W'den başlayarak i = n, …, 1: T[i][c] = T[i−1][c] ise ders i **alınmaz**; değilse alınır ve c −= w_i.

```
Havuz: ornek_veri/secmeli_dersler.csv · 14 ders · AKTS toplamı 63
Tercihler: ornek_veri/tercihler.csv · adayların puan toplamı 765 · AKTS üst sınırı W = 20
0/1 sırt çantası — DP (tam tablo 15 × 21 = 315 hücre, 1260 bayt; geri çıkarmada eşitlikte dersi ALMA):
  en büyük tercih puanı 315 · AKTS 20 / 20 · 5 ders: BIL331 BIL341 BIL345 BIL355 BIL357
    BIL331   Veri Madenciliği                      5 AKTS · puan  75
    BIL341   Yapay Zekâ                            6 AKTS · puan 100
    BIL345   Bulut Bilişim                         3 AKTS · puan  40
    BIL355   Kriptografi                           3 AKTS · puan  40
    BIL357   Bilgi Erişim                          3 AKTS · puan  60
  satır tamponlu DP (yalnız değer, 21 int, 294 hücre): 315 — AYNI
```

![DP tablosu](mini_obs_v2_12_tablo.png)

*Şekil 1. Örnek havuz (v2.2'nin 14 seçmeli dersi; KURGUSAL tercih puanları), W = 20: 315 hücrelik tablo ve geri çıkarma yolu (`./ders_secimi --tablo`). Yeşil: ders alındı; sarı: eşitlik (BIL351 alınsa da alınmasa da 215) — kural ALMA; gri: alınmadı. Son hücre T[14][20] = 315.*

```
  Geri çıkarma (i = 14 … 1; T[i][c] = T[i−1][c] ise ALMA):
    14 BIL357   c = 20: T = 315 ≠ T[13][20] = 310 → ALINDI, c = 17
    13 BIL355   c = 17: T = 255 ≠ T[12][17] = 250 → ALINDI, c = 14
    12 BIL353   c = 14: T = 215 = T[11][14] → ALINMADI
    11 BIL351   c = 14: T = 215 = T[10][14] — alınsaydı da 75 + T[10][9] = 215 (EŞİTLİK) → ALINMADI
    10 BIL349   c = 14: T = 215 = T[9][14] → ALINMADI
     9 BIL347   c = 14: T = 215 = T[8][14] → ALINMADI
     8 BIL345   c = 14: T = 215 ≠ T[7][14] = 205 → ALINDI, c = 11
     7 BIL343   c = 11: T = 175 = T[6][11] → ALINMADI
     6 BIL341   c = 11: T = 175 ≠ T[5][11] = 150 → ALINDI, c = 5
     5 BIL339   c =  5: T =  75 = T[4][5] → ALINMADI
     4 BIL337   c =  5: T =  75 = T[3][5] → ALINMADI
     3 BIL335   c =  5: T =  75 = T[2][5] → ALINMADI
     2 BIL333   c =  5: T =  75 = T[1][5] → ALINMADI
     1 BIL331   c =  5: T =  75 ≠ T[0][5] =   0 → ALINDI, c = 0
```

- **Değişmez:** i. satır yazıldıktan sonra T[i][c] (c = 0..W) ilk i dersin en iyisidir (tümevarım: en iyi kümede ders i ya yoktur — T[i−1][c] — ya vardır — v_i + T[i−1][c − w_i]).
- **Sözde polinom:** iş (n+1)(W+1) hücredir; W'nin **değerine** doğrusal, ama W'yi yazmak için gereken **bit sayısına** üsteldir. AKTS sınırı küçük bir tamsayı olduğu için (W ≤ 1 000) burada çok hızlıdır (§ 8.2).
- **Tek satır** (`sirt_cantasi_deger`): T[i][·] yalnız T[i−1][·]'e bağlı olduğundan tek dizi yeter — ama c **azalan** gezilmelidir: c artan gezilirse R[c − w] bu dersin satırında güncellenmiş olur ve ders birden çok kez alınır (sınırsız sırt çantası; Hata Avcısı, § 9). Tek satır yalnız **değeri** verir; hangi derslerin seçildiği bilgisi kaybolur (Kaputun Altında): kümeyi isteyen tam tablo tutar.

### 4.2 Eşitlik kuralı

Birden çok en iyi küme olabilir (örnekte {BIL331, BIL341, BIL345, BIL355, BIL357} ile {BIL341, BIL345, BIL351, BIL355, BIL357}: ikisi de 315 puan, 20 AKTS). Geri çıkarma T[i][c] = T[i−1][c] olduğunda dersi almaz; bu, kümeleri bit maskesi (bit i = ders i) olarak düşünürsek **en küçük maskeyi** seçmektir: iki en iyi kümenin farklı olduğu en büyük indisli ders, seçilen kümede yoktur. Kanıt: i = n'den geriye, "almadan da en iyiye ulaşılabiliyorsa alma" kararı en yüksek biti 0 yapar; kalan seçim aynı kuralla alt probleme iner. Geri izleme ve dal-sınır en iyiyi "puan büyükse ya da puan eşit ve maske küçükse" günceller, kaba kuvvet maskeleri artan sırada dener: **dört yöntem aynı kümeyi verir** (birim testi ve kâhin). Dal ve sınırda budama **kesin** küçüklükle yapılır: sınır en iyiye eşitse dal budanmaz, yoksa eşit puanlı daha küçük maske kaybolabilirdi.

### 4.3 Aynı problem dört stratejiyle

| Strateji | İş | Örnek havuzda (W = 20) | Doğru mu? |
|---|---|---|---|
| Kaba kuvvet (bit maskesi) | 2ⁿ küme × n | 16 384 küme | en iyi (kâhin) |
| Geri izleme (v2.2 ağacı, AKTS > W ise dur) | uygun kümeler kadar düğüm, O(2ⁿ) | 3 264 düğüm (1 569 budandı); v2.2 `secim_yap` 1 695 uygun küme, aynı düğüm | en iyi |
| Dal ve sınır (+ kesirli sırt çantası sınırı) | sınıra bağlı | 299 düğüm (215 budandı) | en iyi |
| Açgözlü (puan/AKTS oranı, sığanı al) | sıralama + tek geçiş | 295 puan | **değil** (−20) |
| DP (tam tablo) | (n+1)(W+1) hücre | 315 hücre | en iyi |

```
Açgözlü (puan/AKTS oranı azalan, sığanı al — H12): puan 295 · AKTS 18 · BIL331 BIL335 BIL341 BIL357 → en iyiden 20 puan az (EN İYİ DEĞİL)
Kesirli sırt çantası (son ders bölünebilseydi; 0/1 için üst sınır): 325
Geri izleme (v2.2 ağacı, üst sınır budaması): puan 315 · 3264 düğüm (1569 budandı) · küme: AYNI
Dal ve sınır (+ kesirli sırt çantası sınırı): puan 315 · 299 düğüm (215 budandı) · küme: AYNI
Kaba kuvvet (bit maskesi, 2^14 = 16384 küme): puan 315 · küme: AYNI
v2.2 secim_yap(YONTEM_UST, AKTS 0..20): 1695 uygun küme · 3264 düğüm (geri izleme 3264, sayım DP'si 3264: AYNI)
Düğüm ↔ hücre: v2.2 ağacı 3264 düğüm (sayım DP'si) ↔ DP 315 hücre
```

- **Geri izleme = v2.2.** v2.2'nin `secim_yap(YONTEM_UST)` ağacı AKTS aralığındaki **bütün** kümeleri sayar; v2.12 aynı ağaçta yalnız en iyiyi tutar. Düğüm sayısı ikisinde aynıdır ve **aramadan** hesaplanabilir: kök + Σ_{S uygun} (n − 1 − max S) (her uygun küme, en büyük indisinden sonraki dersler kadar çocuk açar). `geri_izleme_dugum_hesapla` bunu "en büyük indisi i, AKTS'si x olan küme sayısı" üzerinden bir **sayım DP'siyle** O(n·W)'de bulur; ölçücü, çalıştırılamayacak kadar büyük ağaçların düğüm sayısını böyle **kesin** bilir ve yalnız süreyi kestirir (§ 8.1).
- **Açgözlü neden yanılır?** Oran sırası: BIL357 (60/3 = 20), BIL341 (100/6 ≈ 16,7), sonra oranı 15 olan BIL331, BIL335 ve BIL351 (eşitlikte küçük indis); ilk dördü 18 AKTS eder ve kalan 2 AKTS'ye hiçbir ders sığmaz. Kesirli sırt çantasında son dersin bir kısmı alınabilseydi açgözlü en iyi olurdu (325, H12); 0/1 sürümünde açgözlü seçim özelliği yoktur. Kesirli değer 0/1 problemin **üst sınırıdır**: dal ve sınır onu kullanır.
- W = 30'da DP 455 puanı bulur, açgözlü 450; W = 45'te açgözlü bu örnekte en iyiye (625) eşittir (`mini_obs_v2_12_ciktilar.txt`, bölüm 2). Rastgele adaylarda açgözlü 27 noktadan 9 tanesinde en iyiden az bulur (en çok 27 puan; en kötü oran 0,948; § 8.1).

### 4.4 Önkoşul kısıtı: katalog kipi

Katalog kipinde adaylar v2.10'un **şimdi alınabilecek** dersleridir: alınmamış ve bütün önkoşulları alınmış dersler. Bir aday başka bir adayın önkoşulu olamaz (önkoşulu alınmamış ders aday değildir), bu yüzden adayların **her alt kümesi önkoşul açısından geçerlidir** ve sırt çantası doğrudan uygulanır. Program yine de seçilen her dersin önkoşullarını ters grafta denetler. **Kapsam dışı:** aynı dönemde bir dersi ve onun önkoşulunu birlikte almak (önkoşul kısıtlı sırt çantası; ağaç DP'si gerektirir) — v2.10'un kuralı buna izin vermez.

```
$ ./ders_secimi --katalog ornek_veri/onkosul.txt --alinan BLM101,MAT101,FIZ101,BLM102 --akts 30
Katalog: ornek_veri/onkosul.txt · 48 ders · alınan 4 ders · adaylar: şimdi alınabilecek 12 ders (bütün önkoşulları alınmış)
Tercihler: ornek_veri/tercihler_katalog.csv · adayların puan toplamı 670 · AKTS üst sınırı W = 30
0/1 sırt çantası — DP (tam tablo 13 × 31 = 403 hücre, 1612 bayt; geri çıkarmada eşitlikte dersi ALMA):
  en büyük tercih puanı 415 · AKTS 30 / 30 · 6 ders: BLM103 BLM104 BLM201 BLM205 ING101 MAT102
    BLM103   Bilgisayar Mühendisliğine Giriş       4 AKTS · puan  55
    BLM104   Ayrık Matematik                       5 AKTS · puan  70
    BLM201   Veri Yapıları                         6 AKTS · puan  95
    BLM205   Nesneye Yönelik Programlama           5 AKTS · puan  85
    ING101   İngilizce I                           4 AKTS · puan  45
    MAT102   Matematik II                          6 AKTS · puan  65
  satır tamponlu DP (yalnız değer, 31 int, 372 hücre): 415 — AYNI
Açgözlü (puan/AKTS oranı azalan, sığanı al — H12): puan 410 · AKTS 29 · BLM103 BLM104 BLM201 BLM205 ING101 MAT203 → en iyiden 5 puan az (EN İYİ DEĞİL)
Kesirli sırt çantası (son ders bölünebilseydi; 0/1 için üst sınır): 420
Geri izleme (v2.2 ağacı, üst sınır budaması): puan 415 · 3238 düğüm (775 budandı) · küme: AYNI
Dal ve sınır (+ kesirli sırt çantası sınırı): puan 415 · 145 düğüm (102 budandı) · küme: AYNI
Kaba kuvvet (bit maskesi, 2^12 = 4096 küme): puan 415 · küme: AYNI
v2.2 secim_yap(YONTEM_UST, AKTS 0..30): 2463 uygun küme · 3238 düğüm (geri izleme 3238, sayım DP'si 3238: AYNI)
Düğüm ↔ hücre: v2.2 ağacı 3238 düğüm (sayım DP'si) ↔ DP 403 hücre
Önkoşul denetimi: seçilen 6 dersin bütün önkoşulları alınmış: EVET (aynı dönemde birbirinin önkoşulu olan dersler kapsam dışı)
```

Öğrenci kaydıyla (`--ogrenci ornek_veri/ogrenciler.csv --no 2301010046`; MEHMET ALİ KAYA'nın yalnız FIZ101'i başarılı):

```
Öğrenci 2301010046 MEHMET ALİ KAYA: BLM101 FF MAT101 DC FIZ101 CB (alınmış)
Katalog: ornek_veri/onkosul.txt · 48 ders · alınan 1 ders · adaylar: şimdi alınabilecek 9 ders (bütün önkoşulları alınmış)
Tercihler: ornek_veri/tercihler_katalog.csv · adayların puan toplamı 440 · AKTS üst sınırı W = 30
…
```

### 4.5 Düzenleme uzaklığı: kod noktası, bayt değil

d(a, b), a'yı b'ye çeviren en az tek karakterlik silme, ekleme ve değiştirme sayısıdır (Levenshtein, 1966). Durum D[i][j] = a'nın ilk i, b'nin ilk j karakteri arasındaki uzaklık; temel durum D[i][0] = i, D[0][j] = j; geçiş D[i][j] = min(D[i−1][j] + 1, D[i][j−1] + 1, D[i−1][j−1] + [aᵢ ≠ bⱼ]) (Wagner ve Fischer, 1974). Satır i yalnız satır i − 1'e bağlıdır: **iki satırlık tampon** yeter (Θ(n) bellek). Öneri için yalnız uzaklık gerektiğinden geri çıkarma (hangi düzenlemeler?) yapılmaz.

![Levenshtein](mini_obs_v2_12_levenshtein.png)

*Şekil 2. "sahın" sorgusu Türkçe katlamayla SAHIN olur. (a) Kod noktası düzeyinde ŞAHİN'e uzaklık 2'dir (S → Ş, I → İ). (b) UTF-8 baytları üzerinde 4'tür: Ş (C5 9E) ve İ (C4 B0) ikişer bayttır; her harf değişikliği bir değiştirme ve bir ekleme olarak sayılır. Renkli hücreler bir en kısa düzenleme yolu.*

**Neden kod noktası?** UTF-8'de Türkçe harfler (ç ğ ı İ ö ş ü) iki bayttır. Bayt düzeyindeki uzaklık bu harflerdeki her yazım hatasını iki kez sayar ve öneri sıralamasını dil yüzünden bozar: 10⁵ kayıtlık örnekte (§ 6) "mehmet yilmas" sorgusuna MEHMET ASLAN, MEHMET POLAT ve MEHMET YALÇIN kod noktası düzeyinde eşit uzaklıktadır (4); bayt düzeyinde ASLAN ve POLAT 5, YALÇIN 6 uzaklıkta kalır — Ç iki bayt olduğu için Türkçe harfli ad listenin sonuna itilir. Sorgu ve terimler önce v2.4'ün `utf8_coz`'uyla kod noktalarına çözülür; kâhin de uzaklığı kod noktalarında, elle çözülmüş bir harf tablosuyla hesaplar.

**Büyük/küçük harf duyarsız.** Sorgu ve terimler v2.9'un Türkçe katlamasından (`tr_katla`) geçer: i → İ, ı → I, â → A; baş/son boşluklar atılır, iç boşluklar teke iner. ASCII klavyeyle yazılan "yilmaz" YİLMAZ olur ve YILMAZ'a uzaklığı 1'dir — öneri tam da bu hatayı yakalar:

```
Sorgu: "sahın" → "SAHIN" (5 kod noktası, 5 bayt)
En yakın 1 terim (kod noktası düzeyinde Levenshtein; eşitlikte Türkçe alfabe sırası):
   1. uzaklık  2 · bayt düzeyinde  4  ŞAHİN                    soyad · 1 kayıt (ilk 2301010052)
Sorgu: "yilmaz" → "YİLMAZ" (6 kod noktası, 7 bayt)
En yakın 3 terim (kod noktası düzeyinde Levenshtein; eşitlikte Türkçe alfabe sırası):
   1. uzaklık  1 · bayt düzeyinde  2  YILMAZ                   soyad · 2 kayıt (ilk 2301010045)
   2. uzaklık  3 · bayt düzeyinde  4  ILGAZ                    ad · 1 kayıt (ilk 2301010052)
   3. uzaklık  4 · bayt düzeyinde  5  İSMAİL                   ad · 1 kayıt (ilk 2301010047)
Budama (aday: uzaklığı hesaplanan terim; hücre: DP hücresi):
  yok            : 23 aday · 0 atlanan · 1068 hücre
  uzunluk farkı  : 19 aday · 4 atlanan · 762 hücre
  uzunluk kovası : 18 aday · 5 atlanan · 672 hücre
Üç yöntem: AYNI (öneriler ve sıraları)
```

### 4.6 Terim sözlüğü ve en yakın k öneri

Menüdeki ad araması (`sinif_isim_bul`, v1.0) bir kaydı **adı, soyadı ya da "AD SOYAD" tam adıyla** bulur. Sözlük de bu üç terimin katlanmış biçimlerinden **farklı** olanlarını tutar: 3N terim bayt sırasıyla sıralanır (`qsort` + `strcmp`), eşitler birleştirilir (kayıt sayısı, tür: ad/soyad/tam ad, en küçük numara), farklı terimler Türkçe alfabe sırasına dizilir (`tr_karsilastir`). 100 000 kayıtta 300 000 terimden farklı olanların sayısı yalnız 1 679: uzaklık her farklı terim için **bir kez** hesaplanır — aynı alt problemi yeniden çözmeme ilkesinin veri düzeyindeki karşılığı.

**En yakın k:** sıralama ölçütü (uzaklık, alfabe sırası); en iyi k, k öğelik sıralı dizide araya ekleyerek tutulur. **Uzunluk farkı budaması:** |len(a) − len(b)| ≤ d(a, b) (her ekleme ya da silme uzunluğu bir değiştirir). Liste dolduktan sonra en kötü önerinin uzaklığı u ise:

- **uzunluk farkı** (`BUDAMA_UZUNLUK`): terimler alfabe sırasıyla taranır; uzunluk farkı ≥ u olan terimin DP'si yapılmaz (uzaklığı u'dan küçük olamaz; u'ya eşitse alfabede sonra geldiği için zaten giremez);
- **uzunluk kovası** (`BUDAMA_KOVA`): terimler uzunluk kovalarındadır (kararlı sayma sıralaması); sorgu uzunluğundan başlayarak Δ = 0, 1, 2, … kovaları taranır, Δ > u olunca durulur. Yakın uzunluktaki iyi adaylar önce bulunur, u hızla küçülür.

Üç yöntem aynı önerileri verir (kâhin, `ara --budama hepsi`):

```
$ ./ara ornek_veri/ogrenciler.csv --oneri 'ilgaz sahin'
Terim sözlüğü: 8 kayıt → 23 farklı terim (ad, soyad ve tam ad; katlanmış, Türkçe alfabe sırası; en uzun 15 kod noktası)
Sorgu: "ilgaz sahin" → "İLGAZ SAHİN" (11 kod noktası, 13 bayt)
En yakın 5 terim (kod noktası düzeyinde Levenshtein; eşitlikte Türkçe alfabe sırası):
   1. uzaklık  2 · bayt düzeyinde  4  ILGAZ ŞAHİN              tam ad · 1 kayıt (ilk 2301010052)
   2. uzaklık  7 · bayt düzeyinde  9  ILGAZ                    ad · 1 kayıt (ilk 2301010052)
   3. uzaklık  7 · bayt düzeyinde  8  ŞAHİN                    soyad · 1 kayıt (ilk 2301010052)
   4. uzaklık  8 · bayt düzeyinde  8  İSMAİL                   ad · 1 kayıt (ilk 2301010047)
   5. uzaklık  9 · bayt düzeyinde 11  CAN                      ad · 1 kayıt (ilk 2301010048)
Budama (aday: uzaklığı hesaplanan terim; hücre: DP hücresi):
  yok            : 23 aday · 0 atlanan · 1958 hücre
  uzunluk farkı  : 23 aday · 0 atlanan · 1958 hücre
  uzunluk kovası : 23 aday · 0 atlanan · 1958 hücre
Üç yöntem: AYNI (öneriler ve sıraları)
```

Menüde (3) Ara) sonuç vermeyen ad aramasından sonra en çok üç öneri, **eşik** m / 3 + 1 düzenleme içindeyse yazılır (m: sorgunun kod noktası sayısı); "ZZZZZZ" gibi uzak sorgularda öneri yazılmaz:

```
$ ./mini_obs ornek_veri/ogrenciler.csv < testler/T7_oneri.txt | grep -E 'Eşleşen|Bunu mu|MEHMET ALİ KAYA'
  Eşleşen kayıt yok: YİLMAS
  Bunu mu demek istediniz? YILMAZ (soyad · 2 kayıt · uzaklık 2)
--------------------------------- ARAMA: MEHMET ALİ KAYA
   2  2301010046  MEHMET ALİ KAYA            46.80 FF   59.20 DC   66.00 CB   1.26
Eşleşen kayıt: 1
  Eşleşen kayıt yok: SULE DOGAN
  Bunu mu demek istediniz? ŞULE DOĞAN (tam ad · 1 kayıt · uzaklık 2)
  Eşleşen kayıt yok: ZZZZZZ
```

### 4.7 Kâhinler

| Sınanan | Kâhin |
|---|---|
| `sirt_cantasi_tablo` (değer, küme, **her hücre**), `sirt_cantasi_deger` | **bütün maskeler**: en büyük puan ve onu veren en küçük maske; ilk i dersin AKTS'si ≤ c olan kümelerinin en büyük puanı (tablonun kendisi) |
| `sirt_cantasi_geri_izleme` (sınırlı/sınırsız), `sirt_cantasi_kaba` | aynı maske; dal-sınır düğümü ≤ geri izleme düğümü |
| `geri_izleme_dugum_hesapla` | v2.2'nin `secim_yap(YONTEM_UST)` ziyaret sayısı = geri izlemenin düğümü = sayım DP'si |
| `sirt_cantasi_acgozlu`, `sirt_cantasi_kesirli` | `qsort`'lu oran sırası (çapraz çarpım, eşitlikte indis) ile ayrı hesap; açgözlü ≤ en iyi ≤ kesirli |
| `levenshtein`, `ad_kod_noktalari` | **naif özyinelemeli** uzaklık (0..5 harf; küçük/büyük, şapkalı, Türkçe İ/ı karışık yazım), harf tablosundan elle çözülmüş büyük harf kod noktalarında; iki yön |
| `ad_sozlugu_kur` | terimler `qsort` + `tr_karsilastir` ile sıralanır ve ayıklanır: aynı terimler, kayıt sayısı, tür ve ilk numara |
| `oneri_bul` (üç budama) | her terim için **tam matrisli** uzaklık, (uzaklık, indis) `qsort`'u, ilk k; aday + atlanan = terim sayısı |

Kâhin örnekleri n = 0..12 ders (AKTS 1..10, puan 0..6 — çok eşitlik — ya da 0..100, W = 0..40) ve 0..30 kayıtlık sınıflardır (adlar ve soyadlar küçük havuzlardan: "CAN" hem ad hem soyad, "ŞAHİN"/"SAHIN" birlikte).

## 5. Bellek sahipliği

| Yapı | Kim ayırır | Kim serbest bırakır | Yaşam süresi |
|---|---|---|---|
| `AdayListesi.a` | `aday_ekle` (× 2, `realloc` geçici işaretçiyle), `aday_uret` | `aday_listesi_birak` | program boyunca |
| DP tablosu (`int *T`, (n+1)(W+1)) | `sirt_cantasi_tablo` (istenirse çağırana verilir) | çağıran (`free`); istenmezse işlev | geri çıkarma ve yazdırma boyunca |
| tek satır, kesirli sıra, tercih geçici dizileri | ilgili işlev | aynı işlev (her çıkış yolunda) | çağrı boyunca |
| `AdSozlugu` (metin, kod noktaları, kayıt, tür, kova …) | `ad_sozlugu_kur` (yarım kalırsa hepsi geri verilir) | `ad_sozlugu_birak` | sorgular boyunca (menüde bir arama) |
| Levenshtein iki satırı | `oneri_bul` (bir kez, en uzun terime göre) | `oneri_bul` | sorgu boyunca |
| `Oneri` dizisi | çağıran (en az k öğe) | çağıran | — |
| önceki sürümlerin yapıları | v2.11 § 5 | v2.11 § 5 | — |

`tercih_oku` biçim hatasında puanları değiştirmez (birim testi altı hatalı girdide denetler); `ad_sozlugu_kur` bellek yetmezse boş sözlük bırakır. `make asan` (yeni programlar, 10⁵ kayıtlık sözlük taban çizgisi, bozuk dosya ve kasıtlı hata kipleri dahil) temiz; `make valgrind` 87 çalıştırmanın hepsinde "ERROR SUMMARY: 0 errors" ve "definitely lost: 0 bytes" (yeni ve test çalıştırmaları):

```
valgrind ./obs_test_vg → çıkış 0 · ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0) · definitely lost: 0 bytes (All heap blocks were freed -- no leaks are possible)
valgrind ./test_kahin_vg --deneme 20 → çıkış 0 · ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0) · definitely lost: 0 bytes (All heap blocks were freed -- no leaks are possible)
valgrind ./test_kahin_vg --deneme 3 --hata-goster sinirsiz → çıkış 1 · ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0) · definitely lost: 0 bytes (All heap blocks were freed -- no leaks are possible)
valgrind ./test_kahin_vg --deneme 3 --hata-goster bayt → çıkış 1 · ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0) · definitely lost: 0 bytes (All heap blocks were freed -- no leaks are possible)
valgrind ./ders_secimi_vg --tablo → çıkış 0 · ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0) · definitely lost: 0 bytes (All heap blocks were freed -- no leaks are possible)
valgrind ./ders_secimi_vg --katalog ornek_veri/onkosul.txt --alinan BLM101,MAT101,FIZ101,BLM102 --akts 30 → çıkış 0 · ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0) · definitely lost: 0 bytes (All heap blocks were freed -- no leaks are possible)
valgrind ./ders_secimi_vg --katalog ornek_veri/onkosul.txt --ogrenci ornek_veri/ogrenciler.csv --no 2301010046 → çıkış 0 · ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0) · definitely lost: 0 bytes (All heap blocks were freed -- no leaks are possible)
valgrind ./ders_secimi_vg --tercih testler/tercih_bozuk.csv → çıkış 1 · ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0) · definitely lost: 0 bytes (All heap blocks were freed -- no leaks are possible)
valgrind ./ara_vg ornek_veri/ogrenciler.csv --oneri ilgaz sahin → çıkış 0 · ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0) · definitely lost: 0 bytes (All heap blocks were freed -- no leaks are possible)
valgrind ./mini_obs_vg ornek_veri/ogrenciler.csv → çıkış 0 · ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0) · definitely lost: 0 bytes (All heap blocks were freed -- no leaks are possible)
valgrind ./olcer_dp_vg dp --n 0,12 --akts 30 --tekrar 1 → çıkış 0 · ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0) · definitely lost: 0 bytes (All heap blocks were freed -- no leaks are possible)
valgrind ./olcer_dp_vg geri --n 12 --akts 30 --tekrar 1 → çıkış 0 · ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0) · definitely lost: 0 bytes (All heap blocks were freed -- no leaks are possible)
valgrind ./olcer_dp_vg dal --n 12 --akts 30 --tekrar 1 → çıkış 0 · ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0) · definitely lost: 0 bytes (All heap blocks were freed -- no leaks are possible)
valgrind ./olcer_dp_vg sozluk --n 300 --tekrar 1 → çıkış 0 · ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0) · definitely lost: 0 bytes (All heap blocks were freed -- no leaks are possible)
valgrind ./olcer_dp_vg oneri_kova --n 1,500 --sorgu 10 --tekrar 1 → çıkış 0 · ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0) · definitely lost: 0 bytes (All heap blocks were freed -- no leaks are possible)
valgrind ./olcer_dp_vg oneri_kayit --n 300 --sorgu 5 --tekrar 1 → çıkış 0 · ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0) · definitely lost: 0 bytes (All heap blocks were freed -- no leaks are possible)
valgrind ./mini_obs_vg oturum.csv → çıkış 0 · ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0) · definitely lost: 0 bytes (All heap blocks were freed -- no leaks are possible)
```

## 6. Kullanım

```
./ders_secimi [--akts W] [--havuz dosya.csv] [--tercih dosya] [--yontem dp|geri|dal|kaba|hepsi] [--tablo]
./ders_secimi --katalog onkosul.txt (--alinan KOD[,KOD…] | --ogrenci dosya --no N) [--tercih dosya] [--akts W]
./ara dosya.csv --oneri SORGU [--k K] [--budama yok|uzunluk|kova|hepsi]
./olcer_dp İŞLEM [--n N1,N2,…] [--akts W] [--tekrar T] [--tohum S] [--butce SN] [--sorgu Q] [--k K]
           [--csv dosya.csv [--ekle]]      İŞLEM: dp satir geri dal kaba sozluk oneri_kayit oneri_yok
                                                  oneri_uzunluk oneri_kova
```

Tercih dosyası `kod;puan` satırlarıdır (ilk veri satırı `kod;puan` başlığı olabilir; `#` yorum); puan 0..1000, listede olup dosyada olmayan dersin puanı 0. Varsayılanlar: havuz `ornek_veri/secmeli_dersler.csv` (v2.2), tercih `ornek_veri/tercihler.csv` (katalog kipinde `ornek_veri/tercihler_katalog.csv`), W = 20. 10⁵ kayıtlık üretilmiş dosyada (`veri_uret`):

```
$ ./veri_uret --n 100000 --tohum 42 --cikti b.csv; ./ara b.csv --oneri 'mehmet yilmas' --k 5
Dosya: b.csv · kayıt: 100000 (numaraya göre sıralı: EVET)
Süre: yükleme 138.541 ms
Terim sözlüğü: 100000 kayıt → 1679 farklı terim (ad, soyad ve tam ad; katlanmış, Türkçe alfabe sırası; en uzun 19 kod noktası)
Sorgu: "mehmet yilmas" → "MEHMET YİLMAS" (13 kod noktası, 14 bayt)
En yakın 5 terim (kod noktası düzeyinde Levenshtein; eşitlikte Türkçe alfabe sırası):
   1. uzaklık  2 · bayt düzeyinde  3  MEHMET YILMAZ            tam ad · 67 kayıt (ilk 2400000932)
   2. uzaklık  4 · bayt düzeyinde  5  AHMET YILMAZ             tam ad · 54 kayıt (ilk 2400001950)
   3. uzaklık  4 · bayt düzeyinde  5  MEHMET ASLAN             tam ad · 57 kayıt (ilk 2400003087)
   4. uzaklık  4 · bayt düzeyinde  5  MEHMET POLAT             tam ad · 59 kayıt (ilk 2400000514)
   5. uzaklık  4 · bayt düzeyinde  6  MEHMET YALÇIN            tam ad · 46 kayıt (ilk 2400000128)
Budama (aday: uzaklığı hesaplanan terim; hücre: DP hücresi):
  yok            : 1679 aday · 0 atlanan · 237692 hücre
  uzunluk farkı  : 1518 aday · 161 atlanan · 222872 hücre
  uzunluk kovası : 1521 aday · 158 atlanan · 223743 hücre
Üç yöntem: AYNI (öneriler ve sıraları)
Süre: sözlük 170.079 ms · yok 0.301 ms · uzunluk farkı 0.308 ms · uzunluk kovası 0.267 ms
```

Hatalar:

```
$ ./ders_secimi --tercih testler/tercih_bozuk.csv; ./ders_secimi --katalog … --alinan XYZ; ./ders_secimi --akts 1001; ./ders_secimi --havuz yok.csv
Havuz: ornek_veri/secmeli_dersler.csv · 14 ders · AKTS toplamı 63
Hata: testler/tercih_bozuk.csv okunamadı: dosya biçimi hatalı (satır 4: adaylarda olmayan ders: BIL999)
Hata: bilinmeyen ders kodu: XYZ
Kullanım: ./ders_secimi [--akts W] [--havuz dosya.csv] [--tercih dosya] [--yontem dp|geri|dal|kaba|hepsi] [--tablo]
          ./ders_secimi --katalog onkosul.txt (--alinan KOD[,KOD...] | --ogrenci dosya --no N) [--tercih dosya] [--akts W] [--yontem ...] [--tablo]
Kullanım: ./ders_secimi [--akts W] [--havuz dosya.csv] [--tercih dosya] [--yontem dp|geri|dal|kaba|hepsi] [--tablo]
          ./ders_secimi --katalog onkosul.txt (--alinan KOD[,KOD...] | --ogrenci dosya --no N) [--tercih dosya] [--akts W] [--yontem ...] [--tablo]
Hata: yok.csv okunamadı: dosya açılamadı
[çıkış kodu: 1]
```

```
$ ./ara ornek_veri/ogrenciler.csv --oneri '  '; ./ara ornek_veri/ogrenciler.csv --oneri x --k 17; ./ara ornek_veri/ogrenciler.csv --no 5 --k 3
Dosya: ornek_veri/ogrenciler.csv · kayıt: 8 (numaraya göre sıralı: EVET)
Süre: yükleme 0.084 ms
Hata: sorgu boş ya da çok uzun (en çok 128 kod noktası)
Kullanım: ./ara dosya.csv|dosya.dat (--no N | --soyad ÖNEK | --icinde DESEN | --oneri SORGU) [--dogrusal] [--izle] [--karma [--tohum T]] [--yontem naif|rk|strstr|hepsi] [--q Q] [--goster K] [--k K] [--budama yok|uzunluk|kova|hepsi]
Kullanım: ./ara dosya.csv|dosya.dat (--no N | --soyad ÖNEK | --icinde DESEN | --oneri SORGU) [--dogrusal] [--izle] [--karma [--tohum T]] [--yontem naif|rk|strstr|hepsi] [--q Q] [--goster K] [--k K] [--budama yok|uzunluk|kova|hepsi]
[çıkış kodu: 2]
```

## 7. Tasarım kararları

1. **Tam tablo + tek satır, ikisi birden.** Küme isteyen kullanıcı tam tabloyu (Θ(n·W) bellek), yalnız değer isteyen (ölçüm, sağlama) tek satırı (Θ(W)) kullanır; program ikisinin değerini karşılaştırır. W ≤ 1000 ve n küçük olduğu için tablo en çok birkaç MiB'tır (§ 8.2).
2. **Eşitlikte ALMA.** Kural geri çıkarmada tek karşılaştırmayla uygulanır ve "en küçük maske" olarak bütün yöntemlerde aynı tanımlanabilir; böylece dört strateji **küme düzeyinde** karşılaştırılır, yalnız değer düzeyinde değil.
3. **v2.2'nin ağacı aynen.** Geri izleme v2.2 ile aynı sıra ve budamayı kullanır ki düğüm sayıları karşılaştırılabilsin; `ders_secimi` v2.2'nin kendi `secim_yap`'ını da çağırır.
4. **Çalıştırmadan say, sonra kestir.** Bütçeyi aşacak geri izleme çalıştırılmaz: düğüm sayısı sayım DP'siyle kesin hesaplanır, süre düğüm başına süreyle kestirilir ve CSV'de işaretlenir (kestirim = 1).
5. **Kod noktası düzeyinde uzaklık, katlanmış metinde.** Bayt düzeyi Türkçe harfleri iki kez sayar; katlama (v2.9) büyük/küçük harf ve şapka farkını uzaklıktan çıkarır.
6. **Kayıtlar değil terimler.** Önerilen, menüde aranabilecek bir dizgidir (ad, soyad ya da tam ad); aynı terimi taşıyan kayıtlar tek öneride sayılır. Sözlük her menü aramasında yeniden kurulur (Θ(N log N); menü boyutlarında anlıktır, 100 000 kayıtta 184,7 ms).
7. **Uzunluk budaması güvenli, eşik yalnız menüde.** Budama önerileri değiştirmez (kanıt § 4.6, kâhin); menünün eşiği (m / 3 + 1) ise bir kullanılabilirlik kararıdır: uzak öneriler gürültüdür.

## 8. Ölçümler

**Düzen:** `-O2`; her nokta için önce sayaç açık bir çalıştırma (puan, hücre, düğüm, budanan, aday, atlanan, kontrol toplamı), sonra 1 ısınma + 5 tekrar (geri izleme, kaba kuvvet ve sözlüksüz taban çizgisinde 3), ortanca; veri hazırlama süre dışında. Sırt çantası: n aday (AKTS 2..8, puan 1..100, ortak LCG, tohum 42 — her n'nin ilk dersleri aynı), W = 15, 30, 45. Öneri: `uretec_sinif` ile 10³…10⁵ kayıt, 50 sorgu (sözlükten rastgele bir terime 1–3 rastgele düzenleme), k = 5; 10⁵ kayıtta 100 sorgu ve k = 1, 5, 16. Makine: Intel(R) Xeon(R) Processor @ 2.80GHz, 2 çekirdek (sanal makine), L2 2 MiB, L3 33 MiB; gcc 13.3.0, glibc 2.39; tarih 2026-10-22 09:17. `make olcum` 38 s sürdü; süreç belleğinin tepesi 41 MiB (DP, n = 10⁴, W = 1 000) ve 32 MiB (sözlüksüz öneri, 10⁵ kayıt). Ölçüm sırasında makinenin 1 dakikalık yük ortalaması başta 0,49, sonda 0,91 idi (2 çekirdek; aynı anda başka ajanların derleme ve ölçümleri çalışıyordu). Aynı programın ardışık çalıştırmaları arasında bile süre iki kata varan sıçramalar gösterebiliyor (süreç, yükü paylaşılan bir sanal çekirdeğe düştüğünde): süreleri gürültülü, hücre, düğüm, aday ve atlanan sayaçlarını kesin kabul edin; tablolarda ortancanın yanında en kısa tekrar da verilmiştir.

![Ölçümler](mini_obs_v2_12_olcum.png)

*Şekil 3. Sol üst: W = 30'da süre ↔ aday sayısı (log; kesikli çizgi ve boş işaret: kestirim). Sağ üst: geri izlemenin düğüm sayısı ↔ DP'nin hücre sayısı (W = 15, 30, 45). Sol alt: DP süresi ↔ tablo hücresi (log–log; noktalı çizgi eğim 1). Sağ alt: öneri sorgusu başına süre ↔ kayıt sayısı.*

### 8.1 Strateji turnuvası

| n | en iyi puan | açgözlü | kesirli sınır | DP hücre | DP (tablo) | DP (tek satır) | dal-sınır düğüm | dal-sınır | geri izleme düğüm | geri izleme | kaba kuvvet |
|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| 10 | 411 | 411 | 411 | 341 | 321 ns | 235 ns | 83 | 755 ns | 896 | 4,1 µs | 37,9 µs |
| 15 | 507 | 507 | 515 | 496 | 513 ns | 276 ns | 393 | 3,5 µs | 12 221 | 37,1 µs | 1,6 ms |
| 20 | 597 | 597 | 597 | 651 | 654 ns | 431 ns | 684 | 10,7 µs | 117 690 | 393,3 µs | 69,1 ms |
| 25 | 597 | 597 | 597 | 806 | 787 ns | 808 ns | 1 163 | 10,3 µs | 576 623 | 1,7 ms | 2,24 s |
| 30 | 643 | 643 | 643 | 961 | 937 ns | 1,0 µs | 1 911 | 19,1 µs | 1 835 786 | 5,8 ms | — |
| 35 | 643 | 643 | 643 | 1 116 | 1,1 µs | 631 ns | 2 629 | 25,2 µs | 5 771 021 | 17,6 ms | — |
| 40 | 687 | 673 (−14) | 687 | 1 271 | 1,2 µs | 715 ns | 4 040 | 46,0 µs | 16 627 024 | 50,3 ms | — |
| 50 | 707 | 707 | 709 | 1 581 | 1,5 µs | 887 ns | 5 875 | 62,4 µs | 147 198 469 | 448,5 ms | — |
| 60 | 782 | 782 | 799 | 1 891 | 1,8 µs | 1,1 µs | 8 912 | 97,0 µs | 663 099 430 | 2,02 s * | — |

*Tablo 1. W = 30 (`olcum/sirt.csv`). "açgözlü": oran sırasıyla bulunan puan (en iyiden farkı); "kesirli sınır": son ders bölünebilseydi. Yıldızlı süre **kestirimdir**: (T + 2) çalıştırma 6 s'lik bütçeyi aşacağı için geri izleme çalıştırılmadı; düğüm sayısı sayım DP'siyle kesin hesaplandı, süre aynı serideki son ölçümün düğüm başına süresiyle çarpıldı. Her noktada DP, tek satır, dal-sınır ve (ölçülen) geri izleme aynı puanı verdi; kaba kuvvet n ≤ 25.*

| n | W = 15: DP hücre | geri düğüm | geri süre | dal düğüm | W = 45: DP hücre | geri düğüm | geri süre | dal düğüm |
|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| 10 | 176 | 281 | 2,3 µs | 85 | 506 | 1 024 | 3,6 µs | 138 |
| 15 | 256 | 1 436 | 10,7 µs | 221 | 736 | 27 764 | 91,4 µs | 397 |
| 20 | 336 | 5 944 | 43,0 µs | 490 | 966 | 530 747 | 1,9 ms | 1 517 |
| 25 | 416 | 15 578 | 105,9 µs | 760 | 1 196 | 4 995 162 | 16,3 ms | 3 011 |
| 30 | 496 | 30 501 | 205,4 µs | 945 | 1 426 | 27 868 677 | 93,1 ms | 2 139 |
| 35 | 576 | 58 722 | 515,4 µs | 1 245 | 1 656 | 143 107 092 | 651,9 ms | 3 277 |
| 40 | 656 | 107 679 | 567,4 µs | 1 732 | 1 886 | 635 957 085 | 2,90 s * | 6 381 |
| 50 | 816 | 398 362 | 2,1 ms | 2 603 | 2 346 | 11 914 883 476 | 54,28 s * | 9 805 |
| 60 | 976 | 997 602 | 6,0 ms | 3 582 | 2 806 | 94 586 511 134 | 430,86 s * | 16 244 |

*Tablo 2. W = 15 ve W = 45: DP hücresi, geri izleme düğümü ve süresi, dal-sınır düğümü.*

**Yorum.**

- **Üstel ↔ sözde polinom.** n her 5 arttığında geri izlemenin düğüm sayısı W = 15'te 1,8–5,1, W = 30'da 2,9–13,6, W = 45'te 4,4–27,1 kat büyür; DP'nin hücresi (n+1)(W+1) ile doğrusal artar. W büyüdükçe uygun küme sayısı artar ve ağaç genişler: n = 60'ta düğüm sayısı W = 15'te 997 602, W = 45'te 94 586 511 134 (sayım DP'si). W = 45, n = 35'te geri izleme DP'den 413 371 kat yavaştır; n = 60'ta ≈ 7 dakika sürerdi (kestirim; ölçülen düğüm başına süre 2,9–6,0 ns).
- **Dal ve sınır** aynı ağacı kesirli sırt çantası sınırıyla budar: n = 60, W = 45'te 16 244 düğüm (300,0 µs) — geri izlemenin düğüm sayısından 5 822 858 kat az. Kötü durumda yine üsteldir (sınır zayıfsa budama olmaz); DP'nin süresi ise girdiye değil yalnız n·W'ye bağlıdır.
- **Kaba kuvvet** n = 25'te 2,24 s sürer (2²⁵ maske × 25 bit); n = 40'ta 2¹⁵ kat, yani ≈ 33 saat sürerdi (kestirim: maske başına süre sabit, bit sayısıyla doğrusal varsayıldı; ölçülmedi).
- **Açgözlü** 27 noktadan 9 tanesinde en iyiden az bulur (en çok 27 puan, en kötü oran 0,948); kesirli sınırla en iyi arasındaki fark ise dal-sınırın ne kadar budayabileceğini gösterir.
- **Süreler.** Küçük tabloda DP 1 µs'nin altındadır ve ölçüm zamanlayıcının çözünürlüğüne yakındır; büyüme sınıfları sayaçlarla (hücre, düğüm) kesin olarak görülür.

### 8.2 DP: sözde polinom süre ve tablo belleği

| n | W | hücre (n+1)(W+1) | tablo (MiB) | DP (tablo) | ns / hücre | DP (tek satır) | ns / hücre |
|--:|--:|--:|--:|--:|--:|--:|--:|
| 40 | 100 | 4 141 | 0,02 | 6,4 µs | 1,55 | 2,8 µs | 0,69 |
| 100 | 100 | 10 201 | 0,04 | 9,6 µs | 0,94 | 8,6 µs | 0,85 |
| 1 000 | 100 | 101 101 | 0,39 | 100,8 µs | 1,00 | 68,5 µs | 0,68 |
| 10 000 | 100 | 1 010 101 | 3,85 | 1,1 ms | 1,10 | 701,3 µs | 0,69 |
| 40 | 1 000 | 41 041 | 0,16 | 32,6 µs | 0,80 | 20,4 µs | 0,51 |
| 100 | 1 000 | 101 101 | 0,39 | 91,9 µs | 0,91 | 52,3 µs | 0,52 |
| 1 000 | 1 000 | 1 002 001 | 3,82 | 1,0 ms | 1,03 | 683,5 µs | 0,68 |
| 10 000 | 1 000 | 10 011 001 | 38,19 | 30,1 ms | 3,01 | 6,5 ms | 0,64 |

*Tablo 3. Büyük n ve W'de DP (`olcum/dp_buyuk.csv`; n > 64'te geri izleme ve açgözlü yoktur). Tablo belleği 4(n+1)(W+1) bayt.*

Süre hücre sayısıyla doğrusaldır (Şekil 3, sol alt). 10 011 001 hücrede tam tablo 30,1 ms (3,01 ns/hücre), tek satır 6,5 ms (0,64 ns/hücre) sürer: tek satır W + 1 = 1 001 int'lik (≈ 4 KiB) bir diziyi L1 önbellekte günceller, tam tablo ise 38 MiB'lık yeni belleğe yazar (ilk dokunuşta sayfa hatası ve ana bellek bant genişliği). 10⁶ hücrede (1 002 001) hücre başına süre 1,03 ns'dir. Bellek–zaman ödünleşimi (Mühendis Gözüyle): küme isteniyorsa tablo zorunludur; yalnız değer isteniyorsa tek satır hem az bellek kullanır hem hızlıdır. (Hirschberg'in böl-ve-fethet yöntemi kümeyi de Θ(W) bellekle çıkarır — kapsam dışı.)

### 8.3 Öneri: sözlük ve budama

| kayıt | farklı terim | sözlük kurma | sözlüksüz (her kayıt) | sözlük, budamasız | + uzunluk farkı | + uzunluk kovası |
|--:|--:|--:|--:|--:|--:|--:|
| 1 000 | 821 | 1,6 ms | 366,5 µs (355,2 µs) | 132,8 µs (127,7 µs) | 104,4 µs (102,0 µs) | 98,5 µs (98,0 µs) |
| 10 000 | 1 678 | 15,8 ms | 3,8 ms (3,5 ms) | 279,9 µs (265,1 µs) | 280,9 µs (224,4 µs) | 250,9 µs (237,3 µs) |
| 100 000 | 1 679 | 184,7 ms | 38,1 ms (35,7 ms) | 272,1 µs (267,4 µs) | 379,5 µs (307,5 µs) | 236,5 µs (223,3 µs) |

*Tablo 4. Sorgu başına süre, ortanca (en kısa tekrar) (`olcum/oneri.csv`; 50 sorgu, k = 5). Dört yöntemin önerileri her kayıt sayısında aynıdır (kontrol toplamı eşit).*

| kayıt | sözlüksüz: aday | hücre | budamasız: aday | hücre | uzunluk farkı: aday | hücre | kova: aday | hücre |
|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| 1 000 | 3 000 | 228 334 | 821 | 93 217 | 623 | 77 643 | 635 | 79 261 |
| 10 000 | 30 000 | 2 337 419 | 1 678 | 199 928 | 1 343 | 171 147 | 1 405 | 178 229 |
| 100 000 | 300 000 | 23 446 494 | 1 679 | 200 758 | 1 395 | 175 023 | 1 447 | 180 103 |

*Tablo 5. Sorgu başına DP sayısı (aday) ve DP hücresi (sayaç; kesin).*

- **Sözlük (aynı alt problemi bir kez çözmek).** 100 000 kayıtta sözlüksüz yöntem sorgu başına 300 000 DP yapar, sözlük 1 679: aday 179 kat, hücre 117 kat azalır; süre 38,1 ms → 272,1 µs (140 kat). Kayıt sayısı 10³ → 10⁵ olunca sözlüksüz sorgu süresi 104 kat büyür (Θ(N)), sözlüklü sorgu yalnız 2,0 kat: üreteçte 40 ad × 40 soyad olduğu için farklı terim sayısı 821 → 1 679 olup doyar. Sözlüğü kurmak (bir kez) 184,7 ms sürer — 679 sorgu kadar.
- **Uzunluk budaması** k = 5'te DP sayısını uzunluk farkıyla %17, kovalarla %14; hücre sayısını %13 ve %10 azaltır. Kazanç sınırlıdır, çünkü sözlüğün 1 679 teriminin 1 600'ü birbirine yakın uzunlukta tam adlardır (üreteç: 40 ad × 40 soyad; "CAN" hem ad hem soyad) ve k = 5'in en kötü uzaklığı birkaç düzenlemedir. Bu farklar ölçüm gürültüsü düzeyindedir (Tablo 4'te ortanca ile en kısa tekrar arasındaki fark); kazancı sayaçlardan okuyun.

### 8.4 Budamanın k'ye bağlılığı

| k | yöntem | aday (100 sorgu) | atlanan | hücre | hücre / budamasız | süre (ortanca) | süre (en kısa) |
|--:|---|--:|--:|--:|--:|--:|--:|
| 1 | budamasız | 167 900 | %0,0 | 19 947 844 | %100 | 26,2 ms | 25,9 ms |
| 1 | uzunluk farkı | 99 778 | %40,6 | 12 708 354 | %64 | 18,0 ms | 16,8 ms |
| 1 | uzunluk kovası | 91 411 | %45,6 | 11 515 319 | %58 | 14,8 ms | 14,5 ms |
| 5 | budamasız | 167 900 | %0,0 | 19 947 844 | %100 | 27,3 ms | 26,6 ms |
| 5 | uzunluk farkı | 138 038 | %17,8 | 17 362 908 | %87 | 24,8 ms | 23,1 ms |
| 5 | uzunluk kovası | 141 427 | %15,8 | 17 664 723 | %89 | 22,6 ms | 22,0 ms |
| 16 | budamasız | 167 900 | %0,0 | 19 947 844 | %100 | 25,9 ms | 25,8 ms |
| 16 | uzunluk farkı | 146 978 | %12,5 | 18 276 796 | %92 | 25,3 ms | 24,2 ms |
| 16 | uzunluk kovası | 147 624 | %12,1 | 18 344 929 | %92 | 25,1 ms | 23,8 ms |

*Tablo 6. 100 000 kayıt, 100 sorgu (`olcum/oneri_k.csv`). Üç yöntemin önerileri her k'de aynı.*

k küçüldükçe en kötü önerinin uzaklığı küçülür ve budama güçlenir: uzunluk kovasının hesapladığı hücrelerin budamasız yönteme oranı k = 1'de %58 (en kısa tekrarların oranı 0,56), k = 16'da %92. Menü 3 öneri ister; daha güçlü bir budama, satırın en küçük değeri u'yu aşınca DP'yi erken bitirmektir (meydan okuma, § 10).

### 8.5 Sınırlılıklar

Süreler paylaşılan bir sanal makinede ölçüldü ve süreçten sürece iki kata varan sıçramalar gösterdi; hücre, düğüm, aday ve atlanan sayaçları makineden bağımsızdır. Geri izlemenin bütçeyi aşan noktaları ve kaba kuvvetin n = 40 süresi kestirimdir. Sentetik adlar 40 × 40 kombinasyondan gelir; gerçek bir öğrenci listesinde farklı terim sayısı daha büyük olur ve sözlüğün kazancı (aday oranı) azalır, budamanın kazancı ise terim uzunluklarının dağılımına bağlıdır. Tercih puanları KURGUSALDIR.

## 9. Testler

- **Birim testleri** (`obs_test`): `439 doğrulama: 37 kural + 22 metin + 24 yapı + 16 dosya + 11 üreteç + 11 sayaç + 13 yinelenen + 16 seçmeli + 27 arama + 26 sıralama + 23 böl-fethet + 19 öbek-doğrusal + 79 bağlı liste + 29 yığın-kuyruk + 36 karma-desen + 25 graf-önkoşul + 12 sınav + 13 seçim-öneri`. Seçim-öneri testleri: ders kitabı sırt çantası örneği ((1, 1), (3, 4), (4, 5), (5, 7), W = 7 → 9) ve tablo hücreleri; açgözlü 8 ve kesirli 9; eşitlik kuralı (iki özdeş ders → ilk ders; (3, 10) ve (2, 10), W = 3 → ilk ders) — dört yöntem aynı maske; W = 0, sığmayan ders, n = 0; 64'ten çok ders, sayım taşması (UINT64_MAX); üreteç; tercih dosyası (başlık, yorum, eksik ders 0) ve altı biçim hatası; örnek havuz W = 20: 315, açgözlü 295, kesirli 325, v2.2 düğümü = sayım DP'si = 3 264; Levenshtein örnekleri (KITTEN/SITTING 3; ŞAHİN/SAHIN kod noktası 2, bayt 4; İ/I 1, bayt 2); katlama (boşluk, şapka, sınırlar); sözlük (8 kayıt → 23 terim, Türkçe sıra, YILMAZ 2 kayıt); üç budama aynı öneri ve atlanan sayıları; ad = soyad ("CAN CAN"); boş sınıf.
- **Kâhin testleri** (`test_kahin`): 300 denemede 686 464, 1 000 denemede 2 301 138 denetim (sırt çantası, Levenshtein, öneri: 26 000), uyuşmazlık yok.
- **Kasıtlı hatalar.** (a) `--hata-goster sinirsiz` — tek satırlı DP'de kapasite ARTAN gezilir (Hata Avcısı). Kâhin değer farkını yakalar; 1..2 dersli bütün küçük girdiler denenerek en küçük karşı örnek basılır (1 ders, AKTS 1, puan 1, W = 2: ders iki kez alınır):

```
$ ./test_kahin --hata-goster sinirsiz
KÂHİN UYUŞMAZLIĞI (tohum 1)
  İşlev      : sirt_cantasi_tablo / sirt_cantasi_deger
  n          : 3
  Beklenen   : puan 136, maske 0x5 (bütün maskeler)
  Bulunan    : tablo: puan 136, maske 0x5; satır: puan 138
  En küçük karşı örnek (1 ders, W = 2): (AKTS 1, puan 1)
    sirt_cantasi_tablo / sirt_cantasi_deger: beklenen puan 1, maske 0x1 (bütün maskeler); bulunan tablo: puan 1, maske 0x1; satır: puan 2
  Yeniden üretmek için: ./test_kahin --tohum 1 --deneme 1 --hata-goster sinirsiz
[çıkış kodu: 1]
```

  (b) `--hata-goster bayt` — uzaklık UTF-8 baytları üzerinde; en küçük karşı örnek boş dizgi ile "Ş":

```
$ ./test_kahin --hata-goster bayt
KÂHİN UYUŞMAZLIĞI (tohum 1)
  İşlev      : levenshtein (kod noktası)
  n          : 8
  Beklenen   : d("sççA", "ÂÂÇş") = 3 (naif özyineleme)
  Bulunan    : 5 (ters yönde 5)
  En küçük karşı örnek: "" ↔ "Ş"
    levenshtein (kod noktası): beklenen d("", "Ş") = 1 (naif özyineleme); bulunan 2 (ters yönde 2)
  Yeniden üretmek için: ./test_kahin --tohum 1 --deneme 1 --hata-goster bayt
[çıkış kodu: 1]
```

## 10. Ders notu için özet (Hafta 13 · Mini-OBS 2 adımı)

**Bu hafta:** Mini-OBS'ye iki dinamik programlama yeteneği ekliyoruz. **Ders seçimi:** AKTS üst sınırı altında tercih puanını en büyük yapan ders kümesini **0/1 sırt çantası** tablosuyla buluyor, seçilen dersleri tablodan **geri çıkarıyor**, eşitlikte belirleyici bir kural uyguluyoruz; aynı problemi v2.2'nin geri izlemesi, dal ve sınır, açgözlü (yanlış) ve kaba kuvvetle çözüp **düğüm ↔ hücre** ve süreleri karşılaştırıyoruz. **"Bunu mu demek istediniz?":** ad araması sonuç vermezse **düzenleme (Levenshtein) uzaklığı** en küçük adları öneriyoruz — Türkçe büyük/küçük harf duyarsız ve **kod noktası** düzeyinde; aday sayısını **uzunluk farkı** budamasıyla azaltıyoruz.

### Gereksinimler

- `secim.h/.c`: aday listesi ve tercih dosyası (`kod;puan`; hatada satır numarası, çıkış 1); tam tablo DP + geri çıkarma (eşitlikte ALMA); tek satırlı DP (c azalan); v2.2 ağacında geri izleme (en iyiyi tutan); dal ve sınır (kesirli sırt çantası sınırı); açgözlü (oran sırası); kaba kuvvet (n ≤ 25).
- `ders_secimi`: havuz kipi (v2.2 havuzu + tercihler) ve katalog kipi (v2.10'un alınabilir dersleri; önkoşul denetimi); `--tablo` ile tablo ve geri çıkarma izi; yöntemlerin kümelerinin karşılaştırması; v2.2 düğüm sayısıyla kıyas.
- `oneri.h/.c`: kod noktası düzeyinde Levenshtein (iki satır); Türkçe katlama (v2.9) + `utf8_coz`; ad, soyad ve tam ad terimlerinin sözlüğü (Türkçe sıra); en yakın k (eşitlikte alfabe sırası); uzunluk farkı budaması.
- Menü: sonuç vermeyen ad aramasından sonra en çok üç öneri (eşikli); `ara --oneri`.
- Testler: DP ↔ bütün maskeler (değer, küme, tablo); v2.2 düğümü ↔ geri izleme; Levenshtein ↔ naif özyineleme; öneri ↔ bütün terimlerle tam hesap.
- Ölçüm: n = 10…40, en az iki W için DP, geri izleme (bütçeyi aşanlar kestirim), kaba kuvvet (n ≤ 25); 10⁵ kayıtta öneri sorgusu süresi ve budamanın etkisi.

### İpuçları

- Tabloyu tek blokta tutun: `T[i * (W + 1) + c]` (`malloc((n + 1) * (W + 1) * sizeof *T)`); her satır yalnız bir öncekine bakar.
- Geri çıkarmada "T[i][c] == T[i−1][c] ise ALMA" eşitlik kuralını belirler; kuralı yazın ve kaba kuvvette "maske artan, kesin büyükse güncelle" ile aynı kümeyi verdiğini test edin.
- Tek satırlı DP'de c'yi **W'den aşağı** gezin; `--hata-goster sinirsiz`'in karşı örneğini (1 ders, AKTS 1, puan 1, W = 2) elle izleyin.
- Geri izlemenin düğüm sayısını tahmin etmek için çalıştırmayın: "en büyük indisi i, toplamı x olan küme sayısı" DP'si sayıyı kesin verir; büyük n'de süreyi düğüm başına süreyle kestirin ve **kestirim** diye işaretleyin.
- Levenshtein'i UTF-8 baytlarında değil, `utf8_coz` ile çözülmüş kod noktalarında hesaplayın; "ŞAHİN"/"SAHIN" ile sınayın (2, bayt düzeyinde 4).
- Büyük/küçük harf için `toupper` kullanmayın: Türkçe i/İ ve ı/I kuralını v2.9'un `tr_katla`'sı uygular.
- Aynı adı taşıyan kayıtlar için DP'yi tekrarlamayın: önce farklı terimleri ayıklayın (sözlük).
- Uzunluk budamasında "≥ u" mu "> u" mu olacağını eşitlik kuralından çıkarın: alfabe sırasıyla taranıyorsa eşit uzaklıktaki sonraki terim zaten giremez.

### Kabul ölçütleri (denetlenebilir)

1. `make` ve `make test` sıfır uyarıyla derlenir; v1.0'ın 99 doğrulaması ve önceki sürümlerin testleri dahil bütün birim testleri (439) ve `test_kahin` (300 deneme) geçer.
2. `./ders_secimi` şunları basar: `en büyük tercih puanı 315 · AKTS 20 / 20 · 5 ders: BIL331 BIL341 BIL345 BIL355 BIL357`, `satır tamponlu DP … 315 — AYNI`, açgözlü için `puan 295 … EN İYİ DEĞİL`, geri izleme, dal-sınır ve kaba kuvvet için `küme: AYNI`, v2.2 için `3264 düğüm (geri izleme 3264, sayım DP'si 3264: AYNI)`.
3. `./ders_secimi --tablo` geri çıkarma izinde `BIL351 … (EŞİTLİK) → ALINMADI` satırı vardır.
4. `./ders_secimi --katalog ornek_veri/onkosul.txt --alinan BLM101,MAT101,FIZ101,BLM102 --akts 30` 12 aday, 415 puan ve `Önkoşul denetimi: … EVET` basar.
5. `./ara ornek_veri/ogrenciler.csv --oneri 'ilgaz sahin'` ilk öneri olarak `uzaklık  2 · bayt düzeyinde  4  ILGAZ ŞAHİN` ve `Üç yöntem: AYNI` basar; menüde "yilmas" araması `Bunu mu demek istediniz? YILMAZ (soyad · 2 kayıt · uzaklık 2)` satırını üretir.
6. `./test_kahin --hata-goster sinirsiz` ve `--hata-goster bayt` uyuşmazlık ve en küçük karşı örnek basar, 1 ile çıkar; `make asan` ve `make valgrind` temizdir.
7. Ölçüm raporunda: n = 10…40 ve en az iki W için DP hücresi ve süresi, geri izleme düğümü ve süresi (kestirimler işaretli), kaba kuvvet n ≤ 25; 10⁵ kayıtta öneri sorgusu süresi; budamasız ↔ budamalı aday sayısı ve yorumu.

### Test senaryoları

| # | Girdi | Beklenen çıktı / davranış |
|---|---|---|
| 1 | (AKTS, puan) = (1, 1), (3, 4), (4, 5), (5, 7); W = 7 | 9 puan: 2. ve 3. ders; açgözlü 8; kesirli 9 |
| 2 | iki özdeş ders (2, 5); W = 2 | 5 puan, ilk ders (eşitlikte en küçük maske) |
| 3 | (3, 10), (2, 10); W = 3 / W = 5 | ilk ders / iki ders, 20 puan |
| 4 | W = 0 ya da n = 0 | boş küme, 0 puan |
| 5 | tek satırlı DP, 1 ders (1, 1), W = 2 | 1 (c artan gezilirse 2 — hata) |
| 6 | örnek havuz, W = 20 | 315; BIL351'de eşitlik → ALMA; açgözlü 295; v2.2 düğümü 3 264 |
| 7 | katalog, `--alinan BLM101,MAT101,FIZ101,BLM102`, W = 30 | 12 aday, 415 puan, önkoşul denetimi EVET |
| 8 | d("KITTEN", "SITTING"), d("", "ABC") | 3, 3 |
| 9 | d("ŞAHİN", "SAHIN") | 2 (kod noktası), 4 (bayt) |
| 10 | "  ismail   öztürk " katlama | "İSMAİL ÖZTÜRK", 13 kod noktası |
| 11 | örnek 8 kayıt, "yilmaz", k = 3 | YILMAZ 1, ILGAZ 3, İSMAİL 4; uzunluk farkı 4, kova 5 terimi atlar |
| 12 | ad = soyad ("CAN CAN") ve "ALİ CAN" | terim CAN: ad + soyad, 2 kayıt |
| 13 | menüde "zzzzzz" | öneri yazılmaz (eşik dışında) |

### Başlangıç noktası (öğrenciye verilenler)

- **Verilir:** kendi v2.11'iniz (ya da referans v2.11), `secim.h` ve `oneri.h` (bildirimler, sözleşmeler, sahiplik), `ornek_veri/tercihler.csv` ve `tercihler_katalog.csv`, `olcer_dp`'nin ölçüm düzeneği (aday ve sorgu üretimi, bütçe ve kestirim), v2.2'nin `secmeli` modülü, v2.4'ün `utf8_coz`'u ve v2.9'un `tr_katla`'sı, Şekil 1 ve 2'nin örnekleri.
- **Yazılır:** `secim.c` (tablo, geri çıkarma, tek satır, geri izleme, dal-sınır, açgözlü, kaba kuvvet, düğüm sayımı), `oneri.c` (Levenshtein, sözlük, en yakın k, budama), `ders_secimi.c`, menü ve `ara` bütünleştirmesi; testler (birim + kâhin); ölçüm ve yorum.
- **Değiştirilmez:** v1.0 kuralları, menünün sonuç bulan aramaları, v2.2'nin `secim_yap`'ı, v2.10'un katalog modülü, ortak modüller.
- **Meydan okuma:** (a) Levenshtein'de satırın en küçük değeri en kötü önerinin uzaklığını aşınca DP'yi erken bitirin (Ukkonen'in kesme fikri) ve § 8.4'ü tekrarlayın; (b) yukarıdan aşağıya (memoization) sırt çantası: v2.9'un karma tablosunda (i, c) durumlarını tutun, ziyaret edilen durum sayısını (n+1)(W+1) ile karşılaştırın; (c) yer değiştirmeyi (YILMAZ ↔ YLIMAZ) bir düzenleme sayan Damerau–Levenshtein uzaklığı; (d) önkoşul kısıtlı ders seçimi: aynı dönemde bir ders ancak önkoşuluyla birlikte seçilebiliyorsa problem nasıl değişir? (ağaç sırt çantası).

## 11. Bilinen sınırlılıklar

- Ders seçimi tek bir dönem içindir; aynı dönemde önkoşul ve dersi birlikte almak, ders saatlerinin çakışması (v2.11) ve zorunlu dersler modellenmez. Tercih puanları KURGUSALDIR.
- DP W ≤ 1 000 AKTS ile sınırlıdır; geri izleme, dal-sınır ve açgözlü n ≤ 64 (64 bitlik maske), kaba kuvvet n ≤ 25.
- Öneri yalnız tam ad, ad ve soyad terimlerine bakar; harf yer değiştirmesi iki düzenleme sayılır (Damerau değil); önerilen terim katlanmış (şapkasız) biçimde yazılır.
- Sözlük her menü aramasında yeniden kurulur (menü boyutları için yeterli; büyük veride sözlük saklanmalıdır — v3.0).
- Süreler paylaşılan makinede yük altında ölçüldü (§ 8.5).

## 12. Kaynaklar

- Bellman, R. (1957). *Dynamic programming*. Princeton University Press.
- Bellman, R. (1984). *Eye of the hurricane: An autobiography*. World Scientific.
- Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2022). *Introduction to algorithms* (4th ed.). MIT Press.
- Kleinberg, J., & Tardos, É. (2006). *Algorithm design*. Pearson/Addison-Wesley.
- Levenshtein, V. I. (1966). Binary codes capable of correcting deletions, insertions, and reversals. *Soviet Physics Doklady, 10*(8), 707–710.
- Wagner, R. A., & Fischer, M. J. (1974). The string-to-string correction problem. *Journal of the ACM, 21*(1), 168–173. https://doi.org/10.1145/321796.321811
